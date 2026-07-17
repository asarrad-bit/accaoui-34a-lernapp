# Prüfungsergebnislisten-Aggregator – statischer Test

Stand: v27.29e

Status: vorbereitet und statisch geprüft, ohne Live-Daten

## Ziel

Normalisierte Ergebniszeilen werden zu sicheren Kennzahlen der
aktuell geladenen Seite zusammengefasst.

Da der Ergebnis-RPC paginiert ist, werden keine unvollständigen
Seitenwerte als globale Prüfungsstatistik ausgegeben.

## Funktion

`aggregateParticipantFullExamResultRows(rows)`

## Voraussetzung

Der Aggregator verwendet ausschließlich:

`normalizeParticipantFullExamResultRows(rows)`

Ungültige Zeilen oder Listen werden vollständig verworfen.

## Seitenbezogene Kennzahlen

- Anzahl der Zeilen auf der geladenen Seite
- bestandene Ergebnisse auf der Seite
- nicht bestandene Ergebnisse auf der Seite
- bester Seitenwert
- durchschnittlicher Seitenwert
- Bestehensquote der Seite
- zeitlich neuester Eintrag der Seite
- `total_count` des sicheren RPC

## Kennzeichnung

`metricsScope` ist immer:

`page_only`

## Globale Werte

Bewusst nicht berechnet werden:

- globale Anzahl bestandener Versuche
- globale Anzahl nicht bestandener Versuche
- globaler Durchschnitt
- globaler Bestwert

Diese Werte wären bei einer einzelnen paginierten Seite
möglicherweise unvollständig.

Daher gilt:

- `canPopulateGlobalOutcomeCounts: false`
- `globalPassedCount: null`
- `globalFailedCount: null`

## Dashboard-Zuordnung

Die unsichtbare Prüfungshistorie kennt jetzt:

- Namen des Aggregators
- vorbereiteten Aggregatorstatus
- Seitenumfang der Kennzahlen
- ausdrückliche Sperre globaler Ergebnisanzahlen

Die sichtbaren Dashboard-Kennzahlen bleiben weiterhin null.

## Sicherheitsgrenze

- kein RPC-Aufruf
- keine Netzwerkverbindung
- kein Supabase-Client
- keine Teilnehmer-ID
- keine Antworten oder Lösungsschlüssel
- keine sichtbare UI-Änderung
- keine Änderung an Fragenbeständen
