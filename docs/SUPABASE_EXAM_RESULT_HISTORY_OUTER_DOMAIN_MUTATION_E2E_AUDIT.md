# Äußerer Fachmutations-End-to-End-Audit

Stand: v27.31v
Status: verbindlicher statischer Audit, nicht live ausgeführt

## Ziel

Der Audit prüft den vollständig gesperrten äußeren
Fachmutations-RPC statisch vom Eingang bis zur Antwort.

Geprüfter RPC:

`public.accaoui_mutate_exam_history_domain`

## Szenariomatrix

### Neue Reservierung

`reserved_new` darf:

- die Domain-Mutation exakt einmal ausführen
- das kompakte Domain-Ergebnis erstellen
- die Idempotenzoperation exakt einmal als Completed abschließen

### Bestehende Pending-Reservierung

`reserved_existing_pending` muss:

- `in_progress` und `pending` zurückgeben
- `retryable = true` setzen
- ohne Domain-Mutation zurückkehren
- ohne erneuten Idempotenzabschluss zurückkehren

### Bestehende Completed-Reservierung

`reserved_existing_completed` muss:

- das gespeicherte kompakte Ergebnis zurückgeben
- `operation_status = completed` setzen
- ohne Domain-Mutation zurückkehren
- ohne erneuten Abschluss zurückkehren

### Bestehende Failed-Reservierung

`reserved_existing_failed` muss:

- den gespeicherten stabilen Fehlercode zurückgeben
- `operation_status = failed` setzen
- ohne Domain-Mutation zurückkehren
- ohne erneuten Abschluss zurückkehren

## Rollbackgrenzen

### Erwarteter Domain-Fehler

Nur stabile Domain-Fehler dürfen innerhalb des inneren
PL/pgSQL-Blocks abgefangen werden.

Der innere Mutationsblock wird zurückgerollt. Anschließend wird
die Idempotenzoperation stabil als Failed abgeschlossen.

### Unerwarteter Fehler

Es darf keinen pauschalen `WHEN OTHERS`-Handler geben.

Unerwartete Fehler werden erneut ausgelöst. Dadurch rollt der
gesamte äußere Datenbankaufruf zurück, einschließlich einer
frisch erzeugten Ausstellung oder Reservierung.

## Clientantwort

Erlaubt sind ausschließlich:

- `outcome`
- `operation_status`
- `result`
- `failure_code`
- `retryable`

Ausgeschlossen bleiben insbesondere:

- interne Operations-UUID
- Operationsidentität
- Payload- und Anfragefingerprints
- gehashter Client-Wiederholungsschlüssel
- Nutzer-ID
- rohe Datenbankfehler

## Sicherheitsgrenze

- kein `GRANT EXECUTE`
- vollständiger Revoke für public, anon und authenticated
- keine direkte Tabellenmutation im äußeren RPC
- keine Frontend-Referenz
- keine Service-Role im Frontend
- keine SQL-Migration in v27.31v
- keine Live-Ausführung

## Automatische Prüfung

`tools/check-supabase-exam-history-outer-domain-mutation-e2e-audit.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.
