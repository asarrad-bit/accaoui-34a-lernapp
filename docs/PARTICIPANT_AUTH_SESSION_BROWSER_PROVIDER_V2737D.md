# v27.37d – Teilnehmer-Auth-/Session-Browser-Provider

## Ziel

v27.37d ergänzt ausschließlich einen isolierten Browser-Provider für die bestehende Teilnehmer-Auth-/Session-Kette.

Browser-Grenze:

`window.ACCAOUI_PARTICIPANT_AUTH_SESSION_APP_PROVIDER`

Öffentliche Oberfläche:

- `resolveSession()`
- `signIn()`
- `signOut()`

## Sicherheitsgrenze

Der Provider komponiert ausschließlich:

- `window.ACCAOUI_SUPABASE_BOOTSTRAP`
- `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY`
- `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY`

Die Komposition erfolgt erst bei einem Methodenaufruf.

Beim Laden des Moduls findet keine Auth-, Session- oder Client-Aktion statt.

## Ergebnisvertrag

Gültige Ergebnisse der bestehenden Bootstrap-Brücke werden unverändert zurückgegeben.

Provider-, Dependency-, Factory-, Bridge- oder Ergebnisfehler werden ausschließlich fail-closed behandelt als:

`{ ok: false, code: "auth_error" }`

Es wird keine neue Auth-/Session-Fachlogik eingeführt.

## Bestehende Grenzen

Eine bereits vorhandene Browser-Grenze wird nicht überschrieben.

Dies gilt auch dann, wenn eine bereits vorhandene Property den Wert `undefined` besitzt oder über die Prototype-Kette vorhanden ist.

Der installierte Provider ist eingefroren und wird als nicht überschreibbare, nicht konfigurierbare Browser-Property veröffentlicht.

## Verbotene Bereiche

v27.37d führt insbesondere nicht aus:

- `initializeClient()`
- `createClient()`
- `getState()`
- eigene `getClient()`-Aufrufe
- direkte Auth-Aufrufe
- `.from(...)`
- eigenen Netzwerkcode
- SQL
- Migrationen
- automatisches SDK-/Config-Laden

Nicht verändert werden:

- `index.html`
- `app.js`
- bestehender Auth-/Session-Adapter
- bestehende Auth-/Session-Bootstrap-Brücke

## Prüfung

Die Prüfung erfolgt ausschließlich lokal und synthetisch über:

`tools/check-participant-auth-session-browser-provider-v2737d.py`

Geprüft werden unter anderem:

- passive Modulinitialisierung
- exakt drei öffentliche Provider-Methoden
- Lazy-Komposition
- unveränderte gültige Brückenresultate
- fail-closed bei ungültigen Abhängigkeiten
- fail-closed bei Factory-/Bridge-Fehlern
- Ablehnung manipulierter Ergebnisse
- Schutz bestehender Browser-Grenzen
- eingefrorene Produktgrenzen
- unveränderte Bestandsdateien

## Betriebsstatus

Supabase live: NEIN

Echte Keys: NEIN

Echte Teilnehmerdaten: NEIN

`index.html`-Einbindung: NEIN

`app.js`-Einbindung: NEIN
