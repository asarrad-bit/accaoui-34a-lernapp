# Disposable Test-Python-Umgebungs-Materialisierungsvertrag

Stand: v27.32i
Status: vollständig gesperrt geplant, nicht ausgeführt

## Ziel

v27.32i beschreibt verbindlich die spätere Erstellung einer
isolierten disposable Python-Testumgebung, ohne sie umzusetzen.

## Vorbedingungen

Erforderlich sind:

- gültiger v27.32h-Descriptor
- Status `descriptor_ready_creation_locked`
- absoluter externer Zielpfad
- Ziel fehlt oder ist leer
- gültiges isoliertes Dependency-Manifest
- ausdrückliche spätere menschliche Freigabe

## Erstellungsgrenze

Die spätere Erstellung darf nur über eine strukturierte
Argumentliste ohne Shell erfolgen:

`{basePythonExecutable} -I -m venv {environmentRoot}`

Die Zielwurzel stammt ausschließlich aus dem geprüften
Descriptor. Bestehende nichtleere Umgebungen dürfen weder
aktualisiert noch geleert werden.

## Nachweise

Nach einer späteren Erstellung müssen unter anderem nachgewiesen
werden:

- Interpreter und `pyvenv.cfg` vorhanden
- `include-system-site-packages = false`
- `sys.prefix` unterscheidet sich von `sys.base_prefix`
- gleiche Python-Major-/Minor-Version wie im Descriptor
- `PYTHONNOUSERSITE=1`
- keine System- oder User-Site-Packages
- Testdependency in dieser Stufe weiterhin nicht installiert

## Rollbackgrenze

Bei späterem Erstellungs- oder Nachweisfehler darf nur der exakte,
nachweislich durch denselben Vorgang neu angelegte Zielpfad
entfernt werden.

Repository, Elternpfade und bereits vorhandene Ziele dürfen nie
gelöscht werden.

## In v27.32i nicht umgesetzt

- kein Materialisierungsplan-Builder
- kein Materialisierer
- keine Dateisystemprüfung oder -änderung
- keine virtuelle Umgebung
- keine Interpreter- oder Installerausführung
- keine Dependency-Installation
- kein Treiberimport
- keine Datenbankverbindung
- keine SQL-Migration oder UI-Anbindung
