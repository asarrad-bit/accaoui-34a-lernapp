-- Accaoui §34a Lern-App
-- Sicherer und atomarer Start der schriftlichen Vollsimulation
-- Stand: v27.27a
-- Status: vorbereitet, nicht live ausgeführt

create unique index if not exists
uq_exam_attempts_open_full_simulation
on public.exam_attempts(participant_id, course_id)
where mode = 'full_simulation'
  and finished_at is null;

create or replace function public.accaoui_start_full_exam(
  p_course_id uuid
)
returns table (
  exam_attempt_id uuid,
  question_count integer,
  max_points integer,
  resumed boolean
)
language plpgsql
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
  v_participant_id uuid;
  v_exam_attempt_id uuid;
  v_recorded_max_points integer;
  v_question_count integer;
  v_key_count integer;
  v_max_points integer;
  v_inserted_questions integer;
  v_inserted_keys integer;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception 'Prüfungsstart erfordert eine Anmeldung.'
      using errcode = '28000';
  end if;

  if p_course_id is null then
    raise exception 'Eine Kurs-ID ist erforderlich.'
      using errcode = '22004';
  end if;

  select p.id
  into v_participant_id
  from public.participants p
  where p.auth_user_id = v_auth_user_id
    and p.status = 'active';

  if not found then
    raise exception 'Kein aktiver Teilnehmerzugang vorhanden.'
      using errcode = '42501';
  end if;

  perform pg_catalog.pg_advisory_xact_lock(
    pg_catalog.hashtextextended(v_auth_user_id::text, 0)
  );

  if not exists (
    select 1
    from public.courses c
    join public.enrollments e
      on e.course_id = c.id
    where c.id = p_course_id
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

  select ea.id, ea.max_points
  into v_exam_attempt_id, v_recorded_max_points
  from public.exam_attempts ea
  where ea.participant_id = v_participant_id
    and ea.course_id = p_course_id
    and ea.mode = 'full_simulation'
    and ea.finished_at is null
  order by ea.created_at desc
  limit 1;

  if found then
    select
      count(*)::integer,
      coalesce(sum(aq.max_points_snapshot), 0)::integer
    into v_question_count, v_max_points
    from public.exam_attempt_questions aq
    where aq.exam_attempt_id = v_exam_attempt_id;

    select count(*)::integer
    into v_key_count
    from public.exam_attempt_question_answer_keys ak
    join public.exam_attempt_questions aq
      on aq.id = ak.attempt_question_id
    where aq.exam_attempt_id = v_exam_attempt_id;

    if v_question_count <> 82
       or v_key_count <> 82
       or v_max_points <> 120
       or v_recorded_max_points <> 120 then
      raise exception
        'Offener Prüfungsversuch besitzt unvollständige Snapshots.'
        using errcode = 'P0001';
    end if;

    return query
    select
      v_exam_attempt_id,
      v_question_count,
      v_max_points,
      true;

    return;
  end if;

  perform q.id
  from public.exam_questions q
  join public.exam_question_answer_keys k
    on k.question_id = q.id
  where q.status = 'active'
    and q.core_position is not null
  order by q.core_position
  for share of q, k;

  select
    count(*)::integer,
    coalesce(sum(q.points), 0)::integer
  into v_question_count, v_max_points
  from public.exam_questions q
  join public.exam_question_answer_keys k
    on k.question_id = q.id
  where q.status = 'active'
    and q.core_position is not null;

  if v_question_count <> 82 or v_max_points <> 120 then
    raise exception
      'Aktive Core-Fragenbank muss exakt 82 Fragen und 120 Punkte enthalten.'
      using errcode = 'P0001';
  end if;

  insert into public.exam_attempts (
    participant_id,
    course_id,
    mode,
    score_points,
    max_points,
    passed,
    started_at
  )
  values (
    v_participant_id,
    p_course_id,
    'full_simulation',
    0,
    v_max_points,
    false,
    statement_timestamp()
  )
  returning id into v_exam_attempt_id;

  insert into public.exam_attempt_questions (
    exam_attempt_id,
    question_id,
    display_order,
    source_question_id_snapshot,
    question_version_snapshot,
    category_snapshot,
    question_type_snapshot,
    question_text_snapshot,
    answer_options_snapshot,
    max_points_snapshot
  )
  select
    v_exam_attempt_id,
    q.id,
    q.core_position,
    q.source_question_id,
    q.version,
    q.category,
    q.question_type,
    q.question_text,
    q.answer_options,
    q.points
  from public.exam_questions q
  join public.exam_question_answer_keys k
    on k.question_id = q.id
  where q.status = 'active'
    and q.core_position is not null
  order by q.core_position;

  get diagnostics v_inserted_questions = row_count;

  if v_inserted_questions <> 82 then
    raise exception
      'Es konnten nicht exakt 82 sichtbare Fragen-Snapshots erstellt werden.'
      using errcode = 'P0001';
  end if;

  insert into public.exam_attempt_question_answer_keys (
    attempt_question_id,
    correct_answers_snapshot,
    explanation_snapshot,
    grading_rule,
    answer_hash_snapshot
  )
  select
    aq.id,
    k.correct_answers,
    k.explanation,
    'per_correct_selection_no_penalty',
    k.answer_hash
  from public.exam_attempt_questions aq
  join public.exam_question_answer_keys k
    on k.question_id = aq.question_id
  where aq.exam_attempt_id = v_exam_attempt_id
  order by aq.display_order;

  get diagnostics v_inserted_keys = row_count;

  if v_inserted_keys <> 82 then
    raise exception
      'Es konnten nicht exakt 82 private Lösungsschlüssel-Snapshots erstellt werden.'
      using errcode = 'P0001';
  end if;

  return query
  select
    v_exam_attempt_id,
    v_inserted_questions,
    v_max_points,
    false;
end;
$$;

revoke all
on function public.accaoui_start_full_exam(uuid)
from public;

revoke all
on function public.accaoui_start_full_exam(uuid)
from anon;

revoke all
on function public.accaoui_start_full_exam(uuid)
from authenticated;

grant execute
on function public.accaoui_start_full_exam(uuid)
to authenticated;

-- Die Rückgabe enthält keine Lösungsschlüssel oder Erklärungen.
-- Fehler rollen den gesamten Prüfungsstart zurück.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
