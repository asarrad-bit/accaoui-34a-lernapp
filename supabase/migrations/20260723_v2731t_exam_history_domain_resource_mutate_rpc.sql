-- Accaoui §34a Lern-App – Domain-Speicher-Mutationshelper
-- Stand: v27.31t
-- Status: vorbereitet, nicht live ausgeführt
--
-- Interner vollständig gesperrter Security-Definer-Helper.
-- Keine direkte App-Ausführung und kein äußerer Mutations-RPC.
-- Nutzerbindung ausschließlich über auth.uid().

create or replace function
public.accaoui_mutate_exam_history_domain_resource(
  p_operation_scope text,
  p_operation text,
  p_resource_identity text,
  p_expected_storage_version bigint,
  p_domain_payload jsonb default null
)
returns table (
  outcome text,
  storage_version bigint,
  is_deleted boolean,
  domain_payload jsonb,
  payload_fingerprint text,
  canonical_byte_length integer,
  created_at timestamptz,
  updated_at timestamptz
)
language plpgsql
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
  v_canonical_payload jsonb;
  v_payload_fingerprint text;
  v_canonical_byte_length integer;
  v_existing public.exam_history_domain_resources%rowtype;
  v_inserted public.exam_history_domain_resources%rowtype;
  v_updated public.exam_history_domain_resources%rowtype;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception using
      errcode = '28000',
      message = 'authentication_required';
  end if;

  if
    p_operation_scope is null
    or p_operation_scope not in (
      'snapshot',
      'cycle_registry'
    )
  then
    raise exception using
      errcode = '22023',
      message = 'domain_storage_scope_invalid';
  end if;

  if
    p_operation is null
    or p_operation not in (
      'write',
      'delete'
    )
  then
    raise exception using
      errcode = '22023',
      message = 'domain_storage_payload_invalid';
  end if;

  if
    p_resource_identity is null
    or p_resource_identity <> trim(p_resource_identity)
    or length(p_resource_identity) not between 1 and 512
  then
    raise exception using
      errcode = '22023',
      message = 'domain_storage_resource_identity_invalid';
  end if;

  if
    p_expected_storage_version is null
    or p_expected_storage_version < 0
  then
    raise exception using
      errcode = '22023',
      message = 'domain_storage_expected_version_invalid';
  end if;

  begin
    select
      validation.canonical_payload,
      validation.payload_fingerprint,
      validation.canonical_byte_length
    into
      v_canonical_payload,
      v_payload_fingerprint,
      v_canonical_byte_length
    from public.accaoui_validate_exam_history_domain_payload(
      p_operation_scope,
      p_operation,
      p_domain_payload
    ) as validation;
  exception
    when sqlstate '22023' then
      raise exception using
        errcode = '22023',
        message = 'domain_storage_payload_invalid';
  end;

  loop
    select resource.*
    into v_existing
    from public.exam_history_domain_resources resource
    where
      resource.auth_user_id = v_auth_user_id
      and resource.operation_scope = p_operation_scope
      and resource.resource_identity = p_resource_identity
    for update;

    if found then
      exit;
    end if;

    if p_operation = 'delete' then
      if p_expected_storage_version = 0 then
        return query
        select
          'already_absent'::text,
          0::bigint,
          true,
          null::jsonb,
          null::text,
          null::integer,
          null::timestamptz,
          null::timestamptz;

        return;
      end if;

      raise exception using
        errcode = '40001',
        message = 'domain_storage_version_conflict';
    end if;

    if p_expected_storage_version <> 0 then
      raise exception using
        errcode = '40001',
        message = 'domain_storage_version_conflict';
    end if;

    begin
      insert into public.exam_history_domain_resources (
        auth_user_id,
        operation_scope,
        resource_identity,
        schema_version,
        domain_payload,
        payload_fingerprint,
        canonical_byte_length,
        storage_version,
        is_deleted
      )
      values (
        v_auth_user_id,
        p_operation_scope,
        p_resource_identity,
        1,
        v_canonical_payload,
        v_payload_fingerprint,
        v_canonical_byte_length,
        1,
        false
      )
      returning *
      into v_inserted;

      return query
      select
        'created'::text,
        v_inserted.storage_version,
        v_inserted.is_deleted,
        v_inserted.domain_payload,
        v_inserted.payload_fingerprint,
        v_inserted.canonical_byte_length,
        v_inserted.created_at,
        v_inserted.updated_at;

      return;
    exception
      when unique_violation then
        null;
    end;
  end loop;

  if
    v_existing.schema_version <> 1
    or v_existing.storage_version < 1
    or (
      v_existing.is_deleted = false
      and (
        v_existing.domain_payload is null
        or v_existing.payload_fingerprint is null
        or v_existing.canonical_byte_length is null
      )
    )
    or (
      v_existing.is_deleted = true
      and (
        v_existing.domain_payload is not null
        or v_existing.payload_fingerprint is not null
        or v_existing.canonical_byte_length is not null
      )
    )
  then
    raise exception using
      errcode = '23514',
      message = 'domain_storage_state_invalid';
  end if;

  if
    v_existing.storage_version <>
      p_expected_storage_version
  then
    raise exception using
      errcode = '40001',
      message = 'domain_storage_version_conflict';
  end if;

  if p_operation = 'delete' then
    if v_existing.is_deleted then
      return query
      select
        'already_deleted'::text,
        v_existing.storage_version,
        true,
        null::jsonb,
        null::text,
        null::integer,
        v_existing.created_at,
        v_existing.updated_at;

      return;
    end if;

    update public.exam_history_domain_resources
    set
      domain_payload = null,
      payload_fingerprint = null,
      canonical_byte_length = null,
      storage_version = storage_version + 1,
      is_deleted = true,
      updated_at = now()
    where id = v_existing.id
    returning *
    into v_updated;

    return query
    select
      'deleted'::text,
      v_updated.storage_version,
      v_updated.is_deleted,
      v_updated.domain_payload,
      v_updated.payload_fingerprint,
      v_updated.canonical_byte_length,
      v_updated.created_at,
      v_updated.updated_at;

    return;
  end if;

  if
    v_existing.is_deleted = false
    and v_existing.payload_fingerprint =
      v_payload_fingerprint
  then
    return query
    select
      'updated'::text,
      v_existing.storage_version,
      v_existing.is_deleted,
      v_existing.domain_payload,
      v_existing.payload_fingerprint,
      v_existing.canonical_byte_length,
      v_existing.created_at,
      v_existing.updated_at;

    return;
  end if;

  update public.exam_history_domain_resources
  set
    schema_version = 1,
    domain_payload = v_canonical_payload,
    payload_fingerprint = v_payload_fingerprint,
    canonical_byte_length = v_canonical_byte_length,
    storage_version = storage_version + 1,
    is_deleted = false,
    updated_at = now()
  where id = v_existing.id
  returning *
  into v_updated;

  return query
  select
    'updated'::text,
    v_updated.storage_version,
    v_updated.is_deleted,
    v_updated.domain_payload,
    v_updated.payload_fingerprint,
    v_updated.canonical_byte_length,
    v_updated.created_at,
    v_updated.updated_at;
end;
$$;

revoke all on function
public.accaoui_mutate_exam_history_domain_resource(
  text,
  text,
  text,
  bigint,
  jsonb
)
from public;

revoke all on function
public.accaoui_mutate_exam_history_domain_resource(
  text,
  text,
  text,
  bigint,
  jsonb
)
from anon;

revoke all on function
public.accaoui_mutate_exam_history_domain_resource(
  text,
  text,
  text,
  bigint,
  jsonb
)
from authenticated;

-- Bewusst kein GRANT EXECUTE.
-- Bewusst kein äußerer Fachmutations-RPC.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
