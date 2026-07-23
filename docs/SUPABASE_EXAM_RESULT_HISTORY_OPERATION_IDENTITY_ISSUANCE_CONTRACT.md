# Operations-ID-Ausstellungsvertrag

Stand: v27.31u
Status: verbindlicher lokaler Vertrag, nicht live ausgeführt

## Ziel

Beliebige browsergenerierte UUIDs dürfen niemals automatisch
als vertrauenswürdige Idempotenz-Operations-IDs gelten.

Gleichzeitig muss ein echter Wiederholungsaufruf dieselbe
serverseitig ausgestellte Operations-ID wiederverwenden können.

## Zwei getrennte Identitäten

### Client-Wiederholungsschlüssel

Der Browser darf einen `client_request_key` erzeugen.

Dieser Schlüssel ist:

- ein unvertrauenswürdiger Wiederholungshinweis
- kein Berechtigungsnachweis
- keine Operations-ID
- keine Grundlage für eine Fachmutation
- mindestens 128 Bit stark
- später nur als SHA-256-Hash speicherbar

### Verifizierte Operations-ID

Die eigentliche `external_operation_id` muss:

- innerhalb der Datenbank erzeugt werden
- eine UUID Version 4 sein
- durch einen Security-Definer-RPC ausgestellt werden
- vor Rückgabe dauerhaft gespeichert werden
- an den authentifizierten Nutzer gebunden sein
- an Bereich, Mutation, Ressource und Fingerprint gebunden sein

## Stabile Wiederverwendung

Bei identischem:

- authentifiziertem Nutzer
- Client-Wiederholungsschlüssel
- kanonischem Anfragefingerprint

muss dieselbe bereits ausgestellte Operations-UUID
zurückgegeben werden.

Damit kann ein Retry nach einer verlorenen Antwort denselben
echten Vorgang fortsetzen.

## Konflikte

Derselbe Client-Wiederholungsschlüssel mit abweichendem:

- Operationsbereich
- Mutationstyp
- Ressourcenbezug
- erwarteter Speicher-Versionsstand
- Payload-Fingerprint

muss geschlossen abgelehnt werden.

Eine übermittelte Operations-UUID ohne passenden gespeicherten
Ausstellungsdatensatz bleibt unverifiziert.

Eine fremde Nutzerzuordnung darf weder übernommen noch
offengelegt werden.

## Vollständige Verifikation

Die Operations-UUID allein reicht niemals aus.

Verifiziert ist sie erst nach Abgleich von:

- `auth.uid()`
- gehashtem Client-Wiederholungsschlüssel
- kanonischem Anfragefingerprint
- Operations-UUID
- Bereich
- Mutation
- Ressource
- erwarteter Speicher-Versionsstand
- Payload-Fingerprint

## Umgesetzt in v27.31h und v27.31i

Eine vollständig gesperrte Ausstellungsdatentabelle ist als
SQL-Migration vorbereitet.

Sie speichert ausschließlich:

- authentifizierten Nutzerbezug
- SHA-256-Hash des Client-Wiederholungsschlüssels
- kanonischen Anfragefingerprint
- serverseitig erzeugte UUID
- Bereich, Mutation, Ressource und Payload-Fingerprint
- Ausstellungszeit

Der interne Ausstellungs-RPC ist ebenfalls vorbereitet.

Er:

- bestimmt den Nutzer ausschließlich über `auth.uid()`
- akzeptiert einen 256-Bit-Client-Wiederholungsschlüssel
- hasht Client-Schlüssel und kanonische Anfrage serverseitig
- lässt die UUID durch den Datenbank-Default erzeugen
- gibt die UUID erst nach erfolgreicher Speicherung zurück
- verwendet bei einem identischen Retry dieselbe UUID
- blockiert abweichende Anfragen mit demselben Client-Schlüssel
- besitzt keine direkte Ausführungsfreigabe für App-Rollen

## Noch nicht umgesetzt

- produktiver Fachmutations-RPC
- Live-Datenbanktests
- Parallelitäts- und Konkurrenztests

Deshalb bleibt die produktive Freigabe gesperrt.

## Sicherheitsgrenze

- SQL-Migration vorbereitet, aber nicht live ausgeführt
- keine direkte Tabellenfreigabe
- interner Ausstellungs-RPC vorbereitet
- keine direkte RPC-Freigabe
- kein Service-Role-Schlüssel im Frontend
- keine echten Teilnehmerdaten
- keine Live-Ausführung
- keine UI-Änderung

## Automatische Prüfung

`tools/check-supabase-exam-history-operation-identity-issuance-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.


## Integrationsaudit v27.31j

Der statische Audit bestätigt:

- der Browser liefert ausschließlich den unvertrauenswürdigen
  `client_request_key`
- der Ausstellungs-RPC akzeptiert keine externe Operations-ID
- die UUID wird durch den Datenbank-Default erzeugt
- die UUID wird erst nach erfolgreicher Speicherung
  zurückgegeben
- Reservierung und Abschluss erwarten dieselbe intern
  ausgestellte UUID
- die kanonischen Bereichs-, Mutations-, Ressourcen- und
  Fingerprint-Parameter stimmen zwischen allen Helfern überein
- alle drei Helfer bleiben für App-Rollen gesperrt
- im Frontend existiert keine direkte Helper-Referenz

Noch nicht vorhanden ist der äußere Fachmutations-RPC, der
Ausstellung, Reservierung, Fachmutation und Abschluss innerhalb
derselben Datenbanktransaktion verbindet.

Deshalb bleibt die produktive Freigabe gesperrt.

Auditwerkzeug:

`tools/check-supabase-exam-history-operation-identity-idempotency-integration.py`


## Speicher-Versionsstand-Erweiterung v27.31q

Der interne Ausstellungs-RPC wurde um
`p_expected_storage_version bigint` erweitert.

Der kanonische Anfragefingerprint besteht jetzt aus:

- Operationsbereich
- Operation
- Ressourcenidentität
- erwartetem Speicher-Versionsstand
- Payload-Fingerprint

Der Client-Wiederholungsschlüssel wird getrennt gehasht und
nicht in diesen Fingerprint aufgenommen.

Die Ausstellungszeile speichert den erwarteten Versionsstand.
Ein Retry mit demselben Client-Schlüssel muss denselben Stand
besitzen; andernfalls wird er geschlossen abgelehnt.

Der Idempotenz-Reservierungshelper bleibt unverändert und wird
im nächsten getrennten Schritt erweitert.

Migration:

`supabase/migrations/20260722_v2731q_exam_history_operation_identity_expected_version_rpc.sql`


## Äußere Integrationsbindung v27.31u

Die serverseitig ausgestellte Operations-UUID wird jetzt
ausschließlich innerhalb des vollständig gesperrten äußeren
Fachmutations-RPCs an die Idempotenzreservierung weitergegeben.

Der Browser übermittelt weiterhin nur den unvertrauenswürdigen
Client-Wiederholungsschlüssel. Die interne UUID bleibt aus der
Clientantwort ausgeschlossen.

Live-Ausführung und direkte App-Freigabe bleiben offen.
