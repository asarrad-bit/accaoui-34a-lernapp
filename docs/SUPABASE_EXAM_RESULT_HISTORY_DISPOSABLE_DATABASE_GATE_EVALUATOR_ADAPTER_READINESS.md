# Disposable Gate-Evaluator und Adapter-Readiness

Stand: v27.32a
Status: implementiert, verbindungsfrei, nicht live ausgeführt

## Ziel

v27.32a setzt den in v27.31z definierten disposable
Umgebungs-Gate-Vertrag als rein deterministischen Evaluator um.

Zusätzlich entsteht ein verbindungsunfähiger
Datenbank-Verbindungsadapter-Readiness-State.

## Gate-Evaluator

Datei:

`tools/accaoui_disposable_environment_gate.py`

Der Evaluator erhält ausschließlich eine bereits übergebene
Mapping-Struktur. Er liest die Prozessumgebung nicht selbst.

Er akzeptiert nur folgende Schlüssel:

- `ACCAOUI_DB_TEST_MODE`
- `ACCAOUI_DB_TEST_TARGET_KIND`
- `ACCAOUI_DB_TEST_HOST`
- `ACCAOUI_DB_TEST_PORT`
- `ACCAOUI_DB_TEST_DATABASE`
- `ACCAOUI_DB_TEST_CONFIRM`

Unbekannte oder fehlende Felder werden geschlossen abgelehnt.

## Deterministische Klassifikation

Abgelehnt werden:

- fehlende Konfiguration
- unvollständige Konfiguration
- unbekannte Felder
- falscher Modus
- falsche Zielart
- entfernte oder unbekannte Hosts
- geschützte oder unbekannte Datenbanken
- ungültige Ports
- falsche destruktive Bestätigung
- URL- oder Connection-String-Formen

Nur der vollständige lokale Descriptor wird als

`eligible_but_connection_locked`

klassifiziert.

## Normalisierung

Der Evaluator:

- schreibt den Host klein
- entfernt einen abschließenden Host-Punkt
- schreibt den Datenbanknamen klein
- wandelt den Port in eine Ganzzahl um
- gibt die destruktive Bestätigung nicht an den Adapter weiter

Die Eingabe wird nicht verändert. Gleiche Eingaben liefern
identische Ergebnisse.

## Adapter-Readiness-State

Datei:

`tools/accaoui_disposable_connection_adapter_readiness.py`

Der Adapter-State erhält ausschließlich das bereits geprüfte
Gate-Ergebnis.

Ein gültiger lokaler Descriptor wird zu:

- Status: `descriptor_valid_connection_locked`
- Grund: `database_driver_not_selected`
- Treiber ausgewählt: nein
- Verbindung erlaubt: nein
- Verbindung erstellt: nein

Jede abgelehnte Gate-Entscheidung wird als `blocked`
weitergegeben.

## Sicherheitsgrenze

Beide Module enthalten:

- keinen Datenbanktreiber
- keine DNS-Auflösung
- keinen Netzwerk- oder Socketcode
- keine Datenbank-URL
- keine Passwörter oder Secrets
- keine Verbindung
- keine Migration
- keine Testausführung
- keine Frontend-Anbindung

## Automatische Prüfung

`tools/check-supabase-exam-history-disposable-database-gate-evaluator-adapter-readiness.py`

Der Prüfer:

1. validiert den v27.32a-Vertrag
2. bindet ihn an v27.31z und v27.31y
3. führt alle Entscheidungsfälle zweimal aus
4. prüft Determinismus und fehlende Eingabemutation
5. prüft die Descriptor-Normalisierung
6. prüft denied- und eligible-Adapterzustände
7. analysiert Importe und verbotenen Verbindungsinhalt
8. bestätigt fehlende SQL- und Frontend-Anbindung

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.

## Noch offen

- Integration des Evaluators in das Harness
- Auswahl eines Testdatenbanktreibers
- Datenbankverbindung und Testausführung
- ausschließlich testseitige Fehlerinjektion
- Konkurrenz- und Autorisierungstests
- direkte App-Freigabe
- UI-Anbindung
