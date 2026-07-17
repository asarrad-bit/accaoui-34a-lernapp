-- Accaoui §34a Lern-App
-- Sichere Liste eigener abgeschlossener Vollsimulationen
-- Stand: v27.29a
-- Status: vorbereitet, nicht live ausgeführt

create or replace function public.accaoui_list_full_exam_results(
  p_limit integer default 20,
  p_offset integer default 0
)
returns table (
  exam_attempt_id uuid,
  course_id uuid,
  course_title text,
  score_points integer,
  max_points integer,
  passed boolean,
  started_at timestamptz,
  finished_at timestamptz,
  total_count bigint
)
language plpgsql
stable
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception
      'Prüfungsergebnisliste erfordert eine Anmeldung.'
      using errcode = '28000';
  end if;

  if p_limit is null
     or p_limit not between 1 and 50 then
    raise exception
      'Das Ergebnislimit muss zwischen 1 und 50 liegen.'
      using errcode = '22023';
  end if;

  if p_offset is null
     or p_offset not between 0 and 10000 then
    raise exception
      'Der Ergebnisoffset muss zwischen 0 und 10000 liegen.'
      using errcode = '22023';
  end if;

  if exists (
    select 1
    from public.exam_attempts ea
    join public.participants p
      on p.id = ea.participant_id
    where p.auth_user_id = v_auth_user_id
      and p.status in ('active', 'expired', 'completed')
      and ea.mode = 'full_simulation'
      and ea.finished_at is not null
      and (
        ea.max_points is null
        or ea.max_points <> 120
        or ea.score_points is null
        or ea.score_points not between 0 and 120
        or ea.passed is null
        or ea.passed <> (ea.score_points >= 60)
        or ea.started_at is null
        or ea.finished_at < ea.started_at
      )
  ) then
    raise exception
      'Mindestens ein gespeichertes Prüfungsergebnis ist ungültig.'
      using errcode = 'P0001';
  end if;

  return query
  select
    ea.id,
    ea.course_id,
    c.title,
    ea.score_points,
    ea.max_points,
    ea.passed,
    ea.started_at,
    ea.finished_at,
    count(*) over ()
  from public.exam_attempts ea
  join public.participants p
    on p.id = ea.participant_id
  left join public.courses c
    on c.id = ea.course_id
  where p.auth_user_id = v_auth_user_id
    and p.status in ('active', 'expired', 'completed')
    and ea.mode = 'full_simulation'
    and ea.finished_at is not null
  order by
    ea.finished_at desc,
    ea.id desc
  limit p_limit
  offset p_offset;
end;
$$;

revoke all
on function public.accaoui_list_full_exam_results(integer, integer)
from public;

revoke all
on function public.accaoui_list_full_exam_results(integer, integer)
from anon;

revoke all
on function public.accaoui_list_full_exam_results(integer, integer)
from authenticated;

grant execute
on function public.accaoui_list_full_exam_results(integer, integer)
to authenticated;

-- Nur eigene abgeschlossene Vollsimulationen.
-- Gesperrte Teilnehmer werden ausgeschlossen.
-- Keine Antworten, Schlüssel oder Erklärungen.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
