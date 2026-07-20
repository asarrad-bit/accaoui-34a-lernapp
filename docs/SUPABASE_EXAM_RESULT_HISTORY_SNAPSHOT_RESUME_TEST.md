# Prüfungsergebnishistorie-Snapshot-Wiederaufnahme-State

Stand: v27.29s

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`mapParticipantFullExamResultHistorySnapshotResumeState(input)`

## Aufgabe

Ein gespeicherter Controller-Snapshot wird zuerst vollständig
durch den Snapshot-Normalizer geprüft.

Nur wiederaufnehmbare Zustände werden anschließend als
kanonischer lokaler Controllerzustand rekonstruiert.

## Wiederaufnehmbare Zustände

- vorbereitete Anfrage
- ausstehende Anfrage als Retry
- vorbereitete Navigationsanfrage

## Blockierte Zustände

- abgeschlossene Anfrage
- verworfene Anfrage
- ungültiger oder manipulierter Snapshot

## Sicherheitsregeln

- keine Wiederaufnahme ohne erfolgreichen Snapshot-Normalizer
- Anfrageidentität muss nach Rekonstruktion identisch bleiben
- ausstehende Zustände werden über den Controller neu gestartet
- terminale Zustände bleiben terminal
- rohe Snapshots und Ergebniszeilen werden nicht ausgegeben
- kein RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- keine Teilnehmer-ID
- keine sichtbare UI
