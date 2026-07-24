# Disposable PostgreSQL-Test-Manifest-Materialisierung

Stand: v27.32f
Status: isoliert materialisiert, nicht installiert, nicht live

## Ergebnis

Das isolierte Test-Dependency-Manifest wurde erstellt:

`tools/test-dependencies/disposable-postgresql-requirements.txt`

Es enthält exakt:

`psycopg[binary]==3.3.4`

## Integrität

- UTF-8 ohne BOM
- ausschließlich LF-Zeilenende
- exakt eine nichtleere Zeile
- abschließender Zeilenumbruch
- SHA-256 im Materialisierungsvertrag gebunden

## Sicherheitsgrenze

Die Datei wird ausschließlich als spätere lokale
Test-Dependency-Beschreibung vorgehalten.

Nicht umgesetzt:

- keine automatische oder manuelle Installation
- kein Installer
- keine Änderung an Standard-Dependencies
- kein Treiberimport
- keine Runtime- oder Frontend-Nutzung
- keine Datenbankverbindung
- keine SQL-Migration oder Testausführung
