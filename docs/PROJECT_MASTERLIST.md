# Accaoui §34a Lern-App – Projekt-Masterliste

Stand: v25.8b
Branch: `main`
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

### Projektarbeitsregel: Arbeit / Zuhause

Bevor an der Accaoui §34a Lern-App gearbeitet wird, zuerst fragen:

> **„Bist du gerade auf Arbeit oder zuhause?“**

Danach immer klären:

1. richtiger Laptop / richtiger Arbeitsstand
2. `git status` prüfen
3. `git pull --ff-only` ausführen
4. nach der Arbeit **Commit + Push** nicht vergessen

Details: `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md` → Arbeitsworkflow / Git-Synchronisation.

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

### Kennzeichnungs- und Sicherheitsregel

1. Cursor-Aufträge immer mit **„NUR FÜR CURSOR – NICHT IN GIT BASH“** kennzeichnen.
2. Git-Bash-Befehle immer mit **„NUR IN GIT BASH AUSFÜHREN“** kennzeichnen.
3. Cursor darf **keinen Commit** und **keinen Push** ausführen (außer ausdrücklich vom Nutzer gewünscht).

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

## 5. Aktueller Versionsstand (bis v25.8b)

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
| v24.3a–i | `points`-Felder in `questions.json` für alle **9 Sachgebiete** vollständig gesetzt |
| v24.3j | Globaler `points`-Check: **82 Core-Fragen / 120 Punkte / 38 Zweipunktfragen** erfolgreich |
| v24.3x | Teilpunkte-Bewertung ab 01.07.2025 auditiert (`EXAM_SIMULATION_AUDIT.md` §10, `EXAM_POINTS_PLAN.md` §10) – **Dokumentation** |
| v24.4b | Vollsimulation nutzt feste **82-Core-Fragen** (`EXAM_CORE_QUESTION_IDS_V244` in `app.js`) |
| v24.5 | Teilpunkte-Logik für Mehrfachantworten im Prüfungsmodus eingebaut (+1 pro richtigem Kreuz) |
| v24.6b | Wiederholungslogik/offene Fragen nach Prüfung; frühe Abgabe; offene Fragen in Auswertung sichtbar – **erledigt** |
| v24.6d | Fragenreihenfolge in Lern-/Wiederholungs-/Fehlermodi wird gemischt – **erledigt** |
| v24.6e | Antwortreihenfolge wird gemischt; korrekte Indizes intern korrekt; `questions.json` unverändert – **erledigt** |
| v24.6f | Prüfungsanalyse responsive stabil (Desktop/Mobile, keine Überlappung) – **erledigt** |
| v24.6g | Fehlerübersicht nach Themen: Premium-Kartenlook, responsive stabil – **erledigt** |
| v24.6x | Prüfungsanalyse optisch/funktional verbessert; Buttontexte; nutzerfreundlicher – **erledigt** |
| v24.6c | Prüfung pausieren / Prüfung fortsetzen; aktive Prüfung wird in `localStorage` gespeichert; Dashboard-Karte „Angefangene Prüfung“; nach Abgabe wird die aktive Session gelöscht – **erledigt** |
| v24.6a | Doppelten Button „Prüfung pausieren“ in der Vollsimulation entfernt; nur ein Pause-Button bleibt sichtbar – **erledigt** |
| v24.7a | Prüfungsnavigation kompakter/einklappbar: 82 Zahlen nicht dauerhaft sichtbar; Summary zeigt aktuelle Frage, beantwortete und offene Fragen; Fragenübersicht per Button ein-/ausblendbar – **erledigt** |
| v24.7b | Lernmodus pausieren / fortsetzen: aktive Lerneinheit wird in `localStorage` gespeichert; Dashboard-Karte „Angefangene Lerneinheit“; Button „Lernen pausieren“ neben „Auswertung anzeigen“; gespeicherte Lerneinheit kann fortgesetzt oder gelöscht werden – **erledigt** |
| v24.7c | Lernmodus-Fortsetzen stabilisiert: ausgewählte Antworten bleiben nach Pause/Fortsetzen sichtbar; bereits ausgewertete Fragen stellen Erklärung, Markierungen und „Nächste Frage“ korrekt wieder her – **erledigt** |
| v24.7d | Automatisches Sicherheits-Speichern bei App-Verlassen: laufende Prüfung oder Lerneinheit wird bei Tab-Wechsel, Browser-Hintergrund, Neuladen oder Schließen automatisch in `localStorage` gesichert – **erledigt** |
| v24.7e | Auto-Save Feintest bestanden: Lernmodus bei Tab-Wechsel, Lernmodus bei Browser-Neuladen und Prüfung bei Browser-Neuladen wurden erfolgreich getestet; Dashboard-Karten „Angefangene Lerneinheit“ und „Angefangene Prüfung“ erscheinen korrekt – **erledigt** |
| v24.8 | Auto-Save-Anzeige ergänzt: nach automatischer Sicherung erscheint eine kleine, unaufdringliche Statusanzeige „Automatisch gespeichert“; Cache-Versionen für `app.js` und `style.css` in `index.html` auf v24.8 gesetzt – **erledigt** |
| v24.9 | Stabilitätstest nach Auto-Save/Pause/Fortsetzen bestanden: Lernmodus-Pause, Lernmodus-Auto-Save, Prüfung-Pause, Prüfung-Auto-Save bei Reload und Session-Löschung nach Abgabe erfolgreich geprüft – **erledigt** |
| v25.0 | Kompletter Qualitätscheck der App durchgeführt: Dashboard, Alle Fragen, Lernkarten, Prüfung, Fehlertraining und mündliche Prüfung geprüft; aktuell keine Fehler festgestellt – **erledigt** |
| v25.1 | Mündliche Prüfung erweitert: vorhandener Prüfungsbogen B aus `oral-sheets-v23.js` ist jetzt in der Modusauswahl startbar; 15 Fallfragen mit Musterantworten, Prüferhinweisen und Auswertung erfolgreich getestet – **erledigt** |
| v25.2a | Mündliche Prüfung erweitert: Prüfungsbogen C als vollständiger Datensatz mit 15 Accaoui-original Fallfragen in `oral-sheets-v23.js` ergänzt – **erledigt** |
| v25.2b | Prüfungsbogen C in der Modusauswahl startbar gemacht; Browser-Test bestanden; Prüfungsbögen A/B/C sind jetzt aktiv – **erledigt** |
| v25.2c | `PROJECT_MASTERLIST.md` auf aktuellen Stand aktualisiert: A/B/C aktiv, insgesamt 45 mündliche Simulationsfragen dokumentiert – **erledigt** |
| v25.3a | Mündliche Prüfung erweitert: Prüfungsbogen D als vollständiger Datensatz mit 15 Accaoui-original Fallfragen in `oral-sheets-v23.js` ergänzt – **erledigt** |
| v25.3b | Prüfungsbogen D in der Modusauswahl startbar gemacht; Browser-Test bestanden; Prüfungsbögen A/B/C/D sind jetzt aktiv – **erledigt** |
| v25.3c | `PROJECT_MASTERLIST.md` auf aktuellen Stand aktualisiert: A/B/C/D aktiv, insgesamt 60 mündliche Simulationsfragen dokumentiert – **erledigt** |
| v25.4a | Mündliche Prüfung erweitert: Prüfungsbogen E als vollständiger Datensatz mit 15 Accaoui-original Fallfragen in `oral-sheets-v23.js` ergänzt – **erledigt** |
| v25.4b | Prüfungsbogen E in der Modusauswahl startbar gemacht; Prüfungsbögen A/B/C/D/E sind jetzt aktiv – **erledigt** |
| v25.4c | `PROJECT_MASTERLIST.md` auf aktuellen Stand aktualisiert: A/B/C/D/E aktiv, insgesamt 75 mündliche Simulationsfragen dokumentiert – **erledigt** |
| v25.5 | Qualitäts-/Stabilitätstest der mündlichen Prüfung A/B/C/D/E bestanden: alle fünf Prüfungsbögen sichtbar und startbar; Frageanzeige, Musterantwort, Weiter-Navigation und Prüferanzeige geprüft – **erledigt** |
| v25.6 | UI-Feinschliff mündliche Prüfung: Buttonlabel der bisherigen 15-Minuten-Simulation zu `Prüfungsbogen A` vereinheitlicht; A/B/C/D/E optisch konsistent – **erledigt** |
| v25.6c | `PROJECT_MASTERLIST.md` auf aktuellen Stand aktualisiert: Prüfungsbogen A Label vereinheitlicht, A/B/C/D/E weiterhin aktiv, insgesamt 75 mündliche Simulationsfragen dokumentiert – **erledigt** |
| v25.7 | Auswahlfenster der mündlichen Prüfung geprüft: Prüfungsbögen A/B/C/D/E sichtbar, Reihenfolge korrekt, Darstellung im Browser sauber; keine weitere UI-Änderung erforderlich – **erledigt** |
| v25.8a | Zufallsprüfung für die mündliche Prüfung eingebaut: 15 zufällige Fragen aus Prüfungsbogen A/B/C/D/E, eigene sheetId `oral_random_v258a`, keine doppelte Fragenlogik innerhalb einer Runde – **erledigt** |
| v25.8b | Zufallsprüfung im Browser getestet: Button sichtbar, Start funktioniert, Frageanzeige/Musterantwort/Navigation sauber, keine Fehlermeldung gemeldet – **erledigt** |

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

**Stand v24.5:** **86 Fragen** im Pool, **82 Core-Fragen / 120 Punkte** in der Vollsimulation umgesetzt; `points`-Felder vollständig (v24.3a–i/j). Teilpunkte-Code im Prüfungsmodus vorhanden (v24.5). Details: `docs/EXAM_SIMULATION_AUDIT.md`, `docs/EXAM_POINTS_PLAN.md`, `docs/EXAM_CORE_SELECTION_PLAN.md`.

### Mündliche Prüfung

| Merkmal | Vorgabe |
|---------|---------|
| Dauer | etwa **15 Minuten** |
| Form | **Einzelprüfung** oder **Gruppe bis zu 5 Teilnehmer** |
| Inhalt | häufig **Praxisfälle** |
| Anforderung | **richtiges Verhalten beschreiben** und **rechtlich begründen** |

**App-Stand v25.8a:** Prüfungsbogen A, B, C, D und E sind startbar, im Browser getestet und im Auswahlfenster optisch einheitlich benannt. Jeder Bogen enthält 15 Fragen. Zusätzlich ist eine Zufallsprüfung startbar, die 15 zufällige Fragen aus den 75 mündlichen Simulationsfragen nutzt.

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

### UI-Hinweis: Prüfungsanalyse nach Themen

**Erledigt (v24.6f / v24.6x):** responsive stabil, Premium-Kartenlook, bessere Buttontexte. Fehlerübersicht nach Themen zusätzlich in **v24.6g** überarbeitet.

---

## 8.2 Prüfungssimulation 82/120 (Stand v24.6g)

| Aspekt | Stand v24.6g |
|--------|-------------|
| Dokument | `docs/EXAM_SIMULATION_AUDIT.md` – **vorhanden** |
| Fragenbank | **86 Fragen** in `questions.json` (Pool-Ziel erreicht) |
| `points`-Felder | **vollständig** in `questions.json` (v24.3a–i); globaler Check **82/120/38** (v24.3j) |
| Vollsimulation (Ist) | **82 feste Core-Fragen** nach `EXAM_CORE_QUESTION_IDS_V244` (v24.4b) |
| Vollsimulation (Soll) | **82 Fragen / 120 Punkte** nach Sachgebietstabelle §7 – **umgesetzt** |
| Punkteplan | `docs/EXAM_POINTS_PLAN.md` – **vorhanden** und in JSON umgesetzt |
| Core-ID-Plan | `docs/EXAM_CORE_SELECTION_PLAN.md` – **vorhanden** und in App umgesetzt (Option A) |
| Teilpunkte-Audit | **v24.3x** dokumentiert; **v24.5** Code umgesetzt |
| App-Status | Timer (120 min), Bestehen (50 %), Core-Auswahl, Teilpunkte und **Fokusnavigation offener Fragen** (v24.6b) **vorhanden** |
| Frühzeitige Abgabe | Button **„Prüfung jetzt abgeben“** – normal: Warnung bei offenen Fragen; Fokusmodus: direktes Ergebnis (offene = unbeantwortet) |
| Prüfungsanalyse UI | **erledigt** (v24.6f, v24.6x) – responsive, Premium-Look |
| Fehlerübersicht UI | **erledigt** (v24.6g) – Premium-Kartenlook, keine Überlappung |
| Fragen-/Antwort-Mix | **erledigt** (v24.6d, v24.6e) – Reihenfolge gemischt, Indizes korrekt |
| Browser-Endtest | **wichtig** – Vollsimulation 82/120 mit Teilbewertung manuell prüfen (v24.6) |

### Empfohlene Folge-Tasks

- **v24.6c** – Prüfung/Lernen pausieren und später fortsetzen (siehe §8.5)
- **v24.6** – Vollsimulation 82/120 mit Teilbewertung im Browser testen und dokumentieren

---

## 8.3 Teilpunkte-Bewertung (Stand v24.5)

| Aspekt | Stand |
|--------|--------|
| Gültig ab | **01.07.2025** – teilrichtige Antworten zählen |
| Regel | Pro **richtige Lösung** 1 Punkt; max. schriftlich **120**; Bestehen **60** (50 %) |
| `points`-Feld | **Anzahl richtiger Antworten** in `questions.json` gesetzt (1 oder 2 in der Regel) |
| App (Ist) | Teilpunkte-Logik im **Prüfungsmodus umgesetzt** (v24.5): +1 pro richtigem Kreuz, Deckelung über `points` |
| Lernmodus | Weiterhin **binär** (alles-oder-nichts) – bewusst getrennt vom Prüfungsmodus |
| Dokumentation | `docs/EXAM_SIMULATION_AUDIT.md` §10, `docs/EXAM_POINTS_PLAN.md` §10 |
| Code-Regel (Prüfung) | Single: voll/0 · Multiple: +1 pro richtigem Kreuz, falsche Zusatzkreuze zählen nicht |
| Offen | **Browser-Endtest** Vollsimulation mit Teilbewertung (v24.6) |

### Roadmap (Teilpunkte und Vollsimulation)

| Task | Inhalt |
|------|--------|
| **v24.3x** | Teilpunkte-Bewertung **dokumentiert** |
| **v24.3a–i/j** | `points`-Felder vollständig + globaler Check **erledigt** |
| **v24.4b** | Core-Auswahl in App **erledigt** |
| **v24.5** | Teilpunkte-Logik **erledigt** |
| **v24.6** | Vollsimulation 82/120 **mit Teilbewertung** im Browser testen |
| **v24.6b** | Wiederholungslogik offener Fragen + frühzeitige Abgabe – **erledigt** (§8.4) |
| **v24.6d/e** | Fragen- und Antwortreihenfolge gemischt – **erledigt** |
| **v24.6f/x/g** | Prüfungsanalyse + Fehlerübersicht UI – **erledigt** |
| **v24.6c** | Pausieren/Fortsetzen Prüfung und Lernen – **offen** (§8.5) |

---

## 8.4 Wiederholungslogik nach Prüfung (erledigt: v24.6b)

| Aspekt | Stand |
|--------|--------|
| Problem (behoben) | Wiederholungsrunden für unbeantwortete Fragen dürfen **nicht** das volle Prüfungsset durchlaufen |
| Beispiel | Nur Fragen **34, 45, 56, 60** unbeantwortet → Nachbearbeitung nur diese vier Fragen |
| Falsch (vorher) | Nach Frage 34 weiter mit **35, 36, 37** aus dem normalen Prüfungsset |
| Richtig (jetzt) | **34 → 45 → 56 → 60** – gefilterte Indexliste `examFocusQuestionIndexes` in `app.js` |
| Frühzeitige Abgabe | **„Prüfung jetzt abgeben“** jederzeit sichtbar; im Fokusmodus direkt `finishExamMode()`, sonst Warnung mit „Trotzdem abgeben“ |
| Offene bei Abgabe | Unbeantwortete Fragen werden in der Auswertung als **unbeantwortet** gezählt (0 Punkte) |
| Commit | `a169595` – v24.6b fix unanswered exam navigation and early submit |
| Status | **erledigt** – Task **v24.6b** |

---

## 8.5 Pausieren und Fortsetzen (offen: v24.6c)

| Aspekt | Stand |
|--------|--------|
| Ziel | Prüfung und Lernen pausieren, später exakt fortsetzen |
| Voraussetzung | Fragen- und Antwortreihenfolge werden gemischt (v24.6d/e) – **konkrete Session-Reihenfolge muss gespeichert werden** |
| Zu speichern | Fragenreihenfolge, Antwortreihenfolge, aktuelle Frage, ausgewählte Antworten, Prüfungstimer, Modus/Sessiontyp, Punkte-/Auswertungszustand soweit nötig |
| Status | **offen** – nächster sinnvoller Entwicklungsschritt |

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

## 10. Planungsdokumente (Stand v24.6h)

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
| `docs/ACCAOUI_SOURCE_MATERIAL_STATUS.md` | Quellenpakete / Musterunterlagen – Status v24.5y – **vorhanden** |
| `docs/ACCAOUI_ORAL_QUESTIONS_STATUS.md` | Mündliche Prüfung / Musterfragen – Status v24.5y – **vorhanden** |
| `docs/PROJECT_MASTERLIST.md` | Diese Datei |

---

## 11. Funktionaler Teststand

| Bereich | Status |
|---------|--------|
| Schriftlicher Prüfungsmodus | **getestet** (Simulation, Statistik, Historie, Fehlertraining) |
| Mündliche Prüfung | **getestet** (Training, Simulation, Bewertung, Fehlertraining; A/B/C/D/E sichtbar, startbar und einheitlich benannt; Zufallsprüfung sichtbar und startbar, v25.8b) |
| Simulation A | **vorhanden** (15-Minuten-Bogen, 15 Fragen) |
| Simulation B | **vorhanden und startbar** (Prüfungsbogen B, 15 Fragen) |
| Simulation C | **vorhanden und startbar** (Prüfungsbogen C, 15 Fragen; v25.2a/b) |
| Simulation D | **vorhanden und startbar** (Prüfungsbogen D, 15 Fragen; v25.3a/b) |
| Simulation E | **vorhanden und startbar** (Prüfungsbogen E, 15 Fragen; v25.4a/b) |
| Lernkarten | vorhanden – **vollständiger Retest empfohlen** |
| Schriftliche Fragenbank | **86 Fragen** in `questions.json` (Pool-Ziel erreicht); Vollsimulation nutzt **82 Core-Fragen** (v24.4b) |
| Prüfungssimulation 82/120 | **umgesetzt** (Core, Teilpunkte, v24.6b); UI v24.6f/x/g **erledigt**; Mix v24.6d/e **erledigt**; **v24.6c** Pause offen |
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

1. **v24.6c – Pausieren/Fortsetzen** – Prüfung und Lernen speichern und fortsetzen; Session-Reihenfolge wegen v24.6d/e sichern (§8.5)
2. **v24.6 – Browser-Endtest** – Vollsimulation 82/120 mit Teilbewertung manuell prüfen
3. **Lernstrategie-Modul** – Vergessenskurve als UI-Modul (v24.x/v25.x), siehe `docs/LEARNING_STRATEGY_MODULE.md` – **kein sofortiger Code-Task**
4. **UX- und Lernlogik-Audit** – Ergebnisdarstellung, Lernmodus vs. Lernkarten, Active Recall (v24.x), siehe §8.1 – **kein sofortiger Code-Task**
5. **Lernkarten vollständig testen** – Fortschritt, Wiederholung, Kategorien
6. **Später v24 Oral Exam Cleanup** – Patch-Schichten reduzieren, einheitliche Bogenlogik A/B/C
7. **Spätere SQL-Planung** – Phase 2 laut `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md`
8. **Später Datenschutz / Rechtstexte** – Impressum, Datenschutz, Nutzungsbedingungen (v26)
9. **Später Supabase / Login** – Auth, Kurse, Fortschritt pro `user_id` (v27, Roadmap Phase 3–6)
10. **Quellenpakete und mündliche Musterfragen gezielt auswerten** – nicht vollständig in neuen Chat laden; siehe `docs/ACCAOUI_SOURCE_MATERIAL_STATUS.md` und `docs/ACCAOUI_ORAL_QUESTIONS_STATUS.md`

**Erledigt:** v24.5 (Teilpunkte); v24.6b (Wiederholung/offene Fragen); v24.6d/e (Mix Fragen/Antworten); v24.6f/x (Prüfungsanalyse UI); v24.6g (Fehlerübersicht UI).

Optional parallel: Projektstruktur gegen alte Kopien prüfen; mündliche Prüfung später als erweiterter Prüfermodus.

---

## 15. Start in neuem Chat

Zuerst nennen:

```txt
docs/PROJECT_MASTERLIST.md
docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md
docs/EXAM_SIMULATION_AUDIT.md
docs/EXAM_POINTS_PLAN.md
docs/EXAM_CORE_SELECTION_PLAN.md
```

Dann **NUR IN GIT BASH AUSFÜHREN**:

```bash
git status
git pull --ff-only
git log -1 --oneline
python tools/preflight.py
```

**Hinweis:** Alte Chat-Uploads und Prüfungsmuster sind **nicht automatisch** Arbeitsgrundlage im neuen Chat. Bei Bedarf Prüfungsmuster erneut hochladen oder im Repo dokumentieren.

Keine Änderung ohne sauberen Arbeitsstand.

v23.5.12
Lernkarten funktional getestet und Layout-Fix umgesetzt. Lange Fragen, Antwortansicht, Erklärungen, Buttons, Gewusst/Nicht gewusst und Wiederholen-Karten werden sauber dargestellt.