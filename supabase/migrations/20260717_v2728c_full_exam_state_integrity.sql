-- Accaoui §34a Lern-App
-- Zustandsintegrität für schriftliche Vollsimulationen
-- Stand: v27.28c
-- Status: vorbereitet, nicht live ausgeführt

do $$
begin
  if exists (
    select 1
    from public.exam_attempts
    where mode = 'full_simulation'
      and (
        max_points <> 120
        or started_at is null
        or (
          finished_at is null
          and (
            score_points <> 0
            or passed
          )
        )
        or (
          finished_at is not null
          and passed <> (score_points >= 60)
        )
      )
  ) then
    raise exception
      'Bestehende Vollsimulationen besitzen ungültige Zustandsdaten.';
  end if;
end;
$$;

alter table public.exam_attempts
  drop constraint if exists
  exam_attempts_full_simulation_state_check;

alter table public.exam_attempts
  add constraint exam_attempts_full_simulation_state_check
  check (
    mode <> 'full_simulation'
    or (
      max_points = 120
      and started_at is not null
      and (
        (
          finished_at is null
          and score_points = 0
          and not passed
        )
        or (
          finished_at is not null
          and passed = (score_points >= 60)
        )
      )
    )
  );
