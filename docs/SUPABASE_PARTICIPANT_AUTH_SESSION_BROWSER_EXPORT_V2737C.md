# Teilnehmer-Auth-/Session Browser-Export v27.37c

Stand: v27.37c

## Ziel

v27.37c ergänzt ausschließlich kontrollierte Browser-Export-Grenzen
für die bereits vorhandenen Teilnehmer-Auth-/Session-Factories.

Die bestehende Auth-/Session-Fachlogik bleibt unverändert.

## Browser-Grenzen

Erlaubt sind ausschließlich:

- `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_ADAPTER_FACTORY`
- `window.ACCAOUI_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_FACTORY`

Die jeweilige Browser-Grenze wird nur gesetzt, wenn ihr bestehender
Wert `undefined` ist.

Eine vorhandene Grenze wird niemals überschrieben.

Die exportierte Property ist:

- enumerable
- nicht configurable
- nicht writable

## CommonJS

Die vorhandenen CommonJS-Verträge bleiben erhalten:

- `createParticipantAuthSessionAdapter`
- `createParticipantAuthSessionBootstrapBridge`

Browser- und CommonJS-Export verwenden jeweils dieselbe Factory.

## Ladeverhalten

Beim Laden der Module erfolgt:

- keine Auth-Operation
- keine Sessionauflösung
- kein `getClient()`
- kein Clientzugriff
- keine Adapteroperation
- kein Netzwerkzugriff
- kein SDK- oder Config-Laden

Die Bootstrap-Brücke bleibt vollständig lazy.

## Sicherheitsgrenzen

Weiterhin verboten sind insbesondere:

- `initializeClient()`
- `createClient()`
- `getState()`
- eigenes Browser-Wiring außerhalb der beiden Grenzen
- `localStorage` und `sessionStorage`
- eigener Netzwerkcode
- `.from(...)`
- SQL und Migrationen
- echte Supabase-Schlüssel
- echte Teilnehmerdaten

## Prüfungen

Die lokalen Checker prüfen weiterhin die bestehenden v27.37a-
und v27.37b-Verträge und zusätzlich:

- exakte Browser-Factory-Namen
- geschützte Property-Descriptoren
- Browser-only-Ausführung
- identische CommonJS-/Browser-Factory
- Nicht-Überschreiben bestehender Grenzen
- passives Verhalten bei nicht beschreibbaren Grenzen
- keine Ladezeit-Side-Effects

Supabase bleibt NICHT LIVE.
