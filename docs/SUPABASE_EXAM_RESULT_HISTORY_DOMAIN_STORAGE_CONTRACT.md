# Domain-Speichervertrag

Stand: v27.31r
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

Eine Implementierung wurde in v27.31n noch nicht erstellt.

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

## Wichtige offene Identitätsbindung

Der erwartete Speicher-Versionsstand beeinflusst die Bedeutung
eines Vorgangs.

Er muss deshalb später in die Operations-ID-Ausstellung und
Idempotenzreservierung eingebunden werden.

Die vorhandenen Helper binden diesen Wert noch nicht. Deshalb
darf der äußere Fachmutations-RPC noch nicht implementiert oder
produktiv freigegeben werden.

## Direkter Zugriff

Die spätere Tabelle muss:

- RLS aktivieren und erzwingen
- ohne direkte Policy bleiben
- alle Rechte für `public`, `anon` und `authenticated`
  entziehen
- ausschließlich durch interne Security-Definer-RPCs
  erreichbar sein

## Noch offen

- Versionsbindung in Operations-ID und Idempotenz
- Speichertabellen-Migration
- interner Speicher-Mutationshelfer
- äußerer Fachmutations-RPC
- Live-, Parallelitäts- und Autorisierungstests

## Sicherheitsgrenze

- keine SQL-Migration in v27.31n
- keine Speichertabelle
- keine Fachmutation
- keine direkten App-Rechte
- keine Live-Ausführung
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
vorbereitet. Die notwendigen Helper-Migrationen fehlen noch.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_EXPECTED_STORAGE_VERSION_IDENTITY_BINDING_CONTRACT.md`


## Gesperrte Versionsspalten-Migration v27.31p

Operations-ID-Ausstellungen und Idempotenzoperationen besitzen
im vorbereiteten Schema jetzt jeweils eine nicht nullable
`expected_storage_version`-Spalte ohne Default.

Vorhandene Zeilen führen zum kontrollierten
Migrationsabbruch. Ein unbekannter Versionsstand wird nicht
erfunden.

Die Domain-Speichertabelle selbst ist weiterhin nicht
implementiert.


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
