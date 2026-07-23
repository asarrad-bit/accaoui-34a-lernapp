-- Accaoui §34a Lern-App – Domain-Speichertabelle
-- Stand: v27.31s
-- Status: vorbereitet, nicht live ausgeführt
--
-- Gemeinsame vollständig gesperrte Speichergrenze für:
-- - Snapshot
-- - Zyklusregister
--
-- Keine direkte App-Policy und keine direkte App-Rollenfreigabe.
-- Keine Fachmutation und kein äußerer Mutations-RPC in diesem Schritt.

do $$
begin
  if to_regclass(
    'public.exam_history_domain_resources'
  ) is not null then
    raise exception using
      errcode = '42P07',
      message = 'exam_history_domain_resources_already_exists';
  end if;
end;
$$;

create table public.exam_history_domain_resources (
  id uuid primary key default gen_random_uuid(),

  auth_user_id uuid not null,

  operation_scope text not null
    constraint exam_history_domain_resources_scope_check
    check (
      operation_scope in (
        'snapshot',
        'cycle_registry'
      )
    ),

  resource_identity text not null
    constraint exam_history_domain_resources_identity_check
    check (
      resource_identity = trim(resource_identity)
      and length(resource_identity) between 1 and 512
    ),

  schema_version smallint not null default 1
    constraint exam_history_domain_resources_schema_version_check
    check (schema_version = 1),

  domain_payload jsonb,

  payload_fingerprint text,

  canonical_byte_length integer,

  storage_version bigint not null
    constraint exam_history_domain_resources_storage_version_check
    check (storage_version >= 1),

  is_deleted boolean not null default false,

  created_at timestamptz not null default now(),

  updated_at timestamptz not null default now(),

  constraint exam_history_domain_resources_unique_identity
    unique (
      auth_user_id,
      operation_scope,
      resource_identity
    ),

  constraint exam_history_domain_resources_fingerprint_check
    check (
      payload_fingerprint is null
      or payload_fingerprint ~ '^[0-9a-f]{64}$'
    ),

  constraint exam_history_domain_resources_byte_length_check
    check (
      canonical_byte_length is null
      or canonical_byte_length >= 0
    ),

  constraint exam_history_domain_resources_time_order_check
    check (updated_at >= created_at),

  constraint exam_history_domain_resources_state_check
    check (
      (
        is_deleted = false
        and domain_payload is not null
        and jsonb_typeof(domain_payload) = 'object'
        and payload_fingerprint is not null
        and payload_fingerprint ~ '^[0-9a-f]{64}$'
        and canonical_byte_length is not null
        and canonical_byte_length >= 0
        and (
          (
            operation_scope = 'snapshot'
            and canonical_byte_length <= 262144
          )
          or
          (
            operation_scope = 'cycle_registry'
            and canonical_byte_length <= 131072
          )
        )
      )
      or
      (
        is_deleted = true
        and domain_payload is null
        and payload_fingerprint is null
        and canonical_byte_length is null
      )
    )
  )
);

create index
  idx_exam_history_domain_resources_user_scope_updated
on public.exam_history_domain_resources (
  auth_user_id,
  operation_scope,
  updated_at desc
);

alter table public.exam_history_domain_resources
  enable row level security;

alter table public.exam_history_domain_resources
  force row level security;

revoke all
on table public.exam_history_domain_resources
from public, anon, authenticated;

-- Bewusst keine Policy.
-- Bewusst kein GRANT.
-- Bewusst kein Mutationshelper.
-- Bewusst kein äußerer Fachmutations-RPC.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
