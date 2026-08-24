# Supabase-Teilnehmerzugangs-Bootstrap-Brücke v27.36c

Stand: v27.36c  
Implementierungszustand: lokal vorbereitet, nicht in die App integriert  
Supabase: **NICHT LIVE**

## 1. Ziel und Architektur

Die CommonJS-Brücke verbindet ausschließlich zwei bereits getrennte lokale
Komponenten: den vorhandenen Supabase-Bootstrap-Provider und den unveränderten
Teilnehmerzugangs-Adapter v27.36b. Sie besitzt keine eigene Teilnehmer-,
Enrollment-, Kurs- oder Zeitbewertungslogik.

Pro `resolveAccess()`-Aufruf liest die Brücke `bootstrap.getClient()` genau
einmal. Ist ein Client vorhanden, übergibt sie ihn zusammen mit der injizierten
UTC-Zeitquelle an die injizierte Adapter-Factory und delegiert die vollständige
Zugangsentscheidung an deren `resolveAccess()`.

Der vorhandene Bootstrap erzeugt oder initialisiert in diesem Schritt keinen
Client. Die Brücke verwendet keine globalen Objekte und keine Bootstrap-,
Config-, SDK- oder Live-State-Prüfung.

## 2. API

```js
const {
  createParticipantAccessBootstrapBridge
} = require("./data/supabase-participant-access-bootstrap-bridge.js");

const bridge = createParticipantAccessBootstrapBridge({
  bootstrap,
  createParticipantAccessAdapter,
  utcNow
});

const accessState = await bridge.resolveAccess();
```

### `injizierte Dependencies`

Die Factory akzeptiert exakt diese drei injizierten Dependencies:

- `bootstrap`: objektförmiger Provider; ausschließlich `getClient` wird gelesen.
- `createParticipantAccessAdapter`: bestehende v27.36b-Factory.
- `utcNow`: explizite UTC-Zeitquelle für den bestehenden Adapter.

Die öffentliche Brückenoberfläche enthält nur `version` und `resolveAccess`.
Eine frei injizierbare Nutzer- oder Teilnehmer-ID existiert nicht.
`session.user.id` bleibt ausschließlich Verantwortung und Nutzerautorität des
unveränderten v27.36b-Adapters.

## 3. Delegationsablauf

1. Exakte Dependency-Oberfläche prüfen.
2. `bootstrap.getClient` einmal lesen und einmal aufrufen.
3. Bei fehlendem Client geschlossen blockieren.
4. Vorhandenen Client ohne fachliche Clientprüfung an
   `createParticipantAccessAdapter({ client, utcNow })` übergeben.
5. `adapter.resolveAccess()` einmal delegiert ausführen.
6. Nur einen minimal gültigen Adapter-Ergebnisumschlag akzeptieren.
7. Ein gültiges Adapter-Ergebnis als dasselbe Objekt unverändert zurückgeben.

Ein vorhandener, aber fachlich ungültiger Client wird bewusst bis zum
v27.36b-Adapter durchgereicht. Dieser liefert dafür `client_invalid`. Die
Für die Brücke gilt damit: keine duplizierte Fachlogik für Client, Session,
Participant, Enrollment oder Course.

## 4. Fail-closed-Grenze und Fail-closed-Regeln

Die Brücke blockiert mit einem kleinen Ergebnis der Form
`{ allowed: false, code }` bei:

- fehlenden, ungültigen oder zusätzlichen Dependencies,
- fehlendem, ungültigem oder werfendem `getClient`,
- `null` oder `undefined` als Client,
- fehlender, ungültiger oder werfender Adapter-Factory,
- ungültigem Adapter oder fehlendem beziehungsweise ungültigem
  `resolveAccess`,
- synchronem Fehler oder Promise-Rejection der Delegation,
- ungültigem oder widersprüchlichem Adapter-Ergebnis.

Rohfehler werden nicht ausgegeben. Es gibt keinen Retry und keine automatische
Bereinigung oder Ersetzung eines vorhandenen Clients.

## 5. Ausdrückliche Sicherheitsgrenzen

- kein `window`, `globalThis` oder `global`
- kein `getState()`
- kein `initializeClient()`
- kein `createClient()`
- keine Config-, SDK- oder Live-Schalter
- kein Netzwerkcode und kein externer Zugriff
- keine Schreiboperation
- kein SQL und keine Migration
- keine App- oder UI-Integration
- keine echten Schlüssel und keine echten Teilnehmerdaten
- keine duplizierte Teilnehmer-, Enrollment- oder Kurslogik

Als unveränderte Bestandsmodule bestehen der vorhandene Bootstrap, der zentrale
Client-Adapter und der Teilnehmerzugangs-Adapter v27.36b fort.

## 6. Testumfang

`tools/check-supabase-participant-access-bootstrap-bridge.py` führt das echte
JavaScript-Brückenmodul ausschließlich mit lokalen synthetischen Abhängigkeiten
und einem Fake-Bootstrap aus. Folgende getestete Fälle werden insbesondere
abgedeckt:

- Dependency- und CommonJS-Oberfläche,
- alle Fail-closed-Pfade von Bootstrap, Factory, Adapter und Ergebnis,
- exakt ein `getClient()`-Aufruf pro Delegation,
- exakt `{ client, utcNow }` als Factory-Argument,
- identische Rückgabe gültiger Adapter-Ergebnisse,
- Durchreichen eines ungültigen Clients bis zu `client_invalid`,
- erfolgreicher `access_allowed`-Pfad mit echtem v27.36b-Adapter und lokalem
  In-Memory-Fake-Client,
- alleinige Nutzerautorität `session.user.id`,
- keine Schreiboperation, kein externer Zugriff und keine verbotenen
  Bootstrap-, Global-, Config-, SDK- oder Live-Pfade,
- zusätzliche Manipulationsprüfungen gegen Getter-, Proxy-, Ergebnis- und
  Autoritätsumgehungen.

Die Tests verwenden kein Netzwerk, keine Datenbank, kein SQL, keine Migration,
keinen echten Supabase-Client und keine echten Teilnehmerdaten.

## 7. Live-Status

Supabase live: NEIN. Die Brücke wird nicht von der App geladen, aktiviert
keinen Login und verändert keinen sichtbaren App-Zustand. Für die lokale
Prüfung gilt außerdem: echte Keys: NEIN, denn der Test verwendet keine
Zugangsschlüssel. Ebenso gilt: echte Teilnehmerdaten: NEIN, denn alle Testdaten
sind lokal und synthetisch.
