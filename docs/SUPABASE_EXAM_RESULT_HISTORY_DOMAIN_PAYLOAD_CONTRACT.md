# Kanonischer Fach-Payload-Vertrag

Stand: v27.31u
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

## SQL-Helfer v27.31m

Ein interner Security-Definer-Helfer ist als SQL-Migration
vorbereitet.

Er:

- validiert Bereich und Operation
- erzwingt die exakten Snapshot- und Registerhüllen
- prüft Schema-Version und Inhaltsobjekt
- prüft maximal 16 Verschachtelungsebenen
- blockiert rekursiv interne Schlüssel
- prüft die kanonische UTF-8-Byteanzahl
- bildet den SHA-256-Fingerprint serverseitig
- akzeptiert Delete ausschließlich mit `null`
- führt keine Tabellenmutation aus
- besitzt keine direkte App-Ausführungsfreigabe

## Noch offen

- Live-Datenbanktests
- Parallelitäts-, Autorisierungs- und Konkurrenztests
- direkte App-Freigabe und UI-Anbindung

## Sicherheitsgrenze

- SQL-Helfer vorbereitet, aber nicht live ausgeführt
- keine Live-Ausführung
- keine echten Teilnehmerdaten
- keine direkte Helper-Freigabe
- keine UI-Änderung

## Automatische Prüfung

`tools/check-supabase-exam-history-domain-payload-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.


## Äußere Payload-Integration v27.31u

Der vollständig gesperrte äußere Fachmutations-RPC ruft den
kanonischen Fach-Payload-Validierungshelper vor
Operations-ID-Ausstellung und Idempotenzreservierung auf.

Nur der serverseitig kanonisierte Payload und dessen interner
Fingerprint werden an die nachfolgenden Helper weitergegeben.
Der Fingerprint bleibt aus der Clientantwort ausgeschlossen.

Die Integration ist statisch vorbereitet, aber weiterhin nicht
live ausgeführt.
