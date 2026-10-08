import unittest
from analytics_data import normalize_analytics

class OccupationTests(unittest.TestCase):
    def test_multilingual_professions_and_tools(self):
        cases=[
          ('机械设计工程师','必须熟悉 SolidWorks、有限元分析','Mechanical Engineering','SolidWorks'),
          ('Elektroingenieur','TIA Portal erforderlich; EPLAN von Vorteil','Electrical Engineering','TIA Portal'),
          ('Bauingenieur','Revit und AutoCAD','Civil Engineering','Revit'),
          ('Bilanzbuchhalter','DATEV und IFRS','Accounting / Audit','DATEV'),
          ('Marketing Manager','Google Analytics, GA4 and HubSpot','Marketing','Google Analytics'),
          ('Laboratory Technician','HPLC and good clinical practice','Laboratory Science','HPLC'),
          ('采购专员','供应链管理、SAP MM','Supply Chain / Logistics','SAP MM'),
          ('Pflegefachkraft','Patientenversorgung und HL7','Nursing','HL7'),
          ('UX Designer','Figma; 用户研究','Design / UX','Figma'),
          ('Recruiter','Personio','Human Resources','Personio'),
        ]
        for title,description,role,tool in cases:
            with self.subTest(title=title):
                a=normalize_analytics(dict(title=title,description=description))
                self.assertEqual(a['role'],role)
                self.assertIn(tool,[t['name'] for t in a['technologies']])
                self.assertNotEqual(a['track'],'Other / Needs review')
                self.assertTrue(all(t['evidence'] for t in a['technologies']))
    def test_aliases_requirements_and_no_invented_tools(self):
        a=normalize_analytics(dict(title='Electrical Engineer',description='TIA Portal required; EPLAN preferred; Google Analytics / GA4'))
        tags={t['name']:t for t in a['technologies']}
        self.assertEqual(tags['TIA Portal']['requirement'],'required')
        self.assertEqual(tags['EPLAN']['requirement'],'preferred')
        self.assertEqual(sum(t['name']=='Google Analytics' for t in a['technologies']),1)
        self.assertEqual(normalize_analytics(dict(title='Accountant',description='English fluent'))['technologies'],[])
        self.assertEqual(normalize_analytics(dict(title='Assistant',description='English fluent',strengths='AutoCAD HPLC'))['technologies'],[])
        names=[t['name'] for t in normalize_analytics(dict(description='good clinical practice; JavaScript; excelled'))['technologies']]
        self.assertNotIn('Google Cloud',names)
        self.assertNotIn('Java',names)
        self.assertNotIn('Excel',names)

if __name__=='__main__': unittest.main()
