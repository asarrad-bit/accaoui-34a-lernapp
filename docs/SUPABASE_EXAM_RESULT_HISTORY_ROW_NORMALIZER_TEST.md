# Prüfungsergebniszeilen-Normalizer – statischer Test

Stand: v27.29d

Status: vorbereitet und statisch geprüft, ohne Live-Daten

## Ziel

Spätere Zeilen des sicheren Ergebnislisten-RPC werden vor einer
Dashboard-Nutzung streng geprüft und auf erlaubte Felder reduziert.

## Funktionen

- `normalizeParticipantFullExamResultRow(row)`
- `normalizeParticipantFullExamResultRows(rows)`

## Erlaubte Eingabefelder

- `exam_attempt_id`
- `course_id`
- `course_title`
- `score_points`
- `max_points`
- `passed`
- `started_at`
- `finished_at`
- `total_count`

## Prüfung einer Ergebniszeile

Geprüft werden:

- gültige UUID der Prüfungsversuchs-ID
- Kurs-ID ist null oder eine gültige UUID
- Kurstitel ist null oder ein begrenzter Text
- Punkte sind ganzzahlig zwischen 0 und 120
- Maximalpunkte sind exakt 120
- `passed` entspricht `score_points >= 60`
- Start- und Abschlusszeit sind gültig
- Abschluss liegt nicht vor dem Start
- `total_count` ist eine sichere positive Ganzzahl

## Prüfung einer Ergebnisliste

- Eingabe muss ein Array sein
- leere Listen bleiben gültig und enthalten keine Daten
- jede Zeile muss einzeln gültig sein
- Prüfungsversuchs-IDs dürfen nicht doppelt vorkommen
- `total_count` muss in allen Zeilen identisch sein
- `total_count` darf nicht kleiner als die Zeilenanzahl sein
- bei einem Fehler wird die gesamte Liste geschlossen verworfen

## Sichere Ausgabe

Ausgegeben werden ausschließlich normalisierte Felder in CamelCase.

Nicht übernommen werden:

- richtige Antworten
- ausgewählte Antworten
- Antwortmöglichkeiten
- Fragetexte
- Erklärungen
- Antwort-Hashes
- Teilnehmer-ID
- unbekannte Zusatzfelder

## Dashboard-Zuordnung

Die unsichtbare Datenquelle aus v27.29c enthält jetzt:

- Namen des Normalizers
- Kennzeichnung `isNormalizerPrepared`
- lokale Normalisierungserlaubnis
- weiterhin ein leeres Ergebnisarray
- weiterhin keinen Live-Aufruf

## Sicherheitsgrenze

- keine Netzwerkverbindung
- kein Supabase-Client
- kein RPC-Aufruf
- keine echten Teilnehmerdaten
- keine sichtbare Prüfungshistorie
- keine autoritative Bewertung im Browser
- keine Änderung an Fragenbeständen
