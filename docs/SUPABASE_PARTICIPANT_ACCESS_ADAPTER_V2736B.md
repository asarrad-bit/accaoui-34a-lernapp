# Supabase-Teilnehmerzugangs-Adapter v27.36b

Stand: v27.36b
Implementierungszustand: lokal vorbereitet, nicht in die App integriert

## 1. Ziel

v27.36b stellt eine kleine, isolierte und fail-closed arbeitende
Teilnehmerzugangs-Komponente bereit. Sie entscheidet ausschließlich anhand
einer validierten Session, eines kanonischen Participants, eines kanonischen
Enrollments, eines kanonischen Courses und einer injizierten UTC-Zeitquelle.

## 2. Scope

Umgesetzt sind nur das CommonJS-Adaptermodul, sein lokaler ausführender Checker
mit synthetischem In-Memory-Fake und die dauerhafte Preflight-Anbindung. Es gibt
keine App-, Login-, SDK-, Config-, Bootstrap-, Netzwerk- oder Datenbankanbindung.

## 3. Kanonisches MVP-Schema und kanonische Tabellen-/Spaltenbindung

Verbindlich ist ausschließlich das MVP-Schema aus
`supabase/migrations/20260710_v2720b_mvp_schema.sql`:

- `participants`: `id,auth_user_id,status`; Status exakt `active`, `blocked`,
  `expired` oder `completed`.
- `enrollments`:
  `id,participant_id,course_id,access_starts_at,access_ends_at,access_status`;
  Access-Status exakt `allowed`, `blocked`, `expired` oder `completed`.
- `courses`: `id,start_date,end_date,status`; Status exakt `active`, `inactive`
  oder `archived`.

Die historischen Alternativen `profiles` und `course_enrollments` sind keine
zweite Produktionslogik. Schema, Migrationen, SQL, RLS und RPCs bleiben
unverändert.

## 4. injizierte Dependencies

`createParticipantAccessAdapter({ client, utcNow })` akzeptiert exakt zwei
explizite Abhängigkeiten:

- `client`: Supabase-kompatibel mit `auth.getSession()` und
  `from(...).select(...).eq(...)`.
- `utcNow`: Funktion, die beim Aufruf genau einen gültigen UTC-Zeitwert liefert.

Fehlende, ungültige oder zusätzliche Dependency-Felder blockieren. Es gibt
keine globale Client-, Config- oder Environment-Auflösung und keinen globalen
veränderlichen Zustand.

## 5. Session-Bindung

Die einzige Nutzerautorität ist `session.user.id`. Der Wert muss eine gültige
UUID sein und wird als exakter Filterwert für `participants.auth_user_id`
verwendet. Frei übergebene `user_id`, `participant_id`, `userId` oder
`participantId` werden weder akzeptiert noch zur Autorisierung verwendet.
Session-Token, User-Objekt und sonstige Sessiondaten werden nicht ausgegeben.

## 6. Queryreihenfolge

Die Lesekette ist strikt seriell und deterministisch:

1. `client.auth.getSession()`
2. `participants` anhand `auth_user_id == session.user.id`
3. `enrollments` anhand `participant_id == participant.id`
4. `courses` anhand `id == enrollment.course_id`
5. rein lokale Ableitung des Access-State

Jede Query fordert nur die in Abschnitt 3 genannten Spalten an. Es gibt keine
parallelen Queries, Retries, Writes, Upserts, Inserts, Updates, Deletes oder
RPC-Aufrufe. Null Treffer und mehr als ein Treffer blockieren; „erste Zeile
gewinnt“ existiert nicht. Nach einem Blocker werden keine Folgequeries gestartet.

## 7. Participant-Regeln

Genau ein objektförmiger Participant ist erforderlich. `id` und
`auth_user_id` müssen gültig sein; `auth_user_id` muss exakt der
`session.user.id` entsprechen. Nur `status == active` erlaubt die weitere
Prüfung. `blocked`, `expired`, `completed`, unbekannte Zustände, fehlende IDs,
fremde Bindungen und ungültige Resultatformen blockieren.

Das MVP-Schema besitzt kein separates Participant-Ablaufdatum. Der Zustand
„expired“ stammt deshalb ausschließlich aus `participants.status == expired`.

## 8. Enrollment-Regeln

Genau ein Enrollment ist erforderlich. `id`, `participant_id` und `course_id`
müssen gültig sein, und `participant_id` muss exakt zum vorher validierten
Participant gehören. Nur `access_status == allowed` erlaubt die weitere
Prüfung. `blocked`, `expired`, `completed`, unbekannte Zustände, ungültige
Zeitwerte und widersprüchliche Zeitbereiche blockieren.

## 9. Course-Regeln

Genau ein Course ist erforderlich. Seine `id` muss exakt der validierten
`enrollment.course_id` entsprechen. Nur `status == active` erlaubt Zugriff.
`inactive`, `archived`, unbekannte Zustände, ungültige ISO-Kalenderdaten und
widersprüchliche Datumsbereiche blockieren.

## 10. UTC-Zeitsemantik

Der Adapter liest die injizierte UTC-Zeitquelle genau einmal. Er verwendet
keinen nicht injizierten aktuellen Uhrwert.

Enrollment-Zeitgrenzen:

- `access_starts_at == null`: unbegrenzt nach vorn.
- `access_ends_at == null`: unbegrenzt nach hinten.
- Start und Ende sind inklusive.
- `now < start` blockiert; `now > end` blockiert.
- Zeitwerte müssen ISO-8601-Instant-Werte mit `Z` oder explizitem Offset sein.

Course-Datumsgrenzen:

- `start_date == null` und `end_date == null`: jeweilige Grenze unbegrenzt.
- Vergleich erfolgt gegen den aktuellen UTC-Kalendertag `YYYY-MM-DD`.
- Start- und Enddatum sind inklusive.

## 11. Access-State-Vertrag

Blockierte Ergebnisse sind stabil und klein:

```js
{ allowed: false, code: "session_missing" }
```

Der einzige Erfolgszustand lautet:

```js
{
  allowed: true,
  code: "access_allowed",
  participantId: "...",
  enrollmentId: "...",
  courseId: "...",
  accessStartsAt: "..." oder null,
  accessEndsAt: "..." oder null
}
```

Ergebnisse und Adapteroberfläche sind eingefroren. Ausgegeben werden nur
primitive, neu abgeleitete Werte; Eingaben und Fake-Daten werden nicht mutiert.

## 12. Fail-closed-Regeln und Codes

Jede Abweichung blockiert deterministisch. Die Codes sind nach Stufe gruppiert:

- Dependencies/Client: `client_missing`, `client_invalid`,
  `dependencies_invalid`, `dependency_fields_invalid`, `utc_source_invalid`,
  `utc_source_failed`, `utc_now_invalid`.
- Session: `session_query_failed`, `session_result_invalid`, `session_missing`,
  `session_invalid`, `session_user_missing`, `session_user_id_invalid`.
- Participant: `participant_query_failed`,
  `participant_query_interface_invalid`, `participant_result_invalid`,
  `participant_missing`, `participant_ambiguous`, `participant_invalid`,
  `participant_id_invalid`, `participant_user_mismatch`,
  `participant_status_invalid`, `participant_blocked`, `participant_expired`,
  `participant_completed`.
- Enrollment: entsprechende Query-, Result-, Missing-, Ambiguous-, ID-,
  Binding- und Statuscodes sowie `enrollment_access_start_invalid`,
  `enrollment_access_end_invalid`, `enrollment_access_range_invalid`,
  `enrollment_access_not_started` und `enrollment_access_ended`.
- Course: entsprechende Query-, Result-, Missing-, Ambiguous-, ID-, Binding-
  und Statuscodes sowie `course_start_date_invalid`, `course_end_date_invalid`,
  `course_date_range_invalid`, `course_not_started` und `course_ended`.

Unbekannte Zustände, unerwartete Resultatformen, fehlende IDs, mehrere Treffer
und widersprüchliche Bindungen werden niemals als Zugriff interpretiert.

## 13. Fehler-Sanitizing

Exceptions sowie Supabase-`error`-Objekte werden an ihrer jeweiligen Stufe
abgefangen und ausschließlich auf stabile Codes abgebildet. Rohmeldungen,
Transportdetails, vollständige Zeilen, Session/User, `access_token`,
`refresh_token`, Passwörter und Secrets gelangen nicht in den Rückgabewert.
Automatische Retries gibt es nicht.

## 14. Fake-Client

Der Checker enthält einen ausschließlich lokalen, synthetischen
In-Memory-Fake-Client für exakt die verwendete minimale Oberfläche. Er kopiert
Fixtures defensiv und protokolliert Session-, Tabellen-, Select- und
Eq-Aufrufe. Damit prüft er Reihenfolge, minimale Spalten, erlaubte Tabellen,
nur lesende Operationen, Fail-fast und fehlende Retries. Er besitzt keine
Live-, Netzwerk-, DNS-, HTTP-, Supabase-, Datenbank-, SQL-, Datei-Schreib-,
Environment- oder echte Zugangsdatenfunktion.

## 15. getestete Fälle

Der ausführende Checker führt den echten JavaScript-Adapter über die vorhandene
lokale Node-Laufzeit aus. Er deckt die 49 verbindlichen Mindestfälle ab:
Client, Session, Participant, Enrollment, Course, sieben Positiv-/Grenzfälle
und zehn Sicherheits-/Vertragsprüfungen. Zusätzlich werden 26
Manipulationsfälle geprüft, darunter ungültige UUIDs und Resultatformen,
fehlende Querymethoden, geworfene Queries, unbekannte Statuswerte,
widersprüchliche Zeit-/Datumsbereiche, exakt einmalige Uhrabfrage, defensive
Ergebnisse, minimale Spalten, Retry-Sperre und getrennte Instanzzustände.

Gesamtumfang: 75 deterministische ausführende Prüfungen.

## 16. Sicherheitsgrenzen (Sicherheitsgrenze)

- Nutzerautorität ausschließlich `session.user.id`.
- Nur `participants`, `enrollments`, `courses` und minimale Spalten.
- Nur serielle Leseoperationen; keine Mutation und kein RPC.
- Keine globale Clientauflösung, keine globale Mutable State-Ablage.
- Keine Tokens, Secrets, Rohfehler oder vollständigen Datensätze im Ergebnis.
- Keine echte URL, kein echter Key und keine echten Teilnehmerdaten.

Expliziter Zustand:

- Supabase live: NEIN
- SDK geladen: NEIN
- echter Client: NEIN
- echte Keys: NEIN
- Service-Role-Key: NEIN
- echte Teilnehmerdaten: NEIN
- Netzwerkzugriff: NEIN
- Datenbankzugriff: NEIN
- App-Integration: NEIN
- Login aktiviert: NEIN

## 17. Unveränderte App-/Live-Komponenten und ausdrücklich nicht umgesetzte Live-Funktionen

Unverändert bleiben `app.js`, `index.html`, `style.css`, `questions.json`, der
zentrale `data/supabase-client-adapter.js`, der Bootstrap, alle Config-Dateien,
alle Migrationen, SQL, RLS, RPCs und die Projekt-Steuerungsdokumente. Nicht
umgesetzt sind App- oder Dashboardintegration, Loginformular oder App-Sperre,
SDK-Laden, Config-Aktivierung, Bootstrap-Verbindung, Live-Supabase-Tests, echte
Nutzer/Participants, echte RLS-/Datenbanktests sowie Anbindungen von Progress,
Prüfungshistorie, Zertifikaten oder Registry.
