# Äußerer Fachmutations-Datenbank-Testvertrag

Stand: v27.31w
Status: verbindlicher Testvertrag, nicht live ausgeführt

## Ziel

Dieser Vertrag beschreibt die späteren echten Datenbanktests für:

`public.accaoui_mutate_exam_history_domain`

v27.31w führt keinen Datenbanktest aus und erzeugt keine
SQL-Migration.

## Testumgebung

Zulässig ist ausschließlich:

- eine getrennte disposable Testdatenbank
- Migrationen in Repository-Reihenfolge
- synthetische Nutzer und Ressourcen
- Rücksetzung zwischen Testfällen
- kontrollierter Test-Owner oder Test-Harness
- interne Tabellenbeobachtung nur im Test-Harness

Unzulässig bleiben:

- Produktionsdatenbank
- echte Teilnehmerdaten
- dauerhafte Grant-Änderungen
- Service-Role im Frontend
- UI-Anbindung

## Autorisierungstests

Zu prüfen sind:

- `public`: direkte Ausführung abgelehnt
- `anon`: direkte Ausführung abgelehnt
- `authenticated`: direkte Ausführung abgelehnt
- kontrollierter Harness ohne `auth.uid()`: `authentication_required`
- kontrollierter Harness mit synthetischem `auth.uid()`: Szenario ausführbar
- keine Nutzer- oder Teilnehmer-ID als Browserparameter
- keine fremde Nutzermutation

## Retrytests

### Identischer abgeschlossener Retry

Gleicher Client-Schlüssel und identische Anfrage müssen:

- dasselbe terminale Ergebnis zurückgeben
- keine neue Domain-Mutation ausführen
- keine neue Speicherversion erzeugen
- keine neue Ausstellungs- oder Reservierungszeile erzeugen

### Pending Retry

Ein bestehender Pending-Vorgang muss:

- `in_progress`
- `operation_status = pending`
- `retryable = true`

zurückgeben und darf weder mutieren noch abschließen.

### Abweichender Versionsstand

Derselbe Client-Schlüssel mit abweichendem erwarteten
Versionsstand muss geschlossen mit

`client_request_key_reused_with_different_request`

abgelehnt werden.

### Bestehender Failed-Vorgang

Ein Retry muss denselben stabilen Fehler zurückgeben und darf
weder erneut mutieren noch erneut abschließen.

## Versionstests

Zu prüfen sind:

- Create nur mit erwarteter Version 0
- erster gespeicherter Stand exakt 1
- zweiter unabhängiger Create mit Version 0 kollidiert
- Update nur gegen den exakten aktuellen Stand
- stale Update kollidiert ohne Zustandsänderung
- Delete erzeugt Tombstone und erhöht exakt um 1
- stale Delete kollidiert ohne Zustandsänderung
- bereits gelöschte Ressource bleibt bei exakter Version
  `already_deleted` ohne weitere Versionserhöhung

## Konkurrenztests

### Zwei Writes mit demselben erwarteten Stand

- genau eine Mutation erfolgreich
- genau ein geschlossener Versionskonflikt
- finale Version nur einmal erhöht
- kein stilles Last-Write-Wins

### Zwei Creates derselben Identität

- genau ein Create erfolgreich
- genau ein geschlossener Konflikt
- final exakt eine Domain-Zeile
- Unique-Konflikt wird erneut fachlich ausgewertet

## Rollbacktests

### Erwarteter Domain-Fehler

- innerer Mutationsblock vollständig zurückgerollt
- stabile Failed-Idempotenzoperation gespeichert
- Retry liefert denselben Fehler
- kein roher Datenbankfehler

### Unerwarteter Fehler

Ein ausschließlich testseitig injizierter Fehler muss:

- den gesamten äußeren Aufruf zurückrollen
- keine Ausstellungszeile hinterlassen
- keine Reservierungszeile hinterlassen
- keine Domain-Änderung hinterlassen
- keinen Failed-Terminalzustand hinterlassen

Ein Produktions-Fault-Hook ist verboten.

## Beobachtungsgrenze

Interne Zeilen dürfen nur der kontrollierte Test-Harness prüfen.
Die Clientantwort bleibt auf folgende Felder begrenzt:

- `outcome`
- `operation_status`
- `result`
- `failure_code`
- `retryable`

Interne UUIDs, Fingerprints und rohe Datenbankfehler bleiben
ausgeschlossen.

## Noch offen

- disposable Datenbank-Harness
- synthetischer Fixture-Katalog
- ausschließlich testseitige Fehlerinjektion
- tatsächliche Datenbanktestausführung
- Konkurrenz- und Autorisierungstestläufe
- direkte App-Freigabe
- UI-Anbindung

## Automatische Prüfung

`tools/check-supabase-exam-history-outer-domain-mutation-database-test-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.
