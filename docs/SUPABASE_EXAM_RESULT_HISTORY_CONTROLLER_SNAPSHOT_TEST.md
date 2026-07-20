# Prüfungsergebnishistorie-Controller-Snapshot-Normalizer

Stand: v27.29r

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`normalizeParticipantFullExamResultHistoryControllerSnapshot(input)`

## Aufgabe

Gespeicherte Controllerzustände werden vor einer späteren
Wiederaufnahme vollständig neu geprüft und kanonisch reduziert.

## Geprüfte Zustände

- vorbereitet
- ausstehend
- abgeschlossen
- Navigation vorbereitet
- verworfen

## Sicherheitsregeln

- feste Snapshot-Version
- Controller- und Lebenszyklusmarker müssen gültig sein
- Anfrageidentität wird neu berechnet
- Status und Zustandsflags müssen zusammenpassen
- abgeschlossene Zustände prüfen Anzahl, Gesamtzahl und Pagination
- Navigationszustände prüfen die vorherige Anfrageidentität
- Ergebniszeilen und rohe Controllerobjekte werden nicht ausgegeben
- kein RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- keine Teilnehmer-ID
- keine sichtbare UI
