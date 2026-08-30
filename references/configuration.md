# Project configuration contract

Each job-search project keeps user-specific information in `<workdir>/.job-search/`. The skill directory must remain candidate-neutral. These files are normally generated from user-supplied CVs and short confirmation choices; users should not have to author them manually.

## Required agent-readable documents

### `candidate-evidence.json` (when source documents are parsed)

Auditable intermediate evidence generated from CV/resume, LinkedIn, certificates, portfolios or project files. It preserves source excerpts, confidence, conflicts and unknowns before a readable profile is rendered. Follow [resume-parser.md](resume-parser.md); do not treat this file as user preference data.

### `profile.md`

Record only verified candidate facts:

- current role and years of experience;
- education and work authorization;
- languages with honest proficiency levels;
- skills with evidence;
- projects or achievements with attributable outcomes;
- exact skills, transferable skills and genuine gaps.

The agent may not convert an omitted fact into a negative claim. Missing evidence is `UNKNOWN`.

End the file with a compact provenance section listing supplied filenames and the facts confirmed directly by the user. Do not embed entire source documents.

### `preferences.md`

Record choices that may change independently from the CV:

- target role families and titles;
- location priority and acceptable work modes;
- seniority and compensation preferences;
- language constraints;
- hard exclusions and stretch exceptions;
- target employers, industries and channels;
- required report languages and delivery adapters.
- Workbench interface language, independently of report language.

## Script-readable settings

### `settings.ini`

```ini
[search]
country_query = germany
fresh_days = 14
exception_days = 30

[locations]
priority_1 = frankfurt, eschborn
priority_2 = remote, germany, deutschland
priority_3 = munich, münchen
broad = berlin, hamburg, stuttgart, cologne, köln

[thresholds]
triage_keep = 65
deep_score = 75
high_value_fit = 80

[delivery]
recent_search_days = 5
report_languages = zh
workbench_language = zh
workbench = true
notion = false
```

`workbench_language` accepts `zh`, `en` or `de`. It controls interface chrome and newly generated display text, not job-language eligibility. `report_languages` remains independent and may contain the report language(s) requested by the user.

Comma-separated location terms are matched case-insensitively. Keep German and English spellings when both appear in job feeds.

## Optional deterministic overrides

- `keywords.txt` replaces `configs/keywords.txt` for ATS parsing.
- `boards.txt` replaces `configs/boards.txt` for ATS downloads.

Overrides replace the default file rather than merging it, so a project has an explicit and reproducible search surface. Copy the default file before editing when only a small adjustment is needed.

## Resolution order

Scripts resolve configuration in this order:

1. explicit `--config-dir`;
2. `<workdir>/.job-search`;
3. skill defaults for non-personal ATS keywords and boards.

Candidate facts and preferences never fall back to a skill-owned personal profile.

For first-run extraction and minimal-question behavior, read [onboarding.md](onboarding.md).
