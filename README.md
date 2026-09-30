# 🇩🇪 job-search-de

Find jobs in Germany, compare them with your CV, and track applications in a browser workbench. Works across professions as a skill for your AI coding agent.

[English](README.md) · [Deutsch](docs/README_de.md) · [中文](docs/README_zh.md) · [日本語](docs/README_ja.md) · [한국어](docs/README_ko.md)

## Quick start

You need an AI agent that can load skills and run commands, internet access, and Python 3. The installer below also needs Node.js/npm (`npx`). This skill requires no additional LLM API key; your agent's usual costs still apply.

### 1. Install

```bash
npx skills add Kevoyuan/job-search-de -g
```

Select your agent in the installer. If the skill does not appear, restart the agent or open a new session.

<details>
<summary>Manual installation</summary>

Clone into your agent's skill directory. For agents that read `~/.agents/skills/`:

```bash
git clone https://github.com/Kevoyuan/job-search-de.git ~/.agents/skills/job-search-de
```

If your agent uses a different directory, change the destination accordingly.

</details>

### 2. Provide your CV

Open a folder for your job search in your agent. Attach your CV or give its file path, such as `./resume.pdf` or `./CV.md`.

No CV ready? Describe your experience and preferences. You can also request job leads first, without personal match scores.

### 3. Ask the agent

Copy this and replace the role and locations:

```text
Use job-search-de. My CV is at ./resume.pdf.
Find software engineer jobs in Berlin or remote within Germany.
Prioritize English-speaking roles posted in the last 14 days.
Generate a match report and a job workbench in English.
```

The agent extracts your background, asks for missing preferences, searches company hiring pages, checks availability and dates, and compares requirements with evidence from your CV.

## What you get

- **Job shortlist:** official application links, locations, and freshness labels. Missing dates are marked as unknown.
- **Match report:** strengths, gaps, and supporting CV evidence.
- **Browser workbench:** open the generated `job-hunt-workbench.html` to filter jobs, switch between table and kanban views, and track applications. Includes four themes and Chinese, English, and German interfaces.

![Job workbench](docs/images/workbench-table.png)

The skill does not submit applications or contact employers without your explicit authorization.

## Everyday use

Ask in plain language, or use these shortcuts in your agent chat after loading the skill. They are not terminal commands; if your agent reserves slash commands, use the plain-language request instead.

| You want to… | Ask or type |
|---|---|
| Find new jobs | `/refresh` or “Find new jobs using my saved preferences.” |
| Check one job | `/match <job URL or pasted description>` |
| Tailor application materials | `/tailor <job ID or URL>` |
| Review recent matches | `/digest` |
| Update the skill | `/update-skill`, or run `npx skills update job-search-de -g` in a terminal |
| Sync with Notion | `/sync` — requires a configured Notion integration. |

## Change your preferences

Tell the agent what to change, for example:

> Search Munich too, exclude senior roles, and change the workbench to German.

The agent stores your profile and preferences in `.job-search/` inside your job-search folder. You do not need to edit these files manually.

| File | Purpose |
|---|---|
| `profile.md` | Verified experience, skills, and qualifications |
| `preferences.md` | Roles, cities, languages, and exclusions |
| `settings.ini` | Search windows, score thresholds, and output languages |

For manual settings and optional company/keyword lists, see the [configuration guide](references/configuration.md).

## Keep the skill up to date

The workbench checks for new releases when it is built and again when you open it. If a newer version exists, a banner appears at the top with a copy button for either update path. Open the **Usage Guide** (the book icon in the header, or press `G`) to see your installed version, re-check manually, and copy the commands.

In your agent chat:

```text
/update-skill
```

Or straight from a terminal:

```bash
npx skills update job-search-de -g
```

To check the published version without updating:

```bash
python3 scripts/check_update.py
```

## Data and privacy

Profile and configuration files are stored locally. Your AI agent may process CV content through its model provider, depending on its settings. Job discovery needs internet access; optional Notion sync sends selected data to Notion.

Availability checks reflect the time of the search and cannot guarantee that a job stays open.

## More details

- [Skill workflow and commands](SKILL.md)
- [How matching is scored](references/scoring.md)
- [Interactive architecture diagram](docs/architecture.html) — download and open in a browser
- [MIT License](LICENSE)
