# Lokaler Registry-Adapter-Verhaltensvertrag v27.34e

Stand: v27.34e

Status:
`planned_local_fake_atomic_consumption_registry_adapter_behavior_fully_locked_not_implemented`

## Zweck

v27.34e schließt die im Abschlussaudit festgestellten
Verhaltensmehrdeutigkeiten für einen späteren ausschließlich lokalen
Atomic-Consumption-Registry-Adapter gegen den unveränderten
v27.34b-Fake-Treiber.

Dieser Schritt erstellt, importiert, instanziiert und verwendet keinen
Adapter. Die spätere Adapterdatei ist weiterhin nicht vorhanden.

Der maschinenlesbare Vertrag ist:

`docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver-adapter-contract.json`

## Kanonische Quellbindung

Der Vertrag bindet per SHA-256:

- den unveränderten v27.34a-Schnittstellenvertrag und seine Dokumentation
- das unveränderte v27.34b-Fake-Treibermodul und seine Dokumentation
- den v27.34a-Vertragschecker
- den v27.34b-Fake-Treiber-Checker
- die kanonischen v27.34a-Abschnitte für Python-Schnittstelle, Eingabe,
  Resultate, Reconciliation, Zeitlimits und Fake-Treiber
- den bestätigten v27.34d-Ausgangscommit
  `84729c58c5fcb61b7f7ad72d1d695ee2d7095b86`

Request-, Result-, Reconciliation- und Treibertypen dürfen später
ausschließlich aus dem v27.34b-Fake-Treibermodul importiert werden.
Kopien oder parallele Neudefinitionen dieser Payloadtypen sind
verboten.

## Spätere Adapterform

Der spätere Modulpfad ist exakt:

`tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py`

Nur dieses Modul darf das öffentliche, nicht
`runtime_checkable`-Protocol `AtomicConsumptionRegistryAdapter`
definieren.

Die konkrete Implementierung muss privat und final sein:

`_LocalFakeAtomicConsumptionRegistryAdapter`

Ihre `__slots__` enthalten ausschließlich `_driver`. Globale
veränderliche Zustände, Singleton-Instanzen und implizite
Dependency-Auflösung sind verboten.

## Factory

Die spätere Factory besitzt exakt diese Signatur:

```python
def build_atomic_consumption_registry_adapter(
    *,
    driver: LocalFakeAtomicConsumptionRegistryDriver,
) -> AtomicConsumptionRegistryAdapter
```

Sie akzeptiert ausschließlich die exakte konkrete
v27.34b-Klasse durch:

```python
type(driver) is _LocalFakeAtomicConsumptionRegistryDriver
```

Subklassen, Wrapper, Proxys, Mocks, alternative Treiber und
Duck-Typing-Objekte werden mit `ValueError` und exakt dieser Nachricht
abgelehnt:

`driver must be the exact v27.34b _LocalFakeAtomicConsumptionRegistryDriver instance`

Die Factory führt keinen Treiberaufruf, keine Probeoperation, keine
Uhrabfrage und keine Zustandsänderung aus.

## Atomare Operation

Die spätere Operation besitzt exakt diese Signatur:

```python
def consume_materialization_authorization_atomically(
    self,
    request: AtomicConsumptionRequest,
) -> AtomicConsumptionResult
```

Vor dem einzigen Aufruf von
`compare_and_set_with_consumption_record` muss eine vollständige
defensive `deepcopy` des Requests erzeugt werden. Der Originalrequest
darf sich nicht verändern.

Es gibt exakt einen Treiberaufruf, keinen Retry und keinen zusätzlichen
Lese- oder Schreibaufruf.

Das Treiberergebnis wird gegen die unveränderten v27.34a-Schemata
geprüft. Ergebnisart, Status, Grund, Feldreihenfolge, Pflicht- und
Verbotsfelder, Python-Typen, Literalwerte, `operationId`,
Consumption-Record und Evidence müssen exakt stimmen. Unbekannte oder
zusätzliche Felder werden blockiert.

Ein gültiges Fachresultat wird nicht umklassifiziert. Es wird als neue
defensive `deepcopy` zurückgegeben; die mutable Treiberinstanz darf
niemals direkt weitergereicht werden.

## Exception-Mapping

Jede von `Exception` abgeleitete Ausnahme bei Request-Kopie,
Treiberaufruf, Ergebnisprüfung oder Ergebnisprojektion wird ohne
Rohfehlertyp und ohne Rohfehlermeldung exakt auf `operation_failed`
abgebildet.

Die Feldreihenfolge lautet:

1. `status`
2. `reason`
3. `resultKind`
4. `operationId`
5. `consumptionStatus`
6. `reconciliationRequired`
7. `retryAllowed`
8. `executionGrant`

Die Werte sind exakt:

- `status = authorization_consumption_blocked_execution_locked`
- `reason = authorization_consumption_operation_failed`
- `resultKind = operation_failed`
- `consumptionStatus = not_consumed_by_operation`
- `reconciliationRequired = false`
- `retryAllowed = false`
- `executionGrant = false`

`operationId` wird nur dann aus dem Originalrequest übernommen, wenn
der Request exakt ein `dict` und sein vorhandenes Feld `operationId`
exakt ein `str` ist. Andernfalls wird der leere String verwendet.
`consumptionRecord` und `evidence` sind verboten.

`BaseException`, `KeyboardInterrupt` und `SystemExit` werden nicht
abgefangen.

## Reconciliation

Die spätere Operation besitzt exakt diese Signatur:

```python
def reconcile_materialization_authorization_consumption(
    self,
    operation_id: str,
) -> ReconciliationResult
```

Vor dem Treiberaufruf muss `type(operation_id) is str` gelten und der
Wert eine kanonische lowercase UUID v4 sein. Ungültige Werte lösen
ohne Treiberaufruf `ValueError` mit exakt dieser Nachricht aus:

`operation_id must be a canonical lowercase UUID v4`

Bei gültiger ID erfolgt exakt ein Aufruf von
`read_consumption_by_operation_id`. Retry, Consumption-Operation und
Zustandsmutation sind verboten.

Das Ergebnis wird gegen die drei exakten v27.34a-Reconciliation-
Payloads geprüft und als defensive `deepcopy` zurückgegeben.

Jede `Exception` des Treibers, der Ergebnisprüfung oder der
Ergebnisprojektion wird ohne Rohfehler mit der validierten
`operation_id` exakt auf `ambiguous` abgebildet:

- `status = authorization_consumption_reconciliation_ambiguous_execution_locked`
- `reason = authorization_consumption_reconciliation_ambiguous`
- `reconciliationKind = ambiguous`
- `consumptionStatus = unknown`
- `writePerformed = false`
- `retryPerformed = false`
- `executionGrant = false`

`consumptionRecord` und `evidence` sind in diesem abgebildeten Ergebnis
verboten.

## Ergebnisvalidierung

Die neun Atomic-Consumption-Ergebnisarten bleiben exakt:

1. `committed`
2. `already_consumed`
3. `parallel_conflict`
4. `binding_conflict`
5. `expired`
6. `adapter_unavailable`
7. `atomicity_unavailable`
8. `commit_ambiguous`
9. `operation_failed`

Die drei Reconciliation-Arten bleiben exakt:

1. `confirmed`
2. `not_found`
3. `ambiguous`

Alle Pflichtfelder, verbotenen Felder, Feldreihenfolgen, Typen,
Literalwerte und Record-/Evidence-Regeln werden unverändert über die
kanonischen SHA-256-Bindungen auf die v27.34a-Schemata festgelegt.
`executionGrant`, `retryAllowed` und `retryPerformed` bleiben false.

## Zeitlimits

Die Vertragsmetadaten bleiben unverändert:

- Operation: 15000 ms
- Connect: 3000 ms
- Statement: 5000 ms
- Lock: 2000 ms

Der rein lokale Adapter implementiert keine Timerlogik, keinen Sleep,
keine Wall-Clock, keine Threads, keine Signale und keinen
Timeout-Retry. Timeoutbezogene Resultate dürfen ausschließlich aus den
injizierten Direktiven des v27.34b-Fake-Treibers stammen.

## Importgrenze

Später erlaubt sind ausschließlich:

- `copy.deepcopy`
- `re.fullmatch`
- `typing.Protocol`
- `typing.final`
- die fünf exakt benötigten Request-, Result-, Reconciliation- und
  Treibernamen aus dem v27.34b-Fake-Treibermodul

Verboten bleiben insbesondere psycopg, PostgreSQL, Supabase,
Datenbank- und Netzwerkbibliotheken, `os`, `pathlib`, `subprocess`,
`socket`, `asyncio`, `threading`, `time`, `datetime`, dynamische
Imports, `importlib`, `eval`, `exec`, Umgebungsvariablen und
Dateisystemzugriffe.

## Historische Checker-Inventur

Der Vertrag inventarisiert exakt 28 unveränderte historische Checker
mit vollständigem Pfad und SHA-256-Dateifingerprint.

Ihre historischen Vertrags-, Fingerprint-, Struktur-, Sicherheits-
und Manipulationsprüfungen bleiben unverändert. v27.34e ändert keinen
dieser Checker.

Eine spätere zustandsabhängige Anpassung darf ausschließlich die
aktuelle unbedingte Dateiabwesenheitssperre umschalten: Ohne
Adapterdatei bleibt die bestehende Sperre aktiv. Mit einer später
ausdrücklich autorisierten Adapterdatei müssen zusätzlich der
v27.34e-Vertrag, der festgelegte neue Adapter-Checker und die
Adapterdokumentation vorliegen. Keine historische Prüfung darf
abgeschwächt werden.

## Sicherheitsgrenze

In v27.34e bleiben echter Registryzugriff, PostgreSQL, Datenbank, SQL,
Supabase, Live-Supabase, Netzwerk, Dateisystem, Prozesse,
Umgebungsvariablen, echte Schlüssel, echte Teilnehmerdaten,
Uhrzugriff, Grant, Token, Autorisierungsverbrauch und
`executionGrant` vollständig verboten beziehungsweise false.

Adapterimplementierung, Adapterimport, Adapterinstanziierung und
Adapteraufruf bleiben nicht autorisiert. Es gibt keine produktive
Freigabe.

Ein späterer Implementierungsschritt und seine Versions-ID dürfen
ausschließlich durch den Projekteigentümer und den verbindlichen
Projektchat ausgewählt und in `docs/tasks/CURRENT_TASK.md` ausdrücklich
autorisiert werden. `v27.34f` wird nicht automatisch ausgewählt.
