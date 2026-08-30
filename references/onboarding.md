# Low-friction candidate onboarding

Use this flow when a project has no usable `.job-search/profile.md` / `preferences.md`, or when the user asks to refresh them from new documents.

## 1. Prefer supplied evidence over questionnaires

Use, in order:

1. files attached by the user in the current conversation;
2. CV/resume, LinkedIn export, portfolio, certificates or project summaries whose paths the user explicitly provides;
3. existing candidate documents already identified inside the current job-search project;
4. short user answers for facts that the documents cannot establish.

Do not scan unrelated home folders, cloud drives or personal workspaces. Do not send private documents to external services unless the user explicitly requests that service.

For PDF, Word or image CVs, use the available document/OCR capability appropriate to the file. Preserve the source filename for provenance.

When any candidate document is supplied, read [resume-parser.md](resume-parser.md) and apply its full extraction prompt and evidence schema.

## 2. Build an auditable evidence file first

Extract and normalize into `.job-search/candidate-evidence.json`:

- current/recent roles, dates and approximate relevant experience;
- education and certifications;
- languages, only at the level explicitly stated;
- skills tied to roles or projects;
- measurable outcomes and scope;
- location and any explicit work authorization;
- likely role families, clearly marked as a draft preference rather than a fact.

Every profile claim must be one of:

- `DOCUMENTED`: explicitly present in a supplied source;
- `USER_CONFIRMED`: confirmed by the user;
- `DRAFT_INFERENCE`: useful hypothesis awaiting confirmation;
- `UNKNOWN`: not established.

Only `DOCUMENTED` and `USER_CONFIRMED` may be used as positive evidence in deep scoring. Never turn `DRAFT_INFERENCE` into a CV claim.

Preserve source references, confidence labels, conflicts and unknowns in `candidate-evidence.json`. Do not skip this intermediate file and write directly from raw CV text to `profile.md`.

After material conflicts are resolved, generate `.job-search/profile.md` from `DOCUMENTED` and `USER_CONFIRMED` evidence. Record a compact source list at the end of the profile; do not copy full CV text when a concise evidence record is sufficient.

## 3. Ask only decision-changing questions

After extraction, ask only for missing information that changes search coverage or hard-constraint decisions. Prefer at most three short questions per round.

When structured-choice UI is available, use it. Otherwise present 2–3 numbered choices plus a free-form option. Put the recommended choice first when a recommendation is justified by the supplied evidence.

Useful question groups:

### Target direction

- Focus on roles closest to recent experience.
- Include adjacent/transferable roles.
- Explore broadly before narrowing.

### Location and work mode

- One primary metro plus remote Germany.
- Germany-wide remote only.
- Multiple named cities / relocation allowed.

### Seniority strategy

- Match documented experience.
- Include one-level stretch roles.
- Include junior/down-level roles as well.

### Delivery language

When a report or Workbench will be delivered and its language is not already configured, ask with short choices:

- Chinese (`zh`).
- English (`en`).
- Chinese + English (`bilingual`).

Record report language and Workbench interface language separately because the user may want different values. Do not ask for a Workbench language when Workbench delivery is disabled. A later plain-language request such as “change the Workbench to English” updates the preference; onboarding choices are not permanent.

Ask work authorization, language requirements, salary floor or relocation constraints only when not established and relevant. Do not require salary disclosure to start a search.

## 4. Generate preferences and settings

Convert confirmed choices into:

- `.job-search/preferences.md` for human-readable strategy;
- `.job-search/settings.ini` for deterministic windows, location terms and thresholds.

Use `delivery.report_languages` for report output and `delivery.workbench_language` for Workbench UI. Supported Workbench values are `zh`, `en` and `de`.

Show the user a concise summary of what was extracted, what was selected and what remains `UNKNOWN`. Do not ask the user to manually rewrite generated files unless they prefer to.

## 5. Updates

When a new CV or source is provided later:

- preserve previously user-confirmed facts unless the user replaces them;
- merge into `candidate-evidence.json` before regenerating `profile.md`;
- reconcile date or title conflicts explicitly;
- update only affected sections;
- keep unsupported old claims out of scoring until resolved.
