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
