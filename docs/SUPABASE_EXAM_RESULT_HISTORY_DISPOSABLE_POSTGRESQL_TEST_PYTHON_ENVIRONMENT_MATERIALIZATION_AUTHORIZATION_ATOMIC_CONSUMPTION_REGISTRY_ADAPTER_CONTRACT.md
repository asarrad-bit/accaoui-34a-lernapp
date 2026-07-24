# Atomarer Verbrauchs-Registry-Adapter-Vertrag

Stand: v27.32u
Status: vollständig gesperrt geplant, nicht implementiert

## Ziel

v27.32u beschreibt den späteren Registry-Adapter für einen durch
v27.32t angenommenen atomaren Verbrauchsoperationsplan.

Es wird kein Adapter implementiert oder aufgerufen.

## Quelle und Adaptereingabe

Erforderlich sind:

- `accepted_atomic_consumption_plan_execution_locked`
- erster Operationsversuch
- Adapterart `single_use_consumption_registry`
- Fähigkeit `atomic_compare_and_set_with_consumption_record`
- Registry-Key aus Request-ID, Nonce und Planfingerprint
- `unused -> consumed`
- Verbrauchsrecord und Nachweisvorlage
- `executionGrant = false`
- Operationszeitlimit 15 Sekunden

## Atomare Operation

Der spätere Adapter muss mit einem einzigen Aufruf:

1. den vollständigen Registry-Key binden,
2. `unused` atomar mit `consumed` vergleichen und setzen,
3. den Verbrauchsrecord in derselben Einheit committen.

Getrenntes Lesen und Schreiben, Upsert, Teilcommit und
automatischer Retry sind verboten.

## Ergebnisse

Nur feste Ergebnisse sind erlaubt:

- committed
- already_consumed
- parallel_conflict
- binding_conflict
- expired
- adapter_unavailable
- atomicity_unavailable
- commit_ambiguous
- operation_failed

Ein unklarer Commit darf nicht automatisch wiederholt werden und
erfordert spätere Reconciliation.

## Sicherheitsgrenze

- keine Adapterimplementierung oder -ausführung
- kein Registrylesen oder -schreiben
- kein Compare-and-set oder Verbrauch
- keine Reconciliation-Ausführung
- keine Uhrabfrage
- kein Token oder Ausführungsgrant
- kein Dateisystem-, Prozess-, Netzwerk- oder Datenbankzugriff
- keine SQL- oder UI-Anbindung
