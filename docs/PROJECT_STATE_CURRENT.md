# Aktueller Projektzustand

Stand: v27.34f
Repository: `asarrad-bit/accaoui-34a-lernapp`
Branch: `main`
Letzter abgeschlossener funktionaler Stand: v27.34b
Letzter direkt bestätigter Vorgänger-Commit: `a0342fa0d8b2614ad35295c125d6bfdab9eca72c`
Aktueller HEAD: DYNAMISCH ZU PRÜFEN
Funktionsstatus: v27.34b abgeschlossen
Weiterer funktionaler Schritt autorisiert: NEIN
Aktueller Blocker: Auswahl durch Projekteigentümer und verbindlichen Projektchat

## Nichtfunktionale Kontinuitätsbereinigung v27.34f

Die vier verbliebenen Projektkontinuitäts-Widerspruchsgruppen wurden
in v27.34f nichtfunktional korrigiert: Der Cursor-Master-Kontext steht
auf v27.34f und dokumentiert v24.6c als erledigt, eine aktive
Folgetask-Auswahl ist entfernt, die Pflichtlektüre bei einem Chatwechsel
ist vollständig gebunden und die vier aktiven automatischen
`git pull --ff-only`-Vorgaben sind durch direkte Arbeitsbaum-, Branch-,
lokale HEAD- und GitHub-HEAD-Prüfungen mit Abweichungs-STOPP ersetzt.
Synchronisation, Commit und Push benötigen weiterhin eine gesonderte
beziehungsweise ausdrückliche Freigabe.

Der Kontinuitäts-Checker erzwingt die neuen v27.34f-Pflichtaussagen,
blockiert Entfernung und Duplikation, alte aktive Task-Auswahl,
automatische Pull-Vorgaben in den betroffenen aktiven Abschnitten und
unvollständige Pflichtlektüre. Die bestehende AGENTS-, dynamische-HEAD-
und Preflight-Prüfung bleibt erhalten.

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

1. `AGENTS.md`, `docs/PROJECT_STATE_CURRENT.md`, `docs/PROJECT_MASTERLIST.md` und `docs/tasks/CURRENT_TASK.md` vollständig lesen.
2. Lokalen Arbeitsbaum und aktuellen lokalen HEAD direkt mit Git prüfen.
3. GitHub-HEAD für `refs/heads/main` direkt prüfen.
4. Lokalen HEAD, GitHub-HEAD und den erwarteten Ausgangsstand miteinander vergleichen.
5. Bei Abweichung oder Widerspruch sofort STOPP.
6. Synchronisation nur nach gesonderter Freigabe ausführen.
7. Nur einen in `docs/tasks/CURRENT_TASK.md` ausdrücklich autorisierten Task und ausschließlich dessen erlaubte Dateien bearbeiten.

## Aktualisierungspflicht nach jedem Versionsabschluss

Nach jedem Versionsabschluss müssen Projektzustand, Masterliste und Task-Steuerung auf Anweisung des Projekteigentümers und des verbindlichen Projektchats aktualisiert werden. Der aktuelle Stand darf keinen zukünftigen Commit-SHA vorwegnehmen. Ohne aktualisierten und ausdrücklich autorisierten `CURRENT_TASK` bleibt jede weitere funktionale Umsetzung gesperrt.
