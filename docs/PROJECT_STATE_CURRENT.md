# Aktueller Projektzustand

Stand: v27.35g
Repository: `asarrad-bit/accaoui-34a-lernapp`
Branch: `main`
Letzter abgeschlossener funktionaler Stand: v27.35g
Abschlusscommit: `f5f261fee67fc17c170ee714ae23761ff1668f17`
Aktueller HEAD: DYNAMISCH ZU PRÜFEN
Funktionsstatus: v27.35g abgeschlossen
Weiterer funktionaler Schritt autorisiert: NEIN
Aktuell autorisierter Task: v27.35f
Aktuelle Taskart: Dokumentation
Aktueller Blocker: KEINER; v27.35f ist als einziger Dokumentationstask autorisiert, Umsetzung offen

## Autorisierter Dokumentationstask v27.35f

`docs/tasks/CURRENT_TASK.md` steht auf `Task-ID: v27.35f`,
`Status: AUTHORIZED`, `Autorisiert: JA`,
`Titel: Wettbewerbsbeobachtung und Accaoui-Positionierung dokumentieren`,
`Funktionaler Ausgangsstand: v27.35g`, funktionaler Ausgangs- und
Vorautorisierungsstand
`003112eaeb9a071a6396634b6da92fa11ae8921a`, v27.35f-Autorisierungscommit
und Umsetzungsbasis
`601dc6f751b6a603a27c4b3405150bf1d75e09fd`, ausschließlich erlaubte Datei
für die Umsetzung
`docs/COMPETITOR_POSITIONING_NOTE_V2735F.md`,
`Commit erlaubt: NEIN` und `Push erlaubt: NEIN`.

v27.35g bleibt der letzte abgeschlossene funktionale Stand. v27.35f ist
der einzige autorisierte Dokumentationstask; seine Umsetzung ist offen.
Die spätere Notiz muss beobachtete, nicht extern verifizierte
Wettbewerber-Werbeaussagen klar von Bewertung und eigener
Accaoui-Empfehlung trennen. Die Leitidee und der Qualitätsmaßstab
„Mit dieser App habe ich es endlich verstanden.“ bleiben verbindlich.

Im abgeschlossenen Autorisierungsschritt wurde
`docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` noch nicht erstellt oder
verändert. In diesem Schritt wurde keine Wettbewerbsnotiz erstellt,
keine App-Datei verändert und kein Folgetask automatisch ausgewählt.
Commit und Push blieben gesperrt.

### Separater nichtfunktionaler v27.35f-Implementierungs-Gate-Korrekturschritt

Der Commit `003112eaeb9a071a6396634b6da92fa11ae8921a` bleibt der funktionale
Ausgangs- und Vorautorisierungsstand. Der historische
v27.35f-Autorisierungscommit
`601dc6f751b6a603a27c4b3405150bf1d75e09fd` ist die verbindliche
Umsetzungsbasis. Der Commit
`d4e46edc48e967509e09ddd1096b54eb0bed5971` ist ein legitimer
nichtfunktionaler v27.35f-Gate-Fix-Commit; zwischen der Umsetzungsbasis
und diesem Commit wurden ausschließlich die vier Steuerungsdokumente
und `tools/check-project-continuity-control.py` verändert.

Der ursprüngliche Checkerfehler war eine starre Gleichheitsprüfung auf
`HEAD == 601dc6f751b6a603a27c4b3405150bf1d75e09fd`. Dadurch wurde der
legitime Gate-Fix-Commit `d4e46edc48e967509e09ddd1096b54eb0bed5971`
nach seinem Commit fälschlich blockiert. Der Checker verlangt deshalb
künftig die Autorisierungsbasis als Vorfahren des aktuellen HEAD und
begrenzt den gesamten committeten Diff von dieser Basis bis HEAD auf die
fünf Gate-Dateien. Der aktuelle HEAD darf ein späterer legitimer
Gate-Commit sein; ein zukünftiger Commit-SHA wird nicht vorweggenommen.

Der frühere SHA-256
`cff217d2b8cd0e9c50c3c1a351ff3de8ee595f0e3c59ed0def0ae1a3f8a799f7`
gehört zur Notizfassung vor der autorisierten Ergänzung „Reaktivierung
nach Lernunterbrechung“. Der aktuelle finale v27.35f-Notiz-Snapshot hat
SHA-256
`983af73fb711cb2b77eb69b51d38ae5f4cf2991d1d976274eee0b4379ef9b023`
und bleibt während dieses getrennten Gate-Korrekturschritts unverändert.
Der Working Tree darf entweder exakt die fünf modifizierten Gate-Dateien
und die ungetrackte Notiz oder nach einem legitimen Gate-Commit nur die
ungetrackte Notiz enthalten. Der Gate-Korrekturschritt betrifft
ausschließlich die vier Steuerungsdokumente und
`tools/check-project-continuity-control.py`.
v27.35f bleibt der einzige aktive Task; für seine Umsetzung bleibt
ausschließlich `docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` erlaubt.
App-, Funktions-, Fragen-, UI-, Marketingmaterial-, Supabase-, SQL-,
Datenbank- und Netzwerkdateien bleiben gesperrt. Commit und Push bleiben
verboten; ein Folgetask wird nicht ausgewählt oder autorisiert.

### Verbindliche v27.35f-Lebenszyklus-State-Machine

Der Kontinuitäts-Checker klassifiziert jeden Commit nach der
Autorisierungsbasis
`601dc6f751b6a603a27c4b3405150bf1d75e09fd` dynamisch aus seiner
tatsächlichen Dateimenge. Nicht leere Commitmengen ausschließlich aus
den fünf Gate-Dateien sind GATE- beziehungsweise nach der Implementation
CLOSURE-Commits. Exakt die Wettbewerbsnotiz ist höchstens einmal als
IMPLEMENTATION-Commit zulässig; ihr Blob muss SHA-256
`983af73fb711cb2b77eb69b51d38ae5f4cf2991d1d976274eee0b4379ef9b023`
haben. Andere Commitmengen bleiben gesperrt.

Die State-Machine akzeptiert vier Zustände: vor Implementation mit
autorisiertem v27.35f und ungetrackter finaler Notiz; nach dem einmaligen
Implementation-Commit weiterhin mit autorisiertem v27.35f und sauberem
Working Tree; lokal vorbereitete Closure mit exakt fünf Gate-Dateien und
`CURRENT_TASK` auf `NONE / BLOCKED / Autorisiert NEIN`; sowie die
committete Closure mit abgeschlossenem Task und sauberem Working Tree.
Closure ist erst nach dynamischem Nachweis des Implementation-Commits
zulässig. Nach einer Closure bleibt jede Rückkehr zu v27.35f ohne neue
Autorisierung gesperrt.

Der spätere Abschlusszustand dokumentiert „v27.35f abgeschlossen“, den
finalen Notiz-SHA, den dynamisch aus Git ermittelten
`Implementierungscommit: <SHA>` und „Kein Folgetask wurde ausgewählt oder
autorisiert.“ Kein zukünftiger Implementation- oder Closure-Commit-SHA
wird vorab eingetragen.

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

Zum damaligen Zeitpunkt blieb `v27.35f` ausschließlich für die später vorgemerkte Wettbewerbsbeobachtungsnotiz reserviert und war noch nicht autorisiert.

Der funktionale Stand bleibt v27.35d, bis v27.35g abgeschlossen ist. Kein Folgeschritt nach v27.35g ist ausgewählt oder autorisiert.

### Nichtfunktionaler v27.35g-Implementierungs-Gate-Korrekturschritt

Getrennt von der eigentlichen v27.35g-Umsetzung wurde ausschließlich `tools/check-project-continuity-control.py` um einen nichtfunktionalen Gate-Korrekturschritt ergänzt; diese Checker-Datei gehört ausschließlich zu diesem getrennten Korrekturschritt. v27.35g blieb damals weiterhin der einzige aktive Task, Status und Autorisierung blieben unverändert bestehen, und der funktionale Ausgangsstand blieb unverändert v27.35d. Der Gate-Korrekturschritt ließ im Arbeitsbaum ausschließlich `app.js` und `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md` zu; `index.html`, `style.css`, `questions.json` und alle anderen Dateien blieben vollständig gesperrt. Die Punkteberechnung in `app.js` und der Testbericht `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md` waren bereits lokal umgesetzt und wurden während dieses Gate-Schritts nicht verändert. Ein Commit und ein Push der funktionalen Umsetzung blieben gesperrt. Damals wurde kein Folgetask ausgewählt; `v27.35f` war noch nicht autorisiert.

## Abgeschlossener funktionaler Stand v27.35g

Die Punkteberechnung der schriftlichen Prüfung wurde korrigiert: eine vollständig richtige Antwort ergibt stets die volle hinterlegte Punktzahl; eine zulässige Teilantwort bei einer Zwei-Punkte-Frage mit mindestens zwei richtigen Optionen ergibt exakt 1 Punkt; jede falsch ausgewählte Option ergibt 0 Punkte.

Bestätigte Ergebnisse: 82 Fragen, 120 Maximalpunkte; alle 13 zuvor betroffenen Fragen (`straf_009`, `bgb_009`, `waffen_004`, `straf_004`, `v23_roso_007`, `technik_004`, `straf_006`, `bgb_012`, `bgb_004`, `straf_013`, `bgb_006`, `uvv_004`, `uvv_008`) liefern jeweils exakt 2/2 Punkte; die im v27.35e-Bericht verwendete Testkonstellation ergibt jetzt exakt 114/120 statt vormals 101/120; alle 82 Fragen vollständig richtig ergeben jetzt exakt 120/120; Pause/Fortsetzen PASS; Fehleranalyse PASS; Fehlertraining PASS; Desktop PASS; Mobil ca. 390 × 844 PASS; keine neuen Konsolenfehler; `localStorage` und `sessionStorage` nach den Tests vollständig restauriert.

Testbericht: `docs/WRITTEN_EXAM_SCORING_FIX_V2735G.md`. Funktionaler Abschlusscommit: `f5f261fee67fc17c170ee714ae23761ff1668f17`.

Vor der funktionalen Umsetzung wurde ein getrennter, nichtfunktionaler Implementierungs-Gate-Korrekturschritt (Commit `bbe5f6ea5366e026327c3fc0c866e1ef37ead6f0`) durchgeführt; siehe Abschnitt „Nichtfunktionaler v27.35g-Implementierungs-Gate-Korrekturschritt“ oben.

Der bestehende v27.35e-FAIL-Bericht `docs/WRITTEN_EXAM_REGRESSION_V2735E.md` bleibt unverändert als historische Fehlerdokumentation erhalten.

Unmittelbar nach dem Abschluss von v27.35g blieb `v27.35f` noch für
die spätere Wettbewerbsbeobachtungsnotiz vorgemerkt und nicht
autorisiert. Der aktuelle Autorisierungsschritt oben ersetzt diesen
damaligen Sperrzustand ausschließlich für den Dokumentationstask
v27.35f. Ein funktionaler oder sonstiger Folgetask wird nicht
automatisch ausgewählt oder abgeleitet.

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
