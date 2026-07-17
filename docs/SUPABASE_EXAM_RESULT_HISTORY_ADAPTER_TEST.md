# Supabase Prüfungsergebnislisten-Adapter – statischer Test

Stand: v27.29b

Status: vorbereitet und statisch geprüft, ohne Live-Verbindung

## Ziel

Der bestehende sichere RPC aus v27.29a erhält einen klaren
lokalen Adaptervertrag, ohne Supabase bereits zu aktivieren.

## Adapter-Funktionen

- `getParticipantExamResultHistoryRpcState()`
- `listParticipantFullExamResults(options)`

## RPC-Vertrag

RPC-Name:

`accaoui_list_full_exam_results`

Erlaubte Parameter:

- `p_limit`
- `p_offset`

Nicht erlaubt:

- Teilnehmer-ID
- Punktewerte
- Bestehensstatus
- Prüfungsversuchs-ID
- Lösungsschlüssel

## Pagination

- Standardlimit: 20
- Mindestlimit: 1
- Höchstlimit: 50
- Mindestoffset: 0
- Höchstoffset: 10000
- nur ganzzahlige Werte

## Lokaler Sicherheitszustand

- RPC-Vertrag ist vorbereitet
- echter RPC-Aufruf ist nicht implementiert
- `canCallRpc` bleibt `false`
- keine Client-Erstellung
- keine Netzwerkabfrage
- keine Anmeldung wird erzwungen
- lokaler Unterrichtsbetrieb bleibt erlaubt
- Ergebnisliste bleibt leer und unsichtbar

## Rückgabe im lokalen Modus

Die Ladefunktion liefert kontrolliert:

- `ok: false`
- `isLiveCall: false`
- leeres Ergebnisarray
- keine Gesamtanzahl
- sicheren Blockierungsgrund
- ausschließlich RPC-Name, Limit und Offset als Request-Vorschau

## Adapter-Integration

Der RPC-State ist enthalten in:

- Supabase-Safety-Summary
- Adapter-Health-State
- öffentlichem Adapter-Export

Die bestehende lokale Dashboard-Prüfungshistorie bleibt
unverändert verborgen und nicht blockierend.

## Automatische Prüfung

`tools/check-supabase-exam-history-adapter.py`

Der Prüfer sperrt insbesondere:

- `.rpc(...)`
- `createClient(...)`
- `window.supabase`
- `fetch(...)`
- `participant_id`
- `service_role`

## Sicherheitsgrenze

- keine echten Supabase-Schlüssel
- keine Live-Datenbank
- keine echten Teilnehmerdaten
- keine Änderung an Fragenbeständen
- keine Änderung am sichtbaren UI
