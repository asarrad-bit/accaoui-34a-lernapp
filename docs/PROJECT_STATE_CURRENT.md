# Aktueller Projektzustand

Stand: v27.35a
Repository: `asarrad-bit/accaoui-34a-lernapp`
Branch: `main`
Letzter abgeschlossener funktionaler Stand: v27.34b
Letzter direkt bestätigter Vorgänger-Commit: `62947209611c17b5a700fb78cfcfa785f055b2f3`
Aktueller HEAD: DYNAMISCH ZU PRÜFEN
Funktionsstatus: v27.34b abgeschlossen
Weiterer funktionaler Schritt autorisiert: JA
Aktuell autorisierter Task: v27.35b
Aktueller Blocker: KEINER für v27.35b; jeder weitere Schritt bleibt gesperrt

## Nichtfunktionale Task-Steuerung v27.35a

Die Projektsteuerung wurde von Task-ID NONE, Status BLOCKED und
Autorisiert NEIN (Stand v27.34f) verbindlich auf den einzigen
autorisierten Folgetask v27.35b umgestellt. Der letzte abgeschlossene
funktionale Stand bleibt unverändert v27.34b.

`docs/tasks/CURRENT_TASK.md` steht jetzt auf `Task-ID: v27.35b`,
`Status: AUTHORIZED`, `Autorisiert: JA`,
`Erwarteter Ausgangscommit: 62947209611c17b5a700fb78cfcfa785f055b2f3`,
`Erlaubte Dateien: app.js`, `Commit erlaubt: NEIN` und
`Push erlaubt: NEIN`.

Der Kontinuitäts-Checker erzwingt diese v27.35a-Pflichtaussagen und
blockiert in seiner Manipulationsmatrix mindestens: eine falsche
Task-ID, einen falschen Status, Autorisiert NEIN, einen anderen
funktionalen Ausgangsstand, einen anderen Ausgangscommit, zusätzliche
oder andere erlaubte Dateien, Commit erlaubt JA, Push erlaubt JA und
die automatische Auswahl eines weiteren Tasks. Zusätzlich prüft der
Checker direkt über Git, dass app.js während v27.35a unverändert
bleibt.

In v27.35a wurde ausschließlich Projektsteuerungsdokumentation
geändert: `docs/PROJECT_STATE_CURRENT.md`, `docs/PROJECT_MASTERLIST.md`,
`docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`, `docs/tasks/CURRENT_TASK.md`
und `tools/check-project-continuity-control.py`. app.js wurde in
v27.35a nicht verändert. Es wurde keine App-, Funktions-, Vertrags-,
Adapter-, Datenbank-, Supabase-, Fragen-, UI- oder Migrationsdatei
verändert. Der funktionale Folgeschritt v27.35b selbst ist noch nicht
umgesetzt.

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

1. `AGENTS.md`, `docs/PROJECT_STATE_CURRENT.md`, `docs/PROJECT_MASTERLIST.md` und `docs/tasks/CURRENT_TASK.md` vollständig lesen.
2. Lokalen Arbeitsbaum und aktuellen lokalen HEAD direkt mit Git prüfen.
3. GitHub-HEAD für `refs/heads/main` direkt prüfen.
4. Lokalen HEAD, GitHub-HEAD und den erwarteten Ausgangsstand miteinander vergleichen.
5. Bei Abweichung oder Widerspruch sofort STOPP.
6. Synchronisation nur nach gesonderter Freigabe ausführen.
7. Nur einen in `docs/tasks/CURRENT_TASK.md` ausdrücklich autorisierten Task und ausschließlich dessen erlaubte Dateien bearbeiten.

## Aktualisierungspflicht nach jedem Versionsabschluss

Nach jedem Versionsabschluss müssen Projektzustand, Masterliste und Task-Steuerung auf Anweisung des Projekteigentümers und des verbindlichen Projektchats aktualisiert werden. Der aktuelle Stand darf keinen zukünftigen Commit-SHA vorwegnehmen. Ohne aktualisierten und ausdrücklich autorisierten `CURRENT_TASK` bleibt jede weitere funktionale Umsetzung gesperrt.
