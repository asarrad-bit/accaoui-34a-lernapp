# Supabase Prüfungs-RPC-Flow – End-to-End-Sicherheitsaudit

Stand: v27.28a

Status: statisch geprüft, nicht live ausgeführt

## Ziel

Der vollständige serverseitige Ablauf der schriftlichen
Vollsimulation wird als zusammenhängender Sicherheitsweg geprüft.

Enthalten sind:

1. sicherer Prüfungsstart
2. sichere Antwortspeicherung
3. serverseitiger Prüfungsabschluss
4. sicherer Ergebnisabruf

## Geprüfte Funktionen

- `public.accaoui_start_full_exam(p_course_id uuid)`
- `public.accaoui_save_exam_answer(
    p_attempt_question_id uuid,
    p_selected_answers jsonb
  )`
- `public.accaoui_finish_full_exam(p_exam_attempt_id uuid)`
- `public.accaoui_get_full_exam_result(
    p_exam_attempt_id uuid
  )`

## Identität und Zugriff

- Identität ausschließlich über `auth.uid()`
- keine Teilnehmer-ID als Browserparameter
- Prüfungsstart nur bei aktivem Teilnehmer- und Kurszugang
- Antwortspeicherung nur für eigene offene Versuchsfragen
- Prüfungsabschluss nur für eigenen offenen Vollsimulationsversuch
- Ergebnisabruf nur für eigenen abgeschlossenen Vollsimulationsversuch
- historische Ergebnisse für `active`, `expired` und `completed`
- `blocked` bleibt ausgeschlossen

## Browsergrenze

Der Browser darf nur übermitteln:

- Kurs-ID beim Prüfungsstart
- Versuchsfragen-ID und ausgewählte Antwortindizes
- Prüfungsversuchs-ID beim Abschluss und Ergebnisabruf

Der Browser übermittelt niemals autoritativ:

- Teilnehmer-ID
- Punkte
- Maximalpunkte
- Bestehensstatus
- Richtig-/Falsch-Status
- Lösungsschlüssel
- richtige Antwortindizes
- Erklärungen

## Fragen- und Lösungsschlüssel-Snapshots

- exakt 82 sichtbare Versuchsfragen
- exakt 120 erreichbare Gesamtpunkte
- exakt 82 private Versuchsschlüssel
- spätere Änderungen der Fragenbank verändern den Versuch nicht
- private Versuchsschlüssel sind nicht direkt lesbar
- Auswahlbegrenzung wird aus dem privaten Schlüssel abgeleitet
- Überauswahl wird beim Speichern und vor der Bewertung gesperrt

## Bewertung und Abschluss

- exakt 82 Antwortzeilen nach Abschluss
- unbeantwortete Fragen werden neutral ergänzt
- Bewertung ausschließlich gegen private Versuchsschlüssel
- Teilpunkte pro ausgewählter richtiger Antwort
- keine Punkte für falsche Auswahlen
- kein Punktabzug
- Bestehensgrenze 60 von 120 Punkten
- Abschluss atomar und idempotent

## Ergebnisintegrität

Der Ergebnisabruf prüft:

- 82 Fragen-Snapshots
- 120 Snapshot-Punkte
- 82 Antwortzeilen
- 120 Antwort-Maximalpunkte
- Summe der Antwortpunkte entspricht dem Prüfungsversuch
- Bestehensstatus entspricht `score_points >= 60`
- beantwortet plus unbeantwortet ergibt 82
- richtig plus teilweise richtig plus falsch plus unbeantwortet ergibt 82
- unbeantwortete Fragen besitzen null Punkte und sind nicht richtig
- gespeicherte Maximalpunkte entsprechen den Fragensnapshots

## Funktionsrechte

Für alle vier RPC-Funktionen gilt:

- `SECURITY DEFINER`
- fester `search_path`
- `row_security = off`
- Execute-Rechte für `public` und `anon` entzogen
- ausschließlich `authenticated` erhält Execute-Recht
- keine direkten Tabellen-Schreibrechte für Teilnehmer

## Prüferabdeckung v27.28a

Der Migrationsprüfer erzwingt zusätzlich ausdrücklich den Marker:

`correct_questions + partial_questions + wrong_questions
+ unanswered_questions = 82`

Damit kann diese Ergebnisintegritätsprüfung nicht unbemerkt aus dem
RPC entfernt werden.

## Sicherheitsgrenze

- keine Live-Supabase-Ausführung
- keine echten Supabase-Schlüssel
- keine echten Teilnehmerdaten
- keine Service-Role im Browser
- keine Änderung an App-Code oder Fragenbeständen
