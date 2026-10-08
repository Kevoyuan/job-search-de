import json,unittest
from pathlib import Path
from scoring_policy import apply_policy,load_policy,WEIGHTS

class ScoringPolicyTests(unittest.TestCase):
    def test_reported_regression(self):
        fixture=json.loads((Path(__file__).parent.parent/'tests/fixtures/seniority_gate.json').read_text())
        for job in fixture['jobs']:
            result=apply_policy(job,load_policy(fixture['settings']))
            self.assertEqual(result['eligibility']['status'],'EXCLUDED_SENIORITY')
            self.assertEqual(result['scoreStage'],'triage')
            self.assertTrue(result['analysis']['requiredYearsEvidence'])
    def test_ranges_and_optional(self):
        policy=load_policy('[thresholds]\nmax_required_years=4')
        for text,excluded in [('3–5 years of experience',False),('5-7 years experience',True),('5+ years experience preferred',False),('5 years experience not required',False),('最多5年经验',False),('Master degree or 7 years experience',False),('Company founded 20 years ago',False),('至少7年供应链经验',True)]:
            with self.subTest(text=text):
                result=apply_policy({'jd':text},policy)
                self.assertEqual(result['eligibility']['status']=='EXCLUDED_SENIORITY',excluded)
    def test_preferences_and_management(self):
        self.assertEqual(load_policy('', '**Target Seniority:** 0–3 years')['maxRequiredYears'],3)
        policy=load_policy('[seniority]\nexclude_non_engineering_managers=true\nmanager_title_exceptions=product manager')
        for title,excluded in [('Logistics Manager',True),('Product Manager',False),('Engineering Manager',False)]:
            self.assertEqual(apply_policy({'title':title},policy)['eligibility']['status']=='EXCLUDED_MANAGEMENT',excluded)
    def test_evidence_provenance_and_gate(self):
        self.assertEqual(apply_policy({'score':92,'scoreStage':'evidence'})['scoreStage'],'unverified')
        review={'dimensions':{k:{'status':'MATCH','jobEvidence':'fixture requirement','candidateEvidence':'fixture profile evidence','reason':'fixture reasoning'} for k in WEIGHTS},'hardConstraints':[{'kind':k,'status':'MATCH','evidence':'fixture review'} for k in ('experience','language','drivingLicence')]}
        job={'scoreStage':'evidence','evidenceAssessment':review,'jd':'7+ years experience required'}
        result=apply_policy(job,{'maxRequiredYears':3})
        self.assertEqual(result['score'],100)
        self.assertEqual(result['eligibility']['status'],'EXCLUDED_SENIORITY')
        review['dimensions']['experience']['status']='UNKNOWN'
        self.assertEqual(apply_policy(job)['scoreStage'],'unverified')

if __name__=='__main__':unittest.main()
