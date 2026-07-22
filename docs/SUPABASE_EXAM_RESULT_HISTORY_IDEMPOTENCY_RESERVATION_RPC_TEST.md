# Idempotenz-Reservierungs-RPC

Stand: v27.31c

Status: SQL-RPC vorbereitet, nicht live ausgeführt

## Migration

`supabase/migrations/20260722_v2731c_exam_history_idempotency_reserve_rpc.sql`

## Funktion

`public.accaoui_reserve_exam_history_idempotency_operation(...)`

## Aufgabe

Der interne RPC reserviert einen Idempotenzvorgang atomar,
ohne die eigentliche Snapshot- oder Zyklusregistermutation
auszuführen.

## Identität

- Nutzer ausschließlich über `auth.uid()`
- keine Nutzer- oder Teilnehmer-ID als Parameter
- externe Operations-ID muss eine UUID Version 4 sein
- kanonische Operationsidentität aus Bereich, Mutation und UUID
- Bereich nur `snapshot` oder `cycle_registry`
- Mutation nur `write` oder `delete`

## Neue Operation

Eine neue Operation wird als `pending` eingefügt.

Rückgabe:

- `reserved_new`
- `operation_status = pending`
- `is_new = true`

`ON CONFLICT DO NOTHING` nutzt die eindeutigen
Datenbankbedingungen als atomare Reservierungsgrenze.

## Identische Wiederholung

Eine vorhandene Operation wird mit `FOR UPDATE` gesperrt und
vollständig gegengeprüft.

Erlaubte Rückgabestatus:

- `reserved_existing_pending`
- `reserved_existing_completed`
- `reserved_existing_failed`

Ein bereits gespeichertes Ergebnis oder ein stabiler
Fehlercode darf bei identischer Wiederholung erneut
zurückgegeben werden.

## Geschlossene Konflikte

Dieselbe Operationsidentität wird abgelehnt, wenn abweichen:

- authentifizierter Nutzer
- Bereich oder Mutation
- Ressourcenidentität
- Payload-Fingerprint

Es werden keine vorhandenen Fremdwerte in Fehlermeldungen
offengelegt.

## Interne Sicherheitsgrenze

- Security Definer mit festem `search_path`
- `row_security = off`
- `public`, `anon` und `authenticated` vollständig entzogen
- bewusst kein `GRANT EXECUTE`
- spätere Nutzung nur innerhalb eines geprüften
  Mutations-RPCs und derselben Datenbanktransaktion
- keine direkte Tabellenfreigabe
- keine Live-Ausführung
- keine echten Teilnehmerdaten
- keine UI-Änderung
