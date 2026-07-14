# Supabase Datenbankplan für Prüfungsfragen

Stand: v27.25b

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

- `question_type` nur `single` oder `multiple`
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

## Anpassung der bestehenden exam_answers

Später erforderlich:

- `question_id text` durch `attempt_question_id uuid` ersetzen
- `correct_answers` aus der teilnehmerlesbaren Struktur entfernen
- eindeutige Kombination aus Versuch und Prüfungsfrage
- `earned_points` und `is_correct` nur durch den Bewertungs-RPC setzen
- `selected_answers` muss ein gültiges JSON-Array sein

## Zugriffsregeln

### Teilnehmer

Teilnehmer erhalten:

- keinen direkten Zugriff auf die gesamte Fragenbank
- keinen Zugriff auf `exam_question_answer_keys`
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
- Typ ist `single` oder `multiple`
- Punktewert ist 1 oder 2
- Antwortmöglichkeiten bilden ein JSON-Array
- richtige Antwortindizes existieren tatsächlich
- Indizes sind eindeutig
- Single-Choice besitzt genau eine richtige Antwort
- Multiple-Choice besitzt mindestens eine richtige Antwort
- Core-Auswahl enthält exakt 82 Positionen und 120 Punkte
- jede importierte Version erhält einen Inhalts-Hash

## Sicherheitsgrenze

- kein Import über den Browser
- keine echten Teilnehmerdaten
- keine Live-Migration
- keine Service-Role-Schlüssel im Frontend
- keine Lösungsschlüssel in teilnehmerlesbaren Tabellen
- keine Bewertung im JavaScript-Browser als autoritative Quelle

## Umsetzungsreihenfolge

1. Schema-Migration für die drei neuen Tabellen
2. RLS- und Rollenregeln
3. lokales Import- und Validierungswerkzeug
4. kontrollierter Fragenbank-Import
5. Prüfungsstart-RPC
6. Bewertungs-RPC
7. Ergebnis-RPC
8. getrennte Testumgebung

## Nächster Schritt

`v27.25c`

Schema-Migration für `exam_questions`,
`exam_question_answer_keys` und `exam_attempt_questions` vorbereiten.

Status: sicherer Fragen-Datenbankplan festgelegt
