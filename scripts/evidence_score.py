#!/usr/bin/env python3
"""Prepare a requirement review or validate and score an explicit evidence assessment."""
import argparse,json
from pathlib import Path
from scoring_policy import requirements,apply_policy,load_policy,WEIGHTS

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--job',required=True,help='Single job JSON object')
    parser.add_argument('--settings'); parser.add_argument('--preferences')
    parser.add_argument('--review',help='Completed evidenceAssessment JSON; omit to prepare a review')
    parser.add_argument('--output',required=True)
    args=parser.parse_args()
    job=json.loads(Path(args.job).read_text())
    policy=load_policy(Path(args.settings).read_text() if args.settings else '',Path(args.preferences).read_text() if args.preferences else '')
    if args.review:
        job['evidenceAssessment']=json.loads(Path(args.review).read_text());job['scoreStage']='evidence'
        result=apply_policy(job,policy)
        if result['scoreStage']!='evidence': parser.error('Incomplete evidence review: UNKNOWN and missing evidence cannot produce a final score')
    else:
        result={'requirements':requirements(job),'eligibility':apply_policy(job,policy)['eligibility'],
          'dimensions':{key:{'status':'UNKNOWN','jobEvidence':'','candidateEvidence':'','reason':''} for key in WEIGHTS},
          'hardConstraints':[{'kind':kind,'status':'UNKNOWN','evidence':''} for kind in ('experience','language','drivingLicence')]}
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
if __name__=='__main__':main()
