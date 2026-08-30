#!/usr/bin/env python3
"""job-search-de: parse downloaded ATS payloads -> filtered, deduped, freshness-classified rows with role typing.
Reads ./ats_raw/* (gh_/ab_/lv_/pj_/sr_/wd_/an_/ro_); writes ats_results.json and prints a table.
Usage: python3 parse_ats.py [--today YYYY-MM-DD] [--workdir DIR] [--keywords path/to/keywords.txt]
"""
import argparse, configparser, datetime, glob, html, json, os, re, sys
import xml.etree.ElementTree as ET

ap = argparse.ArgumentParser()
ap.add_argument('--today', default=None)
ap.add_argument('--workdir', default='.')
ap.add_argument('--keywords', default=None)
ap.add_argument('--config-dir', default=None)
args = ap.parse_args()

WORKDIR = os.path.abspath(args.workdir)
CONFIG_DIR = os.path.abspath(args.config_dir) if args.config_dir else os.path.join(WORKDIR, '.job-search')
settings = configparser.ConfigParser()
settings_path = os.path.join(CONFIG_DIR, 'settings.ini')
if os.path.isfile(settings_path):
    settings.read(settings_path, encoding='utf-8')

TODAY = datetime.date.fromisoformat(args.today) if args.today else datetime.date.today()
FRESH_DAYS = settings.getint('search', 'fresh_days', fallback=14)
CUTOFF = TODAY - datetime.timedelta(days=FRESH_DAYS)

SKILL_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
project_keywords = os.path.join(CONFIG_DIR, 'keywords.txt')
kw_path = args.keywords or (project_keywords if os.path.isfile(project_keywords)
                            else os.path.join(SKILL_ROOT, 'configs', 'keywords.txt'))

STRONG = ["ai engineer", "ai integration", "ai adoption", "ai specialist", "ai consultant",
          "ai solutions", "ai platform", "machine learning", "ml engineer", "genai",
          "generative ai", "llm", "data scientist", "deep learning", "computer vision",
          "applied scientist", "research engineer", "mlops", "artificial intelligence",
          "ki-engineer", "ki engineer", "ki-ingenieur", "ki entwickler", "data science",
          "ai/ml", "ai product", "applied ai", "agentic", "ai agent", "ai automation",
          "forward deployed", "rag engineer"]
WEAK = ["agent", "prompt", "rag", "copilot", "automation"]
EXCLUDE_TITLES = ["intern", "internship", "praktikum", "werkstudent", "working student",
                  "trainee", "phd candidate", "doctoral", "head of", "director",
                  "sap consultant", "devops engineer", "site reliability"]

ROLE_FAMILIES = {
    "agentic_ai_engineering": ["agentic", "ai agent", "agent engineer", "llm engineer", "genai engineer", "generative ai engineer", "rag engineer", "multi-agent", "autonomous agent"],
    "applied_ai": ["applied ai", "ai engineer", "ai specialist", "ai product", "ki-engineer", "ki engineer", "ki-ingenieur", "ki entwickler", "artificial intelligence engineer"],
    "ai_solutions_consulting": ["ai solutions", "ai consultant", "ai transformation", "forward deployed", "customer ai", "solution architect", "generative ai consultant"],
    "ai_automation": ["ai automation", "intelligent automation", "ai workflow", "automation engineer ai"],
    "industrial_scientific": ["industrial ai", "engineering ai", "ai4engineering", "physical ai", "scientific machine learning", "gnn", "geometric deep learning", "simulation", "digital twin"]
}

try:
    for line in open(kw_path, encoding='utf-8'):
        line_str = line.strip()
        if line_str.startswith('STRONG:'):
            STRONG = [k.strip().lower() for k in line_str.split(':', 1)[1].split(',') if k.strip()]
        elif line_str.startswith('WEAK:'):
            WEAK = [k.strip().lower() for k in line_str.split(':', 1)[1].split(',') if k.strip()]
        elif line_str.startswith('EXCLUDE_TITLES:'):
            EXCLUDE_TITLES = [k.strip().lower() for k in line_str.split(':', 1)[1].split(',') if k.strip()]
        elif line_str.startswith('ROLE_FAMILY_AGENTIC:'):
            ROLE_FAMILIES['agentic_ai_engineering'] = [k.strip().lower() for k in line_str.split(':', 1)[1].split(',') if k.strip()]
        elif line_str.startswith('ROLE_FAMILY_APPLIED_AI:'):
            ROLE_FAMILIES['applied_ai'] = [k.strip().lower() for k in line_str.split(':', 1)[1].split(',') if k.strip()]
        elif line_str.startswith('ROLE_FAMILY_SOLUTION_CONSULTING:'):
            ROLE_FAMILIES['ai_solutions_consulting'] = [k.strip().lower() for k in line_str.split(':', 1)[1].split(',') if k.strip()]
        elif line_str.startswith('ROLE_FAMILY_AUTOMATION:'):
            ROLE_FAMILIES['ai_automation'] = [k.strip().lower() for k in line_str.split(':', 1)[1].split(',') if k.strip()]
        elif line_str.startswith('ROLE_FAMILY_INDUSTRIAL:'):
            ROLE_FAMILIES['industrial_scientific'] = [k.strip().lower() for k in line_str.split(':', 1)[1].split(',') if k.strip()]
except FileNotFoundError:
    pass

DEFAULT_LOC_CITY = ["frankfurt", "eschborn", "offenbach", "darmstadt", "wiesbaden", "mainz",
            "bad homburg", "neu-isenburg", "sulzbach", "kronberg", "ruesselsheim",
            "rüsselsheim", "hanau", "aschaffenburg", "kelsterbach", "langen",
            "mörfelden", "hofheim", "oberursel", "bad soden", "dietzenbach",
            "weiterstadt", "griesheim", "frankfurt am main"]
DEFAULT_LOC_BROAD = ["germany", "deutschland", "remote", "munich", "münchen", "berlin",
             "hamburg", "stuttgart", "cologne", "köln", "düsseldorf",
             "duesseldorf", "nuremberg", "nürnberg", "karlsruhe", "heidelberg",
             "erlangen", "dresden", "leipzig", "bremen", "hannover", "bonn", "essen",
             "dortmund", "aachen", "mannheim", "wolfsburg", "ingolstadt", "ulm",
             "augsburg", "freiburg", "regensburg", "duisburg", "wuppertal", "kiel",
             "rostock", "magdeburg", "jena"]

def configured_list(key, fallback):
    if not settings.has_option('locations', key):
        return list(fallback)
    value = settings.get('locations', key)
    values = [item.strip().lower() for item in value.split(',') if item.strip()]
    return values

LOCATION_TIERS = [
    configured_list('priority_1', DEFAULT_LOC_CITY),
    configured_list('priority_2', ['remote', 'germany', 'deutschland']),
    configured_list('priority_3', ['munich', 'münchen']),
]
LOC_CITY = LOCATION_TIERS[0]
LOC_BROAD = list(dict.fromkeys(
    LOCATION_TIERS[1] + LOCATION_TIERS[2] + configured_list('broad', DEFAULT_LOC_BROAD)
))

def is_excluded(title):
    tl = title.lower()
    return any(ex in tl for ex in EXCLUDE_TITLES)

def infer_role_type(title, content=""):
    tl = (title + " " + content[:200]).lower()
    for role_type, keywords in ROLE_FAMILIES.items():
        if any(k in tl for k in keywords):
            return role_type
    if "machine learning" in tl or "ml engineer" in tl:
        return "generic_ml_engineer"
    if "data scientist" in tl or "data science" in tl:
        return "applied_data_science"
    return "applied_ai"

def title_match(t):
    if is_excluded(t):
        return False
    tl = t.lower()
    return any(k in tl for k in STRONG) or any(k in tl for k in WEAK)

def content_ai(text):
    tl = text.lower()
    return any(k in tl for k in ["machine learning", "artificial intelligence", "llm",
                                 "generative", "deep learning", "neural network",
                                 "genai", "large language", "agentic", "rag"])

def loc_match(l):
    ll = l.lower()
    return any(c in ll for c in LOC_CITY) or any(c in ll for c in LOC_BROAD)

def prio(loc):
    ll = loc.lower()
    for index, terms in enumerate(LOCATION_TIERS):
        if any(term in ll for term in terms):
            return index
    return len(LOCATION_TIERS)

out = []
def add(src, title, company, loc, workmodel, date, url, salary, extra="", source_conf="official_ats", content=""):
    if is_excluded(title):
        return
    role_type = infer_role_type(title, content)
    freshness = classify(date)
    out.append({
        "source": src,
        "discoverySource": "ats_" + src,
        "sourceConfidence": source_conf,
        "freshnessConfidence": freshness,
        "roleType": role_type,
        "title": title,
        "company": company,
        "location": loc,
        "work_model": workmodel,
        "date": str(date) if date else None,
        "url": url,
        "salary": salary,
        "extra": extra
    })

def parse_date(s):
    if s is None or s == "": return None
    try:
        if isinstance(s, (int, float)):
            v = float(s)
            if v > 1e12: return datetime.datetime.fromtimestamp(v/1000, datetime.timezone.utc).date()
            return datetime.datetime.fromtimestamp(v, datetime.timezone.utc).date()
        s2 = str(s).strip().replace("Z", "").replace("z", "")
        if "T" in s2: s2 = s2.split("T")[0]
        elif " " in s2: s2 = s2.split(" ")[0]
        if len(s2) >= 10 and s2[:4].isdigit(): return datetime.date.fromisoformat(s2[:10])
    except Exception:
        pass
    return None

def classify(d):
    if d is None: return "ACTIVE_DATE_UNKNOWN"
    if isinstance(d, str):
        d = parse_date(d)
        if d is None: return "ACTIVE_DATE_UNKNOWN"
    return "VERIFIED_FRESH" if d >= CUTOFF else "OLDER_ACTIVE"

def gh():
    for f in glob.glob(os.path.join(WORKDIR, "ats_raw/gh_*.json")):
        slug = os.path.basename(f)[3:-5]
        try: data = json.load(open(f))
        except Exception: continue
        for j in data.get("jobs", []):
            t = j.get("title") or ""; loc = (j.get("location") or {}).get("name") or ""
            if not title_match(t) or not loc_match(loc): continue
            content = j.get("content") or ""
            if not any(k in t.lower() for k in STRONG):
                if not content_ai(content): continue
            upd = j.get("updated_at") or ""
            add("greenhouse", t, j.get("company_name") or slug, loc, "", None,
                j.get("absolute_url") or "", "", "updated_at=" + upd,
                source_conf="official_ats", content=content)

def lv():
    for f in glob.glob(os.path.join(WORKDIR, "ats_raw/lv_*.json")):
        slug = os.path.basename(f)[3:-5]
        try: data = json.load(open(f))
        except Exception: continue
        if isinstance(data, dict) and data.get("error"): continue
        if not isinstance(data, list): continue
        for j in data:
            if not isinstance(j, dict): continue
            t = j.get("text") or ""
            cats = j.get("categories"); loc = ""
            if isinstance(cats, dict): loc = cats.get("location") or ""
            if isinstance(loc, list): loc = ", ".join(loc)
            if not title_match(t) or not loc_match(loc): continue
            desc = j.get("descriptionPlain") or ""
            if not any(k in t.lower() for k in STRONG):
                if not content_ai(desc): continue
            d = parse_date(j.get("createdAt"))
            sal = j.get("salaryRange") or ""
            if isinstance(sal, dict): sal = json.dumps(sal)[:150]
            add("lever", t, slug, loc, j.get("workplaceType") or "", d,
                j.get("hostedUrl") or "", sal, source_conf="official_ats", content=desc)

def ab():
    for f in glob.glob(os.path.join(WORKDIR, "ats_raw/ab_*.json")):
        org = os.path.basename(f)[3:-5]
        try: data = json.load(open(f))
        except Exception: continue
        for j in data.get("jobs", []):
            t = j.get("title") or ""; loc = j.get("location") or ""
            if not title_match(t) or not loc_match(loc): continue
            desc = j.get("descriptionHtml") or ""
            if not any(k in t.lower() for k in STRONG):
                if not content_ai(desc): continue
            d = parse_date(j.get("publishedAt"))
            comp = ""
            if j.get("compensation"): comp = json.dumps(j.get("compensation"))[:200]
            add("ashby", t, org, loc, "remote" if j.get("isRemote") else "", d,
                j.get("jobUrl") or "", comp, source_conf="official_ats", content=desc)

def pj():
    for f in glob.glob(os.path.join(WORKDIR, "ats_raw/pj_*.xml")):
        slug = os.path.basename(f)[3:-4]
        try: root = ET.parse(f).getroot()
        except Exception: continue
        for pos in root.iter("position"):
            name = pos.findtext("name") or ""; office = pos.findtext("office") or ""
            sub = pos.findtext("subcompany") or ""
            created = pos.findtext("created_at") or pos.findtext("createdAt") or ""
            pub = pos.findtext("publication_date") or pos.findtext("publishedAt") or ""
            jid = pos.findtext("id") or ""
            loc = office or sub
            if not title_match(name) or not loc_match(loc): continue
            jd = ""
            jds = pos.find("jobDescriptions")
            if jds is not None:
                for dsc in jds.iter("jobDescription"):
                    jd += " " + (dsc.findtext("name") or "") + " " + (dsc.findtext("value") or "")
            if not any(k in name.lower() for k in STRONG):
                if not content_ai(jd): continue
            d = parse_date(pub or created)
            url = "https://" + slug + ".jobs.personio.de/job/" + jid if jid else "https://" + slug + ".jobs.personio.de"
            add("personio", name, sub or slug, loc, "", d, url, "", source_conf="official_ats", content=jd)

def sr():
    for f in glob.glob(os.path.join(WORKDIR, "ats_raw/sr_*.json")):
        slug = os.path.basename(f)[3:-7]
        try: data = json.load(open(f))
        except Exception: continue
        for j in data.get("content", []):
            t = j.get("name") or ""
            lo = j.get("location") or {}
            loc = (lo.get("city") or "") + " " + (lo.get("country") or "") + (" remote" if lo.get("remote") else "")
            if not title_match(t) or not loc_match(loc): continue
            d = parse_date(j.get("releasedDate"))
            comp = (j.get("company") or {}).get("name") or slug
            jid = j.get("id") or ""
            url = "https://jobs.smartrecruiters.com/" + comp + "/" + str(jid) if jid else ""
            add("smartrecruiters", t, comp, loc, "", d, url, "", "ref=" + (j.get("ref") or ""),
                source_conf="official_ats")

def wd():
    for f in glob.glob(os.path.join(WORKDIR, "ats_raw/wd_*.json")):
        parts = os.path.basename(f)[3:-5].split("_")
        tenant, site = parts[0], parts[1]
        try: data = json.load(open(f))
        except Exception: continue
        for j in data.get("jobPostings", []):
            t = j.get("title") or ""; loc = j.get("locationsText") or ""
            if not title_match(t) or not loc_match(loc): continue
            d = parse_date(j.get("postedOn"))
            path = j.get("externalPath") or ""
            url = "https://" + tenant + ".wd3.myworkdayjobs.com/" + site + path
            add("workday", t, tenant, loc, "", d, url, "", source_conf="official_ats")

def an():
    for f in glob.glob(os.path.join(WORKDIR, "ats_raw/an_*.json")):
        try: data = json.load(open(f))
        except Exception: continue
        for j in data.get("data", []):
            t = j.get("title") or ""; loc = j.get("location") or ""
            if not title_match(t) or not loc_match(loc): continue
            tags = " ".join(j.get("tags") or [])
            desc = j.get("description") or ""
            if not any(k in t.lower() for k in STRONG):
                if not content_ai(tags + " " + desc[:500]): continue
            d = parse_date(j.get("created_at"))
            add("arbeitnow", t, j.get("company_name") or "", loc,
                "remote" if j.get("remote") else "", d, j.get("url") or "",
                "", "tags=" + tags[:80], source_conf="aggregator", content=desc)

def ro():
    f = os.path.join(WORKDIR, "ats_raw/ro.json")
    try: data = json.load(open(f))
    except Exception: return
    rows = data[1:] if isinstance(data, list) else []
    for j in rows:
        if not isinstance(j, dict): continue
        t = j.get("position") or ""; loc = j.get("location") or ""
        ll = loc.lower()
        if not ("germany" in ll or "europe" in ll or "emea" in ll or ll in ["remote", "worldwide", "anywhere", "europe timezone", "eu"]): continue
        if not title_match(t): continue
        tags = " ".join(j.get("tags") or [])
        if not any(k in t.lower() for k in STRONG):
            if not content_ai(tags): continue
        d = parse_date(j.get("date"))
        add("remoteok", t, j.get("company") or "", loc, "remote", d, j.get("url") or "", "",
            source_conf="aggregator", content=tags)

for fn in [gh, lv, ab, pj, sr, wd, an, ro]:
    try: fn()
    except Exception as e:
        print("[" + fn.__name__ + "] crash: " + type(e).__name__ + " " + str(e), file=sys.stderr)

seen = {}
for j in out:
    key = (re.sub(r"[^a-z0-9]", "", (j["company"] or "").lower())[:20],
           re.sub(r"[^a-z0-9]", "", (j["title"] or "").lower())[:30])
    if key in seen:
        prev = seen[key]
        if (prev["date"] is None and j["date"] is not None) or ("jobs.personio" in j["url"] and "jobs.personio" not in prev["url"]):
            seen[key] = j
    else:
        seen[key] = j
res = list(seen.values())
rank = {"VERIFIED_FRESH": 0, "LIKELY_FRESH": 1, "ACTIVE_DATE_UNKNOWN": 2, "OLDER_ACTIVE": 3}
res.sort(key=lambda j: (rank.get(j.get("freshnessConfidence"), 2), prio(j["location"] or ""),
                        -(datetime.date.fromisoformat(j["date"]).toordinal() if j["date"] else 0)))

with open(os.path.join(WORKDIR, "ats_results.json"), "w") as f:
    json.dump(res, f, indent=1, default=str)

print("TODAY=" + str(TODAY) + " CUTOFF=" + str(CUTOFF) +
      " FRESH_DAYS=" + str(FRESH_DAYS) + " CONFIG_DIR=" + CONFIG_DIR +
      " | TOTAL ATS MATCHES: " + str(len(res)))
for j in res:
    print(str(j.get("freshnessConfidence", "?")).ljust(20) + " | " +
          str(j.get("roleType", "?")).ljust(24) + " | " +
          str(j["date"] or "?").ljust(10) + " | " +
          j["title"][:40].ljust(40) + " | " +
          j["company"][:18].ljust(18) + " | " +
          j["location"][:22].ljust(22) + " | " +
          j["source"].ljust(12) + " | " + j["url"][:60])
