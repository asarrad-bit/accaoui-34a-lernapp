-- Accaoui §34a Lern-App
-- Mitarbeiterrollen sauber trennen
-- Stand: v27.28e
-- Status: vorbereitet, nicht live ausgeführt

create or replace function public.accaoui_is_active_staff()
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
  select exists (
    select 1
    from public.admin_profiles ap
    where ap.auth_user_id = auth.uid()
      and ap.status = 'active'
      and ap.role in ('admin', 'dozent', 'support')
  );
$$;

revoke all
on function public.accaoui_is_active_staff()
from public;

revoke all
on function public.accaoui_is_active_staff()
from anon;

revoke all
on function public.accaoui_is_active_staff()
from authenticated;

grant execute
on function public.accaoui_is_active_staff()
to authenticated;

create or replace function public.accaoui_is_admin_or_dozent()
returns boolean
language sql
stable
security definer
set search_path = pg_catalog, public
set row_security = off
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
on function public.accaoui_is_admin_or_dozent()
from public;

revoke all
on function public.accaoui_is_admin_or_dozent()
from anon;

revoke all
on function public.accaoui_is_admin_or_dozent()
from authenticated;

grant execute
on function public.accaoui_is_admin_or_dozent()
to authenticated;

drop policy if exists
  "participants_select_own_or_staff"
on public.participants;

create policy "participants_select_own_or_staff"
on public.participants
for select
to authenticated
using (
  auth_user_id = auth.uid()
  or public.accaoui_is_active_staff()
);

drop policy if exists
  "courses_select_authenticated"
on public.courses;

create policy "courses_select_authenticated"
on public.courses
for select
to authenticated
using (
  status = 'active'
  or public.accaoui_is_active_staff()
);

drop policy if exists
  "enrollments_select_own_or_staff"
on public.enrollments;

create policy "enrollments_select_own_or_staff"
on public.enrollments
for select
to authenticated
using (
  exists (
    select 1
    from public.participants p
    where p.id = enrollments.participant_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_active_staff()
);

drop policy if exists
  "exam_attempts_select_own_or_staff"
on public.exam_attempts;

create policy "exam_attempts_select_own_or_staff"
on public.exam_attempts
for select
to authenticated
using (
  exists (
    select 1
    from public.participants p
    where p.id = exam_attempts.participant_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_active_staff()
);

drop policy if exists
  "exam_answers_select_own_or_staff"
on public.exam_answers;

create policy "exam_answers_select_own_or_staff"
on public.exam_answers
for select
to authenticated
using (
  exists (
    select 1
    from public.exam_attempts ea
    join public.participants p
      on p.id = ea.participant_id
    where ea.id = exam_answers.exam_attempt_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_active_staff()
);

drop policy if exists
  "certificates_select_own_or_staff"
on public.certificates;

create policy "certificates_select_own_or_staff"
on public.certificates
for select
to authenticated
using (
  exists (
    select 1
    from public.participants p
    where p.id = certificates.participant_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_active_staff()
);

-- Bestehende Verwaltungs-Policies verwenden weiterhin
-- accaoui_is_admin_or_dozent(), jetzt ohne Support.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
