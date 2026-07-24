# Disposable Autorisierungsverbrauchsvertrag

Stand: v27.32o
Status: vollständig gesperrt geplant, nicht ausgeführt

## Ziel

v27.32o beschreibt die spätere einmalige Verbrauchsprüfung einer
durch v27.32n genehmigten, aber weiterhin ausführungsgesperrten
Autorisierungsanfrage.

Der Vertrag verbraucht keine Anfrage und erteilt keine Freigabe.

## Quelle

Erforderlich sind:

- Übergangsstatus `transition_applied_execution_locked`
- Anfrage `authorization_request_approved_locked`
- Entscheidung `approve`
- nichtterminaler Genehmigungszustand
- `executionGrant = false`

Abgelehnte, abgelaufene, widerrufene oder noch ausstehende
Anfragen sind nicht verbrauchbar.

## Bindung

Request-ID, Nonce, Akteur, Zweck und Planfingerprint müssen
unverändert an der genehmigten Anfrage gebunden bleiben.

## Ablauf

Ein späterer Verbrauch muss:

- nach Ausgabe und Genehmigung liegen
- strikt vor `expiresAt` erfolgen
- ohne Kulanzzeit auskommen
- eine später vertrauenswürdig gelesene UTC-Zeit verwenden

## Einmalverwendung

Die spätere Registry verwendet als Schlüssel:

- Request-ID
- Nonce
- Planfingerprint

Der Übergang von `unused` zu `consumed` muss atomar erfolgen.

Replay, paralleler Verbrauch, zweite Verwendung sowie Wiederverwendung
von Request-ID oder Nonce sind verboten.

## In v27.32o nicht umgesetzt

- kein Verbrauchs-State
- keine Registry
- kein Compare-and-set
- kein Verbrauchsnachweis
- kein Uhrzugriff
- kein Verbrauch, Token oder Ausführungsgrant
- kein Dateisystem- oder Prozesszugriff
- keine Umgebung oder Installation
- keine Datenbank-, SQL- oder UI-Anbindung
