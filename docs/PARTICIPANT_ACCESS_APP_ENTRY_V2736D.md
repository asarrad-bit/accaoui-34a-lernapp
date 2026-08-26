# Teilnehmerzugangs-App-Einstieg v27.36d

## Ziel

Der bestehende Auth-Einstieg kann einen optionalen Provider unter
`window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER` auswerten. Der Provider stellt
ausschließlich `resolveAccess()` bereit. Ohne Provider bleibt der bisherige
lokale App-Start unverändert.

`window.ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER` ist ein optionaler Provider:
Ist er vorhanden, wird `resolveAccess()` verwendet; bei einem Providerfehler
gilt fail-closed ohne lokalen Fallback.

## Ablauf und Provider-Vertrag

Lokale Auth-Guard-Testzustände werden zuerst geprüft und behalten Vorrang. Ist
der Provider exakt `undefined`, startet der lokale Standardbetrieb. Jeder andere
vorhandene Provider muss ein Objekt mit einer aufrufbaren `resolveAccess()`-
Methode sein. Diese Methode wird je Auth-Entscheidung exakt einmal aufgerufen.

Nur `{ allowed: true, code: "access_allowed" }` ruft `startLocalApp()` exakt
einmal auf. `null`, ungültige Provider, Throw, Reject und ungültige Ergebnisse
blockieren den Start.

## Mapping

- `login_required`: `session_missing`, `session_invalid`,
  `session_user_missing`, `session_user_id_invalid`
- `blocked`: `participant_blocked`, `enrollment_blocked`
- `expired`: `participant_expired`, `enrollment_expired`,
  `enrollment_access_ended`, `course_ended`
- `no_course`: `participant_completed`, `enrollment_missing`,
  `enrollment_completed`, `enrollment_access_not_started`, `course_missing`,
  `course_inactive`, `course_archived`, `course_not_started`

Alle anderen und technischen Codes werden als generischer `access_error`
angezeigt. Interne Codes oder rohe Fehler werden nicht ausgegeben.

## Sicherheitsgrenze und Fail-closed-Regeln

Nach Erkennung eines vorhandenen Providers gibt es bei keinem Fehler einen
lokalen Fallback. Die App führt keine Auth-, Teilnehmer-, Enrollment- oder
Kursabfrage aus, erzeugt keinen Client und aktiviert weder Config noch SDK oder
Live-Betrieb. Es gibt keine duplizierte Fachlogik aus dem Teilnehmerzugangs-
Adapter.

Die unveränderte Bestandsmodule sind Bootstrap, zentraler Client-Adapter,
v27.36b-Teilnehmerzugangs-Adapter und v27.36c-Brücke. Es besteht ausdrücklich
noch keine Browser-Verbindung zu v27.36b/v27.36c; die CommonJS-Module werden
nicht in den Browser geladen oder konvertiert.

## Getestete Fälle

Der Checker verwendet ausschließlich ein lokaler synthetischer Provider-
Harness. Die getestete Fälle umfassen lokalen Start ohne Provider, genau einen
Start bei `access_allowed`, sämtliche Mapping-Codes, ungültige Ergebnisse,
Throw, Reject, fehlende Methoden, Auth-Guard-Vorrang und gezielte
Manipulationsprüfungen. Es gibt keinen Netzwerk-, Datenbank-, SQL- oder
Migrationszugriff.

Supabase bleibt **NICHT LIVE**.

Supabase live: NEIN

echte Keys: NEIN

echte Teilnehmerdaten: NEIN
