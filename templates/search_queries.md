# Config-driven German job-search query builder

Read target role families, locations, languages, employers and channels from `.job-search/preferences.md`. Do not assume Frankfurt, Munich, AI engineering or any other candidate-specific target unless configured.

## 1. Primary-location gap fill

For every primary location, combine:

```text
"{ROLE_TITLE}" "{PRIMARY_LOCATION}"
"{ROLE_KEYWORD}" "{PRIMARY_LOCATION}" Stellenangebot
site:{VERTICAL_PORTAL} "{ROLE_KEYWORD}" "{PRIMARY_LOCATION}"
```

Run enough variants to cover English and German title forms relevant to the configured role family.

## 2. Satellite-city matrix

When the candidate accepts a metro area, expand the primary city into configured commuter cities. Check same-name towns and state/region ambiguity before assigning a location tier.

## 3. Remote and Germany-wide scope

```text
"{ROLE_TITLE}" remote Germany
"{ROLE_TITLE}" remote Deutschland
"{ROLE_KEYWORD}" Germany
```

Verify that “remote” actually permits work from the candidate's configured residence.

## 4. Role-family variants

Generate variants from the configured families. Examples:

- engineering: AI Engineer, Machine Learning Engineer, Applied Scientist
- GenAI/agentic: Agentic AI, LLM, GenAI, RAG, AI Agent
- solutions: Solutions Engineer, Forward Deployed Engineer, Consultant, Architect
- domain: Industrial AI, Financial AI, Health AI, Scientific ML

These are examples, not mandatory targets.

## 5. Priority employer scans

```text
site:{CAREERS_DOMAIN} ({ROLE_TERMS})
"{EMPLOYER}" ({ROLE_TERMS}) jobs Germany
```

Use the employer list in `preferences.md`; do not carry another user's watchlist into the run.

## 6. Startup and vertical portals

Search only configured or contextually relevant portals. Useful German-market examples include JOIN, GermanTechJobs, WeAreDevelopers, DEVjobs.de, DataBerlin, get-in-it.de and Arbeitsagentur Jobsuche.

## 7. Direct links and mirrors

User-provided links have highest verification priority. Treat LinkedIn, StepStone, Indeed, Glassdoor and recruiter mirrors as discovery leads; locate an official careers or ATS page when possible.
