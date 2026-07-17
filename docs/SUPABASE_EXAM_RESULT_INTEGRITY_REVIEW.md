# Accaoui §34a Lern-App – Prüfungsintegrität Behebungsnachweis

Stand: v27.28d

Status: ursprüngliche Befunde statisch behoben, nicht live ausgeführt

## Zweck

Dieses Dokument aktualisiert den ursprünglichen Sicherheitsreview
aus v27.24a.

Die damaligen Befunde bleiben als historische Ausgangslage
nachvollziehbar. Der heutige statische Behebungsstand wird getrennt
davon dokumentiert.

## Historische Ausgangsbefunde v27.24a

1. Browser konnte autoritative Prüfungsergebnisse direkt speichern.
2. Browser konnte Antwortpunkte und Richtig-/Falsch-Werte setzen.
3. Lösungsschlüssel lagen in einer teilnehmerlesbaren Antworttabelle.
4. Kurszugang und Einschreibung wurden beim Prüfungsstart nicht
   ausreichend serverseitig geprüft.
5. Zusätzliche Punkte-, Zeit-, JSON- und Eindeutigkeitsgrenzen fehlten.

## Behebungsstand

### Befund 1 – Prüfungsergebnis manipulierbar

Status: statisch behoben

- direkte Teilnehmer-Inserts in `exam_attempts` wurden gesperrt
- Prüfungsversuche werden über einen geprüften Start-RPC erstellt
- Punkte und Bestehensstatus werden serverseitig berechnet
- der Browser übermittelt keine autoritativen Ergebniswerte
- `score_points <= max_points` wird zusätzlich durch v27.28b erzwungen

### Befund 2 – Antwortbewertung manipulierbar

Status: statisch behoben

- direkte Inserts, Updates und Deletes auf `exam_answers` sind entzogen
- Antworten sind eindeutig an `attempt_question_id` gebunden
- der Browser übermittelt nur ausgewählte Antwortindizes
- Punkte und Richtig-/Falsch-Status werden serverseitig gesetzt
- `earned_points` bleibt zwischen null und `max_points`

### Befund 3 – Lösungsschlüssel sichtbar

Status: statisch behoben

- `correct_answers` wurde aus `exam_answers` entfernt
- zentrale Lösungsschlüssel liegen in einer privaten Tabelle
- jeder Prüfungsversuch besitzt einen privaten Schlüssel-Snapshot
- private Schlüssel besitzen keine Teilnehmer-Policy
- RPC-Rückgaben enthalten keine richtigen Indizes oder Erklärungen

### Befund 4 – Kurszuordnung nicht geprüft

Status: statisch behoben

Der Prüfungsstart-RPC prüft serverseitig:

- Identität über `auth.uid()`
- aktiven Teilnehmerstatus
- aktive Kurseinschreibung
- erlaubten Zugangsstatus
- Beginn und Ende des Zugangszeitraums
- aktiven Kursstatus

## Weitere ursprüngliche Integritätslücken

| Ursprüngliche Lücke | Heutiger statischer Stand |
|---|---|
| `score_points <= max_points` | Constraint v27.28b |
| `earned_points <= max_points` | Antwortintegrität v27.26e |
| `finished_at >= started_at` | Constraint v27.28b |
| nur eine Antwort pro Versuchsfrage | eindeutiger Constraint v27.26e |
| JSON-Werte müssen Arrays sein | JSONB-Checks v27.25c/v27.26e |
| wiederholte Übermittlung | idempotente Start- und Abschlusslogik |
| Überauswahl von Antworten | beim Speichern und vor Bewertung gesperrt |
| Ergebnisdaten widersprüchlich | Ergebnis-RPC prüft 82/120 und Kategorien |

## Direkte Mitarbeiter-Schreibrechte v27.28d

Zusätzlich statisch behoben:

- `exam_attempts_staff_manage` wurde entfernt
- `exam_answers_staff_manage` wurde entfernt
- `INSERT`, `UPDATE` und `DELETE` wurden für alle App-Rollen entzogen
- Support kann Prüfungsdaten nicht direkt verändern
- Admin und Dozent umgehen den RPC-Weg ebenfalls nicht
- spätere administrative Korrekturen benötigen einen
  eigenen sicheren und protokollierten RPC

## Vollsimulations-Zustand v27.28c

Zusätzlich statisch abgesichert:

- offener Vollsimulationsversuch: `0/120`, nicht bestanden
- abgeschlossener Vollsimulationsversuch:
  `passed = (score_points >= 60)`
- Vollsimulationen besitzen immer eine Startzeit
- Vollsimulationen besitzen exakt 120 Maximalpunkte
- ungültige vorhandene Zustände brechen die Migration ab

## Geschlossener Prüfungsweg

Der statisch vorbereitete Prüfungsweg besteht aus:

1. `accaoui_start_full_exam(...)`
2. `accaoui_save_exam_answer(...)`
3. `accaoui_finish_full_exam(...)`
4. `accaoui_get_full_exam_result(...)`

Details:

`docs/SUPABASE_EXAM_RPC_FLOW_AUDIT.md`

## Weiterhin keine Live-Freigabe

Die ursprünglichen Code- und Schema-Befunde sind statisch behoben.

Eine Live-Freigabe erfolgt trotzdem erst nach:

- kontrollierter Ausführung in einer getrennten Dev-/Staging-Datenbank
- echten RLS-Laufzeittests mit Testkonten
- positiven und negativen RPC-Tests
- Prüfung von Migration, Rollback und Backup
- ausdrücklicher Freigabe für die Supabase-Anbindung

## Sicherheitsgrenze

- keine Live-Supabase-Ausführung
- keine echten Supabase-Schlüssel
- keine echten Teilnehmerdaten
- keine Änderung an App-Code oder Fragenbeständen

Status: Ursprüngliche Prüfungsintegritätsbefunde statisch behoben;
Live-Freigabe bleibt bis zu getrennten Laufzeittests gesperrt.
