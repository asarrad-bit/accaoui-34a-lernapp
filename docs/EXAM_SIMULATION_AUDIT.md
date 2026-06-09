# Accaoui §34a – Prüfungssimulation Audit (82 Fragen / 120 Punkte)

Stand: **v24.3x** (Teilpunkte-Audit ergänzt; v24.0 Basis)
Projekt: Accaoui §34a Lern-App
Grundlage: `questions.json` (86 Fragen), `app.js` (Prüfungsmodus), `docs/PROJECT_MASTERLIST.md` §7

**Hinweis:** Dieses Dokument beschreibt den **Ist-Stand** und die **geplante Anpassung**. In v24.0 wird **kein Code** und **keine** `questions.json`-Änderung vorgenommen.

---

## 1. Ausgangslage

- Die **Fragenbank** umfasst aktuell **86 Fragen** (Ziel-Pool nach Ausbauplan erreicht).
- Die **schriftliche Zielsimulation** soll **82 Fragen** umfassen.
- Die **echte Zielstruktur** hat **120 Punkte**.
- **Bearbeitungszeit:** 120 Minuten.
- **Bestehensgrenze:** mindestens **50 Prozent** der erreichbaren Punkte.

Die App enthält bereits Konstanten und UI für eine Vollsimulation mit 82 Fragen und 120-Minuten-Timer (`EXAM_FULL_QUESTION_LIMIT_V20 = 82`, `EXAM_DURATION_SECONDS = 120 * 60`, `EXAM_PASS_PERCENT = 50`). Die **Datenbasis** und **Auswahl-Logik** entsprechen der IHK-nahen Gewichtung jedoch noch nicht vollständig.

---

## 2. Aktueller technischer Befund

| Befund | Detail |
|--------|--------|
| `questions.json` | Enthält **keine** `points`-, `score`- oder `weight`-Felder |
| Alle 86 Fragen | Haben aktuell **kein Punktefeld** in den Daten |
| Fallback in der App | `getQuestionPoints()` nutzt `DEFAULT_QUESTION_POINTS = 1`, wenn kein Feld gesetzt ist |
| Faktische Auswertung | Die Fragenbank ist damit derzeit nur als **86-Punkte-Basis** auswertbar (jede Frage = 1 Punkt) |
| Punkte-Infrastruktur | Die App enthält bereits `getQuestionPoints()`, `getExamMaxPoints()`, `getExamReachedPoints()`, `getExamPassPoints()` – die **Datenbasis** ist aber noch nicht vorbereitet |
| Vollsimulation-Start | `startExamMode()` erzeugt `examQuestions` per `shuffleArray([...allQuestions]).slice(0, limit)` – **zufällig aus dem Gesamtpool**, ohne Sachgebiet und ohne Punktegewichtung |

**Kurzfassung:** Timer, Fragenanzahl (82) und Bestehensgrenze (50 %) sind in der App angelegt; **Punkteverteilung** und **sachgebietsbezogene Ziehung** fehlen noch.

---

## 3. Kritischer Punkt

- Die **Vollsimulation darf nicht** einfach **82 zufällige Fragen** aus `allQuestions` ziehen.
- Die Vollsimulation **muss später** nach **Sachgebiet** und **Zielgewichtung** (Fragen + Punkte pro Kategorie) ziehen.
- **Aktueller Code** (`app.js`, `startExamMode`): `examQuestions = shuffleArray([...allQuestions]).slice(0, Math.min(currentExamLimit, allQuestions.length))`.
- **Bewertung:** Für **Training** und **Smoke-Tests** akzeptabel; für eine **IHK-nahe Vollsimulation** **nicht ausreichend**.

---

## 4. Zielmodell schriftliche Prüfung

| Sachgebiet | Fragen | Punkte |
|------------|-------:|-------:|
| Recht der öffentlichen Sicherheit und Ordnung | 7 | 11 |
| Gewerberecht | 5 | 8 |
| Datenschutzrecht | 5 | 8 |
| Bürgerliches Gesetzbuch | 13 | 21 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 | 21 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 | 13 |
| Umgang mit Waffen | 5 | 8 |
| Umgang mit Menschen | 19 | 19 |
| Grundzüge der Sicherheitstechnik | 7 | 11 |
| **Gesamt** | **82** | **120** |

---

## 5. Rechnerische Punkteverteilung

Für **82 Fragen** und **120 Punkte** werden **38 Zweipunktfragen** und **44 Einpunktfragen** benötigt:

`38 × 2 + 44 × 1 = 76 + 44 = 120`

- **Umgang mit Menschen:** 19 Fragen / 19 Punkte → dort **alle Fragen 1 Punkt** (0 Zweipunktfragen).
- Die **übrigen Sachgebiete** benötigen eine definierte Mischung aus 1- und 2-Punkte-Fragen.

### Zweipunktfragen je Sachgebiet (Zielverteilung)

| Sachgebiet | Zweipunktfragen |
|------------|----------------:|
| Recht der öffentlichen Sicherheit und Ordnung | 4 |
| Gewerberecht | 3 |
| Datenschutzrecht | 3 |
| Bürgerliches Gesetzbuch | 8 |
| Strafgesetzbuch und Strafverfahrensrecht | 8 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 5 |
| Umgang mit Waffen | 3 |
| Umgang mit Menschen | 0 |
| Grundzüge der Sicherheitstechnik | 4 |
| **Summe** | **38** |

---

## 6. Aktueller Fragenbestand (Pool vs. Prüfungsbedarf)

| Sachgebiet | Vorhanden | Benötigt (Prüfung) | Reserve |
|------------|----------:|-------------------:|--------:|
| Recht der öffentlichen Sicherheit und Ordnung | 8 | 7 | +1 |
| Gewerberecht | 8 | 5 | +3 |
| Datenschutzrecht | 5 | 5 | 0 |
| Bürgerliches Gesetzbuch | 13 | 13 | 0 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 | 13 | 0 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 | 8 | 0 |
| Umgang mit Waffen | 5 | 5 | 0 |
| Umgang mit Menschen | 19 | 19 | 0 |
| Grundzüge der Sicherheitstechnik | 7 | 7 | 0 |
| **Gesamt** | **86** | **82** | **+4** |

Stand: Zählung aus `questions.json` (v24.0).

---

## 7. Bewertung

- Die **Fragenbank ist groß genug** für eine 82-Fragen-Vollsimulation (86 Fragen, 4 Reserve im Pool).
- **Recht der öffentlichen Sicherheit und Ordnung** und **Gewerberecht** haben **mehr Fragen als benötigt** und können als **Pool** für die Zufallsauswahl dienen.
- Die **echte Punktegewichtung** (38×2 + 44×1) ist in den **Daten noch nicht umgesetzt**.
- Der **nächste Qualitätsschritt** ist **nicht** mehr Fragenproduktion, sondern **Prüfungslogik** (Punktefelder + sachgebietsbezogene Auswahl + Auswertung).

---

## 8. Empfohlene nächste Tasks

| Task | Inhalt |
|------|--------|
| **v24.1** | `points`-Felder fachlich geplant (`docs/EXAM_POINTS_PLAN.md`) |
| **v24.2** | Feste 82 Core-IDs (`docs/EXAM_CORE_SELECTION_PLAN.md`) |
| **v24.3a–f** | `points`-Felder je Sachgebiet in `questions.json` ergänzen |
| **v24.3x** | **Teilpunkte-Bewertung** auditiert und dokumentiert (dieser Abschnitt §10) |
| **v24.4** | Restliche `points`-Felder fertigstellen |
| **v24.5** | Teilpunkte-Logik technisch prüfen und umsetzen |
| **v24.6** | Vollsimulation **82 Fragen / 120 Punkte** mit Teilbewertung testen |

**Hinweis:** v24.0 / v24.3x = **nur Dokumentation** in diesem Audit – **kein Code** in den Audit-Tasks.

---

## 9. Wichtige Regel: Punktevergabe

**Keine automatische oder blinde Punktevergabe.**

Zweipunktfragen müssen **fachlich sinnvoll** sein, z. B.:

- Mehrfachauswahl (`multiple`)
- Kombinationsfragen (`combination`)
- anspruchsvollere Fallfragen (`praxisfall`)
- prüfungsrelevante Abgrenzungen

**Einfache Wissensfragen** bleiben eher **1 Punkt**.

Die Zuordnung erfolgt **pro Frage** in der Review-/Pflegephase, nicht per Skript über alle Fragen eines Typs.

---

## 10. Teilpunkte-Bewertung (Audit v24.3x, ab 01.07.2025)

**Hinweis:** Nur Audit-/Dokumentationsschritt – **keine technische Umsetzung** in v24.3x.

### 10.1 Bewertungsgrundlage

- Ab **01.07.2025** werden **teilrichtige Antworten** in der Sachkundeprüfung nach § 34a berücksichtigt.
- **Jede richtige Lösung** zählt mit **1 Punkt**.
- Eine Aufgabe mit **zwei richtigen Lösungen** kann **2 Punkte** bringen.
- Wird nur **eine von zwei** richtigen Lösungen erkannt, kann dafür **1 Punkt** erreicht werden.
- **Maximalpunktzahl** schriftlich: **120 Punkte**.
- **Bestehensgrenze:** **50 Prozent** = **60 Punkte**.

### 10.2 Konsequenz für die App

- Die Prüfungsauswertung darf Mehrfachantworten **nicht** nur als komplett richtig oder komplett falsch bewerten.
- Die App muss später **Teilpunkte** berechnen.
- Das `points`-Feld einer Frage soll zur **Anzahl richtiger Antworten** passen:
  - **Eine** richtige Antwort → in der Regel `points: 1`
  - **Zwei** richtige Antworten → in der Regel `points: 2`
- Siehe Zuordnung in `docs/EXAM_POINTS_PLAN.md` und Core-IDs in `docs/EXAM_CORE_SELECTION_PLAN.md`.

### 10.3 Noch offen zu prüfen

- Wie **falsche zusätzliche Markierungen** technisch bewertet werden sollen.
- Ob falsche Kreuze **nur nicht zählen** oder ob sie **Teilpunkte reduzieren**.
- Umsetzung **erst nach fachlicher Entscheidung** und **separatem Code-Task** (v24.5).

### 10.4 Vorläufige technische Zielregel (für späteren Code-Task)

| Fragetyp | Regel |
|----------|--------|
| **Single** (`single`) | Richtige Antwort = volle Punkte · falsche Antwort = **0 Punkte** |
| **Multiple** (`multiple`, `combination` mit mehreren richtigen Indizes) | Pro **korrekt gesetztem Kreuz** = **1 Punkt** · falsche Zusatzantworten dürfen **nicht belohnt** werden · genaue **Abzugslogik** separat festlegen |

**Praxisfall:** Bewertung analog zur Anzahl richtiger Lösungen und dem `points`-Feld – Details in v24.5.

---

## Verweise

- `docs/EXAM_POINTS_PLAN.md` – Punkteplan und Teilpunkte (§10)
- `docs/EXAM_CORE_SELECTION_PLAN.md` – feste 82 Core-IDs
- `docs/PROJECT_MASTERLIST.md` – §7 Prüfungsaufbau, §8.2/§8.3, §14 nächste Aufgaben
- `docs/WRITTEN_QUESTION_EXPANSION_PLAN.md` – Ausbauplan 51 → 86
- `docs/WRITTEN_QUESTION_STANDARD.md` – Fragenstandard

---

*Accaoui-eigene Trainingsfragen – keine 1:1-Übernahme aus IHK- oder Musterprüfungen.*
