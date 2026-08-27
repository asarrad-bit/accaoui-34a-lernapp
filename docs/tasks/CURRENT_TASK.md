# Verbindlicher aktueller Task

Task-ID: v27.36e
Status: AUTHORIZED
Autorisiert: JA
Titel: Browser-Anbindungsweg für die bestehende Teilnehmerzugangskette lokal vorbereiten
Funktionaler Ausgangsstand: v27.35g
Technischer Ausgangsstand: v27.36d vollständig abgeschlossen
Stabile Autorisierungsbasis: `1f7d8b0bf6784227b7211d3fb56d714d73c58d4c`
Erlaubte Implementierungsdateien: `data/supabase-participant-access-adapter.js`, `data/supabase-participant-access-bootstrap-bridge.js`, `data/supabase-participant-access-browser-provider.js`, `tools/check-participant-access-browser-provider-v2736e.py`, `docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md`, `tools/preflight.py`
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Autorisierter Task v27.36e

v27.36e ist der einzige autorisierte Task: Browser-Anbindungsweg für die bestehende Teilnehmerzugangskette lokal vorbereiten.
Dieser GATE-Schritt autorisiert nur die spätere Umsetzung und verändert keine Runtime-, App- oder UI-Datei.

Unverändert gilt „Funktionaler Ausgangsstand: v27.35g.“
Unverändert gilt „Technischer Ausgangsstand: v27.36d vollständig abgeschlossen.“
Unverändert gilt „Stabile Autorisierungsbasis: `1f7d8b0bf6784227b7211d3fb56d714d73c58d4c`.“

Für die spätere IMPLEMENTATION sind exakt sechs Dateien erlaubt:

- `data/supabase-participant-access-adapter.js`
- `data/supabase-participant-access-bootstrap-bridge.js`
- `data/supabase-participant-access-browser-provider.js`
- `tools/check-participant-access-browser-provider-v2736e.py`
- `docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md`
- `tools/preflight.py`

### Verbindliches Funktionsziel

- App -> `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER` -> bestehende v27.36c-Brücke -> v27.36b-Adapter-Factory -> bestehender Supabase-Bootstrap.
- Die CommonJS-Kompatibilität der bestehenden v27.36b- und v27.36c-Module bleibt erhalten; ergänzt werden darf nur eine kleine kontrollierte browserkompatible Exportoberfläche.
- Die kontrollierten Browser-Exports heißen `window.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY` und `window.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY`.
- Keine Fachlogik wird dupliziert. Teilnehmer-, Enrollment-, Kurs- und Zugangsentscheidung bleiben ausschließlich Verantwortung der bestehenden v27.36b-/v27.36c-Kette.
- Der neue Browser-Provider stellt ausschließlich `resolveAccess()` bereit.
- Die Komposition verbindet ausschließlich `window.ACCAOUI_SUPABASE_BOOTSTRAP`, die browserexportierte v27.36b-Factory, die browserexportierte v27.36c-Factory und eine lokale UTC-Zeitquelle.
- `bootstrap.getClient()` wird ausschließlich durch die bestehende Brücke verwendet.
- Der Vertrag behandelt fehlende oder ungültige externe/globale Abhängigkeiten, fehlenden externen Zugriff, Throw, Reject und ungültige Ergebnisse fail-closed; Zugriff wird nicht freigegeben und interne Rohfehler werden nicht ausgegeben. Ein lokaler Fallback und eine automatische Client-Erzeugung sind unzulässig.

### Späterer lokaler Checker

Der spätere Checker arbeitet ausschließlich lokal mit synthetischen Abhängigkeiten und prüft mindestens:

- CommonJS-Kompatibilität der v27.36b-/v27.36c-Bestandsmodule;
- kontrollierte Browser-Exports ohne Überschreiben inkompatibler vorhandener Werte;
- Provider-Oberfläche ausschließlich `resolveAccess()`;
- Komposition ausschließlich aus Bootstrap, v27.36b-Factory, v27.36c-Factory und lokaler UTC-Zeitquelle;
- delegierte `access_allowed`- und blockierte Pfade;
- fail-closed bei fehlenden oder ungültigen Abhängigkeiten, Throw, Reject und ungültigen Ergebnissen;
- keine Fachlogik-Duplizierung und keine verbotenen direkten Aufrufe;
- `index.html` und `app.js` unverändert;
- kein externer Zugriff;
- bestehende v27.36b-/v27.36c-Checker weiterhin PASS.

### Ausdrücklich verboten

Verboten sind `bootstrap.initializeClient()`, `bootstrap.getState()`, `supabase.createClient()`, direkte Auth-/Session-/Tabellenabfragen, frei injizierte `userId`, Netzwerk-, SQL-, Migrations-, RPC-, Config-, SDK-, Live-, Key-, Nutzer- und Teilnehmerdatenzugriffe. `index.html`, `app.js` und `style.css` bleiben unverändert und für v27.36e verboten. Der lokale App-Start bleibt unverändert. Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.

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

Die isolierte Teilnehmerzugangs-Brücke liest ausschließlich
`bootstrap.getClient()`, reicht den vorhandenen Client an die injizierte
Factory des bestehenden v27.36b-Teilnehmerzugangs-Adapters weiter, verwendet
die injizierte UTC-Zeitquelle und delegiert `resolveAccess()`. Alle
Fehlergrenzen bleiben fail-closed; die Brücke dupliziert keine Fachlogik.

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

## Permanenter v27.36c-Lebenszyklus

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
fehlender oder ungültiger Session, Queryfehlern und fehlenden, gesperrten,
abgelaufenen, noch nicht aktiven, fremden, mehrdeutigen oder inkonsistenten
Teilnehmer-, Enrollment- oder Kursdaten. Die Prüfung verwendet ausschließlich
einen lokalen synthetischen In-Memory-Fake-Client.

Keine App-Integration. Kein SDK. Kein realer Client. Kein Netzwerkzugriff.
Kein Datenbankzugriff. Keine SQL-Ausführung. Keine Migrationsausführung.
Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.

Kein Folgetask wurde ausgewählt oder autorisiert. Die nächste Umsetzung
bleibt vollständig BLOCKED, bis sie ausdrücklich autorisiert wird. Commit
und Push bleiben NEIN.

## Permanenter v27.36b-Lebenszyklus

Die stabile Basis `f7672c98a1368dec501416853830ac03e0de2d41` muss Vorfahr
jedes legitimen v27.36b-HEAD bleiben. Der Implementierungscommit wird
dynamisch aus Historie und exakter Dateimenge erkannt. Keine zukünftige
Closure-SHA wird hartcodiert.

GATE enthält ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien.
IMPLEMENTATION enthält exakt die vier autorisierten Implementierungsdateien
und ist höchstens einmal zulässig. CLOSURE enthält erst nach gültiger
IMPLEMENTATION ausschließlich Gate-Dateien und den geschlossenen Taskzustand.

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

## Permanenter v27.36a-Lebenszyklus

Die stabile Autorisierungsbasis ist
`d69290f9de2921886566b1bb398231bf009fc433`. Sie muss Vorfahr des
aktuellen HEAD sein, darf aber nicht dauerhaft als exakter HEAD
verlangt werden. Zukünftige legitime Commit-SHAs werden nicht
hartcodiert.

Der legitime Autorisierungs-GATE-Commit der Phase 2 wird dynamisch aus der
Git-Historie und seiner tatsächlichen Dateimenge erkannt. Er darf nur die
vier Steuerungsdokumente und
`tools/check-project-continuity-control.py` verändern; sein SHA wird
nicht hartcodiert und ist keine dauerhafte HEAD-Vorgabe.

Commits nach der Basis werden aus ihrer tatsächlichen Dateimenge und
dem jeweiligen Taskstatus klassifiziert: GATE ist eine nichtleere
Teilmenge der fünf Gate-Dateien; IMPLEMENTATION/AUDIT ist exakt nur
`docs/SUPABASE_LOGIN_CURRENT_STATE_AUDIT_V2736A.md` und höchstens
einmal zulässig; CLOSURE enthält erst nach diesem Audit ausschließlich
Gate-Dateien und den abgeschlossenen Taskzustand.

Der Lifecycle umfasst sechs Phasen: Autorisierung lokal vorbereitet;
Autorisierung committet, wobei eine weitere lokale Gate-Korrektur
zulässig bleibt; Audit-Datei lokal und als einzige ungetrackte Datei;
Audit exakt einmal committet bei weiterhin autorisiertem v27.36a;
Closure lokal vorbereitet auf `NONE / BLOCKED / Autorisiert NEIN`;
Closure committet und Working Tree sauber. Fremde Dateien, Audit vor
GATE, ein zweiter Audit, Closure vor Audit, Commit oder Push `JA`, ein
automatischer Folgetask und eine Rückkehr aus der Closure bleiben
gesperrt.

Der Audit ist exakt einmal im dynamisch ermittelten Commit
`f545a6c2b14a64a5bcb7bf60a2932315e571ef01` enthalten. Die lokale
Closure verändert exakt die fünf Gate-Dateien. Ein späterer
CLOSURE-Commit wird dynamisch erkannt; sein SHA wird nicht hartcodiert.

Nach der Closure bleibt eine Rückkehr zu `v27.36a / AUTHORIZED` ohne
neue ausdrückliche Autorisierung geschlossen blockiert. Kein Folgetask
ist ausgewählt oder autorisiert.

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

Kein Folgetask wurde ausgewählt oder autorisiert.

Jeder weitere Schritt bleibt gesperrt, bis ein neuer Task ausdrücklich
autorisiert wird. Eine Rückkehr zu v27.35f ist ohne neue ausdrückliche
Autorisierung nicht zulässig.

## Historische Committrennung und Gate-Korrektur

Der Commit `003112eaeb9a071a6396634b6da92fa11ae8921a` ist der funktionale
Ausgangs- und Vorautorisierungsstand. Der historische
v27.35f-Autorisierungscommit
`601dc6f751b6a603a27c4b3405150bf1d75e09fd` ist die verbindliche
Umsetzungsbasis. Der Commit
`d4e46edc48e967509e09ddd1096b54eb0bed5971` ist ein legitimer
nichtfunktionaler v27.35f-Gate-Fix-Commit, der ausschließlich die vier
Steuerungsdokumente und `tools/check-project-continuity-control.py`
verändert hat.

Der separate nichtfunktionale v27.35f-Implementierungs-Gate-
Korrekturschritt darf ausschließlich die vier Steuerungsdokumente und
`tools/check-project-continuity-control.py` verändern. Ursache dieser
fortgeführten Korrektur ist die unzulässige starre Checker-Forderung
`HEAD == 601dc6f751b6a603a27c4b3405150bf1d75e09fd`, durch die der legitime
Gate-Fix-Commit `d4e46edc48e967509e09ddd1096b54eb0bed5971` blockiert wurde.

Der frühere Notiz-SHA
`cff217d2b8cd0e9c50c3c1a351ff3de8ee595f0e3c59ed0def0ae1a3f8a799f7`
gehört zur Fassung vor der autorisierten Ergänzung „Reaktivierung nach
Lernunterbrechung“ und ist kein aktueller Prüfwert mehr. Die fertig
ergänzte Wettbewerbsnotiz ist als finaler v27.35f-Notiz-Snapshot mit
SHA-256
`983af73fb711cb2b77eb69b51d38ae5f4cf2991d1d976274eee0b4379ef9b023`
dokumentiert und muss während dieses Gate-Schritts unverändert bleiben.

Der Checker verlangt künftig, dass der Autorisierungscommit
`601dc6f751b6a603a27c4b3405150bf1d75e09fd` ein Vorfahr des aktuellen
HEAD ist und dass der gesamte bereits committete Bereich von dieser
Basis bis HEAD ausschließlich die fünf Gate-Dateien enthält. Eine starre
Gleichheit des HEAD mit einem einzelnen Gate-Commit ist verboten. Im
Working Tree sind ausschließlich zwei Zustände zulässig: vor dem
Gate-Commit exakt fünf modifizierte Gate-Dateien plus die ungetrackte
Notiz oder nach dem Gate-Commit ausschließlich die ungetrackte Notiz.
Für die Umsetzung bleibt ausschließlich
`docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` erlaubt; sie darf ungetrackt
vorliegen. Keine weitere ungetrackte Datei ist zulässig.

## Verbindliche v27.35f-Lebenszyklus-State-Machine

Die Autorisierungsbasis
`601dc6f751b6a603a27c4b3405150bf1d75e09fd` muss Vorfahr jedes aktuellen
HEAD bleiben. Alle späteren Commitrollen werden ohne zukünftigen
hartcodierten Commit-SHA ausschließlich aus Git-Historie, Dateiumfang,
Taskzustand und Inhaltsnachweis abgeleitet:

- **GATE:** eine nicht leere Teilmenge ausschließlich der fünf
  Gate-Dateien; vor der Implementation bleibt `CURRENT_TASK` autorisiert.
- **IMPLEMENTATION:** exakt nur
  `docs/COMPETITOR_POSITIONING_NOTE_V2735F.md`, höchstens einmal und mit
  SHA-256
  `983af73fb711cb2b77eb69b51d38ae5f4cf2991d1d976274eee0b4379ef9b023`.
- **CLOSURE:** ausschließlich Gate-Dateien, erst nach nachgewiesenem
  IMPLEMENTATION-Commit und mit abgeschlossenem Taskzustand.

Die vier zulässigen Phasen sind:

1. **Vor Implementation:** `v27.35f / AUTHORIZED / Autorisiert JA`;
   Historie nur GATE-Commits; Working Tree nur die ungetrackte finale
   Notiz oder während eines Gate-Schritts zusätzlich exakt die fünf
   modifizierten Gate-Dateien.
2. **Implementation committet:** weiterhin
   `v27.35f / AUTHORIZED / Autorisiert JA`; exakt ein IMPLEMENTATION-
   Commit ist dynamisch aus Git nachgewiesen; Working Tree sauber.
3. **Closure lokal vorbereitet:** erst nach Implementation; Working Tree
   exakt die fünf Gate-Dateien; `CURRENT_TASK` lokal auf `NONE / BLOCKED /
   Autorisiert NEIN`, `Titel: Kein Task autorisiert`, `Erlaubte Dateien:
   KEINE` umgestellt; Commit und Push bleiben gesperrt.
4. **Closure committet:** abgeschlossener Taskzustand und sauberer Working
   Tree; spätere Gate-/Closure-Commits dürfen den abgeschlossenen Zustand
   nicht wieder auf v27.35f zurücksetzen.

Im Abschlusszustand müssen die Steuerungsdokumente „v27.35f
abgeschlossen“, den finalen Notiz-SHA, den aus Git dynamisch ermittelten
`Implementierungscommit: <SHA>` und „Kein Folgetask wurde ausgewählt oder
autorisiert.“ dokumentieren. Closure ohne Implementation, ein zweiter
IMPLEMENTATION-Commit, fremde Commitdateien, ein falscher Notiz-SHA,
zusätzliche Working-Tree-Dateien sowie Commit oder Push `JA` bleiben
geschlossen blockiert.

Während der Umsetzung blieb v27.35f der einzige aktive Task. Commit und
Push blieben verboten, und ein Folgetask wurde nicht ausgewählt oder
autorisiert.

## Historisches Ziel

Eine interne strategische Dokumentation erstellen, die allgemeine
Verkaufs- und Positionierungsmechanismen eines beobachteten
Wettbewerberangebots analysiert und daraus eine eigenständige,
ehrliche Accaoui-Positionierung ableitet.

## Verbindliche Grundlage

Die folgenden Punkte dürfen ausschließlich als beobachtete und nicht
extern verifizierte Wettbewerber-Werbeaussagen beschrieben werden:

- niedriger Einmalpreis im Vergleich zu möglichen Wiederholungs- und Prüfungskosten
- zeitlich unbegrenzte Prüfungssimulationen
- behauptete Abdeckung aller IHK-Fragen
- behauptetes KI-basiertes Erkennen von Schwächen
- Rückerstattungs- oder Risikoumkehr-Versprechen
- dauerhafter Besitz beziehungsweise unbegrenzter Zugang
- Nutzerzahlen, Bewertungen oder sonstiger Social Proof

## Zulässige allgemeine Marketingmechanismen

- Preisanker
- Verlustvermeidung
- klare Nutzenkommunikation
- Risikoumkehr
- Social Proof
- Einfachheit des Angebots
- persönliche Schwächenanalyse
- Prüfungssimulation als konkretes Leistungsversprechen

## Verbindliche Accaoui-Differenzierung

- Wissen verständlich vermitteln
- typische Fehler erkennen und gezielt bearbeiten
- Inhalte langfristig festigen
- realistische schriftliche und mündliche Prüfungsvorbereitung
- nachvollziehbare persönliche Lernführung
- Teilnehmer bis zur Prüfungsreife begleiten
- echte Unterrichts- und Prüfungsvorbereitungserfahrung
- nicht nur Fragen beantworten, sondern Inhalte verstehen

## Qualitätsmaßstab

> „Mit dieser App habe ich es endlich verstanden.“

Die Leitidee aus `docs/PROJECT_MASTERLIST.md` bleibt verbindlich.

## Verboten

- Wettbewerbertexte kopieren
- geschützte Formulierungen nachahmen
- behaupten, der Wettbewerber lüge oder handle rechtswidrig
- nicht belegte Nutzerzahlen oder Bewertungen als Tatsachen darstellen
- behaupten, Accaoui besitze alle originalen IHK-Fragen
- Bestehensgarantien
- unbelegte KI-Versprechen
- unbelegte Rückerstattungsversprechen
- konkrete Preise verbindlich festlegen
- App-Code, UI, Fragenbanken oder Marketingmaterial verändern
- Webrecherche oder externe Behauptungen ohne gesonderten Auftrag
- Funktions-, Fragen-, UI-, Supabase-, SQL- oder Netzwerkänderungen
- automatische Auswahl oder Autorisierung eines Folgetasks

## Akzeptanzkriterien

1. Beobachtung, Bewertung und Accaoui-Empfehlung sind klar getrennt.
2. Wettbewerberaussagen sind ausdrücklich als nicht verifiziert markiert.
3. Keine Formulierung wird vom Wettbewerber übernommen.
4. Chancen und Risiken der Marketingmechanismen werden sachlich erklärt.
5. Eine eigenständige Accaoui-Kernpositionierung wird formuliert.
6. Zulässige und unzulässige Werbeaussagen werden getrennt dokumentiert.
7. Die Leitidee aus `docs/PROJECT_MASTERLIST.md` bleibt verbindlich.
8. Keine Funktions-, Fragen-, UI-, Supabase-, SQL- oder Netzwerkänderung.
9. Ausschließlich `docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` wird im späteren Umsetzungsschritt verändert.
10. Kein Commit und kein Push ohne gesonderte Freigabe.

## Historische Grenze des Autorisierungsschritts

`docs/COMPETITOR_POSITIONING_NOTE_V2735F.md` wurde im abgeschlossenen
Autorisierungsschritt noch nicht erstellt oder verändert. In diesem
Schritt wurde keine Wettbewerbsnotiz erstellt und keine App-Datei
verändert.

Die Umsetzung durfte ausschließlich diesen damaligen `CURRENT_TASK`
bearbeiten. Nach dem Abschluss wurde kein Folgetask automatisch ausgewählt.
