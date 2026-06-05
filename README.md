# Accaoui §34a Lern-App

Professionelle **Web-Lern- und Prüfungsplattform** für Teilnehmer der Accaoui Bildung zur Vorbereitung auf die Sachkundeprüfung nach **§ 34a GewO** (Wach- und Sicherheitsgewerbe).

Trainingscharakter: **keine offizielle IHK-Prüfung**, eigene Accaoui-Fragen und Bewertungslogik.

---

## Hauptfunktionen

| Modul | Beschreibung |
|--------|----------------|
| **Dashboard** | Einstieg und Übersicht |
| **Statistik** | Themen- und Gesamtauswertung |
| **Alle Fragen** | Üben nach Sachgebieten |
| **Lernkarten** | Wiederholung mit Fortschritt |
| **Prüfung** | Schriftliche Prüfungssimulation |
| **Fehlertraining** | Wiederholung falsch beantworteter Fragen |
| **Mündliche Prüfung** | Training, Musterantworten, Bewertung |
| **Simulation A / B** | 15-Minuten-Prüfungssituationen mit Prüferrollen |

---

## Entwicklungsstand

- **Lokale Web-App** im Root-Ordner (`index.html` + JavaScript), XAMPP oder statischer Server
- **Aktueller Branch:** `refactor/oral-exam-module`
- **Speicherung heute:** `localStorage` im Browser (Übergangslösung)
- **Geplant:** Supabase (Auth, Kurse, Fortschritt, Fragen-Workflow) – siehe `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md`
- **Später möglich:** PWA / App Store (nach Rechtstexten und Datenschutz)

Führend ist der **Root-Ordner**; `test/` ist keine Referenz für Produktion.

---

## Schutzregeln (kurz)

1. **Keine offiziellen IHK- oder Musterfragen 1:1** – nur eigene **Accaoui-Trainingsfragen**
2. **Preflight vor jedem Commit:** `python tools/preflight.py`
3. **Geschützte Kern-Dateien** (z. B. `app.js`, `questions.json`, `data/`) – Preflight warnt bei ungeplanten Änderungen (ab v23.5.6)
4. Kein Service-Role-Key und keine Supabase-Secrets im Frontend

Details: `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`, `docs/PROJECT_MASTERLIST.md`

---

## Technische Basis

- **Frontend:** HTML, CSS, JavaScript (`app.js`, `patch-v21.js`, mündliche Module)
- **Daten:** `questions.json`, `data/oral-question-bank.js`, `data/oral-sheets-bank.js`
- **Qualitätssicherung:** Python (`tools/preflight.py`, `tools/audit-categories.py`)
- **Roadmap:** Postgres/Supabase, Row Level Security, optional PWA/Capacitor

---

## Dokumentation

| Thema | Datei |
|--------|--------|
| Projektstand & Aufgaben | `docs/PROJECT_MASTERLIST.md` |
| Cursor / Gesamtkontext | `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` |
| Schriftliche Fragen | `docs/WRITTEN_QUESTION_STANDARD.md` |
| Fragen-DB & Review | `docs/QUESTION_DATABASE_PLAN.md` |
| Supabase-Planung | `docs/SUPABASE_QUESTION_SCHEMA.md`, `docs/SUPABASE_USER_PROGRESS_SCHEMA.md`, `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md` |

---

## Schnellstart (lokal)

1. Repository nach `htdocs` oder gewünschten Webroot legen
2. Im Browser `index.html` öffnen (z. B. über XAMPP)
3. Vor Commits: `python tools/preflight.py` und `git diff --check`

---

## Lizenz / Hinweis

Internes Accaoui-Bildungsprojekt. Inhalte und Rechtstexte (Impressum, Datenschutz) werden vor breitem Rollout und App-Store ergänzt (geplant v26/v28).
