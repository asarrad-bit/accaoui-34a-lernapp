# v27.37b – Isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke

## Status und Umfang

Supabase bleibt NICHT LIVE. Die Brücke verbindet ausschließlich einen injizierten Bootstrap mit dem bestehenden isolierten v27.37a-Teilnehmer-Auth-/Session-Adapter. Sie aktiviert keinen Login und bindet keine Browseroberfläche an.

Der autorisierte Implementierungsumfang besteht exakt aus:

- `data/supabase-participant-auth-session-bootstrap-bridge.js`
- `tools/check-supabase-participant-auth-session-bootstrap-bridge.py`
- `docs/SUPABASE_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_V2737B.md`
- `tools/preflight.py`

Bestehende Produktdateien, Bootstrap und Adapter bleiben unverändert. Ein Commit, ein Push, eine Closure oder ein weiterer Task sind durch diese Implementation nicht autorisiert.

## Factory und öffentliche Oberfläche

Das Modul verwendet ausschließlich CommonJS. Die Factory heißt:

```js
createParticipantAuthSessionBootstrapBridge({
  bootstrap,
  createParticipantAuthSessionAdapter
})
```

Die beiden Dependencies sind exakt `bootstrap` und `createParticipantAuthSessionAdapter`. Die Brücke importiert und erzeugt keinen eigenen Client. Dependencies werden erst beim Aufruf einer öffentlichen Operation inspiziert; `require()` und die Factory-Erzeugung lösen keine Dependency-Getter, Bootstrap-Aufrufe oder Adapter-Erzeugung aus.

Die öffentliche Rückgabe ist exakt:

```js
Object.freeze({
  resolveSession,
  signIn,
  signOut
})
```

Sie besitzt keine vierte Methode und keine Zusatzproperty. Jede Methode liefert asynchron ein Ergebnis des unten beschriebenen Vertrags.

## Ablauf pro Operation

Für jeden Aufruf von `resolveSession()`, `signIn(credentials)` oder `signOut()` wird der vollständige Ablauf neu durchlaufen:

1. Die Dependencies werden innerhalb der Fehlergrenze gelesen und geprüft.
2. `bootstrap.getClient` wird sicher gelesen und als Funktion geprüft.
3. Die gelesene Funktion wird exakt einmal mit `getClient.call(bootstrap)` aufgerufen. Der Receiver bleibt dadurch erhalten.
4. Aus dem erhaltenen Client wird ausschließlich `client.auth` und dieses genau einmal gelesen.
5. Die injizierte Factory wird für diese Operation neu und ausschließlich mit `{ auth }` aufgerufen. Der gesamte Client sowie weitere Dependencies werden nicht weitergegeben.
6. Ausschließlich die zur Operation gehörende Adaptermethode wird sicher gelesen und genau einmal mit `method.apply(adapter, args)` aufgerufen.
7. Das aufgelöste Adapterergebnis wird geprüft und bei Gültigkeit als dasselbe Objekt zurückgegeben.

`getClient()` und `createParticipantAuthSessionAdapter({ auth })` sind synchrone Grenzen. Ausschließlich das Ergebnis der passenden Adaptermethode wird mit `await` aufgelöst. Der Client wird nicht awaited; damit findet auch kein impliziter Zugriff auf `client.then` statt.

Client und Adapter werden nicht zwischen Operationen gecacht. Ein Wechsel des von `getClient()` gelieferten Clients ist deshalb beim nächsten Aufruf wirksam.

`signIn(credentials)` reicht den ursprünglichen Credentials-Wert unverändert als einziges Argument weiter. Die Brücke kopiert oder zerlegt ihn nicht und führt keine eigene E-Mail- oder Passwortvalidierung aus. `resolveSession()` und `signOut()` delegieren ohne Argumente.

Ist bereits eine frühere Stufe ungültig oder wirft sie einen Fehler, werden spätere Stufen nicht mehr aufgerufen. Insbesondere wird eine fehlende oder ungültige `getClient`-Funktion nicht aufgerufen. Die Zusicherung eines einzelnen Aufrufs gilt für jede Operation, die diese gültige Stufe erreicht.

## Gültige Ergebnisse

Ein Ergebnis wird nur akzeptiert, wenn alle folgenden Bedingungen erfüllt sind:

- `Object.getPrototypeOf(result) === Object.prototype`.
- Das Objekt besitzt exakt die beiden eigenen Keys `ok` und `code`, einschließlich der Prüfung nicht aufzählbarer und symbolischer Zusatzkeys.
- Beide Properties sind eigene aufzählbare Datenproperties; Accessor-Properties sind ausgeschlossen.
- `ok` ist ein Boolean und `code` ist ein String.
- `Object.isFrozen(result) === true`.
- Das Paar aus `ok` und `code` ist für die aufgerufene Methode in der folgenden Tabelle enthalten.

| Methode | `ok` | `code` |
| --- | --- | --- |
| `resolveSession` | `true` | `session_available` |
| `resolveSession` | `false` | `session_missing` |
| `resolveSession` | `false` | `session_invalid` |
| `resolveSession` | `false` | `auth_error` |
| `signIn` | `true` | `signed_in` |
| `signIn` | `false` | `credentials_invalid` |
| `signIn` | `false` | `sign_in_failed` |
| `signIn` | `false` | `auth_error` |
| `signOut` | `true` | `signed_out` |
| `signOut` | `false` | `sign_out_failed` |
| `signOut` | `false` | `auth_error` |

Eingefrorene Accessor-Ergebnisse werden ebenfalls abgewiesen: Das Einfrieren eines Getters garantiert keinen unveränderlichen Rückgabewert. Auch Arrays, Instanzen eigener Klassen und Objekte mit `null`-Prototyp erfüllen den Plain-Object-Vertrag nicht.

Ein gültiges Ergebnis wird unverändert und identisch durchgereicht. Die Brücke erzeugt dafür weder ein Ersatzobjekt noch zusätzliche Ergebnisfelder und friert das Adapterergebnis nicht nachträglich ein.

## Fehlergrenzen

Jeder Brückenfehler liefert ausschließlich:

```js
Object.freeze({
  ok: false,
  code: "auth_error"
})
```

Diese Grenze umfasst insbesondere fehlende oder ungültige Dependencies, fehlerhafte Bootstrap- oder Adaptermethoden, Throws, Promise-Rejections, werfende Getter und fehlerhafte Proxy-Zugriffe sowie ungültige Ergebnisobjekte. Fehler beim Prüfen von Prototyp, eigenen Keys, Property-Deskriptoren oder Freeze-Zustand bleiben ebenfalls innerhalb dieser Grenze.

Fehlerresultate besitzen exakt die beiden eigenen aufzählbaren Datenproperties `ok` und `code` und sind eingefrorene Plain Objects. Interne Fehlercodes, Exceptions oder Rohantworten werden nicht nach außen gegeben. Die Brücke übernimmt insbesondere keine Session-, User-, ID-, E-Mail-, Passwort-, Token-, Client-, Auth-, Config-, Key- oder `error.message`-Daten in Ergebnisse.

Die fachliche Interpretation von Auth-Antworten bleibt im bestehenden v27.37a-Adapter. Teilnehmerzugang, Teilnehmerstatus, Enrollment- und Kurslogik bleiben in der bestehenden Zugangslogik.

## Ausgeschlossene Funktionen

Die Brücke enthält keine Aufrufe von `initializeClient()`, `createClient()` oder `getState()`. Sie enthält keine Browser-Exports, Browser-Globals, DOM-, Storage-, Cookie-, IndexedDB- oder Cache-Zugriffe und keinen eigenen Netzwerkcode. Tabellenabfragen, SQL, Migrationen und eigene Teilnehmer-, Enrollment- oder Kurslogik sind ausgeschlossen.

Es gibt keine echten Keys und keine echten Teilnehmerdaten. Sämtliche nachfolgend beschriebenen Tests verwenden lokale synthetische Fakes. Supabase bleibt NICHT LIVE.

## Checker und synthetische Abdeckung

`tools/check-supabase-participant-auth-session-bootstrap-bridge.py` verbindet statische Vertragsprüfungen, dynamische CommonJS-Prüfungen und gezielte Quelltextmanipulationen. Er prüft insbesondere:

- CommonJS, die exakte Factory-/Dependency-Struktur, exakt drei öffentliche Methoden und die eingefrorene Oberfläche.
- Fehlende Side Effects beim Laden und Erzeugen, einschließlich verzögerter Dependency-Inspektion.
- Je Operation einen Bootstrap-Aufruf, den erhaltenen Receiver, den einzelnen Auth-Lesezugriff, einen frischen Adapter und nur den passenden einzelnen Methodenaufruf.
- Clientwechsel zwischen Operationen, unveränderte Credentials sowie unveränderte Objektidentität aller gültigen methodenspezifischen Ergebnisse.
- Ungültige Typen, Prototypen, Keys, Deskriptoren, Freeze-Zustände und methodenfremde Ergebnispaare.
- Fehlende Funktionen, Throws, Rejections, Getter und Proxy-Fehler an den verschiedenen Grenzen.
- Das exakte eingefrorene Fehlerergebnis und den Ausschluss sensitiver Zusatzwerte.
- Den Ausschluss von Browser-, Storage-, Netzwerk- und eigener Domainlogik.

Die Quelltextmanipulationen umfassen zusätzliche Dependencies und öffentliche Properties oder Methoden, entfernte oder doppelte Bootstrap-Aufrufe, Client-Caching, Weitergabe des ganzen Clients oder zusätzlicher Factory-Argumente, verbotene Initialisierungs-/Browser-/Storage-/Netzwerk-/Tabellenlogik sowie Ergebnis-Rewrapping, entfernte Freeze-Aufrufe, zusätzliche Fehlerproperties und das Leaken einer Fehlermeldung. Eine Manipulation muss vom Checker zurückgewiesen werden.

Der temporäre Prüfbereich liegt ausschließlich unter:

```text
.git/accaoui-checker-temp/v2737b-auth-bridge
```

Es gibt keinen `%TEMP%`-Fallback. Dort erzeugte synthetische Testartefakte gehören nicht zum Implementierungsumfang oder zu einem Commit.

## Gemeinsamer synthetischer Fake

Ein gemeinsamer synthetischer Auth-/Client-Zustand verbindet die Brücke mit dem bestehenden v27.37a-Auth-/Session-Adapter und der bestehenden Zugangslogik. Der Testablauf prüft:

1. `signIn` liefert `signed_in`.
2. Die bestehende Zugangslogik liefert für denselben synthetischen Zustand `access_allowed`.
3. `signOut` liefert `signed_out`.
4. Ein nachfolgendes `resolveSession` liefert `session_missing`.

Diese Verbindung entsteht ausschließlich im lokalen Checker. Sie aktiviert keine Browserkette und keine Live-Verbindung.

## Verbindliche Prüfungen und Lifecycle

`tools/preflight.py` führt den neuen Checker verbindlich aus. Bestehende Prüfungen und Regressionen bleiben erhalten. Der bereits bestehende Kontinuitätsvertrag muss die autorisierte Vorbereitung mit exakt den vier Implementierungsdateien als `v2737b_implementation_prepared` erkennen.

Die Prüfkommandos lauten:

```text
py -3 -m py_compile tools/check-supabase-participant-auth-session-bootstrap-bridge.py tools/preflight.py
py -3 tools/check-supabase-participant-auth-session-bootstrap-bridge.py
py -3 tools/check-project-continuity-control.py
py -3 tools/preflight.py
git diff --check
git status --short
```

Maßgeblich sind die tatsächlich ausgeführten Prüfungen und deren Ausgabe. Die Anzahl der positiven, negativen und Manipulationsprüfungen wird vom Checker berichtet; dieses Vertragsdokument nimmt keine Prüfergebnisse vorweg.
