# Supabase Prüfungsversuch-Integrität – statischer Test

Stand: v27.28b

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260717_v2728b_exam_attempt_integrity.sql`

## Ziel

Zusätzliche Datenbankgrenzen verhindern widersprüchliche
Punkte- und Zeitwerte in `exam_attempts`.

## Bestätigte Integritätsregeln

- `score_points` darf `max_points` nicht überschreiten
- offene Prüfungsversuche dürfen `finished_at = null` besitzen
- abgeschlossene Prüfungsversuche benötigen eine Startzeit
- `finished_at` darf nicht vor `started_at` liegen
- bestehende ungültige Daten führen zum Abbruch der Migration
- keine Daten werden automatisch verändert oder gelöscht
- keine neue RLS-Policy
- keine direkten Tabellenrechte
- keine Service-Role
- keine Live-Ausführung

## Einordnung

Die RPC-Funktionen setzen bereits kontrollierte Prüfungswerte.

Die Datenbank-Constraints bilden eine zusätzliche
Defense-in-Depth-Grenze gegen widersprüchliche Daten.

## Sicherheitsgrenze

Es wurden keine echten Teilnehmerdaten verwendet und keine
Migration auf einer Live-Datenbank ausgeführt.
