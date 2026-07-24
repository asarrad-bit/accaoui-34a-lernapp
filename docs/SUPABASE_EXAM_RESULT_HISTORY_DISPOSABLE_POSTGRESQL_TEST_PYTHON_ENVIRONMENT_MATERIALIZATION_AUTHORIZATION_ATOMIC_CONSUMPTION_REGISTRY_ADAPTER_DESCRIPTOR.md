# Atomarer Verbrauchs-Registry-Adapter-Descriptor

Stand: v27.32v
Status: rein, deterministisch und vollständig ausführungsgesperrt

## Ziel

v27.32v setzt einen reinen Descriptor für den späteren atomaren
Autorisierungsverbrauchs-Registry-Adapter um.

Der Descriptor prüft ausschließlich bereits übergebene Fakten.
Er liest keine Umgebung, keine Dateien, keine Registry und keine
Datenbank.

## Quelle

Verbindliche Quelle ist der v27.32u-Vertrag:

`docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-contract.json`

Erforderlich sind:

- Quellversion `v27.32u`
- gesperrter Quellstatus
- Adapterart `single_use_consumption_registry`
- Fähigkeit `atomic_compare_and_set_with_consumption_record`
- erwarteter Zustand `unused`
- gewünschter Zustand `consumed`
- genau ein atomarer Adapteraufruf
- höchstens ein Parallelgewinner
- feste Zeitlimits
- feste Ergebnisarten
- Reconciliation bei unklarem Commit
- vollständig geschlossene Sicherheitsgrenzen

## Descriptor-Ergebnis

Eine gültige Eingabe ergibt:

- Status
  `atomic_consumption_registry_adapter_descriptor_ready_execution_locked`
- Grund
  `authorization_atomic_consumption_registry_adapter_descriptor_ready_execution_locked`
- Descriptor-Version `1`
- kanonische Kopie der geprüften Fakten
- `executionGrant = false`

Fehlende, unbekannte oder manipulierte Felder werden geschlossen
blockiert.

## Zeitlimits

- Gesamtoperation: 15000 ms
- Verbindung: höchstens 3000 ms
- Statement: höchstens 5000 ms
- Lock: höchstens 2000 ms

Timeouts erlauben keinen automatischen Retry.

## Ergebnisarten

Zugelassen sind ausschließlich:

- `committed`
- `already_consumed`
- `parallel_conflict`
- `binding_conflict`
- `expired`
- `adapter_unavailable`
- `atomicity_unavailable`
- `commit_ambiguous`
- `operation_failed`

Ein unklarer Commit darf nicht automatisch wiederholt werden und
erfordert spätere Reconciliation.

## Sicherheitsgrenze

v27.32v führt nichts aus:

- kein Adapteraufruf
- kein Registrylesen oder -schreiben
- kein Compare-and-set
- kein Autorisierungsverbrauch
- kein Token oder Ausführungsgrant
- keine Uhr- oder Umgebungsabfrage
- kein Dateisystemzugriff
- keine Prozess- oder Netzwerkausführung
- kein Treiberimport
- keine Datenbankverbindung
- keine SQL-Migration
- keine UI-Anbindung
- keine Live-Ausführung

## Dateien

- Descriptor:
  `tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_descriptor.py`
- Vertrag:
  `docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-descriptor-contract.json`
- Prüfer:
  `tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-descriptor.py`
