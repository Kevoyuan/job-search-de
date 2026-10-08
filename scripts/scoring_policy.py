"""Deterministic seniority gates and evidence-score provenance. No model calls."""
import configparser
import re
import math
from html import unescape

WEIGHTS = {'hardSkills':30, 'experience':25, 'technicalDepth':20, 'domain':10, 'education':5, 'communication':10}

def load_policy(settings='', preferences=''):
    cfg=configparser.ConfigParser(interpolation=None)
    cfg.read_string(settings or '')
    def number(section,key):
        value=cfg.get(section,key,fallback='').strip()
        if not value: return None
        n=float(value)
        if not math.isfinite(n) or n<0: raise ValueError(key+' must be non-negative')
        return n
    maximum=number('seniority','target_years_max')
    minimum=number('seniority','target_years_min')
    if maximum is None:
        m=re.search(r'target[_ ]years[_ ]max\s*[:=]\s*(\d+)',preferences,re.I)
        if m: maximum=float(m[1])
    if maximum is None:
        m=re.search(r'target seniority[^\n]*?(\d+)\s*[-–—]\s*(\d+)\s*(?:years|年|jahre)',preferences,re.I)
        if m: minimum,maximum=map(float,m.groups())
    if minimum is not None and maximum is not None and minimum>maximum: raise ValueError('target_years_min exceeds max')
    limit=number('thresholds','max_required_years')
    return {'maxRequiredYears':limit if limit is not None else maximum,
            'targetYearsMin':minimum,'targetYearsMax':maximum,
            'excludeManagers':cfg.getboolean('seniority','exclude_non_engineering_managers',fallback=False),
            'managerExceptions':[x.strip().lower() for x in cfg.get('seniority','manager_title_exceptions',fallback='product manager').split(',') if x.strip()]}

def job_text(job):
    values=[]
    for key in ('jd','jdEn','jdDe','jdZh','description','requirements','description_raw'):
        value=job.get(key,'')
        if isinstance(value,list): value='\n'.join(str(v) for v in value if isinstance(v,str))
        if isinstance(value,str) and value: values.append(value)
    text=unescape('\n'.join(values))
    text=re.sub(r'<(script|style)\b[^>]*>.*?</\1>', '', text, flags=re.I|re.S)
    return re.sub(r'<[^>]+>', '\n', text)

def requirements(job):
    items=[]
    section_level='required'
    for clause in re.split(r'[\n;；。]|(?<=[.!?])\s+',job_text(job)):
        clause=clause.strip()
        if not clause: continue
        heading=clause.strip(' #:*-').lower()
        if heading in ('preferred','preferred qualifications','nice to have','wünschenswert','加分项'): section_level='preferred'; continue
        if heading in ('required','requirements','required qualifications','must have','anforderungen','必需条件'): section_level='required'; continue
        preferred=section_level=='preferred' or bool(re.search(r'preferred|nice.to.have|a plus|ideally|wünschenswert|von vorteil|idealerweise|加分|优先',clause,re.I))
        optional=bool(re.search(r'not required|nicht erforderlich|无需|不要求',clause,re.I))
        # Experience context prevents company ages, dates and benefit durations becoming requirements.
        years=re.search(r'(\d+)\s*(?:[-–—]\s*(\d+)\s*)?\+?\s*(?:years?|jahre[n]?|年)',clause,re.I)
        experience=bool(re.search(r'experience|erfahrung|经验',clause,re.I))
        item={'text':clause,'level':'preferred' if preferred else 'mentioned' if optional else 'required', 'kind':'other'}
        if years and experience:
            item.update(kind='experience',minimum=int(years[1]),maximum=int(years[2]) if years[2] else None)
            if re.search(r'up to|bis zu|最多|不超过',clause,re.I): item['level']='mentioned'
            # Alternative qualifications need review, not an unconditional exclusion.
            if re.search(r'\bor\b|\boder\b|或',clause,re.I): item['level']='review'
        elif re.search(r'english|german|deutsch|英语|德语',clause,re.I): item['kind']='language'
        elif re.search(r'driving licen[cs]e|driver.?s licen[cs]e|führerschein|驾照',clause,re.I): item['kind']='drivingLicence'
        if item not in items: items.append(item)
    return items

def evidence_result(job):
    review=job.get('evidenceAssessment')
    if not isinstance(review,dict): return None
    dimensions=review.get('dimensions',{})
    if not isinstance(dimensions,dict): return None
    total=0
    for key,weight in WEIGHTS.items():
        item=dimensions.get(key,{})
        if not isinstance(item,dict): return None
        status=item.get('status')
        if status not in ('MATCH','PARTIAL','GAP'): return None
        if not isinstance(item.get('jobEvidence'),str) or not item['jobEvidence'].strip(): return None
        if status in ('MATCH','PARTIAL') and not (isinstance(item.get('candidateEvidence'),str) and item['candidateEvidence'].strip()): return None
        if not isinstance(item.get('reason'),str) or not item['reason'].strip(): return None
        total+=weight*{'MATCH':1,'PARTIAL':0.5,'GAP':0}[status]
    checks=review.get('hardConstraints')
    if not isinstance(checks,list) or not checks: return None
    for check in checks:
        if not isinstance(check,dict) or check.get('status') not in ('MATCH','GAP','NOT_APPLICABLE') or not check.get('evidence'): return None
    if not {'experience','language','drivingLicence'}.issubset({c.get('kind') for c in checks}): return None
    return total

def apply_policy(job, policy=None):
    result=dict(job); policy=policy or {}; analysis=dict(result.get('analysis') or {})
    items=requirements(result)
    explicit=[x for x in items if x['kind']=='experience' and x['level']=='required']
    analysis['requiredYears']=max((x['minimum'] for x in explicit),default=None)
    analysis['requiredYearsEvidence']=[x['text'] for x in explicit]
    analysis['hardRequirements']=[x for x in items if x['kind']!='other']
    result['analysis']=analysis
    reasons=[]; limit=policy.get('maxRequiredYears')
    if limit is not None and analysis['requiredYears'] is not None and analysis['requiredYears']>limit:
        reasons.append({'code':'EXCLUDED_SENIORITY','evidence':analysis['requiredYearsEvidence'],'limit':limit})
    title=str(result.get('title','')).lower()
    if policy.get('excludeManagers') and re.search(r'\bmanager\b|经理',title) and not any(x in title for x in policy.get('managerExceptions',[])) and not re.search(r'engineering|technical|software|工程|技术',title):
        reasons.append({'code':'EXCLUDED_MANAGEMENT','evidence':result.get('title','')})
    score=evidence_result(result)
    requested=result.get('scoreStage')
    if score is not None and requested=='evidence':
        result['score']=score; result['scoreStage']='evidence'
        for check in result['evidenceAssessment']['hardConstraints']:
            if check['status']=='GAP': reasons.append({'code':'EXCLUDED_HARD_REQUIREMENT','evidence':check['evidence']})
    else:
        result['scoreStage']='triage' if requested=='triage' else 'unverified'
    result['eligibility']={'status':reasons[0]['code'] if reasons else 'NOT_EXCLUDED','reasons':reasons,'policy':policy}
    return result
