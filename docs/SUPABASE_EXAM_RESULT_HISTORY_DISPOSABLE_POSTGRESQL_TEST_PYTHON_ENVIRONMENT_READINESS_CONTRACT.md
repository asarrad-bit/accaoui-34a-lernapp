# Disposable PostgreSQL-Test-Python-Umgebungsvertrag

Stand: v27.32g
Status: Readiness geplant, nicht erstellt, nicht live

## Ziel

v27.32g legt ausschließlich die Grenzen für eine spätere
getrennte Python-Testumgebung fest.

## Umgebungswurzel

Die spätere Umgebung darf nur über die ausdrücklich gesetzte
Variable

`ACCAOUI_DISPOSABLE_TEST_ENV_ROOT`

bestimmt werden.

Es gibt keinen Standardpfad. Der Pfad muss absolut, außerhalb des
Repositories und außerhalb von System-, Global- und
User-Site-Packages liegen.

## Interpreter

Die spätere Umgebung ist vom Typ `python_venv`.

Erlaubt sind:

- Python 3.10 bis 3.14
- gleiche Major-/Minor-Version wie der aufrufende Interpreter
- Windows: `Scripts/python.exe`
- POSIX: `bin/python`
- spätere direkte Interpreterausführung ohne Shell-Aktivierung

## Isolation

- kein System-Site-Packages
- kein User-Site-Packages
- später `PYTHONNOUSERSITE=1`
- kein geerbtes `PYTHONPATH`
- kein geerbtes `VIRTUAL_ENV`
- keine Produktiv-, Frontend- oder App-Start-Nutzung
- keine automatische Erstellung, Aktivierung oder Installation

## In v27.32g nicht umgesetzt

- kein Pfad-Resolver
- keine virtuelle Umgebung
- keine Interpreterausführung
- keine Dependency-Installation
- kein Treiberimport
- keine Datenbankverbindung
- keine SQL-Migration oder UI-Anbindung
