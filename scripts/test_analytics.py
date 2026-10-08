"""Analytics data contracts: evidence, aliases, legacy data, privacy, and generation."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from analytics_data import normalize_analytics
from build_workbench import normalize_job, safe_json_for_script


class AnalyticsTests(unittest.TestCase):
    def test_city_and_technology_aliases_are_deduplicated(self):
        job = {'location':'München / Munich / Remote, Germany', 'jd':'JavaScript and Java, K8s, Kubernetes; PostgreSQL',
               'analysis':{'technologies':[{'name':'K8s','requirement':'preferred','evidence':'Nice to have K8s'},
                                            {'name':'Kubernetes','requirement':'required','evidence':'Required Kubernetes'}]}}
        a = normalize_analytics(job)
        self.assertEqual(a['cities'], ['Munich'])
        tech = {t['name']:t for t in a['technologies']}
        self.assertEqual(tech['Kubernetes']['requirement'], 'required')
        self.assertIn('Java', tech)
        self.assertIn('JavaScript', tech)
        self.assertEqual(len(tech), 4)
        self.assertEqual(normalize_analytics({'jd':'JavaScript'})['technologies'][0]['name'], 'JavaScript')
        self.assertEqual(normalize_analytics({'location':'Remote, Germany'})['cities'], [])
        chinese = normalize_analytics({'location':'德国法兰克福混合办公','jd':'使用Python开发，非JavaScript工程'})
        self.assertEqual(chinese['cities'], ['Frankfurt'])
        self.assertIn('Python', [t['name'] for t in chinese['technologies']])

    def test_no_candidate_text_or_unsubstantiated_facets(self):
        a = normalize_analytics({'reason':'I use Java', 'gap':'Missing Python', 'analysis':{
            'industry':'Finance', 'role':'Backend', 'technologies':[{'name':'SQL'}]}})
        self.assertEqual(a['technologies'], [])
        self.assertIsNone(a['industry'])
        self.assertIsNone(a['role'])
        self.assertEqual(normalize_analytics({'workModel':'Hybrid / Remote'})['workModel'], 'hybrid')

    def test_source_preservation_and_malformed_inputs(self):
        job = {'id':'old','fit':89,'loc':'Berlin','analysis':{'technologies':True}}
        before = copy.deepcopy(job)
        result = normalize_job(job)
        self.assertEqual(job,before)
        self.assertEqual(result['score'],89)
        self.assertEqual(result['analytics']['technologies'],[])
        for invalid in [None, [], 1, True, 'bad']:
            normalize_analytics({'analysis':invalid})
        self.assertNotIn('</script>',safe_json_for_script({'evidence':'</script><img src=x>'}))

    def test_location_modes_are_explicit_without_becoming_cities(self):
        remote=normalize_analytics({'loc':'全德远程','mode':'Remote'})
        self.assertEqual(remote['cities'],[])
        self.assertEqual(remote['locationTags'],['__location_remote__'])
        multi=normalize_analytics({'location':'München / Berlin / Remote'})
        self.assertEqual(set(multi['cities']),{'Munich','Berlin'})
        self.assertIn('__location_multiple__',multi['locationTags'])
        self.assertIn('__location_remote__',multi['locationTags'])
        self.assertEqual(normalize_analytics({'location':'多地'})['locationTags'],['__location_multiple__'])
        self.assertEqual(normalize_analytics({'location':'耶拿'})['cities'],['Jena'])
        region=normalize_analytics({'location':'Rhein-Main region'})
        self.assertEqual(region['locationStatus'],'recorded')
        self.assertEqual(region['cities'],[])
        self.assertEqual(normalize_analytics({})['locationStatus'],'not_recorded')

    def test_technical_detail_and_missing_reasons_are_not_conflated(self):
        self.assertEqual(normalize_analytics({})['technologyStatus'],'no_description')
        self.assertEqual(normalize_analytics({'jd':'英语流利；德语 C1（硬性要求）'})['technologyStatus'],'language_only')
        self.assertEqual(normalize_analytics({'jd':'德/英'})['technologyStatus'],'language_only')
        self.assertEqual(normalize_analytics({'jd':'Design proprietary workflow tooling.'})['technologyStatus'],'unidentified')
        methods=normalize_analytics({'jd':'生产级大语言模型与智能体；语音识别'})
        self.assertEqual(methods['technologyStatus'],'direction_only')
        self.assertEqual(set(t['name'] for t in methods['technologies']),{'LLM','AI Agents','ASR'})
        specific=normalize_analytics({'requirements':['Python required','K8s is a plus','Spark; WebRTC']})
        tags={t['name']:t for t in specific['technologies']}
        self.assertEqual(specific['technologyStatus'],'specific')
        self.assertEqual(tags['Python']['category'],'languages')
        self.assertEqual(tags['Spark']['category'],'data')
        self.assertEqual(tags['Kubernetes']['requirement'],'preferred')
        self.assertEqual(tags['Python']['requirement'],'required')
        self.assertEqual(tags['WebRTC']['category'],'engineering')
        self.assertEqual(normalize_analytics({'jd':'Python not required'})['technologies'][0]['requirement'],'mentioned')
        self.assertEqual(normalize_analytics({'reason':'Python and Spark experience'})['technologies'],[])

    def test_role_categories_cover_real_titles_without_forcing_unknown_titles(self):
        titles={
          'Founding Research Engineer or Research Scientist':'Research / R&D',
          'Application Engineer (f/m/d)':'Application Engineering',
          'Software Engineer - Roboticist':'Robotics',
          'Junior Data & Analytics Consultant (m/f/d)':'Data Consulting',
          'Junior Software Engineer (BSA2A initiative)':'Software Engineering',
          'Enterprise AI Transformation Lead, DACH':'AI Transformation / Enablement',
          'AI Enablement Lead [gn] Data Intelligence':'AI Transformation / Enablement',
          'AI Developer (m/w/d)':'AI Engineering',
          'KI-Entwickler (m/w/d)':'AI Engineering',
          'AI Architect':'AI Architecture',
          'Robot Learning Engineer':'Robotics',
          'AI (Senior) Developer (m/w/d)':'AI Engineering',
          'AI Specialist / AI Expert':'AI Engineering',
          'ML Operations Engineer (m/w/d)':'MLOps / LLMOps',
          'Senior MLOps / LLMOps Engineer':'MLOps / LLMOps',
          'Senior Unreal Engine Developer – Synthetic Data & AI Simulation':'Simulation / Graphics',
          'Senior Consultant in Agentic & Artificial Intelligence':'AI Consulting',
        }
        for title,role in titles.items():
            a=normalize_analytics({'title':title})
            self.assertEqual(a['role'],role,title)
            self.assertEqual(a['evidence']['role'],title)
        self.assertEqual(normalize_analytics({'roleType':'agentic_ai_engineer'})['role'],'AI Engineering')
        self.assertEqual(normalize_analytics({'roleType':'ai_ml'})['role'],'Machine Learning')
        self.assertIsNone(normalize_analytics({'title':'Opportunity','reason':'AI Engineer'})['role'])
        self.assertEqual(normalize_analytics({'title':'Robot Learning Engineer','roleType':'ai_ml'})['role'],'Robotics')
        self.assertIsNone(normalize_analytics({'title':'Opportunity','roleType':'general_match'})['role'])
        curated=normalize_analytics({'title':'AI Engineer','analysis':{'role':'Research / R&D','evidence':{'role':'Verified research responsibilities'}}})
        self.assertEqual(curated['role'],'Research / R&D')

    def test_track_breakdown_broad_directions_are_exclusive(self):
        examples={'Python Software Engineer':'Software & Python','Mechanical Engineer':'Mechanical & Manufacturing',
          'AI / GenAI Engineer':'AI / GenAI & LLM','Data Analyst':'Data & Analytics',
          'Technical Consultant':'Tech Consulting','Validation Engineer':'Validation & QA',
          'Smart Energy & IoT Engineer':'Smart Energy & IoT','Acoustics and Audio DSP Engineer':'Acoustics & Audio DSP'}
        for title,track in examples.items():
            self.assertEqual(normalize_analytics({'title':title})['track'],track)
        self.assertEqual(normalize_analytics({'title':'Unknown vacancy','reason':'Python developer'})['track'],'Other / Needs review')

    def test_demo_is_explicit_and_cannot_embed_private_config(self):
        root = Path(__file__).resolve().parent.parent
        with tempfile.TemporaryDirectory() as folder:
            wd = Path(folder)
            (wd/'.job-search').mkdir()
            (wd/'.job-search/profile.md').write_text('PRIVATE_SENTINEL')
            (wd/'verified_jobs.json').write_text('[]')
            command=[sys.executable,str(root/'scripts/build_workbench.py'),'--workdir',folder,'--no-update-check']
            subprocess.run(command,check=True,capture_output=True)
            html=(wd/'job-hunt-workbench.html').read_text()
            self.assertIn('const RAW_JOBS = [];',html)
            self.assertIn('const DEMO_MODE = false;',html)
            self.assertNotIn('SAMPLE_JOBS',html)
            subprocess.run(command+['--demo'],check=True,capture_output=True)
            demo=(wd/'job-hunt-workbench.html').read_text()
            self.assertNotIn('PRIVATE_SENTINEL',demo)
            self.assertIn('const DEMO_MODE = true;',demo)
            self.assertNotIn('__ANALYTICS_',demo)


if __name__ == '__main__':
    unittest.main()
