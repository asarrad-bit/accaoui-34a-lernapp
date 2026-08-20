# Accaoui §34a Lern-App – Cursor Master Context

Stand: v27.36b
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

v27.36a ist vollständig abgeschlossen.

Audit-Commit: `f545a6c2b14a64a5bcb7bf60a2932315e571ef01`

`CURRENT_TASK` ist `v27.36b` / `AUTHORIZED` / `Autorisiert: JA`.

Ausgangs-HEAD: `f7672c98a1368dec501416853830ac03e0de2d41`

Die Audit-Empfehlung „lokale injizierbare Auth-/Teilnehmerzugangs-Komponente
mit lokalem Fake-Client“ ist jetzt ausdrücklich als v27.36b autorisiert.

Einziger autorisierter Task: Lokale injizierbare
Auth-/Teilnehmerzugangs-Komponente mit Fake-Client umsetzen.

Für die spätere Umsetzung sind genau vier Dateien erlaubt:

- `data/supabase-participant-access-adapter.js`
- `tools/check-supabase-participant-access-adapter.py`
- `docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md`
- `tools/preflight.py`

In diesem Autorisierungsschritt wird die Komponente noch nicht implementiert.

Die spätere Komponente erhält ausschließlich einen explizit injizierten
Supabase-kompatiblen Client und eine injizierte UTC-Zeitquelle. Sie bindet
Nutzer nur über `session.user.id` und verwendet ausschließlich die
kanonischen Tabellen `participants`, `enrollments` und `courses` der
aktuellen MVP-Migrationen. Der Access-State bleibt bei fehlenden,
fehlerhaften, gesperrten, abgelaufenen, fremden, mehrdeutigen oder
inkonsistenten Daten fail-closed.

Der spätere Test verwendet ausschließlich einen lokalen synthetischen
In-Memory-Fake-Client. Keine globale Supabase-Auflösung, kein echter Client,
kein Netzwerk, keine Datenbank, keine SQL- oder Migrationsausführung, kein
SDK und keine Config-Aktivierung.

Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten
Teilnehmerdaten. `app.js`, `index.html`, der zentrale Adapter, Bootstrap,
Config, SQL, Migrationen, RLS, RPCs und Login-UI bleiben unverändert.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g. Kein Folgetask
nach v27.36b wurde ausgewählt oder autorisiert. Commit und Push bleiben NEIN.

### Permanenter v27.36b-Lebenszyklus

`f7672c98a1368dec501416853830ac03e0de2d41` ist die stabile
v27.36b-Autorisierungsbasis und muss Vorfahr jedes legitimen späteren HEAD
bleiben. `HEAD ==` Basis darf nicht dauerhaft verlangt werden. Keine
zukünftige Autorisierungs-, Implementierungs- oder Closure-SHA wird
hartcodiert.

Der Checker klassifiziert Commits dynamisch aus Git-Historie, tatsächlicher
Dateimenge, CURRENT_TASK-Zustand und Working Tree. GATE ist eine nichtleere
Teilmenge der fünf Gate-Dateien. IMPLEMENTATION enthält exakt die vier
autorisierten Implementierungsdateien und ist nur einmal zulässig. CLOSURE
folgt erst nach gültiger IMPLEMENTATION und enthält ausschließlich
Gate-Dateien mit geschlossenem Taskzustand.

Mindestens sechs Phasen werden erkannt: Autorisierung lokal vorbereitet;
Autorisierung committet; Implementation lokal vorbereitet; Implementation
committet; Closure lokal vorbereitet; Closure committet. Legitime
Gate-Korrekturen bleiben möglich.

Falsche Basis, fremde Dateien, Implementation vor Autorisierung, mehrere
Implementierungscommits, App-, UI-, zentraler Adapter-, Bootstrap-, Config-,
SQL-, Migrations-, Supabase- oder Netzwerkänderungen, Commit oder Push `JA`,
automatischer Folgetask, Closure vor Implementation und Rückkehr aus der
abgeschlossenen v27.36b-Closure bleiben geschlossen blockiert.

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
