-- W06 first material/download slice, private synthetic development only.
-- Reuse qualified W03 identity/enrollment functions; no live switch, old policy or key change.
-- SHA-256 uses PostgreSQL17 pg_catalog.sha256(bytea), not an extension search path.
begin;

create table if not exists public.accaoui_training_staff_scope_v1(
 owner_id uuid not null references auth.users(id) on delete cascade,
 course_id uuid not null references public.courses(id) on delete cascade,
 active boolean not null default true,
 expires_at timestamptz,
 primary key(owner_id,course_id)
);
create table if not exists public.accaoui_training_materials_v1(
 id uuid primary key,
 course_id uuid not null references public.courses(id) on delete cascade,
 created_by uuid not null references auth.users(id),
 title text not null check(char_length(title) between 1 and 200),
 filename text not null,
 mime text not null check(mime in ('text/plain','application/json')),
 body text not null check(octet_length(convert_to(body,'UTF8')) between 1 and 262144),
 body_sha256 text not null check(body_sha256 ~ '^[0-9a-f]{64}$' and body_sha256=encode(sha256(convert_to(body,'UTF8')),'hex')),
 version integer not null check(version between 1 and 2147483646),
 state text not null check(state in ('draft','published','revoked')),
 expires_at timestamptz,
 updated_at timestamptz not null default clock_timestamp()
);
create table if not exists public.accaoui_training_material_receipts_v1(
 id uuid primary key default gen_random_uuid(),
 owner_id uuid not null references auth.users(id) on delete cascade,
 course_id uuid not null references public.courses(id) on delete cascade,
 material_id uuid not null references public.accaoui_training_materials_v1(id) on delete cascade,
 operation_id uuid not null,
 version integer not null check(version between 1 and 2147483646),
 body_sha256 text not null check(body_sha256 ~ '^[0-9a-f]{64}$'),
 downloaded_at timestamptz not null default clock_timestamp(),
 unique(owner_id,operation_id)
);
create table if not exists public.accaoui_training_material_operations_v1(
 owner_id uuid not null references auth.users(id) on delete cascade,
 operation_id uuid not null,
 course_id uuid not null references public.courses(id) on delete cascade,
 material_id uuid not null references public.accaoui_training_materials_v1(id) on delete cascade,
 request jsonb not null check(jsonb_typeof(request)='object'),
 response jsonb not null check(jsonb_typeof(response)='object'),
 primary key(owner_id,operation_id)
);
alter table public.accaoui_training_staff_scope_v1 enable row level security;
alter table public.accaoui_training_materials_v1 enable row level security;
alter table public.accaoui_training_material_receipts_v1 enable row level security;
alter table public.accaoui_training_material_operations_v1 enable row level security;
revoke all on public.accaoui_training_staff_scope_v1,public.accaoui_training_materials_v1,
 public.accaoui_training_material_receipts_v1,public.accaoui_training_material_operations_v1 from public,anon,authenticated;
-- Existing private fixture principal only; never shipped to the browser or product.
grant select,insert,update,delete on public.accaoui_training_staff_scope_v1,public.accaoui_training_materials_v1,
 public.accaoui_training_material_receipts_v1,public.accaoui_training_material_operations_v1 to service_role;

create or replace function public.accaoui_training_material_actor_v1(p_owner uuid,p_course uuid)
returns text language plpgsql volatile security definer
set search_path=pg_catalog,pg_temp set row_security=off
as $$
declare role_name text; claims jsonb;
begin
 if not public.accaoui_progress_session_v1(p_owner) then return null; end if;
 claims:=current_setting('request.jwt.claims',true)::jsonb;
 perform 1 from auth.sessions s where s.id=(claims->>'session_id')::uuid and s.user_id=p_owner for share;
 if not found then return null; end if;
 perform 1 from public.courses c where c.id=p_course and c.status='active'
  and (c.start_date is null or c.start_date<=(clock_timestamp() at time zone 'UTC')::date)
  and (c.end_date is null or c.end_date>=(clock_timestamp() at time zone 'UTC')::date) for share;
 if not found then return null; end if;
 select a.role into role_name from public.admin_profiles a join public.accaoui_training_staff_scope_v1 s on s.owner_id=a.auth_user_id
  where a.auth_user_id=p_owner and a.status='active' and a.role in ('admin','dozent')
   and s.course_id=p_course and s.active and (s.expires_at is null or s.expires_at>clock_timestamp()) for share of a,s;
 if found then return role_name; end if;
 perform 1 from public.participants p join public.enrollments e on e.participant_id=p.id
  where p.auth_user_id=p_owner and e.course_id=p_course for share of p,e;
 if found and public.accaoui_progress_access_v1(p_owner,p_course) then return 'participant'; end if;
 return null;
end $$;

create or replace function public.accaoui_training_material_draft_valid_v1(d jsonb)
returns boolean language plpgsql immutable
set search_path=pg_catalog,pg_temp
as $$
declare text_body text; parsed jsonb;
begin
 if d is null or jsonb_typeof(d)<>'object' or (select count(*) from jsonb_object_keys(d))<>7
  or not d ?& array['id','title','filename','mime','body','state','expiresAt']
  or jsonb_typeof(d->'id')<>'string' or (d->>'id')!~*'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
  or jsonb_typeof(d->'title')<>'string' or char_length(d->>'title') not between 1 and 200
  or btrim(d->>'title',U&'\0009\000A\000B\000C\000D\0020\00A0\1680\2000\2001\2002\2003\2004\2005\2006\2007\2008\2009\200A\2028\2029\202F\205F\3000\FEFF')<>d->>'title' or (d->>'title') ~ '[[:cntrl:]]'
  or jsonb_typeof(d->'filename')<>'string' or (d->>'filename')!~'^[A-Za-z0-9][A-Za-z0-9_-]{0,59}\.(txt|json)$'
  or jsonb_typeof(d->'mime')<>'string' or d->>'mime' not in ('text/plain','application/json')
  or (d->>'mime'='text/plain' and right(d->>'filename',4)<>'.txt')
  or (d->>'mime'='application/json' and right(d->>'filename',5)<>'.json')
  or jsonb_typeof(d->'state')<>'string' or d->>'state' not in ('draft','published')
  or jsonb_typeof(d->'body')<>'string'
  or (d->'expiresAt'<>'null'::jsonb and (jsonb_typeof(d->'expiresAt')<>'string'
   or (d->>'expiresAt')!~'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$')) then return false; end if;
 text_body:=d->>'body';
 if octet_length(convert_to(text_body,'UTF8')) not between 1 and 262144
  or translate(text_body,E'\t\r\n','') ~ '[[:cntrl:]]' then return false; end if;
 if d->'expiresAt'<>'null'::jsonb then perform (d->>'expiresAt')::timestamptz; end if;
 if d->>'mime'='application/json' then parsed:=text_body::jsonb;return public.accaoui_progress_json_safe_v1(parsed,0); end if;
 return true;
exception when invalid_text_representation or datetime_field_overflow or invalid_datetime_format then return false;
end $$;

create or replace function public.accaoui_training_material_meta_v1(m public.accaoui_training_materials_v1)
returns jsonb language sql immutable set search_path=pg_catalog,pg_temp
as $$ select jsonb_build_object('id',(m).id,'courseId',(m).course_id,'title',(m).title,'filename',(m).filename,
 'mime',(m).mime,'version',(m).version,'state',(m).state,
 'expiresAt',case when (m).expires_at is null then null else to_char((m).expires_at at time zone 'UTC','YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') end,
 'sha256',(m).body_sha256,'bytes',octet_length(convert_to((m).body,'UTF8'))); $$;
create or replace function public.accaoui_training_material_receipt_v1(r public.accaoui_training_material_receipts_v1)
returns jsonb language sql immutable set search_path=pg_catalog,pg_temp
as $$ select jsonb_build_object('id',(r).id,'ownerId',(r).owner_id,'courseId',(r).course_id,'materialId',(r).material_id,
 'version',(r).version,'sha256',(r).body_sha256,'downloadedAt',to_char((r).downloaded_at at time zone 'UTC','YYYY-MM-DD"T"HH24:MI:SS.MS"Z"')); $$;

create or replace function public.accaoui_training_material_v1(
 p_owner_id uuid,p_action text,p_course_id uuid default null,p_material_id uuid default null,
 p_expected_version integer default null,p_operation_id uuid default null,p_draft jsonb default null)
returns jsonb language plpgsql volatile security definer
set search_path=pg_catalog,pg_temp set row_security=off
as $$
declare role_name text; c record; m public.accaoui_training_materials_v1; op public.accaoui_training_material_operations_v1;
 receipt public.accaoui_training_material_receipts_v1; rows jsonb:='[]'::jsonb; response jsonb; request_value jsonb; actual integer;
begin
 if not public.accaoui_progress_session_v1(p_owner_id) then return jsonb_build_object('status','denied'); end if;
 if p_action not in ('context','list','inspect','receipts','save','revoke','download') or p_action is null then return jsonb_build_object('status','invalid_request'); end if;
 if p_action='context' then
  if p_course_id is not null or p_material_id is not null or p_expected_version is not null or p_operation_id is not null or p_draft is not null then return jsonb_build_object('status','invalid_request'); end if;
  for c in select id,title from public.courses order by id loop
   role_name:=public.accaoui_training_material_actor_v1(p_owner_id,c.id);
   if role_name is not null then rows:=rows||jsonb_build_array(jsonb_build_object('id',c.id,'title',c.title,'role',role_name)); end if;
  end loop;
  return jsonb_build_object('status','ready','ownerId',p_owner_id,'courses',rows);
 end if;
 role_name:=public.accaoui_training_material_actor_v1(p_owner_id,p_course_id);
 if role_name is null then return jsonb_build_object('status','denied'); end if;
 if p_action in ('list','receipts') then
  if p_material_id is not null or p_expected_version is not null or p_operation_id is not null or p_draft is not null then return jsonb_build_object('status','invalid_request'); end if;
  if p_action='list' then
   select coalesce(jsonb_agg(public.accaoui_training_material_meta_v1(x) order by x.id),'[]'::jsonb) into rows
    from public.accaoui_training_materials_v1 x where x.course_id=p_course_id
    and (role_name in ('admin','dozent') or (x.state='published' and (x.expires_at is null or x.expires_at>clock_timestamp())));
   return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'materials',rows);
  end if;
  select coalesce(jsonb_agg(public.accaoui_training_material_receipt_v1(x) order by x.downloaded_at,x.id),'[]'::jsonb) into rows
   from public.accaoui_training_material_receipts_v1 x where x.course_id=p_course_id and (role_name in ('admin','dozent') or x.owner_id=p_owner_id);
  return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'receipts',rows);
 end if;
 if p_material_id is null then return jsonb_build_object('status','invalid_request'); end if;
 if p_action='inspect' then
  if role_name not in ('admin','dozent') then return jsonb_build_object('status','denied'); end if;
  if p_expected_version is not null or p_operation_id is not null or p_draft is not null then return jsonb_build_object('status','invalid_request'); end if;
  select * into m from public.accaoui_training_materials_v1 where id=p_material_id and course_id=p_course_id;
  if not found then return jsonb_build_object('status','not_found'); end if;
  return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'material',public.accaoui_training_material_meta_v1(m),'body',m.body);
 end if;
 if p_operation_id is null or p_expected_version is null or p_expected_version<0 or p_expected_version>2147483645
  or (p_action<>'save' and (p_draft is not null or p_expected_version<1)) then return jsonb_build_object('status','invalid_request'); end if;
 if p_action in ('save','revoke') and role_name not in ('admin','dozent') then return jsonb_build_object('status','denied'); end if;
 if p_action='save' then
  if not public.accaoui_training_material_draft_valid_v1(p_draft) then return jsonb_build_object('status','invalid_request'); end if;
  if (p_draft->>'id')::uuid<>p_material_id
   or (p_draft->>'state'='published' and p_draft->'expiresAt'<>'null'::jsonb and (p_draft->>'expiresAt')::timestamptz<=clock_timestamp()) then return jsonb_build_object('status','invalid_request'); end if;
 end if;
 -- Both locks are transaction-local. Reusing an operation cannot overwrite its earlier payload.
 perform pg_advisory_xact_lock(hashtextextended(p_owner_id::text||':'||p_operation_id::text,0));
 perform pg_advisory_xact_lock(hashtextextended(p_course_id::text||':'||p_material_id::text,0));
 select * into m from public.accaoui_training_materials_v1 where id=p_material_id;
 if found and m.course_id<>p_course_id then return jsonb_build_object('status','denied'); end if;
 actual:=coalesce(m.version,0);
 request_value:=jsonb_build_object('action',p_action,'courseId',p_course_id,'materialId',p_material_id,'expectedVersion',p_expected_version,'draft',p_draft);
 select * into op from public.accaoui_training_material_operations_v1 where owner_id=p_owner_id and operation_id=p_operation_id;
 if found then
  if op.request<>request_value then return jsonb_build_object('status','operation_mismatch'); end if;
  if p_action='download' then
   if m.id is null then return jsonb_build_object('status','not_found'); end if;
   if m.state='revoked' then return jsonb_build_object('status','revoked'); end if;
   if m.state<>'published' then return jsonb_build_object('status','denied'); end if;
   if m.expires_at is not null and m.expires_at<=clock_timestamp() then return jsonb_build_object('status','expired'); end if;
   if actual<>p_expected_version then return jsonb_build_object('status','conflict','currentVersion',actual); end if;
  end if;
  return op.response||jsonb_build_object('replayed',true,'currentVersion',actual);
 end if;
 if p_action<>'save' and m.id is null then return jsonb_build_object('status','not_found'); end if;
 if actual<>p_expected_version then return jsonb_build_object('status','conflict','currentVersion',actual); end if;
 if m.state='revoked' then return jsonb_build_object('status','revoked'); end if;
 if p_action='save' then
  insert into public.accaoui_training_materials_v1(id,course_id,created_by,title,filename,mime,body,body_sha256,version,state,expires_at)
   values(p_material_id,p_course_id,p_owner_id,p_draft->>'title',p_draft->>'filename',p_draft->>'mime',p_draft->>'body',encode(sha256(convert_to(p_draft->>'body','UTF8')),'hex'),actual+1,p_draft->>'state',(p_draft->>'expiresAt')::timestamptz)
   on conflict(id) do update set title=excluded.title,filename=excluded.filename,mime=excluded.mime,body=excluded.body,body_sha256=excluded.body_sha256,version=excluded.version,state=excluded.state,expires_at=excluded.expires_at,updated_at=clock_timestamp()
   returning * into m;
 elsif p_action='revoke' then
  update public.accaoui_training_materials_v1 set state='revoked',version=actual+1,updated_at=clock_timestamp() where id=p_material_id returning * into m;
 else
  if m.state<>'published' then return jsonb_build_object('status','denied'); end if;
  if m.expires_at is not null and m.expires_at<=clock_timestamp() then return jsonb_build_object('status','expired'); end if;
  insert into public.accaoui_training_material_receipts_v1(owner_id,course_id,material_id,operation_id,version,body_sha256)
   values(p_owner_id,p_course_id,p_material_id,p_operation_id,m.version,m.body_sha256) returning * into receipt;
 end if;
 response:=jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'operationId',p_operation_id,'material',public.accaoui_training_material_meta_v1(m),'currentVersion',m.version,'replayed',false);
 if p_action='download' then response:=response||jsonb_build_object('body',m.body,'receipt',public.accaoui_training_material_receipt_v1(receipt)); end if;
 insert into public.accaoui_training_material_operations_v1(owner_id,operation_id,course_id,material_id,request,response)
  values(p_owner_id,p_operation_id,p_course_id,p_material_id,request_value,response);
 return response;
end $$;

revoke all on function public.accaoui_training_material_actor_v1(uuid,uuid),public.accaoui_training_material_draft_valid_v1(jsonb),
 public.accaoui_training_material_meta_v1(public.accaoui_training_materials_v1),public.accaoui_training_material_receipt_v1(public.accaoui_training_material_receipts_v1),
 public.accaoui_training_material_v1(uuid,text,uuid,uuid,integer,uuid,jsonb) from public,anon,authenticated;
grant execute on function public.accaoui_training_material_v1(uuid,text,uuid,uuid,integer,uuid,jsonb) to authenticated;
notify pgrst,'reload schema';
commit;
-- Additive W06 document/inbox revision. Execute only this suffix over the qualified material prefix.
-- Existing MVP certificates are reused; authenticated/anonymous access remains RPC-only.
begin;
create table if not exists public.accaoui_training_documents_v1(
 certificate_id uuid primary key references public.certificates(id) on delete cascade,
 owner_id uuid not null references auth.users(id) on delete cascade,
 course_id uuid not null references public.courses(id) on delete cascade,
 participant_id uuid not null references public.participants(id) on delete cascade,
 version integer not null check(version between 1 and 2147483646),
 preview jsonb not null check(jsonb_typeof(preview)='object'),
 expires_at timestamptz,
 verification_id uuid unique,
 payload jsonb,
 payload_sha256 text,
 check((payload is null and payload_sha256 is null and verification_id is null)
  or (payload is not null and jsonb_typeof(payload)='object' and verification_id is not null and payload_sha256 is not null and payload_sha256=encode(sha256(convert_to(payload::text,'UTF8')),'hex')))
);
create table if not exists public.accaoui_training_messages_v1(
 id uuid primary key,
 course_id uuid not null references public.courses(id) on delete cascade,
 created_by uuid not null references auth.users(id),
 subject text not null check(char_length(subject) between 1 and 200),
 body text not null check(char_length(body) between 1 and 12000),
 recipient_ids uuid[] not null check(cardinality(recipient_ids) between 1 and 500),
 version integer not null check(version between 1 and 2147483646),
 state text not null check(state in ('draft','published','revoked')),
 expires_at timestamptz,
 published_at timestamptz,
 author_name text,
 payload jsonb,
 payload_sha256 text,
 check((payload is null and payload_sha256 is null and published_at is null and author_name is null and state='draft')
  or (payload is not null and jsonb_typeof(payload)='object' and published_at is not null and author_name is not null and payload_sha256 is not null and state in ('published','revoked') and payload_sha256=encode(sha256(convert_to(payload::text,'UTF8')),'hex')))
);
create table if not exists public.accaoui_training_message_targets_v1(
 message_id uuid not null references public.accaoui_training_messages_v1(id) on delete cascade,
 owner_id uuid not null references auth.users(id) on delete cascade,
 course_id uuid not null references public.courses(id) on delete cascade,
 participant_id uuid not null references public.participants(id) on delete cascade,
 participant_name text not null,
 primary key(message_id,owner_id)
);
create table if not exists public.accaoui_training_message_receipts_v1(
 id uuid primary key default gen_random_uuid(),
 message_id uuid not null,
 owner_id uuid not null,
 course_id uuid not null references public.courses(id) on delete cascade,
 version integer not null check(version between 1 and 2147483646),
 payload_sha256 text not null check(payload_sha256 ~ '^[0-9a-f]{64}$'),
 read_at timestamptz not null default clock_timestamp(),
 unique(message_id,owner_id),
 foreign key(message_id,owner_id) references public.accaoui_training_message_targets_v1(message_id,owner_id) on delete cascade
);
create table if not exists public.accaoui_training_document_operations_v1(
 owner_id uuid not null references auth.users(id) on delete cascade,
 operation_id uuid not null,
 course_id uuid not null references public.courses(id) on delete cascade,
 resource_id uuid not null,
 kind text not null check(kind in ('certificate','message')),
 request jsonb not null check(jsonb_typeof(request)='object'),
 committed_version integer not null check(committed_version between 1 and 2147483646),
 primary key(owner_id,operation_id)
);
alter table public.accaoui_training_documents_v1 enable row level security;
alter table public.accaoui_training_messages_v1 enable row level security;
alter table public.accaoui_training_message_targets_v1 enable row level security;
alter table public.accaoui_training_message_receipts_v1 enable row level security;
alter table public.accaoui_training_document_operations_v1 enable row level security;
revoke all on public.certificates,public.accaoui_training_documents_v1,public.accaoui_training_messages_v1,
 public.accaoui_training_message_targets_v1,public.accaoui_training_message_receipts_v1,public.accaoui_training_document_operations_v1 from public,anon,authenticated;
grant select,insert,update,delete on public.certificates,public.accaoui_training_documents_v1,public.accaoui_training_messages_v1,
 public.accaoui_training_message_targets_v1,public.accaoui_training_message_receipts_v1,public.accaoui_training_document_operations_v1 to service_role;

create or replace function public.accaoui_training_iso_v1(t timestamptz)
returns text language sql immutable set search_path=pg_catalog,pg_temp
as $$ select case when t is null then null else to_char(t at time zone 'UTC','YYYY-MM-DD"T"HH24:MI:SS.MS"Z"') end; $$;

create or replace function public.accaoui_training_text_v1(v text,n integer,p_empty boolean,p_multiline boolean)
returns boolean language plpgsql immutable set search_path=pg_catalog,pg_temp
as $$
begin
 if v is null or n<1 or char_length(v)>n then return false; end if;
 if not p_empty and char_length(btrim(v,U&'\0009\000A\000B\000C\000D\0020\00A0\1680\2000\2001\2002\2003\2004\2005\2006\2007\2008\2009\200A\2028\2029\202F\205F\3000\FEFF'))=0 then return false; end if;
 return case when p_multiline then translate(v,E'\t\r\n','') !~ '[[:cntrl:]]' else v !~ '[[:cntrl:]]' end;
end $$;

create or replace function public.accaoui_training_recipient_v1(p_participant uuid,p_course uuid)
returns jsonb language plpgsql volatile security definer set search_path=pg_catalog,pg_temp set row_security=off
as $$
declare r record; full_name text;
begin
 select p.id,p.auth_user_id,p.first_name,p.last_name,c.title into r
 from public.participants p join public.enrollments e on e.participant_id=p.id join public.courses c on c.id=e.course_id
 join auth.users u on u.id=p.auth_user_id
 where p.id=p_participant and p.status='active' and e.course_id=p_course and e.access_status='allowed'
  and (e.access_starts_at is null or e.access_starts_at<=clock_timestamp()) and (e.access_ends_at is null or e.access_ends_at>clock_timestamp())
  and c.status='active' and (c.start_date is null or c.start_date<=(clock_timestamp() at time zone 'UTC')::date)
  and (c.end_date is null or c.end_date>=(clock_timestamp() at time zone 'UTC')::date) for share of p,e,c;
 if not found then return null; end if;
 full_name:=btrim(r.first_name||' '||r.last_name);
 if not public.accaoui_training_text_v1(full_name,300,false,false) or not public.accaoui_training_text_v1(r.title,200,false,false) then return null; end if;
 return jsonb_build_object('participantId',r.id,'ownerId',r.auth_user_id,'name',full_name,'courseTitle',r.title);
end $$;

create or replace function public.accaoui_training_document_meta_v1(d public.accaoui_training_documents_v1,c public.certificates)
returns jsonb language plpgsql volatile security definer set search_path=pg_catalog,pg_temp set row_security=off
as $$
declare stamp timestamptz:=clock_timestamp(); eligible boolean; valid boolean; reason text;
begin
 eligible:=public.accaoui_training_recipient_v1(d.participant_id,d.course_id) is not null;
 valid:=c.status='issued' and eligible and d.payload is not null and (d.expires_at is null or d.expires_at>stamp);
 reason:=case when c.status='issued' and not eligible then 'ineligible' when c.status='issued' and not valid then 'expired' else c.status end;
 return jsonb_build_object('id',d.certificate_id,'courseId',d.course_id,'ownerId',d.owner_id,'participantId',d.participant_id,
  'state',c.status,'version',d.version,'expiresAt',public.accaoui_training_iso_v1(d.expires_at),'verificationId',d.verification_id,
  'preview',d.preview,'canonical',case when d.payload is null then null else d.payload::text end,'sha256',d.payload_sha256,
  'valid',valid,'eligible',eligible,'reason',reason,'checkedAt',public.accaoui_training_iso_v1(stamp));
end $$;

create or replace function public.accaoui_training_message_receipt_meta_v1(r public.accaoui_training_message_receipts_v1)
returns jsonb language sql immutable set search_path=pg_catalog,pg_temp
as $$ select jsonb_build_object('id',(r).id,'ownerId',(r).owner_id,'courseId',(r).course_id,'messageId',(r).message_id,
 'version',(r).version,'sha256',(r).payload_sha256,'readAt',public.accaoui_training_iso_v1((r).read_at),'deliveryKind','local_read_confirmation'); $$;

create or replace function public.accaoui_training_message_meta_v1(m public.accaoui_training_messages_v1,p_actor uuid,p_staff boolean)
returns jsonb language plpgsql volatile security definer set search_path=pg_catalog,pg_temp set row_security=off
as $$
declare own_receipt jsonb; all_receipts jsonb;
begin
 select public.accaoui_training_message_receipt_meta_v1(r) into own_receipt from public.accaoui_training_message_receipts_v1 r where r.message_id=m.id and r.owner_id=p_actor;
 if p_staff then select coalesce(jsonb_agg(public.accaoui_training_message_receipt_meta_v1(r) order by r.read_at,r.id),'[]'::jsonb) into all_receipts from public.accaoui_training_message_receipts_v1 r where r.message_id=m.id; end if;
 return jsonb_build_object('id',m.id,'courseId',m.course_id,'state',m.state,'version',m.version,'subject',m.subject,'body',m.body,
  'expiresAt',public.accaoui_training_iso_v1(m.expires_at),'publishedAt',public.accaoui_training_iso_v1(m.published_at),'authorName',m.author_name,
  'canonical',case when m.payload is null then null else m.payload::text end,'sha256',m.payload_sha256,
  'recipientIds',case when p_staff then to_jsonb(m.recipient_ids) else null end,'receipts',all_receipts,'ownReceipt',own_receipt,'checkedAt',public.accaoui_training_iso_v1(clock_timestamp()));
end $$;

create or replace function public.accaoui_training_document_v1(
 p_owner_id uuid,p_course_id uuid,p_action text,p_resource_id uuid default null,p_expected_version integer default null,
 p_operation_id uuid default null,p_payload jsonb default null,p_verification_id uuid default null)
returns jsonb language plpgsql volatile security definer set search_path=pg_catalog,pg_temp set row_security=off
as $$
declare role_name text; staff boolean; is_certificate boolean; write_action boolean;
 d public.accaoui_training_documents_v1; c public.certificates; m public.accaoui_training_messages_v1;
 op public.accaoui_training_document_operations_v1; receipt public.accaoui_training_message_receipts_v1;
 r record; info jsonb; rows jsonb:='[]'::jsonb; resource jsonb; request_value jsonb; v_preview jsonb; snapshot jsonb;
 actual integer:=0; committed integer; target uuid; target_ids uuid[]; issuer text; stamp timestamptz; expires timestamptz; replayed boolean:=false;
begin
 role_name:=public.accaoui_training_material_actor_v1(p_owner_id,p_course_id);
 if role_name is null then return jsonb_build_object('status','denied'); end if;
 staff:=role_name in ('admin','dozent');
 if p_action is null or p_action not in ('recipients','certificates','get_certificate','verify_certificate','prepare_certificate','issue_certificate','revoke_certificate','messages','get_message','save_message','publish_message','revoke_message','read_message') then return jsonb_build_object('status','invalid_request'); end if;
 write_action:=p_action in ('prepare_certificate','issue_certificate','revoke_certificate','save_message','publish_message','revoke_message','read_message');
 if not write_action then
  if p_expected_version is not null or p_operation_id is not null or p_payload is not null then return jsonb_build_object('status','invalid_request'); end if;
  if p_action='verify_certificate' then
   if p_verification_id is null or p_resource_id is not null then return jsonb_build_object('status','invalid_request'); end if;
  elsif p_verification_id is not null then return jsonb_build_object('status','invalid_request'); end if;
  if p_action in ('recipients','certificates','messages') and p_resource_id is not null then return jsonb_build_object('status','invalid_request'); end if;
  if p_action in ('get_certificate','get_message') and p_resource_id is null then return jsonb_build_object('status','invalid_request'); end if;
  if p_action='recipients' then
   if not staff then return jsonb_build_object('status','denied'); end if;
   for r in select participant_id from public.enrollments where course_id=p_course_id order by participant_id loop
    info:=public.accaoui_training_recipient_v1(r.participant_id,p_course_id);
    if info is not null then rows:=rows||jsonb_build_array(info-'courseTitle'); end if;
   end loop;
   return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'recipients',rows,'checkedAt',public.accaoui_training_iso_v1(clock_timestamp()));
  elsif p_action='certificates' then
   for d in select * from public.accaoui_training_documents_v1 where course_id=p_course_id and (staff or (owner_id=p_owner_id and payload is not null)) order by certificate_id loop
    select * into c from public.certificates where id=d.certificate_id and participant_id=d.participant_id and course_id=d.course_id and certificate_type='participation_confirmation';
    if found then rows:=rows||jsonb_build_array(public.accaoui_training_document_meta_v1(d,c)); end if;
    if jsonb_array_length(rows)>1000 then return jsonb_build_object('status','limit_exceeded'); end if;
   end loop;
   return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'certificates',rows);
  elsif p_action in ('get_certificate','verify_certificate') then
   select * into d from public.accaoui_training_documents_v1 where course_id=p_course_id
    and ((p_action='get_certificate' and certificate_id=p_resource_id) or (p_action='verify_certificate' and verification_id=p_verification_id));
   if not found then return jsonb_build_object('status','not_found'); end if;
   if not staff and (d.owner_id<>p_owner_id or d.payload is null) then return jsonb_build_object('status','denied'); end if;
   select * into c from public.certificates where id=d.certificate_id and participant_id=d.participant_id and course_id=d.course_id and certificate_type='participation_confirmation';
   if not found then return jsonb_build_object('status','denied'); end if;
   return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'certificate',public.accaoui_training_document_meta_v1(d,c));
  elsif p_action='messages' then
   for m in select * from public.accaoui_training_messages_v1 x where x.course_id=p_course_id and (staff or (x.state='published' and (x.expires_at is null or x.expires_at>clock_timestamp()) and exists(select 1 from public.accaoui_training_message_targets_v1 t where t.message_id=x.id and t.owner_id=p_owner_id))) order by id loop
    rows:=rows||jsonb_build_array(public.accaoui_training_message_meta_v1(m,p_owner_id,staff));
    if jsonb_array_length(rows)>1000 then return jsonb_build_object('status','limit_exceeded'); end if;
   end loop;
   return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'messages',rows);
  else
   select * into m from public.accaoui_training_messages_v1 where id=p_resource_id and course_id=p_course_id;
   if not found then return jsonb_build_object('status','not_found'); end if;
   if not staff then
    if not exists(select 1 from public.accaoui_training_message_targets_v1 where message_id=m.id and owner_id=p_owner_id) then return jsonb_build_object('status','denied'); end if;
    if m.state='revoked' then return jsonb_build_object('status','revoked'); end if;
    if m.state<>'published' then return jsonb_build_object('status','denied'); end if;
    if m.expires_at is not null and m.expires_at<=clock_timestamp() then return jsonb_build_object('status','expired'); end if;
   end if;
   return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'message',public.accaoui_training_message_meta_v1(m,p_owner_id,staff));
  end if;
 end if;
 if p_resource_id is null or p_operation_id is null or p_verification_id is not null or p_expected_version is null or p_expected_version<0 or p_expected_version>2147483645 then return jsonb_build_object('status','invalid_request'); end if;
 if p_action not in ('prepare_certificate','save_message') and (p_expected_version<1 or p_payload is not null) then return jsonb_build_object('status','invalid_request'); end if;
 if p_action in ('issue_certificate','revoke_certificate') and role_name<>'admin' then return jsonb_build_object('status','denied'); end if;
 if p_action in ('prepare_certificate','save_message','publish_message','revoke_message') and not staff then return jsonb_build_object('status','denied'); end if;
 if p_action='prepare_certificate' then
  if p_payload is null or jsonb_typeof(p_payload)<>'object' then return jsonb_build_object('status','invalid_request'); end if;
  if (select count(*) from jsonb_object_keys(p_payload))<>4 or not p_payload ?& array['kind','participantId','note','expiresAt']
   or p_payload->>'kind' is distinct from 'synthetic_training' or jsonb_typeof(p_payload->'participantId')<>'string'
   or (p_payload->>'participantId')!~*'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
   or jsonb_typeof(p_payload->'note')<>'string' or not public.accaoui_training_text_v1(p_payload->>'note',1000,true,true) then return jsonb_build_object('status','invalid_request'); end if;
 elsif p_action='save_message' then
  if p_payload is null or jsonb_typeof(p_payload)<>'object' then return jsonb_build_object('status','invalid_request'); end if;
  if (select count(*) from jsonb_object_keys(p_payload))<>4 or not p_payload ?& array['subject','body','recipientIds','expiresAt']
   or jsonb_typeof(p_payload->'subject')<>'string' or not public.accaoui_training_text_v1(p_payload->>'subject',200,false,false)
   or jsonb_typeof(p_payload->'body')<>'string' or not public.accaoui_training_text_v1(p_payload->>'body',12000,false,true)
   or jsonb_typeof(p_payload->'recipientIds')<>'array' then return jsonb_build_object('status','invalid_request'); end if;
  if jsonb_array_length(p_payload->'recipientIds') not between 1 and 500 then return jsonb_build_object('status','invalid_request'); end if;
  target_ids:='{}'::uuid[];
  for info in select value from jsonb_array_elements(p_payload->'recipientIds') loop
   if jsonb_typeof(info)<>'string' or (info#>>'{}')!~*'^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$' then return jsonb_build_object('status','invalid_request'); end if;
   target:=(info#>>'{}')::uuid;if target=any(target_ids) then return jsonb_build_object('status','invalid_request'); end if;target_ids:=array_append(target_ids,target);
  end loop;
 end if;
 if p_action in ('prepare_certificate','save_message') then
  if p_payload->'expiresAt'='null'::jsonb then expires:=null;
  else
   if jsonb_typeof(p_payload->'expiresAt')<>'string' or (p_payload->>'expiresAt')!~'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z$' then return jsonb_build_object('status','invalid_request'); end if;
   begin expires:=(p_payload->>'expiresAt')::timestamptz;exception when invalid_text_representation or datetime_field_overflow or invalid_datetime_format then return jsonb_build_object('status','invalid_request');end;
   if public.accaoui_training_iso_v1(expires) is distinct from p_payload->>'expiresAt' then return jsonb_build_object('status','invalid_request'); end if;
  end if;
 end if;
 is_certificate:=p_action in ('prepare_certificate','issue_certificate','revoke_certificate');
 perform pg_advisory_xact_lock(hashtextextended('w06-doc-op:'||p_owner_id::text||':'||p_operation_id::text,0));
 perform pg_advisory_xact_lock(hashtextextended('w06-doc-resource:'||p_resource_id::text,0));
 if is_certificate then
  select * into d from public.accaoui_training_documents_v1 where certificate_id=p_resource_id for update;
  if found and d.course_id<>p_course_id then return jsonb_build_object('status','denied'); end if;
  if d.certificate_id is not null then
   select * into c from public.certificates where id=d.certificate_id and participant_id=d.participant_id and course_id=d.course_id and certificate_type='participation_confirmation' for update;
   if not found then return jsonb_build_object('status','denied'); end if;
  elsif exists(select 1 from public.certificates where id=p_resource_id) then return jsonb_build_object('status','denied'); end if;
  actual:=coalesce(d.version,0);
 else
  select * into m from public.accaoui_training_messages_v1 where id=p_resource_id for update;
  if found and m.course_id<>p_course_id then return jsonb_build_object('status','denied'); end if;
  actual:=coalesce(m.version,0);
  if p_action='read_message' then
   if m.id is null then return jsonb_build_object('status','not_found'); end if;
   if not exists(select 1 from public.accaoui_training_message_targets_v1 where message_id=m.id and owner_id=p_owner_id) then return jsonb_build_object('status','denied'); end if;
   if m.state='revoked' then return jsonb_build_object('status','revoked'); end if;
   if m.state<>'published' then return jsonb_build_object('status','denied'); end if;
   if m.expires_at is not null and m.expires_at<=clock_timestamp() then return jsonb_build_object('status','expired'); end if;
  end if;
 end if;
 request_value:=jsonb_build_object('action',p_action,'courseId',p_course_id,'resourceId',p_resource_id,'expectedVersion',p_expected_version,'payload',p_payload);
 select * into op from public.accaoui_training_document_operations_v1 where owner_id=p_owner_id and operation_id=p_operation_id;
 if found then
  if op.request<>request_value then return jsonb_build_object('status','operation_mismatch'); end if;
  committed:=op.committed_version;replayed:=true;
 else
  if p_action in ('prepare_certificate','save_message') and expires is not null and expires<=clock_timestamp() then return jsonb_build_object('status','invalid_request'); end if;
  if actual<>p_expected_version then return jsonb_build_object('status','conflict','currentVersion',actual); end if;
  if actual=0 and p_action not in ('prepare_certificate','save_message') then return jsonb_build_object('status','not_found'); end if;
  if is_certificate then
   if p_action='prepare_certificate' then
    if actual>0 and c.status<>'prepared' then return jsonb_build_object('status','immutable'); end if;
    info:=public.accaoui_training_recipient_v1((p_payload->>'participantId')::uuid,p_course_id);
    if info is null then return jsonb_build_object('status','invalid_recipient'); end if;
    if actual>0 and d.participant_id<>(p_payload->>'participantId')::uuid then return jsonb_build_object('status','denied'); end if;
    select display_name into issuer from public.admin_profiles where auth_user_id=p_owner_id and status='active' and role in ('admin','dozent');
    if not public.accaoui_training_text_v1(issuer,200,false,false) then return jsonb_build_object('status','invalid_request'); end if;
    v_preview:=jsonb_build_object('courseTitle',info->>'courseTitle','participantName',info->>'name','issuerName',issuer,'note',p_payload->>'note');
    if actual=0 then insert into public.certificates(id,participant_id,course_id,certificate_type,status) values(p_resource_id,(p_payload->>'participantId')::uuid,p_course_id,'participation_confirmation','prepared') returning * into c;end if;
    insert into public.accaoui_training_documents_v1(certificate_id,owner_id,course_id,participant_id,version,preview,expires_at)
     values(p_resource_id,(info->>'ownerId')::uuid,p_course_id,(p_payload->>'participantId')::uuid,actual+1,v_preview,expires)
     on conflict(certificate_id) do update set version=excluded.version,preview=excluded.preview,expires_at=excluded.expires_at returning * into d;
   elsif p_action='issue_certificate' then
    if c.status<>'prepared' then return jsonb_build_object('status','immutable'); end if;
    info:=public.accaoui_training_recipient_v1(d.participant_id,p_course_id);if info is null then return jsonb_build_object('status','invalid_recipient'); end if;
    stamp:=clock_timestamp();if d.expires_at is not null and d.expires_at<=stamp then return jsonb_build_object('status','expired'); end if;
    select display_name into issuer from public.admin_profiles where auth_user_id=p_owner_id and status='active' and role='admin';
    if not public.accaoui_training_text_v1(issuer,200,false,false) then return jsonb_build_object('status','invalid_request'); end if;
    v_preview:=jsonb_build_object('courseTitle',info->>'courseTitle','participantName',info->>'name','issuerName',issuer,'note',d.preview->>'note');
    snapshot:=v_preview||jsonb_build_object('schema',1,'kind','synthetic_local_training_confirmation','documentId',d.certificate_id,'courseId',d.course_id,'ownerId',d.owner_id,'participantId',d.participant_id,'issuedAt',public.accaoui_training_iso_v1(stamp),'issuedVersion',actual+1,'expiresAt',public.accaoui_training_iso_v1(d.expires_at));
    update public.certificates set status='issued',issued_at=stamp,updated_at=stamp where id=c.id returning * into c;
    update public.accaoui_training_documents_v1 set version=actual+1,preview=v_preview,payload=snapshot,payload_sha256=encode(sha256(convert_to(snapshot::text,'UTF8')),'hex'),verification_id=gen_random_uuid() where certificate_id=d.certificate_id returning * into d;
   else
    if c.status='revoked' then return jsonb_build_object('status','revoked'); end if;
    update public.certificates set status='revoked',revoked_at=clock_timestamp(),updated_at=clock_timestamp() where id=c.id returning * into c;
    update public.accaoui_training_documents_v1 set version=actual+1 where certificate_id=d.certificate_id returning * into d;
   end if;
  else
   if p_action='save_message' then
    if actual>0 and m.state<>'draft' then return jsonb_build_object('status','immutable'); end if;
    foreach target in array target_ids loop if public.accaoui_training_recipient_v1(target,p_course_id) is null then return jsonb_build_object('status','invalid_recipient');end if;end loop;
    insert into public.accaoui_training_messages_v1(id,course_id,created_by,subject,body,recipient_ids,version,state,expires_at)
     values(p_resource_id,p_course_id,p_owner_id,p_payload->>'subject',p_payload->>'body',target_ids,actual+1,'draft',expires)
     on conflict(id) do update set subject=excluded.subject,body=excluded.body,recipient_ids=excluded.recipient_ids,version=excluded.version,expires_at=excluded.expires_at returning * into m;
   elsif p_action='publish_message' then
    if m.state<>'draft' then return jsonb_build_object('status','immutable'); end if;
    stamp:=clock_timestamp();if m.expires_at is not null and m.expires_at<=stamp then return jsonb_build_object('status','expired'); end if;
    rows:='[]'::jsonb;
    foreach target in array m.recipient_ids loop info:=public.accaoui_training_recipient_v1(target,p_course_id);if info is null then return jsonb_build_object('status','invalid_recipient');end if;rows:=rows||jsonb_build_array(info);end loop;
    select display_name into issuer from public.admin_profiles where auth_user_id=p_owner_id and status='active' and role in ('admin','dozent');
    if not public.accaoui_training_text_v1(issuer,200,false,false) then return jsonb_build_object('status','invalid_request'); end if;
    snapshot:=jsonb_build_object('schema',1,'kind','local_synthetic_message','messageId',m.id,'courseId',m.course_id,'subject',m.subject,'body',m.body,'expiresAt',public.accaoui_training_iso_v1(m.expires_at),'publishedAt',public.accaoui_training_iso_v1(stamp),'publishedVersion',actual+1,'authorName',issuer);
    update public.accaoui_training_messages_v1 set version=actual+1,state='published',published_at=stamp,author_name=issuer,payload=snapshot,payload_sha256=encode(sha256(convert_to(snapshot::text,'UTF8')),'hex') where id=m.id returning * into m;
    for info in select value from jsonb_array_elements(rows) loop insert into public.accaoui_training_message_targets_v1(message_id,owner_id,course_id,participant_id,participant_name) values(m.id,(info->>'ownerId')::uuid,p_course_id,(info->>'participantId')::uuid,info->>'name');end loop;
   elsif p_action='revoke_message' then
    if m.state<>'published' then return jsonb_build_object('status','immutable'); end if;
    update public.accaoui_training_messages_v1 set version=actual+1,state='revoked' where id=m.id returning * into m;
   else
    insert into public.accaoui_training_message_receipts_v1(message_id,owner_id,course_id,version,payload_sha256)
     values(m.id,p_owner_id,p_course_id,m.version,m.payload_sha256) on conflict(message_id,owner_id) do nothing;
   end if;
  end if;
  committed:=case when p_action='read_message' then actual else actual+1 end;
  insert into public.accaoui_training_document_operations_v1(owner_id,operation_id,course_id,resource_id,kind,request,committed_version)
   values(p_owner_id,p_operation_id,p_course_id,p_resource_id,case when is_certificate then 'certificate' else 'message' end,request_value,committed);
 end if;
 if is_certificate then resource:=public.accaoui_training_document_meta_v1(d,c);actual:=d.version;
 else resource:=public.accaoui_training_message_meta_v1(m,p_owner_id,staff);actual:=m.version;end if;
 return jsonb_build_object('status','ready','ownerId',p_owner_id,'courseId',p_course_id,'operationId',p_operation_id,'committedVersion',committed,'currentVersion',actual,'resource',resource,'replayed',replayed);
end $$;

revoke all on function public.accaoui_training_iso_v1(timestamptz),public.accaoui_training_text_v1(text,integer,boolean,boolean),public.accaoui_training_recipient_v1(uuid,uuid),
 public.accaoui_training_document_meta_v1(public.accaoui_training_documents_v1,public.certificates),
 public.accaoui_training_message_receipt_meta_v1(public.accaoui_training_message_receipts_v1),
 public.accaoui_training_message_meta_v1(public.accaoui_training_messages_v1,uuid,boolean),
 public.accaoui_training_document_v1(uuid,uuid,text,uuid,integer,uuid,jsonb,uuid) from public,anon,authenticated;
grant execute on function public.accaoui_training_document_v1(uuid,uuid,text,uuid,integer,uuid,jsonb,uuid) to authenticated;
notify pgrst,'reload schema';
commit;
