# Prüfungsergebnishistorie-Datenquellen-Orchestrator

Stand: v27.29k

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`orchestrateParticipantFullExamResultHistoryDataSourceState(input)`

## Aufgabe

Der Orchestrator verbindet:

- sicheren Ladezustands-Mapper
- sicheren Response-Mapper
- sicheren Pagination-Navigationsstate

## Sichere Gesamtzustände

- vorbereitet
- lädt
- erfolgreich
- leer
- Fehler

## Sicherheitsregeln

- ungültige Pagination wird vor der Verarbeitung geschlossen verworfen
- RPC-Antworten laufen ausschließlich durch den Response-Mapper
- Seiteneintragszahl muss zu den normalisierten Ergebnissen passen
- eine leere Folgeseite wird nicht als globale leere Historie behandelt
- rohe RPC- und Transportfehler werden nicht übernommen
- keine Teilnehmer-ID
- kein Supabase-Client
- kein Netzwerk
- kein Live-RPC
- keine sichtbare UI
