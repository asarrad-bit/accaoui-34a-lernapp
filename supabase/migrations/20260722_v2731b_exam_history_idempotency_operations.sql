-- Accaoui §34a Lern-App – Idempotenz-Operationstabelle
-- Stand: v27.31b
-- Status: vorbereitet, nicht live ausgeführt
--
-- Direkter Zugriff aller App-Rollen bleibt gesperrt.
-- Spätere Nutzung ausschließlich über einen geprüften,
-- atomaren Security-Definer-RPC.

create table if not exists public.exam_history_idempotency_operations (
  id uuid primary key default gen_random_uuid(),

  auth_user_id uuid not null,

  operation_identity text not null,

  external_operation_id uuid not null
    constraint exam_history_idempotency_external_id_v4_check
    check (
      external_operation_id::text ~
      '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$'
    ),

  operation_scope text not null
    constraint exam_history_idempotency_scope_check
    check (
      operation_scope in (
        'snapshot',
        'cycle_registry'
      )
    ),

  operation text not null
    constraint exam_history_idempotency_operation_check
    check (
      operation in (
        'write',
        'delete'
      )
    ),

  resource_identity text not null
    constraint exam_history_idempotency_resource_identity_check
    check (
      resource_identity = trim(resource_identity)
      and length(resource_identity) between 1 and 512
    ),

  payload_fingerprint text,

  status text not null default 'pending'
    constraint exam_history_idempotency_status_check
    check (
      status in (
        'pending',
        'completed',
        'failed'
      )
    ),

  result_payload jsonb,

  failure_code text,

  created_at timestamptz not null default now(),

  updated_at timestamptz not null default now(),

  completed_at timestamptz,

  constraint exam_history_idempotency_operation_identity_key
    unique (operation_identity),

  constraint exam_history_idempotency_external_operation_key
    unique (
      operation_scope,
      operation,
      external_operation_id
    ),

  constraint exam_history_idempotency_identity_check
    check (
      operation_identity =
        'exam_history_idempotency:' ||
        operation_scope || ':' ||
        operation || ':' ||
        external_operation_id::text
    ),

  constraint exam_history_idempotency_payload_check
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
    ),

  constraint exam_history_idempotency_result_payload_check
    check (
      result_payload is null
      or jsonb_typeof(result_payload) = 'object'
    ),

  constraint exam_history_idempotency_terminal_state_check
    check (
      (
        status = 'pending'
        and result_payload is null
        and failure_code is null
        and completed_at is null
      )
      or
      (
        status = 'completed'
        and result_payload is not null
        and failure_code is null
        and completed_at is not null
      )
      or
      (
        status = 'failed'
        and result_payload is null
        and failure_code is not null
        and failure_code = trim(failure_code)
        and length(failure_code) between 1 and 128
        and completed_at is not null
      )
    ),

  constraint exam_history_idempotency_time_order_check
    check (
      updated_at >= created_at
      and (
        completed_at is null
        or completed_at >= created_at
      )
    )
);

create index if not exists
  idx_exam_history_idempotency_auth_user_created
on public.exam_history_idempotency_operations (
  auth_user_id,
  created_at desc
);

create index if not exists
  idx_exam_history_idempotency_status_created
on public.exam_history_idempotency_operations (
  status,
  created_at
);

alter table public.exam_history_idempotency_operations
enable row level security;

alter table public.exam_history_idempotency_operations
force row level security;

revoke all
on table public.exam_history_idempotency_operations
from public, anon, authenticated;

-- Keine Direktpolicy.
-- Keine direkte App-Rollenfreigabe.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
