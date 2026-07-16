# Supabase Prüfungsstart-RPC – statischer Sicherheitstest

Stand: v27.27a

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260716_v2727a_exam_start_rpc.sql`

## Funktion

`public.accaoui_start_full_exam(p_course_id uuid)`

## Bestätigte Sicherheitsregeln

- Teilnehmer ausschließlich über `auth.uid()`
- keine Teilnehmer-ID als Browserparameter
- aktiver Teilnehmer erforderlich
- aktiver und zeitlich gültiger Kurszugang erforderlich
- Advisory Lock gegen parallele Doppelstarts
- höchstens eine offene Vollsimulation pro Teilnehmer und Kurs
- vollständiger offener Versuch wird fortgesetzt
- exakt 82 Core-Fragen und 120 Punkte
- sichtbare und private Snapshots entstehen atomar
- Fehler rollen den gesamten Prüfungsstart zurück
- fester `search_path`
- `security definer` mit kontrollierter Funktion
- Ausführungsrecht ausschließlich für `authenticated`
- keine Lösungsschlüssel oder Erklärungen in der Rückgabe

## Rückgabe

- `exam_attempt_id uuid`
- `question_count integer`
- `max_points integer`
- `resumed boolean`

## Sicherheitsgrenze

Keine Migration wurde live ausgeführt.

Es wurden keine echten Teilnehmerdaten und keine geheimen
Supabase-Schlüssel verwendet.
