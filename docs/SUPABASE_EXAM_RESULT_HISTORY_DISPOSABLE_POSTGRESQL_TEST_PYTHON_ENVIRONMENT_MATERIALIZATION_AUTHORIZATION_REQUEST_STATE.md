# Disposable Materialisierungs-Autorisierungsanfrage-State

Stand: v27.32m
Status: rein implementiert, weiterhin gesperrt, nicht live

## Ziel

v27.32m erzeugt aus ausschließlich übergebenen Fakten einen
deterministischen, weiterhin ausführungsgesperrten
Autorisierungsanfrage-State.

## Eingabe

Erforderlich sind:

- durch v27.32k angenommener Plan
- bereitgestellte UUID-v4-Request-ID
- bereitgestellte 32-Byte-Base64url-Nonce
- nichtleere opake menschliche Akteur-ID
- bereitgestellter kanonischer SHA-256-Planfingerprint
- bereitgestellte UTC-Ausgabe- und Ablaufzeit

Der State liest weder Zufall noch aktuelle Uhrzeit.

## Prüfung

- exakter Quellstatus `accepted_execution_locked`
- sämtliche Quell-Ausführungsflags geschlossen
- Fingerprint stimmt mit kanonischem Plan überein
- Request-ID ist lowercase UUID v4
- Nonce dekodiert exakt zu 32 Byte
- Akteur-ID ist getrimmt und frei von Steuerzeichen
- Zeitstempel sind UTC-RFC-3339 ohne Bruchteile
- Ablaufzeit liegt exakt 300 Sekunden nach Ausgabezeit

## Ergebnis

Ein gültiger State endet mit:

`authorization_request_ready_locked`

Die erzeugte Anfrage besitzt den Status:

`authorization_request_pending_locked`

`executionGrant` bleibt `false`.

## Sicherheitsgrenze

- keine Zufalls- oder Uhrabfrage
- kein Token
- keine Genehmigung oder Verbrauchsfreigabe
- kein Dateisystem- oder Prozesszugriff
- keine Umgebung oder Installation
- kein Treiberimport
- keine Datenbank-, SQL- oder UI-Anbindung
