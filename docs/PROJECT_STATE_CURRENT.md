# Aktueller Projektzustand

Stand: v27.37f
Repository: `asarrad-bit/accaoui-34a-lernapp`
Branch: `main`
Letzter abgeschlossener funktionaler Stand: v27.35g
Abschlusscommit: `f5f261fee67fc17c170ee714ae23761ff1668f17`
Aktueller HEAD: DYNAMISCH ZU PRÜFEN
Funktionsstatus: v27.35g abgeschlossen
Weiterer funktionaler Schritt autorisiert: NEIN
Aktuell autorisierter Task: NONE
Aktuelle Taskart: Kein Task autorisiert
Aktueller Blocker: Neue Taskauswahl und ausdrückliche Autorisierung durch Projekteigentümer und verbindlichen Projektchat

## Abgeschlossener technischer Schritt v27.37f

v27.37f – Auth-/Session-Anbindung an den App-Start ist abgeschlossen.

Implementierungscommit: `48a9b27f190e8dc872aedd9df578470ffe4ce9c1`.

Die Auth-/Session-Anbindung gilt ausschließlich für ausdrücklich angeforderten Auth-Modus. Beide Loader bleiben deaktiviert; die bestehende Teilnehmerzugangsprüfung bleibt erforderlich. Supabase bleibt NICHT LIVE.

Kein Folgetask ist autorisiert. Commit und Push bleiben gesperrt.

Die folgenden Abschnitte dokumentieren historische Abschlüsse und Autorisierungen; sie erteilen keine weitere aktuelle Freigabe.

## Autorisierter Task v27.37f

v27.37f – Auth-/Session-Anbindung an den App-Start ist ausschließlich als späterer Implementierungstask autorisiert.

Technische Gate-Basis: `514b0c25805a53f711d963f2fe3b7c08d4eef3e1`.

Dieses direkte Gate erhält den vollständigen v27.37e-Abschluss einschließlich Historie und Dokumenten. Kein zusätzlicher Bootstrap ist erforderlich. Die Implementation bleibt bis zum direkten Commit dieses Gates und einem ausdrücklichen Implementierungsauftrag gesperrt. Dieses Gate implementiert keine Produktänderung.

Der spätere Implementierungsscope umfasst exakt:

- `app.js`
- `tools/check-participant-auth-session-app-entry-v2737f.py`
- `docs/PARTICIPANT_AUTH_SESSION_APP_ENTRY_V2737F.md`
- `tools/preflight.py`

Keine fünfte Implementierungsdatei ist zulässig. In app.js sind ausschließlich initAppBoot(), initAuthFlow() und ein zusammenhängender Hilfsblock unmittelbar vor initAppBoot() erlaubt. Der Hilfsblock wird mit den eigenständigen Kommentarzeilen `// BEGIN v27.37f auth/session app entry` und `// END v27.37f auth/session app entry` begrenzt. Der übrige App-Code bleibt identisch zur Basis, insbesondere bestehender Teilnehmerzugangsresolver, Hinweisansichten, startLocalApp(), Lernlogik und Config-/Health-Funktionen. In der Implementation darf tools/preflight.py ausschließlich die vorbereitete feste Checker-Registrierung ersetzen.

Vorbereitungsbefund: initAppBoot() lädt bisher vor initAuthFlow() optional Config nach. initAuthFlow() erhält lokale Sperren, wartet bei angefordertem Zugangs-Loader auf Readiness und erlaubt bei fehlendem Zugangsprovider ohne Loader-Anforderung einen lokalen Start. Der Auth-Modus muss vor der optionalen Config-Nachladung abzweigen und den Abwesenheits-Fallback sperren. Die vorhandene Zugangsprüfung ermittelt ihre Benutzeridentität selbst aus der Session und prüft Teilnehmer, Enrollment und Kurs; keine Logikduplikation und keine frei übergebene userId.

Aktivierung und alle vier Schalterkombinationen:

A bedeutet exakt data-enabled="true" am Script mit ID accaoui-participant-auth-session-browser-loader. Z bedeutet dasselbe Attribut am bestehenden Teilnehmerzugangs-Loader. Kein neuer URL-, Storage-, Config- oder globaler Aktivierungsschalter. Vorhandene Auth-Globals allein aktivieren nichts.

- A=false, Z=false: bisheriger lokaler Start einschließlich vorhandener injizierter Zugangsprovider; keine Auth-/Session-Aufrufe.
- A=false, Z=true: bisheriger Teilnehmerzugangs-Loader-/Provider-Pfad; keine Auth-/Session-Aufrufe.
- A=true, Z=false: Auth-Readiness, Sessionprüfung, danach bestehende Teilnehmerzugangsprüfung. Ein bereits kontrolliert bereitgestellter Zugangsprovider darf entscheiden; fehlt er oder ist er ungültig, generisch sperren. Kein lokaler Freigabe-Fallback.
- A=true, Z=true: Auth-Readiness, Sessionprüfung, Zugangs-Readiness, bestehende Teilnehmerzugangsprüfung. Nur deren positives access_allowed erlaubt den Start.

Fehlendes Script oder fehlendes/anderes Attribut ist keine Anforderung. Großschreibung, Leerzeichen, Boolean true und "1" sind nicht das exakte "true". Eine strukturell fehlende DOM-Lookup-Funktion erhält den bisherigen lokalen Testpfad. Geworfene Fehler beim Lesen vorhandener Aktivierungsgrenzen werden technisch fail-closed behandelt und dürfen keinen lokalen Fallback auslösen. Aktivierung pro Startversuch einmal erfassen und während asynchroner Wartezeiten nicht herabstufen.

Verbindliche Abnahmekriterien:

1. Lokale Auth-Guard-Testzustände und bestehende lokale Sperren behalten Vorrang: vorhandenen Hinweis anzeigen, keine Session-/Zugangsoperation und kein Warten auf Loader bei lokaler Sperre.
2. Angeforderter Auth-Modus verzweigt vor loadOptionalSupabaseConfig() in die kontrollierte Startprüfung. Kein Aufruf dieser Nachladefunktion, keine zusätzliche Health-/Config-Aktion durch den neuen Zweig; bestehende lokale Sperrprüfung bleibt erforderlich. Kein SDK-/Config-Nachladen und keine Client-Erzeugung.
3. Auf ACCAOUI_PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_READY warten. Nur ein eingefrorener einfacher Datensatz mit exakt eigenen Datenfeldern requested=true, ready=true, status="ready" erlaubt Fortsetzung. Fehlende/ungültige Grenze, Getterfehler, Reject und Fehlerzustand führen zu access_error. Ausstehende Bereitschaft erlaubt weder Sessionauflösung noch Freigabe.
4. Ausschließlich ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER.resolveSession() genau einmal, mit Provider als this und ohne Argumente kontrolliert aufrufen. Keine Adapter-/Bridge-Komposition, direkten Client-/Auth-/Session- oder Datenbankaufrufe im neuen App-Code.
5. Nur der gültige eingefrorene einfache Datensatz mit exakt eigenen Datenfeldern ok=true und code="session_available" führt zur Zugangsprüfung. Gültige ok=false/session_missing oder session_invalid führen zu login_required. auth_error, Throw, Reject, unbekannte Codes, widersprüchliche Werte, zusätzliche/geerbte/accessor-basierte Felder oder ungültige Provider führen generisch zu access_error. Keine Rohfehler, Sessiondaten oder Tokens in UI, Logs oder neuen Globals.
6. Gültige Session allein startet niemals die App. Vorhandenen resolveParticipantAccessAppProviderV2736D() und seine Ergebnis-/Hinweiszuordnung erhalten. Bei Z=true vorher bestehende Zugangs-Readiness abwarten. Fehlender Provider und alle Ablehnungen bleiben gesperrt. Eine inzwischen fehlende/ungültige Session in der erneuten Zugangsprüfung darf ebenfalls nicht freigeben.
7. Wiederholte, parallele oder erneut ausgelöste Boot-/Auth-Flow-Aufrufe teilen einen einzigen Startversuch: höchstens ein resolveSession(), ein resolveAccess() und ein startLocalApp() pro Seitenkontext. Nach Fehler kein späteres Wiederöffnen oder doppeltes Rendern. Keine Überschreibung von Provider-/Readiness-Globals.
8. Neuer synthetischer Checker prüft alle vier Schalterkombinationen, exaktes true, Globals ohne Anforderung, verzögerte Readiness, Ergebnisvalidierung, Fehlerpfade, lokale Vorränge, fehlenden Zugangsprovider mit und ohne Z, Ablehnungen trotz Session, Aufrufreihenfolge/-zahlen und parallelen/mehrfachen Start. Gesamten DOMContentLoaded-/initAppBoot-Pfad einschließlich Config-Nachladeverbot testen; positive lokale Regression erhalten.
9. Echte lokale Provider-/Adapterketten mit synthetischem vorhandenen Client testen: Session plus verweigerter Teilnehmer-/Enrollment-/Kurszugang bleibt gesperrt. signIn/signOut, Client-Erzeugung, SDK-/Config-Laden und fremde Netzwerkoperationen mit Spies als unerlaubt erfassen. Keine echten Keys, Teilnehmerdaten oder Live-Verbindung.
10. Semantische Negativmutationen müssen Session-only-Freigabe, fehlenden Provider-Fallback, übersprungene Readiness, gelockertes true, doppelten Start und Config-Nachladung erkennen. Historische Harnesses und Mutationen bleiben verpflichtend.

Unverändert bleiben index.html (beide Loader data-enabled="false"), beide Browser-Loader, beide Provider, alle Auth-/Session- und Teilnehmerzugangsadapter/-brücken, Bootstrap, SDK, Config, Login-UI, SQL/Migrationen und historische Einzelchecker. Kein Loginformular, kein signIn/signOut, keine automatische Anmeldung, kein Logout-Flow und keine Live-Aktivierung.

Der Lifecycle umfasst von Anfang an exakt:

- `v2737f_authorization_prepared`: Basis-HEAD, autorisierter Task, exakt sechs Gate-Dateien.
- `v2737f_authorization_committed`: ein direkter Gate-Commit, autorisierter Task, sauberer Working Tree.
- `v2737f_implementation_prepared`: Gate committet, autorisierter Task, exakt vier Implementierungsdateien.
- `v2737f_implementation_committed`: eine direkte Implementation, autorisierter Task, sauberer Working Tree.
- `v2737f_closure_prepared`: Implementation committet, geschlossener Task, exakt vier Steuerungsdokumente.
- `v2737f_closure_committed`: eine direkte Closure, geschlossener Task, sauberer Working Tree.

Gate-Dateien sind exakt docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md, docs/PROJECT_MASTERLIST.md, docs/PROJECT_STATE_CURRENT.md, docs/tasks/CURRENT_TASK.md, tools/check-project-continuity-control.py und tools/preflight.py. Closure-Dateien sind exakt die vier Steuerungsdokumente. v2737f_completion_documents erzeugt die Closure mit dem tatsächlichen Implementierungscommit: CURRENT_TASK NONE / BLOCKED / Autorisiert NEIN, letzter Kontrollschritt v27.37f, funktionaler Stand weiterhin v27.35g, kein Folgetask autorisiert.

Alle Zwischencommits werden einzeln gegen exakte Rollen, Dateiumfänge und Dokumentfassungen geprüft. Direkte lineare Übergänge, leerer Staging-Bereich, unveränderte historische Abschnitte und legitime origin/main-Vorfahren sind erforderlich. Kein Überspringen, Wiederholen, Merge, fremder Commit, Wiederöffnen, versteckte zwischenzeitliche Produktänderung oder unbekannter Folgetask. Keine zukünftigen Commit-SHAs hartcodieren.

Das enge zentrale Nachfolgeprofil validiert zuerst die vollständige v27.37e-Closure an dieser historischen Basis und danach den aktuellen v27.37f-Vertrag. Historische Einzelchecker bleiben unverändert. Ihre eingefrorenen Quellen und Produktgrenzen werden geprüft. Derselbe v27.37d-Provider-Harness, v27.37e-Loader-Harness einschließlich aller sechs Mutationen sowie v27.36d-/v27.36f-App-/Loader-Harnesses einschließlich ihrer Mutationen laufen gegen aktuelle erlaubte Quellen. Kein pauschales PASS. Der neue v27.37f-Checker wird ab Implementation verpflichtend registriert; vorher keine Implementierungsartefakte.

Kontinuitätschecker einschließlich isolierter Lifecycle-Positiv-/Negativtests, vollständiger Preflight einschließlich Regressionen, git diff --check und exakter Phasenscope bleiben verpflichtend. Isolierte Lifecycle-Tests verändern weder Dateien noch echte Git-Historie.

Letzter funktionaler Stand bleibt v27.35g, letzter abgeschlossener Kontrollschritt bis zur Closure v27.37e. Supabase bleibt NICHT LIVE. Commit und Push bleiben gesperrt.

Die folgenden Abschnitte dokumentieren historische Abschlüsse und Autorisierungen; sie erteilen keine weitere aktuelle Freigabe.

## Abgeschlossener technischer Schritt v27.37e

v27.37e – Auth-/Session-Browser-Loader ist abgeschlossen.

Implementierungscommit: `a8fe8a6081625c5a9c14b854fedb841613470a2f`.

Der Loader ist deaktiviert eingebunden. Die vorhandene Auth-/Session-Kette und app.js bleiben unverändert. Supabase bleibt NICHT LIVE.

Kein Folgetask ist autorisiert. Commit und Push bleiben gesperrt.

Die folgenden Abschnitte dokumentieren historische Abschlüsse und Autorisierungen; sie erteilen keine weitere aktuelle Freigabe.

## Autorisierter Task v27.37e

v27.37e – Auth-/Session-Browser-Loader ist ausschließlich als späterer Implementierungstask autorisiert.

Technische Gate-Basis: `bdb1f08c0c22cbb00c18ae9c13ea539abd4b919c`.

Dieses direkte Gate erhält den vollständig abgeschlossenen v27.37d-Verlauf. Es benötigt keinen zusätzlichen Bootstrap und autorisiert keinen unbekannten Folgetask. Die Implementation bleibt bis zum direkten Commit dieses Autorisierungs-Gates gesperrt.

Der spätere Implementierungsscope umfasst exakt:

- `data/supabase-participant-auth-session-browser-loader.js`
- `index.html`
- `tools/check-participant-auth-session-browser-loader-v2737e.py`
- `docs/PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_V2737E.md`
- `tools/preflight.py`

Keine sechste Implementierungsdatei ist zulässig. In diesem Gate wird noch keine dieser Produktdateien erstellt oder geändert.

Der Loader bleibt standardmäßig deaktiviert. Nur das exakte Attribut `data-enabled="true"` fordert die lokale Kette an; fehlende, andere oder fehlerhaft gelesene Werte laden keine Module.

Die lokale Ladefolge ist exakt:

1. `data/supabase-participant-auth-session-adapter.js`
2. `data/supabase-participant-auth-session-bootstrap-bridge.js`
3. `data/supabase-participant-auth-session-browser-provider.js`

Jede Stufe wird erst nach erfolgreichem Laden und Prüfung ihrer erwarteten Factory beziehungsweise Provider-Oberfläche fortgesetzt. Bestehende eigene oder geerbte Globals, einschließlich mit undefined belegter Grenzen, werden nicht überschrieben. Ein mehrfacher Ladeversuch darf keine zweite Kette starten.

Die Loader-ID lautet `accaoui-participant-auth-session-browser-loader`. Die einzige neue Bereitschaftsgrenze heißt `ACCAOUI_PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_READY`. Eine angeforderte Kette liefert einen eindeutigen eingefrorenen Bereitschafts- oder Fehlerzustand; Lade-, Grenz- und Prüfungsfehler bleiben fail-closed und geben keine Rohfehler aus.

Beim Laden finden keine Auth-, Session- oder Clientoperationen statt. Keine SDK-/Config-Nachladung, keine Live-Aktivierung, kein eigener Netzwerk- oder Datenbankzugriff und keine SQL-/Migrationsänderung. Das Laden der drei fest vorgegebenen lokalen Scriptressourcen ist die einzige erlaubte Ressourcenanforderung.

`index.html` erhält später ausschließlich eine zusätzliche deaktivierte Loader-Einbindung unmittelbar vor dem bestehenden app.js-Script. Die bestehende Teilnehmerzugangs-Loader-Einbindung bleibt unverändert deaktiviert. `app.js`, die vorhandenen Auth-/Session-Bausteine, Bootstrap, SDK, Config und sämtliche historischen Einzelchecker bleiben unverändert.

Der Lifecycle umfasst von Anfang an exakt:

- `v2737e_authorization_prepared`: Basis-HEAD, autorisierter Task und exakt die sechs Gate-Dateien.
- `v2737e_authorization_committed`: genau ein direkter Gate-Commit, autorisierter Task und sauberer Working Tree.
- `v2737e_implementation_prepared`: Gate committet, autorisierter Task und exakt die fünf Implementierungsdateien.
- `v2737e_implementation_committed`: genau eine direkte Implementation, autorisierter Task und sauberer Working Tree.
- `v2737e_closure_prepared`: Implementation committet, geschlossener Task und exakt die vier Steuerungsdokumente.
- `v2737e_closure_committed`: genau eine direkte Closure, geschlossener Task und sauberer Working Tree.

Gate-Dateien sind exakt die vier Steuerungsdokumente, `tools/check-project-continuity-control.py` und `tools/preflight.py`. Closure-Dateien sind exakt die vier Steuerungsdokumente. Nach der Implementation bleiben die fünf Implementierungsdateien während der Closure unverändert.

Phasen, Commitrollen und Übergänge werden aus linearer Git-Historie, Dokumentvertrag und exaktem Dateiumfang abgeleitet. Übersprungene, wiederholte oder fremde Übergänge sowie Wiederöffnung nach Closure sind verboten. Keine zukünftigen Commit-SHAs werden hartcodiert.

Die v27.37d-Regression bleibt verpflichtend: bis zur Loader-Implementation läuft der unveränderte Provider-Einzelchecker direkt; danach prüft ein enges zentrales Nachfolgeprofil die unveränderten Provider-/Checkerbytes, die exakt erlaubte deaktivierte Index-Ergänzung und denselben historischen synthetischen Provider-Harness. Kein pauschales PASS und kein allgemeiner Bypass.

In der Implementation darf `tools/preflight.py` ausschließlich den fest vorgegebenen Loader-Checker registrieren; alle übrigen Prüfungen bleiben erhalten. Die Closure verändert weder Checker noch Preflight.

Der spätere Loader-Checker muss Deaktivierung, exaktes true, Reihenfolge, Readiness, Fehlerpfade, globale Kollisionen, Mehrfachladung und passive Auth-/Session-Kette lokal synthetisch prüfen. Continuity, vollständiger Preflight, bestehende Regressionen und isolierte Lifecycle-Übergangstests bleiben verpflichtend.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g; der letzte abgeschlossene Kontrollschritt bleibt bis zur v27.37e-Closure v27.37d. Commit und Push bleiben gesperrt. Supabase bleibt NICHT LIVE. Keine echten Keys und keine echten Teilnehmerdaten.

Die folgenden Abschnitte dokumentieren historische Abschlüsse und Autorisierungen; sie erteilen keine weitere aktuelle Freigabe.

## Abgeschlossener technischer Schritt v27.37d

v27.37d abgeschlossen.

Implementierungscommit: `3a3933ceb85e83bac19ca71cc960ecb1674f9a38`

Ergebnis:

- Isolierter Browser-Provider `ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER` umgesetzt.
- Öffentliche Oberfläche bleibt exakt `resolveSession()`, `signIn()` und `signOut()`.
- Die Auth-/Session-Kette wird ausschließlich lazy beim Methodenaufruf komponiert.
- Gültige Bridge-Ergebnisse bleiben unverändert; Fehler werden fail-closed als `auth_error` behandelt.
- Bereits vorhandene Browser-Grenzen werden nicht überschrieben.
- Kein `initializeClient()`, `createClient()`, `getState()`, eigener `getClient()`-Aufruf, Netzwerkcode, SQL oder Migrationen.
- `index.html`, `app.js`, Auth-/Session-Adapter und Bootstrap-Brücke blieben unverändert.
- Der dedizierte v27.37d-Browser-Provider-Checker bestand vor dem Implementierungscommit.
- Der Abschluss ergänzt ausschließlich die fehlende Post-Commit-/Nachfolger-Kontrollphase; historische v27.36e-/v27.36f-Checker bleiben unverändert.
- Supabase bleibt NICHT LIVE.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g.
Kein Folgetask ist ausgewählt oder autorisiert.

## Autorisierter Task v27.37d

Das frische v27.37d-Autorisierungs-Gate autorisiert ausschließlich den Task `v27.37d – Isolierter Browser-Provider für Teilnehmer-Auth-/Session-Kette`.

Technische Gate-Basis: `b5a0bd686d0e953893ea78976b6726897446ce63`.

Die lineare Git-Historie muss vor diesem Gate den einmaligen v27.37d-Bootstrap und dessen einmaligen Repair enthalten.

Der spätere Implementierungsscope umfasst exakt:

- `data/supabase-participant-auth-session-browser-provider.js`
- `tools/check-participant-auth-session-browser-provider-v2737d.py`
- `docs/PARTICIPANT_AUTH_SESSION_BROWSER_PROVIDER_V2737D.md`
- `tools/preflight.py`

Keine fünfte Implementierungsdatei ist zulässig.

Ziel ist ausschließlich ein isolierter Browser-Provider an `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER`.

Der Provider darf ausschließlich `window.ACCAOUI_SUPABASE_BOOTSTRAP`, `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY` und `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY` kontrolliert komponieren.

Die öffentliche Oberfläche darf nur `resolveSession()`, `signIn()` und `signOut()` bereitstellen. Die Komposition erfolgt erst bei einem Methodenaufruf. Beim Laden dürfen keine Auth-, Session- oder Client-Aktionen stattfinden.

Fehlende oder ungültige Abhängigkeiten sowie Fehler und ungültige Ergebnisse müssen fail-closed behandelt werden. Bestehende Browser-Grenzen dürfen nicht überschrieben werden.

Verboten bleiben insbesondere `initializeClient()`, `createClient()`, `getState()`, automatisches SDK-/Config-Laden, `index.html`, `app.js`, Login-UI, eigener Netzwerkcode, `.from(...)`, SQL, Migrationen, echte Keys und echte Teilnehmerdaten.

Der Lifecycle erkennt diese Vorbereitung als `v2737d_authorization_prepared`. Nach einem direkten Autorisierungs-Commit muss `v2737d_authorization_committed` erkannt werden; erst danach darf `v2737d_implementation_prepared` zulässig werden. Keine zukünftige Autorisierungs- oder Implementierungs-SHA wird hartcodiert.

Supabase bleibt NICHT LIVE. Commit und Push bleiben bis zur erfolgreichen Prüfung dieses Autorisierungs-Gates gesperrt.

## v27.37d-GATE-BOOTSTRAP-REPAIR – Kontrollinfrastruktur

v27.37d-GATE-BOOTSTRAP-REPAIR ist ausschließlich Kontrollinfrastruktur.

Stabile Repair-Basis: `68f5525e27de6fa37176125191f960494ed5aedd`.

Der Repair korrigiert ausschließlich die v27.37c-Historiengrenze.

Der einmalige atomare Repair umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Repair-Datei ist zulässig.

v27.37c bleibt vollständig abgeschlossen und wird nicht wieder geöffnet.

CURRENT_TASK bleibt NONE / BLOCKED / nicht autorisiert.

Der Repair kennt ausschließlich `v2737d_gate_bootstrap_repair_prepared` und `v2737d_gate_bootstrap_repair_committed`.

Der spätere v27.37d-Provider-Task wird durch diesen Repair NICHT autorisiert.

Supabase bleibt NICHT LIVE.

## v27.37d-GATE-BOOTSTRAP – Kontrollinfrastruktur

v27.37d-GATE-BOOTSTRAP ist ausschließlich Kontrollinfrastruktur.

Stabile Bootstrap-Basis: `7211e9449a4478d31688daefa313a8722b82da76`.

Der einmalige atomare Bootstrap umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Bootstrap-Datei ist zulässig.

Der spätere Implementierungsscope umfasst exakt:

- `data/supabase-participant-auth-session-browser-provider.js`
- `tools/check-participant-auth-session-browser-provider-v2737d.py`
- `docs/PARTICIPANT_AUTH_SESSION_BROWSER_PROVIDER_V2737D.md`
- `tools/preflight.py`

Keine fünfte Implementierungsdatei ist zulässig.

v27.37c bleibt vollständig abgeschlossen und wird nicht wieder geöffnet.

Der spätere Task heißt exakt `v27.37d – Isolierter Browser-Provider für Teilnehmer-Auth-/Session-Kette`, ist durch diesen Bootstrap aber NICHT autorisiert.

Die spätere Browser-Grenze heißt `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER`.

Sie darf ausschließlich den vorhandenen `window.ACCAOUI_SUPABASE_BOOTSTRAP`, `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY` und `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY` kontrolliert komponieren.

Die spätere öffentliche Oberfläche darf nur `resolveSession()`, `signIn()` und `signOut()` bereitstellen.

`index.html` und `app.js` bleiben in diesem Bootstrap und in der späteren Provider-Implementierung gesperrt.

Dieser Bootstrap kennt ausschließlich `v2737d_gate_bootstrap_prepared` und `v2737d_gate_bootstrap_committed`. Er autorisiert weder eine Implementation noch einen weiteren Folgetask.

Supabase bleibt NICHT LIVE.

## Abgeschlossener technischer Schritt v27.37c

v27.37c abgeschlossen.

Implementierungscommit: `31b9893fb82a9fbafd72856b113d95655aaf2cba`

Ergebnis:

- Kontrollierte Browser-Factory `ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY` umgesetzt.
- Kontrollierte Browser-Factory `ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY` umgesetzt.
- Bestehende CommonJS-Verträge bleiben erhalten.
- Bereits belegte Browser-Grenzen werden nicht überschrieben.
- Beim Laden erfolgen keine Auth-Operation, keine Sessionauflösung und kein Clientzugriff.
- Adapter-Checker: 11 Positiv-, 57 Negativ- und 20 Manipulationsprüfungen PASS.
- Bootstrap-Bridge-Checker: 44 Positiv-, 397 Negativ- und 49 Manipulationsprüfungen PASS.
- Semantische Bridge-Manipulationen: 26 PASS.
- Preflight: PASS.
- `git diff --check`: PASS.
- Supabase bleibt NICHT LIVE.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g.
Kein Folgetask ist ausgewählt oder autorisiert.

## Autorisierter Task v27.37c

Das frische v27.37c-Autorisierungs-Gate autorisiert ausschließlich den Task `v27.37c – Kontrollierte Browser-Export-Grenze für Teilnehmer-Auth-/Session-Factories`.

Technische Gate-Basis: `c2931bba8fb1799e2f55dcb505fb1202dfc9e09a`.

Die lineare Git-Historie muss vor diesem Gate dynamisch genau den einmaligen `v2737c_bootstrap` enthalten.

Der spätere Implementierungsscope umfasst exakt:

- `data/supabase-participant-auth-session-adapter.js`
- `data/supabase-participant-auth-session-bootstrap-bridge.js`
- `tools/check-supabase-participant-auth-session-adapter.py`
- `tools/check-supabase-participant-auth-session-bootstrap-bridge.py`
- `docs/SUPABASE_PARTICIPANT_AUTH_SESSION_BROWSER_EXPORT_V2737C.md`
- `tools/preflight.py`

Keine siebte Implementierungsdatei ist zulässig.

Ziel ist ausschließlich die kontrollierte Browser-Export-Grenze der beiden bereits bestehenden Auth-/Session-Factories. CommonJS-Verhalten, öffentliche Factory-Verträge und bestehende Auth-/Session-Fachlogik bleiben erhalten.

Die erlaubten Browser-Grenzen heißen exakt:

- `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY`
- `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY`

Eine Grenze darf nur gesetzt werden, wenn sie noch unbelegt ist. Bestehende Grenzen dürfen nicht überschrieben werden. Beim Laden dürfen keine Auth-Operation, keine Sessionauflösung und kein Clientzugriff stattfinden.

Verboten bleiben insbesondere `initializeClient()`, `createClient()`, `getState()`, automatisches SDK-/Config-Laden, `index.html`, `app.js`, Login-UI, eigener Netzwerkcode, `.from(...)`, SQL, Migrationen, echte Keys und echte Teilnehmerdaten.

Der Lifecycle erkennt diese Vorbereitung als `v2737c_authorization_prepared`. Nach einem direkten Autorisierungs-Commit muss `v2737c_authorization_committed` erkannt werden; erst danach darf `v2737c_implementation_prepared` zulässig werden. Keine zukünftige Autorisierungs-, Implementierungs- oder Closure-SHA wird hartcodiert.

Supabase bleibt NICHT LIVE. Commit und Push bleiben bis zur erfolgreichen Prüfung gesperrt.

## v27.37c-GATE-BOOTSTRAP – Kontrollinfrastruktur

v27.37c-GATE-BOOTSTRAP ist ausschließlich Kontrollinfrastruktur.

Stabile Bootstrap-Basis: `41c14d89d7557abe64933a72cd6eb7f2272d075e`.

Der einmalige atomare Bootstrap umfasst exakt:

- `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`
- `docs/PROJECT_MASTERLIST.md`
- `docs/PROJECT_STATE_CURRENT.md`
- `docs/tasks/CURRENT_TASK.md`
- `tools/check-project-continuity-control.py`
- `tools/preflight.py`

Keine siebte Datei und keine Produktdatei sind zulässig. v27.37b bleibt vollständig abgeschlossen und wird nicht wieder geöffnet.

Der spätere Task heißt exakt `v27.37c – Kontrollierte Browser-Export-Grenze für Teilnehmer-Auth-/Session-Factories`, ist durch diesen Bootstrap aber NICHT autorisiert. Der aktuelle Task bleibt NONE / BLOCKED / nicht autorisiert. Commit und Push bleiben gesperrt.

Der spätere Implementierungsscope umfasst exakt:

- `data/supabase-participant-auth-session-adapter.js`
- `data/supabase-participant-auth-session-bootstrap-bridge.js`
- `tools/check-supabase-participant-auth-session-adapter.py`
- `tools/check-supabase-participant-auth-session-bootstrap-bridge.py`
- `docs/SUPABASE_PARTICIPANT_AUTH_SESSION_BROWSER_EXPORT_V2737C.md`
- `tools/preflight.py`

Ziel ist ausschließlich eine kontrollierte Browser-Export-Grenze für die bereits bestehenden Factories. Die CommonJS-Oberflächen und das bestehende Auth-/Session-Verhalten bleiben fachlich unverändert.

Die vorgesehenen Browser-Grenzen heißen exakt:

- `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY`
- `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY`

Ein Browser-Export darf nur eine noch nicht belegte Grenze setzen, keine bestehende Grenze überschreiben und beim Laden keine Auth-Operation, keinen Clientzugriff und keine Sessionauflösung ausführen.

Verboten bleiben insbesondere `initializeClient()`, `createClient()`, `getState()`, automatisches SDK-/Config-Laden, `index.html`, `app.js`, Login-UI, eigener Netzwerkcode, `.from(...)`, SQL, Migrationen, echte Keys und echte Teilnehmerdaten.

Dieser Bootstrap kennt ausschließlich die einmalige Vorbereitung `v2737c_gate_bootstrap_prepared` und nach einem direkten Sechs-Dateien-Commit `v2737c_gate_bootstrap_committed`. Erst danach darf ein separates ausdrückliches v27.37c-Autorisierungs-Gate vorbereitet werden. Keine zukünftige Autorisierungs-, Implementierungs- oder Closure-SHA wird hartcodiert.

Kein Produktcode wird durch diesen Bootstrap geändert. Supabase bleibt NICHT LIVE.

## Abgeschlossener technischer Schritt v27.37b

v27.37b abgeschlossen.

Implementierungscommit: `dfa54c5327fb411d2624b05c064a214da18f3b54`

Ergebnis:

- Die isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke ist implementiert und CommonJS-only.
- Die Factory ist `createParticipantAuthSessionBootstrapBridge({ bootstrap, createParticipantAuthSessionAdapter })`.
- Die Dependencies sind exakt `bootstrap` und `createParticipantAuthSessionAdapter`.
- Die öffentliche Oberfläche enthält exakt `resolveSession()`, `signIn(credentials)` und `signOut()` und ist eingefroren.
- `require()` und Factory-Erzeugung verursachen keine Side Effects.
- Pro öffentlicher Operation wird `getClient()` exakt einmal aufgerufen; der Client wird nicht gecacht.
- Ausschließlich `client.auth` wird als exakt `{ auth }` an die Adapterfactory weitergegeben.
- Der Adapter wird pro Operation frisch erzeugt; nur die passende Methode wird genau einmal aufgerufen.
- Credentials werden unverändert weitergegeben; gültige v27.37a-Ergebnisse werden unverändert und identisch delegiert.
- Brückenfehler liefern exakt `Object.freeze({ ok: false, code: "auth_error" })`.
- Sensitive Daten, Session-, User-, Passwort-, Token-, Client-, Auth-, Config- und Rohfehlerwerte werden nicht ausgegeben.
- Es gibt keine Browser-, Storage-, Netzwerk- oder eigene Domainlogik.
- Supabase bleibt NICHT LIVE. Keine echten Keys. Keine echten Teilnehmerdaten.

Bestätigte Testergebnisse der Implementation:

- Positiv: 40 PASS.
- Negativ: 397 PASS.
- Manipulation: 49 PASS.
- Shared-Fake signIn -> access_allowed: PASS.
- Shared-Fake signOut -> session_missing: PASS.
- Continuity: PASS.
- Preflight: PASS.
- v27.36b: PASS.
- v27.36c: PASS.
- v27.36d Regression: PASS.
- v27.36e Regression: PASS.
- v27.36f Regression: PASS.
- v27.37a Regression: PASS.
- v27.37b Nachfolgeprofil: PASS.
- `git diff --check`: PASS.

### Permanenter v27.37b-Lifecycle

Die legitime Historie enthält genau einmal und in dieser Reihenfolge `v2737b_bootstrap`, `v2737b_bootstrap_repair`, `v2737b_gate` und `v2737b_implementation`.

`v2737b_closure_prepared` verlangt die abgeschlossene Implementation, exakt die fünf Closure-Dateien im Working Tree und den kanonischen CLOSED-Kopf: `Task-ID: NONE`, `Status: BLOCKED`, `Autorisiert: NEIN`, `Titel: Kein Task autorisiert`, `Funktionaler Ausgangsstand: v27.35g`, `Letzter abgeschlossener Kontrollschritt: v27.37b`, `Erlaubte Implementierungsdateien: KEINE`, `Commit erlaubt: NEIN` und `Push erlaubt: NEIN`.

Die fünf Closure-Dateien sind ausschließlich `docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md`, `docs/PROJECT_MASTERLIST.md`, `docs/PROJECT_STATE_CURRENT.md`, `docs/tasks/CURRENT_TASK.md` und `tools/check-project-continuity-control.py`. Produkt- und Implementierungsdateien sowie `tools/preflight.py` bleiben unverändert.

Ein späterer legitimer direkter Closure-Commit wird dynamisch als `v2737b_closure_committed` erkannt. Keine zukünftige Closure-SHA wird hartcodiert. Eine zweite Implementation, eine zweite Closure, eine Rückkehr zur Autorisierung und unbekannte Folgetasks bleiben blockiert.

Der letzte abgeschlossene funktionale Stand bleibt v27.35g. Der letzte abgeschlossene Kontrollschritt ist v27.37b.

Kein Folgetask wurde ausgewählt oder autorisiert. Commit und Push bleiben NEIN.

Die folgenden Autorisierungs-, Bootstrap- und Repair-Abschnitte dokumentieren unverändert die historische Freigabe und Kontrollinfrastruktur; sie erteilen keine aktuelle Implementierungs- oder Folgetaskfreigabe.

## Autorisierter Task v27.37b

Das frische v27.37b-Autorisierungs-Gate autorisiert ausschließlich den späteren Task `v27.37b – Isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke`.

Technische Gate-Basis: `8f56e6459f75b4dfd50e7d792dd56d6443d58fd3`.

Die lineare Git-Historie muss vor diesem Gate dynamisch genau `v2737b_bootstrap` und `v2737b_bootstrap_repair` enthalten.

Der spätere Implementierungsscope umfasst exakt:

- `data/supabase-participant-auth-session-bootstrap-bridge.js`
- `tools/check-supabase-participant-auth-session-bootstrap-bridge.py`
- `docs/SUPABASE_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_V2737B.md`
- `tools/preflight.py`

Keine fünfte Implementierungsdatei und keine Produktdatei sind zulässig.

Die Factory ist `createParticipantAuthSessionBootstrapBridge({ bootstrap, createParticipantAuthSessionAdapter })`. Die Dependencies sind exakt `bootstrap` und `createParticipantAuthSessionAdapter`; eine dritte Dependency ist ausgeschlossen. Die öffentliche Oberfläche enthält exakt `resolveSession()`, `signIn({ email, password })` und `signOut()`; eine vierte öffentliche Methode ist ausgeschlossen.

Pro öffentlicher Operation wird `bootstrap.getClient` sicher gelesen, `getClient()` exakt einmal aufgerufen und der Client nicht gecacht. Ausschließlich `client.auth` wird als `{ auth }` an den bestehenden v27.37a-Adapter weitergegeben. Gültige v27.37a-Ergebnisse werden unverändert delegiert. Jeder Brückenfehler liefert exakt `Object.freeze({ ok: false, code: "auth_error" })`; sensitive Session-, User-, ID-, E-Mail-, Passwort-, Token-, Config- und Rohfehlerdaten bleiben ausgeschlossen.

Verboten bleiben `initializeClient()`, `createClient()`, `getState()`, Browser-Wiring oder Browser-Export, `window`, `document`, DOM, `localStorage`, `sessionStorage`, Cookies, IndexedDB, Config-Lesen, eigener Netzwerkcode, `.from(...)`, Teilnehmer-, Enrollment- oder Kurslogik, SQL, Migrationen, echte Keys und echte Teilnehmerdaten.

Der Lifecycle erkennt die Vorbereitung als `v2737b_authorization_prepared`, verlangt den legitimen einmaligen Bootstrap und Repair, den AUTHORIZED-Kopf sowie ausschließlich die fünf Gate-Dateien. Nach dem späteren direkten Gate-Commit wird dynamisch `v2737b_authorization_committed` erkannt; erst danach ist `v2737b_implementation_prepared` zulässig. Keine zukünftige Gate-, Implementierungs- oder Closure-SHA wird hartcodiert.

Supabase bleibt NICHT LIVE.


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

Titel: Enges Preflight-Nachfolgeprofil nach abgeschlossenem v27.36f bootstrapen.

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
