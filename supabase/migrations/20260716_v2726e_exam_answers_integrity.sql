-- Accaoui §34a Lern-App
-- Sichere Zuordnung und Speicherung von Prüfungsantworten
-- Stand: v27.26e
-- Status: vorbereitet, nicht live ausgeführt

-- Keine automatische Löschung vorhandener Altdaten.
-- Eine Datenbank mit alten Antwortzeilen muss vorher kontrolliert migriert werden.
do $$
begin
  if exists (select 1 from exam_answers limit 1) then
    raise exception
      'v27.26e: exam_answers enthält Altdaten; kontrollierte Migration erforderlich';
  end if;
end;
$$;

-- Ermöglicht eine versuchsgebundene zusammengesetzte Fremdschlüsselprüfung.
alter table exam_attempt_questions
drop constraint if exists exam_attempt_questions_id_attempt_unique;

alter table exam_attempt_questions
add constraint exam_attempt_questions_id_attempt_unique
unique (id, exam_attempt_id);

-- Alte freie Fragen-ID und der sichtbare Lösungsschlüssel werden entfernt.
alter table exam_answers
add column if not exists attempt_question_id uuid;

alter table exam_answers
drop column if exists correct_answers;

alter table exam column if not exists attempt_question_id uuid;

alter table exam_answers
drop column if exists correct_answers;

alter table exam_answers
drop column if exists question_id;

alter table exam_answers
alter column attempt_question_id set not null;

alter table exam_answers
alter column max_points drop default;

alter table exam_answers
drop constraint if exists exam_answers_attempt_question_unique;

alter table exam_answers
drop constraint if exists exam_answers_attempt_question_match_fk;

alter table exam_answers
drop constraint if exists exam_answers_selected_answers_array_check;

alter table exam_answers
drop constraint if exists exam_answers_max_points_range_check;

alter table exam_answers
drop constraint if exists exam_answers_earned_points_range_check;

alter table exam_answers
drop constraint if exists exam_answers_is_correct_points_check;

-- Genau eine Antwortzeile pro fester Versuchsfrage.
alter table exam_answers
add constraint exam_answers_attempt_question_unique
unique (attempt_question_id);

-- Verhindert die Zuordnung einer Frage zu einem fremden Prüfungsversuch.
alter table exam_answers
add constraint exam_answers_attempt_question_match_fk
foreign key (attempt_question_id, exam_attempt_id)
references exam_attempt_questions(id, exam_attempt_id)
on delete cascade;

alter table exam_answers
add constraint exam_answers_selected_answers_array_check
check (jsonb_typeof(selected_answers) = 'array');

alter table exam_answers
add constraint exam_answers_max_points_range_check
check (max_points in (1, 2));

alter table exam_answers
add constraint exam_answers_earned_points_range_check
check (earned_points between 0 and max_points);

-- Eine vollständig richtige Antwort muss die volle Punktzahl besitzen.
-- Die endgültige Exact-Set-Prüfung erfolgt später ausschließlich im Bewertungs-RPC.
alter table exam_answers
add constraint exam_answers_is_correct_points_check
check (not is_correct or earned_points = max_points);

create index if not exists idx_exam_answers_attempt_question_id
on exam_answers(attempt_question_id);

-- Direkte Schreibzugriffe bleiben unabhängig von RLS vollständig gesperrt.
revoke insert, update, delete
on table exam_answers
from public, anon, authenticated;

-- Teilnehmer dürfen weiterhin nur ihre eigenen fertigen Ergebnisse lesen.
-- Schreiben und Bewerten folgen später ausschließlich über Security-Definer-RPCs.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
