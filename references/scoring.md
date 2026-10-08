# Candidate-neutral scoring defaults

Projects may override these defaults in `preferences.md` and `settings.ini`.

## Stage 1: Fast Triage

| Dimension | Default points |
|---|---:|
| Role core fit | 35 |
| Seniority fit | 20 |
| Location and work-model fit | 15 |
| Career-direction fit | 15 |
| Stack transferability | 10 |
| Employer quality | 5 |

Default thresholds:

- below `triage_keep`: drop or low-priority lead;
- `triage_keep` through `deep_score - 1`: shortlist only when location or strategy justifies it;
- at or above `deep_score`: deep evidence scoring.

## Stage 2: Evidence scoring

| Category | Default weight |
|---|---:|
| Hard skills | 30% |
| Experience | 25% |
| Technical depth | 20% |
| Domain alignment | 10% |
| Education | 5% |
| Communication and stakeholder skills | 10% |

Coverage labels:

- `MATCH`: direct profile evidence.
- `PARTIAL`: adjacent or transferable evidence; explain the bridge.
- `GAP`: no direct or transferable evidence.
- `UNKNOWN`: insufficient information; do not score as a fabricated failure.

Default calibrated verdicts:

- 90–100: `STRONG_SHORTLIST`
- 80–89: `SHORTLIST`
- 70–79: `MAYBE`
- 60–69: `STRETCH`
- below 60: `REJECT`

Hard constraints override the numeric score when the requirement is explicit and non-negotiable.

## Executable gates and score provenance

Use `scripts/evidence_score.py --job job.json --settings .job-search/settings.ini --preferences .job-search/preferences.md --output review.json` to prepare a review. Fill its six `dimensions` with MATCH/PARTIAL/GAP/UNKNOWN, jobEvidence, candidateEvidence and reason, and review experience/language/drivingLicence in hardConstraints. Then run the same command with `--review review.json --output scored-job.json`. MATCH/PARTIAL/GAP contribute 1/0.5/0 of the dimension weight. UNKNOWN or missing evidence blocks a final score. This helper verifies completeness and computes a deterministic score; the reviewer must verify the cited evidence against the source. A hard-constraint GAP overrides the score.

Persist `scoreStage: triage | evidence`; legacy or unsupported claims become `unverified`. Only validated evidence scores with no exclusion enter high-fit counters and filters. Never relabel title-keyword scores as evidence scores. Numeric legacy scores remain visible with an unverified label.

`[seniority] target_years_min/max` are machine-readable candidate targets. `[thresholds] max_required_years` optionally overrides the maximum required experience; unset means use target_years_max, not a global junior assumption. Legacy explicit `Target Seniority: 0–3 years` is read as a fallback. Required ranges compare their lower bound. Preferred, negated, upper-bound and alternative qualification clauses do not cause automatic seniority exclusion; alternatives need review. Requirements retain original excerpts in analysis.requiredYearsEvidence. Excluded rows are retained with EXCLUDED_SENIORITY / EXCLUDED_MANAGEMENT for audit, never promoted by a high numeric score.

Manager exclusions are opt-in using exclude_non_engineering_managers and manager_title_exceptions. Engineering/technical managers are not covered by that option; their explicit experience requirements still apply. Merge data by stable job identity, retaining evidenceAssessment and scoreStage together; rebuild/save reapplies gates so merging ats_results and verified_jobs cannot bypass them.
