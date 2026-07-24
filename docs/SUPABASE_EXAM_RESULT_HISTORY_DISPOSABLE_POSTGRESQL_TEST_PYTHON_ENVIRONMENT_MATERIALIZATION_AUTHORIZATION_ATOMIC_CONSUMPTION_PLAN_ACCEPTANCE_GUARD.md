# Atomarer Verbrauchsoperationsplan-Annahme-Guard

Stand: v27.32t
Status: rein implementiert, weiterhin gesperrt, nicht live

## Ziel

v27.32t prüft einen v27.32s-Operationsplan vollständig, bevor er
später an einen Registry-Adapter übergeben werden dürfte.

## Geprüfte Grenzen

Der Guard verlangt:

- exakten Status `atomic_consumption_plan_ready_execution_locked`
- vollständig geschlossene Ausführungs- und Adapterflags
- gültige Operations-ID und ersten Versuch
- feste Adapterart und atomare Fähigkeit
- gebundenen Registry-Key
- `unused -> consumed` mit Verbrauchsrecord in derselben Einheit
- identischen Verbrauchsrecord und Nachweisvorlage
- Einmalverwendung und `executionGrant = false`
- höchstens einen parallelen Gewinner
- geschlossene Fehler- und Reconciliation-Regeln
- keine automatische Wiederholung
- kein Zurücksetzen eines bestätigten Verbrauchs auf `unused`

Manipulierte Pläne werden geschlossen blockiert.

## Ergebnis

Ein gültiger Plan wird kanonisch kopiert und endet nur als:

`accepted_atomic_consumption_plan_execution_locked`

## Sicherheitsgrenze

Auch ein angenommener Plan erlaubt nicht:

- Adapteraufruf
- Registrylesen oder -schreiben
- atomaren Compare-and-set
- Verbrauch oder Commit
- Uhrabfrage
- Token oder Ausführungsgrant
- Dateisystem- oder Prozesszugriff
- Umgebung, Installation, Datenbank-, SQL- oder UI-Anbindung
