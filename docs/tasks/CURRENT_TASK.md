# Verbindlicher aktueller Task

Task-ID: NONE
Status: BLOCKED
Autorisiert: NEIN
Titel: Kein Task autorisiert
Funktionaler Ausgangsstand: v27.35g
Letzter abgeschlossener Kontrollschritt: v27.37a
Erlaubte Implementierungsdateien: KEINE
Commit erlaubt: NEIN
Push erlaubt: NEIN

## v27.37b-GATE-BOOTSTRAP-REPAIR – Kontrollinfrastruktur

v27.37b-GATE-BOOTSTRAP-REPAIR korrigiert ausschließlich den phasenfesten und strukturellen CURRENT_TASK-Vertrag in Continuity und Preflight.

Repair-Basis: `b83581612fa25b73f62c4b146e8df782d67c869c`.

Der einmalige atomare Repair umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Datei und keine Produktdatei sind zulässig.

Der Bootstrap-Commit `b83581612fa25b73f62c4b146e8df782d67c869c` bleibt korrekt. Der Repair behebt ausschließlich phasenfremde reale Manipulationsbaselines, unvollständige Kopfstrukturprüfungen und fehlende CURRENT_TASK-Negativtests.

Der kanonische CURRENT_TASK-Kopf reicht exakt von `# Verbindlicher aktueller Task` bis unmittelbar vor dem verpflichtenden ersten `## `-Abschnitt. Er enthält exakt die neun bekannten Felder in definierter Reihenfolge; fehlende, doppelte, unbekannte oder ungeordnete Kopffelder bleiben blockiert. Historische Abschnitte dürfen einen ungültigen aktuellen Kopf weder retten noch einen gültigen Kopf beschädigen.

Die drei kanonischen Taskzustände bleiben BASE_CLOSED, AUTHORIZED und CLOSED. Bootstrap-Phasen verwenden BASE_CLOSED; Authorization- und Implementation-Phasen verwenden AUTHORIZED; Closure-Phasen verwenden CLOSED. Synthetische Manipulationstests verwenden ausschließlich vollständige phasenspezifische CURRENT_TASK-Dokumente und niemals den realen CURRENT_TASK als Test-Baseline.

Der spätere Produktvertrag für `v27.37b – Isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke` bleibt unverändert: exakt zwei Dependencies, exakt drei öffentliche Methoden, `getClient()` exakt einmal pro Operation, kein Client-Cache, ausschließlich `client.auth` als `{ auth }` und für Brückenfehler `Object.freeze({ ok: false, code: "auth_error" })`.

Der vorbereitete Zustand ist `v2737b_gate_bootstrap_repair_prepared`. Nach einem späteren direkten Repair-Commit ist er dynamisch `v2737b_gate_bootstrap_repair_committed`. Keine zukünftige Repair-Commit-SHA wird hartcodiert; der Repair darf nur einmal vorkommen.

`CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`; v27.37b wird durch diesen Repair NICHT autorisiert. Erst nach dem Repair-Commit ist ein frisches separates v27.37b-Autorisierungs-Gate zulässig.

Der lokale Sicherungspatch `.git/v2737b-authorization-preflight-blocked.patch` wird nicht angewendet, nicht verändert und nicht als Implementierungsquelle verwendet.

Kein Produktcode wird geändert. Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.


## v27.37b-GATE-BOOTSTRAP – Kontrollinfrastruktur

v27.37b-GATE-BOOTSTRAP ist ausschließlich Kontrollinfrastruktur.

Stabile Bootstrap-Basis: `b5d676d226891b4f53e9e614e015c433c2616ad1`.

Der einmalige atomare Bootstrap umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Datei und keine Produktdatei sind zulässig. v27.37a bleibt vollständig abgeschlossen und wird nicht wieder geöffnet.

Der spätere Task heißt exakt `v27.37b – Isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke`, ist nach diesem Bootstrap aber NICHT autorisiert. `CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`. Der nächste zulässige Schritt nach einem erfolgreichen Bootstrap-Commit ist ein separates ausdrückliches v27.37b-Autorisierungs-Gate.

Der spätere Implementierungsscope umfasst exakt:

- `data/supabase-participant-auth-session-bootstrap-bridge.js`
- `tools/check-supabase-participant-auth-session-bootstrap-bridge.py`
- `docs/SUPABASE_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_V2737B.md`
- `tools/preflight.py`

Die spätere Factory ist `createParticipantAuthSessionBootstrapBridge({ bootstrap, createParticipantAuthSessionAdapter })`. Die Dependencies sind exakt `bootstrap` und `createParticipantAuthSessionAdapter`; eine dritte Dependency ist ausgeschlossen. Ihre öffentliche Oberfläche enthält exakt `resolveSession()`, `signIn({ email, password })` und `signOut()`. Eine vierte öffentliche Methode ist ausgeschlossen. Pro öffentlicher Operation wird `bootstrap.getClient` sicher genau einmal gelesen und `getClient()` genau einmal aufgerufen; der Client wird nicht dauerhaft gecacht. Ausschließlich `client.auth` wird als exakt `{ auth }` an `createParticipantAuthSessionAdapter({ auth })` weitergegeben.

Gültige methodenspezifische v27.37a-Ergebnisse werden unverändert delegiert. Jeder Brückenfehler liefert ausschließlich das eingefrorene Plain Object `Object.freeze({ ok: false, code: "auth_error" })`; Session-, User-, ID-, E-Mail-, Passwort-, Token-, Config- und Rohfehlerdaten bleiben ausgeschlossen.

Verboten bleiben `initializeClient()`, `getState()`, `createClient()`, Browser-Globals, `window`, `document`, DOM, `localStorage`, `sessionStorage`, Cookies, IndexedDB, Config-Lesen, eigener Netzwerkcode, `.from(...)`, Teilnehmer-, Enrollment- oder Kurslogik, SQL und Migrationen. Bestehende Produktdateien bleiben frozen.

Der Lifecycle erkennt den aktuellen einmaligen Schritt dynamisch als `v2737b_gate_bootstrap_prepared` und nach einem direkten Sechs-Dateien-Commit als `v2737b_gate_bootstrap_committed`. Danach sind ausschließlich die v27.37b-Phasen `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed` zulässig. Keine zukünftige Bootstrap-, Gate-, Implementierungs- oder Closure-SHA wird hartcodiert; eine Wiederholung und eine allgemeine zukünftige Taskfreigabe bleiben blockiert.

Kein Produktcode wurde geändert. Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.

## Abgeschlossener technischer Schritt v27.37a

v27.37a abgeschlossen.

Implementierungscommit: `54f6425fac70da134e3c6f39b376f66fa75063cb`

Ergebnis:

- Der isolierte CommonJS Teilnehmer-Auth-/Session-Adapter ist implementiert.
- Die Factory ist `createParticipantAuthSessionAdapter({ auth })`.
- Die öffentliche Oberfläche enthält exakt:
  - `resolveSession()`
  - `signIn({ email, password })`
  - `signOut()`
- Die einzige Dependency ist `auth`.
- Alle Ergebnisse sind gefrorene Plain Objects mit exakt `{ ok, code }`.
- Sensitive Daten, Sessions, Nutzer, Passwörter, Token und Rohfehler werden nicht nach außen gegeben.
- Es gibt kein Browser-Wiring und keinen Storage-Zugriff.
- Es gibt keinen eigenen Netzwerkcode, keinen Client, kein `createClient()` und kein `initializeClient()`.
- Es gibt keine Tabellenlogik und keine Duplizierung der v27.36b-Fachlogik.
- Supabase bleibt NICHT LIVE.

Testergebnis:

- Positiv: 7 PASS.
- Negativ: 57 PASS.
- Manipulation: 20 PASS.
- Shared-Fake signIn -> access_allowed: PASS.
- Shared-Fake signOut -> session_missing: PASS.
- Continuity: PASS.
- Preflight: PASS.
- v27.36b: PASS.
- v27.36c: PASS.
- v27.36d Regression: PASS.
- v27.36e Regression: PASS.
- v27.36f Regression: PASS.
- v27.37a Nachfolgeprofil: PASS.
- `git diff --check`: PASS.

### Permanenter v27.37a-Lifecycle

Der Lifecycle erkennt weiterhin dynamisch `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed`.

`closure_prepared` verlangt den Implementierungscommit, exakt die fünf Gate-Dateien im Working Tree, `CURRENT_TASK` als `NONE / BLOCKED / Autorisiert NEIN` und unveränderte Produktdateien. `closure_committed` verlangt danach einen direkten Closure-Commit mit exakt diesen fünf Gate-Dateien und einen sauberen Working Tree.

Keine zukünftige Closure-SHA wird hartcodiert.

Eine zweite Implementierung, eine Implementierung nach der Closure und eine implizite Autorisierung werden blockiert. Kein Folgetask wurde ausgewählt oder autorisiert.

## Abgeschlossener atomarer Follow-up-Repair v27.37a-GATE-REPAIR-FOLLOWUP

v27.37a-GATE-REPAIR-FOLLOWUP abgeschlossen.

Der Titel lautet: UTF-8-Historienleser und authorization_prepared-Scope im v27.37a-Nachfolgeprofil korrigieren.

Technische Basis: `ec8f20216d8dcb13417cca27699febc998d6dcd9`.

Der erste v27.37a-GATE-REPAIR bleibt vollständig abgeschlossen und wird nicht wiederholt. Der einmalige atomare FOLLOWUP war erforderlich, weil der v27.37a-Historienpfad Git-Blobs über die Windows-Codepage CP1252 statt strikt als UTF-8 las und weil `authorization_prepared` fälschlich exakt alle fünf statt jeder nichtleeren Teilmenge der Gate-Dateien verlangte.

Der ausdrücklich freigegebene einmalige atomare FOLLOWUP-Repair umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Datei ist erlaubt. Keine Produktfunktion und keine Produktdatei wurden geändert. Die historischen v27.36e-/v27.36f-Produkt- und Sicherheitsverträge bleiben unverändert.

Der v27.37a-Historienpfad verwendet für Git-Blobs ausschließlich den vorhandenen strikt UTF-8-decodierenden Reader. Die globale `run_command()`-Semantik bleibt unverändert. `authorization_prepared` akzeptiert ausschließlich eine nichtleere Teilmenge der fünf Gate-Dateien; leere Mengen, Implementierungsdateien, `tools/preflight.py`, `app.js`, Produktdateien und unbekannte Zusatzdateien bleiben blockiert. Alle späteren Lifecyclephasen und ihre exakten Dateimengen bleiben unverändert streng.

Der Lifecycle erkennt ausschließlich den einmaligen Zustand `v2737a_gate_repair_followup_atomic_prepared` und nach einem direkten Sechs-Dateien-Commit `v2737a_gate_repair_followup_atomic_committed`. Eine Wiederholung und jede zukünftige FOLLOWUP-Commit-SHA bleiben blockiert.

`CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`. v27.37a ist nach dem FOLLOWUP weiterhin nicht autorisiert; der nächste zulässige Schritt ist ein frisches ausdrückliches v27.37a-Autorisierungs-Gate.

Die lokalen Sicherungen `.git/v2737a-gate-preflight-blocked.patch` und `.git/v2737a-gate-after-ec8f202.patch` bleiben unangewendet, unverändert, lokal und außerhalb jedes Commits.

Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten. Commit und Push bleiben NEIN.


## Abgeschlossener atomarer Bootstrap-Repair v27.37a-GATE-REPAIR

v27.37a-GATE-REPAIR abgeschlossen.

Titel des Repairs: Enges Preflight-Nachfolgeprofil nach abgeschlossenem v27.36f bootstrapen.

Stabile Ausgangsbasis: `ac997149fe9600d735dcc237b0a30232d279cc52`.

Historische v27.36f-Grenzen bleiben `a68dd9e81f26c3a887e668b90e9f5e8973c7ddfa` für die Implementierung, `b035c62100b033dbce03a4ab016e4471b4ab54d4` für die Repair-Implementierung, `d2a303e3ca4cfd8b61a1e7b7f8e5c4b43682c712` für die Repair-Closure und `ac997149fe9600d735dcc237b0a30232d279cc52` für die endgültige v27.36f-Closure.

Der ursprüngliche v27.37a-Gate-Versuch konnte den unveränderten Preflight nicht legitim bestehen, weil dessen bisheriges Profil ausschließlich die abgeschlossenen v27.36f-/REPAIR-Lifecyclezustände kannte und bei einem Nachfolgetask auf historische Standalone-Checker zurückfiel. Die v27.36e-/v27.36f-Produktverträge waren dabei unverändert intakt. Ein normaler separater Repair-Gate-Commit hätte deshalb wissentlich keinen verpflichtenden Preflight-PASS erreicht.

Der ausdrücklich freigegebene einmalige atomare Bootstrap-Repair umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Das neue enge Preflight-Nachfolgeprofil akzeptiert nur den aktuellen atomaren Repair, dessen direkt folgenden committeten Zustand und später ausdrücklich autorisierte v27.37a-Gate-, Implementierungs- oder Closurezustände, sofern deren eigener Kontinuitätsvertrag passt. Unbekannte zukünftige Tasks werden nicht pauschal zugelassen. Es gibt keinen allgemeinen Bypass.

`index.html`, `app.js`, `data/supabase-participant-access-adapter.js`, `data/supabase-participant-access-bootstrap-bridge.js`, `data/supabase-participant-access-browser-provider.js` und `data/supabase-participant-access-browser-loader.js` bleiben gegenüber der endgültigen v27.36f-Closure unverändert und werden zusätzlich fachlich gegen die v27.36e-/v27.36f-Sicherheitsverträge geprüft.

Die lokale Sicherung `.git/v2737a-gate-preflight-blocked.patch` bleibt ausschließlich lokal, wird nicht verändert, nicht angewendet und nicht committet.

Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten. Keine automatische Client-Erzeugung. Keine direkten Auth- oder Tabellenabfragen werden freigegeben.

Nach dem Repair ist v27.37a weder ausgewählt noch autorisiert. `CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`; Commit und Push bleiben `NEIN`.

Der Lifecycle erkennt dynamisch `v2737a_gate_repair_atomic_prepared` und nach einem späteren direkten Sechs-Dateien-Commit `v2737a_gate_repair_atomic_committed`. Keine zukünftige Repair-, v27.37a-IMPLEMENTATION- oder v27.37a-CLOSURE-SHA wird hartcodiert.

## Abgeschlossener technischer Schritt v27.36f

v27.36f abgeschlossen.

Der technische Stand ist v27.36f vollständig abgeschlossen. Der letzte abgeschlossene funktionale Stand bleibt v27.35g.

Implementierungscommit: `a68dd9e81f26c3a887e668b90e9f5e8973c7ddfa`

Zusätzlicher enger Prüfpfad-Repair: v27.36f-REPAIR.

Repair-Implementierungscommit: `b035c62100b033dbce03a4ab016e4471b4ab54d4`

Repair-Closure: `d2a303e3ca4cfd8b61a1e7b7f8e5c4b43682c712`

v27.36f-REPAIR vollständig abgeschlossen.

Umgesetzte Dateien:

- `index.html`
- `app.js`
- `data/supabase-participant-access-browser-loader.js`
- `tools/check-participant-access-browser-loader-v2736f.py`
- `docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md`
- `tools/preflight.py`

Ergebnis:

- Loader-ID: `accaoui-participant-access-browser-loader`.
- Der finale Default bleibt `data-enabled="false"`.
- Nur der exakte Attributwert `"true"` fordert die Aktivierung an.
- Bei deaktiviertem Schalter bleibt der lokale Standardbetrieb unverändert und nicht blockierend.
- Bei angeforderter Aktivierung werden Adapter, Brücke und Browser-Provider in fester Reihenfolge geladen.
- Die Readiness-Oberfläche ist `window.ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY`.
- `app.js` verwendet weiterhin den v27.36d-Providervertrag mit `resolveAccess()`.
- Fehler bei angeforderter Aktivierung bleiben fail-closed ohne lokalen Fallback.
- Der generische Fehlerzustand ist `access_error`; interne Rohfehler werden nicht ausgegeben.
- Keine Fachlogik wurde dupliziert.

Repair-Abschluss:

- `closure_prepared` wird korrekt geprüft.
- `closure_committed` wird dynamisch geprüft.
- Die v27.36e-Regression bleibt über das enge v27.36f-Profil geschützt.
- Der Repair-Lifecycle ist vollständig geschlossen.
- Es gibt keinen pauschalen Bypass.
- Keine zukünftige Closure-SHA wird hartcodiert.

Testergebnis:

- v27.36f-Checker: PASS.
- Positivprüfungen: 41 PASS.
- Negativprüfungen: 27 PASS.
- Manipulationsprüfungen: 46 PASS.
- v27.36b-/v27.36c-/v27.36d-/v27.36e-Regressionen: PASS.
- Kontinuitätschecker: PASS.
- Preflight: PASS.
- `git diff --check`: PASS.

Sicherheitsgrenze:

- Supabase bleibt NICHT LIVE.
- Keine echten Keys.
- Keine echten Teilnehmerdaten.
- Kein echter Login ist produktiv aktiviert.
- Keine Live-Aktivierung.
- Kein `initializeClient()`.
- Kein `createClient()`.
- Keine direkte Auth-Abfrage.
- Keine Tabellenabfrage.
- Kein SQL.
- Keine Migration.
- Der Loader-Schalter bleibt standardmäßig `false`.

Kein Folgetask wurde ausgewählt oder autorisiert. Kein neuer Task und keine implizite Autorisierung bestehen.

### Permanenter v27.36f-Lebenszyklus

Der Lifecycle erkennt dynamisch die Phasen `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed` und berücksichtigt den vollständig geschlossenen v27.36f-REPAIR-Verlauf.

Die ursprüngliche CLOSURE ist erst nach IMPLEMENTATION und vollständig geschlossenem Repair-Verlauf zulässig, enthält exakt die fünf Gate-Dateien und setzt beziehungsweise belässt `CURRENT_TASK` auf `NONE / BLOCKED / Autorisiert NEIN`.

Keine zukünftige CLOSURE-SHA wird hartcodiert. Rückkehr zu einem autorisierten v27.36f-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert. Rückkehr zu `v27.36f-REPAIR / AUTHORIZED` bleibt ohne neue ausdrückliche Autorisierung blockiert. Eine erneute v27.36f-IMPLEMENTATION ist nach `closure_committed` unzulässig.

## Abgeschlossener technischer Schritt v27.36e

v27.36e abgeschlossen.

Implementierungscommit: `0c4d64aaa7da7e8dd38fff1d7bf72675cb689a6f`

Umgesetzte Dateien:

- `data/supabase-participant-access-adapter.js`
- `data/supabase-participant-access-bootstrap-bridge.js`
- `data/supabase-participant-access-browser-provider.js`
- `tools/check-participant-access-browser-provider-v2736e.py`
- `docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md`
- `tools/preflight.py`

Ergebnis:

- Die CommonJS-Kompatibilität der v27.36b-/v27.36c-Bestandsmodule bleibt erhalten.
- Kontrollierte Browser-Exports verbinden die bestehenden Factories.
- Browser-Factory-Exports sind `window.ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY` und `window.ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY`.
- Der Browser-App-Provider ist `window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER`.
- Der Browser-Provider stellt ausschließlich `resolveAccess()` bereit.
- Keine Fachlogik wird dupliziert.
- Fehlende oder ungültige Dependencies sowie Throw, Reject und ungültige Ergebnisse bleiben fail-closed.
- Der Kollisionsschutz überschreibt keine inkompatiblen vorhandenen Globals.
- Es gibt keine automatische Client-Erzeugung.
- Es gibt keine direkten Supabase-, Auth- oder Tabellenabfragen im Provider.
- `index.html`, `app.js` und `style.css` bleiben unverändert.
- Die Browser-Kette ist noch NICHT über `index.html` aktiviert.
- Der lokale App-Start bleibt unverändert.
- Supabase bleibt NICHT LIVE.
- Keine echten Keys.
- Keine echten Teilnehmerdaten.

Testergebnis:

- v27.36e-Checker: PASS (Positiv: 22; Negativ: 31; Manipulation: 16).
- v27.36b-Checker: PASS.
- v27.36c-Checker: PASS.
- v27.36d-Regressionsprofil: PASS.
- Kontinuitätschecker: PASS.
- Preflight: PASS.
- `git diff --check`: PASS.

Kein Folgetask wurde ausgewählt oder autorisiert.

### Permanenter v27.36e-Lebenszyklus

Der Lifecycle erkennt dynamisch genau die Phasen `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed`.

Der Implementierungscommit ist historisch dokumentiert. Die Closure wird weiterhin dynamisch aus Git-Historie, Dateiumfang und geschlossenem Taskzustand erkannt.
Keine zukünftige CLOSURE-SHA wird hartcodiert.
Rückkehr zu einem autorisierten v27.36e-Zustand bleibt ohne neue ausdrückliche Autorisierung blockiert.

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
