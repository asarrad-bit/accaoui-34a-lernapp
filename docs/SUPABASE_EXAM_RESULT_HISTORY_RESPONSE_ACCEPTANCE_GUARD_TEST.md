# Prüfungsergebnishistorie-Response-Annahme-Guard

Stand: v27.29n

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`guardParticipantFullExamResultHistoryResponseAcceptance(input)`

## Aufgabe

Der Guard prüft zuerst die Anfrage- und Antwortidentität.

Nur eine Antwort, die exakt zur aktiven Anfragefolge, zum Limit
und zum Offset gehört, darf an den sicheren
Datenquellen-Orchestrator übergeben werden.

## Sichere Zustände

- aktuelle Antwort angenommen
- aktuelle leere Antwort angenommen
- veraltete Antwort ungelesen ignoriert
- ungültige Antwortidentität verworfen
- aktuelle, aber fehlerhafte Antwort sicher reduziert

## Sicherheitsregeln

- veraltete Antworten werden vor dem Lesen der Response verworfen
- keine rohe RPC-Antwort im Rückgabestate
- keine Backend-Fehlerdetails
- kein direkter RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- keine Teilnehmer-ID
- keine sichtbare UI
