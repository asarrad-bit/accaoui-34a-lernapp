# Prüfungsergebnishistorie-Anfrage-Identitätsstate

Stand: v27.29m

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`mapParticipantFullExamResultHistoryRequestIdentity(input)`

## Ziel

Jede vorbereitete Seitenanfrage erhält eine deterministische
Identität aus:

- Anfragefolge
- Limit
- Offset

## Sichere Zustände

- aktive Anfrage-Identität vorbereitet
- Response gehört zur aktuellen Anfrage
- Response gehört zu einer veralteten Anfrage
- Identität oder Anfrage ist ungültig

## Sicherheitsregeln

- Anfragefolge nur als positive sichere Ganzzahl
- Limit und Offset werden erneut validiert
- Offset muss am Limit ausgerichtet sein
- Response-Identitäten müssen kanonisch aufgebaut sein
- veraltete Antworten dürfen nicht übernommen werden
- keine Zufallswerte oder Zeitstempel
- keine RPC-Ausführung
- kein Supabase-Client
- kein Netzwerk
- keine Teilnehmer-ID
- keine Response-Inhalte
- keine sichtbare UI
