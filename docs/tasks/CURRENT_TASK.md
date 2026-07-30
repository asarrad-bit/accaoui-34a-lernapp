# Verbindlicher aktueller Task

Task-ID: NONE
Status: BLOCKED
Autorisiert: NEIN
Letzter abgeschlossener funktionaler Stand: v27.35d
Letzter abgeschlossener Task: v27.35d
Abschlusscommit: `b4d2de5002918766bb45fe001cbbfdb333a6d7c5`
Erwarteter Ausgangscommit: `b4d2de5002918766bb45fe001cbbfdb333a6d7c5`
Erlaubte Dateien: keine
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Abschluss von v27.35d

- Lernmodus eindeutig als „Lernmodus – Wissen prüfen“ gekennzeichnet.
- Lernkarten eindeutig als „Lernkarten – Wissen selbst einschätzen“ gekennzeichnet.
- Führungshinweise über die gemeinsame Klasse `mode-guidance-v2735d`.
- Keine neue Speicherung, keine neuen Storage-Keys, keine Fragenänderung.
- Keine Supabase-, SQL-, Datenbank- oder Netzwerkänderung.
- Bestehende Navigation, Pause/Fortsetzen und localStorage-Logik unverändert.
- Browser-Tests Dashboard, Lernmodus, Lernkarten und Mobilansicht bestanden.
- `node --check app.js`, `git diff --check` und Preflight bestanden.

## Verbindlich festhalten

- v27.35d ist abgeschlossen.
- Kein Folgetask ist ausgewählt.
- Kein Task darf aus Versionsfolge, Erinnerung oder früheren Chats
  abgeleitet werden.
- Ein neuer Task muss ausdrücklich durch Projekteigentümer,
  verbindlichen Projektchat und `CURRENT_TASK` autorisiert werden.
- Commit und Push bleiben bis zu einer gesonderten ausdrücklichen
  Freigabe gesperrt.

## Pflichtfelder eines später autorisierten Tasks

- Task-ID
- Ziel
- Erwarteter Ausgangsstand
- Erlaubte Dateien
- Verbotene Dateien
- Akzeptanzkriterien
- Tests
- Commit-Freigabe
- Push-Freigabe
