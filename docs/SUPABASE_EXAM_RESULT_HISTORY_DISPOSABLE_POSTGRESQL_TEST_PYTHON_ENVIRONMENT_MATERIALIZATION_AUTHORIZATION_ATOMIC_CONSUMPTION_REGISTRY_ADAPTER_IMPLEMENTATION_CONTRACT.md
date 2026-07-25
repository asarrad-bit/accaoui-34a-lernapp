# Registry-Adapter-Implementierungsvertrag

Stand: v27.33g
Status: vollständig gesperrter Vertrag, nicht implementiert, nicht live

## Ziel

v27.33g beschreibt die verbindliche Schnittstelle für eine spätere
Implementierung des atomaren Einmalverbrauch-Registry-Adapters.

Quelle ist ausschließlich der angenommene und weiterhin vollständig
gesperrte v27.33f-Ausführungsplan.

## Festgelegte Schnittstelle

Der spätere Adapter muss:

- die Adapterart `single_use_consumption_registry` verwenden
- die Operation `consume_materialization_authorization_atomically`
  bereitstellen
- ausschließlich die festgelegten zehn Eingabefelder akzeptieren
- atomaren Compare-and-set mit Verbrauchsrecord in derselben
  Transaktion unterstützen
- `unused` nur atomar nach `consumed` ändern
- genau einen Adapteraufruf verwenden
- höchstens einen Parallelgewinner zulassen
- feste Operations-, Connect-, Statement- und Lock-Zeitlimits einhalten
- ausschließlich die festgelegten Ergebnisarten liefern
- Rohfehler unterdrücken
- bei unklarem Commit automatische Wiederholung verbieten
- spätere Reconciliation per Operations-ID verlangen
- Nachweis nur aus einem bestätigten Verbrauchsrecord ableiten
- `consumed` niemals auf `unused` zurücksetzen

## Sicherheitsgrenze

Dieser Vertrag erzeugt und importiert kein Adaptermodul.

Es erfolgen keine Implementierung, Instanziierung, kein Adapteraufruf,
kein Registryzugriff, kein Compare-and-set, kein Verbrauch, kein
Uhr-, Umgebungs-, Datei-, Prozess-, Netzwerk-, Treiber-, Datenbank-,
SQL- oder UI-Zugriff und keine Token- oder Ausführungsfreigabe.
