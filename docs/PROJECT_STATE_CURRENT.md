# Aktueller Projektzustand

Stand: v27.36e
Repository: `asarrad-bit/accaoui-34a-lernapp`
Branch: `main`
Letzter abgeschlossener funktionaler Stand: v27.35g
Abschlusscommit: `f5f261fee67fc17c170ee714ae23761ff1668f17`
Aktueller HEAD: DYNAMISCH ZU PRÜFEN
Funktionsstatus: v27.35g abgeschlossen
Weiterer funktionaler Schritt autorisiert: JA
Aktuell autorisierter Task: v27.36e
Aktuelle Taskart: Lokaler Browser-Anbindungsweg der Teilnehmerzugangskette
Aktueller Blocker: KEINER für die ausdrücklich autorisierte spätere v27.36e-Umsetzung; in diesem Autorisierungs-GATE erfolgt noch keine Implementierung

## Autorisierter Task v27.36e

v27.36e ist der einzige autorisierte Task: Browser-Anbindungsweg für die bestehende Teilnehmerzugangskette lokal vorbereiten.
Dieser GATE-Schritt autorisiert nur die spätere Umsetzung und verändert keine Runtime-, App- oder UI-Datei.

Funktionaler Ausgangsstand: v27.35g.
Technischer Ausgangsstand: v27.36d vollständig abgeschlossen.
Stabile Autorisierungsbasis: `1f7d8b0bf6784227b7211d3fb56d714d73c58d4c`.

Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:

- `data/supabase-participant-access-adapter.js`
- `data/supabase-participant-access-bootstrap-bridge.js`
- `data/supabase-participant-access-browser-provider.js`
- `tools/check-participant-access-browser-provider-v2736e.py`
- `docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md`
- `tools/preflight.py`

Der spätere lokale Browser-Anbindungsweg ist verbindlich:

- App -> `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER` -> bestehende v27.36c-Brücke -> v27.36b-Adapter-Factory -> bestehender Supabase-Bootstrap.
- Die CommonJS-Kompatibilität der bestehenden v27.36b- und v27.36c-Module bleibt erhalten; ergänzt werden darf nur eine kleine kontrollierte browserkompatible Exportoberfläche.
- Die kontrollierten Browser-Exports heißen `window.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY` und `window.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY`.
- Keine Fachlogik wird dupliziert. Teilnehmer-, Enrollment-, Kurs- und Zugangsentscheidung bleiben ausschließlich Verantwortung der bestehenden v27.36b-/v27.36c-Kette.
- Der neue Browser-Provider stellt ausschließlich `resolveAccess()` bereit.
- Die Komposition verbindet ausschließlich `window.ACCAOUI_SUPABASE_BOOTSTRAP`, die browserexportierte v27.36b-Factory, die browserexportierte v27.36c-Factory und eine lokale UTC-Zeitquelle.
- `bootstrap.getClient()` wird ausschließlich durch die bestehende Brücke verwendet.
- Fehlende oder ungültige Abhängigkeiten, Throw, Reject und ungültige Ergebnisse bleiben fail-closed; interne Rohfehler werden nicht ausgegeben.

Verboten bleiben `bootstrap.initializeClient()`, `bootstrap.getState()`, `supabase.createClient()`, direkte Auth-/Session-/Tabellenabfragen, frei injizierte `userId`, Netzwerk-, SQL-, Migrations-, RPC-, Config-, SDK-, Live-, Key-, Nutzer- und Teilnehmerdatenzugriffe. `index.html`, `app.js` und `style.css` bleiben unverändert und für v27.36e verboten. Der lokale App-Start bleibt unverändert. Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.

Der spätere Checker arbeitet ausschließlich lokal mit synthetischen Abhängigkeiten. Er muss CommonJS-Kompatibilität, kontrollierte Browser-Exports, die ausschließliche `resolveAccess()`-Oberfläche, die Factory-Komposition, delegierte erlaubte und blockierte Ergebnisse, vollständiges Fail-closed-Verhalten, die verbotenen Aufrufe, unveränderte `index.html`/`app.js`, fehlenden externen Zugriff und weiterhin grüne v27.36b-/v27.36c-Checker prüfen.

Kein anderer Task und kein Folgetask ist ausgewählt oder autorisiert. Commit und Push bleiben NEIN.

### Permanenter v27.36e-Lebenszyklus

Der Lifecycle erkennt dynamisch genau die Phasen `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed`.

GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien. IMPLEMENTATION enthält exakt die sechs autorisierten Implementierungsdateien und ist höchstens einmal zulässig. CLOSURE ist erst nach IMPLEMENTATION zulässig, enthält exakt die fünf Gate-Dateien und setzt `CURRENT_TASK` auf `NONE / BLOCKED / Autorisiert NEIN`. Keine zukünftige GATE-, IMPLEMENTATION- oder CLOSURE-SHA wird hartcodiert. Rückkehr zu einem autorisierten v27.36e-Zustand bleibt nach der Closure ohne neue ausdrückliche Autorisierung blockiert.

## Abgeschlossener technischer Schritt v27.36d

v27.36d abgeschlossen.

Implementierungscommit: `b375dd3fc5fb820174f34a92ebbea81970b3ae29`

Umgesetzte Dateien:

- `app.js`
- `tools/check-participant-access-app-entry-v2736d.py`
- `docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md`
- `tools/preflight.py`

Ergebnis:

- Optionaler App-Provider: `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`.
- Die Schnittstelle bleibt ausschließlich `resolveAccess()`.
- Ohne Provider bleibt der lokale Standardbetrieb unverändert.
- Lokale Auth-Guard-Testzustände behalten Vorrang.
- Nur `allowed=true` zusammen mit `code="access_allowed"` startet die lokale App.
- Providerfehler und ungültige Ergebnisse bleiben fail-closed.
- Nach einem erkannten Providerfehler gibt es keinen lokalen Fallback.
- Ablehnungscodes werden auf die vorhandenen Zugangsansichten abgebildet.
- Unbekannte und technische Fehler bleiben generisch fail-closed.
- In app.js gibt es keine direkten Supabase- oder Datenbankabfragen.
- Bestehender Bootstrap, zentraler Adapter, v27.36b-Teilnehmerzugangs-Adapter und v27.36c-Brücke bleiben unverändert.
- Es besteht keine Browser-Verbindung zu den CommonJS-v27.36b/v27.36c-Modulen.
- Supabase bleibt NICHT LIVE.
- Keine echten Keys.
- Keine echten Teilnehmerdaten.

Testergebnis:

- v27.36d-Checker: PASS (Positiv: 2; Negativ: 36; Manipulation: 10).
- Kontinuitätschecker: PASS.
- Preflight: PASS.
- `git diff --check`: PASS.

Protected-Core:

- Der allgemeine Protected-Core-Schutz bleibt aktiv.
- Die v27.36d-Ausnahme war ausschließlich auf den autorisierten app.js-Scope begrenzt.
- Keine generelle Freigabe von app.js oder anderen Protected-Core-Dateien.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g.
Kein Folgetask wurde ausgewählt oder autorisiert. Die nächste Umsetzung bleibt
vollständig BLOCKED, bis sie ausdrücklich autorisiert wird.

### Permanenter v27.36d-Lebenszyklus

Die stabile Basis `f2f40389a22ea4a40acd7ebdf7ca672add4baf8e` muss Vorfahr
jedes legitimen v27.36d-HEAD bleiben. Der Lifecycle erkennt dynamisch genau die
Phasen `authorization_prepared`, `authorization_committed`,
`implementation_prepared`, `implementation_committed`, `closure_prepared` und
`closure_committed`.

GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien.
IMPLEMENTATION enthält exakt die vier autorisierten Implementierungsdateien und
ist höchstens einmal zulässig. CLOSURE ist erst nach IMPLEMENTATION zulässig,
enthält exakt die fünf Gate-Dateien und setzt `CURRENT_TASK` wieder auf
`NONE / BLOCKED / Autorisiert NEIN`. Keine zukünftige CLOSURE-SHA wird hartcodiert.
Rückkehr zu einem autorisierten v27.36d-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.

## Abgeschlossener isolierter Technikschritt v27.36c

v27.36c abgeschlossen.

Implementierungscommit: `3b1190a21f1b23aa58a1d90c5b41fa4f7e8d93e6`

Implementierungsdateien:

- `data/supabase-participant-access-bootstrap-bridge.js`
- `tools/check-supabase-participant-access-bootstrap-bridge.py`
- `docs/SUPABASE_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_V2736C.md`
- `tools/preflight.py`

Die lokale Teilnehmerzugangs-Brücke ist isoliert umgesetzt. Sie liest
ausschließlich `bootstrap.getClient()`, reicht den vorhandenen Client an die
injizierte Factory des bestehenden v27.36b-Teilnehmerzugangs-Adapters weiter,
verwendet die injizierte UTC-Zeitquelle und delegiert `resolveAccess()`.
Fehlende, werfende oder ungültige Abhängigkeiten und Ergebnisse werden
fail-closed behandelt. Die Fachlogik bleibt vollständig im bestehenden Adapter.

Die Prüfung verwendet ausschließlich einen lokalen synthetischen
Fake-Bootstrap und Fake-Client. Der Bridge-Checker bestätigt 35
Mindestprüfungen und 20 Manipulationsprüfungen, jeweils PASS.

Bootstrap, zentraler Adapter und v27.36b-Teilnehmerzugangs-Adapter bleiben unverändert.
Keine App- oder UI-Integration. Kein Netzwerkzugriff. Kein SQL. Keine
Migrationen. Supabase bleibt NICHT LIVE.
Keine echten Keys.
Keine echten Teilnehmerdaten.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g.
Kein Folgetask wurde ausgewählt oder autorisiert. Die nächste Umsetzung bleibt
vollständig BLOCKED, bis sie ausdrücklich autorisiert wird. Commit und Push
bleiben NEIN.

### Permanenter v27.36c-Lebenszyklus

Die stabile Basis `d28f3710d6f3e4b9abc427dec8589d3ea98c09be` muss Vorfahr
jedes legitimen v27.36c-HEAD bleiben. Der Implementierungscommit wird dynamisch
aus Historie und exakter Dateimenge erkannt. Keine zukünftige Closure-SHA wird hartcodiert.

GATE, exakt eine IMPLEMENTATION, `closure_prepared` und
`closure_committed` werden dynamisch aus Git-Historie, Dateiumfang,
Taskzustand und Working Tree erkannt. Die Closure ändert ausschließlich die
fünf Gate-Dateien.

Rückkehr zu einem autorisierten v27.36c-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.

## Abgeschlossener isolierter Technikschritt v27.36b

v27.36b abgeschlossen.

Implementierungscommit: `c551f1fb973240bfe2a73a26ff38d4e66d2ccff7`

Implementierungsdateien:

- `data/supabase-participant-access-adapter.js`
- `tools/check-supabase-participant-access-adapter.py`
- `docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md`
- `tools/preflight.py`

Der permanente Preflight enthält den Adapter-Checker. Ergebnis: 49
Mindestprüfungen plus 26 Manipulationsprüfungen = 75 PASS.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g.

Die isolierte Komponente verwendet ausschließlich einen explizit injizierten
Supabase-kompatiblen Client und eine explizit injizierte UTC-Zeitquelle.
`session.user.id` ist die einzige Autorität für die Bindung an die
kanonischen Tabellen `participants`, `enrollments` und `courses`.

Der Access-State arbeitet fail-closed bei fehlendem oder ungültigem Client,
fehlender oder ungültiger Session, Queryfehlern, fehlenden, gesperrten,
abgelaufenen, noch nicht aktiven, fremden, mehrdeutigen oder inkonsistenten
Teilnehmer-, Enrollment- oder Kursdaten. Nur ein vollständig konsistenter
gültiger Fall darf minimal nötige kanonische Zugangsmetadaten liefern.

Die Prüfung verwendet ausschließlich einen lokalen synthetischen
In-Memory-Fake-Client.

Keine App-Integration. Kein SDK. Kein realer Client. Kein Netzwerkzugriff.
Kein Datenbankzugriff. Keine SQL-Ausführung. Keine Migrationsausführung.
Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.

Kein Folgetask wurde ausgewählt oder autorisiert. Die nächste Umsetzung
bleibt vollständig BLOCKED, bis sie ausdrücklich autorisiert wird. Commit
und Push bleiben NEIN.

### Permanenter v27.36b-Lebenszyklus

Die stabile Basis `f7672c98a1368dec501416853830ac03e0de2d41` muss Vorfahr
jedes legitimen v27.36b-HEAD bleiben. Der Implementierungscommit wird
dynamisch aus Historie und exakter Dateimenge erkannt. Keine zukünftige
Closure-SHA wird hartcodiert.

Commitrollen werden dynamisch aus Git-Historie, tatsächlicher Dateimenge,
CURRENT_TASK-Zustand und Working Tree abgeleitet. GATE ist eine nichtleere
Teilmenge ausschließlich der fünf Gate-Dateien. IMPLEMENTATION enthält
exakt die vier für v27.36b autorisierten Implementierungsdateien und ist
höchstens einmal zulässig. CLOSURE enthält erst nach gültiger
IMPLEMENTATION ausschließlich Gate-Dateien und den geschlossenen
Taskzustand.

Der Lifecycle erkennt Autorisierungs-GATE, exakt eine IMPLEMENTATION,
lokal vorbereitete CLOSURE und einen späteren CLOSURE-Commit dynamisch. Eine
Rückkehr zu einem autorisierten v27.36b-Zustand bleibt ohne neue
ausdrückliche Autorisierung blockiert.

## Abgeschlossener Dokumentations-/Bestandsaudit v27.36a

v27.36a abgeschlossen.

Audit-Commit: `f545a6c2b14a64a5bcb7bf60a2932315e571ef01`

Audit-Datei: `docs/SUPABASE_LOGIN_CURRENT_STATE_AUDIT_V2736A.md`

Ergebnis: Supabase/Login ist umfangreich lokal vorbereitet, aber NICHT live.

Zentrale Lücken:

- kanonisches Auth-/Teilnehmerzugangsschema
- SDK/öffentliche Dev-Config noch nicht aktiv
- Auth-/Access-Adapter noch nicht an realen Client angebunden
- keine ausgeführten echten RLS-/Datenbanktests

Technische Schulden:

- doppelte Config-Ladewege
- isolierter Bootstrap
- übergroßer zentraler Adapter
- fragmentierte historische Vertrags-/Readiness-Kette

Audit-Empfehlung: lokale injizierbare Auth-/Teilnehmerzugangs-Komponente
mit lokalem Fake-Client.

Diese Audit-Empfehlung ist KEINE Autorisierung.

Kein Folgetask wurde ausgewählt oder autorisiert.

Kein Live-Supabase.

Keine echten Keys.

Keine echten Teilnehmerdaten.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g.

### Permanenter v27.36a-Lebenszyklus

`d69290f9de2921886566b1bb398231bf009fc433` ist die stabile
v27.36a-Autorisierungsbasis und muss Vorfahr jedes legitimen späteren
HEAD bleiben. Eine dauerhafte Gleichheitsforderung des HEAD mit dieser
Basis ist unzulässig; zukünftige Commit-SHAs werden nicht hartcodiert.

Der legitime Autorisierungs-GATE-Commit der Phase 2 wird dynamisch aus
Git-Historie und tatsächlicher Dateimenge erkannt. Sein SHA wird nicht
hartcodiert und ist keine dauerhaft erforderliche HEAD-Gleichheit.

Der Checker leitet den Zustand aus Git-Historie, tatsächlicher
Dateimenge, Taskstatus und Working Tree ab. GATE-Commits enthalten nur
eine nichtleere Teilmenge der fünf Gate-Dateien. Genau ein späterer
IMPLEMENTATION-/AUDIT-Commit darf ausschließlich
`docs/SUPABASE_LOGIN_CURRENT_STATE_AUDIT_V2736A.md` enthalten. CLOSURE-
Commits dürfen erst danach ausschließlich Gate-Dateien enthalten.

Die sechs Phasen sind: lokal vorbereitete Autorisierung; committierte
Autorisierung einschließlich einer lokal vorbereiteten weiteren
Gate-Korrektur; lokal erstellte ungetrackte Audit-Datei; genau einmal
committierter Audit bei weiterhin autorisiertem Task; erst danach lokal
vorbereitete Closure auf `NONE / BLOCKED / Autorisiert NEIN`; sowie
committierte Closure mit sauberem Working Tree. Audit vor
Autorisierung, zweiter Audit-Commit, fremde Dateien, Closure vor Audit
und Rückkehr aus der Closure bleiben gesperrt.

Der Audit ist exakt einmal im dynamisch ermittelten Commit
`f545a6c2b14a64a5bcb7bf60a2932315e571ef01` enthalten. Die lokale
Closure verändert exakt die fünf Gate-Dateien und schließt `CURRENT_TASK`
auf `NONE / BLOCKED / Autorisiert NEIN`. Ein späterer CLOSURE-Commit
wird weiterhin dynamisch erkannt; sein SHA wird nicht hartcodiert.

Nach der Closure bleibt eine Rückkehr zu `v27.36a / AUTHORIZED` ohne
neue ausdrückliche Autorisierung geschlossen blockiert. Kein Folgetask
ist ausgewählt oder autorisiert. Commit und Push bleiben gesperrt.

## Abgeschlossener Dokumentationstask v27.35f

v27.35f abgeschlossen.

Taskart: interne strategische Dokumentation.

Implementierungscommit: `25829727db8c3bafbc13b6e626748fa1f76b174f`

Finale Notiz: `docs/COMPETITOR_POSITIONING_NOTE_V2735F.md`

Finaler Notiz-SHA-256: `983af73fb711cb2b77eb69b51d38ae5f4cf2991d1d976274eee0b4379ef9b023`

Wettbewerbsbeobachtung, Accaoui-Differenzierung und Reaktivierung nach
Lernunterbrechung sind dokumentiert.

Kein App-Code wurde durch v27.35f verändert.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g.

`docs/tasks/CURRENT_TASK.md` steht auf `Task-ID: NONE`,
`Status: BLOCKED`, `Autorisiert: NEIN`, `Titel: Kein Task autorisiert`,
`Erlaubte Dateien: KEINE`; Commit und Push bleiben gesperrt.

Kein Folgetask wurde ausgewählt oder autorisiert.

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
Während der Umsetzung blieb v27.35f der einzige aktive Task; dafür war
ausschließlich `docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` erlaubt.
App-, Funktions-, Fragen-, UI-, Marketingmaterial-, Supabase-, SQL-,
Datenbank- und Netzwerkdateien blieben gesperrt. Commit und Push blieben
verboten; ein Folgetask wurde nicht ausgewählt oder autorisiert.

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

Der erreichte Abschlusszustand dokumentiert „v27.35f abgeschlossen“, den
finalen Notiz-SHA und den dynamisch aus Git ermittelten
Implementierungscommit. Kein zukünftiger Closure-Commit-SHA wird vorab
eingetragen.

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
