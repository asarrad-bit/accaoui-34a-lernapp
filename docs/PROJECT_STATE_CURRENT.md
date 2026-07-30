# Aktueller Projektzustand

Stand: v27.35d
Repository: `asarrad-bit/accaoui-34a-lernapp`
Branch: `main`
Letzter abgeschlossener funktionaler Stand: v27.35d
Abschlusscommit: `b4d2de5002918766bb45fe001cbbfdb333a6d7c5`
Aktueller HEAD: DYNAMISCH ZU PRÜFEN
Funktionsstatus: v27.35d abgeschlossen
Weiterer funktionaler Schritt autorisiert: NEIN
Aktuell autorisierter Task: NONE
Aktueller Blocker: Kein weiterer Task durch CURRENT_TASK autorisiert

## Abgeschlossener funktionaler Stand v27.35d

Lernmodus und Lernkarten sind für Teilnehmer sprachlich und visuell eindeutig unterschieden.

- Lernmodus eindeutig als „Lernmodus – Wissen prüfen“ gekennzeichnet.
- Führungshinweis im Lernmodus: erst selbst beantworten, danach Antwort auswählen und Lösung prüfen.
- Lernkarten eindeutig als „Lernkarten – Wissen selbst einschätzen“ gekennzeichnet.
- Führungshinweis bei Lernkarten: erst selbst erinnern, danach Lösung anzeigen und mit „Gewusst“ beziehungsweise „Nicht gewusst“ einschätzen.
- Gemeinsame kompakte CSS-Klasse `mode-guidance-v2735d` für beide Führungshinweise.
- Keine neue Speicherung, keine neuen Storage-Keys, keine Fragenänderung.
- Keine Supabase-, SQL-, Datenbank- oder Netzwerkänderung.
- Bestehende Navigation, Pause/Fortsetzen und localStorage-Logik unverändert.

Bestätigte Browser- und Prüf-Tests: Dashboard, Lernmodus, Lernkarten, Mobilansicht ca. 390 × 844 ohne horizontalen Überlauf, keine Konsolenfehler, localStorage vollständig restauriert, `node --check app.js`, `git diff --check`, Preflight.

Funktionaler Abschlusscommit von v27.35d: `b4d2de5002918766bb45fe001cbbfdb333a6d7c5`.

Historisch: Der v27.35c-Steuerungscommit `7b0e110d20e97f0bc8487fe6537e0683d9e25940` autorisierte v27.35d ausschließlich für `app.js`, `index.html` und `style.css`. Der nichtfunktionale Checker-Fix `d83869308a277e077b3da6d7e2c1a23001374a48` korrigierte danach den historischen v27.35c-Gate-Check, damit die autorisierte v27.35d-Umsetzung an `app.js` und `style.css` dadurch nicht blockiert wird.

## Historisch: Nichtfunktionale Task-Steuerung v27.35c

Die Projektsteuerung wurde von Task-ID NONE, Status BLOCKED und
Autorisiert NEIN verbindlich auf den einzigen autorisierten Folgetask
v27.35d umgestellt. Der letzte abgeschlossene funktionale Stand blieb
zu diesem Zeitpunkt unverändert v27.35b.

`docs/tasks/CURRENT_TASK.md` stand während v27.35c auf `Task-ID: v27.35d`,
`Status: AUTHORIZED`, `Autorisiert: JA`,
`Funktionaler Ausgangsstand: v27.35b`,
`Erwarteter Ausgangscommit: e4b6929af552e4245290d3eb5db97815365162e6`,
`Erlaubte Dateien: app.js, index.html, style.css`,
`Commit erlaubt: NEIN` und `Push erlaubt: NEIN`.

Der Kontinuitäts-Checker erzwang diese v27.35c-Pflichtaussagen und
blockierte in seiner Manipulationsmatrix mindestens: eine falsche
Task-ID, einen falschen Status, Autorisiert NEIN, einen anderen
funktionalen Ausgangsstand, einen anderen Ausgangscommit, zusätzliche
oder andere erlaubte Dateien, Commit erlaubt JA, Push erlaubt JA und
die automatische Auswahl eines weiteren Tasks. Zusätzlich prüfte der
Checker direkt über Git, dass `app.js`, `index.html` und `style.css`
während v27.35c gegenüber dem Ausgangscommit unverändert blieben.

In v27.35c wurde ausschließlich Projektsteuerungsdokumentation
geändert. Es wurde keine App-, Funktions-, Vertrags-, Adapter-,
Datenbank-, Supabase-, Fragen-, UI- oder Migrationsdatei verändert.
Der funktionale Folgeschritt v27.35d wurde erst danach umgesetzt und
ist oben als eigener abgeschlossener Abschnitt dokumentiert.

## Abgeschlossener funktionaler Stand v27.35b

Dashboard „Ihr nächster Lernschritt“ ist abgeschlossen. Das Dashboard
zeigt genau einen nächsten Lernschritt.

Priorität:

1. neueste gültige aktive Sitzung
2. Fehlerfragen
3. schwächstes ausreichend belegtes Sachgebiet
4. unbekannte Lernkarten
5. neue Prüfung

Ausschließlich vorhandene localStorage-Daten werden defensiv gelesen.
Es gibt keine neue Speicherung und keine neuen Storage-Keys.
Ungültige Sitzungen und Statistikwerte werden ignoriert.

Prüfung, Lerneinheit und Lernkarten wurden im Browser bestätigt.
Automatisierte Browserprüfung: 6/6 bestanden.
Der v27.35b-Abschlusscommit lautet `f168b96ff26c88e5baca212902081932b8986e85`.

Historischer Zwischenstand vor diesem Abschluss enthielt noch die Aussage
„Letzter abgeschlossener funktionaler Stand: v27.34b“.

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
