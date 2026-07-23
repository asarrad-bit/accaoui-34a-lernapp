# Synthetischer Fixture-Katalog und Harness-Readiness

Stand: v27.31y
Status: implementiert, verbindungsfrei, nicht live ausgeführt

## Ziel

v27.31y materialisiert den in v27.31x festgelegten
synthetischen Fixture-Katalog und ergänzt ein lokal
ausführbares, vollständig verbindungsfreies Harness-Gerüst.

## Fixture-Katalog

Datei:

`tools/fixtures/exam-history-outer-domain-mutation-fixtures.json`

Der Katalog ist eine exakte kanonische Projektion des
v27.31x-Vertrags und enthält:

- zwei synthetische UUID-v4-Testnutzer
- fünf synthetische Ressourcen
- elf eindeutige 256-Bit-Client-Schlüssel
- sechs kanonische Payloads
- feste Versionsstände
- sieben Testszenarien
- zwei Zwei-Parteien-Konkurrenzbarrieren
- Harness-Lebenszyklus und Fehlerinjektionsgrenze

Ein SHA-256-Fingerprint bindet den Katalog an den
v27.31y-Readiness-Vertrag.

## Verbindungsfreies Harness-Gerüst

Datei:

`tools/run-supabase-exam-history-outer-domain-mutation-harness.py`

Der Standardmodus validiert ausschließlich:

- Quellvertrag
- Fixture-Katalog
- Readiness-Vertrag
- kanonischen Fingerprint
- synthetische UUIDs und Ressourcen
- Client-Schlüsselbreite
- Szenario- und Barrierenreferenzen

## Geschlossener Datenbankmodus

Die spätere Ausführung wird über folgende Grenze vorbereitet:

- Flag: `--run-database`
- Umgebung: `ACCAOUI_DB_TEST_MODE=disposable`

In v27.31y ist dieser Modus noch nicht implementiert. Er stoppt
geschlossen mit Exitcode 2.

Dabei gilt ausdrücklich:

- kein Datenbanktreiber
- keine Datenbank-URL
- kein Netzwerkcode
- keine Verbindung
- keine Migration
- keine Testausführung

## Sicherheitsgrenze

Ausgeschlossen bleiben:

- echte Teilnehmerdaten
- echte Namen und E-Mail-Adressen
- Produktionsgeheimnisse
- Service-Role-Schlüssel
- Frontend-Referenzen
- clientseitig auswählbare Fehlerinjektion

## Automatische Prüfung

`tools/check-supabase-exam-history-outer-domain-mutation-harness-readiness.py`

Der Prüfer:

1. vergleicht den Katalog exakt mit v27.31x
2. kontrolliert Fingerprint und Anzahlen
3. analysiert die Harness-Importe und den Quelltext
4. führt den Validate-only-Modus aus
5. prüft den geschlossenen Datenbankmodus
6. bestätigt, dass keine SQL-Migration entstanden ist

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.

## Noch offen

- explizites disposable Umgebungs-Gate
- Datenbank-Verbindungsadapter
- ausschließlich testseitige Fehlerinjektion
- tatsächliche Datenbank-, Konkurrenz- und Autorisierungstests
- direkte App-Freigabe
- UI-Anbindung
