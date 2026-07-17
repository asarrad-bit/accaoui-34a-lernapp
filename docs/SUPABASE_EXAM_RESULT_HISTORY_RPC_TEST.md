# Sichere Prüfungsergebnisliste – statischer RPC-Test

Stand: v27.29a

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260717_v2729a_exam_result_history_rpc.sql`

## Funktion

`public.accaoui_list_full_exam_results(p_limit, p_offset)`

## Ziel

Teilnehmer können ihre abgeschlossenen Vollsimulationen sicher
und seitenweise laden, ohne vorher eine Prüfungsversuchs-ID kennen
zu müssen.

## Identität und Berechtigung

- Teilnehmeridentität ausschließlich über `auth.uid()`
- nur eigene Prüfungsversuche
- nur abgeschlossene Vollsimulationen
- Status `active`, `expired` und `completed`
- Status `blocked` ausgeschlossen
- keine übergebene Teilnehmer-ID

## Pagination

- Standardlimit 20
- Limit nur zwischen 1 und 50
- Offset nur zwischen 0 und 10000
- deterministische Reihenfolge nach Abschlusszeit und Versuchs-ID
- Gesamtzahl eigener Ergebnisse über `total_count`

## Ergebnisdaten

Zurückgegeben werden ausschließlich:

- Prüfungsversuchs-ID
- Kurs-ID und aktueller Kurstitel
- Punkte und Maximalpunkte
- Bestehensstatus
- Start- und Abschlusszeit
- Gesamtzahl eigener abgeschlossener Ergebnisse

## Integritätsprüfung

Vor der Rückgabe wird geprüft:

- exakt 120 Maximalpunkte
- Punktebereich 0 bis 120
- Bestehensstatus entspricht mindestens 60 Punkten
- Startzeit ist vorhanden
- Abschluss liegt nicht vor dem Start

Die vollständige 82-Fragen- und Antwortintegrität bleibt Aufgabe
des detaillierten RPC `accaoui_get_full_exam_result(...)`.

## Sicherheitsgrenze

- keine Antworten
- keine richtigen Antwortindizes
- keine Lösungsschlüssel
- keine Erklärungen
- keine privaten Schlüssel-Tabellen
- keine Schreiboperation
- Ausführungsrecht ausschließlich für `authenticated`
- keine Live-Supabase-Ausführung
- keine echten Teilnehmerdaten oder Schlüssel
