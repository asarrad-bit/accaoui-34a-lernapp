# Prüfungsergebnishistorie-Navigations-Intent-State

Stand: v27.29l

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`mapParticipantFullExamResultHistoryNavigationIntent(input)`

## Unterstützte Intents

- `first`
- `previous`
- `next`
- `retry`

## Sicherheitsregeln

- aktuelle Anfrage muss gültig und am Limit ausgerichtet sein
- Navigation während eines Ladevorgangs ist blockiert
- vorherige und nächste Seite benötigen einen gültigen
  Pagination-State
- Retry ist nur nach einem wiederholbaren Fehler zulässig
- Ziel-Limit und Ziel-Offset werden erneut validiert
- keine RPC-Ausführung
- kein Supabase-Client
- kein Netzwerk
- keine Teilnehmer-ID
- keine rohen Fehlerdetails
- keine sichtbare UI
