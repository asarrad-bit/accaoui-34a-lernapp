# Accaoui §34a Lern-App – Projekt-Masterliste

Stand: v24.3x
Branch: `refactor/oral-exam-module`
Projektordner: `C:\xampp\htdocs\accaoui\v4-dashboard`
Repository: `asarrad-bit/accaoui-34a-lernapp`

---

## 1. Arbeitsregel

Keine Blind-Fixes.

Immer in dieser Reihenfolge arbeiten:

1. Prüfen
2. Klein ändern
3. Browser testen
4. Preflight ausführen
5. Committen
6. Pushen

Vor jedem Commit ausführen:

```bash
python tools/preflight.py
git diff --check
git status --short
```

Nur committen, wenn:

1. Preflight bestanden
2. `git diff --check` keine Ausgabe zeigt
3. nur erlaubte Dateien geändert wurden
4. Browser-Test bestanden ist

Optional bei bewusst freigegebenen Kern-Datei-Änderungen:

```powershell
$env:ACCAOUI_ALLOW_PROTECTED="index.html,app.js"
python tools/preflight.py
```

---

## 2. Cursor-Regel

Cursor bekommt nur enge Aufträge.

Jeder Cursor-Auftrag enthält:

1. Ziel
2. erlaubte Dateien
3. verbotene Dateien
4. konkrete Änderung
5. was nicht geändert werden darf
6. Prüf-Befehle danach
7. kein Commit durch Cursor (außer ausdrücklich gewünscht)
8. keine Zusatzoptimierungen

Cursor darf nicht:

1. große Dateien komplett neu formatieren
2. Zeilenenden ändern
3. mehrere Bereiche gleichzeitig umbauen
4. Refactoring ohne Freigabe machen
5. `test/` ändern, außer ausdrücklich erlaubt

Referenz für neue Chats: `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`

---

## 3. Technische Schutzregeln

Nicht mehr auf großen Dateien verwenden:

```bash
sed -i
```

Betroffene große Dateien:

1. `app.js`
2. `patch-v21.js`
3. `style.css`
4. `questions.json`

Für gezielte Änderungen lieber Python mit Trefferkontrolle verwenden.

`.editorconfig` ist aktiv.

### Preflight-Schutz für Kern-Dateien (ab v23.5.6)

`tools/preflight.py` prüft per `git status --short`, ob geschützte Kern-Dateien geändert wurden:

- `app.js`, `patch-v21.js`, `index.html`, `style.css`
- `oral-exam.css`, `oral-exam.js`, `oral-sheets.js`, `oral-sheets-v23.js`
- `questions.json`
- `data/oral-question-bank.js`, `data/oral-sheets-bank.js`

Bei Treffer ohne Freigabe: Preflight-Fehler mit Hinweis, nur zu committen, wenn die Datei für den Task freigegeben wurde.

Kontrollierte Freigabe: Umgebungsvariable `ACCAOUI_ALLOW_PROTECTED` (kommagetrennte Pfade).

---

## 4. Aktive Hauptdateien

**Der Root-Ordner ist führend.**

**Der Ordner `test/` ist nicht führend und darf nicht als Referenz genutzt werden.**

`index.html` lädt aktiv (Reihenfolge laut Einbindung):

1. `style.css`
2. `oral-exam.css`
3. `app.js`
4. `patch-v21.js`
5. `data/oral-question-bank.js`
6. `data/oral-sheets-bank.js`
7. `oral-sheets.js`
8. `oral-sheets-v23.js`
9. `oral-exam.js`

Weitere führende Dateien im Root:

- `index.html`
- `questions.json`

Werkzeuge (nicht in der App geladen, aber Pflicht vor Commit):

- `tools/preflight.py`
- `tools/audit-categories.py`

---

## 5. Aktueller Versionsstand (bis v24.3x)

### App und mündliche Prüfung (Auszug)

| Version | Inhalt |
|---------|--------|
| v23.4.0 | Mündlicher Fehlertrainer: stabiler Renderer `showOralMistakeTrainingV2340()` |
| v23.4.1 | „FRAGT JETZT“-Badge (Prüfersimulation) |
| v23.4.2 | Fehlerübersicht schriftlich bereinigt |
| v23.4.3 | Kanonische Kategorien + `normalizeCategoryName()` |
| v23.4.4–v23.4.6 | Mündliche/schriftliche Datenquellen und Kategorien normalisiert |
| v23.4.7 | `tools/audit-categories.py` |
| v23.4.8 | `tools/preflight.py` (Basis) |
| v23.5.1 | Simulation B: Button/Start im Modus-Select (Patch) |
| v23.5.2 | Mündliche Prüfung funktional getestet (Simulation A/B, Musterantworten, Bewertung, Fehlertraining, Online-Anzeige) |
| v23.5.6 | Preflight: Schutz geschützter Kern-Dateien + `ACCAOUI_ALLOW_PROTECTED` |

### Dokumentation und Supabase-Planung (v23.5.5–v23.5.10)

| Version | Dokument / Inhalt |
|---------|-------------------|
| v23.5.5 | `docs/QUESTION_DATABASE_PLAN.md` |
| v23.5.5 | `docs/WRITTEN_QUESTION_STANDARD.md` (Vorbereitung) |
| v23.5.7 | `docs/SUPABASE_QUESTION_SCHEMA.md` |
| v23.5.8 | `docs/SUPABASE_USER_PROGRESS_SCHEMA.md` |
| v23.5.9 | `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md` |
| v23.5.10 | `docs/PROJECT_MASTERLIST.md` und `README.md` aktualisiert |
| v23.5.29 | `docs/LEARNING_STRATEGY_MODULE.md` (Vergessenskurve, Lernprinzipien); Prüfungsaufbau § 34a in `PROJECT_MASTERLIST.md` §7 |
| v23.5.48 | Fragenbank-Ausbau abgeschlossen: **86 Fragen** in `questions.json` (inkl. Umgang mit Menschen `umgang_006`–`umgang_019`) |
| v24.0 | `docs/EXAM_SIMULATION_AUDIT.md` – Prüfungssimulation 82/120 auditiert; **kein Code-Task** |
| v24.1 | `docs/EXAM_POINTS_PLAN.md` – Punktefelder fachlich geplant (86 Fragen, Simulationskern 82/120); **keine** `questions.json`-Änderung |
| v24.2 | `docs/EXAM_CORE_SELECTION_PLAN.md` – **Option A:** feste 82 Core-IDs; 4 Reserve-IDs |
| v24.3a–f | `points`-Felder in `questions.json` (Recht, Gewerbe, DS, BGB, Strafrecht, UVV) – **in Arbeit / Teilstände** |
| v24.3x | Teilpunkte-Bewertung ab 01.07.2025 auditiert (`EXAM_SIMULATION_AUDIT.md` §10, `EXAM_POINTS_PLAN.md` §10) – **kein Code** |

**Hinweis:** Supabase ist geplant, aber noch **nicht** in der App eingebunden (kein SQL, keine Live-Verbindung).

---

## 6. Kanonische Kategorien

Feste Reihenfolge (9 Sachgebiete):

1. Recht der öffentlichen Sicherheit und Ordnung
2. Gewerberecht
3. Datenschutzrecht
4. Bürgerliches Gesetzbuch
5. Strafgesetzbuch und Strafverfahrensrecht
6. Unfallverhütungsvorschriften Wach- und Sicherungsdienste
7. Umgang mit Waffen
8. Umgang mit Menschen
9. Grundzüge der Sicherheitstechnik

Alte Begriffe dürfen nur noch als Mapping in `normalizeCategoryName()` stehen.

---

## 7. Sachkundeprüfung nach § 34a GewO – Prüfungsaufbau (Grundlage)

Der offizielle Aufbau der **Sachkundeprüfung nach § 34a GewO** ist für die App-Planung dokumentiert (siehe auch `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` §4, `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md`).

### Schriftliche Prüfung

| Merkmal | Vorgabe |
|---------|---------|
| Aufgaben | **82 geschlossene Aufgaben** |
| Bearbeitungszeit | **120 Minuten** |
| Bestehensgrenze | mindestens **50 Prozent** der Punkte |
| Hilfsmittel | **nicht erlaubt** |
| Mündliche Zulassung | nur bei **bestandenem schriftlichen Teil** |

### Punkte- und Fragengewichtung (schriftlich)

| Nr | Sachgebiet | Fragen | Punkte |
|----|------------|-------:|-------:|
| 1 | Recht der öffentlichen Sicherheit und Ordnung | 7 | 11 |
| 2 | Gewerberecht | 5 | 8 |
| 3 | Datenschutzrecht | 5 | 8 |
| 4 | Bürgerliches Gesetzbuch | 13 | 21 |
| 5 | Strafgesetzbuch und Strafverfahrensrecht | 13 | 21 |
| 6 | Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 | 13 |
| 7 | Umgang mit Waffen | 5 | 8 |
| 8 | Umgang mit Menschen | 19 | 19 |
| 9 | Grundzüge der Sicherheitstechnik | 7 | 11 |
| | **Gesamt** | **82** | **120** |

### Wichtige App-Regel (Fragenbank vs. Prüfung)

Die **Fragenbank** in `questions.json` darf **größer als 82 Fragen** sein (Ziel nach Ausbauplan: **86** Fragen als Pool mit Reserve).

Die **spätere Vollsimulation** der schriftlichen Prüfung soll jedoch **exakt 82 Fragen** nach **Sachgebiet** und **Punktegewichtung** der Tabelle oben ziehen (Zufallsauswahl pro Kategorie aus dem verfügbaren Pool).

**Audit v24.0:** Ist-Stand und Lücken siehe `docs/EXAM_SIMULATION_AUDIT.md`. Aktuell: **86 Fragen**, **keine `points`-Felder** in `questions.json`; Vollsimulation zieht per `shuffleArray` + `slice` – Umsetzung der echten 82/120-Logik erst in **v24.1 ff.**

### Mündliche Prüfung

| Merkmal | Vorgabe |
|---------|---------|
| Dauer | etwa **15 Minuten** |
| Form | **Einzelprüfung** oder **Gruppe bis zu 5 Teilnehmer** |
| Inhalt | häufig **Praxisfälle** |
| Anforderung | **richtiges Verhalten beschreiben** und **rechtlich begründen** |

---

## 8. Lernstrategie-Modul (geplant)

| Aspekt | Stand v23.5.29 |
|--------|----------------|
| Dokument | `docs/LEARNING_STRATEGY_MODULE.md` – **vorhanden** |
| Inhalt | Vergessenskurve, Active Recall, Spaced Repetition, Praxisbezug |
| App-Status | **vorgemerkt**, noch **kein Code** |
| Einbau (später) | farbige Infobox / Modul in **Dashboard**, **Lernkarten** oder **Fehlertraining** |
| Geplante Version | **v24.x** oder **v25.x** |

Kernbotschaft für die App (Beispieltext):

> *Wissen bleibt nicht durch einmaliges Lesen, sondern durch Wiederholung, Anwendung und aktive Abfrage.*

**Hinweis:** Kein sofortiger Code-Task – nur Konzept und Masterlist-Verankerung.

---

## 8.1 UX- und Lernlogik-Audit (geplant, v24.x)

| Aspekt | Stand |
|--------|--------|
| App-Status | **vorgemerkt**, noch **kein Code** |
| Geplante Version | **v24.x** |
| Voraussetzung | Abschluss des **Fragenbank-Ausbaus** (86-Fragen-Pool) |

### Inhalt des Audits

1. **Ergebnisdarstellung** prüfen und vereinheitlichen.
2. **Unterschied zwischen Lernmodus und Lernkarten** klar erklären:
   - **Lernmodus** = echte Wissensabfrage mit richtig/falsch.
   - **Lernkarten** = Selbsteinschätzung mit gewusst/wiederholen/offen.
3. In der App später einen kurzen Hinweis ergänzen:
   > *Lernmodus prüft Ihre Antworten. Lernkarten bewerten Ihre Selbsteinschätzung.*
4. **Themenbereich-Üben:** Nächste Frage erst nach Antwort grundsätzlich beibehalten, weil dies **Active Recall** unterstützt.
5. **Optional später prüfen:**
   - Button „Frage später beantworten“
   - Button „Überspringen und später üben“
   - offene Fragen separat speichern
   - offene Fragen gezielt nachtrainieren
6. **Ziel:** Lernlogik verständlicher machen, **ohne** die aktuelle stabile Funktion zu verändern.

**Hinweis:** Kein Sofort-Code-Task. Umsetzung erst nach Abschluss des Fragenbank-Ausbaus.

---

## 8.2 Prüfungssimulation 82/120 (Audit v24.0)

| Aspekt | Stand v24.0 |
|--------|-------------|
| Dokument | `docs/EXAM_SIMULATION_AUDIT.md` – **vorhanden** |
| Fragenbank | **86 Fragen** in `questions.json` (Pool-Ziel erreicht) |
| `points`-Felder | **teilweise** in `questions.json` (v24.3a–f); App nutzt Fallback 1 Punkt wo fehlend |
| Vollsimulation (Ist) | 82 Fragen per Zufall aus Gesamtpool – **ohne** Sachgebiets- und Punktegewichtung |
| Vollsimulation (Soll) | **82 Fragen / 120 Punkte** nach Sachgebietstabelle §7 |
| Punkteplan | `docs/EXAM_POINTS_PLAN.md` – **vorhanden** (v24.1, fachliche Zuordnung 1/2 Punkte) |
| Core-ID-Plan | `docs/EXAM_CORE_SELECTION_PLAN.md` – **vorhanden** (v24.2, **Option A:** feste 82 Kern-IDs) |
| `points`-Felder in JSON | **teilweise** (v24.3a–f); Rest in **v24.4** |
| Teilpunkte-Audit | **v24.3x** – siehe §8.3; App-Umsetzung **v24.5** |
| App-Status | Timer (120 min) und Bestehen (50 %) vorhanden; **Teilpunkte** und **Core-Auswahl** folgen in v24.4–v24.6 |

### Empfohlene Folge-Tasks

- **v24.3a–f** – `points`-Felder je Sachgebiet (nach `EXAM_POINTS_PLAN.md`) – **teilweise erledigt**
- **v24.3x** – Teilpunkte-Audit dokumentiert – siehe §8.3
- **v24.4** – restliche `points`-Felder + Core-ID-Auswahl in App
- **v24.5** – Teilpunkte-Logik umsetzen
- **v24.6** – Vollsimulation 82/120 mit Teilbewertung testen

**Hinweis:** Audit-Dokumentation (v24.0, v24.1, v24.2, v24.3x) ohne App-Code; `points` in JSON separat (v24.3a–f / v24.4).

---

## 8.3 Teilpunkte-Bewertung (Audit v24.3x)

| Aspekt | Stand |
|--------|--------|
| Gültig ab | **01.07.2025** – teilrichtige Antworten zählen |
| Regel | Pro **richtige Lösung** 1 Punkt; max. schriftlich **120**; Bestehen **60** (50 %) |
| `points`-Feld | Soll **Anzahl richtiger Antworten** abbilden (1 oder 2 in der Regel) |
| App (Ist) | Auswertung noch **binär** bei Mehrfachantworten – **Teilpunkte offen** |
| Dokumentation | `docs/EXAM_SIMULATION_AUDIT.md` §10, `docs/EXAM_POINTS_PLAN.md` §10 |
| Offen | Falsche Zusatzkreuze: ignorieren vs. Abzug – **fachlich vor v24.5** |
| Vorläufige Code-Regel | Single: voll/0 · Multiple: +1 pro richtigem Kreuz, keine Belohnung falscher Zusatzantworten |

### Roadmap (Teilpunkte und Vollsimulation)

| Task | Inhalt |
|------|--------|
| **v24.3x** | Teilpunkte-Bewertung **dokumentiert** (dieser Abschnitt) |
| **v24.4** | Restliche `points`-Felder in `questions.json` fertigstellen |
| **v24.5** | Teilpunkte-Logik technisch prüfen und umsetzen |
| **v24.6** | Vollsimulation 82/120 **mit Teilbewertung** testen |

**Kein Code-Task in v24.3x.**

---

## 9. Prüfskripte

Kategorie-Audit:

```bash
python tools/audit-categories.py
```

Preflight (Pflicht vor jedem Commit):

```bash
python tools/preflight.py
```

---

## 10. Planungsdokumente (Stand v24.3x)

| Dokument | Status |
|----------|--------|
| `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` | Master-Kontext, Roadmap v24–v28, Prüfungsaufbau §4 |
| `docs/WRITTEN_QUESTION_STANDARD.md` | Schriftlicher Fragenstandard – **vorhanden** |
| `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md` | Ausbau 51 → 86 Fragen, Prüfungsziel 82 – **vorhanden** (Pool **86** erreicht) |
| `docs/EXAM_SIMULATION_AUDIT.md` | Prüfungssimulation 82/120 – **vorhanden** (Audit v24.0, kein Code) |
| `docs/EXAM_POINTS_PLAN.md` | Punktevergabe 1/2 pro Frage, Simulationskern 82/120 – **vorhanden** (Plan v24.1, kein JSON) |
| `docs/EXAM_CORE_SELECTION_PLAN.md` | Feste 82 Core-IDs, 4 Reserve – **vorhanden** (Plan v24.2, Option A, kein Code) |
| `docs/QUESTION_DATABASE_PLAN.md` | Fragen-Datenbank, Review, Export – **vorhanden** |
| `docs/LEARNING_STRATEGY_MODULE.md` | Lernstrategie, Vergessenskurve – **vorhanden** (Konzept, kein Code) |
| `docs/SUPABASE_QUESTION_SCHEMA.md` | Supabase-Fragenmodell – **vorhanden** |
| `docs/SUPABASE_USER_PROGRESS_SCHEMA.md` | Nutzer, Kurse, Fortschritt – **vorhanden** |
| `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md` | Umsetzungsreihenfolge Supabase – **vorhanden** |
| `docs/PROJECT_MASTERLIST.md` | Diese Datei |

---

## 11. Funktionaler Teststand

| Bereich | Status |
|---------|--------|
| Schriftlicher Prüfungsmodus | **getestet** (Simulation, Statistik, Historie, Fehlertraining) |
| Mündliche Prüfung | **getestet** (Training, Simulation, Bewertung, Fehlertraining) |
| Simulation A | **vorhanden** (15-Minuten-Bogen) |
| Simulation B | **vorhanden** (Prüfungsbogen B) |
| Lernkarten | vorhanden – **vollständiger Retest empfohlen** |
| Schriftliche Fragenbank | **86 Fragen** in `questions.json` (Pool-Ziel erreicht); Prüfung zieht **82** nach Gewichtung – **noch nicht umgesetzt** |
| Prüfungssimulation 82/120 | **auditiert** (v24.0), Punkte/Core-IDs geplant, **Teilpunkte auditiert** (v24.3x) – siehe `docs/EXAM_*`; App-Teilpunkte **v24.5** |
| Lernstrategie-Modul | **geplant** – siehe `docs/LEARNING_STRATEGY_MODULE.md` |
| UX- und Lernlogik-Audit | **geplant** – siehe §8.1 (v24.x) |

Langfristiges Ziel mündlich: skalierbare Bogen-Auswahl A/B/C/D unter einem Hauptmodus „Prüfungssimulation“ (siehe v24 Oral Exam Cleanup).

---

## 12. Mündlicher Fehlertrainer

Führend ist:

`showOralMistakeTrainingV2340()`

Alte Funktionen werden auf den neuen Renderer umgeleitet:

1. `showOralMistakeTrainingV2324`
2. `showOralMistakeTrainingV2325`
3. `showOralMistakeTrainingV2326`

Keine weiteren Hotfixes an alten mündlichen Fehlertrainer-Renderern.

---

## 13. Werkzeuge (Entwicklungsumgebung)

Installiert (Referenz):

1. Node.js v24.16.0
2. npm 11.13.0
3. Python 3.13.3

---

## 14. Nächste sinnvolle Aufgaben

1. **Prüfungssimulation 82/120** – Punkteplan, Core-IDs und **Teilpunkte-Audit** (v24.3x) **dokumentiert**; als Nächstes: restliche `points` (v24.4), Teilpunkte-Code (v24.5), Test (v24.6); siehe §8.2 / §8.3
2. **Lernstrategie-Modul** – Vergessenskurve als UI-Modul (v24.x/v25.x), siehe `docs/LEARNING_STRATEGY_MODULE.md` – **kein sofortiger Code-Task**
3. **UX- und Lernlogik-Audit** – Ergebnisdarstellung, Lernmodus vs. Lernkarten, Active Recall (v24.x), siehe §8.1 – **kein sofortiger Code-Task**
4. **Lernkarten vollständig testen** – Fortschritt, Wiederholung, Kategorien
5. **Später v24 Oral Exam Cleanup** – Patch-Schichten reduzieren, einheitliche Bogenlogik A/B/C
6. **Spätere SQL-Planung** – Phase 2 laut `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md`
7. **Später Datenschutz / Rechtstexte** – Impressum, Datenschutz, Nutzungsbedingungen (v26)
8. **Später Supabase / Login** – Auth, Kurse, Fortschritt pro `user_id` (v27, Roadmap Phase 3–6)

**Erledigt:** Fragenbank-Ausbau auf **86 Fragen** (v23.5.48, Umgang mit Menschen komplett importiert).

Optional parallel: Projektstruktur gegen alte Kopien prüfen; mündliche Prüfung später als erweiterter Prüfermodus.

---

## 15. Start in neuem Chat

Zuerst nennen:

```txt
docs/PROJECT_MASTERLIST.md
docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md
docs/WRITTEN_QUESTION_STANDARD.md
docs/WRITTEN_QUESTION_EXPANSION_PLAN.md
docs/LEARNING_STRATEGY_MODULE.md
docs/EXAM_SIMULATION_AUDIT.md
docs/EXAM_POINTS_PLAN.md
docs/EXAM_CORE_SELECTION_PLAN.md
docs/QUESTION_DATABASE_PLAN.md
docs/SUPABASE_IMPLEMENTATION_ROADMAP.md
```

Dann ausführen:

```bash
git status
git log -1 --oneline
python tools/preflight.py
```

Keine Änderung ohne sauberen Arbeitsstand.

v23.5.12
Lernkarten funktional getestet und Layout-Fix umgesetzt. Lange Fragen, Antwortansicht, Erklärungen, Buttons, Gewusst/Nicht gewusst und Wiederholen-Karten werden sauber dargestellt.