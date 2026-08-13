# v27.36a – Supabase/Login-Bestandsaudit

## 1. Audit-Grenze

Dieses Audit inventarisiert ausschließlich den lokalen Repository-Stand am
HEAD `cd8e982ae73d63ecd54c388be731c20432ef0666` auf Branch `main`.

Geprüft wurden die Projektsteuerung, Supabase-/Login-Planungen, die lokale
App-Start- und Guard-Logik, Config-, SDK-, Client- und Adapterzustände,
Teilnehmer-, Kurs-, Enrollment-, Ablauf- und Fortschrittsmodelle,
Dashboard- und Prüfungshistorie-Zustände, SQL-Migrationen, RPCs, RLS,
Registry-/Atomic-Consumption-Verträge, lokale Fake-/Testtreiber sowie
Zertifikatsvorbereitungen.

Es wurden keine Live-Verbindung, kein Netzwerkzugriff, kein Datenbankzugriff,
keine SQL- oder Migrationsausführung, keine Config-Aktivierung, keine echten
Schlüssel und keine echten Teilnehmerdaten verwendet. App, UI, Adapter,
Fragen, SQL und Migrationen wurden nicht verändert.

## 2. Zusammenfassung

- **Live-Status: NEIN.** Im Repository ist keine tatsächlich aktive
  Supabase-Anbindung belegt.
- Die App läuft standardmäßig lokal und lässt den Zugriff ohne Login zu.
- Login-, Sperr-, Ablauf- und Kein-Kurs-Zustände funktionieren nur als lokale
  Testzustände über `localStorage`.
- Ein echter Supabase-Client kann technisch durch
  `data/supabase-client-bootstrap.js` erzeugt werden, aber nur nach gültiger
  öffentlicher Config, vorhandenem SDK, zwei expliziten Schaltern und einem
  manuellen Methodenaufruf. Keine dieser Voraussetzungen ist im normalen
  Repository-Betrieb aktiv.
- Der zentrale Adapter ist umfangreich lokal implementiert und getestet,
  führt aber weder Session-, Profil-, Kurs-, Enrollment- noch
  Fortschrittsabfragen aus.
- 30 SQL-Migrationen, RLS-Policies und mehrere Security-Definer-RPCs sind
  statisch vorbereitet und geprüft, jedoch nicht gegen eine Datenbank
  ausgeführt.
- Die Prüfungshistorie besitzt eine weit entwickelte lokale
  Normalisierungs-, Zustands-, Persistenz- und Idempotenzkette. Der
  Browseradapter ruft den vorbereiteten RPC trotzdem nicht auf.
- Die Registry-/Atomic-Consumption-Kette und der lokale In-Memory-Fake-Treiber
  sind technisch ausgearbeitet, betreffen aber die disposable
  Testumgebungs-/Autorisierungsgrenze und sind keine Voraussetzung für einen
  ersten Teilnehmer-Login.
- Vor einer Live-Anbindung ist eine kleine Konsolidierung der Auth-
  Zugriffsschnittstelle erforderlich. Weitere kleinteilige Readiness-States
  würden die wesentliche Lücke nicht schließen.

## 3. Statusmodell A-F

| Stufe | Bedeutung |
|---|---|
| A | Nur geplant oder als Absicht beschrieben |
| B | Vertrag, Spezifikation oder festes Datenmodell vorhanden |
| C | Lokal implementiert oder simuliert |
| D | Lokal mit statischen, Fixture- oder Ausführungstests geprüft |
| E | Technisch für eine echte Anbindung vorbereitet, aber nicht live |
| F | Tatsächlich live angebunden und gegen den realen Dienst belegt |

Eine Stufe bewertet nur den belegten Stand. Insbesondere bedeuten vorhandene
SQL-Dateien, Browser-Stubs oder grüne statische Tests niemals Stufe F.

## 4. Auth und Login

| Nr. | Bereich und Dateien | Stufe | Tatsächlicher Stand | Vorbereitung, Lücke, Abhängigkeit und Risiko |
|---:|---|:---:|---|---|
| 1 | Auth-/Login-Planung: `docs/SUPABASE_LOGIN_ACCESS_PLAN.md`, `docs/SUPABASE_IMPLEMENTATION_ROADMAP.md` | B | Zielreihenfolge Auth, Profil, Kurs, Ablauf und Fortschritt ist dokumentiert. | Keine echte Auth-Konfiguration oder Session. Rollen- und Tabellennamen weichen von den späteren Migrationen ab. |
| 2 | Login-UI-Konzept: `docs/SUPABASE_LOGIN_UI_CONCEPT.md` | B | Login-, Aktiv-, Kein-Kurs-, Abgelaufen- und Gesperrt-Ansichten sind spezifiziert. | Kein E-Mail-/Passwortformular ist aktiv. Historische Aussagen zum App-Einstieg sind durch spätere lokale Guards teilweise überholt. |
| 3 | Auth-Einstieg: `docs/SUPABASE_AUTH_ENTRYPOINT_AUDIT.md`, `app.js` | D | `DOMContentLoaded -> initAppBoot() -> initAuthFlow() -> startLocalApp()` ist real eingebaut. | Die Entscheidung beruht auf lokalen Testzuständen beziehungsweise einem Stub-Health-State, nicht auf einer Supabase-Session. |
| 4 | Lokale Auth-Guards: `app.js`, `docs/SUPABASE_AUTH_GUARD_TEST_MODE.md` | D | `getCurrentAccessState()` und `renderLoginOrAccessNotice()` blockieren lokale Testfälle deterministisch. | Der Standard ist bewusst fail-open für den lokalen Betrieb. Dieser Fallback darf nicht ungeprüft zum Produktionszugang werden. |
| 5 | Login-/Sperr-/Ablauf-Testzustände: `app.js` und die Auth-/Access-State-Testdokumente | D | `login_required`, `expired`, `blocked` und `no_course` sind lokal darstellbar; Rücksetzen ist möglich. | Keine Authentifizierung, kein Passwortfluss, kein Session-Refresh, keine Backendentscheidung. |

## 5. Config und SDK

| Nr. | Bereich und Dateien | Stufe | Tatsächlicher Stand | Vorbereitung, Lücke, Abhängigkeit und Risiko |
|---:|---|:---:|---|---|
| 6 | Config-Platzhalter: `data/supabase-config.example.js`, `.gitignore`, `docs/SUPABASE_CONFIG_SAFETY_PLAN.md` | D | Beispiel enthält nur URL- und Anon-Key-Platzhalter; Platzhalter werden erkannt. | Kein genehmigter öffentlicher Dev-Config-Weg ist aktiv. Service-Role, DB-Passwort und private Schlüssel bleiben zu Recht verboten. |
| 7 | Config-Lader und Config-State: `data/supabase-config-loader.js`, `app.js`, Loader-/State-Tests | D | Der separate Loader ist standardmäßig deaktiviert und fail-safe; `app.js` versucht zusätzlich optional, dieselbe lokale Config per `fetch` zu laden. | Zwei Ladewege sind redundant. Der `fetch`-/Inline-Script-Weg in `app.js` und der Script-Loader sollten vor Live-Betrieb auf einen kanonischen Weg reduziert und CSP-seitig bewertet werden. |
| 8 | SDK-Ladeweg und SDK-State: `docs/SUPABASE_SDK_LOADING_PLAN.md`, `data/supabase-client-adapter.js`, `index.html` | D | Fehlen oder Ungültigkeit von `window.supabase.createClient` wird lokal korrekt klassifiziert. | Das SDK selbst wird nicht geladen; `index.html` enthält keinen Supabase-SDK-Eintrag. Die getestete Zustandslogik ist nicht gleichbedeutend mit einem installierten SDK. |

## 6. Client- und Adapter-Schicht

| Nr. | Bereich und Dateien | Stufe | Tatsächlicher Stand | Vorbereitung, Lücke, Abhängigkeit und Risiko |
|---:|---|:---:|---|---|
| 9 | Supabase-Client-Adapter: `data/supabase-client-adapter.js`, `docs/SUPABASE_CLIENT_ADAPTER_PLAN.md`, `docs/SUPABASE_CLIENT_ADAPTER_TEST.md` | D | Ein 25.330-zeiliger globaler Adapter liefert viele deterministische lokale States, Normalizer und Guards. | Er besitzt keinen aktiven Clientpfad für Session, Profil, Enrollment oder Fortschritt. Größe und Zustandszahl erhöhen Änderungs- und Auditrisiko. |
| 10 | Client-Readiness: Adapter, `docs/SUPABASE_CLIENT_READINESS_TEST.md` | D | Config, SDK, Live-Schalter und Fail-Safe werden ausgewertet; `canCreateClient` bleibt im Adapter immer `false`. | Die Readiness kennt den separat vorhandenen Bootstrap-Client nicht als nutzbare Dependency. Adapter und Bootstrap sind funktional nicht verbunden. |
| 11 | Manueller Client-Bootstrap: `data/supabase-client-bootstrap.js`, `docs/SUPABASE_CLIENT_BOOTSTRAP_TEST.md` | E | Reale `supabase.createClient(url, anonKey, authOptions)`-Logik ist vorhanden und streng manuell gegated. | Das ist näher an einer echten Anbindung als die frühen Planungsdokumente vermuten lassen. Es fehlen SDK, öffentliche Dev-Config, Client-Injektion in den Auth-Adapter und echte Integrationstests. Rohes Initialisierungs-`message` im lokalen State sollte vor produktiver Anzeige begrenzt werden. |
| 12 | Auth-Readiness: Adapter, `docs/SUPABASE_AUTH_READINESS_TEST.md` | D | `getAuthReadinessState()` und `getCurrentSession()` liefern stabile lokale Ergebnisse. | `canCheckSession` ist immer `false`; `getCurrentSession()` ruft niemals `client.auth.getSession()` auf. Login, Logout und Auth-State-Change fehlen. |
| 13 | Teilnehmerzugangs-Readiness: Adapter und Teilnehmerzugangs-Tests | D | Session-, Profil-, Kurs- und Access-Decision-Stubs sowie Health-State sind lokal konsistent. | Alle benötigten Backendinformationen sind `null` oder deaktiviert; lokaler Zugriff ist absichtlich erlaubt. Es gibt keine kanonische produktionsnahe Access-Resolver-Schnittstelle. |

## 7. Teilnehmerzugang / Kurse / Enrollment

| Nr. | Bereich und Dateien | Stufe | Tatsächlicher Stand | Vorbereitung, Lücke, Abhängigkeit und Risiko |
|---:|---|:---:|---|---|
| 14 | Kurse: `docs/SUPABASE_USER_PROGRESS_SCHEMA.md`, `supabase/migrations/20260710_v2720b_mvp_schema.sql` | E | Tabelle `courses` mit Status und Zeitraum liegt als SQL vor. | Nicht migriert oder datenbankgetestet. Plan nennt teils `starts_at`/`ends_at`, Migration `start_date`/`end_date`; diese Semantik muss vor Adaptercode kanonisch festgelegt werden. |
| 15 | Enrollment/Teilnehmerzuordnung: Plan, MVP-Schema und RLS | E | Migrationen enthalten `participants` und `enrollments`, Auth-Bindung über `participants.auth_user_id` und eindeutige Teilnehmer-/Kurszuordnung. | Ältere Pläne nennen `profiles` und `course_enrollments`. Ohne verbindliches Mapping wäre eine Auth-Implementierung mehrdeutig. Keine Zeile wurde real abgefragt. |
| 16 | Ablaufdatum/Zugangsstatus: MVP-Schema, RLS, lokale Access-States | E | `participants.status`, `courses.status`, Kursdaten sowie `enrollments.access_status/access_starts_at/access_ends_at` sind als SQL vorbereitet; lokale UI-Zustände existieren. | Es fehlt eine einzige servernahe Entscheidungsfunktion mit klarer Zeitzone, Vorrangregeln und Fehlerabbildung. Die lokale App prüft diese Spalten nicht. |

## 8. Fortschritt und Dashboard

| Nr. | Bereich und Dateien | Stufe | Tatsächlicher Stand | Vorbereitung, Lücke, Abhängigkeit und Risiko |
|---:|---|:---:|---|---|
| 17 | Fortschritt pro `user_id`: `docs/SUPABASE_USER_PROGRESS_SCHEMA.md`, `app.js` | B | Das Zielmodell für schriftliche Fragen, Prüfungen, Lernkarten und Fehlerhistorien ist detailliert geplant. Die App speichert Fortschritt tatsächlich nur lokal. | Die geplanten Fortschrittstabellen sind nicht als entsprechende Migration vorhanden; es gibt keine Migration von `localStorage`, Konfliktstrategie oder serverseitige Speicherung pro Nutzer. |
| 18 | Dashboard-Datenquellen: Adapter, `app.js`, zahlreiche Dashboard-State-Tests | D | Dashboard, Empfehlungen und Lernstände funktionieren aus lokalen Daten; Supabase-bezogene Dashboard-States sind lokal verborgen oder erlaubt. | Die Supabase-States enthalten keine echten Datenquellen. Die lokale Empfehlung in `app.js` liest lokale Speicherstände, nicht `user_id`-gebundene Daten. |
| 19 | Prüfungsverlauf: Ergebnis-RPC-Migration, Adapter und v27.29*-Tests | E | RPC, Pagination, Normalizer, Response-, Request-, Snapshot- und Persistenzzustände sind statisch beziehungsweise per Fixtures umfangreich geprüft. | `listParticipantFullExamResults()` führt keinen Client-/RPC-Aufruf aus und die Dashboard-Historie bleibt verborgen. Viele Zustände liegen weit vor einer ersten Auth-Session und erzeugen Wartungslast. |
| 20 | Zertifikats-/Dashboard-Vorbereitung: MVP-Schema und Zertifikats-/Dashboard-State-Tests | E | Eine Zertifikatstabelle mit RLS ist als SQL vorbereitet; lokale Dashboardzustände verhindern Anzeige und Aktionen. | Kein Ausstellungs-, Download-, Widerrufs- oder Verifikationsweg ist aktiv. 58 allein nach dem Zertifikats-State-Muster benannte Testdokumente zeigen Überfragmentierung ohne Datenquelle. |

## 9. SQL / Migrationen / RPC

| Nr. | Bereich und Dateien | Stufe | Tatsächlicher Stand | Vorbereitung, Lücke, Abhängigkeit und Risiko |
|---:|---|:---:|---|---|
| 21 | SQL-Planungen: Fragen-, Nutzer-, Roadmap- und Datenbankpläne | B | Datenmodelle, Reihenfolgen, Integrität und Sicherheitsziele sind umfangreich beschrieben. | Mehrere historische Modelle und Benennungen sind nicht vollständig konsolidiert. Dokumentation darf nicht als ausgeführtes Schema behandelt werden. |
| 22 | Migrationen: `supabase/migrations/*.sql`, `tools/check-supabase-migrations.py` | E | 30 geordnete Migrationen decken MVP, Fragen, Snapshots, Integrität, Lockdown, Rollen, Ergebnis-RPCs, Idempotenz und Domain-Speicher ab; statische Checks existieren. | Keine Migration wurde in diesem Audit oder laut Plan live ausgeführt. Es fehlen ein belegter Dev-Datenbankstand, Migrationshistorie, Rollback-/Restore-Probe und echte Schema-Introspektion. |
| 23 | RPC-Verträge und SQL-RPCs: v27.27*, v27.29a, v27.31* | E | Start, Antwortspeicherung, Abschluss, Ergebnis, Historie, Operations-ID, Idempotenz und Domain-Mutation sind als SQL/Verträge vorhanden. | Keine echte Datenbankausführung. Auth-/Kurszugang für den App-Start sollte nicht von der komplexen Exam-History-Idempotenzkette abhängig gemacht werden. |

## 10. Sicherheits- und RLS-Stand

| Nr. | Bereich und Dateien | Stufe | Tatsächlicher Stand | Vorbereitung, Lücke, Abhängigkeit und Risiko |
|---:|---|:---:|---|---|
| 24 | RLS/Sicherheit: MVP-RLS, Fragen-RLS, Direct-Write-Lockdown, Rollenabgrenzung | E | RLS wird aktiviert; Eigenzugriff bindet an `auth.uid()`; spätere Migrationen sperren direkte Prüfungsschreibwege und trennen Support von Admin/Dozent bei Verwaltung. | Nur statisch belegt. Reale RLS-Matrizentests mit synthetischen Rollen, `anon`/`authenticated`, abgelaufenen Enrollments und Negativfällen fehlen. Die frühe Rollen-/Tabellennomenklatur muss konsolidiert werden. |

Unverändert notwendige Sicherheitsgrenzen:

- nur öffentlicher Anon-Key im Browser, niemals Service-Role, DB-Passwort oder
  JWT-Secret;
- `auth.uid()` als einzige Nutzeridentität, keine frei übergebene
  Teilnehmer-ID;
- Default-Deny und echte RLS-Tests vor jeder Live-Freigabe;
- keine autoritative Punkte-, Rollen- oder Zugriffentscheidung im Browser;
- kein stiller lokaler Fail-open-Modus in einer späteren Live-Konfiguration;
- keine Rohfehler, Schlüssel, Lösungsschlüssel oder fremden Teilnehmerdaten.

## 11. Test-, Fake- und Registry-Schichten

| Nr. | Bereich und Dateien | Stufe | Tatsächlicher Stand | Vorbereitung, Lücke, Abhängigkeit und Risiko |
|---:|---|:---:|---|---|
| 25 | Registry/Atomic Consumption und lokale Fake-/Testadapter: v27.31w–v27.34e, `tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_local_fake_driver.py` | D | Verträge, deterministische Resolver, Guards, Manipulationsmatrizen und ein instanzgebundener In-Memory-Fake-Treiber prüfen Einmalverbrauch, Replay, Parallelität und Reconciliation. | Der echte Registry-Adapter `tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter.py` existiert nicht. Die Kette ist für disposable PostgreSQL-Testumgebungsautorisierung relevant, aber keine Voraussetzung für Login, Session, Profil oder Kurszugang. |

Einordnung der Verträge:

- **Für den nächsten Auth-Schritt unmittelbar relevant:** Config-Sicherheit,
  Client-/SDK-Ladegrenze, manueller Bootstrap, Auth-/Participant-Access-Ziele,
  das aktuelle MVP-Schema und die aktuelle RLS-Bindung.
- **Später relevant:** Fragen-, Prüfungs-, Ergebnis-, RLS-, Idempotenz- und
  Domain-Speicher-RPCs, sobald Auth und ein Dev-Datenbankstand tatsächlich
  funktionieren.
- **Historische beziehungsweise für Login nicht erforderliche Last:** die sehr
  feingranularen Dashboard-/Zertifikats-States, Snapshot-Persistenzketten und
  Registry-Autorisierungsstufen. Sie dürfen ihre eigene Sicherheitswirkung
  behalten, sollten aber den ersten Auth-Adapter weder blockieren noch weiter
  vervielfachen.

## 12. Technische Schulden / Redundanzen

1. **Doppelter Config-Ladeweg:** `data/supabase-config-loader.js` und
   `app.js::loadOptionalSupabaseConfig()` versuchen auf unterschiedliche Weise,
   `data/supabase-config.local.js` zu laden.
2. **Getrennter Clientzustand:** Der Adapter behauptet dauerhaft
   `canCreateClient: false`, während der Bootstrap real `createClient()`
   aufrufen kann. Es fehlt Dependency Injection beziehungsweise eine
   kanonische Clientquelle.
3. **Schema-Namenskonflikt:** ältere Dokumente verwenden
   `profiles`/`course_enrollments`/`instructor`; die neueren MVP-Migrationen
   verwenden `participants`/`enrollments`/`dozent` und zusätzliche
   Supportregeln.
4. **Überdimensionierter Adapter:** 25.330 Zeilen bündeln Login-Stubs,
   Dashboard-Stubs, Zertifikatszustände, Prüfungshistorie und Persistenzlogik
   in einer globalen Datei.
5. **Überfragmentierung:** 267 `SUPABASE*`-Dokumente, 64 JSON-Verträge, 69
   `check-supabase*`-Checker und zahlreiche nahezu identische Hidden-/Locked-
   States erschweren die Ermittlung des tatsächlich ausführbaren Pfads.
6. **Vorauseilende Prüfungshistorie:** umfangreiche Request-, Snapshot-,
   Persistenz-, Idempotenz- und Registryketten existieren, obwohl Session,
   Profil und Kurszugang noch nicht real gelesen werden.
7. **Statische Sicherheit ohne Laufzeitnachweis:** SQL und RLS werden gründlich
   textuell geprüft, aber nicht gegen eine disposable oder Dev-Datenbank
   ausgeführt.
8. **Lokaler Fail-open-Standard:** für den aktuellen Offline-Betrieb richtig,
   vor produktiver Auth-Nutzung aber ausdrücklich zu trennen und fail-closed
   umzuschalten.

## 13. Was tatsächlich noch fehlt

Für einen ersten sicheren echten Auth-/Supabase-Pfad fehlen mindestens:

1. eine ausdrückliche Entscheidung, dass die aktuelle Migrationsterminologie
   `participants`/`enrollments`/`courses` kanonisch ist, oder ein eindeutiges
   Mapping aus den älteren Planbegriffen;
2. ein genehmigtes Dev-/Test-Supabase-Ziel ohne Produktions- oder echte
   Teilnehmerdaten;
3. ein reproduzierbar eingebundenes Supabase-SDK und genau ein öffentlicher,
   lokaler Config-Ladeweg;
4. ein gegen die Migrationen tatsächlich aufgebauter und introspektierter
   Dev-Schemastand;
5. ausgeführte RLS-Negativ- und Positivtests mit ausschließlich synthetischen
   Nutzern und Rollen;
6. eine kleine kanonische, injizierbare Auth-/Teilnehmerzugangsschnittstelle,
   die Session, Teilnehmer, Enrollment und Kurs zu genau einem Access-State
   zusammenführt;
7. Login, Logout, Session-Refresh und Auth-State-Change mit sicherem
   Fehlermapping;
8. erst danach die UI-Anbindung und die Umstellung vom lokalen Fail-open-Modus;
9. für Fortschritt pro `user_id` zusätzliche kanonische Migrationen und eine
   Konflikt-/Übernahmestrategie für bestehende lokale Daten.

## 14. Abhängigkeiten und Reihenfolge

Sichere Reihenfolge nach diesem Audit:

1. Schema-/Rollenbegriffe für den Auth-Zugriff innerhalb des nächsten kleinen
   Bausteins ausdrücklich an die aktuellen Migrationen binden.
2. Eine lokale, injizierbare Auth-/Access-Komponente mit Fake-Client bauen und
   vollständig testen.
3. Erst in einem später separat autorisierten Schritt SDK und öffentliche
   Dev-Config kanonisieren sowie Migrationen/RLS gegen ein synthetisches
   Dev-Ziel prüfen.
4. Erst danach Client, Login-UI und App-Start verbinden.
5. Fortschritt, Prüfungshistorie und Zertifikate erst nach belegtem Auth- und
   Kurszugang anbinden.

Die vorhandene Exam-History-/Registry-Kette ist keine Vorbedingung für Schritt
2 und darf dessen Umfang nicht erweitern.

## 15. Genau EIN empfohlener nächster Umsetzungsbaustein

### Empfehlung: lokale injizierbare Auth-/Teilnehmerzugangs-Komponente

**Ziel**

Eine kleine eigenständige Komponente implementieren, die ausschließlich über
einen injizierten Supabase-kompatiblen Client eine Session sowie den dazu
gehörenden `participants`-, `enrollments`- und `courses`-Zustand auswertet und
einen kanonischen, fail-closed Access-State zurückgibt. Ausgeführt und getestet
wird sie ausschließlich mit einem lokalen Fake-Client; sie wird noch nicht in
`index.html` oder `app.js` geladen.

**Warum genau dieser Schritt zuerst**

Er schließt die zentrale Lücke zwischen dem bereits realen, aber isolierten
Client-Bootstrap und den ausschließlich lokalen Access-Stubs. Gleichzeitig
konsolidiert er die aktuelle SQL-Nomenklatur, ohne SDK, Config, Netzwerk, UI,
Live-Schalter, Migrationen oder echte Daten freizugeben. Ein weiterer reiner
Readiness-Vertrag oder zusätzlicher Dashboard-State würde diese Lücke nicht
schließen.

**Voraussetzungen innerhalb des Bausteins**

- `participants`/`enrollments`/`courses` und die Spalten der aktuellen
  MVP-Migrationen werden für diese Komponente explizit als Quellvertrag
  gebunden;
- Nutzeridentität stammt ausschließlich aus `session.user.id`;
- aktuelle Zeit wird injiziert, damit Ablaufregeln deterministisch bleiben;
- der Test-Client ist lokal, synthetisch, in-memory und führt kein Netzwerk
  aus.

**Voraussichtlich benötigte Dateien**

- neue isolierte Implementierungsdatei, zum Beispiel
  `data/supabase-participant-access-adapter.js`;
- neuer lokaler Checker/Fixture-Test unter `tools/`;
- eine kompakte Test- und Schnittstellendokumentation unter `docs/`;
- `tools/preflight.py` zur dauerhaften Testeinbindung;
- die jeweils ausdrücklich autorisierten Projektsteuerungsdateien für den
  Task-Lifecycle.

`app.js`, `index.html`, `data/supabase-client-adapter.js`,
`data/supabase-client-bootstrap.js`, Config-Dateien, SQL und Migrationen sollen
in diesem Baustein unverändert bleiben.

**Ausdrücklich noch nicht machen**

- kein SDK laden und keinen realen Client erzeugen;
- keine Config aktivieren;
- keine Supabase-, Netzwerk- oder Datenbankverbindung;
- keine Migration oder SQL ausführen;
- kein Loginformular und keine App-Zugangssperre aktivieren;
- keine echten Schlüssel, Nutzer oder Teilnehmerdaten;
- keine Fortschritts-, Prüfungs-, Zertifikats- oder Registry-Anbindung;
- keinen Service-Role-Key und keine frei übergebene Nutzer-ID.

**Sicherheitsgrenzen**

- strikt injizierte Dependency, keine implizite globale Clientauflösung;
- fail-closed bei fehlender Session, fehlendem/gesperrtem Teilnehmer,
  fehlendem/gesperrtem/abgelaufenem Enrollment, inaktivem/abgelaufenem Kurs,
  Mehrdeutigkeit und jedem Queryfehler;
- defensive Kopien, keine Eingabemutation, keine Rohfehlerausgabe;
- genau definierte Queryreihenfolge und keine automatischen Retries;
- ausschließlich eigene Nutzerbindung über die Session-ID;
- keine Grant-, Token-, Service-Role- oder Adminlogik.

**Klare Akzeptanzkriterien**

1. Die Komponente akzeptiert nur einen explizit injizierten Client und eine
   injizierte UTC-Zeitquelle.
2. Lokale Fake-Tests decken mindestens ab: keine Session, ungültige Session,
   Teilnehmer fehlt/ist gesperrt/abgelaufen, kein Enrollment, Enrollment
   gesperrt/abgelaufen/noch nicht aktiv, Kurs fehlt/inaktiv/abgelaufen und
   gültiger Zugriff.
3. Fremde Nutzer- oder Teilnehmerbindungen, mehrere widersprüchliche Treffer
   und alle Transport-/Queryfehler werden geschlossen blockiert.
4. Der erfolgreiche State enthält nur die minimal nötigen kanonischen
   Identitäten und Zugangsmetadaten, keine Secrets und keine Rohzeilen.
5. Fake-Client und Eingaben bleiben unverändert; keine globale mutable State,
   kein Netzwerk, keine Datei-, Prozess- oder Umgebungsnutzung.
6. Checker, Manipulationsfälle, `git diff --check` und vollständiger Preflight
   bestehen.
7. Die aktuelle App startet weiterhin unverändert lokal; keine Browser- oder
   Live-Integration findet statt.

Diese Empfehlung ist **keine Autorisierung**, wählt keinen Task aus und legt
keine Versionsnummer fest.

## 16. Nicht autorisierte Folgeschritte

Nicht autorisiert sind insbesondere:

- Installation oder Laden des Supabase-SDK;
- Aktivierung von `ACCAOUI_SUPABASE_LIVE_ENABLED` oder der zweiten
  Bootstrap-Bestätigung;
- Erzeugung eines realen Clients;
- Nutzung einer echten URL oder eines echten Anon-/Service-Role-Keys;
- Verbindung zu Supabase, PostgreSQL oder einem anderen Netzwerkdienst;
- Ausführung von Migrationen, SQL oder RPCs;
- Erstellung echter Auth-Nutzer oder Teilnehmerdaten;
- Integration in `app.js`, `index.html`, Login-UI oder Dashboard;
- Umstellung des lokalen Zugangsmodus;
- Fortschritts-, Prüfungshistorie-, Zertifikats- oder Registry-Live-Anbindung;
- automatische Auswahl eines Folgetasks, Commit oder Push.
