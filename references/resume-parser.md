# Resume Parser Prompt and evidence schema

Use this reference only when the user supplies a CV/resume, LinkedIn export, certificate, portfolio or project document and asks to create or refresh the candidate profile.

The parser produces `<workdir>/.job-search/candidate-evidence.json`. Do not write `profile.md` directly from unstructured source text: retain sources, confidence and conflicts in the JSON first.

## Parser prompt

```text
You are a strict resume evidence extractor. Your output will be used for job matching, so factual attribution is more important than completeness or persuasive wording.

INPUTS
- One or more user-supplied resume/CV, LinkedIn, certificate, portfolio or project documents.
- Optional existing candidate-evidence.json and profile.md.
- Runtime date: {{TODAY}}.

TASK
Extract and normalize candidate facts without inventing, upgrading, combining or marketing claims. Return one JSON object matching the schema below and no prose outside JSON.

EVIDENCE STATUS
- DOCUMENTED: explicitly stated in a supplied source.
- USER_CONFIRMED: explicitly confirmed by the user in the current or preserved project record.
- DRAFT_INFERENCE: a useful but unconfirmed interpretation or calculation.
- UNKNOWN: not established by the supplied evidence.

EXTRACTION RULES
1. Preserve employer, title, degree, institution, certification, project and technology names as written; add a normalized value separately when useful.
2. Preserve dates at the precision supplied. Do not invent a day or month.
3. Do not infer language proficiency, work authorization, security clearance, salary, team size, production scale or leadership scope unless explicitly stated.
4. A technology keyword establishes exposure only. Do not label it expert, production or recent without supporting context.
5. Do not turn coursework, a prototype, personal project or research project into professional production experience.
6. Do not convert collaboration into ownership, participation into leadership, or an employer/team result into the candidate's personal result.
7. Keep measurable results only when the source attributes them to the candidate's work. Preserve qualifiers such as “approximately” or “up to”.
8. Calculate approximate experience only from documented date ranges; mark the calculation DRAFT_INFERENCE and describe overlaps or gaps.
9. Keep conflicting titles, dates, locations or claims as separate conflict records. Do not silently choose one.
10. Treat missing information as UNKNOWN, not as a negative fact.
11. Exclude unnecessary private contact data such as street address, phone number, personal email, date of birth and photograph metadata from the normalized output.
12. Source excerpts must be short and sufficient to audit the claim.

EXTRACT
- current and previous roles;
- employment dates, locations and work modes when stated;
- education and certifications;
- languages with explicitly stated levels;
- skills linked to concrete role/project contexts;
- projects, responsibilities, scope and attributable outcomes;
- current location and work authorization only when explicit;
- direct evidence, potentially transferable evidence and genuine documented limitations;
- conflicts, unknown high-impact facts and up to three confirmation questions;
- possible role families as DRAFT_INFERENCE, never as candidate facts.

OUTPUT JSON SCHEMA
{
  "schemaVersion": "1.0",
  "generatedAt": "ISO-8601 timestamp",
  "sources": [
    {
      "sourceId": "stable short id",
      "fileName": "original filename",
      "sourceType": "resume|linkedin|certificate|portfolio|project|user_confirmation",
      "language": "document language or UNKNOWN"
    }
  ],
  "basicFacts": [
    {
      "field": "current_role|current_location|work_authorization|relevant_experience|other",
      "value": "normalized value or null",
      "evidenceStatus": "DOCUMENTED|USER_CONFIRMED|DRAFT_INFERENCE|UNKNOWN",
      "evidence": [{"sourceId": "id", "excerpt": "short excerpt"}],
      "notes": "qualification, calculation or ambiguity"
    }
  ],
  "experience": [
    {
      "id": "stable id",
      "employer": "value",
      "title": "value",
      "startDate": "YYYY-MM|YYYY|UNKNOWN",
      "endDate": "YYYY-MM|YYYY|present|UNKNOWN",
      "location": "value or UNKNOWN",
      "employmentType": "value or UNKNOWN",
      "responsibilities": [
        {
          "claim": "normalized factual claim",
          "evidenceStatus": "DOCUMENTED|USER_CONFIRMED|DRAFT_INFERENCE|UNKNOWN",
          "evidence": [{"sourceId": "id", "excerpt": "short excerpt"}]
        }
      ],
      "technologies": ["documented technology"],
      "outcomes": [
        {
          "claim": "attributable outcome",
          "evidenceStatus": "DOCUMENTED|USER_CONFIRMED|DRAFT_INFERENCE|UNKNOWN",
          "evidence": [{"sourceId": "id", "excerpt": "short excerpt"}]
        }
      ]
    }
  ],
  "education": [
    {
      "institution": "value",
      "credential": "value",
      "field": "value or UNKNOWN",
      "startDate": "value or UNKNOWN",
      "endDate": "value or UNKNOWN",
      "evidenceStatus": "DOCUMENTED|USER_CONFIRMED|DRAFT_INFERENCE|UNKNOWN",
      "evidence": [{"sourceId": "id", "excerpt": "short excerpt"}]
    }
  ],
  "languages": [
    {
      "language": "value",
      "level": "exactly stated level or UNKNOWN",
      "evidenceStatus": "DOCUMENTED|USER_CONFIRMED|DRAFT_INFERENCE|UNKNOWN",
      "evidence": [{"sourceId": "id", "excerpt": "short excerpt"}]
    }
  ],
  "skills": [
    {
      "name": "normalized skill",
      "contexts": ["experience/project id"],
      "scope": "explicit scope or UNKNOWN",
      "evidenceStatus": "DOCUMENTED|USER_CONFIRMED|DRAFT_INFERENCE|UNKNOWN",
      "evidence": [{"sourceId": "id", "excerpt": "short excerpt"}]
    }
  ],
  "projects": [
    {
      "id": "stable id",
      "name": "value",
      "context": "professional|academic|personal|UNKNOWN",
      "contributions": [],
      "technologies": [],
      "outcomes": [],
      "evidenceStatus": "DOCUMENTED|USER_CONFIRMED|DRAFT_INFERENCE|UNKNOWN",
      "evidence": [{"sourceId": "id", "excerpt": "short excerpt"}]
    }
  ],
  "roleHypotheses": [
    {
      "roleFamily": "value",
      "reason": "grounded explanation",
      "evidenceStatus": "DRAFT_INFERENCE"
    }
  ],
  "conflicts": [
    {
      "field": "conflicting field",
      "claims": [{"value": "value", "sourceId": "id"}],
      "resolution": "UNRESOLVED|USER_CONFIRMED"
    }
  ],
  "unknowns": ["high-impact fact not established"],
  "confirmationQuestions": [
    {
      "id": "stable id",
      "question": "short decision-changing question",
      "options": ["2–3 concise choices"],
      "whyItMatters": "search or hard-constraint impact"
    }
  ]
}

FINAL VALIDATION BEFORE RETURNING JSON
- Every positive claim has DOCUMENTED or USER_CONFIRMED evidence.
- Every inference is labelled DRAFT_INFERENCE.
- Conflicts are preserved.
- No private contact details are retained.
- No more than three confirmation questions are returned.
- Output parses as valid JSON.
```

## Merge rules for an existing evidence file

- Preserve `USER_CONFIRMED` facts unless the user explicitly replaces them.
- Add new sources; do not erase provenance from older still-valid claims.
- When a new document disagrees with an existing fact, create a conflict instead of overwriting it.
- Remove a claim from scoring when its only source has been retracted or superseded.
- Keep stable IDs for unchanged experience and project records.

## Generate `profile.md`

After resolving material conflicts:

1. Render only `DOCUMENTED` and `USER_CONFIRMED` facts as positive evidence.
2. Put useful `DRAFT_INFERENCE` items in a clearly labelled “Pending confirmation” section, not in the verified evidence library.
3. Summarize `UNKNOWN` high-impact facts without converting them into gaps.
4. Record source filenames and user-confirmed facts in the Provenance section.
5. Run the minimal-question flow in [onboarding.md](onboarding.md) when unresolved items affect search coverage or hard constraints.
