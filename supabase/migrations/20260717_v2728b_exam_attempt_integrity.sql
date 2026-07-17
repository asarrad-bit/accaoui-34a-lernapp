-- Accaoui §34a Lern-App
-- Zusätzliche Integritätsgrenzen für Prüfungsversuche
-- Stand: v27.28b
-- Status: vorbereitet, nicht live ausgeführt

do $$
begin
  if exists (
    select 1
    from public.exam_attempts
    where score_points > max_points
  ) then
    raise exception
      'Bestehende Prüfungsversuche enthalten mehr Punkte als maximal erlaubt.';
  end if;

  if exists (
    select 1
    from public.exam_attempts
    where finished_at is not null
      and (
        started_at is null
        or finished_at < started_at
      )
  ) then
    raise exception
      'Bestehende Prüfungsversuche besitzen ungültige Zeitangaben.';
  end if;
end;
$$;

alter table public.exam_attempts
  drop constraint if exists
  exam_attempts_score_within_max_check;

alter table public.exam_attempts
  add constraint exam_attempts_score_within_max_check
  check (score_points <= max_points);

alter table public.exam_attempts
  drop constraint if exists
  exam_attempts_finished_after_started_check;

alter table public.exam_attempts
  add constraint exam_attempts_finished_after_started_check
  check (
    finished_at is null
    or (
      started_at is not null
      and finished_at >= started_at
    )
  );
