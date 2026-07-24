# Atomarer Autorisierungsverbrauchsoperationsvertrag

Stand: v27.32r
Status: vollständig gesperrt geplant, nicht ausgeführt

## Ziel

v27.32r beschreibt die spätere atomare Verbrauchsoperation für
eine durch v27.32q angenommene Verbrauchs-Readiness.

Der Vertrag greift auf keine Registry zu und verbraucht nichts.

## Quelle

Erforderlich sind:

- `accepted_consumption_ready_execution_locked`
- kanonisch angenommene Readiness
- Registryzustand `unused`
- Compare-Zustand `unused`
- Set-Zustand `consumed`
- `singleUse = true`
- `executionGrant = false`

## Registry-Adapter

Der spätere Adapter muss in einer einzigen atomaren Operation:

1. den gebundenen Registry-Key prüfen,
2. `unused` mit `consumed` vergleichen und setzen,
3. den Verbrauchsrecord gemeinsam committen.

Getrenntes Lesen und Schreiben, Upsert, unbedingtes Schreiben
oder Zurücksetzen auf `unused` sind verboten.

## Konflikte und Fehler

- höchstens ein paralleler Gewinner
- bereits verbrauchte oder parallele Zugriffe werden geschlossen
  blockiert
- kein automatischer Retry bei unklarem Commit
- unklarer Commit erfordert spätere Reconciliation
- Rohfehler und Registrywerte werden nicht offengelegt
- ein bestätigter `consumed`-Status darf nie auf `unused`
  zurückgesetzt werden

## Verbrauchsnachweis

Ein Nachweis darf nur aus dem atomar bestätigten Verbrauchsrecord
entstehen.

Er enthält keine Roh-Nonce und bleibt:

`authorization_consumed_execution_locked`

mit:

`executionGrant = false`

## In v27.32r nicht umgesetzt

- kein Operationsplan
- kein Registry-Adapter
- kein Registryzugriff
- kein Compare-and-set
- kein Verbrauchsrecord oder Nachweis
- keine Uhrabfrage
- kein Verbrauch, Token oder Ausführungsgrant
- kein Dateisystem- oder Prozesszugriff
- keine Umgebung, Installation, Datenbank-, SQL- oder UI-Anbindung
