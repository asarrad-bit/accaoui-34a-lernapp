-- Accaoui §34a Lern-App – Operations-ID-Ausstellungen
-- Stand: v27.31h
-- Status: vorbereitet, nicht live ausgeführt
--
-- Der rohe Client-Wiederholungsschlüssel wird nicht gespeichert.
-- Direkter Zugriff aller App-Rollen bleibt gesperrt.

create table if not exists
public.exam_history_operation_identity_issuances (
  id uuid primary key default gen_random_uuid(),

  auth_user_id uuid not null,

  client_request_key_hash text not null
    constraint exam_history_issuance_client_key_hash_check
    check (
      client_request_key_hash ~ '^[0-9a-f]{64}$'
    ),

  request_fingerprint text not null
    constraint exam_history_issuance_request_fingerprint_check
    check (
      request_fingerprint ~ '^[0-9a-f]{64}$'
    ),

  external_operation_id uuid not null
    default gen_random_uuid()
    constraint exam_history_issuance_external_id_v4_check
    check (
      external_operation_id::text ~
      '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    ),

  operation_scope text not null
    constraint exam_history_issuance_scope_check
    check (
      operation_scope in (
        'snapshot',
        'cycle_registry'
      )
    ),

  operation text not null
    constraint exam_history_issuance_operation_check
    check (
      operation in (
        'write',
        'delete'
      )
    ),

  resource_identity text not null
    constraint exam_history_issuance_resource_check
    check (
      resource_identity = trim(resource_identity)
      and length(resource_identity) between 1 and 512
    ),

  payload_fingerprint text,

  issued_at timestamptz not null default now(),

  constraint exam_history_issuance_user_client_key
    unique (
      auth_user_id,
      client_request_key_hash
    ),

  constraint exam_history_issuance_external_operation_id
    unique (
      external_operation_id
    ),

  constraint exam_history_issuance_payload_check
    check (
      (
        operation = 'write'
        and payload_fingerprint is not null
        and payload_fingerprint ~ '^[0-9a-f]{64}$'
      )
      or
      (
        operation = 'delete'
        and payload_fingerprint is null
      )
    )
);

create index if not exists
  idx_exam_history_issuance_user_issued
on public.exam_history_operation_identity_issuances (
  auth_user_id,
  issued_at desc
);

create index if not exists
  idx_exam_history_issuance_request_fingerprint
on public.exam_history_operation_identity_issuances (
  auth_user_id,
  request_fingerprint
);

alter table public.exam_history_operation_identity_issuances
enable row level security;

alter table public.exam_history_operation_identity_issuances
force row level security;

revoke all
on table public.exam_history_operation_identity_issuances
from public, anon, authenticated;

-- Keine Direktpolicy.
-- Keine direkte App-Rollenfreigabe.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
