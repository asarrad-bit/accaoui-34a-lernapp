# Disposable Autorisierungsverbrauchs-Readiness

Stand: v27.32p
Status: rein implementiert, weiterhin gesperrt, nicht live

## Ziel

v27.32p prüft ausschließlich übergebene Fakten und leitet daraus
einen nicht ausführbaren Verbrauchs-Readiness-State ab.

## Voraussetzungen

- genehmigter v27.32n-Übergang
- Status `authorization_request_approved_locked`
- Entscheidung `approve`
- nichtterminal und `executionGrant = false`
- unveränderte Request-ID-, Nonce-, Akteur-, Zweck- und
  Planfingerprint-Bindung
- bereitgestellte Verbrauchszeit nach Genehmigung und strikt vor
  `expiresAt`
- bereitgestellter Registryzustand `unused`

## Blockierungen

Geschlossen blockiert werden unter anderem:

- abgelehnte, abgelaufene, widerrufene oder ausstehende Anfrage
- Bindungsabweichung
- Verbrauch vor Genehmigung oder ab Ablaufzeit
- Registryzustand `consumed`
- Registryzustand `in_flight`
- unbekannter Registryzustand

## Ergebnis

Ein gültiger State endet ausschließlich als:

`consumption_ready_execution_locked`

Der State beschreibt nur den später notwendigen atomaren Übergang
von `unused` zu `consumed`.

## Sicherheitsgrenze

- kein Registrylesen oder -schreiben
- kein Compare-and-set
- kein Verbrauch oder Verbrauchsnachweis
- keine Uhrabfrage
- kein Token oder Ausführungsgrant
- kein Dateisystem- oder Prozesszugriff
- keine Umgebung oder Installation
- keine Datenbank-, SQL- oder UI-Anbindung
