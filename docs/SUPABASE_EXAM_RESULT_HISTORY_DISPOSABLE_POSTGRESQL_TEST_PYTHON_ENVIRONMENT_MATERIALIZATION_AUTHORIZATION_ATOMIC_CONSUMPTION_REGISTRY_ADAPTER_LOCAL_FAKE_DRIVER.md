# Lokaler Fake-Registry-Treiber

Stand: v27.34b

Status: erstes Fake-Treibermodul umgesetzt, vollständig lokal,
deterministisch, instanzgebunden und nicht produktiv

## Quellbindung

v27.34b implementiert ausschließlich das in v27.34a festgelegte
Fake-Treibermodul:

`tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_local_fake_driver.py`

Der maschinenlesbare v27.34a-Schnittstellenvertrag bleibt unverändert.
Sein kanonischer SHA-256-Fingerprint lautet:

`e41efc9592cefffb2c9ffc8bc4a7611a6933cbc57f765f55812d703d08fd2b70`

Es wurde keine parallele Schnittstelle eingeführt.

## Implementierte Schnittstelle

Das Modul stellt die v27.34a-Typen und ausschließlich die festgelegte
Fake-Treiber-Factory bereit:

`build_local_fake_atomic_consumption_registry_driver`

Der erzeugte Treiber besitzt:

- `compare_and_set_with_consumption_record`
- `read_consumption_by_operation_id`

Die Factory verlangt den vollständigen Initialzustand, sämtliche
Simulationsdirektiven und die UTC-Uhr per Dependency Injection. Es
existieren keine optionalen Parameter, keine variadischen Argumente
und keine implizite Abhängigkeitsauflösung.

## Eingabegrenze

`AtomicConsumptionRequest` akzeptiert exakt die zehn durch v27.34a
festgelegten Felder in der festgelegten Reihenfolge:

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

Fehlende, zusätzliche, umgeordnete oder unbekannte verschachtelte
Felder werden geschlossen abgelehnt. UUID-, Nonce-, Fingerprint-,
Akteur-, Zweck-, Zustands-, Record- und Evidence-Bindungen werden
erneut vollständig geprüft. Eingaben, Initialzustände und
Simulationsdirektiven werden nicht verändert.

## Lokaler In-Memory-Zustand

Der Fake-Treiber arbeitet vollständig lokal und ausschließlich mit
instanzgebundenem In-Memory-Zustand.

Jede Factory-Ausführung erzeugt einen getrennten Registryzustand.
Es gibt keinen globalen veränderlichen Registryzustand und keine
gemeinsame Speicherung zwischen zwei Treiberinstanzen.

Der Initialzustand wird tief kopiert. `unused` verlangt einen leeren
Consumption-Record. `consumed` verlangt einen vollständig bestätigten
und identitätsgebundenen Record.

## Atomarer Einmalverbrauch

Der Übergang von `unused` nach `consumed` und die Erzeugung des
bestätigten Consumption-Records erfolgen im selben lokalen atomaren
Sperrabschnitt.

Verbindlich umgesetzt sind:

- höchstens ein Parallelgewinner
- kein getrenntes Read-then-write
- kein Reset von `consumed` auf `unused`
- keine Überschreibung eines bestätigten Records
- zweiter Verbrauch wird geschlossen blockiert
- Replay erzeugt keinen weiteren Verbrauch
- Operations-ID-Reuse mit abweichender Bindung wird blockiert

`consumedAtUtc` stammt ausschließlich aus der injizierten UTC-Uhr.
Ein nicht injizierter Uhrzugriff ist nicht vorhanden.

## Consumption-Record und Evidence

Nur ein bestätigter Übergang erzeugt einen
`ConfirmedConsumptionRecord` mit `confirmed = true`.

Evidence wird ausschließlich aus diesem bestätigten Record
abgeleitet. Nonce- und Record-Fingerprint werden kanonisch mit
SHA-256 gebildet. Roh-Nonce, Rohfehler, Zugangsdaten,
Teilnehmerdaten, Grants und Token werden nicht ausgegeben.

`executionGrant` bleibt in jedem Ergebnis false.

## Exakt neun Ergebnisarten

Der Treiber liefert ausschließlich die neun v27.34a-Ergebnisarten:

1. `committed`
2. `already_consumed`
3. `parallel_conflict`
4. `binding_conflict`
5. `expired`
6. `adapter_unavailable`
7. `atomicity_unavailable`
8. `commit_ambiguous`
9. `operation_failed`

Status, Grund, Verbrauchsstatus, Record- und Evidence-Payload,
Reconciliation-Pflicht, Retry-Sperre und `executionGrant` entsprechen
exakt dem v27.34a-Vertrag.

Nur `committed` enthält Record und Evidence.
`commit_ambiguous` enthält weder Record noch Evidence und verlangt
Reconciliation. Alle Ergebnisarten verbieten automatischen Retry.

## Simulationsgrenze

Zeitlimit-, Verfügbarkeits-, Atomaritäts-, Fehler- und
Commit-Ambiguitätsfälle werden ausschließlich über bei der
Konstruktion injizierte Simulationsdirektiven kontrolliert.

Der Fake-Treiber schläft nicht und misst keine echte Laufzeit.
Eine Direktive wird pro `operationId` höchstens einmal verarbeitet.
Ein wiederholter Aufruf löst keine automatische Wiederholung der
atomaren Operation aus.

Eine kontrolliert mehrdeutige Operation kann entweder:

- einen bestätigten Record nur für die spätere Reconciliation
  sichtbar machen oder
- bis zur Reconciliation ausdrücklich mehrdeutig bleiben

Das direkte Ergebnis behauptet in beiden Fällen keinen Commit.

## Reconciliation

Reconciliation akzeptiert ausschließlich `operationId` und liefert
genau:

- `confirmed`
- `not_found`
- `ambiguous`

Die Operation ist nur lesend. Wiederholte Reconciliation verändert
weder Registryzustand noch Record, Direktiven, Operationsbindung oder
Ambiguitätsstatus.

Nur `confirmed` enthält den bestätigten Record und daraus abgeleitete
Evidence. `not_found` nimmt nicht an, dass die Autorisierung
`unused` ist. `ambiguous` behauptet keinen Commit.

## Ausgeführte Tests

Der v27.34b-Checker führt insbesondere aus:

- erfolgreichen einmaligen Verbrauch
- zweiten Verbrauch und Replay-Sperre
- echten Zwei-Thread-Parallelversuch mit exakt einem Gewinner
- alle neun Ergebnisarten und deren exakte Payloads
- Record- und Evidence-Konsistenz
- kontrollierte mehrdeutige Ergebnisse
- Reconciliation `confirmed`, `not_found` und `ambiguous`
- Zustandsvergleich vor und nach jeder Reconciliation
- Sperre automatischer Wiederholung
- Unveränderlichkeit aller Eingaben
- getrennten Zustand getrennter Treiberinstanzen
- Manipulationsmatrix für Request, Initialzustand und Direktiven
- statische Sperre verbotener Imports und Seiteneffekte

## Sicherheitsgrenze

Nicht umgesetzt oder verwendet wurden:

- kein echter Registry-Adapter
- kein PostgreSQL
- keine Datenbank
- kein SQL
- kein Supabase oder Live-Supabase
- kein Netzwerk
- kein Dateisystemzugriff durch den Treiber
- kein Prozesszugriff
- keine Umgebungsvariablen
- keine echten Schlüssel
- keine echten Teilnehmerdaten
- keine UI
- kein `authorizationGrant`
- kein `authorizationToken`
- kein `executionGrant`

## Folgeschrittgrenze

v27.34b autorisiert keinen weiteren Versionsschritt.
Insbesondere bleiben ein echter Registry-Adapter, dessen Factory,
Adapterimport, Adapterinstanziierung, Adapteraufruf und jede echte
Ausführung vollständig gesperrt.
