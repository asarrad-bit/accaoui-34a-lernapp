# Supabase Antwortspeicher-RPC – statischer Sicherheitstest

Stand: v27.27c

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260716_v2727b_exam_answer_save_rpc.sql`

## Funktion

`public.accaoui_save_exam_answer(
p_attempt_question_id uuid,
p_selected_answers jsonb
)`

## Bestätigte Sicherheitsregeln

- Teilnehmer wird ausschließlich über `auth.uid()` bestimmt
- nur Fragen einer eigenen offenen Vollsimulation sind erlaubt
- aktiver Teilnehmer- und Kurszugang ist erforderlich
- der Browser übermittelt keine Prüfungsversuchs-ID
- der Browser übermittelt keine Punkte
- der Browser übermittelt keinen Ergebnisstatus
- der Browser übermittelt keine Lösungsschlüssel
- `selected_answers` muss ein JSON-Array sein
- nur ganzzahlige und vorhandene Antwortindizes sind erlaubt
- doppelte Antwortindizes werden abgelehnt
- Antwortindizes werden sortiert und normalisiert
- bei `single` und `combination` ist höchstens ein Index erlaubt
- bei `multiple` und `praxisfall` sind mehrere Indizes möglich
- die Punktzahl begrenzt nicht die Zahl auswählbarer Antworten
- erneutes Speichern aktualisiert dieselbe Versuchsfrage
- Punkte und Richtigkeitsstatus bleiben bis zur Bewertung neutral
- Ausführungsrecht ausschließlich für `authenticated`

## Rückgabe

- `attempt_question_id uuid`
- `selected_answers jsonb`
- `saved boolean`

## Sicherheitsgrenze

Keine Migration wurde live ausgeführt.

Es wurden keine echten Teilnehmerdaten und keine geheimen
Supabase-Schlüssel verwendet.
