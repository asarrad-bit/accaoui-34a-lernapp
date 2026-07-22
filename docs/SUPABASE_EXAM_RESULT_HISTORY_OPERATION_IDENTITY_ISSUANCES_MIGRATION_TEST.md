# Operations-ID-Ausstellungstabelle

Stand: v27.31h

Status: SQL-Migration vorbereitet, nicht live ausgeführt

## Migration

`supabase/migrations/20260722_v2731h_exam_history_operation_identity_issuances.sql`

## Tabelle

`public.exam_history_operation_identity_issuances`

## Gespeicherte Identitätsdaten

- authentifizierter Nutzerbezug
- SHA-256-Hash des Client-Wiederholungsschlüssels
- kanonischer Anfragefingerprint
- serverseitig erzeugte UUID Version 4
- Operationsbereich
- Mutation
- Ressourcenidentität
- Write-Payload-Fingerprint
- Ausstellungszeit

Der rohe Client-Wiederholungsschlüssel wird nicht gespeichert.

## Eindeutigkeit

Die Kombination aus Nutzer und gehashtem
Client-Wiederholungsschlüssel ist eindeutig.

Dadurch kann ein späterer Ausstellungs-RPC denselben echten
Retry wiederfinden. Eine UUID kann ebenfalls nur einmal
ausgestellt werden.

## Zugriffsschutz

- Row Level Security aktiviert
- Row Level Security erzwungen
- alle Rechte für `public`, `anon` und `authenticated` entzogen
- keine Direktpolicy
- keine direkte App-Rollenfreigabe
- spätere Nutzung nur über einen geprüften Security-Definer-RPC

## Sicherheitsgrenze

- keine Live-Migration
- kein Ausstellungs-RPC
- kein Frontendzugriff
- keine echten Teilnehmerdaten
- keine UI-Änderung
