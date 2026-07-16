# Supabase Prüfungsfragen Schema- und RLS-Test

Stand: v27.25e

Status: statisch geprüft, nicht live ausgeführt

## Geprüfte Migrationen

- `20260716_v2725c_exam_question_schema.sql`
- `20260716_v2725d_exam_question_rls.sql`

## Geprüfte Tabellen

- `exam_questions`
- `exam_question_answer_keys`
- `exam_attempt_questions`

## Schema-Prüfung

Bestätigt wurden:

- versionierte Fragen
- getrennte private Lösungsschlüssel
- feste Prüfungsfrage-Snapshots
- JSON-Array-Prüfungen
- vier Fragetypen: `single`, `multiple`, `praxisfall`, `combination`
- Punkte nur 1 oder 2
- Core-Positionen nur 1 bis 82
- eindeutige Fragenversionen
- keine doppelten Fragen oder Positionen je Versuch
- RLS auf allen drei Tabellen

## RLS-Prüfung

Bestätigt wurden:

- Prüfungsinhalte nur für aktive Admins und Dozenten
- Support ist ausgeschlossen
- Lösungsschlüssel sind für Teilnehmer gesperrt
- Teilnehmer dürfen nur eigene Prüfungs-Snapshots lesen
- keine Teilnehmer-Schreibpolicy für Snapshots
- fester `search_path` für den Rollen-Helper
- keine Live-Ausführung

## Automatische Migrationsprüfung

Erwarteter Stand:

- 5 SQL-Dateien
- 8 MVP-Tabellen
- 3 sichere Prüfungstabellen
- 11 Tabellen insgesamt
- 15 effektive Basis-Policies
- 3 Fragen-RLS-Policies
- 18 effektive Policies insgesamt

## Sicherheitsgrenze

Die Migrationen sind vorbereitet und statisch geprüft.

Es wurden keine echten Supabase-Schlüssel verwendet und keine
Migration wurde auf einer Live-Datenbank ausgeführt.

Sichere Snapshot-Schreibvorgänge und Prüfungsbewertungen folgen
später ausschließlich über geprüfte RPC-Funktionen.

Status: Fragen-Schema und RLS statisch bestätigt
