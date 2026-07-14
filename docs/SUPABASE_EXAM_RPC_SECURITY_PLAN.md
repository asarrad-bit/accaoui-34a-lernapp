# Supabase RPC-Plan für sichere Prüfungsbewertung

Stand: v27.25a

Status: Architekturplan, nicht live ausgeführt

## Ziel

Prüfungsversuche und Antworten dürfen nicht direkt vom Browser
als autoritative Ergebnisse gespeichert werden.

Punkte, Bestehensstatus und Richtig-/Falsch-Bewertungen werden
ausschließlich serverseitig berechnet.

## Verbindliche Sicherheitsregeln

Der Browser darf niemals selbst übermitteln:

- `participant_id`
- `score_points`
- `passed`
- `correct_answers`
- `earned_points`
- `is_correct`
- autoritative `max_points`

Der angemeldete Benutzer wird serverseitig über `auth.uid()` ermittelt.

## Erforderliche Datenbank-Erweiterung

Vor der RPC-Umsetzung werden benötigt:

1. `exam_questions`
   - Frage-ID
   - Fragetext
   - Antwortmöglichkeiten
   - Punkte
   - Status und Version

2. `exam_question_answer_keys`
   - Frage-ID
   - richtige Antworten
   - niemals für Teilnehmer lesbar

3. `exam_attempt_questions`
   - Prüfungsversuch
   - feste Frageauswahl
   - Reihenfolge
   - gültige Maximalpunkte

Der Lösungsschlüssel darf nicht in einer teilnehmerlesbaren Tabelle liegen.

## RPC 1 – Prüfungsstart

Geplanter Name:

`accaoui_start_exam(p_course_id uuid, p_mode text)`

Serverseitige Prüfungen:

- Benutzer ist angemeldet
- aktiver Teilnehmer zu `auth.uid()` vorhanden
- Teilnehmerstatus erlaubt Zugriff
- gültige Kurseinschreibung vorhanden
- Zugriffszeitraum ist gültig
- Kurs ist aktiv
- Prüfungsmodus ist erlaubt

Serverseitige Aktionen:

- Prüfungsversuch anlegen
- Teilnehmer-ID selbst bestimmen
- Startzeit selbst setzen
- feste Fragen auswählen
- Frageauswahl in `exam_attempt_questions` speichern
- keine Lösungsschlüssel ausgeben

Rückgabe:

- Prüfungsversuch-ID
- Fragen und Antwortmöglichkeiten
- Reihenfolge und Maximalpunkte
- keine richtigen Antworten

## RPC 2 – Prüfung abgeben

Geplanter Name:

`accaoui_submit_exam(p_attempt_id uuid, p_answers jsonb, p_request_id uuid)`

Serverseitige Prüfungen:

- Versuch gehört zum angemeldeten Teilnehmer
- Versuch ist noch nicht abgeschlossen
- jede Frage gehört zum festen Prüfungsversuch
- jede Frage kommt höchstens einmal vor
- ausgewählte Antworten sind gültige JSON-Arrays
- `p_request_id` verhindert doppelte Übermittlung

Serverseitige Aktionen in einer Transaktion:

- Antworten validieren
- private Lösungsschlüssel laden
- Punkte berechnen
- `is_correct` berechnen
- Gesamtpunktzahl berechnen
- Bestehensstatus berechnen
- Antworten speichern
- Versuch abschließen
- Audit-Eintrag erzeugen

Bei einem Fehler wird nichts teilweise gespeichert.

## RPC 3 – Ergebnis lesen

Geplanter Name:

`accaoui_get_exam_result(p_attempt_id uuid)`

Rückgabe nur bei abgeschlossenem Versuch:

- erreichte Punkte
- Maximalpunkte
- Bestehensstatus
- Abschlusszeit
- erlaubte Auswertung je Frage

Richtige Antworten werden nur ausgegeben, wenn später ausdrücklich
ein sicherer Nachbereitungsmodus beschlossen wird.

## RLS-Regeln

- keine direkten Teilnehmer-Inserts in `exam_attempts`
- keine direkten Teilnehmer-Inserts in `exam_answers`
- RPC-Funktionen erhalten eine feste `search_path`
- Funktionsberechtigungen nur für `authenticated`
- keine Service-Role-Schlüssel im Browser
- Antwortschlüssel sind für Teilnehmer vollständig gesperrt

## Noch offene Entscheidung

Die aktuelle lokale Fragenbank ist nicht ausreichend für eine sichere
serverseitige Bewertung.

Vor der RPC-Implementierung muss eine kanonische serverseitige
Fragen- und Lösungsschlüssel-Struktur aufgebaut werden.

## Nächster Schritt

`v27.25b`

Datenbankplan für Fragen, private Lösungsschlüssel und feste
Prüfungsfrage-Snapshots erstellen.

Status: RPC-Sicherheitsarchitektur festgelegt
