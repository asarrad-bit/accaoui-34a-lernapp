# Aktueller Projektzustand

Stand: v27.35g
Repository: `asarrad-bit/accaoui-34a-lernapp`
Branch: `main`
Letzter abgeschlossener funktionaler Stand: v27.35d
Abschlusscommit: `b4d2de5002918766bb45fe001cbbfdb333a6d7c5`
Aktueller HEAD: DYNAMISCH ZU PRÜFEN
Funktionsstatus: v27.35d abgeschlossen
Weiterer funktionaler Schritt autorisiert: JA
Aktuell autorisierter Task: v27.35g
Aktueller Blocker: KEINER für v27.35g; jeder weitere Schritt bleibt gesperrt

## Abgeschlossener Regressionstest v27.35e (FAIL)

`docs/tasks/CURRENT_TASK.md` stand auf `Task-ID: v27.35e`, `Status: AUTHORIZED`, `Autorisiert: JA`, funktionaler Ausgangsstand v27.35d, erwarteter Ausgangscommit `260e6527208769f18018d1db6e6e3b7fbe9d7d7e`, erlaubte Datei `docs/WRITTEN_EXAM_REGRESSION_V2735E.md`, `Commit erlaubt: NEIN`, `Push erlaubt: NEIN`.

Der Regressionstest der schriftlichen Prüfung nach v27.35d wurde vollständig durchgeführt und mit Gesamtergebnis FAIL abgeschlossen. Testbericht-Commit: `db2f12a1af7792c59e9e6411bb127b2f68401713`.

Ursache der Regression: Bei Zwei-Punkte-Fragen mit nur einer richtigen Antwortoption wurde bei vollständig korrekter Beantwortung nur 1 statt 2 Punkte vergeben. Betroffene Fragen-IDs im getesteten Kernfragenpool: `straf_009`, `bgb_009`, `waffen_004`, `straf_004`, `v23_roso_007`, `technik_004`, `straf_006`, `bgb_012`, `bgb_004`, `straf_013`, `bgb_006`, `uvv_004`, `uvv_008`.

Es wurde in v27.35e keine Codekorrektur vorgenommen, kein Commit und kein Push ausgeführt. Der Testbericht `docs/WRITTEN_EXAM_REGRESSION_V2735E.md` bleibt unverändert.

## Autorisierter Task v27.35g

`docs/tasks/CURRENT_TASK.md` steht auf `Task-ID: v27.35g`, `Status: AUTHORIZED`, `Autorisiert: JA`, `Titel: Punkteberechnung schriftliche Prüfung korrigieren`, funktionaler Ausgangsstand v27.35d, erwarteter Ausgangscommit `db2f12a1af7792c59e9e6411bb127b2f68401713`, für die spätere Umsetzung ausschließlich erlaubte Dateien `app.js` und `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md`, `Commit erlaubt: NEIN`, `Push erlaubt: NEIN`.

Ziel von v27.35g: Die Punkteberechnung der schriftlichen Prüfung so korrigieren, dass vollständig korrekt beantwortete Fragen stets ihre volle hinterlegte Punktzahl ergeben.

Verbindlicher Bewertungsvertrag: keine Antwort ergibt 0 Punkte; die ausgewählte Antwortmenge entspricht exakt der vollständigen richtigen Antwortmenge und ergibt die volle hinterlegte Fragepunktzahl; bei einer Zwei-Punkte-Frage mit mindestens zwei richtigen Optionen ergibt eine nicht leere echte Teilmenge ausschließlich richtiger Optionen ohne falsch ausgewählte Option exakt 1 Punkt; eine falsch ausgewählte Option oder eine sonstige nicht vollständig beziehungsweise nicht zulässig teilrichtige Kombination ergibt 0 Punkte; eine Zwei-Punkte-Frage mit nur einer richtigen Antwort ergibt vollständig richtig exakt 2 Punkte; eine Ein-Punkt-Frage ergibt nur vollständig richtig 1 Punkt, sonst 0.

In diesem Steuerungsschritt wird `app.js` noch nicht verändert; die Korrektur erfolgt erst in der später autorisierten Umsetzung. Der bestehende Testbericht `docs/WRITTEN_EXAM_REGRESSION_V2735E.md` darf dabei nicht verändert werden.

`v27.35f` bleibt ausschließlich für die später vorgemerkte Wettbewerbsbeobachtungsnotiz reserviert. `v27.35f` ist nicht autorisiert und wird jetzt nicht bearbeitet.

Der funktionale Stand bleibt v27.35d, bis v27.35g abgeschlossen ist. Kein Folgeschritt nach v27.35g ist ausgewählt oder autorisiert.

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
