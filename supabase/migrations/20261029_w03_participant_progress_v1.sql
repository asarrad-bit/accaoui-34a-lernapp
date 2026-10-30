-- W03 participant progress: private/local qualification only; no live activation.
-- Prerequisites: existing MVP schema, RLS and staff-role-boundary migrations.
begin;

create schema if not exists accaoui_private;
revoke all on schema accaoui_private from public, anon, authenticated;

create or replace function public.accaoui_progress_json_safe_v1(p_value jsonb, p_depth integer)
returns boolean language plpgsql immutable
set search_path = pg_catalog, pg_temp
as $$
declare v record; n integer;
begin
  if p_value is null or p_depth > 12 then return false; end if;
  case jsonb_typeof(p_value)
  when 'object' then
    if (select count(*) from jsonb_object_keys(p_value)) > 2000 then return false; end if;
    for v in select key,value from jsonb_each(p_value) loop
      if length(v.key)>200 or v.key in ('__proto__','prototype','constructor')
         or not public.accaoui_progress_json_safe_v1(v.value,p_depth+1) then return false; end if;
    end loop;
  when 'array' then
    if jsonb_array_length(p_value)>2000 then return false; end if;
    for v in select value from jsonb_array_elements(p_value) loop
      if not public.accaoui_progress_json_safe_v1(v.value,p_depth+1) then return false; end if;
    end loop;
  when 'number' then
    if abs((p_value#>>'{}')::numeric)>9007199254740991 then return false; end if;
  when 'string' then
    if octet_length(p_value#>>'{}')>262144 then return false; end if;
  when 'boolean' then null;
  when 'null' then null;
  else return false;
  end case;
  return true;
exception when others then return false;
end $$;

create or replace function public.accaoui_progress_document_valid_v1(p_document jsonb)
returns boolean language plpgsql immutable
set search_path = pg_catalog, pg_temp
as $$
declare v record; parsed jsonb; kind text; d date;
begin
  if p_document is null or jsonb_typeof(p_document)<>'object'
     or octet_length(p_document::text)>1048576
     or (select count(*) from jsonb_object_keys(p_document))<>2
     or p_document->'schema' is distinct from '1'::jsonb
     or jsonb_typeof(p_document->'values') is distinct from 'object' then return false; end if;
  for v in select key,value from jsonb_each(p_document->'values') loop
    if v.key not in (
      'accaoui_exam_history','accaoui_topic_stats','accaoui_topic_mistakes',
      'accaoui_answered_questions','accaoui_active_session','accaoui_active_learning_session',
      'accaoui_flashcard_progress','accaoui_active_flashcard_session',
      'accaoui_oral_exam_mistakes_v2324','accaoui_exam_date_written_v1',
      'accaoui_exam_date_oral_v1','accaoui_learning_guidance_v1')
      or jsonb_typeof(v.value)<>'string' or octet_length(v.value#>>'{}')>262144
    then return false; end if;
    if v.key in ('accaoui_exam_date_written_v1','accaoui_exam_date_oral_v1') then
      if (v.value#>>'{}')!~'^[0-9]{4}-[0-9]{2}-[0-9]{2}$' then return false; end if;
      d:=(v.value#>>'{}')::date;
      if to_char(d,'YYYY-MM-DD')<>(v.value#>>'{}') then return false; end if;
    else
      parsed:=(v.value#>>'{}')::jsonb;
      kind:=case when v.key in ('accaoui_exam_history','accaoui_oral_exam_mistakes_v2324') then 'array' else 'object' end;
      if jsonb_typeof(parsed)<>kind or not public.accaoui_progress_json_safe_v1(parsed,0) then return false; end if;
    end if;
  end loop;
  return true;
exception when others then return false;
end $$;

create or replace function public.accaoui_progress_session_v1(p_owner_id uuid)
returns boolean language plpgsql volatile security definer
set search_path = pg_catalog, pg_temp
set row_security = off
as $$
declare claims jsonb; sid text;
begin
  claims:=coalesce(nullif(current_setting('request.jwt.claims',true),'')::jsonb,'{}'::jsonb);
  if p_owner_id is null or auth.uid() is distinct from p_owner_id
     or claims->>'role' is distinct from 'authenticated'
     or jsonb_typeof(claims->'exp') is distinct from 'number'
     or (claims->>'exp')::numeric <= extract(epoch from clock_timestamp())
  then return false; end if;
  sid:=claims->>'session_id';
  if sid is null or sid!~*'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' then return false; end if;
  return exists(select 1 from auth.sessions s
    where s.id=sid::uuid and s.user_id=p_owner_id
      and (s.not_after is null or s.not_after>clock_timestamp()));
exception when invalid_text_representation or numeric_value_out_of_range then return false;
end $$;

create or replace function public.accaoui_progress_access_v1(p_owner_id uuid,p_course_id uuid)
returns boolean language sql volatile security definer
set search_path = pg_catalog, pg_temp
set row_security = off
as $$
 select p_course_id is not null and public.accaoui_progress_session_v1(p_owner_id)
 and exists(
   select 1 from public.participants p
   join public.enrollments e on e.participant_id=p.id
   join public.courses c on c.id=e.course_id
   where p.auth_user_id=p_owner_id and p.status='active'
     and c.id=p_course_id and c.status='active' and e.access_status='allowed'
     and (e.access_starts_at is null or e.access_starts_at<=clock_timestamp())
     and (e.access_ends_at is null or e.access_ends_at>clock_timestamp())
     and (c.start_date is null or c.start_date<=(clock_timestamp() at time zone 'UTC')::date)
     and (c.end_date is null or c.end_date>=(clock_timestamp() at time zone 'UTC')::date)
 );
$$;

create table if not exists public.accaoui_participant_progress_v1(
 owner_id uuid not null references auth.users(id) on delete cascade,
 course_id uuid not null references public.courses(id) on delete cascade,
 version bigint not null check(version between 1 and 9007199254740991),
 document jsonb not null check(public.accaoui_progress_document_valid_v1(document)),
 saved_at timestamptz not null default clock_timestamp(),
 primary key(owner_id,course_id)
);
alter table public.accaoui_participant_progress_v1 enable row level security;
revoke all on public.accaoui_participant_progress_v1 from public,anon,authenticated;
grant select on public.accaoui_participant_progress_v1 to authenticated;
drop policy if exists accaoui_progress_owner_read_v1 on public.accaoui_participant_progress_v1;
create policy accaoui_progress_owner_read_v1 on public.accaoui_participant_progress_v1
 for select to authenticated using(owner_id=auth.uid() and public.accaoui_progress_access_v1(owner_id,course_id));

create table if not exists accaoui_private.progress_operations_v1(
 owner_id uuid not null references auth.users(id) on delete cascade,
 course_id uuid not null references public.courses(id) on delete cascade,
 operation_id uuid not null,
 expected_version bigint not null,
 committed_version bigint not null,
 document jsonb not null,
 created_at timestamptz not null default clock_timestamp(),
 primary key(owner_id,course_id,operation_id)
);
alter table accaoui_private.progress_operations_v1 enable row level security;
revoke all on accaoui_private.progress_operations_v1 from public,anon,authenticated;

create or replace function public.accaoui_progress_context_v1(p_owner_id uuid)
returns jsonb language plpgsql volatile security definer
set search_path = pg_catalog, pg_temp
set row_security = off
as $$
declare courses jsonb;
begin
 if not public.accaoui_progress_session_v1(p_owner_id) then return jsonb_build_object('status','denied'); end if;
 select coalesce(jsonb_agg(jsonb_build_object('id',c.id,'title',c.title) order by c.id),'[]'::jsonb)
 into courses from public.courses c where public.accaoui_progress_access_v1(p_owner_id,c.id);
 return jsonb_build_object('status','ready','ownerId',p_owner_id,'courses',courses);
end $$;

create or replace function public.accaoui_progress_read_v1(p_owner_id uuid,p_course_id uuid)
returns jsonb language plpgsql volatile security definer
set search_path = pg_catalog, pg_temp
set row_security = off
as $$
declare row public.accaoui_participant_progress_v1%rowtype;
begin
 if not public.accaoui_progress_access_v1(p_owner_id,p_course_id) then return jsonb_build_object('status','denied'); end if;
 select * into row from public.accaoui_participant_progress_v1
 where owner_id=p_owner_id and course_id=p_course_id;
 return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,
   'version',coalesce(row.version,0),'document',coalesce(row.document,'{"schema":1,"values":{}}'::jsonb));
end $$;

create or replace function public.accaoui_progress_write_v1(
 p_owner_id uuid,p_course_id uuid,p_expected_version bigint,p_operation_id uuid,p_document jsonb)
returns jsonb language plpgsql volatile security definer
set search_path = pg_catalog, pg_temp
set row_security = off
as $$
declare claims jsonb; current_row public.accaoui_participant_progress_v1%rowtype;
 op accaoui_private.progress_operations_v1%rowtype; actual_version bigint; next_version bigint;
begin
 if not public.accaoui_progress_access_v1(p_owner_id,p_course_id) then return jsonb_build_object('status','denied'); end if;
 if p_expected_version is null or p_expected_version<0 or p_expected_version>9007199254740991 or p_operation_id is null then return jsonb_build_object('status','invalid_request'); end if;
 if not public.accaoui_progress_document_valid_v1(p_document) then return jsonb_build_object('status','invalid_document'); end if;
 perform pg_advisory_xact_lock(hashtextextended(p_owner_id::text||':'||p_course_id::text,0));
 claims:=nullif(current_setting('request.jwt.claims',true),'')::jsonb;
 perform 1 from auth.sessions s
 join public.participants p on p.auth_user_id=s.user_id
 join public.enrollments e on e.participant_id=p.id
 join public.courses c on c.id=e.course_id
 where s.id=(claims->>'session_id')::uuid and s.user_id=p_owner_id and c.id=p_course_id
 for share of s,p,e,c;
 if not found or not public.accaoui_progress_access_v1(p_owner_id,p_course_id) then return jsonb_build_object('status','denied'); end if;
 select * into current_row from public.accaoui_participant_progress_v1
 where owner_id=p_owner_id and course_id=p_course_id for update;
 actual_version:=coalesce(current_row.version,0);
 select * into op from accaoui_private.progress_operations_v1
 where owner_id=p_owner_id and course_id=p_course_id and operation_id=p_operation_id;
 if found then
   if op.expected_version<>p_expected_version or op.document<>p_document then return jsonb_build_object('status','operation_mismatch'); end if;
   return jsonb_build_object('status','replayed','ownerId',p_owner_id,'courseId',p_course_id,'operationId',p_operation_id,
     'version',op.committed_version,'document',op.document,'currentVersion',actual_version,'currentDocument',current_row.document);
 end if;
 if actual_version<>p_expected_version then
   return jsonb_build_object('status','conflict','ownerId',p_owner_id,'courseId',p_course_id,'operationId',p_operation_id,
     'version',actual_version,'document',coalesce(current_row.document,'{"schema":1,"values":{}}'::jsonb));
 end if;
 if actual_version=9007199254740991 then return jsonb_build_object('status','version_exhausted'); end if;
 next_version:=actual_version+1;
 insert into public.accaoui_participant_progress_v1(owner_id,course_id,version,document)
 values(p_owner_id,p_course_id,next_version,p_document)
 on conflict(owner_id,course_id) do update set version=excluded.version,document=excluded.document,saved_at=clock_timestamp();
 insert into accaoui_private.progress_operations_v1(owner_id,course_id,operation_id,expected_version,committed_version,document)
 values(p_owner_id,p_course_id,p_operation_id,p_expected_version,next_version,p_document);
 return jsonb_build_object('status','committed','ownerId',p_owner_id,'courseId',p_course_id,'operationId',p_operation_id,
   'version',next_version,'document',p_document,'currentVersion',next_version,'currentDocument',p_document);
end $$;

revoke all on function public.accaoui_progress_json_safe_v1(jsonb,integer) from public,anon,authenticated;
revoke all on function public.accaoui_progress_document_valid_v1(jsonb) from public,anon,authenticated;
revoke all on function public.accaoui_progress_session_v1(uuid) from public,anon,authenticated;
revoke all on function public.accaoui_progress_access_v1(uuid,uuid) from public,anon,authenticated;
revoke all on function public.accaoui_progress_context_v1(uuid) from public,anon,authenticated;
revoke all on function public.accaoui_progress_read_v1(uuid,uuid) from public,anon,authenticated;
revoke all on function public.accaoui_progress_write_v1(uuid,uuid,bigint,uuid,jsonb) from public,anon,authenticated;
grant execute on function public.accaoui_progress_access_v1(uuid,uuid) to authenticated;
grant execute on function public.accaoui_progress_context_v1(uuid) to authenticated;
grant execute on function public.accaoui_progress_read_v1(uuid,uuid) to authenticated;
grant execute on function public.accaoui_progress_write_v1(uuid,uuid,bigint,uuid,jsonb) to authenticated;
-- Actual restricted views for the unchanged participant-access adapter.
-- Requests retain the real SDK response and selected-course filter. No base-table grants.
create or replace view public.accaoui_progress_participant_v1 with (security_barrier=true) as
 select p.id,p.auth_user_id,p.status from public.participants p
 where p.auth_user_id=auth.uid() and exists(
  select 1 from public.enrollments e where e.participant_id=p.id
   and public.accaoui_progress_access_v1(p.auth_user_id,e.course_id));
create or replace view public.accaoui_progress_enrollment_v1 with (security_barrier=true) as
 select e.id,e.participant_id,e.course_id,e.access_starts_at,e.access_ends_at,e.access_status
 from public.enrollments e join public.participants p on p.id=e.participant_id
 where p.auth_user_id=auth.uid() and public.accaoui_progress_access_v1(p.auth_user_id,e.course_id);
create or replace view public.accaoui_progress_course_v1 with (security_barrier=true) as
 select c.id,c.start_date,c.end_date,c.status from public.courses c
 where public.accaoui_progress_access_v1(auth.uid(),c.id);
revoke all on public.accaoui_progress_participant_v1,public.accaoui_progress_enrollment_v1,public.accaoui_progress_course_v1 from public,anon,authenticated;
grant select on public.accaoui_progress_participant_v1,public.accaoui_progress_enrollment_v1,public.accaoui_progress_course_v1 to authenticated;

notify pgrst,'reload schema';
commit;
