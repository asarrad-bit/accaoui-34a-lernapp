# Operations-ID-Ausstellungsvertrag

Stand: v27.31h

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
- Payload-Fingerprint

## Umgesetzt in v27.31h

Eine vollständig gesperrte Ausstellungsdatentabelle ist als
SQL-Migration vorbereitet.

Sie speichert ausschließlich:

- authentifizierten Nutzerbezug
- SHA-256-Hash des Client-Wiederholungsschlüssels
- kanonischen Anfragefingerprint
- serverseitig erzeugte UUID
- Bereich, Mutation, Ressource und Payload-Fingerprint
- Ausstellungszeit

## Noch nicht umgesetzt

- Ausstellungs-RPC
- produktiver Fachmutations-RPC
- Live-Datenbanktests
- Parallelitäts- und Konkurrenztests

Deshalb bleibt die produktive Freigabe gesperrt.

## Sicherheitsgrenze

- SQL-Migration vorbereitet, aber nicht live ausgeführt
- keine direkte Tabellenfreigabe
- keine direkte RPC-Freigabe
- kein Service-Role-Schlüssel im Frontend
- keine echten Teilnehmerdaten
- keine Live-Ausführung
- keine UI-Änderung

## Automatische Prüfung

`tools/check-supabase-exam-history-operation-identity-issuance-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.
