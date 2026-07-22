# Kanonischer Fach-Payload-Vertrag

Stand: v27.31l

Status: verbindlicher lokaler Vertrag, nicht live ausgeführt

## Ziel

Snapshot- und Zyklusregister-Mutationen erhalten getrennte,
eindeutige und größenbegrenzte JSONB-Payload-Verträge.

Der Browser darf keinen Payload-Fingerprint vorgeben. Der
Fingerprint wird ausschließlich innerhalb der Datenbank aus
dem kanonischen Payload abgeleitet.

## Gemeinsame Regeln

### Write

- Payload ist erforderlich
- Payload muss ein JSONB-Objekt sein
- ausschließlich exakt erlaubte Hüllenfelder
- maximal 16 Verschachtelungsebenen
- keine internen Operations-, Hash- oder Fehlerfelder
- Fingerprint ausschließlich serverseitig

### Delete

- Payload muss exakt `null` sein
- Payload-Fingerprint muss intern `null` sein

## Snapshot Write

Beispiel:

~~~json
{
  "schema_version": 1,
  "snapshot": {}
}
~~~

Regeln:

- exakt zwei Hüllenfelder
- `schema_version` exakt `1`
- `snapshot` ist ein nicht leeres JSONB-Objekt
- höchstens 262144 kanonische UTF-8-Bytes
- keine zusätzlichen Hüllenfelder

## Zyklusregister Write

Beispiel:

~~~json
{
  "schema_version": 1,
  "registry": {}
}
~~~

Regeln:

- exakt zwei Hüllenfelder
- `schema_version` exakt `1`
- `registry` ist ein JSONB-Objekt
- leeres Register zulässig
- höchstens 131072 kanonische UTF-8-Bytes
- keine zusätzlichen Hüllenfelder

## Kanonisierung

Die spätere Datenbankimplementierung muss:

1. den Payload als JSONB prüfen
2. den normalisierten PostgreSQL-JSONB-Text erzeugen
3. dessen UTF-8-Byteanzahl prüfen
4. aus diesem Text SHA-256 berechnen
5. den Fingerprint als 64-stelliges Lowercase-Hex verwenden

Identische semantische JSONB-Objekte ergeben damit denselben
Fingerprint, unabhängig von der ursprünglichen
Browserformatierung oder Feldreihenfolge.

## Gesperrte rekursive Schlüssel

Innerhalb der Fach-Payloads sind gesperrt:

- `external_operation_id`
- `operation_identity`
- `payload_fingerprint`
- `client_request_key_hash`
- `request_fingerprint`
- `service_role`
- `raw_database_error`

## Stabile Fehler

Snapshot- und Zyklusregister-Fehler besitzen getrennte stabile,
kleingeschriebene Fehlercodes.

Rohe PostgreSQL-, Exception- oder Stack-Informationen dürfen
nicht gespeichert oder an den Browser zurückgegeben werden.

## Noch offen

- äußerer Fachmutations-RPC
- produktive Domain-Speicherung
- Live-Datenbanktests
- Parallelitäts-, Autorisierungs- und Konkurrenztests

## Sicherheitsgrenze

- keine SQL-Migration in v27.31l
- keine Live-Ausführung
- keine echten Teilnehmerdaten
- keine direkte Helper-Freigabe
- keine UI-Änderung

## Automatische Prüfung

`tools/check-supabase-exam-history-domain-payload-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.
