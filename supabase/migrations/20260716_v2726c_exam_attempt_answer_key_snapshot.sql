-- Accaoui §34a Lern-App
-- Privater Lösungsschlüssel-Snapshot pro Prüfungsfrage
-- Stand: v27.26c
-- Status: vorbereitet, nicht live ausgeführt

create table if not exists exam_attempt_question_answer_keys (
  attempt_question_id uuid primary key
    references exam_attempt_questions(id) on delete cascade,

  correct_answers_snapshot jsonb not null
    check (
      jsonb_typeof(correct_answers_snapshot) = 'array'
      and jsonb_array_length(correct_answers_snapshot) >= 1
    ),

  explanation_snapshot text,

  grading_rule text not null default 'exact_set'
    check (grading_rule in ('exact_set')),

  answer_hash_snapshot text not null
    check (length(trim(answer_hash_snapshot)) >= 32),

  created_at timestamptz not null default now()
);

alter table exam_attempt_question_answer_keys
enable row level security;

revoke all on table exam_attempt_question_answer_keys
from public, anon, authenticated;

-- Keine direkte Policy und kein direkter Grant.
-- Lesen und Schreiben folgen später ausschließlich
-- über geprüfte Security-Definer-RPCs.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
