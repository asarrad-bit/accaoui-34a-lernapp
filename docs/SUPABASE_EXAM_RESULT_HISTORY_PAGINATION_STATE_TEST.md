# Prüfungsergebnishistorie-Pagination-Navigationsstate

Stand: v27.29j

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`mapParticipantFullExamResultHistoryPaginationState(input)`

## Zustände

- Gesamtzahl noch unbekannt
- leere Ergebnisliste
- erste Seite
- mittlere Seite
- letzte Seite
- ungültige Pagination
- technisch begrenzte Navigation

## Berechnete Werte

- aktuelle Seite
- Gesamtseiten
- vorheriger Offset
- nächster Offset
- erste oder letzte Seite
- vorwärts und rückwärts navigierbar
- bekannte oder unbekannte Gesamtzahl

## Sicherheitsgrenze

- Limit 1 bis 50
- Offset 0 bis 10000
- Offset muss am Seitenlimit ausgerichtet sein
- keine Ableitung eines nächsten Offsets ohne bekannte Gesamtzahl
- kein RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- keine echten Teilnehmerdaten
- keine sichtbare UI
