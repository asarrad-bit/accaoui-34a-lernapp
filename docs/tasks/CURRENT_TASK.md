# Verbindlicher aktueller Task

Task-ID: v27.37a
Status: AUTHORIZED
Autorisiert: JA
Titel: Isolierten Teilnehmer-Auth-/Session-Adapter mit synthetischem Fake-Auth-Vertrag implementieren
Funktionaler Ausgangsstand: v27.35g
Letzter abgeschlossener Kontrollschritt: v27.37a-GATE-REPAIR-FOLLOWUP
Erlaubte Implementierungsdateien: `data/supabase-participant-auth-session-adapter.js`, `tools/check-supabase-participant-auth-session-adapter.py`, `docs/SUPABASE_PARTICIPANT_AUTH_SESSION_ADAPTER_V2737A.md`, `tools/preflight.py`
Commit erlaubt: NEIN
Push erlaubt: NEIN

## Autorisierter Task v27.37a

v27.37a ist ausdrücklich autorisiert.

Der Titel lautet: Isolierten Teilnehmer-Auth-/Session-Adapter mit synthetischem Fake-Auth-Vertrag implementieren.

Technische v27.37a-Basis: `2da93d2931178fb225b41a301d21658b40729857`.

Der v27.37a-GATE-REPAIR und der v27.37a-GATE-REPAIR-FOLLOWUP bleiben vollständig abgeschlossen. Die FOLLOWUP-Grenze `2da93d2931178fb225b41a301d21658b40729857` wird nicht erneut geöffnet oder wiederholt. Die aktuelle Autorisierung beginnt einen neuen eigenständigen v27.37a-Lifecycle ab dieser Grenze.

Die spätere Implementierung umfasst exakt vier Dateien:

- `data/supabase-participant-auth-session-adapter.js`
- `tools/check-supabase-participant-auth-session-adapter.py`
- `docs/SUPABASE_PARTICIPANT_AUTH_SESSION_ADAPTER_V2737A.md`
- `tools/preflight.py`

Keine fünfte Implementierungsdatei ist erlaubt.

### Öffentlicher Vertrag

Das neue isolierte Modul ist `data/supabase-participant-auth-session-adapter.js`. Die Factory lautet exakt `createParticipantAuthSessionAdapter({ auth })`.

Die öffentliche Oberfläche enthält exakt:

- `resolveSession()`
- `signIn({ email, password })`
- `signOut()`

Eine vierte öffentliche Methode ist verboten. Die einzige injizierte Dependency ist `auth`. Ausschließlich `auth.getSession()`, `auth.signInWithPassword(...)` und `auth.signOut()` dürfen verwendet werden.

Jede öffentliche Rückgabe ist ein gefrorenes Plain Object mit exakt den zwei Properties `{ ok: boolean, code: string }`.

- `resolveSession()` gibt ausschließlich `session_available`, `session_missing`, `session_invalid` oder `auth_error` zurück.
- `signIn({ email, password })` gibt ausschließlich `signed_in`, `credentials_invalid`, `sign_in_failed` oder `auth_error` zurück.
- `signOut()` gibt ausschließlich `signed_out`, `sign_out_failed` oder `auth_error` zurück.

Session, User, `user.id`, E-Mail, Passwort, Token, `access_token`, `refresh_token`, Auth-Response, Config, Key, Error-Objekt und Error-Message dürfen niemals öffentlich zurückgegeben werden. Rohfehler bleiben ausgeschlossen.

### Sicherheitsgrenze

v27.37a darf `app.js`, `index.html`, den Browser-Loader oder bestehende Supabase-Produktmodule nicht ändern. `window`, `document`, DOM, `localStorage`, `sessionStorage`, Cookies sowie das Speichern von Passwörtern oder Tokens sind verboten. Client-Erzeugung, `createClient()`, `initializeClient()`, Config-Lesen, `fetch`, `XMLHttpRequest`, `WebSocket`, `.from(...)`, Teilnehmer-, Enrollment- oder Kursabfragen, SQL, Migrationen, eine frei übergebene `userId` und jede Live-Schaltung von Supabase sind verboten.

Die bestehende Teilnehmer-Fachautorität bleibt ausschließlich `session.user.id` im vorhandenen v27.36b-Teilnehmerzugangs-Adapter. Keine Fachlogik daraus darf dupliziert werden. Der Browser-Loader bleibt unverändert bei `data-enabled="false"`. Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.

Mindestens diese Produktdateien bleiben gegenüber der technischen Basis unverändert:

- `index.html`
- `app.js`
- `data/supabase-client-bootstrap.js`
- `data/supabase-client-adapter.js`
- `data/supabase-participant-access-adapter.js`
- `data/supabase-participant-access-bootstrap-bridge.js`
- `data/supabase-participant-access-browser-provider.js`
- `data/supabase-participant-access-browser-loader.js`
- `questions.json`
- `style.css`

### Späterer Testvertrag

Getestet wird ausschließlich lokal mit einem synthetischen In-Memory Fake Auth. `resolveSession()` prüft gültige, fehlende und ungültige Sessions, fehlenden oder ungültigen User beziehungsweise `user.id`, Response-Error, Throw und Reject. `signIn()` prüft Erfolg, ungültige Eingaben, Response-Error, Throw und Reject. `signOut()` prüft Erfolg, Response-Error, Throw und Reject.

Zusätzlich werden exakt zwei Ergebnisproperties, `Object.freeze`, das Ausbleiben von Passwort-, Session-, User-, Token- und Rohfehler-Leaks, die einzige Dependency, die Storage-, Netzwerk-, Tabellen- und Client-Erzeugungssperren sowie die synthetische Integration geprüft: `signIn` führt über den bestehenden v27.36b-Teilnehmerzugangs-Adapter zu `access_allowed`; `signOut` führt über denselben unveränderten Adapter zu `session_missing`.

### Permanenter v27.37a-Lifecycle

Die technische Basis ist `2da93d2931178fb225b41a301d21658b40729857`. Der Lifecycle erkennt dynamisch exakt `authorization_prepared`, `authorization_committed`, `implementation_prepared`, `implementation_committed`, `closure_prepared` und `closure_committed`.

`authorization_prepared` verlangt HEAD auf der technischen Basis, eine nichtleere Teilmenge ausschließlich der fünf Gate-Dateien im Working Tree und den autorisierten v27.37a-Task ohne Implementierungsdatei. `authorization_committed` verlangt einen sauberen Working Tree und genau einen legitimen Gate-Commit direkt nach der Basis, der ausschließlich Gate-Dateien enthält.

`implementation_prepared` verlangt den legitimen Gate-Commit und exakt die vier Implementierungsdateien im Working Tree. `implementation_committed` verlangt einen sauberen Working Tree und einen direkten Implementierungscommit mit exakt diesen vier Dateien.

`closure_prepared` verlangt die legitim committete Implementierung, exakt die fünf Gate-Dateien im Working Tree und `CURRENT_TASK` geschlossen als `NONE / BLOCKED / Autorisiert NEIN`. `closure_committed` verlangt einen sauberen Working Tree, einen direkten Closure-Commit mit exakt den fünf Gate-Dateien und den weiterhin geschlossenen Taskzustand.

Ein zweites Gate, eine zweite Implementierung, ein Gate nach der Implementierung, eine Closure vor der Implementierung, eine Implementierung nach der Closure, unbekannte History-Rollen und spätere unbekannte Tasks werden blockiert. Keine zukünftige Gate-, Implementierungs- oder Closure-SHA wird hartcodiert.

Dieser Gate-Schritt autorisiert keine Produktimplementierung. Commit und Push bleiben NEIN.

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
