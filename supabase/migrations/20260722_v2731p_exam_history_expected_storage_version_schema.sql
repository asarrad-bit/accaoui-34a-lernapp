-- Accaoui §34a Lern-App – Speicher-Versionsstand-Schema
-- Stand: v27.31p
-- Status: vorbereitet, nicht live ausgeführt
--
-- Bestehende Zeilen erhalten niemals automatisch einen
-- erfundenen erwarteten Speicher-Versionsstand.
--
-- Enthält eine Zieltabelle bereits Zeilen, bricht die
-- Migration kontrolliert ab.
--
-- Keine Helper-, Fach- oder Idempotenzmutation.
-- Keine direkte App-Rollenfreigabe.

do $$
begin
  if exists (
    select 1
    from public.exam_history_operation_identity_issuances
    limit 1
  ) then
    raise exception using
      errcode = 'P0001',
      message =
        'exam_history_issuance_existing_rows_require_expected_storage_version_backfill';
  end if;

  if exists (
    select 1
    from public.exam_history_idempotency_operations
    limit 1
  ) then
    raise exception using
      errcode = 'P0001',
      message =
        'exam_history_idempotency_existing_rows_require_expected_storage_version_backfill';
  end if;
end;
$$;

alter table
public.exam_history_operation_identity_issuances
add column expected_storage_version bigint not null
constraint exam_history_issuance_expected_storage_version_check
check (
  expected_storage_version >= 0
);

alter table
public.exam_history_idempotency_operations
add column expected_storage_version bigint not null
constraint exam_history_idempotency_expected_storage_version_check
check (
  expected_storage_version >= 0
);

alter table
public.exam_history_operation_identity_issuances
enable row level security;

alter table
public.exam_history_operation_identity_issuances
force row level security;

alter table
public.exam_history_idempotency_operations
enable row level security;

alter table
public.exam_history_idempotency_operations
force row level security;

revoke all
on table public.exam_history_operation_identity_issuances
from public, anon, authenticated;

revoke all
on table public.exam_history_idempotency_operations
from public, anon, authenticated;

-- Bewusst kein DEFAULT:
-- Jeder spätere interne Insert muss den Versionsstand
-- ausdrücklich und geprüft übermitteln.
--
-- Keine Direktpolicy.
-- Kein GRANT.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
