-- Accaoui §34a Lern-App
-- Sicherer Prüfungsabschluss mit serverseitiger Bewertung
-- Stand: v27.27d
-- Status: vorbereitet, nicht live ausgeführt

create or replace function public.accaoui_finish_full_exam(
  p_exam_attempt_id uuid
)
returns table (
  exam_attempt_id uuid,
  answered_questions integer,
  correct_questions integer,
  score_points integer,
  max_points integer,
  passed boolean,
  finished_at timestamptz,
  already_finished boolean
)
language plpgsql
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
  v_participant_id uuid;
  v_course_id uuid;
  v_recorded_score integer;
  v_recorded_max integer;
  v_recorded_passed boolean;
  v_recorded_finished_at timestamptz;
  v_snapshot_count integer;
  v_key_count integer;
  v_rule_count integer;
  v_snapshot_max integer;
  v_answer_count integer;
  v_answered_count integer;
  v_correct_count integer;
  v_graded_count integer;
  v_score integer;
  v_finished_at timestamptz;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception 'Prüfungsabschluss erfordert eine Anmeldung.'
      using errcode = '28000';
  end if;

  if p_exam_attempt_id is null then
    raise exception 'Eine Prüfungsversuchs-ID ist erforderlich.'
      using errcode = '22004';
  end if;

  select
    ea.participant_id,
    ea.course_id,
    ea.score_points,
    ea.max_points,
    ea.passed,
    ea.finished_at
  into
    v_participant_id,
    v_course_id,
    v_recorded_score,
    v_recorded_max,
    v_recorded_passed,
    v_recorded_finished_at
  from public.exam_attempts ea
  join public.participants p
    on p.id = ea.participant_id
  where ea.id = p_exam_attempt_id
    and p.auth_user_id = v_auth_user_id
    and p.status = 'active'
    and ea.mode = 'full_simulation'
  for update of ea;

  if not found then
    raise exception
      'Prüfungsversuch gehört nicht zum aktiven Teilnehmer.'
      using errcode = '42501';
  end if;

  -- Wiederholte Abschlussaufrufe liefern dasselbe gespeicherte Ergebnis.
  if v_recorded_finished_at is not null then
    select
      count(*)::integer,
      count(*) filter (
        where jsonb_array_length(ans.selected_answers) > 0
      )::integer,
      count(*) filter (
        where ans.is_correct
      )::integer
    into
      v_answer_count,
      v_answered_count,
      v_correct_count
    from public.exam_answers ans
    where ans.exam_attempt_id = p_exam_attempt_id;

    if v_answer_count <> 82
       or v_recorded_max <> 120
       or v_recorded_score not between 0 and 120 then
      raise exception
        'Abgeschlossener Prüfungsversuch besitzt ungültige Ergebnisdaten.'
        using errcode = 'P0001';
    end if;

    return query
    select
      p_exam_attempt_id,
      v_answered_count,
      v_correct_count,
      v_recorded_score,
      v_recorded_max,
      v_recorded_passed,
      v_recorded_finished_at,
      true;

    return;
  end if;

  if not exists (
    select 1
    from public.courses c
    join public.enrollments e
      on e.course_id = c.id
    where c.id = v_course_id
      and c.status = 'active'
      and e.participant_id = v_participant_id
      and e.access_status = 'allowed'
      and (
        e.access_starts_at is null
        or e.access_starts_at <= statement_timestamp()
      )
      and (
        e.access_ends_at is null
        or e.access_ends_at > statement_timestamp()
      )
  ) then
    raise exception 'Kein aktiver Kurszugang vorhanden.'
      using errcode = '42501';
  end if;

  select
    count(*)::integer,
    count(ak.attempt_question_id)::integer,
    count(*) filter (
      where ak.grading_rule =
        'per_correct_selection_no_penalty'
    )::integer,
    coalesce(sum(aq.max_points_snapshot), 0)::integer
  into
    v_snapshot_count,
    v_key_count,
    v_rule_count,
    v_snapshot_max
  from public.exam_attempt_questions aq
  left join public.exam_attempt_question_answer_keys ak
    on ak.attempt_question_id = aq.id
  where aq.exam_attempt_id = p_exam_attempt_id;

  if v_snapshot_count <> 82
     or v_key_count <> 82
     or v_rule_count <> 82
     or v_snapshot_max <> 120 then
    raise exception
      'Prüfungsversuch besitzt keine vollständigen 82/120-Snapshots.'
      using errcode = 'P0001';
  end if;

  -- Fehlende Antworten werden als unbeantwortet mit null Punkten ergänzt.
  insert into public.exam_answers (
    exam_attempt_id,
    attempt_question_id,
    selected_answers,
    earned_points,
    max_points,
    is_correct
  )
  select
    aq.exam_attempt_id,
    aq.id,
    '[]'::jsonb,
    0,
    aq.max_points_snapshot,
    false
  from public.exam_attempt_questions aq
  where aq.exam_attempt_id = p_exam_attempt_id
  on conflict (attempt_question_id)
  do nothing;

  select
    count(*)::integer,
    count(*) filter (
      where jsonb_array_length(ans.selected_answers) > 0
    )::integer
  into
    v_answer_count,
    v_answered_count
  from public.exam_answers ans
  where ans.exam_attempt_id = p_exam_attempt_id;

  if v_answer_count <> 82 then
    raise exception
      'Prüfungsversuch besitzt nicht exakt 82 Antwortzeilen.'
      using errcode = 'P0001';
  end if;

  with grades as (
    select
      ans.id as answer_id,
      aq.max_points_snapshot::integer as question_max_points,

      (
        select count(*)::integer
        from jsonb_array_elements_text(
          ans.selected_answers
        ) selected(value)
        where exists (
          select 1
          from jsonb_array_elements_text(
            ak.correct_answers_snapshot
          ) correct(value)
          where correct.value = selected.value
        )
      ) as correct_selection_count,

      (
        jsonb_array_length(ans.selected_answers) =
          jsonb_array_length(ak.correct_answers_snapshot)

        and not exists (
          select 1
          from jsonb_array_elements_text(
            ans.selected_answers
          ) selected(value)
          where not exists (
            select 1
            from jsonb_array_elements_text(
              ak.correct_answers_snapshot
            ) correct(value)
            where correct.value = selected.value
          )
        )

        and not exists (
          select 1
          from jsonb_array_elements_text(
            ak.correct_answers_snapshot
          ) correct(value)
          where not exists (
            select 1
            from jsonb_array_elements_text(
              ans.selected_answers
            ) selected(value)
            where selected.value = correct.value
          )
        )
      ) as is_exact

    from public.exam_answers ans
    join public.exam_attempt_questions aq
      on aq.id = ans.attempt_question_id
     and aq.exam_attempt_id = ans.exam_attempt_id
    join public.exam_attempt_question_answer_keys ak
      on ak.attempt_question_id = aq.id
    where ans.exam_attempt_id = p_exam_attempt_id
      and ak.grading_rule =
        'per_correct_selection_no_penalty'
  ),
  calculated as (
    select
      g.answer_id,
      g.question_max_points,
      g.is_exact,
      case
        when g.is_exact then g.question_max_points
        else least(
          g.correct_selection_count,
          g.question_max_points
        )
      end as earned_points
    from grades g
  ),
  updated as (
    update public.exam_answers ans
    set
      earned_points = calculated.earned_points,
      max_points = calculated.question_max_points,
      is_correct = calculated.is_exact
    from calculated
    where ans.id = calculated.answer_id
    returning
      ans.earned_points,
      ans.max_points,
      ans.is_correct
  )
  select
    count(*)::integer,
    coalesce(sum(updated.earned_points), 0)::integer,
    coalesce(sum(updated.max_points), 0)::integer,
    count(*) filter (
      where updated.is_correct
    )::integer
  into
    v_graded_count,
    v_score,
    v_snapshot_max,
    v_correct_count
  from updated;

  if v_graded_count <> 82
     or v_snapshot_max <> 120
     or v_score not between 0 and 120 then
    raise exception
      'Serverseitige Prüfungsbewertung ist unvollständig.'
      using errcode = 'P0001';
  end if;

  v_finished_at := statement_timestamp();

  update public.exam_attempts ea
  set
    score_points = v_score,
    max_points = v_snapshot_max,
    passed = (v_score >= 60),
    finished_at = v_finished_at
  where ea.id = p_exam_attempt_id
    and ea.finished_at is null;

  if not found then
    raise exception
      'Prüfungsversuch konnte nicht abgeschlossen werden.'
      using errcode = 'P0001';
  end if;

  return query
  select
    p_exam_attempt_id,
    v_answered_count,
    v_correct_count,
    v_score,
    v_snapshot_max,
    (v_score >= 60),
    v_finished_at,
    false;
end;
$$;

revoke all
on function public.accaoui_finish_full_exam(uuid)
from public;

revoke all
on function public.accaoui_finish_full_exam(uuid)
from anon;

revoke all
on function public.accaoui_finish_full_exam(uuid)
from authenticated;

grant execute
on function public.accaoui_finish_full_exam(uuid)
to authenticated;

-- Der Browser liefert keine Punkte, Ergebniswerte oder Lösungsschlüssel.
-- Bewertung und Abschluss erfolgen innerhalb einer Transaktion.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
