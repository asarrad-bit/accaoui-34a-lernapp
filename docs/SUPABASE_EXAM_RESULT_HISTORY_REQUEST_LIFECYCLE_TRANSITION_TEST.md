# Prüfungsergebnishistorie-Lebenszyklus-Übergangs-Guard

Stand: v27.29p

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`guardParticipantFullExamResultHistoryRequestLifecycleTransition(input)`

## Erlaubte Übergänge

- vorbereitet zu ausstehend
- vorbereitet zu verworfen
- ausstehend zu abgeschlossen
- ausstehend zu verworfen

Abgeschlossene und verworfene Anfragen sind Endzustände.

## Sicherheitsregeln

- aktueller Lebenszyklus-State muss gültig sein
- Anfrageidentität wird neu berechnet und verglichen
- Phasenflags müssen zum aktuellen Zustand passen
- Abschluss benötigt einen gültigen Response-Annahme-State
- Verwerfung benötigt einen erlaubten Grund
- Zielzustand muss dieselbe Anfrageidentität besitzen
- keine RPC-Ausführung
- kein Supabase-Client
- kein Netzwerk
- keine Teilnehmer-ID
- keine sichtbare UI
