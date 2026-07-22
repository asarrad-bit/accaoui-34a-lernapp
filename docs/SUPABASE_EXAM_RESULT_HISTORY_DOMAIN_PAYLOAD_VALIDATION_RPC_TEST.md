# Fach-Payload-Validierungs-RPC

Stand: v27.31m

Status: SQL-Helfer vorbereitet, nicht live ausgeführt

## Migration

`supabase/migrations/20260722_v2731m_exam_history_domain_payload_validate_rpc.sql`

## Funktion

`public.accaoui_validate_exam_history_domain_payload(...)`

## Eingaben

- Operationsbereich
- Operation
- Fach-Payload als JSONB oder `null`

Der Helfer akzeptiert keine:

- Nutzer- oder Teilnehmer-ID
- Operations-UUID
- Client-Wiederholungsschlüssel
- Operationsidentität
- Browser-Fingerprints

## Snapshot Write

Geprüft werden:

- JSONB-Objekt
- exakt `schema_version` und `snapshot`
- Schema-Version exakt 1
- nicht leeres Snapshot-Objekt
- höchstens 262144 kanonische UTF-8-Bytes

## Zyklusregister Write

Geprüft werden:

- JSONB-Objekt
- exakt `schema_version` und `registry`
- Schema-Version exakt 1
- Register als Objekt
- leeres Register zulässig
- höchstens 131072 kanonische UTF-8-Bytes

## Rekursive Prüfung

Der Helfer prüft:

- maximal 16 Verschachtelungsebenen
- gesperrte interne Schlüssel in allen Objekten und Arrays

## Delete

Delete verlangt exakt einen SQL-`null`-Payload.

Rückgabe:

- kanonischer Payload `null`
- Fingerprint `null`
- kanonische Byteanzahl 0

## Fingerprint

Bei Write wird der PostgreSQL-JSONB-Text verwendet.

Aus dessen UTF-8-Bytes wird serverseitig SHA-256 berechnet und
als 64-stelliges kleingeschriebenes Hex zurückgegeben.

## Mutationsfreiheit

Der Helfer:

- führt kein `INSERT` aus
- führt kein `UPDATE` aus
- führt kein `DELETE FROM` aus
- ruft keine Operations-ID-, Reservierungs- oder
  Abschlusshelfer auf

## Zugriffsschutz

- Security Definer
- fester `search_path`
- `row_security = off`
- vollständiger Revoke für `public`, `anon` und
  `authenticated`
- kein direktes `GRANT EXECUTE`
- keine Live-Ausführung
- keine echten Teilnehmerdaten
- keine UI-Änderung
