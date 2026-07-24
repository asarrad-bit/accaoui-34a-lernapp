# Registry-Adapter-Descriptor-Annahme-Guard

Stand: v27.32w
Status: rein implementiert, weiterhin gesperrt, nicht live

## Ziel

v27.32w prüft den kanonischen v27.32v-Registry-Adapter-
Descriptor vollständig, bevor er später als Grundlage einer
Adapter-Readiness dienen dürfte.

## Geprüfte Grenzen

Der Guard verlangt:

- exakten Quellstatus und -grund
- vollständig geschlossene Quell- und Sicherheitsflags
- Descriptor-Version 1
- Quellbindung an v27.32u
- feste Adapterart und atomare Fähigkeit
- Zustandswechsel `unused -> consumed`
- genau einen Adapteraufruf und höchstens einen Parallelgewinner
- feste Operations-, Connect-, Statement- und Lock-Zeitlimits
- ausschließlich festgelegte Ergebnisarten
- Reconciliation bei unklarem Commit
- keine automatische Wiederholung
- `executionGrant = false`

Manipulierte, fehlende oder unbekannte Felder werden geschlossen
blockiert.

## Ergebnis

Ein gültiger Descriptor wird kanonisch kopiert und endet nur als:

`accepted_atomic_consumption_registry_adapter_descriptor_execution_locked`

## Sicherheitsgrenze

Auch ein angenommener Descriptor erlaubt nicht:

- Adapterimplementierung oder Adapteraufruf
- Registrylesen oder -schreiben
- atomaren Compare-and-set oder Verbrauch
- Reconciliation-Zugriff
- Uhr-, Umgebungs- oder Dateisystemzugriff
- Prozess-, Netzwerk-, Treiber- oder Datenbankzugriff
- SQL-Migration oder UI-Anbindung
- Token oder Ausführungsgrant
