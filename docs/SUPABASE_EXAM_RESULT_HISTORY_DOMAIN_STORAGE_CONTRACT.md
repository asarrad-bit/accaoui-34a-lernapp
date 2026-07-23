# Domain-Speichervertrag

Stand: v27.31s
Status: verbindlicher lokaler Vertrag, nicht live ausgeführt

## Ziel

Snapshot und Zyklusregister erhalten eine gemeinsame sichere
Speichergrenze mit Nutzerbindung, monotonem Versionsstand und
geschlossenem Konkurrenzschutz.

## Logische Zeilenidentität

Eine aktuelle Speicherzeile wird eindeutig bestimmt durch:

- authentifizierten Nutzer
- Operationsbereich
- Ressourcenidentität

Der Nutzer wird ausschließlich über `auth.uid()` bestimmt.

## Vorgeschlagenes Speichermodell

Vorgesehene Tabelle:

`public.exam_history_domain_resources`

Die Tabelle wird seit v27.31s als vollständig gesperrte Schema-Migration vorbereitet.

## Speicher-Versionsstand

Jede Ressource besitzt einen monotonen `storage_version`.

Regeln:

- neue Ressource: erwartete Version 0
- erste gespeicherte Version: 1
- Änderung: exakter aktueller Versionsstand erforderlich
- erfolgreiche Änderung: Version plus 1
- Delete: exakter aktueller Versionsstand erforderlich
- erfolgreiche Löschung: Tombstone und Version plus 1
- Versionsstände werden nach Delete nicht wiederverwendet

## Write-Semantik

Der spätere Mutationsweg muss:

1. die Ressource sperren
2. den aktuellen Versionsstand lesen
3. den erwarteten Versionsstand vergleichen
4. den Payload über den Validierungshelfer prüfen
5. nur bei exaktem Treffer schreiben
6. die Version atomar erhöhen

Stilles Last-Write-Wins ist verboten.

## Identischer Payload

Ein Write mit identischem kanonischem Fingerprint erzeugt
keine unnötige neue Speicher-Version.

## Delete-Semantik

Delete speichert einen Tombstone:

- `is_deleted = true`
- Payload `null`
- Payload-Fingerprint `null`
- kanonische Byteanzahl `null`
- Speicher-Version erhöht

Physisches Löschen im normalen Mutationsweg ist verboten.

## Konkurrenzschutz

Erforderlich sind:

- `SELECT ... FOR UPDATE`
- Versionsvergleich innerhalb der Sperre
- erneute Auswertung nach konkurrierendem Unique-Konflikt
- Ablehnung veralteter Writes
- Ablehnung veralteter Deletes
- gemeinsame Transaktion mit Idempotenzabschluss

## Versionsbindung

Der erwartete Speicher-Versionsstand beeinflusst die Bedeutung
eines Vorgangs.

Seit v27.31r binden deshalb beide internen Identitätshelper
denselben Stand:

- Operations-ID-Ausstellung
- Idempotenzreservierung

Die End-to-End-Weitergabe durch den äußeren Fachmutations-RPC
bleibt weiterhin offen.

## Direkter Zugriff

Die spätere Tabelle muss:

- RLS aktivieren und erzwingen
- ohne direkte Policy bleiben
- alle Rechte für `public`, `anon` und `authenticated`
  entziehen
- ausschließlich durch interne Security-Definer-RPCs
  erreichbar sein

## Noch offen

- interner Speicher-Mutationshelfer
- äußerer Fachmutations-RPC
- Live-, Parallelitäts- und Autorisierungstests

## Sicherheitsgrenze

- gesperrte SQL-Schema-Migration, nicht live ausgeführt
- Speichertabelle ohne direkten App-Zugriff
- kein Speicher-Mutationshelfer
- keine Fachmutation
- kein äußerer Fachmutations-RPC
- keine UI-Änderung

## Automatische Prüfung

`tools/check-supabase-exam-history-domain-storage-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.


## Identitätsbindungsvertrag v27.31o

Die notwendige Bindung des erwarteten Speicher-Versionsstands
ist jetzt verbindlich festgelegt.

Der Versionsstand muss:

- im Anfragefingerprint der Operations-ID-Ausstellung liegen
- in der Idempotenzreservierung gespeichert werden
- Teil der vollständigen Operationsidentität sein
- bei vorhandenen Reservierungen exakt verglichen werden
- beim Abschluss aus der Reservierung gelesen werden

Die gesperrte Spaltenmigration ist seit v27.31p
vorbereitet. Ausstellungs- und Reservierungshelper binden den
Versionsstand seit v27.31r.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_EXPECTED_STORAGE_VERSION_IDENTITY_BINDING_CONTRACT.md`


## Gesperrte Versionsspalten-Migration v27.31p

Operations-ID-Ausstellungen und Idempotenzoperationen besitzen
im vorbereiteten Schema jetzt jeweils eine nicht nullable
`expected_storage_version`-Spalte ohne Default.

Vorhandene Zeilen führen zum kontrollierten
Migrationsabbruch. Ein unbekannter Versionsstand wird nicht
erfunden.

Die Domain-Speichertabelle wird seit v27.31s als
vollständig gesperrte Schema-Migration vorbereitet.


## Teilweise Identitätsbindung v27.31q

Der erwartete Speicher-Versionsstand wird jetzt durch den
Operations-ID-Ausstellungshelper gebunden.

Noch offen bleibt seine verbindliche Einbindung in den
Idempotenz-Reservierungshelper. Bis dahin bleiben die gesamte
Identitätsbindung und der äußere Fachmutations-RPC gesperrt.


## Vollständige innere Versionsbindung v27.31r

Der erwartete Speicher-Versionsstand wird jetzt durch beide
internen Identitätshelper gebunden:

- Operations-ID-Ausstellung
- Idempotenzreservierung

Ausstellung und Reservierung speichern und vergleichen
denselben Versionsstand.

Die Domain-Speichertabelle und der äußere Fachmutations-RPC
sind weiterhin nicht implementiert. Die End-to-End-Bindung
bleibt deshalb produktiv gesperrt.


## Gesperrte Domain-Speichertabelle v27.31s

Die vorbereitete Tabelle
`public.exam_history_domain_resources` speichert Snapshot und
Zyklusregister über dieselbe Sicherheitsgrenze.

Eindeutige Zeilenidentität:

- `auth_user_id`
- `operation_scope`
- `resource_identity`

Der gespeicherte Zustand enthält:

- Schema-Version 1
- kanonischen Fach-Payload
- serverseitigen SHA-256-Fingerprint
- kanonische Byteanzahl
- monotonen `storage_version`-Stand ab 1
- Live- oder Tombstone-Zustand
- Erstellungs- und Änderungszeit

Live-Zeilen erzwingen Payload, Fingerprint und das jeweilige
Bereichsgrößenlimit. Tombstones erzwingen `null` für Payload,
Fingerprint und Byteanzahl.

RLS ist aktiviert und erzwungen. Es existiert keine direkte
Policy und alle Tabellenrechte für `public`, `anon` und
`authenticated` sind entzogen.

Migration:

`supabase/migrations/20260723_v2731s_exam_history_domain_resources.sql`
