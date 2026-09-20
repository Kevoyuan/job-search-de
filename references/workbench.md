# Workbench delivery model

## Legacy single-file workbench

The existing `job-hunt-workbench.html` is a self-contained HTML/CSS/JavaScript application. It is now built deterministically from `verified_jobs.json` by `scripts/build_workbench.py`. The manual flow below describes older projects.

Current update path:

```text
ATS/Web discovery + verification + scoring
                  ↓
          report_zh.md
                  ↓
Agent converts accepted rows into JS objects
                  ↓
prepend/update const JOBS = [...] inside job-hunt-workbench.html
                  ↓
browser renders table, cards and kanban locally
```

The Agent also updates `CURRENT_VERSION`, `addedIn`, preferably `addedOn`, visible counts and footer metadata. Stable job IDs must be preserved.

Separate status path:

```text
Notion Job database
        ↓
sync_notion_status.py
        ↓
notion-status.js
        ↓
workbench status rendering
```

Browser remarks and fallback statuses live in `localStorage`; rebuilding the HTML must not overwrite them.

The “近期新增岗位” view reads `delivery.recent_search_days` from `.job-search/settings.ini` as its default rolling calendar-day window. The UI may expose a local `X`-day filter and remember that display override in `localStorage`; changing the UI filter does not rewrite project configuration. Keep the filter visible even when the selected window contains zero jobs so the user can widen it again.

Workbench interface language reads `delivery.workbench_language` (`zh`, `en` or `de`) independently from report language. A UI selector may provide a local display override, including a “follow settings” mode. Persist only that override key and do not rewrite project files from a static `file://` page. When the user changes the language through an agent command, update `settings.ini` and `preferences.md`, rerun the project configuration sync, and preserve job IDs, status values, remarks and other browser state. Stored job analysis may remain in its source/generated language until the next report/job-data regeneration; never pretend it was translated.

When localized job display text is available, keep the existing base field for backward compatibility and add `<field>Zh` / `<field>En` variants (for example `reasonZh` and `reasonEn`). English and bilingual views must fall back honestly to the stored base value when a translation is absent.


Workbench UI supports instant client-side theme switching across 4 curated design systems:
- `notion`: Editorial Craft Warm Workspace — the reference look, kept exactly as shipped. Do not restyle it when reworking the other themes.
- `obsidian`: editorial index on deep green-tinted slate (`#181d1d` canvas, `#212827` surface, sage `#c8d8a9` accent, dark green `#243d2d` strengths / dark rose `#442d31` gaps).
- `bauhaus`: warm gray-green industrial (`#e8e8e3` resin, square zero radii, dark `#30392d` table header with light text, olive-yellow `#d7de79` primary, 4px header rule).
- `bento`: pale mint workspace (`#eef3f1` canvas, white surface, forest `#426e58` accent, 7–12px radii, soft shadows, pill score badges, 3px left rule on evidence panels).

Theme selection is pure CSS-driven (zero LLM token consumption) and persists across page reloads in browser `localStorage`.

### Theme refresh pack

`templates/theme-refresh.css` holds the treatment for the three non-default
themes; `scripts/build_workbench.py` appends it to the end of the main
stylesheet at build time, so the generated workbench stays a single
self-contained HTML file. Every selector in the pack must be scoped with
`:is(html[data-theme="obsidian"],html[data-theme="bauhaus"],html[data-theme="bento"])`
or a single non-default `html[data-theme="…"]` attribute selector. A rule that
matches `notion`, or an unscoped `html[data-theme]` selector, silently changes
the reference look and fails the contract below.

Two failure modes are easy to hit and cheap to avoid:

- The literal `</style>` sequence anywhere in the pack (including inside a
  comment) terminates the stylesheet element early and drops the remaining CSS
  without any console error. Write "the closing style tag" instead.
- Per-theme token blocks only win when their selector is at least as specific as
  the one shipped in the template; `html[data-theme="obsidian"]` beats the
  template's `[data-theme="obsidian"]`, a bare `[data-theme]` does not.

Verification after any theme change: compare computed styles of the shipped
workbench against the previous build for `notion` (must be identical), and
against the approved preview for the other three themes. `scripts/test_workbench_browser.cjs`
plus a computed-style probe covers this; the probe list used for direction A
("索引编辑") lives in the project's `design-demos/theme-redesign/verify-applied.cjs`.

## Interactive candidate config editor

Workbench provides an integrated **Candidate Configuration & Preferences Drawer**:
- Reads and displays candidate facts (`profile.md`), search preferences (`preferences.md`), and deterministic thresholds (`settings.ini`).
- **File System Access API integration**: Users can click "关联本地目录" to authorize browser access to their local `.job-search/` folder. Edits made in the drawer (or through the visual form mode) can be written back directly to disk with one click (`Ctrl+S` / `Cmd+S`).
- **Graceful Fallback**: For browsers without direct File System Access (like Safari), users can export modified files or copy Markdown content to clipboard.
- **Visual Form & Source modes**: Allows editing key parameters via interactive form controls or directly editing Markdown/INI source code with real-time dirty status indicators.

## Update notifications with one-click copy

Top notification banner and modal prompts display available updates alongside one-click copy buttons for upgrade commands (`/update-skill` and `npx skills update job-search-de -g`) with instant clipboard toast feedback.

## Report HTML

`report_zh.html` or another language-specific report is generated from Markdown by `scripts/build_html.sh`, then post-processed by `scripts/fix_html.py`. This is independent from the workbench.

## Deterministic architecture

```text
verified_jobs.json (job data)
candidate config (.job-search/profile.md, preferences.md, settings.ini)
              ↓
build_workbench.py + templates/workbench_template.html
              ↓
generated job-hunt-workbench.html (interactive, editable, 4 themes)
```


## Job field compatibility

The builder accepts a job list or an object containing `jobs`. It maps legacy
`fit/co/loc/mode/date/sal` to `score/company/location/workModel/datePosted/salary`.
Existing canonical fields win, including an explicit null score. Original fields,
IDs, evidence, and source JSON remain unchanged. Numeric scores from 0 through 100
are retained; missing, invalid, or out-of-range scores become null and display as
“Unrated” in all views. Unrated jobs remain visible with no score filter, are
excluded from high-fit counts/filters, and sort after scored jobs in either direction.
This adapter does not calculate or validate the evidence behind an existing score,
and does not infer freshness or role classification from legacy fields.

Regression checks: `python3 scripts/test_workbench.py` and
`node scripts/test_workbench_browser.cjs <generated-html>` (requires Playwright;
set `PLAYWRIGHT_MODULE` to its installed module path if necessary).

## Recent search results control

Always render this section above the job list. Count jobs by their `addedOn`
date within the last X local calendar days, including today. Exclude missing,
invalid, and future discovery dates; do not substitute posting dates or freshness.
Default to `[delivery].recent_search_days` (fallback 5). Accept whole numbers
1–3650 and persist the display override as `job_workbench_recent_search_days`.
“Use configured window” removes the override. Render a compact standalone card grid at the very top, before the full-list controls, with
company, title, score, location, and discovery date. Click a card for full details
and the apply link. Use five columns on wide desktop and responsive breakpoints
below that. Show two rows by default with expand/collapse.
Sort newest discovery dates first, then descending score. The main list filters
and table/kanban switch do not affect this section. Keep the section visible
when the count is zero. Older jobs and browser application state remain stored.
Every search refresh must preserve original `addedOn` for existing jobs and set
it to the discovery date for newly accepted jobs; do not renew it on each rebuild.

## Compact analysis layout

Main-list rows expand in place into two labeled panels: green for stored fit
evidence, rose for gaps and risks. Both use readable text and dark-theme variants.
On small screens they stack vertically. Filtering hides the expanded tray with
its parent job. Full details retain the same color distinction and all job data.
