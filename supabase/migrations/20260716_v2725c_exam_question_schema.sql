-- Accaoui §34a Lern-App – sicheres Prüfungsfragen-Schema
-- Stand: v27.25c
-- Status: vorbereitet, nicht live ausgeführt
--
-- Direkter Browserzugriff bleibt gesperrt.
-- Lösungsschlüssel werden getrennt gespeichert.

create table if not exists exam_questions (
  id uuid primary key default gen_random_uuid(),
  source_question_id text not null,
  version integer not null default 1
    check (version > 0),
  category text not null,
  question_type text not null
    check (question_type in ('single', 'multiple')),
  question_text text not null,
  answer_options jsonb not null
    check (
      jsonb_typeof(answer_options) = 'array'
      and jsonb_array_length(answer_options) >= 2
    ),
  points smallint not null
    check (points in (1, 2)),
  core_position smallint
    check (core_position between 1 and 82),
  status text not null default 'draft'
    check (status in ('draft', 'active', 'retired')),
  content_hash text not null
    check (length(trim(content_hash)) >= 32),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (source_question_id, version)
);

create table if not exists exam_question_answer_keys (
  question_id uuid primary key
    references exam_questions(id) on delete cascade,
  correct_answers jsonb not null
    check (
      jsonb_typeof(correct_answers) = 'array'
      and jsonb_array_length(correct_answers) >= 1
    ),
  explanation text,
  answer_hash text not null
    check (length(trim(answer_hash)) >= 32),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists exam_attempt_questions (
  id uuid primary key default gen_random_uuid(),
  exam_attempt_id uuid not null
    references exam_attempts(id) on delete cascade,
  question_id uuid not null
    references exam_questions(id) on delete restrict,
  display_order smallint not null
    check (display_order > 0),
  source_question_id_snapshot text not null,
  question_version_snapshot integer not null
    check (question_version_snapshot > 0),
  category_snapshot text not null,
  question_type_snapshot text not null
    check (question_type_snapshot in ('single', 'multiple')),
  question_text_snapshot text not null,
  answer_options_snapshot jsonb not null
    check (
      jsonb_typeof(answer_options_snapshot) = 'array'
      and jsonb_array_length(answer_options_snapshot) >= 2
    ),
  max_points_snapshot smallint not null
    check (max_points_snapshot in (1, 2)),
  created_at timestamptz not null default now(),
  unique (exam_attempt_id, display_order),
  unique (exam_attempt_id, question_id)
);

create index if not exists idx_exam_questions_status
on exam_questions(status);

create index if not exists idx_exam_questions_category
on exam_questions(category);

create unique index if not exists uq_exam_questions_active_core_position
on exam_questions(core_position)
where status = 'active' and core_position is not null;

create index if not exists idx_exam_attempt_questions_attempt
on exam_attempt_questions(exam_attempt_id);

alter table exam_questions enable row level security;
alter table exam_question_answer_keys enable row level security;
alter table exam_attempt_questions enable row level security;

revoke all on table exam_questions
from public, anon, authenticated;

revoke all on table exam_question_answer_keys
from public, anon, authenticated;

revoke all on table exam_attempt_questions
from public, anon, authenticated;

-- RLS-Policies und sichere RPC-Zugriffe folgen separat.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
