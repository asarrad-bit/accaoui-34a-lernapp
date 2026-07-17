# Supabase Prüfungsdaten-Schreibsperre – statischer Test

Stand: v27.28d

Status: vorbereitet und statisch geprüft, nicht live ausgeführt

## Migration

`20260717_v2728d_exam_direct_write_lockdown.sql`

## Ziel

Autoritative Prüfungsdaten dürfen von keiner App-Rolle direkt
in den Tabellen verändert werden.

Schreibvorgänge erfolgen ausschließlich über die geprüften
Security-Definer-RPC-Funktionen.

## Entfernte Policies

- `exam_attempts_staff_manage`
- `exam_answers_staff_manage`

Die alten `FOR ALL`-Policies waren zu weit gefasst.

Sie hätten auch Rollen, die nur Mitarbeiter-Lesezugriff benötigen,
direkte Änderungen an Prüfungsversuchen und Antworten ermöglicht.

## Entzogene Tabellenrechte

Für `public`, `anon` und `authenticated` wurden entzogen:

- `INSERT`
- `UPDATE`
- `DELETE`

Betroffene Tabellen:

- `exam_attempts`
- `exam_answers`

## Weiterhin erlaubt

- Teilnehmer lesen eigene Prüfungsdaten
- berechtigte Mitarbeiter lesen erforderliche Prüfungsdaten
- Prüfungsstart über `accaoui_start_full_exam(...)`
- Antwortspeicherung über `accaoui_save_exam_answer(...)`
- Abschluss über `accaoui_finish_full_exam(...)`
- Ergebnisabruf über `accaoui_get_full_exam_result(...)`

## Sicherheitswirkung

- Teilnehmer können keine autoritativen Prüfungswerte direkt setzen
- Support kann keine Prüfungsergebnisse direkt verändern
- Admin und Dozent umgehen den sicheren RPC-Weg nicht
- Punkte und Bestehensstatus bleiben serverseitig kontrolliert
- Antworten bleiben ausschließlich RPC-gebunden
- spätere administrative Korrekturen benötigen einen eigenen
  geprüften und protokollierten Admin-RPC

## Sicherheitsgrenze

- keine Live-Supabase-Ausführung
- keine echten Teilnehmerdaten
- keine echten Schlüssel
- keine Service-Role
- keine Änderung an App-Code oder Fragenbeständen
