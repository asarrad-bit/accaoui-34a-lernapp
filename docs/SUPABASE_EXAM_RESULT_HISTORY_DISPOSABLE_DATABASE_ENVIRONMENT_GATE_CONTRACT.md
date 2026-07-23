# Disposable Datenbank-Umgebungs-Gate-Vertrag

Stand: v27.31z
Status: vollständig gesperrt vorbereitet, nicht live ausgeführt

## Ziel

Dieser Vertrag legt die spätere Grenze zwischen einer ausdrücklich
erlaubten lokalen disposable Testdatenbank und jedem unbekannten,
entfernten oder produktiven Ziel fest.

v27.31z implementiert noch kein Gate und keinen
Datenbank-Verbindungsadapter.

## Pflichtumgebung

Später müssen alle folgenden Werte gleichzeitig vorhanden sein:

- `ACCAOUI_DB_TEST_MODE=disposable`
- `ACCAOUI_DB_TEST_TARGET_KIND=local_postgres`
- `ACCAOUI_DB_TEST_HOST`
- `ACCAOUI_DB_TEST_PORT`
- `ACCAOUI_DB_TEST_DATABASE`
- `ACCAOUI_DB_TEST_CONFIRM=DESTROY_SYNTHETIC_TEST_DATA`

Fehlende oder unbekannte Angaben werden immer abgelehnt.

## Erlaubte Zielklasse

Zulässig vorbereitet sind ausschließlich Loopback-Ziele:

- `127.0.0.1`
- `localhost`
- `::1`

Der Datenbankname muss exakt lauten:

`accaoui_exam_history_disposable_test`

Der Port muss eine Ganzzahl zwischen 1024 und 65535 sein.

Es erfolgen keine DNS- oder IP-Auflösungen.

## Verbotene Ziele

Abgelehnt werden insbesondere:

- entfernte Hostnamen und IP-Adressen
- Supabase-, AWS-, Azure- und Google-Cloud-Ziele
- unbekannte Zielklassen
- Produktions- oder Live-Bezeichnungen
- Standarddatenbanken wie `postgres`
- `template0` und `template1`
- URL- oder Connection-String-Eingaben
- unvollständige oder falsch bestätigte Umgebungen

## Entscheidungsmatrix

Auch ein vollständig gültiger lokaler Descriptor erhält in
v27.31z nur:

`eligible_but_connection_locked`

Der Grund bleibt:

`adapter_not_implemented`

Es wird keine Verbindung geöffnet.

## Spätere Adaptergrenze

Der spätere Verbindungsadapter darf ausschließlich einen bereits
validierten Gate-Descriptor erhalten.

Er darf nicht:

- rohe Umgebungsvariablen selbst interpretieren
- URL oder Connection-String annehmen
- Passwort, Service-Role-Key oder Produktionssecret annehmen
- DNS auflösen
- Socket öffnen
- Datenbanktreiber importieren
- Migrationen oder Tests ausführen
- eine Verbindung zurückgeben

Die Standardentscheidung bleibt `deny`.

## Sicherheitsgrenze

Ausgeschlossen bleiben:

- echte Teilnehmerdaten
- echte Namen und E-Mail-Adressen
- Produktionsgeheimnisse
- Datenbank-URLs
- Netzwerkzugriff
- Frontend-Referenzen
- clientseitig wählbare Ziele oder Fehlerinjektion

## Automatische Prüfung

`tools/check-supabase-exam-history-disposable-database-environment-gate-contract.py`

Der Prüfer kontrolliert:

1. Vertrag und Entscheidungsmatrix
2. Loopback- und Datenbanknamengrenze
3. geschlossenen Adaptervertrag
4. weiterhin verbindungsfreies v27.31y-Harness
5. fehlenden Datenbanktreiber und Netzwerkcode
6. fehlende SQL-Migration und Frontend-Referenz

Der Prüfer ist dauerhaft in `tools/preflight.py` eingebunden.

## Noch offen

- tatsächlicher Gate-Evaluator
- Verbindungsadapter-Readiness-State
- Auswahl eines Testdatenbanktreibers
- Datenbankverbindung und Testausführung
- testseitige Fehlerinjektion
- Konkurrenz- und Autorisierungstestläufe
- direkte App-Freigabe
- UI-Anbindung
