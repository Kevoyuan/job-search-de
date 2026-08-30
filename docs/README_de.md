# 🇩🇪 job-search-de — KI-gestützte Pipeline zur Jobsuche & -bewertung in Deutschland

<p align="center">
  <a href="../README.md"><b>English</b></a> •
  <a href="README_de.md"><b>Deutsch</b></a> •
  <a href="README_zh.md"><b>中文</b></a> •
  <a href="README_ja.md"><b>日本語</b></a> •
  <a href="README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-Bereit-blue.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/Zielmarkt-Deutschland%20KI%2FTech-emerald.svg?style=flat-square" alt="Zielmarkt" />
  <img src="https://img.shields.io/badge/Bewertung-Evidenzbasiert-purple.svg?style=flat-square" alt="Bewertungsmethode" />
  <img src="https://img.shields.io/badge/Lizenz-MIT-green.svg?style=flat-square" alt="Lizenz" />
</p>

Ein intelligenter, kandidatenneutraler KI-Agenten-Skill und eine automatisierte Pipeline zur Entdeckung, Verifikation, zweistufigen evidenzbasierten Bewertung, Berichterstellung und Verwaltung von Tech- und KI-Positionen in Deutschland.

---

## 🥊 Warum `job-search-de` vs. Traditionelle Jobbörsen

| Dimension | Traditionelle Jobbörsen (LinkedIn / StepStone / Indeed) | 🇩🇪 `job-search-de` Pipeline |
|---|---|---|
| **Aktualität & Echtheit** | 30%–50% sind veraltet, Ghost-Jobs oder Headhunter-Reposts | **100% Live & Verifiziert** (Direkte ATS-API-Abfragen + Schema.org Echtzeitprüfung) |
| **Datenschutz & Privatsphäre** | Lebensläufe werden auf externen Cloud-Servern gespeichert | **100% Lokal & Vertraulich** (Daten verbleiben ausschließlich lokal in `<workdir>/.job-search/`) |
| **Matching-Qualität** | Reine Keyword-Treffer mit vielen Fehlalarmen | **Zweistufiges Evidenzbasiertes Scoring** (Zitiert echte Fakten, keine KI-Halluzinationen) |
| **Bewerbungs-Management** | Manuelle Excel-Tabellen und unübersichtliche Lesezeichen | **Interaktive 4-Theme Workbench** (Kanban, Tabellenfilter, Shortcuts, 1-Klick Pitch Hooks) |
| **Agent-Integration** | Isoliert von modernen KI-Workflows | **Natives Agent-Skill-Protokoll** (Antigravity, Claude Code, Cursor, OpenClaw ready) |

---

## 📸 Demo & Benutzeroberfläche

### 🎨 4-Design-Themes in Echtzeit (0 Token Reines CSS)
> Nahtloser Wechsel zwischen **Notion Craft**, **Linear Obsidian**, **Bauhaus Grid** und **Bento Quartz**.

![Workbench Theme-Wechsler](images/theme-switcher.gif)

---

### 1. Interaktive Job-Workbench im Notion-Stil (Tabellenansicht)
> Echtzeit-Statusverfolgung, mehrdimensionale Filter, Frische-Indikatoren und kalibrierte Passungs-Scores.

![Workbench Tabellenansicht](images/workbench-table.png)

---

### 2. Bewerbungs-Pipeline-Kanban
> Visuelles Lifecycle-Management für Bewerbungen (Offen, Beworben, Interview, Angebot, Archiviert).

![Workbench Kanban-Ansicht](images/workbench-kanban.png)

---

### 3. Lokales Kandidatenprofil & Einstellungs-Drawer
> Kandidatenneutrale Architektur: Persönliche Daten, Einschränkungen, Zielstädte und Auslieferungseinstellungen verbleiben sicher im lokalen Verzeichnis `.job-search/`.

![Workbench Einstellungs-Drawer](images/workbench-config-drawer.png)

---

### 4. Umfassender Analysebericht
> Regionale Aufschlüsselung (Frankfurt, München, Berlin, Remote Deutschland, strategische Ausnahmen) mit tiefgehendem Abgleich zwischen Anforderungsprofil und Kandidatenevidenz.

![Analysebericht](images/report-overview.png)

---

## 🌟 Hauptfunktionen

- 🎯 **Datenschutz & Kandidatenneutralität**: Die Skill-Logik ist vollständig von individuellen Profildaten entkoppelt. Alle persönlichen Daten liegen lokal unter `<workdir>/.job-search/`.
- 🔍 **Direkte ATS-Schnittstellen**: Durchsucht offizielle Bewerbermanagementsysteme (Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable) direkt – ohne Verzögerungen durch Drittanbieter-Jobbörsen.
- ⚡ **Automatisierte Verifikation**: Echtzeit-Prüfung von URLs, HTTP-Status und strukturierte Schema.org JSON-LD-Extraktion (`datePosted`, `validThrough`, Einstellungsstatus).
- 📊 **Kalibrierte zweistufige Evidenzbewertung**:
  - **Stufe 1 (Schnelltriage)**: Direkter Ausschluss unpassender Rollen nach Seniorität, Gehalt und harten Kriterien.
  - **Stufe 2 (Tiefenabgleich JD ➔ Profil)**: Strikte Trennung von Muss- und Kann-Kriterien mit Zitierung verifizierter Nachweise aus dem Profil.
- 🗂️ **Interaktive Notion-Style Workbench**: Moderne, rein clientseitige HTML/JS-Arbeitsumgebung mit Kanban-Board, Tabellenansicht, dynamischen Filtern und optionaler Notion-Synchronisation.
- 📑 **Mehrsprachige Berichterstellung**: Automatisch generierte strukturierte Markdown- und HTML-Berichte nach regionalen Prioritäten.

---

## 🔄 Workflow-Pipeline

```text
       Kandidatendokumente (Lebenslauf, LinkedIn, Portfolio)
                          │
                          ▼
            [1. Onboarding & Extraktion]
                          │ (Erstellt .job-search/profile.md & preferences.md)
                          ▼
              [2. Mehrkanal-Recherche]
         Direkte ATS-Abfragen + Gezielte Web-Suchen
                          │
                          ▼
         [3. Normalisierung & Verifikation]
         Schema.org JSON-LD + HTTP-Datumsprüfung
                          │
                          ▼
         [4. Zweistufige Evidenzbewertung]
      Triage-Filter ➔ Tiefenabgleich JD gegen Fakten
                          │
                          ▼
          [5. Berichterstellung & Übergabe]
     Management-Report + Interaktive Workbench + Notion
```

---

## 📁 Repository-Struktur

```text
job-search-de/
├── SKILL.md                  # Agent Skill Einstiegspunkt und Regeln
├── README.md                 # Hauptdokumentation (Englisch)
├── VERSION                   # Semantische Versionierung (z.B. 1.1.0)
├── assets/
│   └── config-template/      # Konfigurationsvorlagen
│       ├── profile.md        # Verifiziertes Kandidatenprofil
│       ├── preferences.md    # Sucheinschränkungen & Zielvorgaben
│       └── settings.ini      # Schwellenwerte & Suchfenster
├── configs/
│   ├── boards.txt            # Überwachte ATS-Unternehmensliste
│   ├── keywords.txt          # Suchbegriffe & Rollen-Keywords
│   └── profile.md            # Referenz-Profilspezifikation
├── references/
│   ├── configuration.md      # Konfigurationsverträge
│   ├── onboarding.md         # Onboarding-Richtlinien
│   ├── resume-parser.md      # Regeln zur Lebenslauffakten-Extraktion
│   ├── scoring.md            # Evidenzbasiertes Scoring-Modell
│   └── workbench.md          # Workbench-Integrationsvertrag & Theme-System
├── scripts/
│   ├── bump_version.py       # Auto semantic version bumper
│   ├── check_update.py       # Versionsprüfer gegen GitHub
│   ├── update_skill.sh       # Ein-Befehl-Skill-Aktualisierer
│   ├── download.sh           # Batch-Downloader für ATS-APIs
│   ├── parse_ats.py          # ATS-Daten-Parser und Normalisierer
│   ├── verify.sh             # Job-URL- und Metadaten-Validator
│   ├── init_config.py        # Lokale Vorlageninitialisierung
│   ├── build_html.sh         # Workbench-Build-Skript
│   └── fix_html.py           # HTML-Report-Daten-Injektor
├── templates/
│   ├── agent_prompt_common.md# Standardisierte Prompt-Blöcke
│   ├── report_skeleton.md    # Report-Vorlage
│   └── search_queries.md     # Suchabfrage-Matrizen
└── docs/
    ├── README_zh.md          # Chinesische Dokumentation (中文)
    ├── README_de.md          # Deutsche Dokumentation (Diese Datei)
    ├── README_ja.md          # Japanische Dokumentation (日本語)
    ├── README_ko.md          # Koreanische Dokumentation (한국어)
    └── images/               # Demo-Screenshots und animiertes Theme-GIF
```

---

## 🚀 Schnellstart (In 3 einfachen Schritten)

### 1. Skill installieren
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. Lebenslauf im Arbeitsverzeichnis ablegen
Legen Sie Ihren Lebenslauf (z. B. `resume.pdf`, `CV.md` oder LinkedIn-Export) im Arbeitsordner ab.

### 3. KI-Agenten beauftragen
Geben Sie Ihrem KI-Assistenten einfach folgende Anweisung:

> **"Finde aktuelle KI/ML-Stellen in Frankfurt, München oder Remote Deutschland, die zu meinem Lebenslauf passen."**

Der Agent übernimmt den gesamten Ablauf vollautomatisch:
1. 📄 **Profil erstellen**: Extrahiert Fakten in das lokale `.job-search/profile.md`.
2. 🔍 **Live-Recherche**: Zieht aktuelle Stellen direkt aus Greenhouse, Lever, Ashby, Personio etc.
3. ⚡ **Echtzeit-Verifikation**: Prüft URLs und Veröffentlichungsdaten via Schema.org.
4. 📊 **Evidenzbewertung**: Gleicht Anforderungen mit den verifizierten Profil-Fakten ab.
5. 🗂️ **Auslieferung**: Erstellt den Management-Bericht und aktualisiert die interaktive HTML-Workbench.

<details>
<summary><b>🛠️ Manuelle CLI-Befehle (Optional für Entwickler)</b></summary>

Falls Sie die Skripte manuell ohne Agenten ausführen möchten:

```bash
# Lokale Vorlagen initialisieren
python3 ~/.agents/skills/job-search-de/scripts/init_config.py --workdir .

# ATS-Stellen herunterladen und parsen
bash ~/.agents/skills/job-search-de/scripts/download.sh --workdir .
python3 ~/.agents/skills/job-search-de/scripts/parse_ats.py --today $(date +%Y-%m-%d) --workdir .

# URLs validieren
bash ~/.agents/skills/job-search-de/scripts/verify.sh urls.txt
```
</details>

---

## ⚡ Verfügbare Befehle (Commands)

Diese Befehle können Sie direkt im Dialog mit Ihrem KI-Agenten nutzen:

| Befehl | Beschreibung |
|---|---|
| `/refresh` | **Frische Suche starten**: Führt vollständigen ATS-Abruf, Verifikation, Evidenzbewertung und Workbench-Update durch. |
| `/update-skill` | **Skill aktualisieren**: Zieht automatisch die neuesten Updates von GitHub via `npx skills update job-search-de -g`. |
| `/match <URL / JD>` | **Sofort-Match**: Gleicht eine beliebige Stellenanzeige direkt mit den Fakten Ihres Profils ab. |
| `/tailor <ID / URL>` | **Lebenslauf & Anschreiben**: Generiert maßgeschneiderte CV-Punkte und ein deutsches Anschreiben basierend auf verifizierten Fakten. |
| `/sync` | **Notion-Synchronisation**: Gleicht Bewerbungsstatus bidirektional mit der Notion-Datenbank ab. |
| `/digest` | **Tagesüberblick**: Fasst die Top 5 der neu veröffentlichten Stellen der letzten 24–48 Stunden zusammen. |

---

## ⚙️ Lokale Konfiguration (`.job-search/`)

Alle persönlichen Kandidatendaten verbleiben ausschließlich in Ihrem lokalen `.job-search/`-Verzeichnis:

<details>
<summary><b>📂 Beispiel <code>.job-search/preferences.md</code> & <code>settings.ini</code></b></summary>

```markdown
# Präferenzen (.job-search/preferences.md)

- **Zielrollen:** Senior AI Engineer, Machine Learning Engineer
- **Zielregionen:** Frankfurt am Main, Deutschland (100% Remote)
- **Mindest-Fit-Score:** 75
- **Sprachen:** Verhandlungssicheres Englisch (B2 Deutsch)
```

```ini
# Einstellungen (.job-search/settings.ini)
[scoring]
fit_threshold = 75
require_direct_ats = true

[delivery]
workbench_language = de
auto_open_browser = true
```
</details>

---

## ❓ Häufig gestellte Fragen (FAQ)

<details>
<summary><b>1. Benötige ich kostenpflichtige LinkedIn- oder Scraping-APIs?</b></summary>

**Nein.** Die Pipeline verbindet sich direkt mit den offiziellen, öffentlichen ATS-Karriere-Endpunkten (Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable) der rekrutierenden Unternehmen.
</details>

<details>
<summary><b>2. Werden meine Daten oder mein Lebenslauf auf externe Server hochgeladen?</b></summary>

**Nein.** Das Parsing, der Faktenabgleich und das Rendering der Workbench erfolgen vollständig lokal in Ihrer Arbeitsumgebung. Es gibt keine Telemetrie.
</details>

<details>
<summary><b>3. Kann ich Zielstädte oder Suchbegriffe anpassen?</b></summary>

**Ja.** Bearbeiten Sie einfach `.job-search/preferences.md` oder `.job-search/settings.ini` lokal.
</details>

---

## 📄 Lizenz

Veröffentlicht unter der [MIT-Lizenz](LICENSE).
