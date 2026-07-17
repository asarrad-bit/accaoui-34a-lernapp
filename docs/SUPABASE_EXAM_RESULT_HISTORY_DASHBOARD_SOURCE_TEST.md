# Prüfungshistorie-Dashboard-Datenquelle – statischer Test

Stand: v27.29c

Status: vorbereitet und statisch geprüft, ohne Live-Verbindung

## Ziel

Der sichere Ergebnislisten-Adapter aus v27.29b wird als
zukünftige Datenquelle der vorhandenen Dashboard-Prüfungshistorie
zugeordnet.

Es wird noch keine Ergebnisliste geladen oder angezeigt.

## Neuer State

`getParticipantDashboardExamHistoryDataSourceState()`

## Datenquelle

- Typ: `supabase_rpc`
- RPC: `accaoui_list_full_exam_results`
- Standardlimit: 20
- Standardoffset: 0
- Einträge: leeres Array
- Gesamtanzahl: null

## Dashboard-Zuordnung

`getParticipantDashboardExamHistoryState()` enthält jetzt:

- Status der Datenquelle
- Datenquellentyp
- RPC-Name
- vorbereitete Pagination
- Kennzeichnung, dass die Datenquelle vorbereitet ist
- Kennzeichnung, dass Laden weiterhin gesperrt ist
- sichere Local-Mode-Blockierung

## Unveränderter lokaler Zustand

- Prüfungshistorie bleibt unsichtbar
- `canRender` bleibt false
- `canLoadExamHistory` bleibt false
- `hasExamHistoryData` bleibt false
- Ergebnisliste bleibt leer
- kein UI-Blocker
- kein Login-Zwang
- lokaler Zugriff bleibt erlaubt

## Sicherheitsgrenze

Der automatische Prüfer verbietet innerhalb der Datenquelle:

- `.rpc(...)`
- Aufruf der Ergebnislisten-Ladefunktion
- `createClient(...)`
- `window.supabase`
- `fetch(...)`
- `XMLHttpRequest`
- Teilnehmer-ID
- Service-Role

## Automatische Prüfung

`tools/check-supabase-exam-history-adapter.py`

## Nicht Bestandteil

- keine sichtbare Dashboard-Karte
- kein echter RPC-Aufruf
- keine echten Teilnehmerdaten
- keine Berechnung von Durchschnitt oder Bestwert
- keine Änderung an schriftlichen, mündlichen oder
  Lernkartenfragen
