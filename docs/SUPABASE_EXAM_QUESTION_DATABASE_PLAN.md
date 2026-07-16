# Supabase Datenbankplan für Prüfungsfragen

Stand: v27.27c

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

`v27.27d`

Sicheren Prüfungsabschluss-RPC mit serverseitiger Bewertung
gegen die privaten Lösungsschlüssel-Snapshots vorbereiten.

Status: Antwortspeicher-RPC fachlich korrigiert
