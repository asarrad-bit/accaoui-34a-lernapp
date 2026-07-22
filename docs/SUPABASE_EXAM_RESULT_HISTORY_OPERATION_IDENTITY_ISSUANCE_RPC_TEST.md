# Operations-ID-Ausstellungs-RPC

Stand: v27.31i

Status: SQL-RPC vorbereitet, nicht live ausgeführt

## Migration

`supabase/migrations/20260722_v2731i_exam_history_operation_identity_issue_rpc.sql`

## Funktion

`public.accaoui_issue_exam_history_operation_identity(...)`

## Eingaben

- `client_request_key`
- Operationsbereich
- Mutation
- Ressourcenidentität
- Write-Payload-Fingerprint oder `null` bei Delete

Der Client-Wiederholungsschlüssel muss aus exakt 64
kleingeschriebenen Hex-Zeichen bestehen. Er stellt damit einen
256-Bit-Wert dar.

## Serverseitige Ableitungen

Der RPC bildet innerhalb der Datenbank:

1. SHA-256-Hash des Client-Wiederholungsschlüssels
2. SHA-256-Fingerabdruck einer kanonischen JSONB-Anfrage

Die kanonische Anfrage enthält:

- Client-Wiederholungsschlüssel
- Bereich
- Mutation
- Ressource
- Payload-Fingerprint

Der rohe Client-Wiederholungsschlüssel wird nicht gespeichert.

## Neue Ausstellung

Bei einer neuen Kombination aus Nutzer und gehashtem
Wiederholungsschlüssel wird ein Datensatz eingefügt.

Die UUID wird über den Datenbank-Default `gen_random_uuid()`
erzeugt und erst nach erfolgreicher Speicherung zurückgegeben.

Rückgabe:

- `issued_new`
- `is_new = true`

## Identische Wiederholung

Bei einem vorhandenen Datensatz wird die Zeile mit
`FOR UPDATE` gesperrt.

Stimmen Anfragefingerprint, Bereich, Mutation, Ressource und
Payload-Fingerprint vollständig überein, wird dieselbe
gespeicherte UUID zurückgegeben.

Rückgabe:

- `issued_existing`
- `is_new = false`

## Konflikt

Derselbe Client-Wiederholungsschlüssel mit einer abweichenden
Anfrage wird geschlossen mit

`operation_identity_request_key_conflict`

abgelehnt.

Vorhandene Werte werden nicht offengelegt oder überschrieben.

## Sicherheitsgrenze

- Nutzer ausschließlich über `auth.uid()`
- Security Definer mit festem `search_path`
- `row_security = off`
- keine Nutzer- oder Teilnehmer-ID als Parameter
- keine externe Operations-ID als Parameter
- vollständiger Revoke für `public`, `anon` und `authenticated`
- keine direkte Ausführungsfreigabe
- keine Fachmutation
- keine Live-Ausführung
- keine echten Teilnehmerdaten
- keine UI-Änderung
