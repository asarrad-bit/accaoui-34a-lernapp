-- Accaoui §34a Lern-App – äußerer Fachmutations-RPC
-- Stand: v27.31u
-- Status: vorbereitet, nicht live ausgeführt
--
-- Verbindet innerhalb eines einzelnen Datenbankaufrufs:
-- 1. Authentifizierung und Payload-Kanonisierung
-- 2. Operations-ID-Ausstellung
-- 3. Idempotenzreservierung
-- 4. Domain-Speichermutation
-- 5. Idempotenzabschluss
--
-- Keine direkte Tabellenmutation in diesem äußeren RPC.
-- Keine Ausgabe interner UUIDs, Hashes oder Fingerprints.
-- Noch keine direkte App-Ausführungsfreigabe.

create or replace function
public.accaoui_mutate_exam_history_domain(
  p_client_request_key text,
  p_operation_scope text,
  p_operation text,
  p_resource_identity text,
  p_expected_storage_version bigint,
  p_domain_payload jsonb default null
)
returns table (
  outcome text,
  operation_status text,
  result jsonb,
  failure_code text,
  retryable boolean
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

  v_external_operation_id uuid;

  v_reservation_status text;
  v_operation_status text;
  v_reserved_result jsonb;
  v_reserved_failure text;

  v_domain_outcome text;
  v_storage_version bigint;
  v_is_deleted boolean;
  v_created_at timestamptz;
  v_updated_at timestamptz;
  v_domain_result jsonb;

  v_failure_code text;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception using
      errcode = '28000',
      message = 'authentication_required';
  end if;

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

  select issued.external_operation_id
  into v_external_operation_id
  from public.accaoui_issue_exam_history_operation_identity(
    p_client_request_key,
    p_operation_scope,
    p_operation,
    p_resource_identity,
    p_expected_storage_version,
    v_payload_fingerprint
  ) as issued;

  if v_external_operation_id is null then
    raise exception using
      errcode = 'P0001',
      message = 'outer_operation_identity_missing';
  end if;

  select
    reservation.reservation_status,
    reservation.operation_status,
    reservation.result_payload,
    reservation.failure_code
  into
    v_reservation_status,
    v_operation_status,
    v_reserved_result,
    v_reserved_failure
  from public.accaoui_reserve_exam_history_idempotency_operation(
    v_external_operation_id,
    p_operation_scope,
    p_operation,
    p_resource_identity,
    p_expected_storage_version,
    v_payload_fingerprint
  ) as reservation;

  if v_reservation_status is null then
    raise exception using
      errcode = 'P0001',
      message = 'outer_idempotency_reservation_missing';
  end if;

  if v_reservation_status = 'reserved_existing_pending' then
    return query
    select
      'in_progress'::text,
      'pending'::text,
      null::jsonb,
      null::text,
      true;

    return;
  end if;

  if v_reservation_status = 'reserved_existing_completed' then
    return query
    select
      coalesce(
        v_reserved_result ->> 'outcome',
        'completed'
      )::text,
      'completed'::text,
      v_reserved_result,
      null::text,
      false;

    return;
  end if;

  if v_reservation_status = 'reserved_existing_failed' then
    return query
    select
      'failed'::text,
      'failed'::text,
      null::jsonb,
      v_reserved_failure,
      false;

    return;
  end if;

  if v_reservation_status <> 'reserved_new' then
    raise exception using
      errcode = '23514',
      message = 'outer_reservation_status_invalid';
  end if;

  begin
    select
      mutation.outcome,
      mutation.storage_version,
      mutation.is_deleted,
      mutation.created_at,
      mutation.updated_at
    into
      v_domain_outcome,
      v_storage_version,
      v_is_deleted,
      v_created_at,
      v_updated_at
    from public.accaoui_mutate_exam_history_domain_resource(
      p_operation_scope,
      p_operation,
      p_resource_identity,
      p_expected_storage_version,
      v_canonical_payload
    ) as mutation;

    if
      v_domain_outcome is null
      or v_storage_version is null
    then
      raise exception using
        errcode = '23514',
        message = 'domain_storage_state_invalid';
    end if;

    v_domain_result := jsonb_build_object(
      'outcome',
      v_domain_outcome,
      'storage_version',
      v_storage_version,
      'is_deleted',
      v_is_deleted,
      'created_at',
      v_created_at,
      'updated_at',
      v_updated_at
    );

  exception
    when sqlstate '22023'
      or sqlstate '40001'
      or sqlstate '23514'
    then
      get stacked diagnostics
        v_failure_code = message_text;

      if v_failure_code not in (
        'domain_storage_expected_version_invalid',
        'domain_storage_version_conflict',
        'domain_storage_resource_identity_invalid',
        'domain_storage_scope_invalid',
        'domain_storage_payload_invalid',
        'domain_storage_state_invalid'
      )
      then
        raise;
      end if;

      perform
        public.accaoui_complete_exam_history_idempotency_operation(
          v_external_operation_id,
          p_operation_scope,
          p_operation,
          p_resource_identity,
          v_payload_fingerprint,
          'failed',
          null,
          v_failure_code
        );

      return query
      select
        'failed'::text,
        'failed'::text,
        null::jsonb,
        v_failure_code,
        false;

      return;
  end;

  perform
    public.accaoui_complete_exam_history_idempotency_operation(
      v_external_operation_id,
      p_operation_scope,
      p_operation,
      p_resource_identity,
      v_payload_fingerprint,
      'completed',
      v_domain_result,
      null
    );

  return query
  select
    v_domain_outcome,
    'completed'::text,
    v_domain_result,
    null::text,
    false;
end;
$$;

revoke all on function
public.accaoui_mutate_exam_history_domain(
  text,
  text,
  text,
  text,
  bigint,
  jsonb
)
from public;

revoke all on function
public.accaoui_mutate_exam_history_domain(
  text,
  text,
  text,
  text,
  bigint,
  jsonb
)
from anon;

revoke all on function
public.accaoui_mutate_exam_history_domain(
  text,
  text,
  text,
  text,
  bigint,
  jsonb
)
from authenticated;

-- Bewusst kein GRANT EXECUTE.
-- Bewusst keine direkte Tabellenmutation.
-- Bewusst keine UI-Anbindung.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
