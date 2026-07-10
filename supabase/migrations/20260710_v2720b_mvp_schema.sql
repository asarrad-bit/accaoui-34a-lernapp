-- Accaoui §34a Lern-App – Supabase MVP Schema
-- Stand: v27.20b
-- Status: vorbereitet, nicht live ausgeführt
-- Sicherheit: keine Keys, keine Teilnehmerdaten, keine Service-Role-Nutzung

create extension if not exists pgcrypto;

create table if not exists participants (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid unique,
  first_name text not null,
  last_name text not null,
  email text unique not null,
  phone text,
  status text not null default 'active'
    check (status in ('active', 'blocked', 'expired', 'completed')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists courses (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  course_type text not null
    check (course_type in ('sachkunde_34a', 'grosser_schein', 'intensiv_10_tage', 'drei_monate', 'sechs_monate')),
  start_date date,
  end_date date,
  status text not null default 'active'
    check (status in ('active', 'inactive', 'archived')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists enrollments (
  id uuid primary key default gen_random_uuid(),
  participant_id uuid not null references participants(id) on delete cascade,
  course_id uuid not null references courses(id) on delete cascade,
  access_starts_at timestamptz,
  access_ends_at timestamptz,
  access_status text not null default 'allowed'
    check (access_status in ('allowed', 'blocked', 'expired', 'completed')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (participant_id, course_id)
);

create table if not exists exam_attempts (
  id uuid primary key default gen_random_uuid(),
  participant_id uuid not null references participants(id) on delete cascade,
  course_id uuid references courses(id) on delete set null,
  mode text not null
    check (mode in ('full_simulation', 'training', 'category_test', 'repeat_mistakes')),
  score_points integer not null default 0 check (score_points >= 0),
  max_points integer not null default 0 check (max_points >= 0),
  passed boolean not null default false,
  started_at timestamptz,
  finished_at timestamptz,
  created_at timestamptz not null default now()
);

create table if not exists exam_answers (
  id uuid primary key default gen_random_uuid(),
  exam_attempt_id uuid not null references exam_attempts(id) on delete cascade,
  question_id text not null,
  selected_answers jsonb not null default '[]'::jsonb,
  correct_answers jsonb not null default '[]'::jsonb,
  earned_points integer not null default 0 check (earned_points >= 0),
  max_points integer not null default 0 check (max_points >= 0),
  is_correct boolean not null default false,
  created_at timestamptz not null default now()
);

create table if not exists certificates (
  id uuid primary key default gen_random_uuid(),
  participant_id uuid not null references participants(id) on delete cascade,
  course_id uuid references courses(id) on delete set null,
  certificate_type text not null default 'participation_confirmation',
  status text not null default 'prepared'
    check (status in ('prepared', 'issued', 'blocked', 'revoked')),
  issued_at timestamptz,
  revoked_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists admin_profiles (
  id uuid primary key default gen_random_uuid(),
  auth_user_id uuid unique not null,
  display_name text not null,
  role text not null
    check (role in ('admin', 'dozent', 'support')),
  status text not null default 'active'
    check (status in ('active', 'blocked')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists audit_logs (
  id uuid primary key default gen_random_uuid(),
  actor_user_id uuid,
  action text not null,
  target_table text,
  target_id uuid,
  metadata jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_participants_auth_user_id on participants(auth_user_id);
create index if not exists idx_enrollments_participant_id on enrollments(participant_id);
create index if not exists idx_exam_attempts_participant_id on exam_attempts(participant_id);
create index if not exists idx_exam_answers_attempt_id on exam_answers(exam_attempt_id);
create index if not exists idx_certificates_participant_id on certificates(participant_id);
create index if not exists idx_admin_profiles_auth_user_id on admin_profiles(auth_user_id);
create index if not exists idx_audit_logs_actor_user_id on audit_logs(actor_user_id);

alter table participants enable row level security;
alter table courses enable row level security;
alter table enrollments enable row level security;
alter table exam_attempts enable row level security;
alter table exam_answers enable row level security;
alter table certificates enable row level security;
alter table admin_profiles enable row level security;
alter table audit_logs enable row level security;

-- RLS-Policies folgen separat in v27.20c/v27.21.
-- Diese Migration legt nur das sichere MVP-Grundschema an.
