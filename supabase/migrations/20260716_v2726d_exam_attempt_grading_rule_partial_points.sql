-- Accaoui §34a Lern-App
-- Teilpunkte-Bewertungsregel für Versuchsschlüssel
-- Stand: v27.26d
-- Status: vorbereitet, nicht live ausgeführt

alter table exam_attempt_question_answer_keys
drop constraint if exists
exam_attempt_question_answer_keys_grading_rule_check;

alter table exam_attempt_question_answer_keys
alter column grading_rule
set default 'per_correct_selection_no_penalty';

update exam_attempt_question_answer_keys
set grading_rule = 'per_correct_selection_no_penalty'
where grading_rule = 'exact_set';

alter table exam_attempt_question_answer_keys
add constraint
exam_attempt_question_answer_keys_grading_rule_check
check (
  grading_rule in ('per_correct_selection_no_penalty')
);

-- Regel:
-- Jede ausgewählte richtige Antwort ergibt einen Punkt.
-- Falsche Auswahlen ergeben keinen Punkt und keinen Punktabzug.
-- Die maximale Punktzahl wird durch den Fragen-Snapshot begrenzt.
-- Keine Rechteänderung und keine Live-Ausführung.
