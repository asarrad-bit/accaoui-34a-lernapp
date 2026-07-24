# Disposable PostgreSQL-Test-Dependency-Manifest-Vertrag

Stand: v27.32e
Status: isoliert geplant, noch nicht materialisiert, nicht live

## Ziel

v27.32e legt verbindlich fest, wie die spätere
PostgreSQL-Testdependency vom Produktiv- und Frontendbetrieb
getrennt werden muss.

## Zukünftiger Manifestpfad

`tools/test-dependencies/disposable-postgresql-requirements.txt`

Der Pfad ist ausschließlich für lokale disposable
Datenbanktests vorgesehen.

## Erlaubter Inhalt

Das spätere Manifest darf genau eine direkte Dependency enthalten:

`psycopg[binary]==3.3.4`

Nicht erlaubt sind weitere Dependencies, offene Versionsbereiche,
URL-, VCS-, lokale Pfad- oder Editable-Abhängigkeiten.

## Strikte Isolation

Die Dependency darf weder im Produktivbetrieb noch im Browser,
Frontend-Bundle, Anwendungsstart, Standard-Preflight oder in
Standard-/Projekt-/Lock-Dependency-Dateien erscheinen.

Eine spätere Installation erfordert eine getrennte Testumgebung,
eine bewusste menschliche Aktion und einen separaten
freigegebenen Umsetzungsschritt.

## In v27.32e nicht umgesetzt

- Manifestdatei noch nicht erstellt
- keine Dependency deklariert
- kein Installationsbefehl
- keine virtuelle Umgebung verändert
- kein Netzwerkdownload
- kein Treiberimport
- keine Datenbankverbindung
- keine SQL-Migration oder UI-Anbindung
