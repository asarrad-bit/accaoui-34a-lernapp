# Prüfungsergebnishistorie-Anfrage-Lebenszyklus

Stand: v27.29o

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`mapParticipantFullExamResultHistoryRequestLifecycle(input)`

## Zustände

- vorbereitet
- ausstehend
- abgeschlossen
- verworfen
- ungültig

## Regeln

Eine abgeschlossene Anfrage benötigt einen erfolgreich geprüften
Response-Annahme-State mit exakt passender Anfrageidentität.

Verwerfungsgründe sind auf Abbruch, Ablösung durch eine neue
Anfrage oder das Ignorieren einer veralteten Antwort begrenzt.

Es gibt keinen RPC-, Client- oder Netzwerkaufruf, keine
Teilnehmer-ID, keine rohe Response und keine sichtbare UI.
