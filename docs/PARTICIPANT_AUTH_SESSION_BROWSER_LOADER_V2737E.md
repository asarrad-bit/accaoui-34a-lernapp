# v27.37e – Teilnehmer-Auth-/Session-Browser-Loader

## Umfang

Der Loader verbindet ausschließlich die drei vorhandenen lokalen Browser-Module.
Er enthält keine Auth-/Session-Fachlogik und erzeugt keinen Client.
Keine Auth-, Session- oder Clientoperation findet beim Laden statt.

Supabase bleibt NICHT LIVE. Keine echten Keys und keine echten Teilnehmerdaten.

## Aktivierung und lokale Ressourcen

Die Script-ID lautet `accaoui-participant-auth-session-browser-loader`.
Das ausführende klassische Script muss das über diese ID gefundene Script sein.
Nur der exakte String `data-enabled="true"` startet einen Ladeversuch.
Fehlende Elemente, fehlende Attribute, andere Werte und Fehler beim Lesen
bleiben ohne Modulanforderung und ohne neue Readiness-Grenze.

In der Anwendung bleibt die Einbindung bei `data-enabled="false"`.
Die zusätzliche Zeile steht unmittelbar vor dem bestehenden app.js-Script.
Der vorhandene Teilnehmerzugangs-Loader bleibt unverändert deaktiviert.

Es werden ausschließlich diese lokalen Ressourcen angefordert, in dieser Reihenfolge:

1. `data/supabase-participant-auth-session-adapter.js`
2. `data/supabase-participant-auth-session-bootstrap-bridge.js`
3. `data/supabase-participant-auth-session-browser-provider.js`

Die absoluten Ressourcen-URLs werden relativ zur tatsächlichen Dokument-URL
gebildet. Ein fremdes HTML-base-Ziel wird nicht verwendet. Erlaubt sind
HTTP/HTTPS-Dokumente ohne Benutzerinformationen in der URL. Der Loader lädt
keine SDK-, Config-, Fremd-, dynamisch übergebenen oder weiteren Scriptressourcen.

Jedes Script wird mit `async = false` eingefügt. Erst nach seinem load-Ereignis
und erfolgreicher Exportprüfung darf die nächste Stufe beginnen.
Jede Stufe hat ein Zeitlimit von 15000 Millisekunden.

## Kollisionsschutz und Prüfung der Exporte

Die drei erwarteten Grenzen sind:

- `ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY`
- `ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY`
- `ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER`

Vor jedem Einfügen werden alle noch zu ladenden Grenzen auf Anwesenheit
geprüft. Eigene und geerbte Properties gelten auch mit dem Wert undefined
als belegt. Bestehende Grenzen werden weder überschrieben noch als Ersatz
für eine neu geprüfte Ladestufe übernommen. Belegte Getter werden nicht gelesen.

Geladene Exporte müssen eigene, enumerable, nicht schreibbare und nicht
konfigurierbare Datenproperties sein. Adapter- und Bridge-Export müssen
Funktionen sein; sie werden bei der Prüfung nicht aufgerufen.
Der Provider muss ein eingefrorenes Plain Object mit exakt den drei eigenen
Datenmethoden `resolveSession`, `signIn` und `signOut` sein.
Accessor-Methoden, Zusatzfelder und ungültige Oberflächen werden abgelehnt.
Vor weiteren Stufen und vor der Bereitschaft werden bereits geprüfte
Exportidentitäten erneut geprüft.

## Readiness und Fehler

Die einzige neue öffentliche Loader-Grenze heißt:

`window.ACCAOUI_PARTICIPANT_AUTH_SESSION_BROWSER_LOADER_READY`

Bei einem angeforderten Start reserviert der Loader diese Grenze synchron,
bevor die erste Ressource angefordert wird. Ihr Wert ist ein eingefrorenes
Promise; die Property ist enumerable, nicht schreibbar und nicht konfigurierbar.
Sie verhindert einen zweiten Ladeversuch während der laufenden Kette und
nach deren Erfolg oder Fehler.

Das Promise bleibt während des Ladens ausstehend und erfüllt sich einmalig
mit einem dieser eingefrorenen Plain Objects:

- Erfolg: `{ requested: true, ready: true, status: "ready" }`
- Fehler: `{ requested: true, ready: false, status: "error" }`

Es gibt keine Ablehnung mit Rohfehlern, kein Logging interner Fehler und keine
Session-, Nutzer-, Token-, Passwort-, Client- oder Configwerte im Ergebnis.
Readiness bestätigt ausschließlich die geprüften Exporte. Sie bestätigt
weder eine Anmeldung noch eine Session, Zugangsberechtigung oder App-Freigabe.

Ist bereits die Readiness-Grenze selbst belegt, auch geerbt oder mit undefined,
wird sie unverändert gelassen und keine Ressource angefordert. Ein nicht
beschreibbares Window wird ebenso behandelt. Eine fehlende oder ungültige
Readiness-Grenze ist kein Bereitschaftsnachweis.

Ressourcenfehler, fehlende Exporte, Kollisionen, DOM-/Prüfungsfehler und
Zeitüberschreitungen enden geschlossen im Fehlerzustand. Pro Script wird
höchstens ein Ereignis angenommen. Timer und Handler werden aufgeräumt;
bei Fehlern wird das eingefügte Script nach Möglichkeit entfernt.
Späte oder doppelte Ereignisse starten keine weitere Kette und ändern
keinen abgeschlossenen Zustand. Es gibt keinen automatischen Retry oder Fallback.

Bereits erfolgreich installierte, unveränderliche Exporte werden bei einem
späteren Fehler nicht zurückgebaut. Auch ein verspätet abgeschlossenes
Script darf einen terminalen Fehlerzustand nicht zu ready ändern.
Ein späterer Verbraucher muss den Readiness-Erfolg ausdrücklich abwarten.

## Unveränderte Grenzen

Keine Factory und keine Provider-Methode wird durch den Loader aufgerufen.
Bootstrap, Auth, Session, Client, SDK, Config, Storage und Datenbank bleiben
unberührt. Keine Login-UI, keine App-Verkabelung, kein SQL und keine Migrationen.
Die bestehenden Auth-/Session-Bausteine und app.js bleiben unverändert.

## Lifecycle und Preflight

Die Umsetzung setzt `v2737e_authorization_committed` voraus.
Mit genau den fünf autorisierten Implementierungsdateien wird
`v2737e_implementation_prepared` erkannt. Die bestehende Kontrolllogik
bleibt unverändert und kennt bereits alle sechs Lifecycle-Phasen.

In `tools/preflight.py` wird ausschließlich die vorhandene Registrierung
`V2737E_IMPLEMENTATION_CHECKER` auf den festgelegten neuen Checkerpfad gesetzt.
Alle anderen Preflight-Zeilen bleiben unverändert.

Die v27.37d-Regression läuft nach der Index-Ergänzung über das bereits
autorisierte zentrale Nachfolgeprofil: unveränderte Provider-/Checkerquellen,
exakt deaktivierte Index-Ergänzung und derselbe historische Provider-Harness.
Historische Einzelchecker werden nicht bearbeitet.

## Lokale Prüfung

`py -3 -B tools/check-participant-auth-session-browser-loader-v2737e.py`

Der neue Checker prüft den echten Loader in einem synthetischen DOM und einer
isolierten JavaScript-VM. Die drei vorhandenen lokalen Module werden tatsächlich
ausgeführt. Bootstrap-, Config-, Storage- und Netzwerkgrenzen sind mit
fehlschlagenden Zugriffswächtern versehen; zusätzliche Factory-/Methodenwächter
belegen den passiven Ablauf. Es wird kein Browser-Netzwerk gestartet.

Abgedeckt sind Deaktivierung und exaktes true, feste lokale Reihenfolge,
ausstehende und abgeschlossene Readiness, unveränderliche Ergebnisse,
eigene/geerbte Kollisionen einschließlich undefined und Accessoren,
Kollisionen vor Folgestufen, wiederholte Loader-Ausführung, ungültige Exporte,
DOM-/Ressourcenfehler, Zeitüberschreitungen sowie doppelte und späte Ereignisse.
Semantisch manipulierte Loader-Fassungen werden ausschließlich im Arbeitsspeicher
geprüft und müssen durch dieselben Verhaltenstests scheitern.

Zusätzlich verpflichtend: Projektkontinuitätschecker, vollständiger Preflight
einschließlich v27.37d-Nachfolgeprofil, `git diff --check` und exakter
Fünf-Dateien-Scope. Keine echte Git-Historie wird für Tests verändert.

Commit und Push erfolgen ausschließlich nach gesondertem ausdrücklichem Auftrag.
