"""Evidence-preserving analytics adapter. No network, inference, or fit scoring."""
import re
from occupation_rules import PROFESSIONAL_TOOLS, PROFESSIONAL_METHODS, OCCUPATION_ROLES

CITY_ALIASES = {
    'munich': 'Munich', 'münchen': 'Munich', 'muenchen': 'Munich', '慕尼黑': 'Munich',
    'berlin': 'Berlin', '柏林': 'Berlin', 'hamburg': 'Hamburg', '汉堡': 'Hamburg',
    'cologne': 'Cologne', 'köln': 'Cologne', 'koeln': 'Cologne', '科隆': 'Cologne',
    'frankfurt': 'Frankfurt', 'frankfurt am main': 'Frankfurt',
    'düsseldorf': 'Düsseldorf', 'duesseldorf': 'Düsseldorf',
    'nürnberg': 'Nuremberg', 'nuremberg': 'Nuremberg', 'stuttgart': 'Stuttgart',
    '法兰克福': 'Frankfurt', '纽伦堡': 'Nuremberg', '杜塞尔多夫': 'Düsseldorf',
    '斯图加特': 'Stuttgart', 'darmstadt': 'Darmstadt', '达姆施塔特': 'Darmstadt',
    'mainz': 'Mainz', '美因茨': 'Mainz', 'heidelberg': 'Heidelberg', '海德堡': 'Heidelberg',
    'wiesbaden': 'Wiesbaden', '威斯巴登': 'Wiesbaden', 'bad homburg': 'Bad Homburg',
    'karlsruhe': 'Karlsruhe', '卡尔斯鲁厄': 'Karlsruhe', 'aachen': 'Aachen', '亚琛': 'Aachen',
    'leipzig': 'Leipzig', '莱比锡': 'Leipzig', 'dresden': 'Dresden', '德累斯顿': 'Dresden',
    'bonn': 'Bonn', '波恩': 'Bonn', 'essen': 'Essen', 'mannheim': 'Mannheim',
}
TECH_ALIASES = {
    'k8s': 'Kubernetes', 'kubernetes': 'Kubernetes', 'javascript': 'JavaScript',
    'java': 'Java', 'typescript': 'TypeScript', 'python': 'Python', 'golang': 'Go',
    'react.js': 'React', 'reactjs': 'React', 'react': 'React', 'node.js': 'Node.js',
    'nodejs': 'Node.js', 'postgres': 'PostgreSQL', 'postgresql': 'PostgreSQL',
    'aws': 'AWS', 'amazon web services': 'AWS', 'gcp': 'Google Cloud',
    'google cloud': 'Google Cloud', 'azure': 'Azure', 'docker': 'Docker',
    'terraform': 'Terraform', 'sql': 'SQL', 'c++': 'C++', 'c#': 'C#',
    '.net': '.NET', 'rust': 'Rust', 'pytorch': 'PyTorch', 'tensorflow': 'TensorFlow',
    'fastapi': 'FastAPI', 'pydantic': 'Pydantic', 'scikit-learn': 'scikit-learn',
    'langgraph': 'LangGraph', 'langchain': 'LangChain', 'llamaindex': 'LlamaIndex',
    'crewai': 'CrewAI', 'rag': 'RAG', 'mcp': 'MCP', 'n8n': 'n8n',
    'vllm': 'vLLM', 'sglang': 'SGLang', 'tensorrt-llm': 'TensorRT-LLM',
    'cuda': 'CUDA', 'triton': 'Triton', 'cutlass': 'CUTLASS', 'langfuse': 'Langfuse',
    'pytest': 'Pytest', 'pandas': 'Pandas', 'numpy': 'NumPy', 'onnx': 'ONNX',
    'mlflow': 'MLflow', 'databricks': 'Databricks', 'snowflake': 'Snowflake',
}
# Explicit local aliases; cities remain cities, with location modes stored separately.
CITY_ALIASES.update({
    'jena':'Jena', '耶拿':'Jena', 'magdeburg':'Magdeburg', '马格德堡':'Magdeburg',
    'ulm':'Ulm', '乌尔姆':'Ulm', 'bochum':'Bochum', '波鸿':'Bochum',
    'eschborn':'Eschborn', '埃施博恩':'Eschborn', '巴特洪堡':'Bad Homburg',
    '埃森':'Essen', 'gilching':'Gilching', 'brühl':'Brühl', 'bruehl':'Brühl',
    'zürich':'Zurich', 'zurich':'Zurich', '苏黎世':'Zurich',
    'münster':'Münster', 'muenster':'Münster', 'kronberg':'Kronberg',
    'chemnitz':'Chemnitz', '开姆尼茨':'Chemnitz', 'paderborn':'Paderborn',
    'augsburg':'Augsburg', '奥格斯堡':'Augsburg', 'deggendorf':'Deggendorf',
    '德根多夫':'Deggendorf', 'hofheim':'Hofheim', '霍夫海姆':'Hofheim',
    'london':'London', '伦敦':'London', 'paris':'Paris', '巴黎':'Paris',
    'lyon':'Lyon', '里昂':'Lyon', 'vienna':'Vienna', 'wien':'Vienna', '维也纳':'Vienna',
    'dublin':'Dublin', '都柏林':'Dublin', 'hong kong':'Hong Kong', '香港':'Hong Kong',
})
TECH_GROUPS = {
 'languages': 'Python Java JavaScript TypeScript Go Rust SQL C++ C#'.split(),
 'frameworks': ['React','Node.js','.NET','FastAPI','Pydantic','scikit-learn','PyTorch','TensorFlow','Pandas','NumPy','Spring Boot','Django','Vue','Angular','Next.js'],
 'cloud': ['AWS','Google Cloud','Azure','Databricks','Snowflake','Kubernetes','Docker','Terraform','Linux','Ansible','Helm'],
 'data': ['PostgreSQL','MySQL','MongoDB','Redis','Elasticsearch','Spark','Kafka','Airflow','dbt','Flink','Hadoop','Neo4j','Qdrant','Pinecone'],
 'ai_tools': ['LangGraph','LangChain','LlamaIndex','CrewAI','vLLM','SGLang','TensorRT-LLM','CUDA','Triton','CUTLASS','Langfuse','ONNX','MLflow','Hugging Face','OpenAI API','Ollama'],
 'engineering': ['Pytest','Git','GitLab','GitHub Actions','Jenkins','n8n','WebSocket','WebRTC','REST','GraphQL','OAuth','ROS','ROS 2','ANSYS','Abaqus','CATIA','Inventor','PLC','TCP/IP','IEEE 1588','TSN','PTP'],
 'methods': ['RAG','MCP','LLM','Generative AI','AI Agents','Machine Learning','Deep Learning','Computer Vision','NLP','ASR','TTS','VAD','Fine-tuning','Prompt Engineering','MLOps','LLMOps','CI/CD','CAD','BIM','Imitation Learning','Reinforcement Learning','GNN','Data Governance','Data Engineering','Distributed Systems','Embedded Systems','Robotics','Edge Computing','Autonomous Navigation','Data Science'],
}
# Professional tools reuse the engineering group; methods remain distinct from tools.
TECH_GROUPS['engineering'].extend(n for n in PROFESSIONAL_TOOLS if n not in TECH_GROUPS['engineering'])
TECH_GROUPS['methods'].extend(n for n in PROFESSIONAL_METHODS if n not in TECH_GROUPS['methods'] and n != 'PLC')
for vocabulary in (PROFESSIONAL_TOOLS, PROFESSIONAL_METHODS):
    for name, aliases in vocabulary.items():
        for alias in aliases: TECH_ALIASES[alias] = name
TECH_CATEGORY={name:group for group,names in TECH_GROUPS.items() for name in names}
for names in TECH_GROUPS.values():
    for name in names:
        TECH_ALIASES.setdefault(name.lower(),name)
TECH_ALIASES.update({
 'apache spark':'Spark','apache kafka':'Kafka','apache airflow':'Airflow',
 'huggingface':'Hugging Face','springboot':'Spring Boot','nextjs':'Next.js',
 'vue.js':'Vue','vuejs':'Vue','ros2':'ROS 2','大语言模型':'LLM','大模型':'LLM',
 'genai':'Generative AI','生成式 ai':'Generative AI','生成式ai':'Generative AI',
 '智能体':'AI Agents','agentic ai':'AI Agents','ai agent':'AI Agents','ai agents':'AI Agents',
 'multi-agent':'AI Agents','multiagent':'AI Agents','agentic':'AI Agents',
 '机器学习':'Machine Learning','深度学习':'Deep Learning','计算机视觉':'Computer Vision',
 '自然语言处理':'NLP','语音识别':'ASR','语音合成':'TTS',
 'fine tuning':'Fine-tuning','finetuning':'Fine-tuning','微调':'Fine-tuning',
 'prompt 工程':'Prompt Engineering','提示词工程':'Prompt Engineering',
 'ci / cd':'CI/CD','ci-cd':'CI/CD','数据治理':'Data Governance',
 '数据工程':'Data Engineering','分布式系统':'Distributed Systems',
 '嵌入式':'Embedded Systems','机器人':'Robotics','模仿学习':'Imitation Learning',
 '强化学习':'Reinforcement Learning','图神经网络':'GNN','边缘计算':'Edge Computing',
 '自主导航':'Autonomous Navigation','数据科学':'Data Science','data scientist':'Data Science',
 'retrieval augmented generation':'RAG','检索增强生成':'RAG',
 'model context protocol':'MCP','llms':'LLM','large language model':'LLM','large language models':'LLM',
 'ml engineer':'Machine Learning','ai/ml':'Machine Learning','deep-learning':'Deep Learning',
 'agent orchestration':'AI Agents','agent 架构':'AI Agents','agent-orchestrierung':'AI Agents',
})


def literal_match(alias, source):
    return re.search(r'(?<![a-z0-9_+#])'+re.escape(alias)+r'(?![a-z0-9_+#])',source,re.I)


def source_text(value):
    if isinstance(value,str): return value.strip()
    if isinstance(value,list): return '\n'.join(source_text(v) for v in value if isinstance(v,(str,list)))
    return ''


def language_only(source):
    # A whole saved summary must be about language proficiency, not just mention it.
    clauses=[c.strip() for c in re.split(r'[;；\n。]',source) if c.strip()]
    language=r'英语|德语|英文|德文|english|german|deutsch|当地语言|德[/／、+ ]英|英[/／、+ ]德'
    return bool(clauses) and all(re.search(language,c,re.I) and not re.search(
        r'经验|开发|架构|工程|系统|软件|技术栈|数据|编程|experience|engineer|develop|software|technical|programming',c,re.I) for c in clauses)


def requirement_from_clause(clause):
    if re.search(r'not required|nicht erforderlich|无需|不要求|非必需',clause,re.I): return 'mentioned'
    preferred=bool(re.search(r'nice.to.have|preferred|a plus|加分|优先|wünschenswert|von vorteil',clause,re.I))
    required=bool(re.search(r'\brequired\b|\bmust\b|mandatory|必需|必须|硬性要求|erforderlich|zwingend',clause,re.I))
    return 'preferred' if preferred and not required else 'required' if required and not preferred else 'mentioned'


# Deliberately do not auto-extract ambiguous "Go", "R", "C", or "Spring".
ROLE_ALIASES = {
 'backend':'Backend','backend engineer':'Backend','backend_ai':'Backend',
 'platform / devops':'Platform / DevOps','devops':'Platform / DevOps',
 'sre / cloud':'SRE / Cloud','data engineering':'Data Engineering',
 'frontend':'Frontend','full stack':'Full Stack','fullstack':'Full Stack',
 'agentic_ai_engineer':'AI Engineering','agentic_ai_engineering':'AI Engineering',
 'applied_ai_engineer':'AI Engineering','applied_ai':'AI Engineering',
 'ai_software_engineer':'AI Engineering','ai_automation':'AI Engineering',
 'agentic_ai_multiagent':'AI Engineering','llm_rag':'AI Engineering',
 'ml_engineering_agentic':'Machine Learning','ai_ml':'Machine Learning',
 'ai_solutions_engineer':'AI Solutions Engineering','agentic_ai_solutions':'AI Solutions Engineering',
 'genai_solution':'AI Solutions Engineering','ai_solutions_consultant':'AI Consulting',
 'ai_solutions_consulting':'AI Consulting','ai_consulting':'AI Consulting',
 'conversational_ai_consulting':'AI Consulting',
 'forward_deployed_ai':'Forward Deployed Engineering',
 'forward_deployed_engineer':'Forward Deployed Engineering',
 'industrial_ai_cae':'Simulation / Graphics','engineering_ai_3d':'Simulation / Graphics',
 'industrial_scientific':'Simulation / Graphics','physical_engineering_ai':'Robotics',
 'physical_ai_engineer':'Robotics','embedded_ai_engineer':'Embedded Engineering',
 'ai_product_engineer':'Product Engineering','ai_enabler':'AI Transformation / Enablement',
 'data_scientist_ml':'Data Science','software_engineering':'Software Engineering',
}
# Specific titles precede general software/AI matches. No company-name or candidate inference.
TITLE_ROLES = [
 (r'forward[ -]deployed|\bfde\b','Forward Deployed Engineering'),
 (r'\bmlops\b|\bllmops\b|\bml[ -]operations\b|machine.learning.operations','MLOps / LLMOps'),
 (r'research.engineer|research.scientist|wissenschaftl|研发工程|研究工程|研究科学','Research / R&D'),
 (r'robot|roboticist|robotik|机器人','Robotics'),
 (r'unreal.engine|synthetic.data|simulation|仿真|图形','Simulation / Graphics'),
 (r'(?:\bai\b|\bki\b|genai|artificial intelligence|generative ai|agent).*architect|architect.*(?:\bai\b|\bki\b|genai|agent)','AI Architecture'),
 (r'(?:\bai\b|\bki\b).*?(?:transformation|enablement|enabler)|(?:transformation|enablement).*?\bai\b','AI Transformation / Enablement'),
 (r'(?:\bai\b|\bki\b|genai|agentic|artificial intelligence).*consultant|consultant.*(?:\bai\b|\bki\b|genai|agentic|artificial intelligence)','AI Consulting'),
 (r'(?:data|analytics).*consultant|consultant.*(?:data|analytics)','Data Consulting'),
 (r'solution.*architect','Solution Architecture'),
 (r'backend|back.end','Backend'),(r'frontend|front.end','Frontend'),
 (r'full.stack','Full Stack'),(r'data.scientist','Data Science'),
 (r'data.*engineer','Data Engineering'),
 (r'datenmanager|data.manager|data.governance','Data Management / Governance'),
 (r'machine.learning|\bml.engineer','Machine Learning'),
 (r'platform|devops','Platform / DevOps'),
 (r'\bsre\b|site.reliability','SRE / Cloud'),
 (r'(?:\bai\b|\bki\b|genai).*solutions?.*(?:engineer|developer)|solutions?.*(?:\bai\b|\bki\b|genai).*engineer','AI Solutions Engineering'),
 (r'(?:\bai\b|\bki\b|\bllm\b|genai|generative.ai|agentic).*?(?:engineer|developer|entwickler|specialist|expert|automation)|(?:engineer|developer|entwickler|specialist).*?(?:\bai\b|\bki\b|\bllm\b|genai|generative.ai)','AI Engineering'),
 (r'product.engineer','Product Engineering'),
 (r'application.engineer|applikationsingenieur','Application Engineering'),
 (r'embedded|firmware','Embedded Engineering'),
 (r'software.engineer|software.developer|softwareentwickler','Software Engineering'),
]


TITLE_ROLES = [(pattern, role) for pattern, role, _ in OCCUPATION_ROLES] + TITLE_ROLES


def clean(value):
    return value.strip() if isinstance(value, str) else ''


def normalize_analytics(job):
    """Preserve source fields. Put validated facets in a separate derived object."""
    raw = job.get('analysis', {})
    raw = raw if isinstance(raw, dict) else {}
    out = {'analyzedAt': clean(raw.get('analyzedAt')), 'cities': [], 'industry': None,
           'role': None, 'roleSource': None, 'technologies': [], 'workModel': None, 'evidence': {}}
    evidence = raw.get('evidence', {})
    evidence = evidence if isinstance(evidence, dict) else {}
    cities = raw.get('cities')
    if isinstance(cities, list) and clean(evidence.get('cities')):
        out['cities'] = list(dict.fromkeys(CITY_ALIASES.get(c.lower(), c) for c in map(clean, cities)
                                         if c and not re.search(r'remote|hybrid|germany|deutschland|远程', c, re.I)))
        out['evidence']['cities'] = clean(evidence['cities'])
    else:
        loc = clean(job.get('location')) or clean(job.get('loc'))
        out['cities'] = list(dict.fromkeys(canonical for alias, canonical in CITY_ALIASES.items()
                                          if (alias in loc if re.search(r'[\u4e00-\u9fff]', alias)
                                              else re.search(r'(?<!\w)' + re.escape(alias) + r'(?!\w)', loc, re.I))))
        if out['cities']:
            out['evidence']['cities'] = loc
    for field in ('industry', 'role'):
        if clean(raw.get(field)) and clean(evidence.get(field)):
            out[field] = clean(raw[field])
            out['evidence'][field] = clean(evidence[field])
            if field=='role': out['roleSource']='saved_evidence'
    if not out['role']:
        for pattern, role in TITLE_ROLES:
            if re.search(pattern, clean(job.get('title')), re.I):
                out['role'] = role
                out['evidence']['role'] = job['title']
                out['roleSource']='title_rules'
                break
    if not out['role'] and clean(job.get('roleType')):
        recorded=clean(job['roleType'])
        canonical=ROLE_ALIASES.get(recorded.lower())
        if not canonical and recorded in {role for _,role in TITLE_ROLES}:
            canonical=recorded
        if canonical:
            out['role']=canonical
            out['evidence']['role']=recorded
            out['roleSource']='roleType'
    if out['role']:
        out['role'] = ROLE_ALIASES.get(out['role'].lower(), out['role'])
    out['roleClassificationVersion']='local-role-rules-v3'
    loc = clean(job.get('location')) or clean(job.get('loc'))
    mode = clean(job.get('workModel')) or clean(job.get('mode'))
    if re.search(r'hybrid|混合', mode or loc, re.I):
        out['workModel'] = 'hybrid'
    elif re.search(r'remote|远程', mode or loc, re.I):
        out['workModel'] = 'remote'
    elif re.search(r'on.?site|现场|现场办公|vor ort', mode or loc, re.I):
        out['workModel'] = 'onsite'
    technologies = raw.get('technologies', [])
    technologies = technologies if isinstance(technologies, list) else []
    by_name = {}
    for item in technologies:
        if not isinstance(item, dict) or not clean(item.get('name')) or not clean(item.get('evidence')):
            continue
        name = clean(item['name'])
        name = TECH_ALIASES.get(name.lower(), name)
        requirement = item.get('requirement')
        requirement = requirement if requirement in ('required', 'preferred', 'mentioned') else 'mentioned'
        existing = by_name.get(name.casefold())
        rank = {'required': 3, 'preferred': 2, 'mentioned': 1}
        if not existing or rank[requirement] > rank[existing['requirement']]:
            by_name[name.casefold()] = dict(name=name, requirement=requirement, evidence=clean(item['evidence']))
            for field in ('sourceField','sourceUrl','extractionMethod'):
                if clean(item.get(field)): by_name[name.casefold()][field]=clean(item[field])
    # Read only stored job-side evidence. Candidate strengths/gaps are never sources.
    description_fields=('jd','jdZh','jdEn','jdDe','description','requirements','skills','techStack')
    descriptions=[source_text(job.get(field)) for field in description_fields]
    for field in ('title',)+description_fields:
        source=source_text(job.get(field))
        for alias,name in TECH_ALIASES.items():
            match=literal_match(alias,source)
            if not match: continue
            clause=next((c.strip() for c in re.split(r'[;；\n。]',source) if literal_match(alias,c)),source)
            requirement='mentioned' if field=='title' else requirement_from_clause(clause)
            existing=by_name.get(name.casefold())
            rank={'required':3,'preferred':2,'mentioned':1}
            if not existing or rank[requirement]>rank[existing['requirement']]:
                by_name[name.casefold()]=dict(name=name,requirement=requirement,evidence=clause,sourceField=field,extractionMethod='local_rules')
    for tech in by_name.values():
        tech['category']=TECH_CATEGORY.get(tech['name'],'other')
    out['technologies']=list(by_name.values())
    out['technologyGroups']=list(dict.fromkeys(t['category'] for t in out['technologies']))
    description='\n'.join(filter(None,descriptions))
    out['technologyStatus']=('specific' if any(t['category']!='methods' for t in out['technologies']) else
        'direction_only' if out['technologies'] else 'no_description' if not description else
        'language_only' if language_only(description) else 'unidentified')
    out['extractionVersion']='local-rules-v3'
    out['track'],out['trackEvidence'],out['trackSource']=classify_track(job,out['role'])
    out['trackClassificationVersion']='local-track-rules-v2'
    # Location qualifiers are not cities. Expose them as explicitly named filter tags.
    remote=bool(re.search(r'remote|远程|home.?office',loc,re.I)) or bool(re.search(r'remote|远程',mode,re.I))
    multiple=len(out['cities'])>1 or bool(re.search(r'多地|多市|多个城市|\d+\s*地之一|multiple.locations|multi.location|mehrere.standorte|verschiedene.standorte',loc,re.I))
    out['locationTags']=out['cities'].copy()
    if remote: out['locationTags'].append('__location_remote__')
    if multiple: out['locationTags'].append('__location_multiple__')
    if not out['locationTags']:
        if loc:
            # Keep a region or an unrecognized stored place visible verbatim, not fabricated.
            out['locationTags']=['__location_recorded__:'+loc]
            out['locationStatus']='recorded'
        else:
            out['locationStatus']='not_recorded'
    else: out['locationStatus']='identified'
    out['evidence']['location']=loc or mode
    return out

TRACKS = ('Software & Python','General Engineering','AI / GenAI & LLM',
          'Data & Analytics','Tech Consulting','Validation & QA',
          'Smart Energy & IoT','Acoustics & Audio DSP','Other / Needs review')

TRACKS = tuple(dict.fromkeys(TRACKS + tuple(track for _, _, track in OCCUPATION_ROLES)))

def classify_track(job, role=None):
    """One evidence-backed direction per job; broad engineering is a valid category."""
    raw=job.get('analysis') if isinstance(job.get('analysis'),dict) else {}
    evidence=raw.get('evidence') if isinstance(raw.get('evidence'),dict) else {}
    if raw.get('track') in TRACKS and clean(evidence.get('track')) and raw.get('trackExtractionMethod')!='local_track_rules':
        return raw['track'],evidence['track'],'saved_evidence'
    title=clean(job.get('title'))
    for pattern, occupation, track in OCCUPATION_ROLES:
        if re.search(pattern,title,re.I) or role == occupation:
            return track,title or clean(job.get('roleType')),'local_track_rules'
    specific=[
      (r'acoustic|audio|\bdsp\b|sound|akustik|声学|音频','Acoustics & Audio DSP'),
      (r'validation|verification|quality.assurance|\bqa\b|test.engineer|testingenieur|测试|验证','Validation & QA'),
      (r'\biot\b|smart.energy|smart.grid|energy.engineer|energy.system|energietechnik|能源|物联网','Smart Energy & IoT'),
      (r'consultant|consulting|berater|beratung|咨询','Tech Consulting'),
      (r'\bdata\b|analytics|daten|数据|分析','Data & Analytics'),
      (r'\bai\b|\bki\b|genai|\bllm\b|\bml\b|machine.learning|deep.learning|artificial.intelligence|generative.ai|agentic|robot.learning|人工智能|机器学习|大模型|智能体','AI / GenAI & LLM'),
      (r'software|python|backend|back.end|frontend|front.end|full.stack|web.develop|developer|entwickler|软件|后端|前端|全栈','Software & Python'),
    ]
    for pattern,track in specific:
        if re.search(pattern,title,re.I): return track,title,'local_track_rules'
    role_tracks={
      'AI Engineering':'AI / GenAI & LLM','Machine Learning':'AI / GenAI & LLM','AI Architecture':'AI / GenAI & LLM',
      'AI Transformation / Enablement':'AI / GenAI & LLM','AI Solutions Engineering':'AI / GenAI & LLM',
      'MLOps / LLMOps':'AI / GenAI & LLM','AI Consulting':'Tech Consulting','Data Consulting':'Tech Consulting',
      'Data Engineering':'Data & Analytics','Data Science':'Data & Analytics','Data Management / Governance':'Data & Analytics',
      'Software Engineering':'Software & Python','Backend':'Software & Python','Frontend':'Software & Python',
      'Full Stack':'Software & Python','Platform / DevOps':'Software & Python','SRE / Cloud':'Software & Python',
    }
    if role in role_tracks:return role_tracks[role],title or clean(job.get('roleType')),'local_track_rules'
    if re.search(r'engineer|engineering|ingenieur|roboticist|scientist|工程|研发|研究',title,re.I):
        return 'General Engineering',title,'local_track_rules'
    # For a generic title, consult only stored job-side description, never candidate text.
    description=source_text(job.get('jd')) or source_text(job.get('description'))
    for pattern,track in specific:
        match=re.search(pattern,description,re.I)
        if match:
            return track,description[max(0,match.start()-80):match.end()+160],'local_track_rules'
    return 'Other / Needs review',title or 'No saved title/description','local_track_rules'
