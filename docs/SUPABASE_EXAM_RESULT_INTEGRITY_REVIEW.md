# Accaoui §34a Lern-App – Sicherheitsreview Prüfungsintegrität

Stand: v27.24a

Status: Sicherheitsreview abgeschlossen, keine Live-Ausführung

## Geprüfte Dateien

- `supabase/migrations/20260710_v2720b_mvp_schema.sql`
- `supabase/migrations/20260710_v2721a_mvp_rls_policies.sql`

## Kritischer Befund 1 – Prüfungsergebnis manipulierbar

Die Tabelle `exam_attempts` enthält unter anderem:

- `score_points`
- `max_points`
- `passed`
- `course_id`
- `started_at`
- `finished_at`

Die aktuelle Teilnehmer-Insert-Policy prüft nur, ob die verwendete
`participant_id` zum angemeldeten Benutzer gehört.

Sie verhindert nicht, dass der Browser selbst einen beliebigen Punktestand,
eine beliebige Maximalpunktzahl oder einen beliebigen Bestehensstatus sendet.

Risikostufe: kritisch

## Kritischer Befund 2 – Antwortbewertung manipulierbar

Die Tabelle `exam_answers` enthält unter anderem:

- `selected_answers`
- `correct_answers`
- `earned_points`
- `max_points`
- `is_correct`

Die aktuelle Teilnehmer-Insert-Policy prüft nur, ob der Prüfungsversuch
zum angemeldeten Teilnehmer gehört.

Damit könnte ein Browser derzeit selbst richtige Antworten, erreichte Punkte
und den Richtig-/Falsch-Status eintragen.

Risikostufe: kritisch

## Hoher Befund 3 – Lösungsschlüssel sichtbar

Teilnehmer dürfen eigene Datensätze aus `exam_answers` lesen.

Da `correct_answers` in derselben Tabelle gespeichert wird und keine
Spaltenbegrenzung vorhanden ist, wäre auch der Lösungsschlüssel lesbar.

Während einer laufenden Prüfung darf der Lösungsschlüssel nicht ausgeliefert
werden.

Risikostufe: hoch

## Hoher Befund 4 – Kurszuordnung nicht geprüft

Ein Teilnehmer kann beim Prüfungsversuch derzeit eine `course_id` angeben.

Die Insert-Policy prüft nicht:

- ob eine Einschreibung besteht
- ob der Kurs aktiv ist
- ob der Zugriff erlaubt oder noch gültig ist

Risikostufe: hoch

## Weitere Integritätslücken

Noch nicht abgesichert:

- `score_points <= max_points`
- `earned_points <= max_points`
- `finished_at >= started_at`
- nur eine Antwort pro Frage und Prüfungsversuch
- JSON-Werte müssen tatsächlich Arrays sein
- Schutz vor mehrfacher oder wiederholter Ergebnisübermittlung

## Verbindliche Sicherheitsentscheidung

Vor jeder Live-Anbindung gilt:

1. Teilnehmer dürfen keine autoritativen Ergebnisse direkt eintragen.
2. `score_points`, `passed`, `earned_points`, `is_correct` und
   `correct_answers` werden niemals aus dem Browser übernommen.
3. Die Bewertung erfolgt über einen vertrauenswürdigen Server-/RPC-Weg.
4. Eine Prüfung wird nur für einen gültig eingeschriebenen Teilnehmer angelegt.
5. Lösungsschlüssel werden während einer laufenden Prüfung nicht ausgeliefert.
6. Direkte Teilnehmer-Insert-Policies werden vor dem Live-Test gesperrt.
7. Erst danach wird ein kontrollierter Speicher- und Bewertungsweg aufgebaut.

## Nächster Umsetzungsschritt

`v27.24b`

- direkte Teilnehmer-Inserts für `exam_attempts` und `exam_answers` entfernen
- RLS-Migration und Migrationsprüftool anpassen
- späteren geprüften RPC-Weg vorbereiten

## Bewertung

Die aktuelle Migration ist noch nicht für die Speicherung echter
Prüfungsergebnisse freigegeben.

Die festgestellten Risiken betreffen nur die vorbereitete, noch nicht live
ausgeführte Supabase-Struktur. Der lokale App-Betrieb bleibt unverändert.

Status: Review abgeschlossen – Live-Freigabe gesperrt
