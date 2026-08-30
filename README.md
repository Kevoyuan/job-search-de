# 🇩🇪 job-search-de — AI-Powered Job Discovery & Evaluation Pipeline

<p align="center">
  <a href="README.md"><b>English</b></a> •
  <a href="docs/README_de.md"><b>Deutsch</b></a> •
  <a href="docs/README_zh.md"><b>中文</b></a> •
  <a href="docs/README_ja.md"><b>日本語</b></a> •
  <a href="docs/README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-Ready-blue.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/Target-Germany%20AI%2FTech-emerald.svg?style=flat-square" alt="Target Market" />
  <img src="https://img.shields.io/badge/Scoring-Evidence--Based-purple.svg?style=flat-square" alt="Scoring Mode" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" />
</p>

An intelligent, candidate-neutral AI Agent skill and pipeline designed to automate the discovery, verification, two-stage evidence-based scoring, reporting, and management of tech/AI jobs across Germany.

---

## 🥊 Why `job-search-de` vs Traditional Job Boards

| Dimension | Traditional Boards (LinkedIn / StepStone / Indeed) | 🇩🇪 `job-search-de` Pipeline |
|---|---|---|
| **Listing Freshness** | 30%–50% are expired, ghost listings, or headhunter reposts | **100% Live & Verified** (Direct ATS API queries + real-time Schema.org validation) |
| **Privacy & Security** | Resumes stored on external cloud databases | **100% Local & Confidential** (Data resides strictly in local `<workdir>/.job-search/`) |
| **Match Quality** | Opaque keyword matching with false positives | **Two-Stage Evidence Scoring** (Cites exact profile facts, zero hallucinated matches) |
| **Search Management** | Manual spreadsheets and fragmented bookmarking | **Interactive 4-Theme Workbench** (Kanban, table filters, hotkeys, 1-click pitch hooks) |
| **Agent Ecosystem** | Isolated from modern AI workflows | **Native Agent Skill** (Antigravity, Claude Code, Cursor, OpenClaw ready) |

---

## 📸 Demo & Interface

### 🎨 Instant 4-Theme Switcher (0-Token Pure CSS)
> Seamlessly switch between **Notion Craft (Warm Editorial)**, **Linear Obsidian (Dark Mode)**, **Bauhaus Grid (Industrial Minimal)**, and **Bento Quartz (Spatial Glass)** with zero token consumption and instant local persistence. Press <kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> / <kbd>4</kbd> to switch instantly.

![Workbench Multi-Theme Switcher](docs/images/theme-switcher.gif)

---

### 1. Interactive Notion-Style Job Workbench (Table View)
> Live status tracking, multi-dimensional filters, freshness indicators, and calibrated fit scores.

![Workbench Table View](docs/images/workbench-table.png)

---

### 2. Application Pipeline Kanban
> Drag-and-drop or status-driven application lifecycle management (To Apply, Applied, Interview, Offer, Archived).

![Workbench Kanban View](docs/images/workbench-kanban.png)

---

### 3. Local Candidate Profile & Rule Drawer
> Candidate-neutral architecture: Personal facts, constraints, target cities, and delivery configs stay strictly in your local `.job-search/` directory.

![Workbench Config Drawer](docs/images/workbench-config-drawer.png)

---

### 4. Comprehensive Intelligence Report
> Multi-regional breakdown (Frankfurt, Munich, Berlin, Germany Remote, Stretch exceptions) with deep JD-to-Profile evidence matching.

![Intelligence Report](docs/images/report-overview.png)

---

## 🌟 Key Features

- 🎯 **Privacy-First & Candidate-Neutral**: Skill logic is strictly decoupled from candidate data. Personal background, constraints, and preferences are stored exclusively in `<workdir>/.job-search/`.
- 🎨 **4 Curated Design Themes (0-Token Pure CSS)**: Instant switching between **Notion Craft**, **Linear Obsidian (Dark Mode)**, **Bauhaus Grid**, and **Bento Quartz** with zero token overhead and local persistence.
- ⌨️ **Power Keyboard Navigation (<kbd>?</kbd>)**: Navigate via <kbd>J</kbd>/<kbd>K</kbd>, expand with <kbd>Enter</kbd>, open career links with <kbd>O</kbd>, quick search with <kbd>/</kbd>, and switch themes via <kbd>1</kbd>/<kbd>2</kbd>/<kbd>3</kbd>/<kbd>4</kbd>.
- 📋 **1-Click Tailored Pitch Hook**: Generates a professional, job-specific cover letter opening based on verified JD evidence matches and copies it directly to your clipboard.
- ⚡ **Quick Preset Filter Chips**: 1-click presets for `🔥 Fit ≥ 85`, `📍 Frankfurt Area`, `🏠 Full Remote`, `🇬🇧 English Only`, and `🎯 To Apply`.
- 🔍 **Direct ATS Discovery**: Fetches active listings directly from top ATS APIs (Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable) — bypassing outdated job aggregator scrapers.
- ⚡ **Automated Verification Pipeline**: Real-time URL health check, HTTP status validation, and Schema.org JSON-LD extraction (`datePosted`, `validThrough`, active hiring status).
- 📊 **Calibrated Two-Stage Evidence Scoring**:
  - **Stage 1 (Fast Triage)**: Instant hard exclusions, seniority filtering, and threshold pruning.
  - **Stage 2 (Deep JD-to-Profile Matching)**: Separates Required vs Preferred criteria, requiring explicit citation of verified candidate evidence (no hallucinated matches).
- 🗂️ **Interactive Notion-Style Workbench**: Pure client-side modern HTML/JS interface with Kanban board, Table view, filter presets, and optional Notion database bi-directional status sync.
- 🔄 **Runtime Version Check & Auto-Update**: Auto-checks GitHub for upstream updates and displays live version status badge (`v1.1.0`) with 1-click upgrade instructions.

---

## 🔄 Pipeline Workflow

```text
       Candidate Documents (CV, LinkedIn, Portfolio)
                          │
                          ▼
            [1. Onboarding & Extraction]
                          │ (Generates .job-search/profile.md & preferences.md)
                          ▼
             [2. Multi-Channel Discovery]
           ATS Direct Pulls + Targeted Gap-Fill
                          │
                          ▼
             [3. Normalization & Verification]
           Schema.org JSON-LD + HTTP Date Check
                          │
                          ▼
           [4. Two-Stage Evidence Scoring]
       Triage Filter ➔ JD-to-Profile Fact Matching
                          │
                          ▼
            [5. Reporting & Sync Delivery]
     Executive Report + Interactive HTML Workbench + Notion
```

---

## 📁 Repository Structure

```text
job-search-de/
├── SKILL.md                  # Agent skill entrypoint and operational rules
├── README.md                 # Primary project documentation (English)
├── VERSION                   # Semantic version definition (e.g. 1.1.0)
├── assets/
│   └── config-template/      # Configuration templates
│       ├── profile.md        # Verified candidate background template
│       ├── preferences.md    # Job search constraints & targets
│       └── settings.ini      # Scoring thresholds & date windows
├── configs/
│   ├── boards.txt            # Default ATS companies & endpoints
│   ├── keywords.txt          # Target search keywords & queries
│   └── profile.md            # Reference profile specification
├── references/
│   ├── configuration.md      # Configuration contracts & specifications
│   ├── onboarding.md         # Candidate onboarding guidelines
│   ├── resume-parser.md      # Resume evidence extraction rules
│   ├── scoring.md            # Calibrated evidence scoring rubric
│   └── workbench.md          # Workbench integration & multi-theme contract
├── scripts/
│   ├── bump_version.py       # Auto semantic version bumper
│   ├── check_update.py       # Online/offline upstream update checker
│   ├── update_skill.sh       # One-command skill updater
│   ├── download.sh           # Batch ATS API downloader
│   ├── parse_ats.py          # ATS data parser & normalizer
│   ├── verify.sh             # Job URL & metadata validator
│   ├── init_config.py        # Initialize .job-search/ templates
│   ├── build_html.sh         # Workbench packaging script
│   └── fix_html.py           # HTML report data injector
├── templates/
│   ├── agent_prompt_common.md# Standardized agent prompt blocks
│   ├── report_skeleton.md    # Executive report template
│   └── search_queries.md     # Query composition matrices
└── docs/
    ├── README_zh.md          # Chinese documentation (中文)
    ├── README_de.md          # German documentation (Deutsch)
    ├── README_ja.md          # Japanese documentation (日本語)
    ├── README_ko.md          # Korean documentation (한국어)
    └── images/               # Demo screenshots & animated theme GIF
```

---

## 🚀 Quick Start (Zero-Setup Workflow)

### 1. Install the Skill
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. Drop Your CV in Your Workspace
Place your resume or profile (e.g. `resume.pdf`, `CV.md`, or LinkedIn export) in your working folder.

### 3. Talk to Your AI Agent
Simply prompt your agent (Antigravity, Claude Code, Cursor, Codex, OpenClaw):

> **"Find active AI/ML Engineer jobs in Frankfurt, Munich, or Remote Germany that match my CV."**

```text
> 👤 User: "Find active AI/ML Engineer jobs in Frankfurt or Germany Remote matching my CV."

🤖 Agent:
[1/4] 📄 Parsed resume into local .job-search/profile.md (6 verified skills, 4 project facts)
[2/4] 🔍 Queried direct ATS APIs (Greenhouse, Lever, Ashby, Personio...) → Discovered 42 active roles
[3/4] ⚡ Verified live URLs and Schema.org posting dates (0 expired listings)
[4/4] 📊 Scored JD requirements against verified profile facts:
      • 8 High-Fit Roles (Fit ≥ 85)
      • 14 Moderate-Fit Roles (70 ≤ Fit < 85)
✨ Generated executive intelligence report & updated `job-hunt-workbench.html`!
```

<details>
<summary><b>🛠️ Advanced / Manual CLI Pipeline (Optional)</b></summary>

If you prefer running the raw scripts manually without an agent:

```bash
# Initialize local configs
python3 ~/.agents/skills/job-search-de/scripts/init_config.py --workdir .

# Download ATS listings & parse
bash ~/.agents/skills/job-search-de/scripts/download.sh --workdir .
python3 ~/.agents/skills/job-search-de/scripts/parse_ats.py --today $(date +%Y-%m-%d) --workdir .

# Verify URLs
bash ~/.agents/skills/job-search-de/scripts/verify.sh urls.txt
```
</details>

---

## ⚡ Available Commands & Shortcuts

You can trigger the following commands directly in your AI Agent conversation:

| Command | Action Description |
|---|---|
| `/refresh` | **Run Fresh Discovery**: Executes full ATS pull, live verification, two-stage evidence scoring, and updates the Workbench & Report. |
| `/update-skill` | **Auto-Update Skill**: Checks and pulls the latest upstream updates from GitHub via `npx skills update job-search-de -g`. |
| `/match <url / jd>` | **Instant JD Match**: Evaluates an ad-hoc job URL or pasted JD against verified facts in your profile. |
| `/tailor <id / url>` | **CV & Anschreiben Generator**: Produces tailored CV bullet points and German cover letter grounded in verified facts. |
| `/sync` | **Notion Sync**: Bi-directionally synchronizes application pipeline statuses with Notion Job Tracker database. |
| `/digest` | **60-Second Daily Digest**: Summarizes the top 5 high-fit fresh roles discovered in the last 24–48 hours. |

---

## 🤖 Using as an AI Agent Skill

This skill complies with the standard Agent Skill protocol (Antigravity, Claude Code, OpenClaw, Gemini CLI, Cursor, etc.).

Add it to your skill configurations:

```json
{
  "skills": [
    "~/.agents/skills/job-search-de"
  ]
}
```

When prompt-triggered (e.g., *"Find German Machine Learning Engineer jobs matching my profile in Frankfurt or Remote"*), the Agent automatically executes the full discovery-to-evaluation pipeline following `SKILL.md`.

---

## ⚙️ Privacy-First Configuration (`.job-search/`)

All candidate-specific data lives exclusively in your project root's `.job-search/` directory:

<details>
<summary><b>📂 View example <code>.job-search/preferences.md</code> & <code>settings.ini</code></b></summary>

```markdown
# Target Preferences (.job-search/preferences.md)

- **Target Roles:** Senior AI Engineer, Machine Learning Engineer, Applied AI Lead
- **Target Regions:** Frankfurt am Main, Rhine-Main Area, Germany (Full Remote)
- **Minimum Fit Score:** 75
- **Languages:** Fluent English (B2 German basic)
```

```ini
# Search Settings (.job-search/settings.ini)
[scoring]
fit_threshold = 75
require_direct_ats = true

[delivery]
workbench_language = en
auto_open_browser = true
```
</details>

---

## ❓ Frequently Asked Questions (FAQ)

<details>
<summary><b>1. Do I need paid LinkedIn or scraping API keys?</b></summary>

**No.** The pipeline connects directly to official, public ATS career endpoints (Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable) used by hiring companies, completely bypassing proprietary scrapers and paid API limits.
</details>

<details>
<summary><b>2. Is my resume or personal information uploaded to any server?</b></summary>

**No.** All parsing, evidence matching, and workbench rendering happen entirely locally within your workspace and your AI Agent session. Zero external telemetry or cloud storage is involved.
</details>

<details>
<summary><b>3. Can I customize the target cities, keywords, or language criteria?</b></summary>

**Yes.** Simply modify `.job-search/preferences.md` or `.job-search/settings.ini`. You can define custom location priorities (e.g., Munich, Berlin, Hamburg), salary expectations, or German language exemptions without touching any code.
</details>

---

## 📄 License

Distributed under the [MIT License](LICENSE).
