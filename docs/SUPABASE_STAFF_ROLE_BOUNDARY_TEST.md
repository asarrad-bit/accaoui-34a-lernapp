# Supabase Mitarbeiter-Rollentrennung – statischer Test

Stand: v27.28e

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260717_v2728e_staff_role_boundary.sql`

## Ziel

Lese- und Verwaltungsrechte werden eindeutig getrennt.

## Aktive Mitarbeiter

Der Helper `accaoui_is_active_staff()` umfasst:

- Admin
- Dozent
- Support

Dieser Helper wird ausschließlich für notwendige
Mitarbeiter-Lesezugriffe verwendet.

## Verwaltungsrollen

Der Helper `accaoui_is_admin_or_dozent()` umfasst nur:

- Admin
- Dozent

Support ist ausdrücklich ausgeschlossen.

## Neu gesetzte Select-Policies

- `participants_select_own_or_staff`
- `courses_select_authenticated`
- `enrollments_select_own_or_staff`
- `exam_attempts_select_own_or_staff`
- `exam_answers_select_own_or_staff`
- `certificates_select_own_or_staff`

Die eigenen Teilnehmerzugriffe bleiben erhalten.

## Sicherheitswirkung

- Support kann erforderliche Daten lesen
- Support kann Teilnehmer, Kurse und Einschreibungen nicht verwalten
- Support kann Zertifikate nicht verwalten
- Support kann Prüfungsinhalte nicht verwalten
- Support kann Prüfungsversuche oder Antworten nicht schreiben
- Verwaltungsrechte bleiben auf aktive Admins und Dozenten begrenzt
- direkte Prüfungs-Schreibrechte bleiben vollständig gesperrt

## Funktionssicherheit

Für beide Rollen-Helper gilt:

- `SECURITY DEFINER`
- fester `search_path`
- `row_security = off`
- keine Ausführung für `public` oder `anon`
- Ausführung ausschließlich für `authenticated`

## Sicherheitsgrenze

- keine Live-Supabase-Ausführung
- keine echten Teilnehmerdaten
- keine echten Schlüssel
- keine Service-Role
- keine Änderung an App-Code oder Fragenbeständen
