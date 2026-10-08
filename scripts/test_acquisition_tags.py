"""Acquisition stores full JD evidence and reusable tags before any UI build."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from save_job_analysis import enrich_job

ROOT=Path(__file__).resolve().parent.parent

class AcquisitionTagTests(unittest.TestCase):
    def test_saved_tags_refresh_without_losing_curated_evidence(self):
        job={'id':'stable','score':83,'status':'applied','notes':'Keep me','jd':'Python required',
             'analysis':{'industry':'Software','evidence':{'industry':'Saved employer text'},
                         'technologies':[{'name':'Bespoke SDK','requirement':'preferred','evidence':'Bespoke SDK is a plus'}]}}
        saved=enrich_job(job,'2026-10-06')
        self.assertNotIn('technologyExtractedAt',job['analysis'])
        self.assertEqual(saved['score'],83);self.assertEqual(saved['notes'],'Keep me')
        self.assertEqual(saved['analysis']['industry'],'Software')
        saved['jd']='JavaScript required'
        updated=enrich_job(saved,'2026-10-06')
        tags={t['name']:t for t in updated['analysis']['technologies']}
        self.assertNotIn('Python',tags)
        self.assertIn('JavaScript',tags);self.assertIn('Bespoke SDK',tags)
        self.assertEqual(enrich_job(updated,'2026-10-06'),updated)

    def test_ats_parser_retains_html_and_lever_requirement_sections(self):
        with tempfile.TemporaryDirectory() as folder:
            wd=Path(folder);raw=wd/'ats_raw';raw.mkdir()
            html='<p>Python required</p><script>Terraform required</script><p>K8s is a plus</p>'
            (raw/'gh_example.json').write_text(json.dumps({'jobs':[{'title':'AI Engineer','location':{'name':'Berlin'},'content':html,'absolute_url':'https://example.org/jobs/1'}]}))
            (raw/'lv_other.json').write_text(json.dumps([{'text':'AI Engineer','categories':{'location':'Munich'},'descriptionPlain':'Build intelligent products.',
                'lists':[{'text':'Requirements','content':'<li>JavaScript required</li><li>Postgres is a plus</li>'}],
                'hostedUrl':'https://example.org/jobs/2'}]))
            subprocess.run([sys.executable,str(ROOT/'scripts/parse_ats.py'),'--workdir',folder,'--today','2026-10-06'],check=True,capture_output=True)
            jobs=json.loads((wd/'ats_results.json').read_text());self.assertEqual(len(jobs),2)
            gh=next(j for j in jobs if j['source']=='greenhouse')
            self.assertEqual(gh['description_raw'],html)
            self.assertNotIn('Terraform',gh['jd'])
            tags={t['name']:t for t in gh['analysis']['technologies']}
            self.assertEqual(tags['Python']['requirement'],'required')
            self.assertEqual(tags['Kubernetes']['requirement'],'preferred')
            self.assertEqual(tags['Python']['sourceUrl'],'https://example.org/jobs/1')
            lever=next(j for j in jobs if j['source']=='lever')
            self.assertIn('Requirements',lever['jd'])
            self.assertEqual({t['name'] for t in lever['analysis']['technologies']},{'JavaScript','PostgreSQL'})

    def test_cli_preserves_wrapper_and_backs_up_original(self):
        with tempfile.TemporaryDirectory() as folder:
            file=Path(folder)/'jobs.json'
            original=json.dumps({'metadata':{'version':7},'jobs':[{'id':'a','jd':'English fluent','score':91}]})
            file.write_text(original)
            subprocess.run([sys.executable,str(ROOT/'scripts/save_job_analysis.py'),'--jobs-file',str(file),'--date','2026-10-06'],check=True,capture_output=True)
            result=json.loads(file.read_text())
            self.assertEqual(result['metadata'],{'version':7})
            self.assertEqual(result['jobs'][0]['analysis']['technologyStatus'],'language_only')
            self.assertEqual(next(Path(folder).glob('*.bak-before-tags-*')).read_text(),original)

if __name__=='__main__':unittest.main()
