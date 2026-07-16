# Supabase Auswahlbegrenzung – statischer Sicherheitcat > docs/SUPABASE_EXAM_SELECTION_LIMIT_SECURITY_TEST.md <<'stest

Stand: v27.27e

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260716_v2727e_exam_selection_limit_security.sql`

## Korrigierte Funktionen

- `public.accaoui_save_exam_answer(uuid, jsonb)`
- `public.accaoui_finish_full_exam(uuid)`

## Bestätigte Sicherheitsregeln

- die erlaubte Auswahlzahl stammt aus dem privaten Lösungssnapshot
- richtige Antwortindizes werden nicht an den Browser ausgegeben
- Auswahlzahl und Punktewert bleiben getrennte Regeln
- `single` und `combination` benötigen genau einen richtigen Index
- `multiple` und `praxisfall` dürfen mehrere richtige Indizes besitzen
- mehr Auswahlen als richtige Lösungspositionen werden abgelehnt
- Antwortindizes bleiben auf Bereich und Duplikate geprüft
- manipulierte Überauswahlen werden beim Abschluss erneut abgelehnt
- alte Antwortspeicher- und Abschluss-RPCs werden kontrolliert ersetzt
- beide Funktionen besitzen einen festen `search_path`
- beide Funktionen verwenden `row_security=off`
- Ausführungsrecht ausschließlich für `authenticated`
- keine direkten Tabellenrechte werden vergeben
- keine Lösungsschlüssel werden zurückgegeben

## Sicherheitswirkung

Ein Teilnehmer kann nicht mehr alle Antwortmöglichkeiten auswählen,
um trotz falscher Zusatzkreuze automatisch alle möglichen Punkte zu
erhalten.

## Sicherheitsgrenze

Keine Migration wurde live ausgeführt.

Es wurden keine echten Teilnehmerdaten und keine geheimen
Supabase-Schlüssel verwendet.
