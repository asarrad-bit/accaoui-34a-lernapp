-- Accaoui §34a Lern-App – Operations-ID-Ausstellung mit Speicher-Version
-- Stand: v27.31q
-- Status: vorbereitet, nicht live ausgeführt
--
-- Interner Security-Definer-Helfer.
-- Keine direkte Ausführungsfreigabe für App-Rollen.
-- Der rohe Client-Wiederholungsschlüssel wird nur separat gehasht.
-- Der kanonische Anfragefingerprint enthält keinen rohen Client-Schlüssel.
-- Der erwartete Speicher-Versionsstand wird gespeichert und bei Retry verglichen.

create or replace function
public.accaoui_issue_exam_history_operation_identity(
  p_client_request_key text,
  p_operation_scope text,
  p_operation text,
  p_resource_identity text,
  p_expected_storage_version bigint,
  p_payload_fingerprint text default null
)
returns table (
  external_operation_id uuid,
  issuance_status text,
  issued_at timestamptz,
  is_new boolean
)
language plpgsql
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
  v_client_request_key_hash text;
  v_request_fingerprint text;
  v_inserted_id uuid;
  v_inserted_external_operation_id uuid;
  v_inserted_issued_at timestamptz;
  v_existing
    public.exam_history_operation_identity_issuances%rowtype;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception using
      errcode = '28000',
      message = 'authentication_required';
  end if;

  if
    p_client_request_key is null
    or p_client_request_key !~ '^[0-9a-f]{64}$'
  then
    raise exception using
      errcode = '22023',
      message = 'client_request_key_invalid';
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

  v_client_request_key_hash :=
    encode(
      digest(
        convert_to(
          p_client_request_key,
          'UTF8'
        ),
        'sha256'
      ),
      'hex'
    );

  v_request_fingerprint :=
    encode(
      digest(
        convert_to(
          jsonb_build_object(
            'operation_scope',
              p_operation_scope,
            'operation',
              p_operation,
            'resource_identity',
              p_resource_identity,
            'expected_storage_version',
              p_expected_storage_version,
            'payload_fingerprint',
              p_payload_fingerprint
          )::text,
          'UTF8'
        ),
        'sha256'
      ),
      'hex'
    );

  insert into
    public.exam_history_operation_identity_issuances
    as issuance (
      auth_user_id,
      client_request_key_hash,
      request_fingerprint,
      operation_scope,
      operation,
      resource_identity,
      expected_storage_version,
      payload_fingerprint
    )
  values (
    v_auth_user_id,
    v_client_request_key_hash,
    v_request_fingerprint,
    p_operation_scope,
    p_operation,
    p_resource_identity,
    p_expected_storage_version,
    p_payload_fingerprint
  )
  on conflict do nothing
  returning
    issuance.id,
    issuance.external_operation_id,
    issuance.issued_at
  into
    v_inserted_id,
    v_inserted_external_operation_id,
    v_inserted_issued_at;

  if v_inserted_id is not null then
    return query
    select
      v_inserted_external_operation_id,
      'issued_new'::text,
      v_inserted_issued_at,
      true;

    return;
  end if;

  select issuance.*
  into v_existing
  from public.exam_history_operation_identity_issuances
    as issuance
  where
    issuance.auth_user_id =
      v_auth_user_id
    and issuance.client_request_key_hash =
      v_client_request_key_hash
  for update;

  if not found then
    raise exception using
      errcode = '40001',
      message =
        'operation_identity_issuance_conflict_unresolved';
  end if;

  if
    v_existing.request_fingerprint <>
      v_request_fingerprint
    or v_existing.operation_scope <>
      p_operation_scope
    or v_existing.operation <>
      p_operation
    or v_existing.resource_identity <>
      p_resource_identity
    or v_existing.expected_storage_version <>
      p_expected_storage_version
    or v_existing.payload_fingerprint
      is distinct from
      p_payload_fingerprint
  then
    raise exception using
      errcode = '23505',
      message =
        'operation_identity_request_key_conflict';
  end if;

  return query
  select
    v_existing.external_operation_id,
    'issued_existing'::text,
    v_existing.issued_at,
    false;
end;
$$;

revoke all on function
public.accaoui_issue_exam_history_operation_identity(
  text,
  text,
  text,
  text,
  bigint,
  text
)
from public;

revoke all on function
public.accaoui_issue_exam_history_operation_identity(
  text,
  text,
  text,
  text,
  bigint,
  text
)
from anon;

revoke all on function
public.accaoui_issue_exam_history_operation_identity(
  text,
  text,
  text,
  text,
  bigint,
  text
)
from authenticated;

drop function if exists
public.accaoui_issue_exam_history_operation_identity(
  text,
  text,
  text,
  text,
  text
);

-- Keine direkte Ausführungsfreigabe.
-- Keine Änderung am Idempotenz-Reservierungshelper.
-- Keine Fachmutation und keine Live-Ausführung.
