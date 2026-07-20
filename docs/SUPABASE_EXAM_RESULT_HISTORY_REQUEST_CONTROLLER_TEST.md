# Prüfungsergebnishistorie-Anfrage-Controller

Stand: v27.29q

Status: lokal vorbereitet und ausführbar, ohne Live-RPC

## Funktion

`mapParticipantFullExamResultHistoryRequestControllerState(input)`

## Controller-Aktionen

- Anfrage initialisieren
- vorbereitete Anfrage starten
- aktuelle Response sicher annehmen
- nächste oder vorherige Anfrage vorbereiten
- Anfrage mit geprüftem Grund verwerfen

## Verbundene Sicherheitsbausteine

- Navigations-Intent-State
- Anfrage-Identitätsstate
- Anfrage-Lebenszyklus-State
- Lebenszyklus-Übergangs-Guard
- Response-Annahme-Guard

Veraltete Responses werden vor dem Lesen ignoriert. Eine neue
Navigation benötigt eine höhere Anfragefolge und eine zum
abgeschlossenen Lebenszyklus passende Datenquellenanfrage.

Keine RPC-Ausführung, kein Supabase-Client, kein Netzwerk,
keine Teilnehmer-ID, keine rohe Response und keine sichtbare UI.
