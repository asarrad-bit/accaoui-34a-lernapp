# Disposable Test-Python-Umgebungsdescriptor-Resolver

Stand: v27.32h
Status: rein implementiert, Erstellung gesperrt, nicht live

## Ziel

v27.32h ergänzt einen deterministischen Resolver für einen
späteren isolierten Test-Python-Umgebungsdescriptor.

## Eingabe

Der Resolver akzeptiert ausschließlich ein übergebenes Mapping
mit:

- Plattform
- absoluter Umgebungswurzel
- absoluter Repositorywurzel
- Wurzelart `dedicated_external`
- aufrufender und angeforderter Pythonversion
- vollständigen Isolationsfakten

Unbekannte oder fehlende Felder werden geschlossen abgelehnt.

## Prüfung

Der Resolver prüft rein lexikalisch:

- Windows- oder POSIX-Pfadform
- absolute Pfade
- keine Umgebung im Repository
- Python 3.10 bis 3.14
- exakt gleiche angeforderte und aufrufende Pythonversion
- keine System- oder User-Site-Packages
- `PYTHONNOUSERSITE` verpflichtend
- keine Vererbung von `PYTHONPATH` oder `VIRTUAL_ENV`

## Erfolgszustand

Ein gültiger Fall ergibt nur:

`descriptor_ready_creation_locked`

mit:

`test_environment_descriptor_ready_creation_locked`

Der Descriptor enthält den plattformspezifischen späteren
Interpreterpfad und die gebundene isolierte Manifestdependency.

## Sicherheitsgrenze

- kein Prozessumgebungslesen
- kein Dateisystemlesen oder -schreiben
- keine Pfadauflösung gegen das echte Dateisystem
- keine Umgebungserstellung
- keine Interpreter- oder Installerausführung
- kein Treiberimport
- keine Datenbankverbindung
- keine SQL-Migration oder UI-Anbindung
