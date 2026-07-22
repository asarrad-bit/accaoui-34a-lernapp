-- Accaoui §34a Lern-App – Idempotenz-Abschluss-RPC
-- Stand: v27.31d
-- Status: vorbereitet, nicht live ausgeführt
--
-- Interner Sicherheitshelfer.
-- Keine direkte Ausführungsfreigabe für App-Rollen.
-- Führt keine Snapshot- oder Registermutation aus.

create or replace function
public.accaoui_complete_exam_history_idempotency_operation(
  p_external_operation_id uuid,
  p_operation_scope text,
  p_operation text,
  p_resource_identity text,
  p_payload_fingerprint text,
  p_terminal_status text,
  p_result_payload jsonb,
  p_failure_code text
)
returns table (
  operation_identity text,
  completion_status text,
  operation_status text,
  result_payload jsonb,
  failure_code text,
  completed_at timestamptz,
  was_updated boolean
)
language plpgsql
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
  v_operation_identity text;
  v_operation_id uuid;
  v_completed_at timestamptz;
  v_existing
    public.exam_history_idempotency_operations%rowtype;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception using
      errcode = '28000',
      message = 'authentication_required';
  end if;

  if
    p_external_operation_id is null
    or p_external_operation_id::text !~
      '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
  then
    raise exception using
      errcode = '22023',
      message = 'external_operation_id_invalid';
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
      message = 'operation_scope_invalid';
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
      message = 'operation_invalid';
  end if;

  if
    p_resource_identity is null
    or p_resource_identity <> trim(p_resource_identity)
    or length(p_resource_identity) not between 1 and 512
  then
    raise exception using
      errcode = '22023',
      message = 'resource_identity_invalid';
  end if;

  if
    p_operation = 'write'
    and (
      p_payload_fingerprint is null
      or p_payload_fingerprint !~ '^[0-9a-f]{64}$'
    )
  then
    raise exception using
      errcode = '22023',
      message = 'payload_fingerprint_invalid';
  end if;

  if
    p_operation = 'delete'
    and p_payload_fingerprint is not null
  then
    raise exception using
      errcode = '22023',
      message = 'delete_payload_fingerprint_not_allowed';
  end if;

  if
    p_terminal_status is null
    or p_terminal_status not in (
      'completed',
      'failed'
    )
  then
    raise exception using
      errcode = '22023',
      message = 'terminal_status_invalid';
  end if;

  if
    p_terminal_status = 'completed'
    and (
      p_result_payload is null
      or jsonb_typeof(p_result_payload) <> 'object'
      or octet_length(p_result_payload::text) > 32768
      or p_failure_code is not null
    )
  then
    raise exception using
      errcode = '22023',
      message = 'completion_result_invalid';
  end if;

  if
    p_terminal_status = 'failed'
    and (
      p_result_payload is not null
      or p_failure_code is null
      or p_failure_code <> trim(p_failure_code)
      or p_failure_code !~ '^[a-z0-9_]{1,128}$'
    )
  then
    raise exception using
      errcode = '22023',
      message = 'completion_failure_invalid';
  end if;

  v_operation_identity :=
    'exam_history_idempotency:' ||
    p_operation_scope || ':' ||
    p_operation || ':' ||
    p_external_operation_id::text;

  select io.*
  into v_existing
  from public.exam_history_idempotency_operations io
  where
    io.operation_identity =
      v_operation_identity
  for update;

  if not found then
    raise exception using
      errcode = 'P0002',
      message = 'idempotency_operation_not_reserved';
  end if;

  if
    v_existing.auth_user_id <>
      v_auth_user_id
  then
    raise exception using
      errcode = '42501',
      message = 'idempotency_operation_owner_conflict';
  end if;

  if
    v_existing.external_operation_id <>
      p_external_operation_id
    or v_existing.operation_scope <>
      p_operation_scope
    or v_existing.operation <>
      p_operation
  then
    raise exception using
      errcode = '23505',
      message = 'idempotency_operation_identity_conflict';
  end if;

  if
    v_existing.resource_identity <>
      p_resource_identity
  then
    raise exception using
      errcode = '23505',
      message = 'idempotency_operation_resource_conflict';
  end if;

  if
    v_existing.payload_fingerprint
      is distinct from
    p_payload_fingerprint
  then
    raise exception using
      errcode = '23505',
      message = 'idempotency_operation_payload_conflict';
  end if;

  if v_existing.status = 'pending' then
    v_operation_id :=
      v_existing.id;

    v_completed_at :=
      greatest(
        clock_timestamp(),
        v_existing.created_at
      );

    update public.exam_history_idempotency_operations
    set
      status = p_terminal_status,
      result_payload =
        case
          when p_terminal_status = 'completed'
            then p_result_payload
          else null
        end,
      failure_code =
        case
          when p_terminal_status = 'failed'
            then p_failure_code
          else null
        end,
      updated_at = v_completed_at,
      completed_at = v_completed_at
    where
      id = v_operation_id
      and status = 'pending';

    if not found then
      raise exception using
        errcode = '40001',
        message = 'idempotency_completion_concurrent_conflict';
    end if;

    select io.*
    into v_existing
    from public.exam_history_idempotency_operations io
    where io.id = v_operation_id;

    return query
    select
      v_existing.operation_identity,
      case v_existing.status
        when 'completed'
          then 'completed_new'
        when 'failed'
          then 'failed_new'
      end::text,
      v_existing.status,
      v_existing.result_payload,
      v_existing.failure_code,
      v_existing.completed_at,
      true;

    return;
  end if;

  if
    v_existing.status = 'completed'
    and p_terminal_status = 'completed'
    and v_existing.result_payload =
      p_result_payload
    and p_failure_code is null
  then
    return query
    select
      v_existing.operation_identity,
      'already_completed'::text,
      v_existing.status,
      v_existing.result_payload,
      null::text,
      v_existing.completed_at,
      false;

    return;
  end if;

  if
    v_existing.status = 'failed'
    and p_terminal_status = 'failed'
    and v_existing.result_payload is null
    and v_existing.failure_code =
      p_failure_code
  then
    return query
    select
      v_existing.operation_identity,
      'already_failed'::text,
      v_existing.status,
      null::jsonb,
      v_existing.failure_code,
      v_existing.completed_at,
      false;

    return;
  end if;

  if
    v_existing.status in (
      'completed',
      'failed'
    )
  then
    raise exception using
      errcode = '23505',
      message = 'idempotency_operation_terminal_conflict';
  end if;

  raise exception using
    errcode = '23514',
    message = 'idempotency_operation_status_invalid';
end;
$$;

revoke all on function
public.accaoui_complete_exam_history_idempotency_operation(
  uuid,
  text,
  text,
  text,
  text,
  text,
  jsonb,
  text
)
from public;

revoke all on function
public.accaoui_complete_exam_history_idempotency_operation(
  uuid,
  text,
  text,
  text,
  text,
  text,
  jsonb,
  text
)
from anon;

revoke all on function
public.accaoui_complete_exam_history_idempotency_operation(
  uuid,
  text,
  text,
  text,
  text,
  text,
  jsonb,
  text
)
from authenticated;

-- Bewusst keine direkte Ausführungsfreigabe.
-- Spätere Nutzung nur innerhalb desselben geprüften
-- Security-Definer-Mutations-RPCs und derselben Transaktion.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
