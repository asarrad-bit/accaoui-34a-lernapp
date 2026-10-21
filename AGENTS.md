# Aktive Ergänzung – persönlich bestätigte Entwicklungsfolge W00–W08

Paket ACCAOUI_AUTOMATISCHE_ENTWICKLUNGSFOLGE_20261021_V1; tatsächliche direkte Gesamtbestätigung:
Steuerchat 01a13bb5-4447-72c3-84d4-55246679ce0d,
Turn 01a15e2f-a343-7a40-a370-5fe2871e1129,
Nachricht 01a15e2f-a3f6-7262-86ea-ed8986e1090f.
Vollständiger bestätigter Plan: docs/DEVELOPMENT_SEQUENCE_V1.md.
Aktuelles genaues Paket/Pfadmanifest: docs/tasks/CURRENT_TASK.md und
docs/tasks/DEVELOPMENT_QUEUE_V1.json. Nur diese vorab genehmigte feste Folge.

Die bisherige Auswahl-/Folgetasksperre gilt weiter außerhalb dieser Queue.
Innerhalb der bestätigten Folge darf WORK CURRENT_TASK vor jeder Paketmutation
auf das erste geeignete festgelegte Paket setzen und nach bestandenen Pflichtchecks
ohne Routinezwischenfreigabe fortfahren. Keine neuen Aufgaben erfinden.
Die sonst unveränderte Regel „Bei jedem Fehler sofort STOPP“ wird ausschließlich
für diese Folge präzisiert: reine Aufruffehler ohne gestartete Fachprüfung/Mutation
einmal korrigieren; gewöhnliche Implementierungsfehler im aktiven Manifest höchstens
zwei gezielte Korrekturrunden mit passenden Tests. Echte Schutzkonflikte, fremde
Änderungen, ungeklärte Basis/Befugnis, automatische Ablehnung oder Geheimnis-/Datenfehler:
sofort STOPP. W01-Dauerlauf höchstens einmal, bei FAIL/TIMEOUT/Abbruch/Belegverlust STOPP.
Originalchecker, fachliche Erwartungen und Zeitbudgets bleiben erhalten.

Geprüfte sinnvolle Paket-Commits und normale Pushes sind durch diese konkrete
Gesamtbestätigung erlaubt, ausschließlich nach vollständiger Kontinuität,
vollständigem Original-Preflight mit Python3, diff-Prüfung und exaktem Schutz-/Scope-PASS.
GitHub danach direkt bestätigen. Keine leeren Verwaltungscommits, kein Force,
Amend/Rebase/Reset/Restore/Merge oder automatisches Entstagen.
v27.37n/Audit bleiben STOPP / NOT VERIFIED; Audit unverändert, unversioniert und
unkopiert/unübertragen. Keine alte Rohbelegsuche. Supabase NICHT LIVE.
Keine Produktion/Stores, echten Daten/Schlüssel/Nachrichten oder kostenpflichtigen Dienste.
Ein technischer Ausführer im bestehenden WORK-Chat, keine neuen Chats/Agenten.

## Unveränderte frühere allgemeine Regeln

# Verbindliche Projektregeln

- `docs/PROJECT_MASTERLIST.md` ist die verbindliche Projektquelle.
- Vor jeder Arbeit müssen vollständig gelesen werden:
  - `docs/PROJECT_STATE_CURRENT.md`
  - `docs/PROJECT_MASTERLIST.md`
  - `docs/tasks/CURRENT_TASK.md`
- Kein Task darf aus Versionsfolgen, früheren Chats oder Erinnerung abgeleitet werden.
- Eine Umsetzung ist nur zulässig, wenn `docs/tasks/CURRENT_TASK.md` den Task ausdrücklich autorisiert.
- Bei einem Widerspruch zwischen den verbindlichen Projektdateien sofort STOPP.
- Bei einem Chatwechsel muss der neue Chat den GitHub-HEAD direkt prüfen.
- Lokaler Arbeitsbaum und GitHub-Stand müssen vor Änderungen bestätigt werden.
- Vor jeder Änderung müssen zusätzlich gelesen werden:
  - `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
  - `docs/SUPABASE_EXAM_QUESTION_DATABASE_PLAN.md`
- Nur den ausdrücklich vorgegebenen Versionsschritt bearbeiten.
- Keine eigenständige Auswahl des nächsten Tasks.
- Keine Live-Supabase-Verbindung.
- Keine echten Schlüssel oder Zugangsdaten.
- Keine echten Teilnehmerdaten.
- Schriftliche Fragen, mündliche Fragen und Lernkarten getrennt halten.
- Kein `git reset`.
- Kein `git restore`.
- Keine unerwarteten Änderungen entfernen.
- Vor jedem Commit:
  - `git diff --check`
  - `tools/preflight.py` muss mit einem verfügbaren Python-3-Interpreter ausgeführt werden.
  - Erlaubte Reihenfolge: `py -3`, `python`, `python3` oder ein vorhandener absoluter Python-Pfad.
  - Der Preflight darf niemals übersprungen werden.
- Bei jedem Fehler sofort STOPP.
- Bei STOPP nicht committen und nicht pushen.
- Commit und Push nur nach ausdrücklichem Auftrag.
- Niemals direkt behaupten, ein Push sei erfolgreich, bevor GitHub geprüft wurde.
