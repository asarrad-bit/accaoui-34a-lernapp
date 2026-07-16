# Supabase Prüfungsfragen Schema- und RLS-Test

Stand: v27.26e

Status: statisch geprüft, nicht live ausgeführt

## Geprüfte Migrationen

- `20260716_v2725c_exam_question_schema.sql`
- `20260716_v2725d_exam_question_rls.sql`
- `20260716_v2726c_exam_attempt_answer_key_snapshot.sql`
- `20260716_v2726d_exam_attempt_grading_rule_partial_points.sql`
- `20260716_v2726e_exam_answers_integrity.sql`

## Geprüfte Tabellen

- `exam_questions`
- `exam_question_answer_keys`
- `exam_attempt_questions`
- `exam_attempt_question_answer_keys`

## Schema-Prüfung

Bestätigt wurden:

- versionierte Fragen
- getrennte private Lösungsschlüssel
- feste Prüfungsfrage-Snapshots
- private Lösungsschlüssel-Snapshots pro Versuchsfrage
- Teilpunkte: ein Punkt pro ausgewählter richtiger Antwort, kein Punktabzug
- `correct_answers` aus `exam_answers` entfernt
- Antworten eindeutig an `attempt_question_id` gebunden
- Versuchsfrage und Prüfungsversuch per Fremdschlüssel abgeglichen
- `selected_answers` als JSON-Array abgesichert
- Punktebereiche und Ergebniszustand abgesichert
- JSON-Array-Prüfungen
- vier Fragetypen: `single`, `multiple`, `praxisfall`, `combination`
- Punkte nur 1 oder 2
- Core-Positionen nur 1 bis 82
- eindeutige Fragenversionen
- keine doppelten Fragen oder Positionen je Versuch
- RLS auf allen vier Tabellen

## RLS-Prüfung

Bestätigt wurden:

- Prüfungsinhalte nur für aktive Admins und Dozenten
- Support ist ausgeschlossen
- zentrale und versuchsbezogene Lösungsschlüssel sind für Teilnehmer gesperrt
- Teilnehmer dürfen nur eigene Prüfungs-Snapshots lesen
- keine Teilnehmer-Schreibpolicy für Snapshots
- direkte Inserts, Updates und Deletes auf `exam_answers` entzogen
- fester `search_path` für den Rollen-Helper
- keine Live-Ausführung

## Automatische Migrationsprüfung

Erwarteter Stand:

- 8 SQL-Dateien
- 8 MVP-Tabellen
- 4 sichere Prüfungstabellen
- 12 Tabellen insgesamt
- 15 effektive Basis-Policies
- 3 Fragen-RLS-Policies
- 18 effektive Policies insgesamt

## Sicherheitsgrenze

Die Migrationen sind vorbereitet und statisch geprüft.

Es wurden keine echten Supabase-Schlüssel verwendet und keine
Migration wurde auf einer Live-Datenbank ausgeführt.

Sichere Snapshot-Schreibvorgänge und Prüfungsbewertungen folgen
später ausschließlich über geprüfte RPC-Funktionen.

Status: Fragen-Schema, RLS, private Versuchsschlüssel, Teilpunkte und Antwortintegrität statisch bestätigt
