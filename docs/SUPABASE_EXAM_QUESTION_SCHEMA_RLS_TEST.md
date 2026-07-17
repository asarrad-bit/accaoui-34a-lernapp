# Supabase Prüfungsfragen Schema- und RLS-Test

Stand: v27.28c

Status: statisch geprüft, nicht live ausgeführt

## Geprüfte Migrationen

- `20260716_v2725c_exam_question_schema.sql`
- `20260716_v2725d_exam_question_rls.sql`
- `20260716_v2726c_exam_attempt_answer_key_snapshot.sql`
- `20260716_v2726d_exam_attempt_grading_rule_partial_points.sql`
- `20260716_v2726e_exam_answers_integrity.sql`
- `20260716_v2727a_exam_start_rpc.sql`
- `20260716_v2727b_exam_answer_save_rpc.sql`
- `20260716_v2727d_exam_finish_rpc.sql`
- `20260716_v2727e_exam_selection_limit_security.sql`
- `20260717_v2727f_exam_result_rpc.sql`
- `20260717_v2728b_exam_attempt_integrity.sql`
- `20260717_v2728c_full_exam_state_integrity.sql`

## Geprüfte Tabellen

- `exam_questions`
- `exam_question_answer_keys`
- `exam_attempt_questions`
- `exam_attempt_question_answer_keys`

## Schema-Prüfung

Bestätigt wurden:

- versionierte Fragen
- getrennte private Lösungsschlüssel
- feste Prüfungsfrage-Snapshots
- private Lösungsschlüssel-Snapshots pro Versuchsfrage
- Teilpunkte: ein Punkt pro ausgewählter richtiger Antwort, kein Punktabzug
- `correct_answers` aus `exam_answers` entfernt
- Antworten eindeutig an `attempt_question_id` gebunden
- Versuchsfrage und Prüfungsversuch per Fremdschlüssel abgeglichen
- `selected_answers` als JSON-Array abgesichert
- Punktebereiche und Ergebniszustand abgesichert
- JSON-Array-Prüfungen
- vier Fragetypen: `single`, `multiple`, `praxisfall`, `combination`
- Punkte nur 1 oder 2
- Core-Positionen nur 1 bis 82
- eindeutige Fragenversionen
- keine doppelten Fragen oder Positionen je Versuch
- RLS auf allen vier Tabellen

## RLS-Prüfung

Bestätigt wurden:

- Prüfungsinhalte nur für aktive Admins und Dozenten
- Support ist ausgeschlossen
- zentrale und versuchsbezogene Lösungsschlüssel sind für Teilnehmer gesperrt
- Teilnehmer dürfen nur eigene Prüfungs-Snapshots lesen
- keine Teilnehmer-Schreibpolicy für Snapshots
- direkte Inserts, Updates und Deletes auf `exam_answers` entzogen
- fester `search_path` für den Rollen-Helper
- keine Live-Ausführung

## Prüfungsstart-RPC-Prüfung

Bestätigt wurden:

- Teilnehmeridentität ausschließlich über `auth.uid()`
- aktiver Teilnehmer-, Kurs- und Einschreibungszugang
- Advisory Lock gegen parallele Doppelstarts
- eindeutiger offener Versuch pro Teilnehmer und Kurs
- idempotentes Fortsetzen vollständiger offener Versuche
- exakt 82 Fragen und 120 Punkte
- atomare sichtbare und private Snapshots
- fester `search_path` und `row_security=off`
- Ausführungsrecht ausschließlich für `authenticated`
- keine Lösungsschlüssel in der RPC-Rückgabe

## Antwortspeicher-RPC-Prüfung

Bestätigt wurden:

- nur eigene offene Versuchsfragen
- ausschließlich Fragen-ID und ausgewählte Indizes als Eingabe
- keine Punkte oder Lösungsschlüssel als Browserparameter
- gültige, eindeutige und normalisierte Antwortindizes
- höchstens eine Auswahl bei `single` und `combination`
- mehrere Auswahlen bei `multiple` und `praxisfall`
- keine Begrenzung der Auswahlzahl durch den Punktewert
- neutrale Ergebniswerte bis zur serverseitigen Bewertung

## Prüfungsabschluss-RPC-Prüfung

Bestätigt wurden:

- ausschließlich eigener schriftlicher Vollsimulationsversuch
- Teilnehmeridentität über `auth.uid()`
- Sperre gegen parallele Abschlussaufrufe
- idempotente Rückgabe bereits gespeicherter Ergebnisse
- exakt 82 Fragen, 82 private Schlüssel und 120 Punkte
- neutrale Antwortzeilen für unbeantwortete Fragen
- serverseitige Bewertung gegen private Versuchsschlüssel
- volle Punkte bei exakter Antwort
- Teilpunkte ohne Punktabzug
- Bestehensgrenze 60 von 120 Punkten
- atomare Aktualisierung von Antworten und Prüfungsversuch
- keine Punkte oder Ergebniswerte als Browserparameter
- keine Lösungsschlüssel in der Rückgabe

## Auswahlbegrenzungs-Sicherheitsprüfung

Bestätigt wurden:

- Auswahlgrenze aus privatem Versuchsschlüssel
- keine Offenlegung richtiger Antwortindizes
- Trennung von Auswahlzahl und Fragepunktzahl
- Sperre gegen Überauswahl beim Speichern
- erneute Sperre gegen Überauswahl vor der Bewertung
- gültige Lösungssnapshot-Grenzen
- kontrolliertes Ersetzen beider RPC-Funktionen
- feste `search_path`- und `row_security`-Einstellungen
- Ausführungsrecht ausschließlich für `authenticated`

## Prüfungsergebnis-RPC-Prüfung

Bestätigt wurden:

- ausschließlich eigener abgeschlossener Vollsimulationsversuch
- Teilnehmeridentität ausschließlich über `auth.uid()`
- historische Ergebnisse für `active`, `expired` und `completed`
- Teilnehmerstatus `blocked` ausgeschlossen
- exakt 82 Fragen-Snapshots und 120 Gesamtpunkte
- exakt 82 gespeicherte Antwortzeilen
- Punkteabgleich zwischen Antworten und Prüfungsversuch
- Bestehensabgleich mit `score_points >= 60`
- beantwortete und unbeantwortete Fragen ergeben zusammen 82
- richtige, teilweise richtige, falsche und unbeantwortete Fragen ergeben zusammen 82
- sichere Ergebniszusammenfassung ohne Lösungsschlüssel
- keine Erklärungen oder richtigen Antwortindizes
- keine privaten Versuchsschlüssel-Tabellen im RPC
- keine Schreiboperationen
- Ausführungsrecht ausschließlich für `authenticated`



## Prüfungsversuch-Integritätsprüfung v27.28b

Bestätigt wurden:

- bestehende ungültige Punktewerte brechen die Migration ab
- bestehende ungültige Zeitwerte brechen die Migration ab
- `score_points` darf `max_points` nicht überschreiten
- abgeschlossene Versuche benötigen eine Startzeit
- Abschlusszeit darf nicht vor der Startzeit liegen
- keine automatische Datenänderung
- keine neue Policy und keine direkten Rechte
- dokumentiert in
  `docs/SUPABASE_EXAM_ATTEMPT_INTEGRITY_TEST.md`

## Vollsimulations-Zustandsintegrität v27.28c

Bestätigt wurden:

- Vollsimulationen besitzen immer exakt 120 Maximalpunkte
- Startzeit ist für Vollsimulationen verpflichtend
- offene Versuche besitzen null Punkte und sind nicht bestanden
- abgeschlossene Versuche gleichen `passed` mit
  `score_points >= 60` ab
- bestehende ungültige Daten brechen die Migration ab
- keine automatische Datenänderung oder Löschung
- keine neue Policy und keine direkten Rechte
- dokumentiert in
  `docs/SUPABASE_FULL_EXAM_STATE_INTEGRITY_TEST.md`

## End-to-End-Prüferabdeckung v27.28a

Zusätzlich statisch bestätigt:

- Start, Antwortspeicherung, Abschluss und Ergebnisabruf bilden
  einen geschlossenen serverseitigen Prüfungsweg
- Browserparameter enthalten keine autoritativen Ergebniswerte
- private Versuchsschlüssel bleiben außerhalb der Rückgaben
- der Migrationsprüfer erzwingt ausdrücklich, dass richtige,
  teilweise richtige, falsche und unbeantwortete Fragen
  zusammen exakt 82 ergeben
- dokumentiert in `docs/SUPABASE_EXAM_RPC_FLOW_AUDIT.md`

## Automatische Migrationsprüfung

Erwarteter Stand:

- 15 SQL-Dateien
- 8 MVP-Tabellen
- 4 sichere Prüfungstabellen
- 12 Tabellen insgesamt
- 15 effektive Basis-Policies
- 3 Fragen-RLS-Policies
- 18 effektive Policies insgesamt

## Sicherheitsgrenze

Die Migrationen sind vorbereitet und statisch geprüft.

Es wurden keine echten Supabase-Schlüssel verwendet und keine
Migration wurde auf einer Live-Datenbank ausgeführt.

Sichere Snapshot-Schreibvorgänge und Prüfungsbewertungen folgen
später ausschließlich über geprüfte RPC-Funktionen.

Status: Fragen-Schema, RLS, private Versuchsschlüssel, Teilpunkte,
Antwortintegrität, Prüfungsstart-RPC, Antwortspeicher-RPC,
Prüfungsabschluss, Auswahlbegrenzung, Ergebnisabruf und
Vollsimulations-Zustandsintegrität statisch bestätigt
