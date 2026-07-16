-- Accaoui §34a Lern-App
-- Sicheres Speichern ausgewählter Prüfungsantworten
-- Stand: v27.27b
-- Status: vorbereitet, nicht live ausgeführt

create or replace function public.accaoui_save_exam_answer(
  p_attempt_question_id uuid,
  p_selected_answers jsonb
)
returns table (
  attempt_question_id uuid,
  selected_answers jsonb,
  saved boolean
)
language plpgsql
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
  v_exam_attempt_id uuid;
  v_course_id uuid;
  v_max_points integer;
  v_option_count integer;
  v_answer_count integer;
  v_distinct_count integer;
  v_normalized_answers jsonb;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception 'Antwortspeicherung erfordert eine Anmeldung.'
      using errcode = '28000';
  end if;

  if p_attempt_question_id is null then
    raise exception 'Eine Versuchsfragen-ID ist erforderlich.'
      using errcode = '22004';
  end if;

  if p_selected_answers is null
     or jsonb_typeof(p_selected_answers) <> 'array' then
    raise exception 'Ausgewählte Antworten müssen ein JSON-Array sein.'
      using errcode = '22023';
  end if;

  select
    aq.exam_attempt_id,
    ea.course_id,
    aq.max_points_snapshot,
    jsonb_array_length(aq.answer_options_snapshot)
  into
    v_exam_attempt_id,
    v_course_id,
    v_max_points,
    v_option_count
  from public.exam_attempt_questions aq
  join public.exam_attempts ea
    on ea.id = aq.exam_attempt_id
  join public.participants p
    on p.id = ea.participant_id
  where aq.id = p_attempt_question_id
    and p.auth_user_id = v_auth_user_id
    and p.status = 'active'
    and ea.mode = 'full_simulation'
    and ea.finished_at is null
  for update of aq, ea;

  if not found then
    raise exception
      'Versuchsfrage gehört nicht zu einer offenen eigenen Prüfung.'
      using errcode = '42501';
  end if;

  if not exists (
    select 1
    from public.courses c
    join public.enrollments e
      on e.course_id = c.id
    where c.id = v_course_id
      and c.status = 'active'
      and e.participant_id = (
        select ea.participant_id
        from public.exam_attempts ea
        where ea.id = v_exam_attempt_id
      )
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

  v_answer_count := jsonb_array_length(p_selected_answers);

  if v_answer_count > v_max_points then
    raise exception
      'Es wurden mehr Antworten gewählt als für diese Frage erlaubt.'
      using errcode = '22023';
  end if;

  if exists (
    select 1
    from jsonb_array_elements(p_selected_answers) as item(value)
    where case
      when jsonb_typeof(item.value) <> 'number' then true
      when (item.value #>> '{}') !~ '^[0-9]+$' then true
      else (item.value #>> '{}')::integer >= v_option_count
    end
  ) then
    raise exception
      'Mindestens ein Antwortindex ist ungültig.'
      using errcode = '22023';
  end if;

  select count(distinct item.value #>> '{}')::integer
  into v_distinct_count
  from jsonb_array_elements(p_selected_answers) as item(value);

  if v_distinct_count <> v_answer_count then
    raise exception
      'Doppelte Antwortindizes sind nicht erlaubt.'
      using errcode = '22023';
  end if;

  select coalesce(
    jsonb_agg(
      (item.value #>> '{}')::integer
      order by (item.value #>> '{}')::integer
    ),
    '[]'::jsonb
  )
  into v_normalized_answers
  from jsonb_array_elements(p_selected_answers) as item(value);

  insert into public.exam_answers (
    exam_attempt_id,
    attempt_question_id,
    selected_answers,
    earned_points,
    max_points,
    is_correct
  )
  values (
    v_exam_attempt_id,
    p_attempt_question_id,
    v_normalized_answers,
    0,
    v_max_points,
    false
  )
  on conflict (attempt_question_id)
  do update set
    selected_answers = excluded.selected_answers,
    earned_points = 0,
    max_points = excluded.max_points,
    is_correct = false
  where exam_answers.exam_attempt_id = excluded.exam_attempt_id;

  if not found then
    raise exception 'Antwort konnte nicht sicher gespeichert werden.'
      using errcode = 'P0001';
  end if;

  return query
  select
    p_attempt_question_id,
    v_normalized_answers,
    true;
end;
$$;

revoke all
on function public.accaoui_save_exam_answer(uuid, jsonb)
from public;

revoke all
on function public.accaoui_save_exam_answer(uuid, jsonb)
from anon;

revoke all
on function public.accaoui_save_exam_answer(uuid, jsonb)
from authenticated;

grant execute
on function public.accaoui_save_exam_answer(uuid, jsonb)
to authenticated;

-- Der Browser übermittelt ausschließlich Versuchsfragen-ID
-- und ausgewählte Antwortindizes.
-- Punkte, Ergebnisstatus und Lösungsschlüssel werden nicht angenommen.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
