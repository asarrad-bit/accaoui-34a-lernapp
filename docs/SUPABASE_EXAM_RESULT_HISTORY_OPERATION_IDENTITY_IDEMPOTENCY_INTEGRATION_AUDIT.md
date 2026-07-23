# Operations-ID-/Idempotenz-Integrationsaudit

Stand: v27.31j

Status: statischer Sicherheits-Audit, keine Live-Ausführung

## Geprüfte Bestandteile

1. Operations-ID-Ausstellungstabelle v27.31h
2. Operations-ID-Ausstellungs-RPC v27.31i
3. Idempotenz-Reservierungs-RPC v27.31c
4. Idempotenz-Abschluss-RPC v27.31d
5. Operations-ID-Ausstellungsvertrag
6. transaktionaler Fachmutationsvertrag

## Browsergrenze

Der spätere äußere Fachmutations-RPC darf vom Browser nur den
unvertrauenswürdigen `client_request_key` erhalten.

Eine `external_operation_id` darf nicht als Browserparameter
der Ausstellungsgrenze akzeptiert werden.

## Interne UUID-Ausstellung

Der Ausstellungs-RPC:

- akzeptiert keine externe Operations-ID
- hasht den Client-Wiederholungsschlüssel serverseitig
- hasht die kanonische Anfrage serverseitig
- lässt die UUID durch den Datenbank-Default erzeugen
- gibt sie erst nach erfolgreicher Speicherung zurück
- verwendet sie bei identischen Retries erneut

## Übergabe an die Idempotenzgrenze

Reservierung und Abschluss verwenden exakt:

- intern ausgestellte UUID
- Operationsbereich
- Mutation
- Ressourcenidentität
- Payload-Fingerprint

Die vier kanonischen Fachparameter stimmen mit dem
Ausstellungs-RPC überein.

## Zugriffsschutz

Ausstellungs-, Reservierungs- und Abschluss-RPC:

- sind interne Security-Definer-Helfer
- besitzen einen festen `search_path`
- sind für `public`, `anon` und `authenticated` vollständig
  entzogen
- werden nicht direkt im Frontend referenziert
- besitzen kein direktes `GRANT EXECUTE`

## Noch fehlende Verbindung

Ein äußerer transaktionaler Fachmutations-RPC ist noch nicht
implementiert.

Er muss später innerhalb einer einzigen Datenbanktransaktion:

1. den Nutzer authentifizieren
2. die Operations-ID intern ausstellen oder wiederverwenden
3. ausschließlich diese intern erhaltene UUID reservieren
4. nur bei `reserved_new` fachlich mutieren
5. den Vorgang terminal abschließen
6. vorhandene Pending- oder Terminalzustände ohne erneute
   Fachmutation behandeln

Eine browserseitig gelieferte Operations-ID ist unzulässig.

## Auditergebnis

Die vorhandenen internen Schnittstellen sind strukturell
kompatibel und geschlossen geschützt.

Die produktive Freigabe bleibt dennoch gesperrt, bis der äußere
Fachmutations-RPC implementiert und mit Live- und
Parallelitätstests geprüft wurde.

## Automatische Prüfung

`tools/check-supabase-exam-history-operation-identity-idempotency-integration.py`

Der Audit ist dauerhaft in `tools/preflight.py` eingebunden.

## Sicherheitsgrenze

- keine neue SQL-Migration
- kein äußerer Fachmutations-RPC
- keine direkte Helper-Freigabe
- keine echten Teilnehmerdaten
- keine Live-Ausführung
- keine UI-Änderung


## Äußerer RPC-Schnittstellenvertrag v27.31k

Der spätere äußere Fachmutations-RPC darf ausschließlich
folgende Browserparameter akzeptieren:

- Client-Wiederholungsschlüssel
- Operationsbereich
- Mutation
- Ressourcenidentität
- Fach-Payload

Nicht als Browserparameter erlaubt sind insbesondere:

- Operations-UUID
- Operationsidentität
- Payload-Fingerprint
- Nutzer- oder Teilnehmer-ID
- Ergebnis- oder Fehlerstatus

Der äußere RPC muss den Payload kanonisieren und den
Payload-Fingerprint serverseitig ableiten.

Die intern ausgestellte UUID darf ausschließlich intern an
Reservierung und Abschluss weitergegeben werden. Sie wird nicht
Teil der Clientantwort.

Maschinenlesbarer Vertrag:

`docs/contracts/exam-history-outer-domain-mutation-rpc-interface-contract.json`


## Fach-Payload-Grenze v27.31l

Snapshot und Zyklusregister besitzen jetzt getrennte
kanonische Write-Payload-Hüllen.

Delete akzeptiert in beiden Bereichen ausschließlich `null`.

Payload-Fingerprint und kanonische Byteanzahl müssen später
serverseitig aus dem normalisierten PostgreSQL-JSONB-Text
abgeleitet werden.

Der Browser darf weder Fingerprints noch interne Operations-
oder Anfrageidentitäten in den Fach-Payload einschleusen.

Vertrag:

`docs/contracts/exam-history-domain-payload-contract.json`


## Payload-Validierungshelfer v27.31m

Ein interner SQL-Helfer validiert jetzt statisch geprüft:

- Operationsbereich und Operation
- kanonische Snapshot- oder Registerhülle
- Schema-Version
- Inhaltsobjekt
- rekursive Tiefe
- gesperrte interne Schlüssel
- kanonische UTF-8-Größe
- serverseitigen SHA-256-Fingerprint

Der Helfer verändert keine Tabelle und ruft keinen
Idempotenz- oder Operations-ID-Helfer auf.

Der äußere Fachmutations-RPC ist weiterhin nicht umgesetzt.


## Domain-Speicher-Versionsgrenze v27.31n

Snapshot und Zyklusregister erhalten einen monotonen
Speicher-Versionsstand.

Veraltete Write- oder Delete-Anfragen müssen geschlossen
abgelehnt werden. Ein stilles Last-Write-Wins ist unzulässig.

Der erwartete Versionsstand ist Teil der fachlichen
Anfrageidentität. Die vorhandenen Operations-ID- und
Idempotenzhelper binden ihn noch nicht.

Diese Lücke blockiert weiterhin den äußeren Fachmutations-RPC.


## Speicher-Versionsstand-Identitätsbindung v27.31o

Der erwartete `storage_version`-Stand ist verbindlich als Teil
des Operations-ID-Anfragefingerprints und der vollständigen
Idempotenzidentität definiert.

Gleicher Client-Wiederholungsschlüssel mit abweichendem
Versionsstand muss geschlossen kollidieren.

Die bestehenden Tabellen und Helper wurden noch nicht
angepasst. Der äußere Fachmutations-RPC bleibt gesperrt.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_EXPECTED_STORAGE_VERSION_IDENTITY_BINDING_CONTRACT.md`


## Speicher-Versionsstand-Schema v27.31p

Die beiden internen Tabellen erhalten im vorbereiteten Schema
jeweils:

`expected_storage_version bigint not null`

Der Wert besitzt keinen Default und muss mindestens 0 sein.

Sobald vorhandene Zeilen erkannt werden, bricht die Migration
ab. Es findet kein automatischer oder erfundener Backfill
statt.

Ausstellungs- und Reservierungshelper sind weiterhin nicht
angepasst. Der äußere Fachmutations-RPC bleibt gesperrt.


## Operations-ID-Versionsbindung v27.31q

Der interne Operations-ID-Ausstellungs-RPC bindet jetzt den
erwarteten Speicher-Versionsstand in:

- den kanonischen Anfragefingerprint
- die gespeicherte Ausstellungszeile
- den exakten Retry-Vergleich

Der rohe Client-Wiederholungsschlüssel bleibt ein getrennt
gehashter Lookup-Hinweis.

Reservierungs- und Abschlussgrenze wurden nicht verändert.
Die vollständige Integration bleibt deshalb offen.


## Idempotenz-Versionsbindung v27.31r

Der interne Reservierungs-RPC erhält denselben
`p_expected_storage_version`-Wert wie der
Operations-ID-Ausstellungshelper.

Der Wert wird:

- auf mindestens 0 validiert
- in der Idempotenzoperationszeile gespeichert
- bei einer vorhandenen Reservierung exakt verglichen
- bei Abweichung als Identitätskonflikt geschlossen abgelehnt

Der Abschlusshelper akzeptiert keinen neuen Versionsparameter
und kann die gespeicherte Identität nicht überschreiben.

Damit sind die beiden inneren Versionsgrenzen vorbereitet. Die
äußere transaktionale Fachintegration bleibt weiterhin offen.


## Äußere transaktionale Integration v27.31u

Der äußere RPC verbindet Operations-ID-Ausstellung,
Idempotenzreservierung, Domain-Mutation und
Idempotenzabschluss in einem Datenbankaufruf.

Pending- und Terminalwiederholungen führen keine erneute
Domain-Mutation aus. Erwartete Domain-Fehler werden nach
Teilrollback stabil abgeschlossen; unerwartete Fehler rollen
den gesamten Aufruf zurück.

Interne UUIDs und Fingerprints bleiben aus der Clientantwort
ausgeschlossen. Eine direkte Ausführungsfreigabe existiert
noch nicht.
