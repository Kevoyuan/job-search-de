---
name: job-search-de
description: Universal AI Agent pipeline for discovering, verifying, evidence-scoring, reporting, and managing jobs across Germany for ANY profession (Tech, Software, Data, AI/ML, Marketing, Sales, Finance, HR, Operations, Design, Consulting). Fully candidate-neutral and configurable via local .job-search/ directory.
---

# job-search-de — Universal German Job-Search & Evaluation Pipeline

This skill is a universal, candidate-neutral search and evaluation engine for all professional domains across Germany (Tech, Software, Data, AI/ML, Marketing, Sales, Finance, HR, Operations, Design, Consulting). It does not store any candidate-specific profile inside the skill directory. Each user or project keeps its background and preferences under `.job-search/` in the active working directory.

```text
Project configuration
        ↓
Discover → Verify → Triage → Evidence Score → Report → Delivery
```

## 0. Pre-flight & Version Check

Before running job discovery, evaluation, or workbench tasks:

1. Run `python3 scripts/check_update.py`.
2. If a new version is available, inform the user with a concise 1-line update reminder:
   `💡 job-search-de update available (v{remote}). Type /update-skill to upgrade.`
3. Continue executing the user's requested action without blocking.

## 1. Candidate onboarding and configuration

Check the active working directory for:

- `.job-search/profile.md`: verified candidate facts and evidence; scoring and advice may claim only what this file supports.
- `.job-search/preferences.md`: target roles, locations, work modes, language constraints, exclusions, exceptions, and delivery preferences.
- `.job-search/settings.ini`: deterministic search windows, location terms, thresholds, and delivery settings.
- `.job-search/keywords.txt`: optional replacement for the skill's default role keywords.
- `.job-search/boards.txt`: optional replacement for the skill's default ATS company list.

Read [references/configuration.md](references/configuration.md) for the complete contract.

If `profile.md` or `preferences.md` is missing:

1. Read CVs, LinkedIn exports, certificates, portfolios, or project evidence supplied in the current conversation or explicitly identified by the user.
2. Follow [references/onboarding.md](references/onboarding.md) to build a draft profile and infer only defensible search preferences. Do not ask the user to re-enter facts already present in supplied materials.
3. Ask only for missing answers that change search scope, hard constraints, or requested delivery. Prefer 2–3 short choices and no more than three questions per round.
4. If no candidate material is available, run `python3 scripts/init_config.py --workdir <workdir>` and fill the generated templates through short choices.
5. Discovery and verification may continue without personal scoring when the user only wants job leads. Matching, CV tailoring, or application priority must not substitute guesses for missing candidate evidence.

During onboarding, only documented or user-confirmed facts may become positive scoring evidence. Mark hypotheses as drafts and keep missing facts as `UNKNOWN`.

## 2. Discover

1. Resolve today's date at runtime; never hard-code an old run date.
2. Download ATS sources with `bash scripts/download.sh --workdir <workdir>`.
3. Normalize and pre-filter ATS data with `python3 scripts/parse_ats.py --today <YYYY-MM-DD> --workdir <workdir>`.
4. Build web queries from role-family × location × job-language variants in `preferences.md`.
5. Always run a targeted gap-fill search for the user's top location. Prioritize named employers, nearby cities, and user-provided links.
6. Select startup and vertical channels from the user's strategy; no fixed platform is mandatory for every candidate.

Read [templates/search_queries.md](templates/search_queries.md) for query composition.

## 3. Normalize and verify

- Deduplicate primarily by company + title + location. Prefer official careers or ATS URLs.
- Use `scripts/verify.sh <urls.txt>` to collect HTTP status, `datePosted`, `datePublished`, and `validThrough`.
- Rank source confidence as `official_ats` > `company_careers` > `aggregator` > `search_snippet`.
- Read freshness windows from `.job-search/settings.ini`:
  - `VERIFIED_FRESH`: an official date falls within the configured window.
  - `LIKELY_FRESH`: a recent lead has an active official page but no reliable official date.
  - `ACTIVE_DATE_UNKNOWN`: the official page confirms that the role is open without a posting date.
  - `OLDER_ACTIVE`: the role is older than the freshness window but remains open.
  - `CLOSED`: the role is no longer active and must be excluded.
- Never present an aggregator index date as an official posting date. Record salary only when its source is explicit.

Write normalized results to `verified_jobs.json`. A legacy project may temporarily merge `ats_results.json` with manually verified report rows, but disclose that difference in the delivery.

## 4. Two-stage evidence scoring

Read `profile.md` and `preferences.md` before scoring. Follow Evidence Before Score: do not choose a score first and search for supporting facts afterward.

### Stage 1: Fast triage

- Apply user-defined hard exclusions first.
- Use thresholds from `settings.ini`; dimensions may include role, seniority, location, career direction, skill transferability, and employer quality.
- Exclude low-triage roles or retain them only as low-priority leads.
- Send roles at or above `deep_score`, plus configured strategic exceptions, to Stage 2.

### Stage 2: JD-to-profile evidence scoring

1. Separate Required from Preferred criteria.
2. Label each criterion `MATCH`, `PARTIAL`, `GAP`, or `UNKNOWN`.
3. Every `MATCH` or `PARTIAL` must cite real evidence from `profile.md`.
4. Check language, education, work authorization, years of experience, location, and other hard constraints.
5. Produce a calibrated score, recruiter-style conclusion, risks, and 1–3 positioning suggestions attributable to verified facts.

Read [references/scoring.md](references/scoring.md) for the general defaults when the project does not override them.

## 5. Reports

Derive report sections from location priorities in `preferences.md` and delivery settings in `settings.ini`, rather than from a fixed candidate or city:

- primary location;
- remote or Germany-wide scope;
- other target locations;
- high-value active or stretch exceptions;
- evidence analysis for roles above the deep-score threshold;
- channel attribution, coverage gaps, and market observations.

Use [templates/report_skeleton.md](templates/report_skeleton.md) as a replaceable structure. Generate only the languages and formats requested by the user.

## 6. Delivery and Workbench synchronization

Read delivery choices from `.job-search/preferences.md` and `.job-search/settings.ini`. The legacy `job-hunt-workbench.html` adapter must:

- prepend new jobs while preserving stable job IDs;
- record `addedIn` and preferably `addedOn: YYYY-MM-DD` for every newly accepted role;
- calculate “recently added” from the last `recent_search_days` calendar days, never from a count of versions;
- read the Workbench interface language from `workbench_language`, independently of `report_languages`;
- support `zh`, `en`, and `de`, with a local UI override that can return to “follow settings”;
- preserve stored job analysis in its actual generated/source language unless localized fields exist; optional localized fields use `<field>Zh` and `<field>En` beside the base field;
- never overwrite or bulk-migrate browser `localStorage` status and remarks;
- keep candidate-private data out of the skill directory and out of Notion status adapters.

If the user later says “change the Workbench to English/Chinese/German,” update project-level `preferences.md` and `settings.ini`, rerun the project configuration sync, and update the interface without rerunning scoring or replacing job/application state.

Before delivering any Workbench change, run:

1. Node `vm.Script` syntax compilation.
2. A DOM smoke test proving that list and board views render, recent-job counts are correct, and the newest search batch is pinned first.
3. Language tests for `zh`, `en`, and `de`, including “follow settings,” refresh persistence for explicit local overrides, and no initial-load mutation of `localStorage`.
4. A mobile-width overflow check.

The current legacy Workbench is a semi-automatic single-file adapter with an embedded `JOBS` array; it is not fully generated from one canonical data file. Report HTML and Notion status use separate generation paths. Read [references/workbench.md](references/workbench.md) before modifying it.

## 7. Supported Commands

Users or agents can invoke these specialized shortcuts:

- `/refresh` [location/role/days]: Trigger an end-to-end fresh job discovery run (ATS download + targeted web search + date verification + two-stage evidence scoring + HTML report and Workbench update).
- `/update-skill`: Auto-update the `job-search-de` skill to the latest release from GitHub (`scripts/update_skill.sh` or `npx skills update job-search-de -g`).
- `/match <url_or_jd>`: Fast deep evidence scoring of an ad-hoc job URL or pasted JD text against verified facts in `.job-search/profile.md`.
- `/tailor <job_id_or_url>`: Generate tailored CV bullet points and a German Anschreiben (cover letter) grounded strictly in verified profile achievements.
- `/sync`: Bidirectionally synchronize application statuses between local Workbench and Notion Job Database (`notion-job-tracker`).
- `/digest`: Generate a quick 60-second morning executive briefing summarizing newly verified roles from the last 24-48 hours.

## 8. Non-negotiable boundaries

- Do not submit applications or contact employers unless the user explicitly authorizes the specific action.
- Do not invent jobs, dates, salary, candidate history, language proficiency, work authorization, or skills.
- Do not copy one user's configuration into another project.
- Do not turn missing information into a negative claim; use `UNKNOWN` and flag it for confirmation.
- Preserve `discoverySource`, `sourceConfidence`, `freshnessConfidence`, and `roleType` on every run for channel and quality review.

## 9. Resources

| Path | Purpose |
|---|---|
| `scripts/update_skill.sh` | Auto-update skill to latest GitHub version |
| `scripts/init_config.py` | Create candidate-neutral project configuration templates |
| `scripts/download.sh` | Download ATS and public-channel payloads |
| `scripts/parse_ats.py` | Normalize, classify, freshness-label, and triage ATS roles |
| `scripts/verify.sh` | Verify official URLs and posting dates |
| `scripts/build_html.sh` | Build report HTML |
| `configs/keywords.txt` | Default German AI role keywords |
| `configs/boards.txt` | Default German-market ATS companies |
| `references/configuration.md` | Project configuration contract |
| `references/onboarding.md` | Evidence-first, low-friction onboarding |
| `references/resume-parser.md` | Resume Parser Prompt, evidence JSON schema, and merge rules |
| `references/scoring.md` | General scoring defaults |
| `references/workbench.md` | Legacy Workbench data flow and recommended architecture |
