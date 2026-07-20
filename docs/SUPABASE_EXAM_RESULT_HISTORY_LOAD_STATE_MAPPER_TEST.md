# Prüfungsergebnishistorie-Ladezustands-Mapper

Stand: v27.29i

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`mapParticipantFullExamResultHistoryLoadState(input)`

## Sichere Zustände

- `exam_result_history_load_prepared`
- `exam_result_history_load_loading`
- `exam_result_history_load_success`
- `exam_result_history_load_empty`
- `exam_result_history_load_error`

## Verarbeitung

Bei einer aufgelösten Anfrage wird ausschließlich der sichere
Response-Mapper aus v27.29h verwendet.

Erfolgreiche Ergebnisse, leere Ergebnisse und ungültige Daten
werden klar getrennt. Abgelehnte Anfragen liefern ausschließlich
den neutralen Grund `rpc_request_failed`.

## Sicherheitsgrenze

- kein RPC-Aufruf
- kein Supabase-Client
- kein Netzwerk
- keine echten Teilnehmerdaten
- keine rohen Backend- oder Netzwerkfehler
- keine Teilnehmer-ID
- keine Antworten oder Lösungsschlüssel
- keine sichtbare UI
