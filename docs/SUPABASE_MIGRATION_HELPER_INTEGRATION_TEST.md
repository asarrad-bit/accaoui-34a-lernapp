# Accaoui §34a Lern-App – Migration-Helper-Integration

Stand: v27.22c

## Ziel

Die lokale Supabase-Migrationsprüfung ist fest in den Accaoui-Helper integriert.

## Ausführungsreihenfolge

Beim Aufruf von:

`py -3 tools/accaoui-helper.py`

werden ausgeführt:

1. `tools/check-supabase-migrations.py`
2. `tools/preflight.py`
3. `git diff --check`
4. `git status --short`

## Erwartetes Ergebnis

Die Ausgabe enthält:

`Supabase-Migrationsprüfung: OK`

Danach laufen die bisherigen Preflight- und Git-Prüfungen weiter.

## Sicherheitsverhalten

- keine SQL-Migration wird ausgeführt
- keine Supabase-Verbindung wird aufgebaut
- keine Keys werden benötigt
- keine Teilnehmerdaten werden verarbeitet
- bei einem Fehler wird der Helper beendet
- bestehende Preflight-Prüfungen bleiben erhalten

## Bewertung

Die Migrationsstruktur wird jetzt bei jedem normalen Helper-Durchlauf automatisch geprüft.

Status: integriert und lokal geprüft
