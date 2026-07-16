# Supabase Prüfungsabschluss-RPC – statischer Sicherheitstest

Stand: v27.27d

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260716_v2727d_exam_finish_rpc.sql`

## Funktion

`public.accaoui_finish_full_exam(p_exam_attempt_id uuid)`

## Bestätigte Sicherheitsregeln

- Teilnehmeridentität ausschließlich über `auth.uid()`
- nur der eigene Prüfungsversuch darf abgeschlossen werden
- nur schriftliche Vollsimulationen sind erlaubt
- Prüfungsversuch wird gegen parallele Abschlüsse gesperrt
- bereits abgeschlossene Versuche liefern dasselbe Ergebnis
- aktiver Teilnehmer- und Kurszugang wird geprüft
- exakt 82 sichtbare Fragen-Snapshots erforderlich
- exakt 82 private Lösungsschlüssel-Snapshots erforderlich
- Gesamtpunktzahl muss exakt 120 betragen
- unbeantwortete Fragen werden mit `[]` und null Punkten ergänzt
- Bewertung erfolgt ausschließlich gegen private Versuchsschlüssel
- vollständige exakte Antwort erhält die vollen Fragepunkte
- teilrichtige Auswahlen erhalten Punkte je richtigem Kreuz
- falsche Auswahlen erzeugen keinen Punktabzug
- Teilpunkte werden durch die Fragepunktzahl gedeckelt
- alle 82 Antwortzeilen werden serverseitig bewertet
- bestanden ab 60 von 120 Punkten
- Bewertung und Abschluss erfolgen atomar
- der Browser liefert keine Punkte oder Ergebniswerte
- Ausführungsrecht ausschließlich für `authenticated`
- keine Lösungsschlüssel in der Rückgabe

## Rückgabe

- `exam_attempt_id uuid`
- `answered_questions integer`
- `correct_questions integer`
- `score_points integer`
- `max_points integer`
- `passed boolean`
- `finished_at timestamptz`
- `already_finished boolean`

## Sicherheitsgrenze

Keine Migration wurde live ausgeführt.

Es wurden keine echten Teilnehmerdaten und keine geheimen
Supabase-Schlüssel verwendet.
