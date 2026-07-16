-- Accaoui §34a Lern-App – Prüfungsfragen RLS
-- Stand: v27.25d
-- Status: vorbereitet, nicht live ausgeführt

create or replace function public.accaoui_is_exam_content_manager()
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, public
as $$
  select exists (
    select 1
    from public.admin_profiles ap
    where ap.auth_user_id = auth.uid()
      and ap.status = 'active'
      and ap.role in ('admin', 'dozent')
  );
$$;

revoke all
on function public.accaoui_is_exam_content_manager()
from public;

grant execute
on function public.accaoui_is_exam_content_manager()
to authenticated;

drop policy if exists
  "exam_questions_content_manager_manage"
on public.exam_questions;

create policy "exam_questions_content_manager_manage"
on public.exam_questions
for all
to authenticated
using (public.accaoui_is_exam_content_manager())
with check (public.accaoui_is_exam_content_manager());

drop policy if exists
  "exam_question_answer_keys_content_manager_manage"
on public.exam_question_answer_keys;

create policy "exam_question_answer_keys_content_manager_manage"
on public.exam_question_answer_keys
for all
to authenticated
using (public.accaoui_is_exam_content_manager())
with check (public.accaoui_is_exam_content_manager());

drop policy if exists
  "exam_attempt_questions_select_own_or_content_manager"
on public.exam_attempt_questions;

create policy "exam_attempt_questions_select_own_or_content_manager"
on public.exam_attempt_questions
for select
to authenticated
using (
  exists (
    select 1
    from public.exam_attempts ea
    join public.participants p
      on p.id = ea.participant_id
    where ea.id = exam_attempt_questions.exam_attempt_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_exam_content_manager()
);

grant select, insert, update, delete
on table public.exam_questions
to authenticated;

grant select, insert, update, delete
on table public.exam_question_answer_keys
to authenticated;

grant select
on table public.exam_attempt_questions
to authenticated;

-- Teilnehmer erhalten keine Insert-, Update- oder Delete-Rechte
-- auf Prüfungs-Snapshots.
-- Snapshot-Schreibzugriffe folgen später ausschließlich über sichere RPCs.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
