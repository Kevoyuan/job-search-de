# 🇩🇪 job-search-de — Universelle Job-Discovery- & Evaluierungs-Pipeline für Deutschland

<p align="center">
  <a href="../README.md"><b>English</b></a> •
  <a href="README_de.md"><b>Deutsch</b></a> •
  <a href="README_zh.md"><b>中文</b></a> •
  <a href="README_ja.md"><b>日本語</b></a> •
  <a href="README_ko.md"><b>한국어</b></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Agent%20Skill-Ready-blue.svg?style=flat-square" alt="Agent Skill" />
  <img src="https://img.shields.io/badge/License-MIT-green.svg?style=flat-square" alt="License" />
</p>

`job-search-de` ist ein universelles, kandidatenneutrales KI-Agent-Skill für die automatisierte Suche, Verifizierung, evidenzbasierte Bewertung und Verwaltung von Stellenangeboten für **alle Berufsfelder in Deutschland** — einschließlich Software Engineering, Data & KI, Marketing, Sales, Finanzen, HR, Operations, Design und Consulting.

---

## Warum job-search-de

| Dimension | Traditionelle Jobbörsen (LinkedIn / StepStone / Indeed) | `job-search-de` Pipeline |
|---|---|---|
| **Aktualität & Echtheit** | 30%–50% sind veraltet, Ghost-Jobs oder Headhunter-Reposts | **100% Live & Verifiziert** (Direkte ATS-API-Abfragen + Schema.org Echtzeitprüfung) |
| **Datenschutz & Privatsphäre** | Lebensläufe werden auf externen Cloud-Servern gespeichert | **100% Lokal & Vertraulich** (Daten verbleiben ausschließlich lokal in `<workdir>/.job-search/`) |
| **Matching-Qualität** | Reine Keyword-Treffer mit vielen Fehlalarmen | **Zweistufiges Evidenzbasiertes Scoring** (Zitiert echte Fakten, keine KI-Halluzinationen) |
| **Bewerbungs-Management** | Manuelle Excel-Tabellen und unübersichtliche Lesezeichen | **Interaktive 4-Theme Workbench** (Kanban, Tabellenfilter, Shortcuts, 1-Klick Pitch Hooks) |
| **Agent-Integration** | Isoliert von modernen KI-Workflows | **Natives Agent-Skill-Protokoll** (Antigravity, Claude Code, Cursor, OpenClaw ready) |

---

## Benutzeroberfläche & Demo

### 4 Design-Themes in Echtzeit (0 Token Reines CSS)
> Nahtloser Wechsel zwischen **Notion Craft (Warm Editorial)**, **Linear Obsidian (Dark Mode)**, **Bauhaus Grid (Industriell Minimal)** und **Bento Quartz (Spatial Glass)** ohne Token-Kosten. Drücken Sie <kbd>1</kbd> / <kbd>2</kbd> / <kbd>3</kbd> / <kbd>4</kbd> zum sofortigen Umschalten.

![Workbench Theme-Wechsler](images/theme-switcher.gif)

---

### 1. Interaktive Tabellen-Datenbankansicht
> Live-Statusverfolgung, mehrdimensionale Filter, Aktualitätsanzeigen und kalibrierte Fit-Scores.

![Workbench Tabellenansicht](images/workbench-table.png)

---

### 2. Bewerbungspipeline-Kanban
> Drag-and-Drop oder statusgesteuertes Lebenszyklusmanagement (Zu bewerben, Beworben, Interview, Angebot, Archiviert).

![Workbench Kanban-Ansicht](images/workbench-kanban.png)

---

### 3. Lokales Kandidatenprofil & Regel-Drawer
> Datenschutzorientierte Architektur: Persönliche Fakten, Einschränkungen, Zielstädte und Konfigurationen verbleiben ausschließlich in Ihrem lokalen `.job-search/`-Verzeichnis.

![Workbench Konfigurations-Drawer](images/workbench-config-drawer.png)

---

### 4. Umfassender Marktbericht
> Multi-regionale Aufschlüsselung (Frankfurt, München, Berlin, Deutschland Remote) mit tiefem JD-zu-Profil-Evidenzabgleich.

![Marktbericht](images/report-overview.png)

---

## Hauptfunktionen

- **Datenschutz an erster Stelle**: Skill-Logik und Kandidatendaten sind strikt entkoppelt. Persönliche Daten und Präferenzen verbleiben ausschließlich lokal in `<workdir>/.job-search/`.
- **4 Design-Themes in Echtzeit**: Nahtloser Wechsel zwischen **Notion Craft (Warm Editorial)**, **Linear Obsidian (Dark Mode)**, **Bauhaus Grid (Industriell Minimal)** und **Bento Quartz (Spatial Glass)** ohne Token-Kosten.
- **Tastatur-Power-Navigation**: Schnelle Navigation mit <kbd>J</kbd>/<kbd>K</kbd>, Aufklappen mit <kbd>Enter</kbd>, Karrierelink öffnen mit <kbd>O</kbd>, Suche mit <kbd>/</kbd> und Themes mit <kbd>1</kbd>/<kbd>2</kbd>/<kbd>3</kbd>/<kbd>4</kbd>.
- **1-Klick-Bewerbungs-Pitch**: Generiert ein maßgeschneidertes Anschreiben-Intro basierend auf den verifizierten Match-Kriterien.
- **Schnellfilter-Chips**: 1-Klick-Filter für `Fit ≥ 85`, `Raum Frankfurt`, `100% Remote`, `Nur Englisch` und `Zu bewerben`.
- **Direkte ATS-Erkennung**: Ruft aktuelle Stellenangebote direkt über offizielle ATS-APIs ab (Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Workable).
- **Automatisierte Validierungs-Pipeline**: Echtzeit-Prüfung von URLs, HTTP-Status und Schema.org JSON-LD Metadaten.
- **Zweistufiges Evidenzbasiertes Scoring**:
  - **Stufe 1 (Schnelle Triage)**: Harte Ausschlusskriterien und Schwellenwert-Filterung.
  - **Stufe 2 (Tiefenabgleich)**: Differenzierung zwischen Muss- und Kann-Kriterien mit Pflicht zur Evidenzzitierung.
- **Interaktive Workbench**: Moderne, rein clientseitige HTML/JS-Oberfläche mit Kanban-Board, Tabellenansicht und optionalem Notion-Sync.
- **Laufzeit-Update-Prüfung**: Automatische Erkennung neuer GitHub-Releases mit Live-Versionsanzeige (`v1.1.1`).

---

## Pipeline-Workflow

```text
         Kandidatenunterlagen (Lebenslauf, LinkedIn, Portfolio)
                                   │
                                   ▼
                   [1. Onboarding & Profilerstellung]
                                   │ (Erzeugt .job-search/profile.md & preferences.md)
                                   ▼
                      [2. Multi-Kanal-Discovery]
                 Direkte ATS-Abfragen + Gezielte Suche
                                   │
                                   ▼
                 [3. Bereinigung & Echtzeitverifikation]
                 Schema.org JSON-LD + HTTP-Statusprüfung
                                   │
                                   ▼
                   [4. Zweistufiges Evidenz-Scoring]
                 Triage-Filter ➔ Profil-Faktenabgleich
                                   │
                                   ▼
                [5. Berichterstellung & Synchronisation]
        Managementbericht + Interaktive HTML-Workbench + Notion
```

---

## Projektstruktur

```text
job-search-de/
├── SKILL.md                  # Agent Skill Einstiegspunkt und Regeln
├── README.md                 # Hauptdokumentation (Englisch)
├── VERSION                   # Semantische Versionierung (z.B. 1.1.1)
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
│   ├── bump_version.py       # Versions-Bumper
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

## Schnellstart

### 1. Skill installieren
```bash
npx skills add Kevoyuan/job-search-de -g
```

### 2. Lebenslauf ablegen
Legen Sie Ihren Lebenslauf (z.B. `resume.pdf`, `CV.md` oder LinkedIn-Export) in Ihrem Arbeitsordner ab.

### 3. Mit KI-Agent ausführen
Geben Sie Ihrem KI-Assistenten (Antigravity, Claude Code, Cursor, OpenClaw) einfach die Anweisung:

> **"Finde passende KI/ML-Stellen in Frankfurt, München oder Remote Deutschland basierend auf meinem Lebenslauf."**

```text
> User: "Finde passende KI/ML-Stellen in Frankfurt oder Remote Deutschland."

Agent:
[1/4] Lebenslauf geparst in .job-search/profile.md (6 verifizierte Skills)
[2/4] ATS-APIs abgefragt (Greenhouse, Lever, Ashby, Personio...) → 42 aktive Stellen
[3/4] URLs und Schema.org-Daten validiert (0 abgelaufene Stellen)
[4/4] JD-Anforderungen mit Fakten abgeglichen:
      • 8 Top-Stellen (Fit ≥ 85)
      • 14 Gute Stellen (70 ≤ Fit < 85)
Managementbericht und interaktive Workbench job-hunt-workbench.html generiert!
```

---

## Unterstützte Befehle

| Befehl | Beschreibung |
|---|---|
| `/refresh` | **Vollständige Aktualisierung**: Führt erneuten ATS-Abruf, Verifizierung, Evidenz-Scoring durch und aktualisiert Workbench & Bericht. |
| `/update-skill` | **Skill-Update**: Lädt die neueste GitHub-Version herunter. |
| `/match <url / jd>` | **Einzelabgleich**: Bewertet eine einzelne Stelle gegen Ihr Profil. |
| `/tailor <id / url>` | **Anschreiben-Generator**: Erzeugt maßgeschneiderte CV-Punkte und deutsches Anschreiben. |
| `/sync` | **Notion-Sync**: Synchronisiert Status mit Ihrer Notion-Job-Datenbank. |
| `/digest` | **Tages-Digest**: Fasst die Top 5 neuen Stellen der letzten 24–48h zusammen. |

---

## Konfiguration & Datenschutz

Alle persönlichen Daten verbleiben ausschließlich in Ihrem lokalen `.job-search/`-Verzeichnis:

<details>
<summary><b>Beispiel <code>.job-search/preferences.md</code> & <code>settings.ini</code></b></summary>

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

## FAQ

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

## Lizenz

Veröffentlicht unter der [MIT-Lizenz](LICENSE).
