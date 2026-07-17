# Supabase Prüfungsergebnis-RPC – statischer Sicherheitstest

Stand: v27.27f

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260717_v2727f_exam_result_rpc.sql`

## Funktion

`public.accaoui_get_full_exam_result(p_exam_attempt_id uuid)`

## Zweck

Sicherer Abruf der Ergebniszusammenfassung eines eigenen,
abgeschlossenen schriftlichen Vollsimulationsversuchs.

Historische Ergebnisse bleiben auch nach dem Ende eines Kurses
für berechtigte Teilnehmer abrufbar.

## Bestätigte Sicherheitsregeln

- Teilnehmeridentität ausschließlich über `auth.uid()`
- nur der eigene Prüfungsversuch darf abgerufen werden
- nur schriftliche Vollsimulationen sind erlaubt
- nur abgeschlossene Prüfungsversuche sind erlaubt
- Teilnehmerstatus `active`, `expired` oder `completed`
- Teilnehmerstatus `blocked` ist ausgeschlossen
- exakt 82 sichtbare Fragen-Snapshots erforderlich
- Gesamtpunktzahl muss exakt 120 betragen
- exakt 82 gespeicherte Antwortzeilen erforderlich
- gespeicherte Antwortpunkte müssen mit dem Prüfungsversuch übereinstimmen
- Bestehensstatus muss `score_points >= 60` entsprechen
- beantwortete und unbeantwortete Fragen ergeben zusammen 82
- richtige, teilweise richtige, falsche und unbeantwortete Fragen ergeben zusammen 82
- keine Lösungsschlüssel in der Rückgabe
- keine Erklärungen in der Rückgabe
- keine richtigen Antwortindizes in der Rückgabe
- keine privaten Versuchsschlüssel-Tabellen werden vom RPC gelesen
- keine Schreiboperationen
- Ausführungsrecht ausschließlich für `authenticated`

## Rückgabe

- `exam_attempt_id uuid`
- `course_id uuid`
- `course_title text`
- `score_points integer`
- `max_points integer`
- `passed boolean`
- `started_at timestamptz`
- `finished_at timestamptz`
- `total_questions integer`
- `answered_questions integer`
- `correct_questions integer`
- `partial_questions integer`
- `wrong_questions integer`
- `unanswered_questions integer`

## Sicherheitsgrenze

Keine Migration wurde live ausgeführt.

Es wurden keine echten Teilnehmerdaten, keine geheimen
Supabase-Schlüssel und keine Service-Role verwendet.
