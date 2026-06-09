# Accaoui §34a Lern-App – Cursor Master Context

Stand: v24.5
Projekt: Accaoui §34a Lern-App
Lokaler Pfad: `C:\xampp\htdocs\accaoui\v4-dashboard`
Branch: `main`
Repository: `asarrad-bit/accaoui-34a-lernapp`

## 1. Sofort-Regel

Keine Blind-Fixes. Cursor darf nicht eigenständig optimieren.

Immer zuerst prüfen:

```bash
git status
git log -1 --oneline
python tools/preflight.py
```

Vor jedem Commit:

```bash
python tools/preflight.py
git diff --check
git status --short
```

Nur committen, wenn Preflight grün ist, `git diff --check` keine Ausgabe zeigt und nur erlaubte Dateien geändert wurden.

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

### Entwicklungsstand Prüfungssimulation (v24.5)

| Version | Inhalt | Status |
|---|---|---|
| v24.3a–i | `points`-Felder alle 9 Sachgebiete | **erledigt** |
| v24.3j | Globaler Check 82 Core / 120 Punkte / 38 Zweipunktfragen | **erledigt** |
| v24.4b | Vollsimulation mit festen 82-Core-IDs | **erledigt** |
| v24.5 | Teilpunkte für Mehrfachantworten im Prüfungsmodus | **erledigt** |
| v24.6 | Browser-Endtest Vollsimulation mit Teilbewertung | **offen** |
| v24.6b | Wiederholungslogik: nur gefilterte Fragen (z. B. 34→45→56→60) | **offen** |
| v24.6x | Prüfungsanalyse nach Themen: UI-Kontraste/Karten | **offen** |

### UI-Hinweis Prüfungsanalyse

Die **Prüfungsanalyse nach Themen** wirkt aktuell blass und nicht klar genug strukturiert. Späterer UI-Task: stärkere Kontraste, klarere Karten, bessere Button-Position, professionellere Ergebnisdarstellung.

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

### v24.6 – Prüfungssimulation testen und nacharbeiten

1. Browser-Endtest 82/120 mit Teilbewertung (v24.6)
2. Wiederholungslogik korrigieren (v24.6b): nur gefilterte Fragen, z. B. 34→45→56→60, nicht 34→35→36
3. Prüfungsanalyse UI verbessern (v24.6x)

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

Als Nächstes (Code-Tasks):

1. **v24.6b** – Wiederholungslogik nach Prüfung: eigene gefilterte Fragenliste für unbeantwortete/falsche Fragen
2. **v24.6** – Browser-Endtest Vollsimulation 82/120 mit Teilbewertung
3. **v24.6x** – Prüfungsanalyse nach Themen optisch überarbeiten

Fehlerbeschreibung v24.6b:

- Wenn nur Fragen **34, 45, 56, 60** unbeantwortet sind, darf die Wiederholungsrunde **nur diese vier** enthalten.
- **Falsch:** 34 → 35 → 36 (volles Prüfungsset)
- **Richtig:** 34 → 45 → 56 → 60 (gefilterte Liste in fester Reihenfolge)

## 15. Wenn ein neuer Chat beginnt

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

**Hinweis:** Neue Chats starten mit **GitHub-Dokumenten** (Liste oben). Große ZIPs mit Quellen-PDFs **nur bei Bedarf** hochladen – nicht standardmäßig in jeden Chat.

| Status-Dokument | Inhalt |
|-----------------|--------|
| `docs/ACCAOUI_SOURCE_MATERIAL_STATUS.md` | Quellenpakete, PDF-ZIPs, Extraktions- und Prüfstatus |
| `docs/ACCAOUI_ORAL_QUESTIONS_STATUS.md` | Mündliche Prüfung, Musterfragen, offene Aufgaben |

Alte Chat-Uploads und Prüfungsmuster sind **nicht automatisch** Arbeitsgrundlage im neuen Chat. Bei Bedarf erneut hochladen oder im Repo dokumentieren.

Keine Änderung ohne sauberen Arbeitsstand.
