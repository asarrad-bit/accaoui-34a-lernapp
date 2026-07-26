# Local-Fake-Registry-Treiber-Schnittstellenvertrag

Stand: v27.34a

Status: Schnittstelle vollständig festgelegt, vollständig gesperrt,
nicht implementiert und nicht live

## Ausgangslage

Das Abschlussaudit der Vertragskette v27.33g bis v27.33y endete für
die unmittelbare Fake-Adapter-Implementierung mit `NO-GO`.

Adapterart, Operationsname, zehn Eingabefelder, neun Ergebnisarten,
Atomarität, Zeitlimits und Sicherheitsgrenzen waren bereits festgelegt.
Nicht vollständig normiert waren jedoch:

- konkrete Python-Signaturen und Rückgabetypen
- Typ-, Pflicht-, Leerwert- und Wertregeln der Eingabefelder
- Pflicht- und Verbotsfelder jedes Ergebnisses
- Entwurfs- und bestätigtes Consumption-Record-Schema
- Evidence-Schema
- Zuordnung der vier vorhandenen Zeitlimits
- lokale deterministische Fake-Treiber-Semantik
- nur lesende Reconciliation-Schnittstelle

v27.34a schließt ausschließlich diese Mehrdeutigkeiten. Der Schritt
erteilt keine Implementierungs- oder Ausführungsfreigabe.

## Quellbindung

Der Vertrag bindet sich ausschließlich an v27.33y:

- Vertragsstatus
  `implemented_pure_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness_acceptance_execution_locked`
- Annahmestatus
  `accepted_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness_execution_locked`
- Annahmegrund
  `authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness_accepted_execution_locked`
- kanonischer SHA-256-Fingerprint des v27.33y-Vertrags
- weiterhin kein Grant, Token, Verbrauch oder `executionGrant`

## Python-Schnittstellen

Der maschinenlesbare Vertrag legt ohne optionale, variadische oder
dynamische Signaturen fest:

- `AtomicConsumptionRegistryAdapter`
- `LocalFakeAtomicConsumptionRegistryDriver`
- `InjectedUtcClock`
- Adapter-Factory
  `build_atomic_consumption_registry_adapter`
- Fake-Treiber-Factory
  `build_local_fake_atomic_consumption_registry_driver`
- atomare Adapteroperation
  `consume_materialization_authorization_atomically`
- atomare Treiberoperation
  `compare_and_set_with_consumption_record`
- Adapter-Reconciliation
  `reconcile_materialization_authorization_consumption`
- nur lesende Treiber-Reconciliation
  `read_consumption_by_operation_id`

Treiber, Anfangszustand, Simulationsdirektiven und UTC-Uhr müssen
später ausschließlich per Dependency Injection geliefert werden.

## Exaktes Eingabeschema

`AtomicConsumptionRequest` enthält exakt und in unveränderter
Reihenfolge:

1. `operationId`
2. `requestId`
3. `authorizationNonce`
4. `planFingerprint`
5. `actorId`
6. `purpose`
7. `expectedState`
8. `desiredState`
9. `consumptionRecord`
10. `evidenceTemplate`

Für jedes Feld sind Python-Typ, Pflicht, erlaubte Werte,
Leerwertregel und Unveränderlichkeit festgelegt. Unbekannte,
fehlende oder zusätzliche verschachtelte Felder bleiben verboten.

Die bestehenden Bindungen bleiben unverändert:

- UUID-v4 für Operation und Anfrage
- 32-Byte-Base64url-Nonce ohne Padding
- kanonischer SHA-256-Planfingerprint
- opake, nicht leere Akteur-ID
- Zweck exakt
  `disposable_test_python_environment_materialization`
- `unused -> consumed`

## Consumption-Record und Evidence

Der Eingabe-Record ist ein unbestätigter
`ConsumptionRecordDraft`. Er muss alle sechs Identitätsfelder
unverändert binden und besitzt `confirmed = false`.

Nur die erfolgreiche atomare Zustandsänderung darf daraus einen
`ConfirmedConsumptionRecord` mit `confirmed = true` und einer über
die injizierte UTC-Uhr erzeugten `consumedAtUtc`-Zeit bilden.

Es gilt:

- Compare-and-set und bestätigter Record in derselben atomaren Einheit
- höchstens ein Parallelgewinner
- keine Bestätigung vor Commit
- kein Record ohne Zustandsänderung
- keine Zustandsänderung ohne Record
- kein Reset von `consumed` auf `unused`
- Replay bleibt gesperrt

`ConsumptionEvidence` darf ausschließlich aus einem bestätigten
Record entstehen. Es enthält nur die festgelegten Felder, einen
SHA-256-Nonce-Fingerprint und einen kanonischen Record-Fingerprint.
Roh-Nonce, Rohfehler, Zugangsdaten und Teilnehmerdaten sind im
Evidence verboten.

## Neun Ergebnisarten

Die Ergebnisarten bleiben exakt:

1. `committed`
2. `already_consumed`
3. `parallel_conflict`
4. `binding_conflict`
5. `expired`
6. `adapter_unavailable`
7. `atomicity_unavailable`
8. `commit_ambiguous`
9. `operation_failed`

Für jede Art sind Status, Grund, Pflicht- und Verbotsfelder,
Verbrauchsstatus, Evidence-Regel, Terminalität,
Reconciliation-Pflicht, Retry-Sperre und `executionGrant = false`
maschinenlesbar festgelegt.

Nur `committed` darf bestätigten Record und Evidence liefern.
`commit_ambiguous` darf weder Record noch Evidence behaupten und
verlangt Reconciliation. Automatische Wiederholung ist für alle
Ergebnisarten verboten.

## Zeitlimits

Es werden keine neuen Werte eingeführt:

- Operation: 15000 Millisekunden für die gesamte Adapteroperation
- Connect: 3000 Millisekunden für injizierte Treiberverfügbarkeit
- Statement: 5000 Millisekunden für Compare-and-set und Record
- Lock: 2000 Millisekunden für den lokalen atomaren Sperrabschnitt

Der Fake-Treiber darf weder schlafen noch echte Laufzeitmessung
verwenden. Zeitlimitfälle werden ausschließlich deterministisch über
injizierte Simulationsdirektiven ausgelöst.

Ein bekannter Nicht-Commit wird geschlossen auf den festgelegten
Fehlertyp abgebildet. Ein unbekannter Commit-Ausgang wird immer
`commit_ambiguous`.

## Lokale Fake-Treiber-Semantik

Der spätere Fake-Treiber muss:

- vollständig lokal und deterministisch arbeiten
- ausschließlich instanzgebundenen In-Memory-Zustand verwenden
- den Übergang und Record in einem atomaren Sperrabschnitt ausführen
- höchstens einen Gewinner zulassen
- Replay und Bindungsersetzung blockieren
- kontrollierte mehrdeutige Ergebnisse über injizierte Direktiven
  simulieren
- Reconciliation ausschließlich über `operationId` ermöglichen
- ausschließlich eine injizierte UTC-Uhr verwenden

Verboten bleiben globale veränderliche Registryzustände, echte
Datenbank, PostgreSQL, Supabase, Netzwerk, Dateisystem, Prozesse,
Umgebungsvariablen, echte Schlüssel und echte Teilnehmerdaten.

## Reconciliation

Reconciliation akzeptiert ausschließlich `operationId` und liefert
genau einen der Zustände:

- `confirmed`
- `not_found`
- `ambiguous`

Die Operation ist nur lesend. Sie darf nicht schreiben, nicht erneut
verbrauchen und keinen automatischen Retry auslösen.

Nur `confirmed` darf bestätigten Record und daraus abgeleitetes
Evidence liefern. `not_found` darf nicht `unused` annehmen.
`ambiguous` darf keinen Commit behaupten.

## Sicherheitsgrenze

In v27.34a bleiben insbesondere gesperrt:

- Autorisierungsgrant und Autorisierungstoken
- `authorizationMayBeConsumed`
- `executionGrant`
- Fake-Treiber- und Adapterimplementierung
- Adapterimport, Instanziierung und Aufruf
- Registrylesen und -schreiben
- Compare-and-set und Reconciliation-Lesen
- Uhr-, Umgebungs-, Datei- und Prozesszugriff
- Treiber-, Datenbank-, PostgreSQL-, SQL- und Netzwerkzugriff
- Supabase und Live-Supabase
- Frontend und UI

Es wurden kein Fake-Treiber und kein Adaptermodul erstellt.

## Nächster Schritt

Der nächste Schritt ist ausschließlich v27.34b:

erstes lokales Fake-Registry-Treibermodul nach exakt diesem Vertrag.

v27.34b ist durch v27.34a noch nicht autorisiert. Auch v27.34b darf
keine echte Datenbank, kein PostgreSQL, kein Supabase, kein Netzwerk,
keine echten Schlüssel und keine echten Teilnehmerdaten verwenden.
