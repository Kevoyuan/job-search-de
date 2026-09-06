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
- `notion`: Notion Craft Warm Editorial Workspace (Default - Paper canvas, ink charcoal, soft pastel property chips)
- `obsidian`: Linear Obsidian High-Velocity Dark Engine (`#010102` deep void, `#5e6ad2` lavender, hairline technical panels)
- `bauhaus`: Braun / Dieter Rams Functional Industrial Minimalism (Warm matte resin, hairline precision dividers, signature Braun amber accent `#e8590c`, tactile convex hardware keys)
- `bento`: Apple Spatial Bento Quartz Glassmorphism (VisionOS / macOS frosted translucent quartz, Apple Action Blue `#0071e3`, specular reflections, floating glass tiles)

Theme selection is pure CSS-driven (zero LLM token consumption) and persists across page reloads in browser `localStorage`.

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

