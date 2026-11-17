# Changelog

## 1.7.1 — 2026-11-17

- Recognize experience requirements such as “7+ years in engineering”, including lists of alternative specialties, while keeping equivalent qualifications for review and avoiding company-age claims.
- Preserve reviewed exclusion decisions with supporting evidence and preference provenance when normalizing jobs and rebuilding the workbench.

## 1.7.0 — 2026-11-17

- Add a daily action queue for due follow-ups, applications being prepared and evidence-scored jobs to review.
- Track application and follow-up dates, contacts and status history locally, with versioned JSON export and conflict-preserving restore. Existing browser notes and statuses remain readable.
- Make reports opt-in. Add centralized, change-aware backups with retention controls, a preview command and a cleanup status snapshot in the workbench.
- Write workbench and job analysis files atomically and skip unchanged data writes.

Application records remain in the current browser until exported; filesystem backup cleanup does not back them up. Automatic scheduled cleanup is configured per machine, not installed by the skill.

## 1.6.0 — 2026-10-08

- Add offline job analytics with primary track breakdown, collection-date scopes, distributions and cross-analysis. Charts share filters with the job list and support keyboard controls, three languages, five themes and mobile layouts.
- Persist evidence-backed job directions, roles and technology tags during acquisition. Expand local rules to 25 occupational categories, 78 professional tools and 29 methods/standards; preserve remote and multiple-location qualifiers.
- Add deterministic seniority and optional management exclusions, structured seniority settings, score-stage provenance and an evidence-review scoring helper. Triage and unverified scores no longer enter high-fit filters or counters. Existing scores remain visible with their verification status.
- Fix Markdown visual-form parsing for bold labels, education entries, separators and empty sections while preserving source edits. Render HTML job descriptions as inert readable text.
- Preserve Ctrl/Meta browser shortcuts and restrict configuration-save shortcuts to the configuration editor.
- Vendor offline chart/font resources with licenses; ship only explicitly fictional demonstration data.
- Add analytics, acquisition, occupation, scoring and browser regressions. Extend CI with data/scoring unit tests.

Migration: configure `[seniority] target_years_min/max` and optionally `[thresholds] max_required_years`. Complete an `evidenceAssessment` using `scripts/evidence_score.py` before publishing an evidence match score. Legacy numeric scores without complete evidence are displayed as unverified. Hard exclusions override numeric scores.
