# Teilnehmer-Auth-/Session-Adapter v27.37a

## Ziel und Isolation

v27.37a stellt ein isoliertes CommonJS-Modul für die syntaktische Prüfung einer Auth-Session sowie für An- und Abmeldung bereit. Die Factory lautet `createParticipantAuthSessionAdapter({ auth })`; `auth` ist die einzige injizierte Dependency. Die öffentliche, eingefrorene Adapteroberfläche enthält ausschließlich `resolveSession()`, `signIn({ email, password })` und `signOut()`.

Es gibt kein Browser-Wiring, keinen Browser-Export und keine Seiteneffekte beim Laden oder Erzeugen des Adapters. Auth wird erst durch den Aufruf einer der drei öffentlichen Methoden verwendet.

## Ergebnisvertrag und Codes

Jedes öffentliche Ergebnis ist ein eingefrorenes Plain Object mit exakt `{ok,code}`. Es werden ausschließlich folgende Codes ausgegeben:

- `resolveSession()`: `session_available`, `session_missing`, `session_invalid`, `auth_error`
- `signIn({ email, password })`: `signed_in`, `credentials_invalid`, `sign_in_failed`, `auth_error`
- `signOut()`: `signed_out`, `sign_out_failed`, `auth_error`

## Datenminimierung

Session, User, ID, E-Mail, Passwort, Token, Auth-Antworten und Rohfehler werden nicht nach außen gegeben. Das Passwort wird weder verändert noch gespeichert oder persistiert. Eine verwendbare Session verlangt eine syntaktisch gültige `session.user.id` nach demselben UUID-Standard wie der bestehende Zugangsadapter.

## Synthetischer Test- und Integrationsvertrag

Als Testdouble dient ausschließlich ein lokaler synthetischer In-Memory Fake Auth. Er prüft Factory und Oberfläche, sämtliche Ergebnisformen, gültige und fehlerhafte Session-, Sign-in- und Sign-out-Pfade, exakte Aufrufzahlen, Datenminimierung sowie echte temporäre Quellmutationen.

Der Shared Fake wird gleichzeitig vom neuen Adapter und vom unveränderten v27.36b-Teilnehmerzugangs-Adapter verwendet. Vor der Anmeldung liefert der bestehende Adapter `session_missing`; nach `signed_in` liefert er `access_allowed`; nach `signed_out` liefert er erneut `session_missing`. Teilnehmer-, Enrollment- und Kurslogik verbleiben ausschließlich im Test-Fake und im unveränderten v27.36b-Teilnehmerzugangs-Adapter.

## Sicherheitsgrenzen

Das Modul verwendet nur `auth.getSession()`, `auth.signInWithPassword(...)` und `auth.signOut()`. Es enthält weder Browser-, DOM- oder Storage-Zugriffe noch Client-Erzeugung, Config-Lesen, Netzwerkcode, Tabellenzugriffe, SQL, Migrationen oder Teilnehmer-Fachlogik. Eine frei übergebene Nutzer-ID ist ausgeschlossen; die bestehende Teilnehmerautorität `session.user.id` wird nicht dupliziert.

Supabase NICHT LIVE. Es werden keine echten Keys und keine echten Teilnehmerdaten verwendet. Keine App- oder index.html-Änderung wurde vorgenommen. Es gibt kein Folgetask vor Closure.
