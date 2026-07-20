# Prüfungsergebnishistorie-Snapshot-Erstellungsstate

Stand: v27.29t

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`mapParticipantFullExamResultHistorySnapshotCreationState(input)`

## Aufgabe

Nur wiederaufnehmbare Controllerzustände werden in einen
versionierten und datensparsamen Snapshot überführt.

## Zulässige Zustände

- vorbereitete Anfrage
- ausstehende Anfrage
- vorbereitete Navigationsanfrage

## Blockierte Zustände

- abgeschlossene Anfrage
- verworfene Anfrage
- ungültiger oder manipulierter Controllerzustand

## Sicherheitsregeln

- Controllerzustand wird zuerst vollständig normalisiert
- Anfrage und Lebenszyklus werden kanonisch rekonstruiert
- erstellter Snapshot muss den Normalizer erneut bestehen
- keine Ergebniszeilen
- keine unbekannten Controllerfelder
- keine Teilnehmer-ID
- keine Zeitstempel oder Zufallswerte
- kein RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- kein Local- oder Session-Storage
- keine sichtbare UI
