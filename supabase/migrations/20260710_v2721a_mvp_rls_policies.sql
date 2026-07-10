-- Accaoui §34a Lern-App – Supabase MVP RLS Policies
-- Stand: v27.21a
-- Status: vorbereitet, nicht live ausgeführt
-- Sicherheit: keine Keys, keine Teilnehmerdaten, keine Service-Role-Nutzung

create or replace function public.accaoui_is_admin_or_dozent()
returns boolean
language sql
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.admin_profiles ap
    where ap.auth_user_id = auth.uid()
      and ap.status = 'active'
      and ap.role in ('admin', 'dozent', 'support')
  );
$$;

create or replace function public.accaoui_is_admin()
returns boolean
language sql
security definer
set search_path = public
as $$
  select exists (
    select 1
    from public.admin_profiles ap
    where ap.auth_user_id = auth.uid()
      and ap.status = 'active'
      and ap.role = 'admin'
  );
$$;

drop policy if exists "participants_select_own_or_staff" on participants;
create policy "participants_select_own_or_staff"
on participants
for select
to authenticated
using (
  auth_user_id = auth.uid()
  or public.accaoui_is_admin_or_dozent()
);

drop policy if exists "participants_staff_manage" on participants;
create policy "participants_staff_manage"
on participants
for all
to authenticated
using (public.accaoui_is_admin_or_dozent())
with check (public.accaoui_is_admin_or_dozent());

drop policy if exists "courses_select_authenticated" on courses;
create policy "courses_select_authenticated"
on courses
for select
to authenticated
using (
  status = 'active'
  or public.accaoui_is_admin_or_dozent()
);

drop policy if exists "courses_staff_manage" on courses;
create policy "courses_staff_manage"
on courses
for all
to authenticated
using (public.accaoui_is_admin_or_dozent())
with check (public.accaoui_is_admin_or_dozent());

drop policy if exists "enrollments_select_own_or_staff" on enrollments;
create policy "enrollments_select_own_or_staff"
on enrollments
for select
to authenticated
using (
  exists (
    select 1
    from participants p
    where p.id = enrollments.participant_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_admin_or_dozent()
);

drop policy if exists "enrollments_staff_manage" on enrollments;
create policy "enrollments_staff_manage"
on enrollments
for all
to authenticated
using (public.accaoui_is_admin_or_dozent())
with check (public.accaoui_is_admin_or_dozent());

drop policy if exists "exam_attempts_select_own_or_staff" on exam_attempts;
create policy "exam_attempts_select_own_or_staff"
on exam_attempts
for select
to authenticated
using (
  exists (
    select 1
    from participants p
    where p.id = exam_attempts.participant_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_admin_or_dozent()
);

drop policy if exists "exam_attempts_insert_own" on exam_attempts;
create policy "exam_attempts_insert_own"
on exam_attempts
for insert
to authenticated
with check (
  exists (
    select 1
    from participants p
    where p.id = exam_attempts.participant_id
      and p.auth_user_id = auth.uid()
  )
);

drop policy if exists "exam_attempts_staff_manage" on exam_attempts;
create policy "exam_attempts_staff_manage"
on exam_attempts
for all
to authenticated
using (public.accaoui_is_admin_or_dozent())
with check (public.accaoui_is_admin_or_dozent());

drop policy if exists "exam_answers_select_own_or_staff" on exam_answers;
create policy "exam_answers_select_own_or_staff"
on exam_answers
for select
to authenticated
using (
  exists (
    select 1
    from exam_attempts ea
    join participants p on p.id = ea.participant_id
    where ea.id = exam_answers.exam_attempt_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_admin_or_dozent()
);

drop policy if exists "exam_answers_insert_own" on exam_answers;
create policy "exam_answers_insert_own"
on exam_answers
for insert
to authenticated
with check (
  exists (
    select 1
    from exam_attempts ea
    join participants p on p.id = ea.participant_id
    where ea.id = exam_answers.exam_attempt_id
      and p.auth_user_id = auth.uid()
  )
);

drop policy if exists "exam_answers_staff_manage" on exam_answers;
create policy "exam_answers_staff_manage"
on exam_answers
for all
to authenticated
using (public.accaoui_is_admin_or_dozent())
with check (public.accaoui_is_admin_or_dozent());

drop policy if exists "certificates_select_own_or_staff" on certificates;
create policy "certificates_select_own_or_staff"
on certificates
for select
to authenticated
using (
  exists (
    select 1
    from participants p
    where p.id = certificates.participant_id
      and p.auth_user_id = auth.uid()
  )
  or public.accaoui_is_admin_or_dozent()
);

drop policy if exists "certificates_staff_manage" on certificates;
create policy "certificates_staff_manage"
on certificates
for all
to authenticated
using (public.accaoui_is_admin_or_dozent())
with check (public.accaoui_is_admin_or_dozent());

drop policy if exists "admin_profiles_select_own_or_admin" on admin_profiles;
create policy "admin_profiles_select_own_or_admin"
on admin_profiles
for select
to authenticated
using (
  auth_user_id = auth.uid()
  or public.accaoui_is_admin()
);

drop policy if exists "admin_profiles_admin_manage" on admin_profiles;
create policy "admin_profiles_admin_manage"
on admin_profiles
for all
to authenticated
using (public.accaoui_is_admin())
with check (public.accaoui_is_admin());

drop policy if exists "audit_logs_staff_select" on audit_logs;
create policy "audit_logs_staff_select"
on audit_logs
for select
to authenticated
using (public.accaoui_is_admin_or_dozent());

-- Direkte Teilnehmer-Updates bleiben im MVP absichtlich gesperrt.
-- Profiländerungen kommen später über geprüfte RPC-/Admin-Wege.
