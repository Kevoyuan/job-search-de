# 🇩🇪 job-search-de: Universal Job Discovery & Evaluation Skill for Germany

<p align="center">
  <a href="README.md"><b>English</b></a> •
  <a href="docs/README_de.md"><b>Deutsch</b></a> •
  <a href="docs/README_zh.md"><b>中文</b></a> •
  <a href="docs/README_ja.md"><b>日本語</b></a> •
  <a href="docs/README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-Ready-1e5e3a.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/Zero%20API%20Key-Agent--Native-emerald.svg?style=flat-square" alt="Zero API Key" />
  <img src="https://img.shields.io/badge/Compatible-Antigravity%20%7C%20Claude%20Code%20%7C%20Cursor%20%7C%20Codex%20%7C%20OpenClaw-black.svg?style=flat-square" alt="Compatible Agents" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" />
</p>

`job-search-de` is an open, candidate-neutral **AI Agent Skill** engineered to run directly inside any modern Coding Agent environment (such as Google Antigravity, Claude Code, Cursor, Codex, OpenClaw, Gemini CLI, or Windsurf).

> **Important: Agent-Native Skill, Not an API-Key Tool**  
> Unlike traditional job tools or Python scripts that ask you to provide an `OPENAI_API_KEY` or pay for third-party LLM cloud endpoints, `job-search-de` is a pure **Agent Skill**:
> - **Zero external API keys required**: Your host Coding Agent supplies the reasoning, context management, and command execution natively.
> - **Zero cloud telemetry**: All candidate resumes, constraints, and scoring matrices remain strictly in your local `<workdir>/.job-search/` directory.
> - **Works across any profession**: Supports Software Engineering, Data, Cloud/DevOps, AI/ML, Product, Marketing, Sales, Finance, HR, Operations, Design, and Consulting across Germany.

---

## Why job-search-de

| Dimension | Traditional Boards (LinkedIn / StepStone) | Typical API Scraper Scripts | `job-search-de` Agent Skill |
|---|---|---|---|
| **Setup & Credentials** | Manual accounts, captchas, ad tracking | Requires user to supply paid API keys (`OPENAI_API_KEY`) | **Zero API keys needed**; mounts as a native skill in your existing Coding Agent |
| **Listing Freshness** | 30%-50% expired, ghost listings, reposts | Scrapers break on layout changes | **100% Live & Verified** via direct ATS APIs + Schema.org date validation |
| **Data Privacy** | Resumes stored on external commercial clouds | Resumes sent to external third-party endpoints | **100% Local Confidential Sandbox** (`<workdir>/.job-search/`) |
| **Match Reliability** | Opaque keyword matching with false positives | Uncalibrated single-prompt hallucinations | **Two-Stage Evidence Scoring** citing exact facts from your profile |
| **Deliverable UI** | Web portals cluttered with ads | Terminal text dumps or static CSVs | **Interactive 4-Theme Workbench** (Kanban, table, 0-token offline CSS) |
| **Agent Integration** | Isolated from developer workflows | Standalone CLI, disconnected from agent memory | **Native Agent Protocol** (`SKILL.md`, `references/`, `templates/`) |

---

## How the Agent Executes

When loaded into your Coding Agent, you simply ask in natural language. The Agent activates `job-search-de` and executes the pipeline autonomously:

```text
User: "Find active Machine Learning Engineer jobs in Frankfurt or Germany Remote matching my CV."
                                    │
                                    ▼
Agent (Activated via job-search-de skill):
 ├── [1/5] Parse Resume & Build Facts ──► Extracts verified skills into .job-search/profile.md
 ├── [2/5] Direct ATS API Discovery ────► Queries Greenhouse, Lever, Ashby, Personio (0 aggregators)
 ├── [3/5] Live Verification ───────────► Checks HTTP status & Schema.org JSON-LD dates (filters ghost jobs)
 ├── [4/5] Two-Stage Evidence Scoring ──► Cites exact profile facts per requirement (zero hallucinated fit)
 └── [5/5] Deliver Offline Artifact ────► Compiles 4-theme interactive job-hunt-workbench.html & report
```

---

## Demo: Interactive Workbench (Agent Deliverable)

The Agent compiles and delivers a standalone, zero-token client-side HTML cockpit (`job-hunt-workbench.html`) with 4 anti-slop design themes:

### Multi-Theme Switcher (0-Token Pure CSS)
> Seamlessly switch between **Editorial Craft** (Warm Paper), **Dark Velocity** (Cybernetic Dark), **Industrial Precision** (Braun Functional Minimal), and **Spatial Quartz** (Frosted Glassmorphism). Supports numeric hotkeys (<kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> / <kbd>4</kbd>), system `color-scheme` synchronization, and full accessibility overrides (`prefers-reduced-motion` and `prefers-reduced-transparency`).

![Workbench Multi-Theme Switcher](docs/images/theme-switcher.gif)

---

### 1. Interactive Job Workbench (Table View)
> Live status tracking, multi-dimensional filters, freshness indicators, and calibrated fit scores.

![Workbench Table View](docs/images/workbench-table.png)

---

### 2. Application Pipeline Kanban
> Drag-and-drop and status-driven application lifecycle management (To Apply, Applied, Interview, Offer, Archived).

![Workbench Kanban View](docs/images/workbench-kanban.png)

---

### 3. Local Candidate Profile & Rule Drawer
> Complete candidate neutrality: Personal facts, constraints, target cities, and delivery configs stay strictly in your local `.job-search/` directory.

![Workbench Config Drawer](docs/images/workbench-config-drawer.png)

---

### 4. Comprehensive Intelligence Report
> Multi-regional breakdown (Frankfurt, Munich, Berlin, Germany Remote, Stretch exceptions) with deep JD-to-Profile evidence matching.

![Intelligence Report](docs/images/report-overview.png)

---

## Features

- **Agent-Native Architecture**: Mounts directly into your existing Coding Agent (Antigravity, Claude Code, Cursor, Codex, OpenClaw). Zero third-party API key setup.
- **Privacy-First Sandbox**: Personal background, constraints, and preferences are stored exclusively in local `<workdir>/.job-search/`.
- **4 Anti-Slop Design Themes**: Calibrated WCAG AA contrast standards across all themes (Editorial Craft, Dark Velocity, Industrial Precision, Spatial Quartz) with zero token overhead and local persistence.
- **Full Accessibility Guardrails**: Built-in `@media (prefers-reduced-motion: reduce)` to suppress looping pulses and `@media (prefers-reduced-transparency: reduce)` for solid contrast fallbacks.
- **Power Keyboard Navigation**: Full keyboard control with shortcuts cheat sheet (<kbd>?</kbd>), list traversal (<kbd>J</kbd>/<kbd>K</kbd>), details expansion (<kbd>Enter</kbd>), application link opening (<kbd>O</kbd>), search focus (<kbd>/</kbd>), and numeric theme switching (<kbd>1</kbd>/<kbd>2</kbd>/<kbd>3</kbd>/<kbd>4</kbd>).
- **1-Click Tailored Pitch Generator**: Produces a customized cover letter opening grounded in verified JD evidence matching and copies it directly to clipboard.
- **Direct ATS Discovery**: Queries active listings directly from official ATS APIs (Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable), completely bypassing outdated aggregator scrapers.
- **Automated Verification Pipeline**: Real-time URL health check, HTTP status validation, and Schema.org JSON-LD extraction (`datePosted`, `validThrough`, active hiring status).
- **Two-Stage Evidence Scoring**:
  - **Stage 1 (Triage)**: Hard exclusions, seniority matching, and threshold pruning.
  - **Stage 2 (Deep Matching)**: Separation of Required vs Preferred criteria, requiring explicit citation of verified candidate evidence (no hallucinated scores).
- **Runtime Version Check & Update**: Checks GitHub upstream silently and presents a live version badge with one-command upgrade instructions.

---

## System Architecture

> 🌐 **Explore the interactive standalone architecture diagram**: [**`docs/architecture.html`**](docs/architecture.html) (Built with [Archify](https://github.com/tt-a1i/archify) showcase profile; supports dark/light themes, relationship tracing, guided chapters, presentation mode, and vector export).

![job-search-de System Architecture](docs/images/architecture.png)

---

## Quick Start

### 1. Install as a Skill in Your Agent
Run the standard skills CLI:
```bash
npx skills add Kevoyuan/job-search-de -g
```
Or clone directly into your agent's skills path:
```bash
git clone https://github.com/Kevoyuan/job-search-de.git ~/.agents/skills/job-search-de
```

### 2. Drop Your Resume in Your Workspace
Place your resume or background document (e.g. `resume.pdf`, `CV.md`, or LinkedIn export) in your project workspace.

### 3. Prompt Your Coding Agent
In your Coding Agent (Antigravity, Claude Code, Cursor, Codex, OpenClaw), speak naturally:

> **"Find active AI/ML Engineer jobs in Frankfurt, Munich, or Remote Germany that match my CV."**

```text
> User: "Find active AI/ML Engineer jobs in Frankfurt or Germany Remote matching my CV."

Agent:
[1/4] Parsed resume into local .job-search/profile.md (6 verified skills, 4 project facts)
[2/4] Queried direct ATS APIs (Greenhouse, Lever, Ashby, Personio...) -> Discovered 42 active roles
[3/4] Verified live URLs and Schema.org posting dates (0 expired listings)
[4/4] Scored JD requirements against verified profile facts:
      • 8 High-Fit Roles (Fit >= 85)
      • 14 Moderate-Fit Roles (70 <= Fit < 85)
Generated executive intelligence report & updated job-hunt-workbench.html!
```

---

## Supported Coding Agents

This project follows open agent skill protocols and is verified to work out-of-the-box with:

- **Google Antigravity**: Place in `~/.agents/skills/` or `~/.gemini/antigravity/skills/`.
- **Anthropic Claude Code**: Install via `npx skills add Kevoyuan/job-search-de -g` or configure in `CLAUDE.md`.
- **Cursor**: Reference skill directory in project `.cursorrules` or Agent context.
- **Codex / Gemini CLI**: Standard skill folder mount.
- **OpenClaw**: Global skill discovery path.

---

## Available Commands

When interacting with your Coding Agent, you can trigger specific workflows:

| Command | Action Description |
|---|---|
| `/refresh` | **Run Fresh Discovery**: Executes full ATS pull, live verification, two-stage evidence scoring, and updates Workbench & Report. |
| `/update-skill` | **Auto-Update Skill**: Checks and pulls the latest upstream updates from GitHub via `npx skills update job-search-de -g`. |
| `/match <url / jd>` | **Instant JD Match**: Evaluates an ad-hoc job URL or pasted JD against verified facts in your profile. |
| `/tailor <id / url>` | **CV & Anschreiben Generator**: Produces tailored CV bullet points and German cover letter grounded in verified facts. |
| `/sync` | **Notion Sync**: Bi-directionally synchronizes application pipeline statuses with Notion Job Tracker database. |
| `/digest` | **60-Second Daily Digest**: Summarizes the top 5 high-fit fresh roles discovered in the last 24-48 hours. |

---

## Configuration & Local Privacy

All candidate-specific data lives exclusively in your project root's `.job-search/` directory:

<details>
<summary><b>View example <code>.job-search/preferences.md</code> & <code>settings.ini</code></b></summary>

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

## FAQ

<details>
<summary><b>1. Do I need an OpenAI, Anthropic, or other LLM API key?</b></summary>

**No.** This is an Agent Skill, not an API client script. Your existing Coding Agent (Antigravity, Claude Code, Cursor, etc.) provides all LLM reasoning, parsing, and execution. You do not need to register for any API keys or pay per token.
</details>

<details>
<summary><b>2. Do I need paid LinkedIn or scraping API keys?</b></summary>

**No.** The skill connects directly to official, public ATS career endpoints (Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable) used by hiring companies, completely bypassing proprietary scrapers and paid API limits.
</details>

<details>
<summary><b>3. Is my resume or personal information uploaded to any server?</b></summary>

**No.** All parsing, evidence matching, and workbench rendering happen entirely locally within your workspace and your AI Agent session. Zero external telemetry or cloud storage is involved.
</details>

<details>
<summary><b>4. Can I customize target cities, keywords, or language criteria?</b></summary>

**Yes.** Simply modify `.job-search/preferences.md` or `.job-search/settings.ini`. You can define custom location priorities (e.g., Munich, Berlin, Hamburg), salary expectations, or German language exemptions without touching any code.
</details>

---

## License

Distributed under the [MIT License](LICENSE).
