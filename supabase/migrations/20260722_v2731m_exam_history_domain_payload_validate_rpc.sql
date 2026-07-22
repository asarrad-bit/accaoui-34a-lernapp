-- Accaoui §34a Lern-App – Fach-Payload-Validierungshelfer
-- Stand: v27.31m
-- Status: vorbereitet, nicht live ausgeführt
--
-- Validiert und kanonisiert ausschließlich Fach-Payloads.
-- Keine Fach-, Idempotenz- oder sonstige Tabellenmutation.
-- Keine direkte Ausführungsfreigabe für App-Rollen.

create or replace function
public.accaoui_validate_exam_history_domain_payload(
  p_operation_scope text,
  p_operation text,
  p_domain_payload jsonb default null
)
returns table (
  canonical_payload jsonb,
  payload_fingerprint text,
  canonical_byte_length integer
)
language plpgsql
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_canonical_text text;
  v_canonical_bytes integer;
  v_payload_fingerprint text;
  v_max_depth integer;
  v_forbidden_key text;
begin
  if
    p_operation_scope is null
    or p_operation_scope not in (
      'snapshot',
      'cycle_registry'
    )
  then
    raise exception using
      errcode = '22023',
      message = 'domain_payload_scope_invalid';
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
      message = 'domain_payload_operation_invalid';
  end if;

  if p_operation = 'delete' then
    if p_domain_payload is not null then
      raise exception using
        errcode = '22023',
        message = 'domain_payload_delete_must_be_null';
    end if;

    return query
    select
      null::jsonb,
      null::text,
      0::integer;

    return;
  end if;

  if p_operation_scope = 'snapshot' then
    if p_domain_payload is null then
      raise exception using
        errcode = '22023',
        message = 'snapshot_payload_required';
    end if;

    if jsonb_typeof(p_domain_payload) <> 'object' then
      raise exception using
        errcode = '22023',
        message = 'snapshot_payload_must_be_object';
    end if;

    if
      jsonb_object_length(p_domain_payload) <> 2
      or not (p_domain_payload ? 'schema_version')
      or not (p_domain_payload ? 'snapshot')
    then
      raise exception using
        errcode = '22023',
        message = 'snapshot_payload_fields_invalid';
    end if;

    if
      jsonb_typeof(
        p_domain_payload -> 'schema_version'
      ) <> 'number'
      or p_domain_payload ->> 'schema_version' <> '1'
    then
      raise exception using
        errcode = '22023',
        message = 'snapshot_schema_version_invalid';
    end if;

    if
      jsonb_typeof(
        p_domain_payload -> 'snapshot'
      ) <> 'object'
      or p_domain_payload -> 'snapshot' = '{}'::jsonb
    then
      raise exception using
        errcode = '22023',
        message = 'snapshot_content_invalid';
    end if;
  else
    if p_domain_payload is null then
      raise exception using
        errcode = '22023',
        message = 'cycle_registry_payload_required';
    end if;

    if jsonb_typeof(p_domain_payload) <> 'object' then
      raise exception using
        errcode = '22023',
        message = 'cycle_registry_payload_must_be_object';
    end if;

    if
      jsonb_object_length(p_domain_payload) <> 2
      or not (p_domain_payload ? 'schema_version')
      or not (p_domain_payload ? 'registry')
    then
      raise exception using
        errcode = '22023',
        message = 'cycle_registry_payload_fields_invalid';
    end if;

    if
      jsonb_typeof(
        p_domain_payload -> 'schema_version'
      ) <> 'number'
      or p_domain_payload ->> 'schema_version' <> '1'
    then
      raise exception using
        errcode = '22023',
        message = 'cycle_registry_schema_version_invalid';
    end if;

    if
      jsonb_typeof(
        p_domain_payload -> 'registry'
      ) <> 'object'
    then
      raise exception using
        errcode = '22023',
        message = 'cycle_registry_content_invalid';
    end if;
  end if;

  with recursive payload_nodes(value, depth) as (
    select
      p_domain_payload,
      1

    union all

    select
      child.value,
      payload_nodes.depth + 1
    from payload_nodes
    cross join lateral (
      select object_item.value
      from jsonb_each(
        case
          when jsonb_typeof(payload_nodes.value) = 'object'
            then payload_nodes.value
          else '{}'::jsonb
        end
      ) as object_item(key, value)

      union all

      select array_item.value
      from jsonb_array_elements(
        case
          when jsonb_typeof(payload_nodes.value) = 'array'
            then payload_nodes.value
          else '[]'::jsonb
        end
      ) as array_item(value)
    ) as child
  )
  select max(depth)
  into v_max_depth
  from payload_nodes;

  if v_max_depth > 16 then
    if p_operation_scope = 'snapshot' then
      raise exception using
        errcode = '22023',
        message = 'snapshot_payload_depth_exceeded';
    else
      raise exception using
        errcode = '22023',
        message = 'cycle_registry_payload_depth_exceeded';
    end if;
  end if;

  with recursive payload_nodes(value) as (
    select p_domain_payload

    union all

    select child.value
    from payload_nodes
    cross join lateral (
      select object_item.value
      from jsonb_each(
        case
          when jsonb_typeof(payload_nodes.value) = 'object'
            then payload_nodes.value
          else '{}'::jsonb
        end
      ) as object_item(key, value)

      union all

      select array_item.value
      from jsonb_array_elements(
        case
          when jsonb_typeof(payload_nodes.value) = 'array'
            then payload_nodes.value
          else '[]'::jsonb
        end
      ) as array_item(value)
    ) as child
  )
  select object_key.key
  into v_forbidden_key
  from payload_nodes
  cross join lateral jsonb_object_keys(
    case
      when jsonb_typeof(payload_nodes.value) = 'object'
        then payload_nodes.value
      else '{}'::jsonb
    end
  ) as object_key(key)
  where object_key.key = any(
    array[
      'external_operation_id',
      'operation_identity',
      'payload_fingerprint',
      'client_request_key_hash',
      'request_fingerprint',
      'service_role',
      'raw_database_error'
    ]::text[]
  )
  limit 1;

  if v_forbidden_key is not null then
    if p_operation_scope = 'snapshot' then
      raise exception using
        errcode = '22023',
        message = 'snapshot_payload_forbidden_key';
    else
      raise exception using
        errcode = '22023',
        message = 'cycle_registry_payload_forbidden_key';
    end if;
  end if;

  v_canonical_text := p_domain_payload::text;

  if v_canonical_text is null then
    raise exception using
      errcode = '22023',
      message = 'domain_payload_canonicalization_failed';
  end if;

  v_canonical_bytes :=
    octet_length(
      convert_to(
        v_canonical_text,
        'UTF8'
      )
    );

  if
    p_operation_scope = 'snapshot'
    and v_canonical_bytes > 262144
  then
    raise exception using
      errcode = '22023',
      message = 'snapshot_payload_too_large';
  end if;

  if
    p_operation_scope = 'cycle_registry'
    and v_canonical_bytes > 131072
  then
    raise exception using
      errcode = '22023',
      message = 'cycle_registry_payload_too_large';
  end if;

  v_payload_fingerprint :=
    encode(
      public.digest(
        convert_to(
          v_canonical_text,
          'UTF8'
        ),
        'sha256'
      ),
      'hex'
    );

  if
    v_payload_fingerprint is null
    or v_payload_fingerprint !~ '^[0-9a-f]{64}$'
  then
    raise exception using
      errcode = '22023',
      message = 'domain_payload_canonicalization_failed';
  end if;

  return query
  select
    p_domain_payload,
    v_payload_fingerprint,
    v_canonical_bytes;
end;
$$;

revoke all on function
public.accaoui_validate_exam_history_domain_payload(
  text,
  text,
  jsonb
)
from public;

revoke all on function
public.accaoui_validate_exam_history_domain_payload(
  text,
  text,
  jsonb
)
from anon;

revoke all on function
public.accaoui_validate_exam_history_domain_payload(
  text,
  text,
  jsonb
)
from authenticated;

-- Bewusst kein GRANT EXECUTE.
-- Keine Tabellenmutation.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
