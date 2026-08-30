# Workbench delivery model

## Legacy single-file workbench

The existing `job-hunt-workbench.html` is a self-contained HTML/CSS/JavaScript application. It is not currently built from `verified_jobs.json` by a deterministic generator.

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
- `notion`: Warm Editorial Notion Craft Workspace (Default)
- `obsidian`: High-Velocity Linear / Obsidian Dark Mode
- `bauhaus`: Swiss Bauhaus Industrial Brutalism (High-contrast Sharp Grid)
- `bento`: Modern Spatial Bento Box with Frosted Quartz Glass

Theme selection is pure CSS-driven (zero LLM token consumption) and persists across page reloads in browser `localStorage`.

## Report HTML

`report_zh.html` or another language-specific report is generated from Markdown by `scripts/build_html.sh`, then post-processed by `scripts/fix_html.py`. This is independent from the workbench.

## Recommended deterministic architecture

For a reusable multi-user skill, prefer:

```text
verified_jobs.json (job data)
candidate config (private scoring context)
application-status adapter
              ↓
build_workbench.py + neutral HTML template
              ↓
generated workbench HTML
```

The builder should validate the job schema, assign/preserve stable IDs through an ID registry, serialize only display-safe candidate conclusions, and leave status/remarks outside generated job data. Until such a builder exists, describe the legacy adapter as semi-automated rather than fully generated.
