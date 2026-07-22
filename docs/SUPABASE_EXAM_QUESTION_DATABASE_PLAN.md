# Supabase Datenbankplan für Prüfungsfragen

Stand: v27.31f

Status: Datenbankplan, nicht live ausgeführt

## Ziel

Die lokale Fragenbank wird später kontrolliert in eine serverseitige,
versionierte und manipulationsgeschützte Struktur übertragen.

## Zuordnung aus questions.json

- `id` → `source_question_id`
- `category` → `category`
- `type` → `question_type`
- `points` → `points`
- `question` → `question_text`
- `answers` → `answer_options`
- `correct` → private Lösungsschlüssel-Tabelle
- `explanation` → private Lösungsschlüssel-Tabelle

## Tabelle exam_questions

Geplante Felder:

- `id uuid primary key`
- `source_question_id text not null`
- `version integer not null`
- `category text not null`
- `question_type text not null`
- `question_text text not null`
- `answer_options jsonb not null`
- `points smallint not null`
- `core_position smallint`
- `status text not null`
- `content_hash text not null`
- `created_at timestamptz not null`

Regeln:

- `question_type` nur `single`, `multiple`, `praxisfall` oder `combination`
- `single` und `combination` haben genau eine richtige Antwort
- `multiple` und `praxisfall` können mehrere richtige Antworten haben
- `points` nur 1 oder 2
- `core_position` nur 1 bis 82 oder null
- Kombination aus `source_question_id` und `version` ist eindeutig
- veröffentlichte Inhaltsversionen werden nicht überschrieben
- Änderungen erzeugen eine neue Version
- nur aktive Versionen dürfen für neue Prüfungen ausgewählt werden

Statuswerte:

- `draft`
- `active`
- `retired`

## Tabelle exam_question_answer_keys

Diese Tabelle ist für Teilnehmer vollständig gesperrt.

Geplante Felder:

- `question_id uuid primary key`
- `correct_answers jsonb not null`
- `explanation text`
- `answer_hash text not null`
- `created_at timestamptz not null`

Regeln:

- `question_id` verweist auf eine konkrete Fragenversion
- `correct_answers` muss ein JSON-Array sein
- Antwortindizes müssen innerhalb der Antwortmöglichkeiten liegen
- Lösungsschlüssel werden nicht über Teilnehmer-RPCs ausgegeben
- vorhandene Lösungsschlüssel werden nicht überschrieben

## Tabelle exam_attempt_questions

Diese Tabelle speichert die feste Frageauswahl eines Prüfungsversuchs.

Geplante Felder:

- `id uuid primary key`
- `exam_attempt_id uuid not null`
- `question_id uuid not null`
- `display_order smallint not null`
- `source_question_id_snapshot text not null`
- `question_version_snapshot integer not null`
- `category_snapshot text not null`
- `question_type_snapshot text not null`
- `question_text_snapshot text not null`
- `answer_options_snapshot jsonb not null`
- `max_points_snapshot smallint not null`
- `created_at timestamptz not null`

Regeln:

- jede Position pro Prüfungsversuch ist eindeutig
- jede Frage kommt pro Prüfungsversuch höchstens einmal vor
- sichtbare Inhalte werden beim Prüfungsstart festgeschrieben
- spätere Änderungen der Fragenbank verändern laufende Versuche nicht
- richtige Antworten werden nicht in dieser Tabelle gespeichert

## Tabelle exam_attempt_question_answer_keys

Diese private Tabelle friert den Lösungsschlüssel ein, der beim
Start eines konkreten Prüfungsversuchs gültig war.

Geplante Felder:

- `attempt_question_id uuid primary key`
- `correct_answers_snapshot jsonb not null`
- `explanation_snapshot text`
- `grading_rule text not null`
- `answer_hash_snapshot text not null`
- `created_at timestamptz not null`

Regeln:

- genau ein privater Lösungsschlüssel pro Versuchsfrage
- Bewertungsregel: `per_correct_selection_no_penalty`
- jede ausgewählte richtige Antwort ergibt einen Punkt
- falsche Auswahlen ergeben keinen Punkt und keinen Punktabzug
- Deckelung durch `max_points_snapshot`
- Erstellung gemeinsam mit dem sichtbaren Fragen-Snapshot
- spätere Änderungen am zentralen Lösungsschlüssel verändern
  bestehende Prüfungsversuche nicht
- kein direkter Teilnehmer-, Support- oder Browserzugriff
- Lesen und Schreiben nur über geprüfte Bewertungs-RPCs

## Tabelle exam_answers nach Integritätsmigration v27.26e

Vorbereitete Zielstruktur:

- `exam_attempt_id uuid not null`
- `attempt_question_id uuid not null`
- `selected_answers jsonb not null`
- `earned_points integer not null`
- `max_points integer not null`
- `is_correct boolean not null`
- `created_at timestamptz not null`

Entfernt:

- freie `question_id text`
- teilnehmerlesbare `correct_answers`

Regeln:

- genau eine Antwortzeile pro `attempt_question_id`
- `attempt_question_id` muss zum gleichen `exam_attempt_id` gehören
- `selected_answers` muss ein JSON-Array sein
- `max_points` nur 1 oder 2
- `earned_points` nur zwischen 0 und `max_points`
- `is_correct=true` setzt die volle Punktzahl voraus
- bestehende Altdaten werden nicht automatisch gelöscht
- direkte Inserts, Updates und Deletes sind vollständig entzogen
- Schreiben und Bewerten nur über geprüfte Security-Definer-RPCs

## Zugriffsregeln

### Teilnehmer

Teilnehmer erhalten:

- keinen direkten Zugriff auf die gesamte Fragenbank
- keinen Zugriff auf `exam_question_answer_keys`
- keinen Zugriff auf `exam_attempt_question_answer_keys`
- nur die festen Fragen ihres eigenen Prüfungsversuchs
- keine direkten Insert-, Update- oder Delete-Rechte

### Mitarbeiter

- Admin und Dozent dürfen Fragen verwalten
- Support erhält keinen Zugriff auf Lösungsschlüssel
- für Prüfungsinhalte wird eine eigene Rollenprüfung benötigt

Geplanter Rollen-Helper:

`accaoui_is_exam_content_manager()`

Erlaubte Rollen:

- `admin`
- `dozent`

## Importprüfung für questions.json

Vor einem Import wird geprüft:

- jede Fragen-ID ist eindeutig
- Kategorie ist kanonisch
- Typ ist `single`, `multiple`, `praxisfall` oder `combination`
- Punktewert ist 1 oder 2
- Antwortmöglichkeiten bilden ein JSON-Array
- richtige Antwortindizes existieren tatsächlich
- Indizes sind eindeutig
- `single` und `combination` besitzen genau eine richtige Antwort
- `multiple` und `praxisfall` besitzen mindestens eine richtige Antwort
- Core-Auswahl enthält exakt 82 Positionen und 120 Punkte
- jede importierte Version erhält einen Inhalts-Hash

## Prüfungsstart-RPC v27.27a

Der vorbereitete RPC `accaoui_start_full_exam(p_course_id uuid)`:

- bestimmt den Teilnehmer ausschließlich über `auth.uid()`
- prüft aktiven Teilnehmer-, Kurs- und Einschreibungsstatus
- berücksichtigt Beginn und Ende des Kurszugangs
- verhindert parallele doppelte Prüfungsstarts
- setzt einen vollständigen offenen Versuch sicher fort
- verlangt exakt 82 Core-Fragen und 120 Punkte
- erstellt sichtbare und private Snapshots atomar
- verwendet `per_correct_selection_no_penalty`
- gibt keine Lösungsschlüssel oder Erklärungen zurück
- besitzt einen festen `search_path`
- ist nur für `authenticated` ausführbar
- wurde noch nicht live ausgeführt

## Antwortspeicher-RPC v27.27b / Korrektur v27.27c

Der Antwortspeicher-RPC:

- akzeptiert nur Versuchsfragen-ID und ausgewählte Indizes
- prüft die eigene offene Vollsimulation
- akzeptiert keine Browserpunkte oder Lösungsschlüssel
- validiert und normalisiert alle Antwortindizes
- erlaubt bei `single` und `combination` höchstens eine Auswahl
- erlaubt bei `multiple` und `praxisfall` mehrere Auswahlen
- koppelt die erlaubte Auswahlzahl nicht an den Punktewert
- speichert bis zur Bewertung neutrale Ergebniswerte
- wurde noch nicht live ausgeführt

## Prüfungsabschluss-RPC v27.27d

Der vorbereitete RPC `accaoui_finish_full_exam(...)`:

- akzeptiert ausschließlich die Prüfungsversuchs-ID
- bestimmt den Teilnehmer über `auth.uid()`
- erlaubt nur den eigenen Vollsimulationsversuch
- sperrt den Versuch gegen parallele Abschlussaufrufe
- behandelt wiederholte Abschlussaufrufe idempotent
- verlangt vollständige 82/120-Fragen- und Schlüsselsnapshots
- ergänzt unbeantwortete Fragen mit neutralen Antwortzeilen
- bewertet ausschließlich gegen private Versuchsschlüssel-Snapshots
- vergibt volle Punkte bei exakter Antwort
- vergibt Teilpunkte pro richtigem Kreuz ohne Punktabzug
- schreibt Punkte, Bestehensstatus und Abschlusszeit atomar
- setzt die Bestehensgrenze auf 60 von 120 Punkten
- gibt keine Lösungsschlüssel oder Erklärungen zurück
- ist ausschließlich für `authenticated` ausführbar
- wurde noch nicht live ausgeführt

## Auswahlbegrenzungs-Korrektur v27.27e

Die korrigierten Antwortspeicher- und Abschlussfunktionen:

- leiten die erlaubte Auswahlzahl aus dem privaten Versuchsschlüssel ab
- geben keine richtigen Antwortindizes an den Browser zurück
- trennen Auswahlgrenze und erreichbare Punktzahl
- sperren Überauswahlen bereits beim Speichern
- prüfen Überauswahlen vor der Bewertung erneut
- verhindern das automatische Erzielen von Punkten durch Auswahl aller Optionen
- behalten die Teilpunktebewertung ohne Punktabzug bei
- wurden noch nicht live ausgeführt

## Prüfungsergebnis-RPC v27.27f

Der vorbereitete RPC
`public.accaoui_get_full_exam_result(p_exam_attempt_id uuid)`:

- bestimmt den Teilnehmer ausschließlich über `auth.uid()`
- erlaubt nur den eigenen abgeschlossenen Vollsimulationsversuch
- erlaubt historische Ergebnisse für `active`, `expired` und `completed`
- schließt den Teilnehmerstatus `blocked` aus
- verlangt exakt 82 Fragen-Snapshots und 120 Gesamtpunkte
- verlangt exakt 82 gespeicherte Antwortzeilen
- gleicht die gespeicherten Antwortpunkte mit `score_points` ab
- gleicht `passed` mit `score_points >= 60` ab
- prüft beantwortete und unbeantwortete Fragen auf insgesamt 82
- prüft richtige, teilweise richtige, falsche und unbeantwortete Fragen auf insgesamt 82
- gibt nur eine sichere Ergebniszusammenfassung zurück
- gibt keine Lösungsschlüssel, Erklärungen oder richtigen Antwortindizes zurück
- liest keine privaten Versuchsschlüssel-Tabellen
- ist ausschließlich für `authenticated` ausführbar
- wurde nicht live ausgeführt

## Prüfungsergebnisliste v27.29a

Der vorbereitete RPC
`public.accaoui_list_full_exam_results(p_limit, p_offset)`:

- bestimmt den Teilnehmer ausschließlich über `auth.uid()`
- lädt nur eigene abgeschlossene Vollsimulationen
- erlaubt historische Ergebnisse für `active`, `expired` und `completed`
- schließt `blocked` aus
- begrenzt das Limit auf 1 bis 50
- begrenzt den Offset auf 0 bis 10000
- sortiert deterministisch nach Abschlusszeit und Versuchs-ID
- liefert die Gesamtzahl über `total_count`
- gibt keine Antworten, Schlüssel oder Erklärungen zurück
- ist ausschließlich für `authenticated` ausführbar
- wurde nicht live ausgeführt

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_RPC_TEST.md`

## Ergebnislisten-Adaptervertrag v27.29b

Der lokale Supabase-Adapter enthält jetzt:

- einen klaren State für den RPC
  `accaoui_list_full_exam_results`
- ausschließlich `p_limit` und `p_offset` als spätere Parameter
- lokale Prüfung der Pagination
- einen stabilen leeren Rückgabevertrag
- einen sicheren Blockierungsgrund im lokalen Modus
- keine Teilnehmer-ID als Browserparameter
- keinen echten RPC-, Client- oder Netzwerkaufruf

Die bestehende Prüfungshistorie bleibt lokal verborgen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_ADAPTER_TEST.md`

## Dashboard-Datenquellen-Zuordnung v27.29c

Der vorbereitete Ergebnislisten-RPC ist jetzt als zukünftige
Datenquelle der bestehenden Dashboard-Prüfungshistorie zugeordnet.

Dabei gilt weiterhin:

- keine sichtbare Prüfungshistorie
- kein echter RPC-Aufruf
- keine Netzwerkverbindung
- leeres Ergebnisarray
- keine Teilnehmer-ID als Parameter
- keine Blockierung des lokalen Betriebs
- vorhandener RPC- und Paginationvertrag bleibt unverändert

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_DASHBOARD_SOURCE_TEST.md`

## Ergebniszeilen-Normalizer v27.29d

Vor einer späteren Dashboard-Nutzung werden RPC-Ergebniszeilen
streng normalisiert.

Geprüft werden:

- UUIDs
- ausschließlich erlaubte Ergebnisfelder
- exakt 120 Maximalpunkte
- Punktebereich 0 bis 120
- Bestehensgrenze 60 Punkte
- gültige Start- und Abschlusszeiten
- konsistentes `total_count`
- doppelte Prüfungsversuchs-IDs

Ungültige Listen werden vollständig geschlossen verworfen.

Es gibt weiterhin keinen Live-RPC-Aufruf und kein sichtbares UI.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_ROW_NORMALIZER_TEST.md`

## Seitenbezogener Ergebnis-Aggregator v27.29e

Normalisierte Ergebniszeilen können jetzt sicher zu Kennzahlen
der aktuell geladenen Seite zusammengefasst werden.

Berechnet werden ausschließlich:

- Seitenanzahl
- bestandene und nicht bestandene Seiteneinträge
- Seitenbestwert
- Seitendurchschnitt
- Seitenbestehensquote
- neuester Eintrag der Seite

Wegen der Pagination werden keine Seitenwerte als globale
Bestanden-, Nicht-bestanden-, Durchschnitts- oder Bestwertzahlen
ausgegeben.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PAGE_AGGREGATOR_TEST.md`

## Lokale Fixture-Tests v27.29g

Normalizer und seitenbezogener Aggregator werden jetzt mit
festen lokalen Beispieldaten tatsächlich ausgeführt.

Geprüft werden gültige, leere und ungültige Ergebnislisten,
Duplikate, `total_count`, 120/60-Punktelogik sowie alle
seitenbezogenen Kennzahlen.

Der Fixture-Test läuft isoliert ohne Supabase-Client,
Netzwerkverbindung oder echte Teilnehmerdaten und ist in den
Preflight eingebunden.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_FIXTURE_TEST.md`

## Sicherer Response-Mapper v27.29h

Spätere Antworten des Ergebnislisten-RPC werden lokal auf einen
stabilen und datensparsamen Vertrag reduziert.

Erfolg, leere Ergebnisse, ungültige Daten und RPC-Fehler werden
sicher getrennt. Rohe Backend-Fehlerdetails und unbekannte
Transportfelder werden nicht übernommen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_RESPONSE_MAPPER_TEST.md`

## Sicherer Ladezustands-Mapper v27.29i

Der lokale Adapter kann jetzt die Zustände vorbereitet, laden,
erfolgreich, leer und Fehler stabil und datensparsam abbilden.

Aufgelöste Antworten werden ausschließlich über den sicheren
Response-Mapper verarbeitet. Rohe Backend- und Netzwerkfehler
werden nicht übernommen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_LOAD_STATE_MAPPER_TEST.md`

## Pagination-Navigationsstate v27.29j

Die lokale Prüfungsergebnishistorie kann jetzt erste, mittlere,
letzte und leere Seiten sowie eine noch unbekannte Gesamtzahl
stabil abbilden.

Vorherige und nächste Offsets werden ausschließlich aus validem
Limit, ausgerichtetem Offset, Seiteneintragszahl und bekannter
Gesamtzahl berechnet. Die technische Offset-Grenze 10000 wird
nicht überschritten.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PAGINATION_STATE_TEST.md`

## Datenquellen-Orchestrator v27.29k

Ladezustand, sichere RPC-Response-Verarbeitung und Pagination
werden jetzt zu einem stabilen lokalen Gesamtzustand verbunden.

Der Orchestrator unterscheidet vorbereitet, lädt, erfolgreich,
leer und Fehler. Eine leere Folgeseite wird nicht fälschlich als
globale leere Prüfungshistorie behandelt.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_DATA_SOURCE_ORCHESTRATOR_TEST.md`

## Navigations-Intent-State v27.29l

Erste, vorherige, nächste und wiederholte Seitenanfragen werden
jetzt lokal in einen validierten, datensparsamen Request-State
überführt.

Navigation während des Ladens, Navigation außerhalb verfügbarer
Seiten und unzulässige Wiederholungen werden sicher blockiert.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_NAVIGATION_INTENT_TEST.md`

## Anfrage-Identitätsstate v27.29m

Jede lokale Seitenanfrage erhält jetzt eine deterministische
Identität aus Anfragefolge, Limit und Offset.

Eintreffende Antwortidentitäten werden erneut validiert und als
aktuell oder veraltet eingeordnet. Veraltete Antworten dürfen
nicht auf den aktiven Datenquellenzustand angewendet werden.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_REQUEST_IDENTITY_TEST.md`

## Response-Annahme-Guard v27.29n

Eintreffende Seitenantworten werden jetzt zuerst gegen die
Identität der aktiven Anfrage geprüft.

Nur exakt passende Antworten werden an den sicheren
Datenquellen-Orchestrator übergeben. Veraltete Antworten werden
vor dem Lesen des Response-Inhalts ignoriert.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_RESPONSE_ACCEPTANCE_GUARD_TEST.md`

## Anfrage-Lebenszyklus-State v27.29o

Lokale Ergebnislisten-Anfragen können jetzt als vorbereitet,
ausstehend, abgeschlossen oder verworfen eingeordnet werden.

Ein Abschluss ist nur mit einem angenommenen Response-State
derselben Anfrageidentität zulässig. Verwerfungsgründe sind
fest begrenzt.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_REQUEST_LIFECYCLE_TEST.md`

## Lebenszyklus-Übergangs-Guard v27.29p

Zustandswechsel lokaler Ergebnislisten-Anfragen werden jetzt
über einen eigenen sicheren Guard geprüft.

Vorbereitet darf nur zu ausstehend oder verworfen wechseln.
Ausstehend darf nur abgeschlossen oder verworfen werden.
Abgeschlossene und verworfene Anfragen sind Endzustände.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_REQUEST_LIFECYCLE_TRANSITION_TEST.md`

## Anfrage-Controller-State v27.29q

Navigation, Anfrageidentität, Lebenszyklus, Zustandsübergänge
und Response-Annahme werden jetzt in einem sicheren lokalen
Controller-State verbunden.

Der Controller kann Anfragen initialisieren, starten,
abschließen, navigieren und kontrolliert verwerfen. Veraltete
Responses werden weiterhin vor dem Lesen ignoriert.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_REQUEST_CONTROLLER_TEST.md`

## Controller-Snapshot-Normalizer v27.29r

Gespeicherte lokale Anfrage-Controllerzustände werden jetzt vor
einer Wiederaufnahme vollständig neu geprüft und kanonisch
reduziert.

Identität, Lebenszyklus, Statusflags, Pagination und vorherige
Navigationsanfrage müssen widerspruchsfrei zusammenpassen.
Ergebniszeilen werden nicht in den Snapshot-Ausgabestate
übernommen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_CONTROLLER_SNAPSHOT_TEST.md`

## Snapshot-Wiederaufnahme-State v27.29s

Normalisierte Controller-Snapshots können jetzt in einen
kanonischen lokalen Wiederaufnahme-State überführt werden.

Vorbereitete, ausstehende und vorbereitete Navigationsanfragen
werden sicher rekonstruiert. Abgeschlossene und verworfene
Zustände bleiben blockierte Endzustände.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_SNAPSHOT_RESUME_TEST.md`

## Snapshot-Erstellungsstate v27.29t

Wiederaufnehmbare Controllerzustände können jetzt in einen
versionierten, datensparsamen Snapshot überführt werden.

Vorbereitete, ausstehende und navigierte Zustände werden
kanonisch rekonstruiert und anschließend erneut durch den
Snapshot-Normalizer geprüft. Terminale Zustände bleiben
geschlossen blockiert.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_SNAPSHOT_CREATION_TEST.md`

## Snapshot-Serialisierungsstate v27.29u

Kanonisch erzeugte Snapshots können jetzt deterministisch als
JSON serialisiert werden.

Die serialisierte Struktur besitzt eine feste Begrenzung von
4096 UTF-8-Bytes, wird erneut geparst und muss anschließend den
Snapshot-Normalizer mit unveränderter Identität, Phase und
unverändertem Controllerstatus bestehen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_SNAPSHOT_SERIALIZATION_TEST.md`

## Snapshot-Deserialisierungsstate v27.29v

Serialisiertes Snapshot-JSON wird jetzt vor dem Parsen nach Typ
und maximal 4096 UTF-8-Bytes geprüft.

Nach dem Parsen müssen Snapshot-Normalizer, kanonische
Snapshot-Erstellung, erneute Serialisierung und sicherer
Wiederaufnahme-State vollständig übereinstimmen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_SNAPSHOT_DESERIALIZATION_TEST.md`

## Snapshot-Persistenzvertrag v27.29w

Für Snapshots existiert jetzt ein sicherer lokaler Vertrag für
Save-, Load- und Delete-Intents.

Speicherschlüssel werden aus einem festen Namensraum und der
kanonischen Anfrageidentität gebildet. Save und Load erzwingen
erneut Serialisierung beziehungsweise Deserialisierung und
Identitätsgleichheit. Es findet kein echter Storage-Zugriff statt.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_SNAPSHOT_PERSISTENCE_CONTRACT_TEST.md`

## Persistenz-Adapter-Readiness-State v27.29x

Ein später injizierter Snapshot-Storage-Adapter kann jetzt
ausschließlich lokal auf Read-, Write- und Delete-Fähigkeiten
geprüft werden.

Adaptermarker, Vertragsversion und eigene Datenmethoden werden
getrennt validiert. Getter, geerbte Methoden und Storage-
Operationen werden nicht ausgeführt.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_STORAGE_ADAPTER_READINESS_TEST.md`

## Persistenz-Operationsplan-State v27.29y

Persistenzvertrag und Storage-Adapter-Readiness werden jetzt
in einem sicheren lokalen Operationsplan verbunden.

Save benötigt Write, Load benötigt Read und Delete benötigt
Delete. Die jeweils geplante Methode wird dabei nicht aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_OPERATION_PLAN_TEST.md`

## Persistenz-Operationsfreigabe-State v27.29z

Ein vorbereiteter Persistenz-Operationsplan kann jetzt zusammen
mit Persistenzvertrag und aktueller Adapter-Readiness erneut
vollständig geprüft werden.

Die Readiness erhält einen deterministischen Fingerprint.
Veränderte Fähigkeiten oder manipulierte Plandaten werden
geschlossen blockiert. Keine Storage-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_OPERATION_RELEASE_TEST.md`

## Persistenz-Ausführungs-Guard v27.30a

Freigabe, Persistenzvertrag und tatsächlich injizierter
Storage-Adapter werden jetzt unmittelbar vor einer späteren
Ausführung erneut vollständig geprüft.

Operationsplan und Freigabe werden neu berechnet. Die benötigte
eigene Datenmethode muss vorhanden sein, wird aber nicht
aufgerufen oder im Ergebnisstate offengelegt.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_EXECUTION_GUARD_TEST.md`

## Persistenz-Aufrufvertrag v27.30b

Aus einem gültigen Persistenz-Ausführungs-Guard kann jetzt ein
kanonisches Methoden- und Argumenteschema erzeugt werden.

Read, Write und Delete besitzen feste Argumentnamen und eine
feste Reihenfolge. Schlüssel, Identitäten und Write-Payload
werden erneut geprüft. Keine Storage-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_INVOCATION_CONTRACT_TEST.md`

## Persistenz-Aufrufpaket-State v27.30c

Ausführungs-Guard, Aufrufvertrag und tatsächlich injizierter
Storage-Adapter werden jetzt erneut zu einem sicheren lokalen
Aufrufpaket zusammengebunden.

Guard und Aufrufvertrag werden vollständig neu erzeugt.
Operation, Methode, Identitäten und Argumente müssen exakt
übereinstimmen. Keine Storage-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_INVOCATION_PACKAGE_TEST.md`

## Persistenz-Ergebnisvertrag v27.30d

Spätere Rückgabewerte von Read, Write und Delete können jetzt
getrennt und datensparsam normalisiert werden.

Read akzeptiert kanonisches Snapshot-JSON oder einen leeren
Wert. Write verlangt eine eindeutige Bestätigung. Delete wird
idempotent als gelöscht oder bereits nicht vorhanden abgebildet.
Keine Storage-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_RESULT_CONTRACT_TEST.md`

## Persistenz-Ergebnisannahme-Guard v27.30e

Normalisierte Persistenzergebnisse können jetzt nur angenommen
werden, wenn sie zum aktuell aktiven Aufrufpaket gehören.

Aufrufpaket, Schlüssel, Operation und Identitäten werden erneut
geprüft. Ergebnisse älterer Aufrufpakete werden geschlossen als
veraltet ignoriert. Keine Storage-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_RESULT_ACCEPTANCE_TEST.md`

## Persistenz-Abschlussstate v27.30f

Angenommene Persistenzergebnisse können jetzt in sichere
terminale Zustände überführt werden.

Read wird als wiederaufnehmbar oder leer abgeschlossen. Write
wird eindeutig bestätigt. Delete wird als gelöscht oder bereits
nicht vorhanden idempotent abgeschlossen. Keine Storage- oder
UI-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_COMPLETION_STATE_TEST.md`

## Persistenz-Zyklusstate v27.30g

Aufrufpaket, Ergebnisvertrag, Ergebnisannahme und terminaler
Abschluss können jetzt als zusammenhängender Persistenzzyklus
geprüft werden.

Ergebnisannahme und Abschluss werden vollständig neu berechnet.
Alle Zustände, Schlüssel und Identitäten müssen exakt
übereinstimmen. Keine Storage- oder UI-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_STATE_TEST.md`

## Persistenz-Zyklus-Wiederholungs-Guard v27.30h

Terminal abgeschlossene Persistenzzyklen können jetzt anhand
ihrer kanonischen Zyklusidentität nur einmal freigegeben werden.

Bereits registrierte Zyklusidentitäten werden geschlossen
blockiert. Unterschiedliche neue Identitäten können in einem
begrenzten lokalen Folgezustand vorbereitet werden. Keine
Storage- oder UI-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REPETITION_TEST.md`

## Persistenz-Zyklusregister-State v27.30i

Die begrenzte Liste terminal abgeschlossener Zyklusidentitäten
kann jetzt kanonisch normalisiert und als versionierter lokaler
Register-Payload vorbereitet werden.

Identitäten werden strukturell geprüft, dedupliziert und
deterministisch sortiert. Ein gültiger Wiederholungs-Guard kann
genau einen neuen Eintrag ergänzen. Doppelte Zyklen lassen das
Register unverändert. Keine Storage- oder UI-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_STATE_TEST.md`

## Persistenz-Zyklusregister-Serialisierung v27.30j

Der kanonische und versionierte Payload des lokalen
Persistenz-Zyklusregisters kann jetzt deterministisch und
größenbegrenzt als JSON serialisiert werden.

Status, Flags, Identitäten und Payload werden erneut geprüft.
Der Register-Mapper wird für einen vollständigen Rundlauf erneut
ausgeführt. Keine Storage- oder UI-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_SERIALIZATION_TEST.md`

## Persistenz-Zyklusregister-Deserialisierung v27.30k

Serialisierte Persistenz-Zyklusregister können jetzt nach einer
Größenprüfung sicher geparst und als kanonische versionierte
Register-States rekonstruiert werden.

Payload, Version, Felder und Identitäten werden erneut geprüft.
Register-Mapper und Serialisierungsstate müssen einen exakten
Rundlauf ergeben. Keine Storage- oder UI-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_DESERIALIZATION_TEST.md`

## Persistenz-Zyklusregister-Vertrag v27.30l

Save, Load und Delete des lokalen Persistenz-Zyklusregisters
können jetzt in einem eigenen kanonischen Namensraum vorbereitet
werden.

Save akzeptiert ausschließlich einen gültigen und erneut
geprüften Register-Serialisierungsstate. Load und Delete besitzen
keinen Payload. Keine Storage- oder UI-Methode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_CONTRACT_TEST.md`

## Zyklusregister-Storage-Adapter-Readiness v27.30m

Ein später injizierter Storage-Adapter für das
Persistenz-Zyklusregister kann jetzt ausschließlich anhand
eigener Read-, Write- und Delete-Datenmethoden geprüft werden.

Geerbte Methoden und Accessor-Properties werden nicht akzeptiert.
Keine Methodenreferenz wird übernommen und keine Methode wird
aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_STORAGE_ADAPTER_READINESS_TEST.md`

## Zyklusregister-Persistenz-Operationsplan v27.30n

Zyklusregister-Vertrag und Adapter-Readiness können jetzt zu
einem sicheren lokalen Operationsplan verbunden werden.

Save wird Write, Load wird Read und Delete bleibt Delete.
Payload, Fähigkeiten und Readiness-Fingerprint werden erneut
geprüft. Fehlende Fähigkeiten werden geschlossen blockiert.
Keine Adaptermethode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_OPERATION_PLAN_TEST.md`

## Zyklusregister-Persistenz-Operationsfreigabe v27.30o

Ein Zyklusregister-Operationsplan kann jetzt nur mit derselben
erneut berechneten Adapter-Readiness freigegeben werden.

Readiness-Fingerprint, benötigte Fähigkeit, Operationsidentitäten
und Save-Payload werden erneut geprüft. Blockierte Pläne bleiben
geschlossen blockiert. Keine Adaptermethode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_OPERATION_RELEASE_TEST.md`

## Zyklusregister-Persistenz-Ausführungs-Guard v27.30p

Operationsfreigabe und derselbe injizierte Storage-Adapter
können jetzt unmittelbar vor einem späteren Methodenaufruf
erneut vollständig geprüft werden.

Readiness-Fingerprint, Fähigkeit, Methode, Identitäten und
Save-Payload werden erneut validiert. Blockierte Freigaben
bleiben geschlossen blockiert. Keine Adaptermethode wird
aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_EXECUTION_GUARD_TEST.md`

## Zyklusregister-Persistenz-Aufrufvertrag v27.30q

Der Zyklusregister-Ausführungs-Guard kann jetzt in kanonische
Read-, Write- und Delete-Aufrufargumente übersetzt werden.

Identitäten, Readiness-Fingerprint, Fähigkeit und Save-Payload
werden erneut geprüft. Blockierte Ausführungen bleiben ohne
Aufrufargumente geschlossen blockiert. Keine Adaptermethode wird
aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_INVOCATION_CONTRACT_TEST.md`

## Zyklusregister-Persistenz-Aufrufpaket v27.30r

Der kanonische Zyklusregister-Aufrufvertrag kann jetzt mit
demselben erneut geprüften Storage-Adapter und dessen eigener
Read-, Write- oder Delete-Methode verbunden werden.

Readiness-Fingerprint, Fähigkeit, Methode, Argumente,
Identitätskette und Save-Payload werden erneut geprüft.
Blockierte Verträge bleiben ohne Argumente geschlossen
blockiert. Keine Adaptermethode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_INVOCATION_PACKAGE_TEST.md`

## Zyklusregister-Persistenz-Ergebnisvertrag v27.30s

Spätere Read-, Write- und Delete-Rückgaben des
Persistenz-Zyklusregisters können jetzt streng und datensparsam
normalisiert werden.

Read akzeptiert ausschließlich kanonisches Register-JSON oder
einen leeren Wert. Write verlangt eine eindeutige Bestätigung.
Delete wird idempotent als gelöscht oder bereits nicht vorhanden
abgebildet. Rohe Fehlerdetails werden nicht übernommen und keine
Adaptermethode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_RESULT_CONTRACT_TEST.md`

## Zyklusregister-Persistenz-Ergebnisannahme v27.30t

Normalisierte Zyklusregister-Persistenzergebnisse können jetzt
nur dem aktuell passenden Aufrufpaket zugeordnet werden.

Aufrufpaket-Identität, Intent, Operation, Readiness,
Identitätskette und Ergebnisinhalt werden erneut geprüft.
Abweichende Paketidentitäten werden geschlossen als veraltet
ignoriert. Keine Adaptermethode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_RESULT_ACCEPTANCE_TEST.md`

## Zyklusregister-Persistenz-Abschlussstate v27.30u

Angenommene Zyklusregister-Persistenzergebnisse können jetzt in
terminale kanonische Zustände überführt werden.

Read wird als verwendbares Register oder leer abgeschlossen.
Write wird eindeutig bestätigt. Delete wird idempotent als
gelöscht oder bereits nicht vorhanden abgeschlossen.
Identitätskette, Readiness und Ergebnisinhalt werden erneut
geprüft. Keine Adaptermethode wird aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_COMPLETION_STATE_TEST.md`

## Zyklusregister-Persistenz-Zyklusstate v27.30v

Aufrufpaket, Ergebnisvertrag, Ergebnisannahme und terminaler
Abschluss des Zyklusregisters können jetzt als ein
zusammenhängender Persistenzzyklus erneut geprüft werden.

Ergebnisannahme und Abschluss werden neu berechnet und müssen
mit den bereitgestellten kanonischen Zuständen exakt
übereinstimmen. Identitäten, Status, Readiness und Ergebnisdaten
bleiben vollständig verbunden. Keine Adaptermethode wird
aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_CYCLE_STATE_TEST.md`

## Zyklusregister-Persistenz-Zyklus-Wiederholungs-Guard v27.30w

Ein terminal abgeschlossener Zyklusregister-Persistenzzyklus
kann jetzt nur einmal zur weiteren lokalen Verarbeitung
freigegeben werden.

Zyklusstatus, Identitätskette, Readiness und Ergebnisinhalt
werden erneut geprüft. Bereits registrierte Zyklusidentitäten
werden geschlossen blockiert. Unterschiedliche neue
Zyklusidentitäten bleiben zulässig. Keine Adaptermethode wird
aufgerufen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_CYCLE_REGISTRY_CYCLE_REPETITION_TEST.md`

## Persistenz-Rekursionsgrenze v27.30x

Die geplante weitere Registrierung der
Zyklusregister-Persistenzzyklen wurde nach einem
Architektur-Audit bewusst nicht als neuer State umgesetzt.

Die vorhandenen Register-Persistenz-Zyklusidentitäten
unterscheiden nur `load`, `save` und `delete`. Ein dauerhaftes
Folgeregister würde deshalb legitime spätere Vorgänge
fälschlich blockieren.

Die Persistenz eines solchen Folgeregisters würde außerdem
erneut ein eigenes Wiederholungsregister erfordern und damit
eine nicht abschließbare rekursive Kette erzeugen.

Die v27.30-Reihe endet deshalb an dieser klaren Grenze.
Produktive Idempotenz muss später über eindeutige
Operationsidentitäten und atomare Storage- oder
Datenbanksemantik umgesetzt werden.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PERSISTENCE_RECURSION_BOUNDARY_AUDIT.md`

## Produktiver Idempotenz-Integrationsvertrag v27.31a

Die Voraussetzungen für eine spätere produktive
Idempotenzlösung sind jetzt als lokaler Vertrag vorbereitet.

Jeder reale Write- oder Delete-Vorgang benötigt eine eigene
serverseitig ausgestellte UUID. Schreibvorgänge benötigen
zusätzlich einen kanonischen Payload-Fingerprint.

Die spätere Datenbank muss die vollständige Operationsidentität
atomar und eindeutig speichern. Wiederholte identische Vorgänge
dürfen das bereits vorhandene Ergebnis verwenden. Dieselbe
Operationsidentität mit abweichendem Payload muss geschlossen
abgelehnt werden.

Der lokale Vertrag behauptet weder eine bereits verifizierte
Identitätsquelle noch eine bereits erzwungene Atomarität.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_PRODUCTIVE_IDEMPOTENCY_INTEGRATION_CONTRACT_TEST.md`

## Idempotenz-Operationstabelle v27.31b

Eine vollständig gesperrte serverseitige Tabelle für spätere
produktive Idempotenz ist vorbereitet.

Die Tabelle speichert pro realem Write- oder Delete-Vorgang:

- serverseitig bestimmten Nutzerbezug
- kanonische Operationsidentität
- externe UUID Version 4
- Operationsbereich und Mutation
- Ressourcenidentität
- Write-Payload-Fingerprint
- Bearbeitungsstatus
- kanonisches Ergebnis oder stabilen Fehlercode
- Erstellungs-, Aktualisierungs- und Abschlusszeiten

Unique Constraints sichern sowohl die vollständige
Operationsidentität als auch Bereich, Mutation und externe UUID
atomar ab.

RLS ist aktiviert und erzwungen. Alle direkten Tabellenrechte
für `public`, `anon` und `authenticated` sind entzogen. Es
existiert keine Direktpolicy und keine App-Rollenfreigabe.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_IDEMPOTENCY_OPERATIONS_MIGRATION_TEST.md`

## Idempotenz-Reservierungs-RPC v27.31c

Ein interner atomarer Reservierungs-RPC ist vorbereitet.

Der RPC:

- bestimmt den Nutzer ausschließlich über `auth.uid()`
- akzeptiert keine Nutzer- oder Teilnehmer-ID
- validiert UUID, Bereich, Mutation, Ressource und Fingerprint
- reserviert neue Vorgänge über die Unique Constraints
- erkennt identische Wiederholungen
- sperrt vorhandene Vorgänge mit `FOR UPDATE`
- gibt vorhandene Pending-, Completed- oder Failed-Zustände
  bei identischer Wiederholung kontrolliert zurück
- blockiert Konflikte bei Nutzer, Ressource oder Fingerprint
- führt noch keine eigentliche Snapshot- oder Registermutation aus

Der RPC bleibt ein interner Sicherheitshelfer. Es gibt bewusst
kein direktes `GRANT EXECUTE` für App-Rollen. Eine spätere
Mutation muss Reservierung und Fachoperation innerhalb
derselben Datenbanktransaktion verbinden.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_IDEMPOTENCY_RESERVATION_RPC_TEST.md`

## Idempotenz-Abschluss-RPC v27.31d

Ein interner atomarer Abschluss-RPC ist vorbereitet.

Der RPC:

- bestimmt den Nutzer ausschließlich über `auth.uid()`
- akzeptiert keine Nutzer- oder Teilnehmer-ID
- verlangt einen zuvor reservierten Vorgang
- prüft Bereich, Mutation, Ressource und Fingerprint erneut
- sperrt die Operation mit `FOR UPDATE`
- überführt ausschließlich `pending` nach `completed` oder `failed`
- speichert bei Erfolg einen kanonischen JSONB-Ergebnis-Payload
- speichert bei Fehler nur einen stabilen Fehlercode
- lässt identische terminale Wiederholungen vollständig unverändert
- blockiert abweichende zweite Abschlüsse ohne Überschreiben

Der RPC bleibt intern und besitzt keine direkte
Ausführungsfreigabe für App-Rollen.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_IDEMPOTENCY_COMPLETION_RPC_TEST.md`

## End-to-End-Idempotenz-RPC-Flow-Audit v27.31e

Operationstabelle, Reservierungs-RPC und Abschluss-RPC werden
jetzt durch einen eigenen statischen Audit zusammenhängend
geprüft.

Der Audit erzwingt:

- dieselbe kanonische Identitätsparameterschnittstelle
- dieselbe kanonische Operationsidentität
- atomare Reservierung über die Unique Constraints
- Abschluss ausschließlich aus dem Pending-Zustand
- unveränderte Wiederverwendung identischer Terminalzustände
- Blockierung abweichender zweiter Abschlüsse
- vollständige direkte Zugriffssperre
- keine Fachmutation innerhalb der beiden internen Helfer

Der Audit stellt ausdrücklich fest, dass die spätere
Fachmutation noch nicht mit Reservierung und Abschluss
verbunden ist. Eine produktive Freigabe besteht deshalb noch
nicht.

Das Auditwerkzeug ist dauerhaft in den Preflight eingebunden.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_IDEMPOTENCY_FLOW_AUDIT.md`

## Transaktionaler Fachmutations-Integrationsvertrag v27.31f

Ein verbindlicher und maschinenlesbarer Vertrag legt jetzt die
spätere Integrationsgrenze für produktive Fachmutationen fest.

Verbindliche Reihenfolge:

1. authentifizieren und validieren
2. Operation atomar reservieren
3. Reservierungsstatus auswerten
4. ausschließlich bei `reserved_new` fachlich mutieren
5. terminalen Abschluss speichern
6. kanonisches Ergebnis zurückgeben

Bestehende Pending-, Completed- oder Failed-Operationen dürfen
keine erneute Fachmutation auslösen.

Erwartete Fachfehler müssen ihre Teilmutation in einer
Subtransaktion zurückrollen, bevor ein stabiler Failed-Abschluss
gespeichert wird. Unerwartete Fehler müssen die vollständige
Datenbanktransaktion zurückrollen.

Der Vertrag ist dauerhaft im Preflight geprüft. Es wurde kein
neuer SQL-RPC ergänzt und es besteht weiterhin keine
produktive Freigabe.

Details:

`docs/SUPABASE_EXAM_RESULT_HISTORY_TRANSACTIONAL_MUTATION_INTEGRATION_CONTRACT.md`

## Direkte Prüfungs-Schreibsperre v27.28d

Die zusätzliche Lockdown-Migration:

- entfernt direkte Mitarbeiter-Schreibpolicies für Prüfungsversuche
- entfernt direkte Mitarbeiter-Schreibpolicies für Prüfungsantworten
- entzieht `INSERT`, `UPDATE` und `DELETE` für alle App-Rollen
- lässt geprüfte Lesezugriffe bestehen
- zwingt alle Schreibvorgänge durch den sicheren RPC-Weg
- verhindert direkte Ergebnisänderungen durch Support
- verlangt für spätere administrative Korrekturen einen
  eigenen geprüften Admin-RPC
- wurde nicht live ausgeführt

Details:

`docs/SUPABASE_EXAM_DIRECT_WRITE_LOCKDOWN_TEST.md`

## Vollsimulations-Zustandsintegrität v27.28c

Die zusätzliche Zustandsmigration erzwingt:

- Vollsimulationen besitzen exakt 120 Maximalpunkte
- jede Vollsimulation besitzt eine Startzeit
- offene Versuche bleiben bei null Punkten und `passed=false`
- abgeschlossene Versuche besitzen einen zur Punktzahl passenden
  Bestehensstatus
- ungültige bestehende Zustände brechen die Migration ab
- bestehende Daten werden nicht automatisch verändert
- keine Live-Ausführung

Details:

`docs/SUPABASE_FULL_EXAM_STATE_INTEGRITY_TEST.md`

## Prüfungsversuch-Integrität v27.28b

Die zusätzliche Integritätsmigration:

- bricht bei vorhandenen ungültigen Punktewerten ab
- erzwingt `score_points <= max_points`
- bricht bei ungültigen Start-/Abschlusszeiten ab
- verlangt bei abgeschlossenen Versuchen eine Startzeit
- erzwingt `finished_at >= started_at`
- verändert keine bestehenden Daten automatisch
- wurde nicht live ausgeführt

Details:

`docs/SUPABASE_EXAM_ATTEMPT_INTEGRITY_TEST.md`

## End-to-End-Sicherheitsaudit v27.28a

Der vollständige sichere Prüfungsweg wurde zusammenhängend geprüft:

1. Prüfungsstart erzeugt feste sichtbare und private Snapshots
2. Antwortspeicherung akzeptiert nur gültige eigene Versuchsfragen
3. Prüfungsabschluss bewertet ausschließlich serverseitig
4. Ergebnisabruf liefert nur eine sichere Zusammenfassung

Der Migrationsprüfer erzwingt zusätzlich ausdrücklich, dass
richtige, teilweise richtige, falsche und unbeantwortete Fragen
zusammen exakt 82 ergeben.

Details:

`docs/SUPABASE_EXAM_RPC_FLOW_AUDIT.md`

## Sicherheitsgrenze

- kein Import über den Browser
- keine echten Teilnehmerdaten
- keine Live-Migration
- keine Service-Role-Schlüssel im Frontend
- keine Lösungsschlüssel in teilnehmerlesbaren Tabellen
- keine Bewertung im JavaScript-Browser als autoritative Quelle

## Umsetzungsreihenfolge

1. Schema-Migration für die vier sicheren Prüfungstabellen
2. RLS- und Rollenregeln
3. lokales Import- und Validierungswerkzeug
4. kontrollierter Fragenbank-Import
5. Prüfungsstart-RPC
6. Bewertungs-RPC
7. Ergebnis-RPC
8. getrennte Testumgebung

## Nächster Schritt

Nach GitHub-Bestätigung von `v27.31f` kann `v27.31g`
eine sichere Grenze für die vertrauenswürdige Ausstellung und
Wiederverwendung externer Operations-IDs vorbereiten.

Sie muss verhindern, dass beliebige browsergenerierte oder
fremde Operations-IDs als verifiziert gelten, und zugleich
eine stabile Wiederholungs-ID für denselben echten Vorgang
ermöglichen. Eine Live-Ausführung erfolgt weiterhin nicht.

Status: Sicherer Prüfungs-RPC-Weg, Prüfungsversuch-Integrität,
Vollsimulations-Zustandsintegrität, direkte Prüfungs-Schreibsperre,
Mitarbeiter-Rollentrennung, sichere Prüfungsergebnisliste,
lokaler Adaptervertrag, Dashboard-Datenquellen-Zuordnung,
Normalizer, Seitenaggregator, Fixture-Tests, sicherer
Response-Mapper, Ladezustands-Mapper, Pagination-State,
Datenquellen-Orchestrator, Navigations-Intent-State,
Anfrage-Identitätsstate, Response-Annahme-Guard,
Anfrage-Lebenszyklus-State, Lebenszyklus-Übergangs-Guard,
Anfrage-Controller-State, Controller-Snapshot-Normalizer,
Snapshot-Wiederaufnahme-State, Snapshot-Erstellungsstate,
Snapshot-Serialisierungsstate, Snapshot-Deserialisierungsstate,
Snapshot-Persistenzvertrag, Persistenz-Adapter-Readiness-State,
Persistenz-Operationsplan-State,
Persistenz-Operationsfreigabe-State,
Persistenz-Ausführungs-Guard, Persistenz-Aufrufvertrag,
Persistenz-Aufrufpaket-State, Persistenz-Ergebnisvertrag,
Persistenz-Ergebnisannahme-Guard, Persistenz-Abschlussstate,
Persistenz-Zyklusstate, Persistenz-Zyklus-Wiederholungs-Guard,
Persistenz-Zyklusregister-State,
Persistenz-Zyklusregister-Serialisierungsstate,
Persistenz-Zyklusregister-Deserialisierungsstate,
Persistenz-Zyklusregister-Vertrag,
Zyklusregister-Storage-Adapter-Readiness-State,
Zyklusregister-Persistenz-Operationsplan-State,
Zyklusregister-Persistenz-Operationsfreigabe-State,
Zyklusregister-Persistenz-Ausführungs-Guard,
Zyklusregister-Persistenz-Aufrufvertrag,
Zyklusregister-Persistenz-Aufrufpaket-State,
Zyklusregister-Persistenz-Ergebnisvertrag,
Zyklusregister-Persistenz-Ergebnisannahme-Guard,
Zyklusregister-Persistenz-Abschlussstate,
Zyklusregister-Persistenz-Zyklusstate und
Zyklusregister-Persistenz-Zyklus-Wiederholungs-Guard vorbereitet
sowie die Persistenz-Rekursionsgrenze v27.30x dokumentiert;
produktiver Idempotenz-Integrationsvertrag v27.31a und
vollständig gesperrte Idempotenz-Operationstabelle v27.31b und
interner atomarer Idempotenz-Reservierungs-RPC v27.31c und
interner atomarer Idempotenz-Abschluss-RPC v27.31d vorbereitet,
End-to-End-Idempotenz-RPC-Flow-Audit v27.31e und transaktionaler
Fachmutations-Integrationsvertrag v27.31f dauerhaft in den
Preflight eingebunden;
keine Live-Ausführung
