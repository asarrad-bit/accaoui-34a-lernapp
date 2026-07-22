# Speicher-Versionsstand-Identitätsbindung

Stand: v27.31p

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

Die internen Ausstellungs- und Reservierungshelper binden den
Versionsstand weiterhin noch nicht.

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
