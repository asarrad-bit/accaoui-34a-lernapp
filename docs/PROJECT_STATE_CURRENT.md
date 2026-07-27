# Aktueller Projektzustand

Stand: v27.34e
Repository: `asarrad-bit/accaoui-34a-lernapp`
Branch: `main`
Letzter abgeschlossener funktionaler Stand: v27.34b
Letzter direkt bestätigter Vorgänger-Commit: `84729c58c5fcb61b7f7ad72d1d695ee2d7095b86`
Aktueller HEAD: DYNAMISCH ZU PRÜFEN
Funktionsstatus: v27.34b abgeschlossen
Weiterer funktionaler Schritt autorisiert: NEIN
Aktueller Blocker: Auswahl durch Projekteigentümer und verbindlichen Projektchat

## Vertragsklärung v27.34e

Der vollständig gesperrte Verhaltensvertrag für einen späteren ausschließlich lokalen Atomic-Consumption-Registry-Adapter gegen den unveränderten v27.34b-Fake-Treiber wurde in v27.34e abgeschlossen. Factory-Typidentität, Adapterform, defensive Request- und Ergebnis-Kopien, exakte Ergebnisvalidierung, Exception-Mapping, Reconciliation, Timeout-Zuständigkeit, Importgrenze und die Inventur der 28 historischen Sperrchecker sind ohne offene Entscheidung festgelegt.

Der letzte funktionale Stand bleibt v27.34b. Es wurde kein Adapter erstellt, importiert, instanziiert oder aufgerufen. Es ist kein funktionaler Folgeschritt autorisiert.

## Dynamische Prüfung bei jedem Arbeitsbeginn

- Der aktuelle HEAD muss bei jedem Arbeitsbeginn mit Git neu ermittelt werden.
- Der lokale Arbeitsbaum muss sauber oder sein vollständiger erlaubter Änderungsumfang bestätigt sein.
- Der GitHub-Stand von `refs/heads/main` muss direkt geprüft werden.
- Lokaler HEAD und GitHub-HEAD müssen vor Änderungen übereinstimmen.
- Ein zukünftiger oder selbstreferenzieller Commit-SHA darf nicht vorab eingetragen werden.

## Weiterhin verboten

- echter Registry-Adapter
- PostgreSQL
- Datenbank
- SQL
- Supabase und Live-Supabase
- Netzwerk
- `authorizationGrant`
- `authorizationToken`
- `executionGrant`

## Verbindliches Verfahren beim Chatwechsel

1. `docs/PROJECT_STATE_CURRENT.md`, `docs/PROJECT_MASTERLIST.md` und `docs/tasks/CURRENT_TASK.md` vollständig lesen.
2. Lokalen Arbeitsbaum und aktuellen lokalen HEAD direkt mit Git prüfen.
3. GitHub-HEAD für `refs/heads/main` direkt prüfen.
4. Lokalen HEAD, GitHub-HEAD und den erwarteten Ausgangsstand miteinander vergleichen.
5. Bei Abweichung oder Widerspruch sofort STOPP.
6. Nur einen in `docs/tasks/CURRENT_TASK.md` ausdrücklich autorisierten Task und ausschließlich dessen erlaubte Dateien bearbeiten.

## Aktualisierungspflicht nach jedem Versionsabschluss

Nach jedem Versionsabschluss müssen Projektzustand, Masterliste und Task-Steuerung auf Anweisung des Projekteigentümers und des verbindlichen Projektchats aktualisiert werden. Der aktuelle Stand darf keinen zukünftigen Commit-SHA vorwegnehmen. Ohne aktualisierten und ausdrücklich autorisierten `CURRENT_TASK` bleibt jede weitere funktionale Umsetzung gesperrt.
