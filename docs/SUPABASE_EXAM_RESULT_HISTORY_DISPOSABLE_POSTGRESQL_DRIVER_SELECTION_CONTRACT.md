# Disposable PostgreSQL-Treiberauswahlvertrag

Stand: v27.32c
Status: ausgewählt, nicht installiert, nicht live ausgeführt

## Ziel

v27.32c legt verbindlich fest, welcher PostgreSQL-Treiber später
ausschließlich für die lokale disposable Datenbank-Testumgebung
verwendet werden darf.

## Ausgewählter Treiber

- Distribution: `psycopg`
- Extra: `binary`
- feste Spezifikation: `psycopg[binary]==3.3.4`
- Importname: `psycopg`
- Generation: Psycopg 3
- kein Pool-Extra
- kein Async-Modus

Die Binary-Variante ist ausgewählt, damit keine lokale
`libpq`- oder Compilerinstallation vorausgesetzt wird.

## Kompatibilitätsgrenze

Der Vertrag begrenzt den späteren Einsatz auf:

- Python 3.10 bis 3.14
- PostgreSQL 10 bis 18
- Windows, Linux und macOS
- ausschließlich lokale disposable Testdatenbanken

Produktiver Einsatz ist ausgeschlossen.

## Importgrenze

Der Treiber darf später nur innerhalb einer eigenen
Verbindungsadapter-Funktion importiert werden.

Voraussetzungen:

1. Gate-Ergebnis ist `eligible_but_connection_locked`
2. Adapter-Readiness besitzt einen validierten Descriptor
3. disposable Modus ist ausdrücklich gesetzt
4. installierte Version stimmt exakt mit 3.3.4 überein
5. Binary-Implementierung ist verfügbar

Modulweite Imports im Harness, Evaluator oder aktuellen
Adapter-Readiness-State bleiben verboten.

## Timeouts

Später verbindlich:

- Verbindungsaufbau: 3 Sekunden
- SQL-Anweisung: 5 Sekunden
- Sperrwartezeit: 2 Sekunden
- Leerlauf in Transaktion: 10 Sekunden
- gesamtes Szenario: 15 Sekunden

Timeouts werden geschlossen behandelt und nicht automatisch
wiederholt.

## Transaktionsgrenze

- `autocommit` bleibt aus
- jedes Szenario erhält eine eigene explizite Transaktion
- Fixture-Daten dürfen nicht committed werden
- nach Assertions erfolgt Rollback
- erwartete Domain-Fehler verwenden einen Savepoint
- unerwartete Fehler rollen vollständig zurück
- zwischen Szenarien wird die disposable Datenbank zurückgesetzt

## Geschlossene Fehlerfälle

Festgelegt sind stabile interne Fehlercodes für:

- fehlenden oder falschen Treiber
- falsche Treiberimplementierung
- abgelehntes Gate
- ungültigen Descriptor
- Timeout oder verweigerte Verbindung
- Authentifizierungsfehler
- fehlende disposable Datenbank
- Statement- und Lock-Timeout
- unerwartete Treiberfehler

Rohe Treiberfehler dürfen nicht nach außen gelangen.

## Noch nicht umgesetzt

- keine Dependency-Datei geändert
- kein Treiber installiert
- kein Treiber importiert
- kein Verbindungsadapter
- keine Credential-Auflösung
- keine Datenbankverbindung
- keine Migration oder Testausführung
- keine Frontend-Anbindung

## Automatische Prüfung

`tools/check-supabase-exam-history-disposable-postgresql-driver-selection-contract.py`

Der Prüfer validiert Vertrag, Runtime-Importgrenze,
Dependency-Dateien, fehlende SQL-Migration und fehlende
Frontend-Anbindung.
