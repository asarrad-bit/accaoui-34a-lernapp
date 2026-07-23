# Äußerer Fachmutations-RPC-Schnittstellenvertrag

Stand: v27.31t
Status: verbindlicher lokaler Vertrag, nicht live ausgeführt

## Ziel

Der spätere äußere Security-Definer-RPC ist der einzige
zulässige Einstiegspunkt für eine produktive
Prüfungshistorien-Fachmutation.

Interne Operations-ID-, Reservierungs- und Abschlusshelfer
dürfen nicht direkt vom Browser aufgerufen werden.

## Erlaubte Browserparameter

Der äußere RPC akzeptiert ausschließlich:

1. `p_client_request_key`
2. `p_operation_scope`
3. `p_operation`
4. `p_resource_identity`
5. `p_expected_storage_version`
6. `p_domain_payload`

## Verbotene Browserparameter

Nicht akzeptiert werden insbesondere:

- externe Operations-UUID
- kanonische Operationsidentität
- Payload-Fingerprint
- Hash des Client-Wiederholungsschlüssels
- Anfragefingerprint
- Nutzer-ID
- Teilnehmer-ID
- Ergebnis-Payload
- Fehlercode
- interner Status

## Serverseitige Ableitungen

Der äußere RPC muss selbst:

- den Nutzer ausschließlich über `auth.uid()` bestimmen
- den Fach-Payload kanonisieren
- bei Write den SHA-256-Payload-Fingerprint berechnen
- bei Delete einen `null`-Fingerprint verwenden
- die Operations-UUID intern ausstellen oder wiederverwenden
- die kanonische Operationsidentität intern reservieren

Der Browser darf keine dieser abgeleiteten Identitäten
vorgeben.

## Payload-Regeln

### Write

- `p_domain_payload` muss ein JSONB-Objekt sein
- der Payload muss zum späteren bereichsspezifischen Schema passen
- der Fingerprint wird ausschließlich serverseitig berechnet

### Delete

- `p_domain_payload` muss `null` sein
- der Payload-Fingerprint muss intern `null` sein

Die kanonischen Payload-Hüllen für Snapshot und
Zyklusregister sind seit v27.31l verbindlich festgelegt.

## Verbindliche interne Reihenfolge

1. authentifizieren und autorisieren
2. Eingaben validieren
3. Fach-Payload kanonisieren
4. Payload-Fingerprint ableiten
5. Operations-ID intern ausstellen oder wiederverwenden
6. Idempotenzoperation reservieren
7. Reservierungsstatus geschlossen auswerten
8. ausschließlich bei `reserved_new` fachlich mutieren
9. Operation terminal abschließen
10. kanonische Clientantwort zurückgeben

## Reservierungsstatus

### `reserved_new`

- Fachmutation erlaubt
- terminaler Abschluss erforderlich

### `reserved_existing_pending`

- keine erneute Fachmutation
- kontrollierter In-Progress-Zustand

### `reserved_existing_completed`

- keine erneute Fachmutation
- gespeichertes Ergebnis wiederverwenden

### `reserved_existing_failed`

- keine erneute Fachmutation
- gespeicherten stabilen Fehler wiederverwenden

## Clientantwort

Erlaubt:

- fachliches Ergebnis
- sicherer Operationsstatus
- stabiler Fehlercode
- Retry-Hinweis

Nicht erlaubt:

- Operations-UUID
- Operationsidentität
- interne Hashes oder Fingerprints
- Nutzer- oder Teilnehmer-ID
- rohe Datenbankfehler

## Noch nicht umgesetzt

- äußerer Fachmutations-RPC
- Live-Datenbanktests
- Parallelitäts-, Autorisierungs- und Konkurrenztests

Deshalb bleibt die produktive Freigabe gesperrt.

## Sicherheitsgrenze

- kein SQL-RPC in v27.31k
- keine direkte Helper-Ausführungsfreigabe
- keine direkte Tabellenfreigabe
- keine echten Teilnehmerdaten
- keine Live-Ausführung
- keine UI-Änderung

## Automatische Prüfung

`tools/check-supabase-exam-history-outer-domain-mutation-rpc-interface-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.


## Kanonische Fach-Payloads v27.31l

### Snapshot Write

Exakte Hüllenfelder:

- `schema_version`
- `snapshot`

`schema_version` ist exakt `1`.

`snapshot` muss ein nicht leeres JSONB-Objekt sein.

Die vollständige kanonische Payload darf höchstens
262144 UTF-8-Bytes besitzen.

### Zyklusregister Write

Exakte Hüllenfelder:

- `schema_version`
- `registry`

`schema_version` ist exakt `1`.

`registry` muss ein JSONB-Objekt sein. Ein leeres Register ist
zulässig.

Die vollständige kanonische Payload darf höchstens
131072 UTF-8-Bytes besitzen.

### Delete

Für Snapshot und Zyklusregister muss der Fach-Payload bei
Delete exakt `null` sein.

### Kanonisierung und Fingerprint

Die Datenbank muss den normalisierten JSONB-Text verwenden und
daraus serverseitig einen SHA-256-Fingerprint als
64-stelligen kleingeschriebenen Hex-Wert bilden.

Zusätzliche Hüllenfelder sowie interne Operations-, Hash- und
Fingerprintfelder sind unzulässig.

Maschinenlesbarer Vertrag:

`docs/contracts/exam-history-domain-payload-contract.json`


## Interner Payload-Helfer v27.31m

Die kanonische Payload-Prüfung und
SHA-256-Fingerprint-Ableitung ist als vollständig gesperrter
interner SQL-Helfer vorbereitet.

Der spätere äußere Fachmutations-RPC muss diesen Helfer
verwenden und darf keinen Browser-Fingerprint übernehmen.

Der Helfer führt selbst keine Fach- oder Idempotenzmutation
aus.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_DOMAIN_PAYLOAD_VALIDATION_RPC_TEST.md`


## Domain-Speichergrenze v27.31n

Write und Delete müssen zusätzlich den erwarteten
`storage_version`-Stand übermitteln.

- Version 0 bedeutet ausschließlich Neuanlage
- positive Version bedeutet exakter aktueller Stand
- Abweichungen werden geschlossen als Versionskonflikt
  abgelehnt
- Delete erzeugt einen monotonen Tombstone
- stilles Last-Write-Wins ist verboten

Der Versionsstand muss vor der Umsetzung des äußeren RPCs noch
in Operations-ID-Ausstellung und Idempotenzreservierung
eingebunden werden.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_DOMAIN_STORAGE_CONTRACT.md`


## Versionsstand-Identitätsbindung v27.31o

Der vom Browser übermittelte erwartete Speicher-Versionsstand
muss intern unverändert an Operations-ID-Ausstellung und
Idempotenzreservierung weitergegeben werden.

Er wird in beiden Grenzen Teil der kanonischen
Anfrageidentität.

Die beiden internen Tabellen sind seit v27.31p im
vorbereiteten Schema erweitert.

Der Ausstellungshelper bindet den Versionsstand seit v27.31q.

Ausstellungs- und Reservierungshelper binden seit v27.31r
denselben erwarteten Versionsstand verbindlich.

Eine Implementierung des äußeren RPCs bleibt dennoch gesperrt,
bis Domain-Speichertabelle und Fachmutationsweg vorbereitet
sind.


## Domain-Speichertabelle v27.31s

Die vollständig gesperrte Domain-Speichertabelle ist jetzt als
Schema-Migration vorbereitet.

Der äußere Fachmutations-RPC bleibt gesperrt, bis ein interner
Speicher-Mutationshelper den Payload-Validierungshelfer, exakten
Versionsvergleich, Row Lock, monotone Versionserhöhung und
Tombstone-Übergang atomar verbindet.


## Interner Domain-Mutationshelper v27.31t

Die innere Domain-Speichermutation ist jetzt vorbereitet.

Der spätere äußere Fachmutations-RPC muss denselben erwarteten
Versionsstand an Operations-ID-Ausstellung,
Idempotenzreservierung und Domain-Mutationshelper weitergeben
und alle Schritte in einer Datenbanktransaktion verbinden.

Direkte Browserausführung des internen Helpers bleibt verboten.
