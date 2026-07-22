# Transaktionaler Fachmutations-Integrationsvertrag

Stand: v27.31f

Status: verbindlicher lokaler Vertrag, nicht live ausgeführt

## Ziel

Eine spätere produktive Fachmutation muss Reservierung,
Fachmutation und Idempotenzabschluss innerhalb eines einzigen
geprüften Security-Definer-Mutations-RPCs verbinden.

## Verbindliche Reihenfolge

1. Nutzer ausschließlich über `auth.uid()` bestimmen
2. Eingaben und vertrauenswürdige Operations-ID prüfen
3. Idempotenzoperation atomar reservieren
4. anhand des Reservierungsstatus geschlossen verzweigen
5. ausschließlich bei `reserved_new` die Fachmutation ausführen
6. erfolgreichen oder stabil fehlgeschlagenen Abschluss speichern
7. ausschließlich kanonisches Ergebnis zurückgeben

## Entscheidungsmatrix

### `reserved_new`

- Fachmutation erlaubt
- anschließend terminaler Abschluss erforderlich
- Erfolg und Completed-Abschluss committen gemeinsam

### `reserved_existing_pending`

- keine erneute Fachmutation
- kein zweiter Abschluss
- kontrollierter In-Progress-Zustand

### `reserved_existing_completed`

- keine erneute Fachmutation
- gespeichertes Ergebnis unverändert wiederverwenden

### `reserved_existing_failed`

- keine erneute Fachmutation
- gespeicherten stabilen Fehlerzustand wiederverwenden

## Erwartete Fachfehler

Erwartete und kontrolliert behandelbare Fachfehler müssen
innerhalb eines PL/pgSQL-Exception-Blocks beziehungsweise einer
Subtransaktion behandelt werden.

Dadurch werden alle Teiländerungen der Fachmutation
zurückgerollt, bevor der Idempotenzvorgang mit einem stabilen
Fehlercode als `failed` abgeschlossen wird.

Rohe Datenbankfehler dürfen weder gespeichert noch an den
Browser zurückgegeben werden.

## Unerwartete interne Fehler

Nicht kontrolliert behandelbare interne Fehler müssen erneut
ausgelöst werden.

Die vollständige Datenbanktransaktion muss dann
zurückgerollt werden, einschließlich:

- neuer Idempotenzreservierung
- Fachmutation
- möglichem Abschluss

Ein teilweise gespeicherter Zustand ist unzulässig.

## Identitätsgrenze

Die externe Operations-ID muss aus einer später geprüften
vertrauenswürdigen Server- oder Datenbankquelle stammen.

Noch nicht erfüllt:

- verifizierte Operations-ID-Ausstellung
- produktiver Fachmutations-RPC
- Live-Datenbanktests
- echte Parallelitäts- und Konkurrenztests

Deshalb bleibt die produktive Freigabe gesperrt.

## Sicherheitsgrenze

- kein neuer SQL-RPC in v27.31f
- keine direkte Helper-Ausführungsfreigabe
- keine direkte Tabellenfreigabe
- kein Frontendzugriff
- keine echten Teilnehmerdaten
- keine Live-Ausführung
- keine UI-Änderung

## Automatische Prüfung

`tools/check-supabase-exam-history-transactional-mutation-contract.py`

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.
