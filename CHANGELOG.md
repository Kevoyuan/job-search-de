# Changelog

## 1.6.0 — 2026-10-08

- Add offline job analytics with primary track breakdown, collection-date scopes, distributions and cross-analysis. Charts share filters with the job list and support keyboard controls, three languages, five themes and mobile layouts.
- Persist evidence-backed job directions, roles and technology tags during acquisition. Expand local rules to 25 occupational categories, 78 professional tools and 29 methods/standards; preserve remote and multiple-location qualifiers.
- Add deterministic seniority and optional management exclusions, structured seniority settings, score-stage provenance and an evidence-review scoring helper. Triage and unverified scores no longer enter high-fit filters or counters. Existing scores remain visible with their verification status.
- Fix Markdown visual-form parsing for bold labels, education entries, separators and empty sections while preserving source edits. Render HTML job descriptions as inert readable text.
- Preserve Ctrl/Meta browser shortcuts and restrict configuration-save shortcuts to the configuration editor.
- Vendor offline chart/font resources with licenses; ship only explicitly fictional demonstration data.
- Add analytics, acquisition, occupation, scoring and browser regressions. Extend CI with data/scoring unit tests.

Migration: configure `[seniority] target_years_min/max` and optionally `[thresholds] max_required_years`. Complete an `evidenceAssessment` using `scripts/evidence_score.py` before publishing an evidence match score. Legacy numeric scores without complete evidence are displayed as unverified. Hard exclusions override numeric scores.
