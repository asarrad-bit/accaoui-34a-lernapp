-- Accaoui §34a Lern-App
-- Sicherer Abruf eines eigenen abgeschlossenen Prüfungsergebnisses
-- Stand: v27.27f
-- Status: vorbereitet, nicht live ausgeführt

create or replace function public.accaoui_get_full_exam_result(
  p_exam_attempt_id uuid
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
  total_questions integer,
  answered_questions integer,
  correct_questions integer,
  partial_questions integer,
  wrong_questions integer,
  unanswered_questions integer
)
language plpgsql
stable
security definer
set search_path = pg_catalog, public
set row_security = off
as $$
declare
  v_auth_user_id uuid;
  v_course_id uuid;
  v_course_title text;
  v_score integer;
  v_max integer;
  v_passed boolean;
  v_started_at timestamptz;
  v_finished_at timestamptz;

  v_snapshot_count integer;
  v_snapshot_max integer;

  v_answer_count integer;
  v_answered_count integer;
  v_correct_count integer;
  v_partial_count integer;
  v_wrong_count integer;
  v_unanswered_count integer;
  v_answer_score integer;
  v_answer_max integer;
  v_point_mismatch_count integer;
  v_invalid_unanswered_count integer;
begin
  v_auth_user_id := auth.uid();

  if v_auth_user_id is null then
    raise exception 'Ergebnisabruf erfordert eine Anmeldung.'
      using errcode = '28000';
  end if;

  if p_exam_attempt_id is null then
    raise exception 'Eine Prüfungsversuchs-ID ist erforderlich.'
      using errcode = '22004';
  end if;

  select
    ea.course_id,
    c.title,
    ea.score_points,
    ea.max_points,
    ea.passed,
    ea.started_at,
    ea.finished_at
  into
    v_course_id,
    v_course_title,
    v_score,
    v_max,
    v_passed,
    v_started_at,
    v_finished_at
  from public.exam_attempts ea
  join public.participants p
    on p.id = ea.participant_id
  left join public.courses c
    on c.id = ea.course_id
  where ea.id = p_exam_attempt_id
    and p.auth_user_id = v_auth_user_id
    and p.status in ('active', 'expired', 'completed')
    and ea.mode = 'full_simulation'
    and ea.finished_at is not null;

  if not found then
    raise exception
      'Abgeschlossenes eigenes Prüfungsergebnis wurde nicht gefunden.'
      using errcode = '42501';
  end if;

  select
    count(*)::integer,
    coalesce(sum(aq.max_points_snapshot), 0)::integer
  into
    v_snapshot_count,
    v_snapshot_max
  from public.exam_attempt_questions aq
  where aq.exam_attempt_id = p_exam_attempt_id;

  select
    count(*)::integer,

    count(*) filter (
      where jsonb_array_length(ans.selected_answers) > 0
    )::integer,

    count(*) filter (
      where ans.is_correct
    )::integer,

    count(*) filter (
      where jsonb_array_length(ans.selected_answers) > 0
        and not ans.is_correct
        and ans.earned_points > 0
    )::integer,

    count(*) filter (
      where jsonb_array_length(ans.selected_answers) > 0
        and not ans.is_correct
        and ans.earned_points = 0
    )::integer,

    count(*) filter (
      where jsonb_array_length(ans.selected_answers) = 0
    )::integer,

    coalesce(sum(ans.earned_points), 0)::integer,
    coalesce(sum(ans.max_points), 0)::integer,

    count(*) filter (
      where ans.max_points <> aq.max_points_snapshot
    )::integer,

    count(*) filter (
      where jsonb_array_length(ans.selected_answers) = 0
        and (
          ans.earned_points <> 0
          or ans.is_correct
        )
    )::integer

  into
    v_answer_count,
    v_answered_count,
    v_correct_count,
    v_partial_count,
    v_wrong_count,
    v_unanswered_count,
    v_answer_score,
    v_answer_max,
    v_point_mismatch_count,
    v_invalid_unanswered_count

  from public.exam_answers ans
  join public.exam_attempt_questions aq
    on aq.id = ans.attempt_question_id
   and aq.exam_attempt_id = ans.exam_attempt_id
  where ans.exam_attempt_id = p_exam_attempt_id;

  if v_snapshot_count <> 82
     or v_snapshot_max <> 120
     or v_answer_count <> 82
     or v_answer_max <> 120
     or v_max <> 120
     or v_score not between 0 and 120
     or v_answer_score <> v_score
     or v_passed <> (v_score >= 60)
     or v_point_mismatch_count <> 0
     or v_invalid_unanswered_count <> 0
     or v_answered_count + v_unanswered_count <> 82
     or (
       v_correct_count
       + v_partial_count
       + v_wrong_count
       + v_unanswered_count
     ) <> 82 then
    raise exception
      'Gespeichertes Prüfungsergebnis besitzt ungültige Ergebnisdaten.'
      using errcode = 'P0001';
  end if;

  return query
  select
    p_exam_attempt_id,
    v_course_id,
    v_course_title,
    v_score,
    v_max,
    v_passed,
    v_started_at,
    v_finished_at,
    v_answer_count,
    v_answered_count,
    v_correct_count,
    v_partial_count,
    v_wrong_count,
    v_unanswered_count;
end;
$$;

revoke all
on function public.accaoui_get_full_exam_result(uuid)
from public;

revoke all
on function public.accaoui_get_full_exam_result(uuid)
from anon;

revoke all
on function public.accaoui_get_full_exam_result(uuid)
from authenticated;

grant execute
on function public.accaoui_get_full_exam_result(uuid)
to authenticated;

-- Historische Ergebnisse bleiben nach Kursabschluss abrufbar.
-- Gesperrte Teilnehmer werden ausgeschlossen.
-- Keine Lösungsschlüssel, Erklärungen oder richtigen Indizes.
-- Keine Live-Ausführung in diesem Arbeitsschritt.
