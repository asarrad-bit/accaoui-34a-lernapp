# Disposable Harness-Gate-Integration

Stand: v27.32b
Status: implementiert, verbindungsfrei, nicht live ausgeführt

## Ziel

v27.32b integriert Gate-Evaluator und Adapter-Readiness-State aus
v27.32a in den gesperrten Harness-Datenbankmodus.

Bei `--run-database` liest das Harness ausschließlich die sechs
erlaubten Testvariablen, wertet den Descriptor aus, erzeugt den
Adapterstatus und stoppt immer mit Exitcode 2.

Geprüft werden leere Umgebung, gültiger Loopback-Descriptor und
entferntes Ziel. Der Validate-only-Modus bleibt unverändert.

Auch beim gültigen lokalen Descriptor gibt es keinen
Datenbanktreiber, kein DNS, Netzwerk, Socket, Verbindung,
Migration oder Datenbanktest.
