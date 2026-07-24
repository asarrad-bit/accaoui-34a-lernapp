# Atomarer Registry-Adapter-Ausführungsvertrag

Stand: v27.32z
Status: vollständig gesperrter Vertrag, nicht implementiert, nicht live

## Ziel

v27.32z bindet eine spätere atomare Registry-Adapter-Ausführung
ausschließlich an die angenommene v27.32y-Readiness.

## Festgelegte Ausführungsgrenzen

Der spätere Adapter muss:

- die Adapterart `single_use_consumption_registry` verwenden
- atomaren Compare-and-set mit Verbrauchsrecord bereitstellen
- `unused` nur atomar nach `consumed` ändern
- genau einen Adapteraufruf verwenden
- höchstens einen Parallelgewinner zulassen
- feste Operations-, Connect-, Statement- und Lock-Zeitlimits einhalten
- ausschließlich die festgelegten Ergebnisarten liefern
- Rohfehler unterdrücken
- bei unklarem Commit automatische Wiederholung verbieten
- spätere Reconciliation per Operations-ID verlangen
- Nachweis nur aus dem bestätigten Verbrauchsrecord ableiten
- `consumed` niemals auf `unused` zurücksetzen

## Sicherheitsgrenze

Dieser Vertrag implementiert und startet nichts.

Es erfolgen kein Adapteraufruf, kein Registryzugriff, kein
Compare-and-set, kein Verbrauch, kein Uhr-, Datei-, Prozess-,
Netzwerk-, Treiber-, Datenbank-, SQL- oder UI-Zugriff und keine
Token- oder Ausführungsfreigabe.
