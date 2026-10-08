# Collected-job tag statistics

The **Jobs / Analysis** switch shares the main search, score, freshness and quick
filters. Within Analysis, **Distributions / Cross analysis** shows job labels and
counts. Recent search cards retain their independent calendar window. The sample
describes collected jobs rather than the entire German labor market.

## Job data contract

Each job may add these evidenced optional fields:

```json
{
  "analysis": {
    "analyzedAt": "2026-10-05",
    "cities": ["Munich", "Berlin"],
    "industry": "Manufacturing",
    "role": "AI Engineering",
    "evidence": {
      "cities": "Saved listing says München or Berlin",
      "industry": "Saved employer description explicitly identifies manufacturing",
      "role": "Original title: Applied AI Engineer"
    },
    "technologies": [
      {"name": "Kubernetes", "requirement": "preferred", "evidence": "K8s is a plus"}
    ]
  }
}
```

Industry means the employer's primary industry, not the candidate's sector or a
technology. Save null when it cannot be established from stored employer evidence.
Recruiting agency listings do not establish a client's industry. Preserve original
titles, descriptions, IDs, dates, evidence and scores. Do not invent translations.

The builder creates a derived `analytics` object without rewriting input JSON.
It validates the optional fields, canonicalizes explicit city/technology aliases,
and deduplicates within each job. For legacy rows it extracts recognizable cities
from `location`, job categories from `roleType` or explicit title phrases, and
literal technical mentions from stored titles, JDs, descriptions and requirement/skill lists. It never extracts technology
requirements from candidate strengths/gaps, guesses industries from company names,
or treats a bare mention as required. Explicit required/preferred wording is recognized
only within the same stored clause; mixed or negated wording remains mentioned. Unknown ambiguous terms such
as standalone Go, R, C or Spring need explicit agent annotation.

Technology requirement values are `required`, `preferred`, `mentioned`.
Duplicate aliases retain the strongest explicitly supplied requirement and its
supporting evidence. Invalid requirement labels become `mentioned`; missing evidence
is rejected. Source metadata remains available alongside normalized data.

## Agent workflow

Read saved job descriptions and employer evidence. Generate optional per-job
`analysis` fields for cities, industry, role and technologies. Record the analysis
date and preserve original fields, IDs, fit scores and unknowns. Existing-data-only
enrichment uses local saved sources. Rebuild with
`python3 scripts/build_workbench.py --workdir <workdir> --lang zh`.

## Counting and interaction

Each job contributes at most once to each city/technology category. An industry,
role and work model have one normalized category. Remote is a work model, not a
city. Missing categories have a selectable Unknown bucket.

All shares divide by the total number of currently selected jobs, including rows
with unknown information. Multi-label totals can exceed 100%. Coverage reports
known rows / selected rows. Technology bars break down required/preferred/mentioned.

Bars toggle facets; the "Add a filter" controls expose the complete dataset's
categories, so users can add alternatives even after narrowing the charts.
Values within one facet are OR; facets and main-list filters are AND. Matrix cells
replace their two axes with the selected pair while preserving other filters.
Row/column selectors change matrix display only. All filters have removable chips
and a global reset. The matching jobs section opens original details; switching
back to Jobs preserves filters and the previous table/kanban view.

## Demo and verification

`--demo` uses only `tests/fixtures/analytics_demo.json`, including its fictional
configuration and settings; it must not embed private workdir data. Normal empty builds
stay empty, with no silent sample-job fallback. The tracked sample workbench is
built with `--demo --lang zh --no-update-check`.

Checks:

```sh
python3 scripts/test_workbench.py
python3 scripts/test_analytics.py
PLAYWRIGHT_MODULE=/path/to/playwright node scripts/test_workbench_browser.cjs job-hunt-workbench.html
PLAYWRIGHT_MODULE=/path/to/playwright node scripts/test_analytics_browser.cjs job-hunt-workbench.html
```

Public previews may contain only the fictional fixture. Real job collections
and candidate configuration remain local. Source modules in `templates/analytics.js`
and `templates/analytics.css` are inlined by the builder; there is no chart CDN,
LLM call or network requirement for analytics.

## Lieflat Charts design provenance

The analysis surface uses **Mono** throughout: paper `#F0EFEB`, ink `#1C1C1A`,
and the token gray ladder. Inter is bundled and embedded into the generated HTML.
Only the analysis section changes typography and palette; existing workbench
navigation, themes, candidate configuration and job views remain separate surfaces.

Chart mode was selected because the request is to redesign job-tag statistics,
not produce a narrative report. The L1–L20 and F1–F17 catalog was reviewed;
no Glance, maps or report template is needed. The installed skill's sparse checkout
omitted galleries, so the exact tracked files were read from its Git HEAD.

| Shape | Candidate | Decision |
|---|---|---|
| Tag ranking | L2 Dot Cascade, `What breaks, stacked and ranked` | Rejected: rotated narrow category labels do not fit long job/industry names. |
| Tag ranking | L15 Ballot Tally, `What they fear, tick by tick` | Rejected: a fixed hundred-unit queue would imply rounded percentages; this sample has exact integer jobs and more than six tags. |
| Tag ranking | L12 Type Colonnade, `Forty-four repos, ten owners` | Rejected: multi-label location/technology data are not exclusive assignments, and 273 records exceed its intended 50-record range. |
| Tag ranking | F1 Rung Bars, `Revenue by plan, rung by rung` | Rejected: vertical labels would need much more width or rotate long categories. |
| Tag ranking | **F5 Tick Rows**, `Six teams, shipped and counted` | Selected: a horizontal, countable queue supports exact jobs, long labels, ranking and independent multi-label counts. |
| Cross counts | **L4 Arc Matrix**, `Eight products land in twelve cities` | Selected: the default 6×6 view and capped 8×8 selectors fit the ≤100-cell contract. |
| Cross counts | L9 Bubble Almanac, `Eight years of tickets, one almanac` | Rejected: this is categorical cross counting, not a year sequence; hand-drawn overlapping bubbles obscure clickable cells. |
| Cross counts | F10 Dot Heat, `When support gets loud` | Rejected: its weekday/hour interpretation is unnecessary; L4 directly supports category/category counts. |

F5's actual card and C1 script in `templates/basics-gallery.html` supply the
horizontal unit strokes, fifth-unit markers, label positions, endpoint totals and
unit-by-unit reveal. One stroke is exactly one job; no synthetic records, rounding,
broken axes or percentage units. Up to eight ranks occupy a chart frame; browse
all tags with eight-item pages. Missing labels are shown and selectable separately,
with the full selected-job denominator and exact count in the data table.

L4's actual card and `3 · arc bubble matrix` script in
`templates/lupi-gallery.html` supply bowed row horizons, tiny zero markers,
square-root radii, gray intensity bands and top-four annotations. A shared
radius scale keeps circle area proportional to count. Native SVG buttons and
transparent 48px hit regions support pointer and keyboard selection; full labels
and values are available in accessible names, titles and the data table.

The complete Mono token module is vendored in `assets/vendor/lieflat-mono.js`.
The only lifecycle adaptation adds a disposer to `obsReveal` so repeated filtering
cleans up detached observers, event listeners and registered timers. Replay uses
the same reveal hook. CSS animations are scoped to analysis, use the documented
fast-out easing, and disable under `prefers-reduced-motion`. ResizeObserver redraws
the distribution frame at its actual width, preserving readable labels on mobile;
the cross chart scrolls inside its own keyboard-reachable region.

The adapted Lieflat source is under PolyForm Noncommercial 1.0.0, independently
of this repository's MIT license. Its notice URL is embedded in generated HTML
and source. Inter remains under SIL Open Font License 1.1, embedded alongside its
license text. Full terms are retained in `references/licenses/`.

## Analytics layout refinement

The analysis shell now shares the workbench typography, theme tokens and control
geometry; Mono is confined to the chart card. Sample count and actions occupy the
header, while view switching, category selection and filter disclosure share a
single desktop row. Mobile keeps both views and all actions reachable.

SVGs have an explicit physical width, rather than scaling a narrow viewBox to the
entire page. Rankings use 48px minimum rows, measured full-label wrapping and a
1120px width cap. Cross charts retain bowed horizons and proportional bubble area,
with 128–160px columns, 56px minimum rows, horizontal wrapped labels and bounded
horizontal scrolling. Unknown coverage and exact-value tables remain available.
The exact-value table scrolls within 360px; original job details and notes still
use the existing workbench drawer. Internal F5/L4 identifiers stay in source and
provenance documentation rather than appearing as product-facing metadata.

Visual verification uses `scripts/test_analytics_layout.cjs` for unscaled SVGs,
label bounds, language/theme combinations, keyboard scrolling, no page overflow
and 200% reflow. `premium-ui.json` scopes the strict static audit to maintained
source templates and records canonical native select ownership. Generated HTML
and historical architecture/design demo documents are not separate UI owners.


## Local extraction v2: explicit location and technology information

`analytics_data.py` builds every tag locally from saved records, with no model or
network calls. `extractionVersion: local-rules-v2` identifies the rule set. Existing
source JSON remains unchanged. Extend aliases here rather than asking an Agent
to regenerate statistics on each build.

- `cities` remains actual standardized cities only. `locationTags` adds the reserved
  `__location_remote__` and `__location_multiple__` qualifiers. City filters retain
  all named cities; a multi-city record also matches Multiple locations. Explicit
  remote arrangements (including hybrid remote options) match Remote; original
  location/work-model evidence remains available. These categories overlap.
- Unrecognized but recorded location strings remain visible verbatim with an
  “Recorded location” label. Only a missing location becomes “Location not recorded”.
- Technology tags carry a derived `category`: languages, frameworks, cloud, data,
  ai_tools, engineering, methods or other. Named tools are distinguished from
  broader technical directions; LLM or robotics does not imply Python/PyTorch.
- `technologyStatus` is mutually exclusive: specific, direction_only, language_only,
  no_description, unidentified. `language_only` requires the saved description to
  consist of language requirements. No match in a substantive saved description
  stays `unidentified`; this never asserts that no technical requirements exist.
- Technology rankings and matrix filters expose separate missing-reason buckets.
  Technology categories and information status have their own selectable
  distributions; the exact technology table also shows category and requirement level.

Shares still use all filtered jobs. Location, technology and technology-category
counts may overlap. Technology information statuses partition the selected jobs.
Regression tests cover remote/multiple location qualifiers, city aliases, retained
unrecognized places, missing-reason distinctions, category assignment, explicit
requirement wording, exclusions of candidate text and immutable source records.


## Persist at acquisition

`parse_ats.py` retains `description_raw`, full plain-text `jd`, description source
URL, capture date and availability status. It calls `enrich_job` before writing
`ats_results.json`, so acquisition results already contain `analysis.technologies`,
category, requirement, evidence, source field/URL and extraction method, plus
technology information status, groups, extraction version and date. Lever list
sections and additional content are retained; source HTML scripts/styles are
excluded from extracted plain text while original HTML stays stored as evidence.

Web/manual acquisition and verified-row merges must preserve the full JD and tags.
Run `python3 scripts/save_job_analysis.py --jobs-file <workdir>/verified_jobs.json`
after saving those records. The utility writes atomically and backs up in-place
updates. `--output` writes a separate file. It supports both arrays and `jobs`
wrappers and preserves other fields, IDs, fit scores and metadata. Generated tags
are re-extracted when stored descriptions change; manually curated evidenced tags
remain. Missing source descriptions are explicitly recorded and should be fetched
from official detail pages during acquisition where available. The extractor
matches a local vocabulary; genuinely unrecognized technology names remain
unidentified until the dictionary or an evidenced explicit tag is added.

During the normal official-description verification pass, explicitly retain clearly
named technologies outside the local dictionary as evidenced `analysis.technologies`
entries. The local persistence utility preserves these curated tags as
`saved_evidence` alongside `local_rules` tags. No separate model call is required.


## Local role classification v2

Explicit curated role labels with saved evidence take precedence. Otherwise,
specific title patterns classify research, robotics, data consulting, application
engineering, software/product engineering, AI development/architecture/enablement,
and MLOps/LLMOps before broad AI matches. Known `roleType` codes provide a fallback;
`general_match` and unsupported codes do not become invented job categories.
Canonical categories normalize aliases and display translated Chinese/German labels
while original titles and roleType fields remain preserved. The acquisition saver
persists `analysis.role`, `analysis.evidence.role`, classification method/version
and date. Generated categories refresh when titles/rules change; curated categories
remain authoritative. Unclassifiable titles stay “Job category not yet identified”.

## Primary track breakdown

The default distribution is a compact horizontal bar chart of one primary track
per collected job: Software & Python, General Engineering, AI / GenAI & LLM,
Data & Analytics, Tech Consulting, Validation & QA, Smart Energy & IoT and
Acoustics & Audio DSP. Specific title patterns take precedence; known role families
and saved job descriptions provide fallbacks. Other / Needs review remains a
separate review entry when evidence cannot establish a direction. Candidate text
and employer names never assign tracks. Counts are exclusive and sum to selected jobs.

Acquisition saves `analysis.track`, `analysis.evidence.track`, classification method,
version and date. Curated evidenced tracks are retained. Generated tracks update
with local rules. Browser scopes use collection date `addedOn`, not publication
date: added today / latest dated batch / all collected. The default prefers today;
if no dated additions exist today it opens the latest batch with an explicit date.
A manually selected empty today scope stays empty. The scope also filters the job
list and has a removable chip; resetting all filters selects all collected jobs.
Technical cross analysis includes recognized categories and technologies only,
with missing-information status available in its separate distribution.

### Other occupations: local extraction

`scripts/occupation_rules.py` extends the local vocabulary beyond software: mechanical/manufacturing, electrical/automation, construction, finance, marketing, sales/customer support, HR, supply chain/operations, healthcare/laboratory, design, education, legal/compliance and IT security. English, German and Chinese title patterns assign a primary track and role. Saved descriptions provide professional tools (for example SolidWorks, TIA Portal, DATEV, HPLC) and methods (for example IFRS, GMP, Six Sigma). Tools use the engineering category; methods retain the separate methods category. No occupation implies a tool without textual evidence. Unknown records and candidate-side text never supply invented skills. The collection/save pipeline applies these same rules; re-run `save_job_analysis.py` and rebuild to refresh old locally generated tags.
