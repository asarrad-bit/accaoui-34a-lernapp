# Supabase Prüfungsintegrität-Lockdown Test

Stand: v27.24c

## Geprüfte Migration

`supabase/migrations/20260714_v2724b_exam_result_insert_lockdown.sql`

## Sicherheitsziel

Teilnehmer dürfen keine autoritativen Prüfungsdaten direkt eintragen.

Entfernte Policies:

- `exam_attempts_insert_own`
- `exam_answers_insert_own`

Es wird keine neue Teilnehmer-Insert-Policy angelegt.

## Automatische Prüfung

`py -3 tools/check-supabase-migrations.py`

Erwartet:

- 17 Basis-RLS-Policies
- 15 effektive RLS-Policies
- direkte Prüfungs-Inserts gesperrt
- keine Live-Ausführung

Ein vertrauenswürdiger RPC-/Server-Weg folgt später.

Status: Lockdown statisch geprüft
