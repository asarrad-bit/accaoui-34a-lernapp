-- Accaoui §34a Lern-App – Idempotenz-Reservierungs-RPC
-- mit erwarteter Speicher-Versionsbindung
-- Stand: v27.31r
-- Status: vorbereitet, nicht live ausgeführt
--
-- Interner Sicherheitshelfer.
-- Keine direkte Freigabe für App-Rollen.
-- Führt noch keine Snapshot- oder Registermutation aus.
-- Der Abschlusshelper erhält keinen neuen Versionsparameter.

create or replace function
public.accaoui_reserve_exam_history_idempotency_operation(
  p_external_operation_id uuid,
  p_operation_scope text,
  p_operation text,
  p_resource_identity text,
  p_expected_storage_version bigint,
  p_payload_fingerprint text default null
)
returns table (
  operation_identity text,
  reservation_status text,
  operation_status text,
  result_payload jsonb,
  failure_code text,
  is_new boolean
)
language plpgsql
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
  v_operation_identity text;
  v_inserted_id uuid;
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
    p_expected_storage_version is null
    or p_expected_storage_version < 0
  then
    raise exception using
      errcode = '22023',
      message = 'expected_storage_version_invalid';
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

  v_operation_identity :=
    'exam_history_idempotency:' ||
    p_operation_scope || ':' ||
    p_operation || ':' ||
    p_external_operation_id::text;

  insert into
    public.exam_history_idempotency_operations (
      auth_user_id,
      operation_identity,
      external_operation_id,
      operation_scope,
      operation,
      resource_identity,
      expected_storage_version,
      payload_fingerprint
    )
  values (
    v_auth_user_id,
    v_operation_identity,
    p_external_operation_id,
    p_operation_scope,
    p_operation,
    p_resource_identity,
    p_expected_storage_version,
    p_payload_fingerprint
  )
  on conflict do nothing
  returning id
  into v_inserted_id;

  if v_inserted_id is not null then
    return query
    select
      v_operation_identity,
      'reserved_new'::text,
      'pending'::text,
      null::jsonb,
      null::text,
      true;

    return;
  end if;

  select io.*
  into v_existing
  from public.exam_history_idempotency_operations io
  where
    io.operation_identity =
      v_operation_identity
  for update;

  if not found then
    raise exception using
      errcode = '40001',
      message = 'idempotency_reservation_conflict_unresolved';
  end if;

  if
    v_existing.auth_user_id <>
      v_auth_user_id
  then
    raise exception using
      errcode = '23505',
      message = 'idempotency_operation_owner_conflict';
  end if;

  if
    v_existing.external_operation_id <>
      p_external_operation_id
    or v_existing.operation_scope <>
      p_operation_scope
    or v_existing.operation <>
      p_operation
    or v_existing.expected_storage_version <>
      p_expected_storage_version
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

  if
    v_existing.status not in (
      'pending',
      'completed',
      'failed'
    )
  then
    raise exception using
      errcode = '23514',
      message = 'idempotency_operation_status_invalid';
  end if;

  return query
  select
    v_existing.operation_identity,
    case v_existing.status
      when 'pending'
        then 'reserved_existing_pending'
      when 'completed'
        then 'reserved_existing_completed'
      when 'failed'
        then 'reserved_existing_failed'
    end::text,
    v_existing.status,
    v_existing.result_payload,
    v_existing.failure_code,
    false;
end;
$$;

revoke all on function
public.accaoui_reserve_exam_history_idempotency_operation(
  uuid,
  text,
  text,
  text,
  bigint,
  text
)
from public;

revoke all on function
public.accaoui_reserve_exam_history_idempotency_operation(
  uuid,
  text,
  text,
  text,
  bigint,
  text
)
from anon;

revoke all on function
public.accaoui_reserve_exam_history_idempotency_operation(
  uuid,
  text,
  text,
  text,
  bigint,
  text
)
from authenticated;

drop function if exists
public.accaoui_reserve_exam_history_idempotency_operation(
  uuid,
  text,
  text,
  text,
  text
);

-- Bewusst kein GRANT EXECUTE.
-- Spätere Nutzung ausschließlich innerhalb eines geprüften
-- Security-Definer-Mutations-RPCs und derselben Transaktion.
-- Keine Änderung am Abschlusshelper.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
