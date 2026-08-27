# Accaoui §34a Lern-App – Cursor Master Context

Stand: v27.36f
Projekt: Accaoui §34a Lern-App
Arbeit: `C:\a34a`
Zuhause: `C:\xampp\htdocs\accaoui\v4-dashboard`
Branch: `main`
Repository: `asarrad-bit/accaoui-34a-lernapp`
Letzter abgeschlossener funktionaler Stand: v27.35g
Abschlusscommit: `f5f261fee67fc17c170ee714ae23761ff1668f17`

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

### Autorisierter Task v27.36f

v27.36f ist der einzige autorisierte Task.

Kontrollierten Browser-Aktivierungsweg für den Teilnehmerzugang hinter explizitem Schalter vorbereiten.

Dieser GATE-Schritt autorisiert nur die spätere Umsetzung; in diesem Schritt wird keine Implementierung vorgenommen.

Die funktionale Grundlage bleibt v27.35g. Die technische Grundlage ist der vollständig abgeschlossene Stand v27.36e. Die stabile Autorisierungsbasis ist `dc0d3fc87bde407cfac94fd598601ce4e80dfad7`.

Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:

- `index.html`
- `app.js`
- `data/supabase-participant-access-browser-loader.js`
- `tools/check-participant-access-browser-loader-v2736f.py`
- `docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md`
- `tools/preflight.py`

Verbindlicher Aktivierungsvertrag:

- `index.html` erhält genau ein kleines Loader-Skript mit der stabilen ID `accaoui-participant-access-browser-loader` unmittelbar vor `app.js`; der finale Default lautet `data-enabled="false"`.
- Ausschließlich der exakte Attributwert `"true"` fordert die Aktivierung an. Storage-, Query-, Cookie- oder frei steuerbare Nutzerwerte dürfen den Schalter nicht beeinflussen.
- Bei `data-enabled="false"` werden weder Teilnehmerzugangskette noch Provider, Client, Auth-, Datenbank- oder Netzwerkzugriff gestartet; der lokale Standardbetrieb bleibt unverändert und nicht blockierend.
- Bei `data-enabled="true"` lädt der Loader in fester Reihenfolge Adapter, Brücke und Browser-Provider und verwendet anschließend den bestehenden `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`.
- Die bevorzugte Readiness-Oberfläche ist `window.ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY`; sie legt weder Client, `userId`, Session-, Teilnehmer-, Kurs-, Key- noch Configdaten offen.
- `app.js` prüft ausschließlich die Loader-Readiness und verwendet danach unverändert den bestehenden v27.36d-Providervertrag mit `resolveAccess()`.
- Ist Aktivierung angefordert, bleiben fehlender oder nicht ausgeführter Loader, Ladefehler, fehlende Dependencies und ungültige Readiness fail-closed; es gibt keinen lokalen Fallback, und die App zeigt ausschließlich den generischen Zustand `access_error` ohne interne Rohfehler.
- `app.js` erkennt den Loader-Script-Tag mit `data-enabled="true"` auch dann als angeforderte Aktivierung, wenn das Loader-Skript fehlt oder nicht ausgeführt wurde.
- Keine Fachlogik aus v27.36b, v27.36c, v27.36d oder v27.36e wird dupliziert.

Sicherheitsgrenze:

- Keine Live-Aktivierung, kein `bootstrap.initializeClient()`, kein `supabase.createClient()`, kein SDK- oder Config-Zugriff, keine direkten Auth- oder Tabellenabfragen, kein SQL und keine Migrationen.
- Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.
- Die vorhandenen v27.36b-/v27.36c-/v27.36d-/v27.36e-Module, Bootstrap, Config, SQL, Migrationen, `questions.json` und `style.css` bleiben unverändert.
- Der spätere Checker arbeitet ausschließlich lokal mit synthetischen Browserzuständen und echten Manipulationsprüfungen; er prüft Default-off, exaktes `true`, Ladefolge, Readiness, fail-closed, Verbote, unveränderte Bestandsmodule und die Regressionen v27.36b/v27.36c/v27.36d/v27.36e.
- Der spätere Bericht dokumentiert Architektur, Schalter, Ladefolge, Readiness, Fail-closed-Grenze, Tests und ausdrücklich `Supabase live: NEIN`, `echte Keys: NEIN` und `echte Teilnehmerdaten: NEIN`.

Kein anderer Task und kein Folgetask ist ausgewählt oder autorisiert. Commit und Push bleiben NEIN.

### Permanenter v27.36f-Lebenszyklus

Der Lifecycle erkennt dynamisch genau die Phasen `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed`.

GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien. IMPLEMENTATION enthält exakt die sechs autorisierten Implementierungsdateien und ist höchstens einmal zulässig. CLOSURE ist erst nach IMPLEMENTATION zulässig, enthält exakt die fünf Gate-Dateien und setzt `CURRENT_TASK` auf `NONE / BLOCKED / Autorisiert NEIN`.

Keine zukünftige GATE-, IMPLEMENTATION- oder CLOSURE-SHA wird hartcodiert. Die stabile Basis bleibt ausschließlich als historische Autorisierungsbasis zulässig. Rückkehr zu einem autorisierten v27.36f-Zustand bleibt nach der Closure ohne neue ausdrückliche Autorisierung blockiert.

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
