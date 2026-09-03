# Accaoui §34a Lern-App – Cursor Master Context

Stand: v27.37a
Projekt: Accaoui §34a Lern-App
Arbeit: `C:\a34a`
Zuhause: `C:\xampp\htdocs\accaoui\v4-dashboard`
Branch: `main`
Repository: `asarrad-bit/accaoui-34a-lernapp`
Letzter abgeschlossener funktionaler Stand: v27.35g
Abschlusscommit: `f5f261fee67fc17c170ee714ae23761ff1668f17`

## v27.37b-GATE-BOOTSTRAP-REPAIR – Kontrollinfrastruktur

v27.37b-GATE-BOOTSTRAP-REPAIR korrigiert ausschließlich den phasenfesten und strukturellen CURRENT_TASK-Vertrag in Continuity und Preflight.

Repair-Basis: `b83581612fa25b73f62c4b146e8df782d67c869c`.

Der einmalige atomare Repair umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Datei und keine Produktdatei sind zulässig.

Der Bootstrap-Commit `b83581612fa25b73f62c4b146e8df782d67c869c` bleibt korrekt. Der Repair behebt ausschließlich phasenfremde reale Manipulationsbaselines, unvollständige Kopfstrukturprüfungen und fehlende CURRENT_TASK-Negativtests.

Der kanonische CURRENT_TASK-Kopf reicht exakt von `# Verbindlicher aktueller Task` bis unmittelbar vor dem verpflichtenden ersten `## `-Abschnitt. Er enthält exakt die neun bekannten Felder in definierter Reihenfolge; fehlende, doppelte, unbekannte oder ungeordnete Kopffelder bleiben blockiert. Historische Abschnitte dürfen einen ungültigen aktuellen Kopf weder retten noch einen gültigen Kopf beschädigen.

Die drei kanonischen Taskzustände bleiben BASE_CLOSED, AUTHORIZED und CLOSED. Bootstrap-Phasen verwenden BASE_CLOSED; Authorization- und Implementation-Phasen verwenden AUTHORIZED; Closure-Phasen verwenden CLOSED. Synthetische Manipulationstests verwenden ausschließlich vollständige phasenspezifische CURRENT_TASK-Dokumente und niemals den realen CURRENT_TASK als Test-Baseline.

Der spätere Produktvertrag für `v27.37b – Isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke` bleibt unverändert: exakt zwei Dependencies, exakt drei öffentliche Methoden, `getClient()` exakt einmal pro Operation, kein Client-Cache, ausschließlich `client.auth` als `{ auth }` und für Brückenfehler `Object.freeze({ ok: false, code: "auth_error" })`.

Der vorbereitete Zustand ist `v2737b_gate_bootstrap_repair_prepared`. Nach einem späteren direkten Repair-Commit ist er dynamisch `v2737b_gate_bootstrap_repair_committed`. Keine zukünftige Repair-Commit-SHA wird hartcodiert; der Repair darf nur einmal vorkommen.

`CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`; v27.37b wird durch diesen Repair NICHT autorisiert. Erst nach dem Repair-Commit ist ein frisches separates v27.37b-Autorisierungs-Gate zulässig.

Der lokale Sicherungspatch `.git/v2737b-authorization-preflight-blocked.patch` wird nicht angewendet, nicht verändert und nicht als Implementierungsquelle verwendet.

Kein Produktcode wird geändert. Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.


## v27.37b-GATE-BOOTSTRAP – Kontrollinfrastruktur

v27.37b-GATE-BOOTSTRAP ist ausschließlich Kontrollinfrastruktur.

Stabile Bootstrap-Basis: `b5d676d226891b4f53e9e614e015c433c2616ad1`.

Der einmalige atomare Bootstrap umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Datei und keine Produktdatei sind zulässig. v27.37a bleibt vollständig abgeschlossen und wird nicht wieder geöffnet.

Der spätere Task heißt exakt `v27.37b – Isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke`, ist nach diesem Bootstrap aber NICHT autorisiert. `CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`. Der nächste zulässige Schritt nach einem erfolgreichen Bootstrap-Commit ist ein separates ausdrückliches v27.37b-Autorisierungs-Gate.

Der spätere Implementierungsscope umfasst exakt:

- `data/supabase-participant-auth-session-bootstrap-bridge.js`
- `tools/check-supabase-participant-auth-session-bootstrap-bridge.py`
- `docs/SUPABASE_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_V2737B.md`
- `tools/preflight.py`

Die spätere Factory ist `createParticipantAuthSessionBootstrapBridge({ bootstrap, createParticipantAuthSessionAdapter })`. Die Dependencies sind exakt `bootstrap` und `createParticipantAuthSessionAdapter`; eine dritte Dependency ist ausgeschlossen. Ihre öffentliche Oberfläche enthält exakt `resolveSession()`, `signIn({ email, password })` und `signOut()`. Eine vierte öffentliche Methode ist ausgeschlossen. Pro öffentlicher Operation wird `bootstrap.getClient` sicher genau einmal gelesen und `getClient()` genau einmal aufgerufen; der Client wird nicht dauerhaft gecacht. Ausschließlich `client.auth` wird als exakt `{ auth }` an `createParticipantAuthSessionAdapter({ auth })` weitergegeben.

Gültige methodenspezifische v27.37a-Ergebnisse werden unverändert delegiert. Jeder Brückenfehler liefert ausschließlich das eingefrorene Plain Object `Object.freeze({ ok: false, code: "auth_error" })`; Session-, User-, ID-, E-Mail-, Passwort-, Token-, Config- und Rohfehlerdaten bleiben ausgeschlossen.

Verboten bleiben `initializeClient()`, `getState()`, `createClient()`, Browser-Globals, `window`, `document`, DOM, `localStorage`, `sessionStorage`, Cookies, IndexedDB, Config-Lesen, eigener Netzwerkcode, `.from(...)`, Teilnehmer-, Enrollment- oder Kurslogik, SQL und Migrationen. Bestehende Produktdateien bleiben frozen.

Der Lifecycle erkennt den aktuellen einmaligen Schritt dynamisch als `v2737b_gate_bootstrap_prepared` und nach einem direkten Sechs-Dateien-Commit als `v2737b_gate_bootstrap_committed`. Danach sind ausschließlich die v27.37b-Phasen `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed` zulässig. Keine zukünftige Bootstrap-, Gate-, Implementierungs- oder Closure-SHA wird hartcodiert; eine Wiederholung und eine allgemeine zukünftige Taskfreigabe bleiben blockiert.

Kein Produktcode wurde geändert. Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.

## Abgeschlossener technischer Schritt v27.37a

v27.37a abgeschlossen.

Implementierungscommit: `54f6425fac70da134e3c6f39b376f66fa75063cb`

Ergebnis:

- Der isolierte CommonJS Teilnehmer-Auth-/Session-Adapter ist implementiert.
- Die Factory ist `createParticipantAuthSessionAdapter({ auth })`.
- Die öffentliche Oberfläche enthält exakt:
  - `resolveSession()`
  - `signIn({ email, password })`
  - `signOut()`
- Die einzige Dependency ist `auth`.
- Alle Ergebnisse sind gefrorene Plain Objects mit exakt `{ ok, code }`.
- Sensitive Daten, Sessions, Nutzer, Passwörter, Token und Rohfehler werden nicht nach außen gegeben.
- Es gibt kein Browser-Wiring und keinen Storage-Zugriff.
- Es gibt keinen eigenen Netzwerkcode, keinen Client, kein `createClient()` und kein `initializeClient()`.
- Es gibt keine Tabellenlogik und keine Duplizierung der v27.36b-Fachlogik.
- Supabase bleibt NICHT LIVE.

Testergebnis:

- Positiv: 7 PASS.
- Negativ: 57 PASS.
- Manipulation: 20 PASS.
- Shared-Fake signIn -> access_allowed: PASS.
- Shared-Fake signOut -> session_missing: PASS.
- Continuity: PASS.
- Preflight: PASS.
- v27.36b: PASS.
- v27.36c: PASS.
- v27.36d Regression: PASS.
- v27.36e Regression: PASS.
- v27.36f Regression: PASS.
- v27.37a Nachfolgeprofil: PASS.
- `git diff --check`: PASS.

### Permanenter v27.37a-Lifecycle

Der Lifecycle erkennt weiterhin dynamisch `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed`.

`closure_prepared` verlangt den Implementierungscommit, exakt die fünf Gate-Dateien im Working Tree, `CURRENT_TASK` als `NONE / BLOCKED / Autorisiert NEIN` und unveränderte Produktdateien. `closure_committed` verlangt danach einen direkten Closure-Commit mit exakt diesen fünf Gate-Dateien und einen sauberen Working Tree.

Keine zukünftige Closure-SHA wird hartcodiert.

Eine zweite Implementierung, eine Implementierung nach der Closure und eine implizite Autorisierung werden blockiert. Kein Folgetask wurde ausgewählt oder autorisiert.

## Abgeschlossener atomarer Follow-up-Repair v27.37a-GATE-REPAIR-FOLLOWUP

v27.37a-GATE-REPAIR-FOLLOWUP abgeschlossen.

Der Titel lautet: UTF-8-Historienleser und authorization_prepared-Scope im v27.37a-Nachfolgeprofil korrigieren.

Technische Basis: `ec8f20216d8dcb13417cca27699febc998d6dcd9`.

Der erste v27.37a-GATE-REPAIR bleibt vollständig abgeschlossen und wird nicht wiederholt. Der einmalige atomare FOLLOWUP war erforderlich, weil der v27.37a-Historienpfad Git-Blobs über die Windows-Codepage CP1252 statt strikt als UTF-8 las und weil `authorization_prepared` fälschlich exakt alle fünf statt jeder nichtleeren Teilmenge der Gate-Dateien verlangte.

Der ausdrücklich freigegebene einmalige atomare FOLLOWUP-Repair umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Datei ist erlaubt. Keine Produktfunktion und keine Produktdatei wurden geändert. Die historischen v27.36e-/v27.36f-Produkt- und Sicherheitsverträge bleiben unverändert.

Der v27.37a-Historienpfad verwendet für Git-Blobs ausschließlich den vorhandenen strikt UTF-8-decodierenden Reader. Die globale `run_command()`-Semantik bleibt unverändert. `authorization_prepared` akzeptiert ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien; leere Mengen, Implementierungsdateien, `tools/preflight.py`, `app.js`, Produktdateien und unbekannte Zusatzdateien bleiben blockiert. Alle späteren Lifecyclephasen und ihre exakten Dateimengen bleiben unverändert streng.

Der Lifecycle erkennt ausschließlich den einmaligen Zustand `v2737a_gate_repair_followup_atomic_prepared` und nach einem direkten Sechs-Dateien-Commit `v2737a_gate_repair_followup_atomic_committed`. Eine Wiederholung und jede zukünftige FOLLOWUP-Commit-SHA bleiben blockiert.

`CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`. v27.37a ist nach dem FOLLOWUP weiterhin nicht autorisiert; der nächste zulässige Schritt ist ein frisches ausdrückliches v27.37a-Autorisierungs-Gate.

Die lokalen Sicherungen `.git/v2737a-gate-preflight-blocked.patch` und `.git/v2737a-gate-after-ec8f202.patch` bleiben unangewendet, unverändert, lokal und außerhalb jedes Commits.

Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten. Commit und Push bleiben NEIN.


## 1. Sofort-Regel

Keine Blind-Fixes. Cursor darf nicht eigenständig optimieren.

Codex darf ebenfalls ausschließlich den in
`docs/tasks/CURRENT_TASK.md` ausdrücklich autorisierten Task und nur
dessen erlaubte Dateien bearbeiten. Codex darf keinen Folgetask
ableiten, automatisch auswählen oder autorisieren.

Immer zuerst prüfen:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Lokalen und GitHub-HEAD direkt vergleichen. Bei einer Abweichung
sofort STOPP. Eine Synchronisation ist nur nach gesonderter Freigabe
zulässig.

Vor jedem Commit:

```bash
python tools/preflight.py
git diff --check
git status --short
```

Nur committen, wenn Preflight grün ist, `git diff --check` keine Ausgabe zeigt und nur erlaubte Dateien geändert wurden.

### Arbeitsworkflow / Git-Synchronisation

**Bevor** an der Accaoui §34a Lern-App gearbeitet wird, zuerst fragen:

> **„Bist du gerade auf Arbeit oder zuhause?“**

Danach immer in dieser Reihenfolge:

1. **Richtiger Laptop / richtiger Arbeitsstand** klären (Arbeit vs. Zuhause)
2. lokalen Arbeitsbaum mit `git status --short` prüfen
3. Branch und lokalen HEAD direkt prüfen
4. GitHub-HEAD für `refs/heads/main` direkt prüfen
5. lokalen und GitHub-HEAD vergleichen; bei Abweichung sofort STOPP
6. Synchronisation nur nach gesonderter Freigabe
7. Commit und Push nur nach ausdrücklicher Freigabe

## 2. Ziel der App

Die Accaoui §34a Lern-App ist eine professionelle Lern- und Prüfungsplattform für Teilnehmer von Accaoui Bildung.

Kernmodule:

1. Dashboard
2. Statistik
3. Alle Fragen
4. Lernkarten
5. Schriftliche Prüfung
6. Fehlertraining
7. Mündliche Prüfung
8. Später Teilnehmer-Login
9. Später Supabase-Datenbank
10. Später PWA/App-Store-Fähigkeit

Die App darf nicht wie eine einfache Fragen-App wirken, sondern wie ein Premium-Lernsystem.

## 3. Aktive Hauptdateien

Führend ist der Root-Ordner, nicht `test/`.

Aktiv geladen bzw. relevant:

```txt
index.html
style.css
oral-exam.css
app.js
patch-v21.js
questions.json
data/oral-question-bank.js
data/oral-sheets-bank.js
oral-sheets.js
oral-sheets-v23.js
oral-exam.js
tools/audit-categories.py
tools/preflight.py
```

`test/` ist nicht führend und darf nicht als Referenz genutzt werden.

## 4. Aufbau Sachkundeprüfung nach § 34a GewO

### Schriftlicher Teil

1. 82 geschlossene Aufgaben
2. 120 Minuten Bearbeitungszeit
3. keine Hilfsmittel
4. mindestens 50 Prozent zum Bestehen
5. Zulassung zur mündlichen Prüfung nur bei bestandenem schriftlichen Teil

### Gewichtung schriftlich

| Sachgebiet | Fragen | Punkte |
|---|---:|---:|
| Recht der öffentlichen Sicherheit und Ordnung | 7 | 11 |
| Gewerberecht | 5 | 8 |
| Datenschutzrecht | 5 | 8 |
| Bürgerliches Gesetzbuch | 13 | 21 |
| Strafgesetzbuch und Strafverfahrensrecht | 13 | 21 |
| Unfallverhütungsvorschriften Wach- und Sicherungsdienste | 8 | 13 |
| Umgang mit Waffen | 5 | 8 |
| Umgang mit Menschen | 19 | 19 |
| Grundzüge der Sicherheitstechnik | 7 | 11 |

### Mündliche Prüfung

1. Einzelprüfung oder Gruppe bis zu fünf Teilnehmer
2. häufig Fallbeispiele aus der Praxis
3. richtiges Verhalten beschreiben und rechtlich begründen
4. Richtwert: etwa 15 Minuten

## 5. Kanonische Kategorien

Diese Reihenfolge ist verbindlich:

1. Recht der öffentlichen Sicherheit und Ordnung
2. Gewerberecht
3. Datenschutzrecht
4. Bürgerliches Gesetzbuch
5. Strafgesetzbuch und Strafverfahrensrecht
6. Unfallverhütungsvorschriften Wach- und Sicherungsdienste
7. Umgang mit Waffen
8. Umgang mit Menschen
9. Grundzüge der Sicherheitstechnik

Alte Begriffe dürfen nur in Mapping-Funktionen vorkommen, z. B. `normalizeCategoryName()`.

## 6. Schriftliche Fragenbank

Aktueller funktionaler Stand:

1. schriftlicher Prüfungsmodus funktioniert
2. Speicherung in localStorage funktioniert
3. Statistik funktioniert
4. Fehlerdaten funktionieren
5. Prüfungshistorie funktioniert
6. Fehlertraining funktioniert
7. Kategorien-Normalisierung funktioniert
8. **86 Fragen** in `questions.json` (Pool-Ziel erreicht)
9. **`points`-Felder vollständig** für alle 9 Sachgebiete (v24.3a–i); globaler Check **82/120/38** (v24.3j)
10. **Vollsimulation** nutzt feste **82-Core-Fragen** (v24.4b)
11. **Teilpunkte-Logik** im Prüfungsmodus eingebaut (v24.5)
12. **Wiederholungslogik offener Prüfungsfragen** + frühe Abgabe (v24.6b)
13. **Fragen-/Antwort-Mix** in Lern- und Fehlermodi (v24.6d/e)
14. **Prüfungsanalyse UI** responsive + Premium (v24.6f, v24.6x)
15. **Fehlerübersicht nach Themen** Premium + responsive (v24.6g)

### Entwicklungsstand v24.6 (Auszug)

| Version | Inhalt | Status |
|---|---|---|
| v24.6b | Offene Fragen gezielt; frühe Abgabe; unbeantwortet in Auswertung | **erledigt** |
| v24.6d | Fragenreihenfolge in Lern-/Wiederholungs-/Fehlermodi gemischt | **erledigt** |
| v24.6e | Antwortreihenfolge gemischt; Indizes intern korrekt; JSON unverändert | **erledigt** |
| v24.6f | Prüfungsanalyse responsive stabil | **erledigt** |
| v24.6x | Prüfungsanalyse optisch/funktional; Buttontexte verbessert | **erledigt** |
| v24.6g | Fehlerübersicht nach Themen: Premium, responsive | **erledigt** |
| v24.6c | Pausieren/Fortsetzen Prüfung und Lernen | **erledigt** |
| v24.6 | Browser-Endtest Vollsimulation mit Teilbewertung | **offen** |

Ziel:

1. kurzfristig von 51 auf 82 schriftliche Fragen
2. mittelfristig 250–300 Fragen
3. langfristig 500–1.000+ Fragen

Neue schriftliche Fragen müssen dem Standard aus `docs/WRITTEN_QUESTION_STANDARD.md` folgen.

Pflichtfelder langfristig:

```txt
id
mode: written
topic
subtopic
questionType
points
difficulty
examRelevance
ihkSimilarityRisk
sourceStyle: accaoui_original
question
answers
correct / correctAnswers
explanation
```

## 7. Mündliche Prüfung

Aktueller funktionaler Stand:

1. Training nach Themen
2. 15-Minuten-Simulation A
3. 15-Minuten-Simulation B
4. Volltraining
5. Musterantworten
6. Bewertung Sicher / Noch üben
7. mündliches Fehlertraining
8. Online-Anzeige funktioniert

Struktur Simulation:

1. Prüfer 1: Fragen 1–5
2. Vorsitz: Fragen 6–10
3. Prüfer 3: Fragen 11–15

Später nötig:

1. skalierbare Prüfungsbogen-Auswahl A/B/C/D ...
2. v24 Oral Exam Cleanup
3. Patch-Schichten reduzieren
4. einheitliche Bogenlogik
5. mündliche Prüfung stärker modularisieren

## 8. IHK-/Musterfragen-Regel

Musterprüfungen und IHK-nahe Unterlagen sind nur Analysequelle und Strukturvorbild.

Nicht erlaubt:

1. offizielle Fragen 1:1 übernehmen
2. Originallösungen 1:1 übernehmen
3. gleiche Reihenfolge übernehmen
4. IHK-Logos oder offizielle IHK-Bezeichnungen nutzen
5. App als offizielle IHK-App darstellen

Erlaubt:

1. Sachgebiete als Orientierung nutzen
2. Struktur der Prüfung nachbilden
3. eigene Accaoui-Fragen formulieren
4. eigene Trainingsbewertung nutzen
5. klarer Hinweis: Keine offizielle IHK-Prüfung

## 9. Fragen-Datenbank-Strategie

Bei vielen Fragen nicht mehr direkt in `questions.json` arbeiten.

Professioneller Prozess:

```txt
Rohfragen sammeln
→ fachlich prüfen
→ Dubletten prüfen
→ rechtlich prüfen
→ eigene Accaoui-Frage formulieren
→ freigeben
→ veröffentlichen
```

Geplante Tabellen:

```txt
question_imports
raw_questions
written_questions
oral_questions
question_reviews
question_versions
```

Status-Stufen:

```txt
imported
needs_review
rewrite_required
reviewed
approved
published
archived
```

Nur `published` darf später in der App erscheinen.

## 10. Supabase-Zielarchitektur

Supabase ist als spätere Datenbank gesetzt.

Geplant:

1. Supabase Auth
2. Postgres
3. Row Level Security
4. user_id pro Teilnehmer
5. course_id
6. Fortschritt pro Frage
7. Prüfungsergebnisse
8. Fehlerhistorie
9. Lernkartenfortschritt
10. mündliche Prüfungsergebnisse
11. Teilnehmerstatus aktiv/inaktiv
12. Rollenmodell Teilnehmer / Dozent / Admin

Service Role Key niemals im Frontend speichern.

## 11. Datenschutz und Rechtssicherheit

Später erforderlich:

1. Impressum
2. Datenschutzerklärung
3. Nutzungsbedingungen
4. Hinweis zu Trainingscharakter
5. Hinweis: keine offizielle IHK-Prüfung
6. Lösch-/Kontaktmöglichkeit für Teilnehmerdaten
7. keine unnötigen Trackingdaten
8. keine externen Dienste ohne Prüfung

Aktuell:

1. keine bekannten externen Dienste
2. keine CDN-Abhängigkeiten
3. keine Analytics
4. keine API-Keys im Frontend
5. Supabase noch nicht eingebaut

## 12. Cursor-Auftragsregel

Jeder Cursor-Auftrag muss enthalten:

1. Ziel
2. erlaubte Dateien
3. verbotene Dateien
4. konkrete Änderung
5. was nicht geändert werden darf
6. Prüf-Befehle danach
7. kein Commit durch Cursor
8. keine Zusatzoptimierungen

Cursor darf nicht:

1. große Dateien komplett neu formatieren
2. Zeilenenden ändern
3. mehrere Bereiche gleichzeitig umbauen
4. Refactoring ohne Freigabe machen
5. `test/` ändern, außer ausdrücklich erlaubt
6. Code mit `--fix`, Prettier oder automatischer Formatierung verändern

### Codex-Auftragsregel

Codex muss vor jeder Änderung `docs/tasks/CURRENT_TASK.md` vollständig
lesen und darf ausschließlich den dort ausdrücklich autorisierten Task
bearbeiten. Für Codex gelten derselbe erlaubte Dateiumfang, dieselben
Verbote und dieselben Prüfpflichten wie im Taskvertrag.

Codex darf insbesondere nicht:

1. einen Task aus Versionsfolgen, früheren Chats oder Erinnerung ableiten
2. andere Dateien als die in `CURRENT_TASK` erlaubten Dateien verändern
3. Zusatzoptimierungen oder Refactorings ohne Freigabe ausführen
4. Webrecherche, Netzwerk-, Supabase- oder SQL-Arbeit ohne ausdrücklichen Auftrag ausführen
5. einen Commit oder Push ohne ausdrückliche Freigabe ausführen
6. nach Abschluss automatisch einen Folgetask auswählen oder autorisieren

### Kennzeichnungs- und Sicherheitsregel

1. Cursor-Aufträge immer mit **„NUR FÜR CURSOR – NICHT IN GIT BASH“** kennzeichnen.
2. Git-Bash-Befehle immer mit **„NUR IN GIT BASH AUSFÜHREN“** kennzeichnen.
3. Cursor darf **keinen Commit** und **keinen Push** ausführen (außer ausdrücklich vom Nutzer gewünscht).

## 13. Roadmap ab jetzt

### v23.5.4 – Gesamtstand bereinigen

1. README aktualisieren
2. PROJECT_MASTERLIST bereinigen
3. PROJECT_STRUCTURE_AUDIT neu erstellen oder wiederherstellen
4. aktuelle Module dokumentieren
5. Roadmap sauber festlegen

### v23.5.5 – Fragen-Datenbank-Konzept

1. `docs/QUESTION_DATABASE_PLAN.md` erstellen
2. Tabellenmodell beschreiben
3. Review-Prozess beschreiben
4. Export-Strategie in App beschreiben

### v23.5.6 – Supabase Tabellenstruktur planen

1. Tabellenentwurf
2. RLS-Konzept
3. Rollenmodell
4. Datenfluss

### v23.5.7 – Rohfragen importieren

1. Rohfragen nur intern speichern
2. keine Veröffentlichung
3. Prüfung und Umformulierung vorbereiten

### v23.5.8 – geprüfte Fragen exportieren

1. approved/published Fragen exportieren
2. `questions.json` und mündliche Datenbanken kontrolliert erweitern
3. Preflight und Browser-Test

### v24 – Oral Exam Cleanup

1. Patch-Schichten reduzieren
2. mündliche Prüfung modularisieren
3. einheitliche Bogenlogik A/B/C
4. Fehlertraining stabil anbinden

### v24.3–v24.5 – Schriftliche Prüfungssimulation (erledigt)

1. `points`-Felder vollständig (v24.3a–i/j)
2. 82-Core-Fragen in Vollsimulation (v24.4b)
3. Teilpunkte-Logik im Prüfungsmodus (v24.5)

### v24.6 – Prüfungssimulation und UX (Auszug)

**Erledigt:** v24.6b (Wiederholung/offene Fragen), v24.6c (Pausieren/Fortsetzen), v24.6d/e (Mix), v24.6f/x (Prüfungsanalyse UI), v24.6g (Fehlerübersicht UI)

**Offen:**

1. **v24.6** – Browser-Endtest 82/120 mit Teilbewertung

### v25 – Schriftliche Fragenbank ausbauen

1. Fragenbank über 86 hinaus erweitern
2. Review- und Import-Prozess (siehe `docs/QUESTION_DATABASE_PLAN.md`)

### v26 – Rechtstexte

1. Impressum
2. Datenschutzerklärung
3. Nutzungsbedingungen
4. Trainingshinweise

### v27 – Supabase/Login

1. Auth
2. Teilnehmer aktiv/inaktiv
3. Fortschritt pro Nutzer
4. Admin-/Dozentenbereich

### v28 – PWA/App-Store

1. PWA-Struktur
2. Capacitor prüfen
3. Google Play Data Safety
4. Apple App Privacy

## 14. Nächster sinnvoller Schritt

### Abgeschlossener atomarer Bootstrap-Repair v27.37a-GATE-REPAIR

v27.37a-GATE-REPAIR abgeschlossen.

Titel: Enges Preflight-Nachfolgeprofil nach abgeschlossenem v27.36f bootstrapen.

Stabile Ausgangsbasis: `ac997149fe9600d735dcc237b0a30232d279cc52`.

Historische v27.36f-Grenzen bleiben `a68dd9e81f26c3a887e668b90e9f5e8973c7ddfa` für die Implementierung, `b035c62100b033dbce03a4ab016e4471b4ab54d4` für die Repair-Implementierung, `d2a303e3ca4cfd8b61a1e7b7f8e5c4b43682c712` für die Repair-Closure und `ac997149fe9600d735dcc237b0a30232d279cc52` für die endgültige v27.36f-Closure.

Der ursprüngliche v27.37a-Gate-Versuch konnte den unveränderten Preflight nicht legitim bestehen, weil dessen bisheriges Profil ausschließlich die abgeschlossenen v27.36f-/REPAIR-Lifecyclezustände kannte und bei einem Nachfolgetask auf historische Standalone-Checker zurückfiel. Die v27.36e-/v27.36f-Produktverträge waren dabei unverändert intakt. Ein normaler separater Repair-Gate-Commit hätte deshalb wissentlich keinen verpflichtenden Preflight-PASS erreicht.

Der ausdrücklich freigegebene einmalige atomare Bootstrap-Repair umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Das neue enge Preflight-Nachfolgeprofil akzeptiert nur den aktuellen atomaren Repair, dessen direkt folgenden committeten Zustand und später ausdrücklich autorisierte v27.37a-Gate-, Implementierungs- oder Closurezustände, sofern deren eigener Kontinuitätsvertrag passt. Unbekannte zukünftige Tasks werden nicht pauschal zugelassen. Es gibt keinen allgemeinen Bypass.

`index.html`, `app.js`, `data/supabase-participant-access-adapter.js`, `data/supabase-participant-access-bootstrap-bridge.js`, `data/supabase-participant-access-browser-provider.js` und `data/supabase-participant-access-browser-loader.js` bleiben gegenüber der endgültigen v27.36f-Closure unverändert und werden zusätzlich fachlich gegen die v27.36e-/v27.36f-Sicherheitsverträge geprüft.

Die lokale Sicherung `.git/v2737a-gate-preflight-blocked.patch` bleibt ausschließlich lokal, wird nicht verändert, nicht angewendet und nicht committet.

Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten. Keine automatische Client-Erzeugung. Keine direkten Auth- oder Tabellenabfragen werden freigegeben.

Nach dem Repair ist v27.37a weder ausgewählt noch autorisiert. `CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`; Commit und Push bleiben `NEIN`.

Der Lifecycle erkennt dynamisch `v2737a_gate_repair_atomic_prepared` und nach einem späteren direkten Sechs-Dateien-Commit `v2737a_gate_repair_atomic_committed`. Keine zukünftige Repair-, v27.37a-IMPLEMENTATION- oder v27.37a-CLOSURE-SHA wird hartcodiert.

### Abgeschlossener technischer Schritt v27.36f

v27.36f abgeschlossen.

Der technische Stand ist v27.36f vollständig abgeschlossen. Der letzte abgeschlossene funktionale Stand bleibt v27.35g.

Implementierungscommit: `a68dd9e81f26c3a887e668b90e9f5e8973c7ddfa`

Zusätzlicher enger Prüfpfad-Repair: v27.36f-REPAIR.

Repair-Implementierungscommit: `b035c62100b033dbce03a4ab016e4471b4ab54d4`

Repair-Closure: `d2a303e3ca4cfd8b61a1e7b7f8e5c4b43682c712`

v27.36f-REPAIR vollständig abgeschlossen.

Umgesetzte Dateien:

- `index.html`
- `app.js`
- `data/supabase-participant-access-browser-loader.js`
- `tools/check-participant-access-browser-loader-v2736f.py`
- `docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md`
- `tools/preflight.py`

Ergebnis:

- Loader-ID: `accaoui-participant-access-browser-loader`.
- Der finale Default bleibt `data-enabled="false"`.
- Nur der exakte Attributwert `"true"` fordert die Aktivierung an.
- Bei deaktiviertem Schalter bleibt der lokale Standardbetrieb unverändert und nicht blockierend.
- Bei angeforderter Aktivierung werden Adapter, Brücke und Browser-Provider in fester Reihenfolge geladen.
- Die Readiness-Oberfläche ist `window.ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY`.
- `app.js` verwendet weiterhin den v27.36d-Providervertrag mit `resolveAccess()`.
- Fehler bei angeforderter Aktivierung bleiben fail-closed ohne lokalen Fallback.
- Der generische Fehlerzustand ist `access_error`; interne Rohfehler werden nicht ausgegeben.
- Keine Fachlogik wurde dupliziert.

Repair-Abschluss:

- `closure_prepared` wird korrekt geprüft.
- `closure_committed` wird dynamisch geprüft.
- Die v27.36e-Regression bleibt über das enge v27.36f-Profil geschützt.
- Der Repair-Lifecycle ist vollständig geschlossen.
- Es gibt keinen pauschalen Bypass.
- Keine zukünftige Closure-SHA wird hartcodiert.

Testergebnis:

- v27.36f-Checker: PASS.
- Positivprüfungen: 41 PASS.
- Negativprüfungen: 27 PASS.
- Manipulationsprüfungen: 46 PASS.
- v27.36b-/v27.36c-/v27.36d-/v27.36e-Regressionen: PASS.
- Kontinuitätschecker: PASS.
- Preflight: PASS.
- `git diff --check`: PASS.

Sicherheitsgrenze:

- Supabase bleibt NICHT LIVE.
- Keine echten Keys.
- Keine echten Teilnehmerdaten.
- Kein echter Login ist produktiv aktiviert.
- Keine Live-Aktivierung.
- Kein `initializeClient()`.
- Kein `createClient()`.
- Keine direkte Auth-Abfrage.
- Keine Tabellenabfrage.
- Kein SQL.
- Keine Migration.
- Der Loader-Schalter bleibt standardmäßig `false`.

Kein Folgetask wurde ausgewählt oder autorisiert. Kein neuer Task und keine implizite Autorisierung bestehen.

#### Permanenter v27.36f-Lebenszyklus

Der Lifecycle erkennt dynamisch die Phasen `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed` und berücksichtigt den vollständig geschlossenen v27.36f-REPAIR-Verlauf.

Die ursprüngliche CLOSURE ist erst nach IMPLEMENTATION und vollständig geschlossenem Repair-Verlauf zulässig, enthält exakt die fünf Gate-Dateien und setzt beziehungsweise belässt `CURRENT_TASK` auf `NONE / BLOCKED / Autorisiert NEIN`.

Keine zukünftige CLOSURE-SHA wird hartcodiert. Rückkehr zu einem autorisierten v27.36f-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert. Rückkehr zu `v27.36f-REPAIR / AUTHORIZED` bleibt ohne neue ausdrückliche Autorisierung blockiert. Eine erneute v27.36f-IMPLEMENTATION ist nach `closure_committed` unzulässig.

### Abgeschlossener technischer Schritt v27.36e

v27.36e abgeschlossen.

Implementierungscommit: `0c4d64aaa7da7e8dd38fff1d7bf72675cb689a6f`

Umgesetzte Dateien:

- `data/supabase-participant-access-adapter.js`
- `data/supabase-participant-access-bootstrap-bridge.js`
- `data/supabase-participant-access-browser-provider.js`
- `tools/check-participant-access-browser-provider-v2736e.py`
- `docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md`
- `tools/preflight.py`

Ergebnis:

- Die CommonJS-Kompatibilität der v27.36b-/v27.36c-Bestandsmodule bleibt erhalten.
- Kontrollierte Browser-Exports verbinden die bestehenden Factories.
- Browser-Factory-Exports sind `window.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY` und `window.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY`.
- Der Browser-App-Provider ist `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`.
- Der Browser-Provider stellt ausschließlich `resolveAccess()` bereit.
- Keine Fachlogik wird dupliziert.
- Fehlende oder ungültige Dependencies sowie Throw, Reject und ungültige Ergebnisse bleiben fail-closed.
- Der Kollisionsschutz überschreibt keine inkompatiblen vorhandenen Globals.
- Es gibt keine automatische Client-Erzeugung.
- Es gibt keine direkten Supabase-, Auth- oder Tabellenabfragen im Provider.
- `index.html`, `app.js` und `style.css` bleiben unverändert.
- Die Browser-Kette ist noch NICHT über `index.html` aktiviert.
- Der lokale App-Start bleibt unverändert.
- Supabase bleibt NICHT LIVE.
- Keine echten Keys.
- Keine echten Teilnehmerdaten.

Testergebnis:

- v27.36e-Checker: PASS (Positiv: 22; Negativ: 31; Manipulation: 16).
- v27.36b-Checker: PASS.
- v27.36c-Checker: PASS.
- v27.36d-Regressionsprofil: PASS.
- Kontinuitätschecker: PASS.
- Preflight: PASS.
- `git diff --check`: PASS.

Kein Folgetask wurde ausgewählt oder autorisiert.

### Permanenter v27.36e-Lebenszyklus

Der Lifecycle erkennt dynamisch genau die Phasen `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed`.

Der Implementierungscommit ist historisch dokumentiert. Die Closure wird weiterhin dynamisch aus Git-Historie, Dateiumfang und geschlossenem Taskzustand erkannt.
Keine zukünftige CLOSURE-SHA wird hartcodiert.
Rückkehr zu einem autorisierten v27.36e-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.

### Abgeschlossener technischer Schritt v27.36d

v27.36d abgeschlossen.

Implementierungscommit: `b375dd3fc5fb820174f34a92ebbea81970b3ae29`

Umgesetzte Dateien:

- `app.js`
- `tools/check-participant-access-app-entry-v2736d.py`
- `docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md`
- `tools/preflight.py`

Ergebnis:

- Optionaler App-Provider: `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`.
- Die Schnittstelle bleibt ausschließlich `resolveAccess()`.
- Ohne Provider bleibt der lokale Standardbetrieb unverändert.
- Lokale Auth-Guard-Testzustände behalten Vorrang.
- Nur `allowed=true` zusammen mit `code="access_allowed"` startet die lokale App.
- Providerfehler und ungültige Ergebnisse bleiben fail-closed.
- Nach einem erkannten Providerfehler gibt es keinen lokalen Fallback.
- Ablehnungscodes werden auf die vorhandenen Zugangsansichten abgebildet.
- Unbekannte und technische Fehler bleiben generisch fail-closed.
- In app.js gibt es keine direkten Supabase- oder Datenbankabfragen.
- Bestehender Bootstrap, zentraler Adapter, v27.36b-Teilnehmerzugangs-Adapter und v27.36c-Brücke bleiben unverändert.
- Es besteht keine Browser-Verbindung zu den CommonJS-v27.36b/v27.36c-Modulen.
- Supabase bleibt NICHT LIVE.
- Keine echten Keys.
- Keine echten Teilnehmerdaten.

Testergebnis:

- v27.36d-Checker: PASS (Positiv: 2; Negativ: 36; Manipulation: 10).
- Kontinuitätschecker: PASS.
- Preflight: PASS.
- `git diff --check`: PASS.

Protected-Core:

- Der allgemeine Protected-Core-Schutz bleibt aktiv.
- Die v27.36d-Ausnahme war ausschließlich auf den autorisierten app.js-Scope begrenzt.
- Keine generelle Freigabe von app.js oder anderen Protected-Core-Dateien.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g.
Kein Folgetask wurde ausgewählt oder autorisiert. Die nächste Umsetzung bleibt
vollständig BLOCKED, bis sie ausdrücklich autorisiert wird.

### Permanenter v27.36d-Lebenszyklus

Die stabile Basis `f2f40389a22ea4a40acd7ebdf7ca672add4baf8e` muss Vorfahr
jedes legitimen v27.36d-HEAD bleiben. Der Lifecycle erkennt dynamisch genau die
Phasen `authorization_prepared`, `authorization_committed`,
`implementation_prepared`, `implementation_committed`, `closure_prepared` und
`closure_committed`.

GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien.
IMPLEMENTATION enthält exakt die vier autorisierten Implementierungsdateien und
ist höchstens einmal zulässig. CLOSURE ist erst nach IMPLEMENTATION zulässig,
enthält exakt die fünf Gate-Dateien und setzt `CURRENT_TASK` wieder auf
`NONE / BLOCKED / Autorisiert NEIN`. Keine zukünftige CLOSURE-SHA wird hartcodiert.
Rückkehr zu einem autorisierten v27.36d-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.

## 15. Wenn ein neuer Chat beginnt

Zuerst vollständig lesen:

```txt
AGENTS.md
docs/PROJECT_STATE_CURRENT.md
docs/PROJECT_MASTERLIST.md
docs/tasks/CURRENT_TASK.md
```

Vor jeder Änderung zusätzlich vollständig lesen:

```txt
docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md
docs/SUPABASE_EXAM_QUESTION_DATABASE_PLAN.md
```

Danach Branch und Commitstände direkt prüfen:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git ls-remote origin refs/heads/main
```

Lokalen und GitHub-HEAD direkt vergleichen. Bei einer Abweichung
sofort STOPP. Synchronisation nur nach gesonderter Freigabe.
Kein Task darf aus Versionsfolgen, früheren Chats oder
Erinnerung abgeleitet werden. Commit und Push erfolgen niemals
automatisch.

**Hinweis:** Neue Chats starten mit **GitHub-Dokumenten** (Liste oben). Große ZIPs mit Quellen-PDFs **nur bei Bedarf** hochladen – nicht standardmäßig in jeden Chat.

| Status-Dokument | Inhalt |
|-----------------|--------|
| `docs/ACCAOUI_SOURCE_MATERIAL_STATUS.md` | Quellenpakete, PDF-ZIPs, Extraktions- und Prüfstatus |
| `docs/ACCAOUI_ORAL_QUESTIONS_STATUS.md` | Mündliche Prüfung, Musterfragen, offene Aufgaben |

Alte Chat-Uploads und Prüfungsmuster sind **nicht automatisch** Arbeitsgrundlage im neuen Chat. Bei Bedarf erneut hochladen oder im Repo dokumentieren.

Keine Änderung ohne sauberen Arbeitsstand.
