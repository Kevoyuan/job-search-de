#!/usr/bin/env python3
"""Persist local technology tags and job categories alongside saved job evidence."""
import argparse
import copy
import datetime
import json
import os
from pathlib import Path
import tempfile
from analytics_data import normalize_analytics
from scoring_policy import apply_policy, load_policy


def enrich_job(job, extracted_at, policy=None):
    if not isinstance(job, dict):
        raise ValueError('Each job must be a JSON object')
    result = copy.deepcopy(job)
    existing = result.get('analysis', {})
    if not isinstance(existing, dict):
        raise ValueError('analysis must be an object; refusing to replace existing data')
    analysis = copy.deepcopy(existing)
    # Re-extract generated tags when stored descriptions change, keeping curated evidence.
    extraction_input=copy.deepcopy(result)
    tags=analysis.get('technologies',[])
    if isinstance(tags,list):
        extraction_input.setdefault('analysis',{})['technologies']=[t for t in tags if not isinstance(t,dict) or t.get('extractionMethod')!='local_rules']
    if analysis.get('roleExtractionMethod') in ('title_rules','roleType'):
        extraction_input['analysis'].pop('role',None)
        extraction_input['analysis'].setdefault('evidence',{}).pop('role',None)
    derived = normalize_analytics(extraction_input)
    analysis['role']=derived['role']
    analysis.setdefault('evidence',{})['role']=derived['evidence'].get('role','')
    analysis['roleExtractionMethod']=derived['roleSource']
    analysis['roleClassificationVersion']=derived['roleClassificationVersion']
    analysis['roleClassifiedAt']=extracted_at
    analysis['track']=derived['track']
    analysis['evidence']['track']=derived['trackEvidence']
    analysis['trackExtractionMethod']=derived['trackSource']
    analysis['trackClassificationVersion']=derived['trackClassificationVersion']
    analysis['trackClassifiedAt']=extracted_at
    technologies = derived['technologies']
    for tag in technologies:
        tag.setdefault('sourceUrl', result.get('url', ''))
        tag.setdefault('extractionMethod','saved_evidence')
    analysis.update(technologies=technologies,
                    technologyGroups=derived['technologyGroups'],
                    technologyStatus=derived['technologyStatus'],
                    technologyExtractionVersion=derived['extractionVersion'],
                    technologyExtractedAt=extracted_at)
    result['analysis'] = analysis
    return apply_policy(result, policy)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs-file', required=True)
    ap.add_argument('--output', help='Write a separate file; default updates input with a backup')
    ap.add_argument('--date', default=datetime.datetime.now(datetime.timezone.utc).date().isoformat())
    args = ap.parse_args()
    datetime.date.fromisoformat(args.date)
    source = Path(args.jobs_file).resolve()
    original = source.read_bytes()
    data = json.loads(original)
    jobs = data if isinstance(data, list) else data.get('jobs') if isinstance(data, dict) else None
    if not isinstance(jobs, list):
        raise ValueError('Expected a job list or an object containing a jobs list')
    config_dir = source.parent / '.job-search'
    read_config = lambda name: (config_dir / name).read_text() if (config_dir / name).exists() else ''
    policy = load_policy(read_config('settings.ini'), read_config('preferences.md'))
    enriched = [enrich_job(job, args.date, policy) for job in jobs]
    if isinstance(data, list):
        data = enriched
    else:
        data['jobs'] = enriched
    output = Path(args.output).resolve() if args.output else source
    if output == source:
        backup = source.with_name(source.name + '.bak-before-tags-' + datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
        backup.write_bytes(original)
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=output.parent, delete=False) as handle:
        temporary = handle.name
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write('\n')
    try:
        os.replace(temporary, output)
    finally:
        if os.path.exists(temporary): os.unlink(temporary)
    print(f'Saved technology tags and job categories for {len(enriched)} jobs: {output}')


if __name__ == '__main__':
    main()
