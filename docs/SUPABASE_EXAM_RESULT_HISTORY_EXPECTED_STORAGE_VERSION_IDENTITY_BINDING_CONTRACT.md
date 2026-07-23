# Speicher-Versionsstand-Identitätsbindung

Stand: v27.31u
Status: verbindlicher lokaler Integrationsvertrag,
nicht live ausgeführt

## Ziel

Der erwartete `storage_version`-Stand muss Teil der
Operations-ID-Ausstellung und der Idempotenzidentität werden.

Ohne diese Bindung könnte derselbe Wiederholungsschlüssel oder
dieselbe Operations-UUID versehentlich für fachlich
unterschiedliche Versionsstände wiederverwendet werden.

## Browsergrenze

Der Browser darf den erwarteten Versionsstand ausschließlich
an den späteren äußeren Fachmutations-RPC übermitteln.

Direkte Aufrufe interner Ausstellungs-, Reservierungs- oder
Abschlusshelfer bleiben verboten.

## Operations-ID-Ausstellung

Der Ausstellungs-Anfragefingerprint muss enthalten:

- Operationsbereich
- Operation
- Ressourcenidentität
- erwarteten Speicher-Versionsstand
- Payload-Fingerprint

Gleicher Client-Wiederholungsschlüssel und identische Anfrage:

- dieselbe gespeicherte Operations-UUID wird wiederverwendet

Gleicher Client-Wiederholungsschlüssel, aber anderer
Versionsstand:

- geschlossener Anfragekonflikt
- keine neue UUID
- keine Fachmutation

## Idempotenzreservierung

Die vollständige Idempotenzidentität muss enthalten:

- Nutzer
- Operationsbereich
- Operation
- Ressourcenidentität
- erwarteten Speicher-Versionsstand
- Payload-Fingerprint

Eine vorhandene Reservierung mit abweichendem Versionsstand
darf nicht als identische Operation behandelt werden.

## Abschluss

Der Abschlusshelfer benötigt keinen neuen Browserparameter.

Er muss den gespeicherten Versionsstand der reservierten
Operation verwenden und darf ihn nicht verändern oder
überschreiben.

## Erforderliche spätere Schemaänderungen

Beide internen Tabellen benötigen eine gesperrte Spalte:

`expected_storage_version bigint not null`

Zusätzlich erforderlich:

- Wert mindestens 0
- sichere Behandlung bestehender Zeilen
- Einbindung in Fingerprint und Operationsidentität
- keine direkten Tabellenrechte
- keine direkte Helper-Ausführungsfreigabe

## Aktueller Stand

Die beiden internen Tabellenschemata enthalten jetzt
`expected_storage_version bigint not null` mit Mindestwert 0.

Der interne Operations-ID-Ausstellungshelper bindet den
Versionsstand jetzt im Anfragefingerprint, in der gespeicherten
Ausstellungszeile und beim Retry-Vergleich.

Der Idempotenz-Reservierungshelper bindet den Versionsstand
jetzt ebenfalls in der gespeicherten Operationszeile und im
exakten Retry-Vergleich.

Deshalb bleiben gesperrt:

- Speichertabellen-Implementierung
- Speicher-Mutationshelfer
- äußerer Fachmutations-RPC
- produktive Freigabe

## Sicherheitsgrenze

- gesperrte Schema-Migration vorbereitet, nicht live ausgeführt
- keine Tabellenänderung
- keine Helper-Änderung
- keine Fachmutation
- keine Live-Ausführung
- keine UI-Änderung

## Automatische Prüfung

`tools/check-supabase-exam-history-expected-storage-version-identity-binding.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.


## Schema-Migration v27.31p

Die beiden internen Tabellen erhalten:

`expected_storage_version bigint not null`

mit der Bedingung:

`expected_storage_version >= 0`

Es existiert bewusst kein Default.

Jeder spätere interne Insert muss den Wert ausdrücklich und
geprüft übergeben.

### Bestehende Zeilen

Enthält eine der beiden Tabellen bereits Zeilen, bricht die
Migration kontrolliert ab.

Es wird niemals automatisch Version 0 oder ein anderer
erfundener Wert gesetzt.

### Unveränderte Sicherheitsgrenze

- RLS bleibt aktiviert und erzwungen
- keine Direktpolicy
- vollständiger Revoke für `public`, `anon` und
  `authenticated`
- keine Helper-Änderung
- keine Fachmutation
- keine Live-Ausführung

Migration:

`supabase/migrations/20260722_v2731p_exam_history_expected_storage_version_schema.sql`


## Operations-ID-Ausstellungsbindung v27.31q

Der interne Ausstellungs-RPC akzeptiert zusätzlich:

`p_expected_storage_version bigint`

Der Wert:

- muss mindestens 0 sein
- liegt im kanonischen Anfragefingerprint
- wird in der Ausstellungszeile gespeichert
- wird bei einem bestehenden Retry exakt verglichen
- führt bei abweichender Wiederverwendung desselben
  Client-Schlüssels zu einem geschlossenen Konflikt

Der rohe Client-Wiederholungsschlüssel wird nur separat gehasht
und ist kein Bestandteil des kanonischen Anfragefingerprints.

Die alte Fünf-Parameter-Funktionsüberladung wird entfernt.
Direkte Ausführung für App-Rollen bleibt vollständig gesperrt.

Migration:

`supabase/migrations/20260722_v2731q_exam_history_operation_identity_expected_version_rpc.sql`


## Idempotenz-Reservierungsbindung v27.31r

Der interne Reservierungs-RPC akzeptiert zusätzlich:

`p_expected_storage_version bigint`

Der Wert:

- muss mindestens 0 sein
- wird in der Idempotenzoperationszeile gespeichert
- gehört zur vollständigen Operationsidentität
- wird bei einer vorhandenen Reservierung exakt verglichen
- führt bei derselben Operations-UUID mit abweichendem Stand
  zu `idempotency_operation_identity_conflict`

Die kanonische `operation_identity`-Zeichenfolge bleibt an
Bereich, Operation und serverseitig ausgestellte UUID gebunden.
Der erwartete Versionsstand wird als zusätzlicher
Identitätsbestandteil separat gespeichert und geprüft.

Die alte Fünf-Parameter-Funktionsüberladung wird entfernt.
Direkte Ausführung für App-Rollen bleibt vollständig gesperrt.

Der Abschlusshelper erhält keinen neuen Versionsparameter. Er
liest den Stand ausschließlich aus der reservierten Zeile.

Migration:

`supabase/migrations/20260722_v2731r_exam_history_idempotency_expected_version_reserve_rpc.sql`


## Domain-Speichertabelle v27.31s

Nach der vollständigen inneren Versionsbindung steht jetzt die
gesperrte Domain-Speichertabelle bereit.

Der `storage_version`-Stand besitzt keinen Default und beginnt
bei einer durch den späteren Mutationshelper kontrollierten
Neuanlage mit 1.

Die End-to-End-Weitergabe des erwarteten Versionsstands durch
den äußeren Fachmutations-RPC bleibt weiterhin offen.


## Domain-Mutationsbindung v27.31t

Der erwartete Speicher-Versionsstand wird jetzt zusätzlich im
internen Domain-Speicher-Mutationshelper innerhalb der
Zeilensperre exakt verglichen.

Die vollständige äußere Weitergabe desselben Werts an
Operations-ID-Ausstellung, Idempotenzreservierung und
Domain-Mutation bleibt Aufgabe des späteren äußeren
Fachmutations-RPCs.


## Geschlossene End-to-End-Versionsbindung v27.31u

Der äußere Fachmutations-RPC reicht exakt denselben
`p_expected_storage_version`-Wert an Ausstellung, Reservierung
und Domain-Mutation weiter.

Eine Wiederholung mit abweichendem Stand kollidiert damit
bereits in der Operationsidentität oder spätestens innerhalb
der gesperrten Domain-Zeile.

Live-, Konkurrenz- und Autorisierungstests bleiben weiterhin
offen.
