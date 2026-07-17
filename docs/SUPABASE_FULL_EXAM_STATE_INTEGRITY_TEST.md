# Supabase Vollsimulation-Zustandsintegrität – statischer Test

Stand: v27.28c

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260717_v2728c_full_exam_state_integrity.sql`

## Ziel

Schriftliche Vollsimulationen dürfen nur einen konsistenten
offenen oder abgeschlossenen Zustand besitzen.

## Offener Vollsimulationsversuch

Erforderlich sind:

- `mode = full_simulation`
- `max_points = 120`
- `started_at` ist gesetzt
- `finished_at` ist null
- `score_points = 0`
- `passed = false`

Antworten dürfen währenddessen gespeichert werden.

Der autoritative Gesamtpunktestand wird erst beim
serverseitigen Prüfungsabschluss gesetzt.

## Abgeschlossener Vollsimulationsversuch

Erforderlich sind:

- `max_points = 120`
- `started_at` ist gesetzt
- `finished_at` ist gesetzt
- `passed` entspricht exakt `score_points >= 60`

Zusätzlich gelten weiterhin:

- `score_points <= max_points`
- `finished_at >= started_at`

## Migrationsverhalten

- bestehende ungültige Vollsimulationen brechen die Migration ab
- keine automatische Korrektur bestehender Daten
- keine Löschung bestehender Daten
- keine neue RLS-Policy
- keine direkten Tabellenrechte
- keine Service-Role
- keine Live-Ausführung

## Sicherheitsgrenze

Es wurden keine echten Teilnehmerdaten und keine geheimen
Supabase-Schlüssel verwendet.
