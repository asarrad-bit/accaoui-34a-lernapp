# Disposable Materialisierungs-Autorisierungsanfrage-Vertrag

Stand: v27.32l
Status: vollständig gesperrt geplant, nicht ausgestellt

## Ziel

v27.32l beschreibt die spätere menschliche
Autorisierungsanfrage für einen bereits durch v27.32k geprüften
Materialisierungsplan.

Der Vertrag erzeugt weder eine Anfrage noch eine Freigabe.

## Quell- und Planbindung

Die spätere Anfrage darf nur an einen Plan mit

`accepted_execution_locked`

gebunden werden.

Der Plan wird nicht roh gespeichert. Die Bindung erfolgt über
einen kanonischen SHA-256-Fingerprint.

## Identität und Ablauf

Später erforderlich:

- Request-ID als UUID v4
- 32 Byte Nonce als Base64url ohne Padding
- Akteurtyp `human_operator`
- nichtleere opake Akteur-ID
- exakt fünf Minuten Gültigkeit
- keine Verlängerung, Wiederverwendung oder Replay

Initialstatus:

`authorization_request_pending_locked`

`executionGrant` bleibt `false`.

Auch eine spätere Genehmigung bleibt ausführungsgesperrt.

## In v27.32l nicht umgesetzt

- kein Anfrage-Builder oder Anfragestate
- keine UUID, Nonce oder Uhrzeit
- keine Anfrage oder Tokenausgabe
- keine Genehmigung oder Ausführungsfreigabe
- kein Dateisystem- oder Prozesszugriff
- keine Umgebung oder Installation
- keine Datenbank-, SQL- oder UI-Anbindung
