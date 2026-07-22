# Idempotenz-Abschluss-RPC

Stand: v27.31d

Status: SQL-RPC vorbereitet, nicht live ausgeführt

## Migration

`supabase/migrations/20260722_v2731d_exam_history_idempotency_complete_rpc.sql`

## Funktion

`public.accaoui_complete_exam_history_idempotency_operation(...)`

## Aufgabe

Der interne RPC schließt einen bereits reservierten
Idempotenzvorgang atomar als `completed` oder `failed` ab.

Er führt selbst keine Snapshot- oder Zyklusregistermutation
aus.

## Identität und Besitz

- Nutzer ausschließlich über `auth.uid()`
- keine Nutzer- oder Teilnehmer-ID als Parameter
- UUID Version 4 erforderlich
- Bereich, Mutation und kanonische Operationsidentität geprüft
- Ressourcenidentität erneut geprüft
- Write-Payload-Fingerprint erneut geprüft
- nur der reservierende Nutzer darf den Vorgang abschließen

## Erfolgreicher Abschluss

`completed` verlangt:

- JSONB-Objekt als Ergebnis
- höchstens 32768 Byte
- keinen Fehlercode

Der Vorgang wechselt atomar von `pending` zu `completed`.

## Fehlgeschlagener Abschluss

`failed` verlangt:

- keinen Ergebnis-Payload
- stabilen kleingeschriebenen Fehlercode
- ausschließlich Buchstaben, Zahlen und Unterstriche
- höchstens 128 Zeichen

Der Vorgang wechselt atomar von `pending` zu `failed`.

## Wiederholungen

Ein identischer bereits terminaler Abschluss wird unverändert
zurückgegeben:

- `already_completed`
- `already_failed`

`updated_at`, `completed_at`, Ergebnis und Fehlercode werden
nicht erneut verändert.

## Konflikte

Ein bereits terminaler Vorgang wird niemals überschrieben.

Abweichende zweite Abschlüsse werden geschlossen mit
`idempotency_operation_terminal_conflict` blockiert.

## Interne Sicherheitsgrenze

- Security Definer mit festem `search_path`
- `row_security = off`
- Zeilensperre über `FOR UPDATE`
- vollständiger Revoke für `public`, `anon` und `authenticated`
- keine direkte Ausführungsfreigabe
- keine Live-Ausführung
- keine echten Teilnehmerdaten
- keine UI-Änderung
