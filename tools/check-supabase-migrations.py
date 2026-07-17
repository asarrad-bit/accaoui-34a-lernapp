from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

SCHEMA = "20260710_v2720b_mvp_schema.sql"
RLS = "20260710_v2721a_mvp_rls_policies.sql"
LOCKDOWN = "20260714_v2724b_exam_result_insert_lockdown.sql"
QUESTION_SCHEMA = "20260716_v2725c_exam_question_schema.sql"
QUESTION_RLS = "20260716_v2725d_exam_question_rls.sql"
ATTEMPT_KEY_SNAPSHOT = "20260716_v2726c_exam_attempt_answer_key_snapshot.sql"
GRADING_RULE_FIX = "20260716_v2726d_exam_attempt_grading_rule_partial_points.sql"
EXAM_ANSWERS_INTEGRITY = "20260716_v2726e_exam_answers_integrity.sql"
EXAM_START_RPC = "20260716_v2727a_exam_start_rpc.sql"
EXAM_ANSWER_SAVE_RPC = "20260716_v2727b_exam_answer_save_rpc.sql"
EXAM_FINISH_RPC = "20260716_v2727d_exam_finish_rpc.sql"
EXAM_SELECTION_LIMIT_SECURITY = "20260716_v2727e_exam_selection_limit_security.sql"
EXAM_RESULT_RPC = "20260717_v2727f_exam_result_rpc.sql"
EXAM_ATTEMPT_INTEGRITY = (
    "20260717_v2728b_exam_attempt_integrity.sql"
)
FULL_EXAM_STATE_INTEGRITY = (
    "20260717_v2728c_full_exam_state_integrity.sql"
)
EXAM_DIRECT_WRITE_LOCKDOWN = (
    "20260717_v2728d_exam_direct_write_lockdown.sql"
)
STAFF_ROLE_BOUNDARY = (
    "20260717_v2728e_staff_role_boundary.sql"
)

EXPECTED_TABLES = {
    "participants",
    "courses",
    "enrollments",
    "exam_attempts",
    "exam_answers",
    "certificates",
    "admin_profiles",
    "audit_logs",
}

QUESTION_TABLES = {
    "exam_questions",
    "exam_question_answer_keys",
    "exam_attempt_questions",
    "exam_attempt_question_answer_keys",
}


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


if not MIGRATIONS.is_dir():
    fail("Migrationsordner fehlt.")

files = sorted(p.name for p in MIGRATIONS.glob("*.sql"))

for required in (
    SCHEMA,
    RLS,
    LOCKDOWN,
    QUESTION_SCHEMA,
    QUESTION_RLS,
    ATTEMPT_KEY_SNAPSHOT,
    GRADING_RULE_FIX,
    EXAM_ANSWERS_INTEGRITY,
    EXAM_START_RPC,
    EXAM_ANSWER_SAVE_RPC,
    EXAM_FINISH_RPC,
    EXAM_SELECTION_LIMIT_SECURITY,
    EXAM_RESULT_RPC,
    EXAM_ATTEMPT_INTEGRITY,
    FULL_EXAM_STATE_INTEGRITY,
    EXAM_DIRECT_WRITE_LOCKDOWN,
    STAFF_ROLE_BOUNDARY,
):
    if required not in files:
        fail(f"Migration fehlt: {required}")

if files.index(SCHEMA) >= files.index(RLS):
    fail("RLS-Migration steht vor dem Grundschema.")

if files.index(RLS) >= files.index(LOCKDOWN):
    fail("Prüfungs-Lockdown steht vor der RLS-Migration.")

if files.index(LOCKDOWN) >= files.index(QUESTION_SCHEMA):
    fail("Fragen-Schema steht vor dem Prüfungs-Lockdown.")

if files.index(QUESTION_SCHEMA) >= files.index(QUESTION_RLS):
    fail("Fragen-RLS steht vor dem Fragen-Schema.")

if files.index(QUESTION_RLS) >= files.index(ATTEMPT_KEY_SNAPSHOT):
    fail("Versuchsschlüssel-Snapshot steht vor dem Fragen-RLS.")

if files.index(ATTEMPT_KEY_SNAPSHOT) >= files.index(GRADING_RULE_FIX):
    fail("Teilpunkte-Korrektur steht vor dem Versuchsschlüssel-Snapshot.")

if files.index(GRADING_RULE_FIX) >= files.index(EXAM_ANSWERS_INTEGRITY):
    fail("Antwortintegrität steht vor der Teilpunkte-Korrektur.")

if files.index(EXAM_ANSWERS_INTEGRITY) >= files.index(EXAM_START_RPC):
    fail("Prüfungsstart-RPC steht vor der Antwortintegrität.")

if files.index(EXAM_START_RPC) >= files.index(EXAM_ANSWER_SAVE_RPC):
    fail("Antwortspeicher-RPC steht vor dem Prüfungsstart-RPC.")

if files.index(EXAM_ANSWER_SAVE_RPC) >= files.index(EXAM_FINISH_RPC):
    fail("Prüfungsabschluss-RPC steht vor dem Antwortspeicher-RPC.")

if files.index(EXAM_FINISH_RPC) >= files.index(
    EXAM_SELECTION_LIMIT_SECURITY
):
    fail(
        "Auswahlbegrenzungs-Korrektur steht vor dem "
        "Prüfungsabschluss-RPC."
    )

if files.index(EXAM_SELECTION_LIMIT_SECURITY) >= files.index(
    EXAM_RESULT_RPC
):
    fail(
        "Ergebnisabruf-RPC steht vor der "
        "Auswahlbegrenzungs-Korrektur."
    )

if files.index(EXAM_RESULT_RPC) >= files.index(
    EXAM_ATTEMPT_INTEGRITY
):
    fail(
        "Prüfungsversuch-Integrität steht vor dem "
        "Ergebnisabruf-RPC."
    )

if files.index(EXAM_ATTEMPT_INTEGRITY) >= files.index(
    FULL_EXAM_STATE_INTEGRITY
):
    fail(
        "Vollsimulations-Zustandsintegrität steht vor der "
        "Prüfungsversuch-Integrität."
    )

if files.index(FULL_EXAM_STATE_INTEGRITY) >= files.index(
    EXAM_DIRECT_WRITE_LOCKDOWN
):
    fail(
        "Direkte Prüfungs-Schreibsperre steht vor der "
        "Vollsimulations-Zustandsintegrität."
    )

if files.index(EXAM_DIRECT_WRITE_LOCKDOWN) >= files.index(
    STAFF_ROLE_BOUNDARY
):
    fail(
        "Mitarbeiter-Rollentrennung steht vor der "
        "direkten Prüfungs-Schreibsperre."
    )

schema = (MIGRATIONS / SCHEMA).read_text(encoding="utf-8")
rls = (MIGRATIONS / RLS).read_text(encoding="utf-8")
lockdown = (MIGRATIONS / LOCKDOWN).read_text(encoding="utf-8")
question_schema = (
    MIGRATIONS / QUESTION_SCHEMA
).read_text(encoding="utf-8")
question_rls = (
    MIGRATIONS / QUESTION_RLS
).read_text(encoding="utf-8")
attempt_key_snapshot = (
    MIGRATIONS / ATTEMPT_KEY_SNAPSHOT
).read_text(encoding="utf-8")

grading_rule_fix = (
    MIGRATIONS / GRADING_RULE_FIX
).read_text(encoding="utf-8")

exam_answers_integrity = (
    MIGRATIONS / EXAM_ANSWERS_INTEGRITY
).read_text(encoding="utf-8")

exam_start_rpc = (
    MIGRATIONS / EXAM_START_RPC
).read_text(encoding="utf-8")

exam_answer_save_rpc = (
    MIGRATIONS / EXAM_ANSWER_SAVE_RPC
).read_text(encoding="utf-8")

exam_finish_rpc = (
    MIGRATIONS / EXAM_FINISH_RPC
).read_text(encoding="utf-8")

exam_selection_limit_security = (
    MIGRATIONS / EXAM_SELECTION_LIMIT_SECURITY
).read_text(encoding="utf-8")

exam_result_rpc = (
    MIGRATIONS / EXAM_RESULT_RPC
).read_text(encoding="utf-8")

exam_attempt_integrity = (
    MIGRATIONS / EXAM_ATTEMPT_INTEGRITY
).read_text(encoding="utf-8")

full_exam_state_integrity = (
    MIGRATIONS / FULL_EXAM_STATE_INTEGRITY
).read_text(encoding="utf-8")

exam_direct_write_lockdown = (
    MIGRATIONS / EXAM_DIRECT_WRITE_LOCKDOWN
).read_text(encoding="utf-8")

staff_role_boundary = (
    MIGRATIONS / STAFF_ROLE_BOUNDARY
).read_text(encoding="utf-8")

question_schema_bundle = (
    question_schema
    + "\n"
    + attempt_key_snapshot
    + "\n"
    + grading_rule_fix
)

tables = set(
    re.findall(
        r"create\s+table\s+if\s+not\s+exists\s+([a-z_]+)",
        schema,
        flags=re.IGNORECASE,
    )
)

missing_tables = EXPECTED_TABLES - tables
if missing_tables:
    fail(f"Tabellen fehlen: {sorted(missing_tables)}")

for table in EXPECTED_TABLES:
    pattern = rf"alter\s+table\s+{table}\s+enable\s+row\s+level\s+security"
    if not re.search(pattern, schema, flags=re.IGNORECASE):
        fail(f"RLS-Aktivierung fehlt für: {table}")

question_tables = set(
    re.findall(
        r"create\s+table\s+if\s+not\s+exists\s+([a-z_]+)",
        question_schema_bundle,
        flags=re.IGNORECASE,
    )
)

missing_question_tables = QUESTION_TABLES - question_tables
if missing_question_tables:
    fail(
        f"Sichere Prüfungstabellen fehlen: "
        f"{sorted(missing_question_tables)}"
    )

unexpected_question_tables = question_tables - QUESTION_TABLES
if unexpected_question_tables:
    fail(
        f"Unerwartete Prüfungstabellen: "
        f"{sorted(unexpected_question_tables)}"
    )

for table in QUESTION_TABLES:
    pattern = rf"alter\s+table\s+{table}\s+enable\s+row\s+level\s+security"
    if not re.search(
        pattern,
        question_schema_bundle,
        flags=re.IGNORECASE,
    ):
        fail(f"RLS-Aktivierung fehlt für Prüfungstabelle: {table}")

question_schema_lower = question_schema_bundle.lower()
question_schema_compact = re.sub(
    r"\s+",
    " ",
    question_schema_lower,
)

required_question_markers = (
    "unique (source_question_id, version)",
    "unique (exam_attempt_id, display_order)",
    "unique (exam_attempt_id, question_id)",
    "jsonb_typeof(answer_options) = 'array'",
    "jsonb_typeof(correct_answers) = 'array'",
    "jsonb_typeof(answer_options_snapshot) = 'array'",
    "jsonb_typeof(correct_answers_snapshot) = 'array'",
    "references exam_attempt_questions(id) on delete cascade",
    "drop constraint if exists exam_attempt_question_answer_keys_grading_rule_check",
    "alter column grading_rule",
    "set default 'per_correct_selection_no_penalty'",
    "set grading_rule = 'per_correct_selection_no_penalty'",
    "where grading_rule = 'exact_set'",
    "grading_rule in ('per_correct_selection_no_penalty')",
    "revoke all on table exam_attempt_question_answer_keys",
    "question_type in ('single', 'multiple', 'praxisfall', 'combination')",
    "question_type_snapshot in ('single', 'multiple', 'praxisfall', 'combination')",
    "revoke all on table exam_question_answer_keys",
)

for marker in required_question_markers:
    if marker not in question_schema_compact:
        fail(f"Fragen-Schema-Anweisung fehlt: {marker}")

if "create policy" in question_schema_lower:
    fail("Fragen-Schema darf noch keine RLS-Policy erstellen.")

attempt_key_snapshot_lower = attempt_key_snapshot.lower()

if "create policy" in attempt_key_snapshot_lower:
    fail("Privater Versuchsschlüssel darf keine Direktpolicy erhalten.")

if "grant " in attempt_key_snapshot_lower:
    fail("Privater Versuchsschlüssel darf keinen Direktgrant erhalten.")

grading_rule_fix_lower = grading_rule_fix.lower()

if "create policy" in grading_rule_fix_lower:
    fail("Teilpunkte-Korrektur darf keine Policy erstellen.")

if "grant " in grading_rule_fix_lower:
    fail("Teilpunkte-Korrektur darf keinen Grant erstellen.")

exam_answers_integrity_lower = exam_answers_integrity.lower()
exam_answers_integrity_compact = re.sub(
    r"\s+",
    " ",
    exam_answers_integrity_lower,
)

required_answer_integrity_markers = (
    "if exists (select 1 from exam_answers limit 1)",
    "unique (id, exam_attempt_id)",
    "add column if not exists attempt_question_id uuid",
    "drop column if exists correct_answers",
    "drop column if exists question_id",
    "alter column attempt_question_id set not null",
    "alter column max_points drop default",
    "unique (attempt_question_id)",
    "foreign key (attempt_question_id, exam_attempt_id)",
    "references exam_attempt_questions(id, exam_attempt_id) on delete cascade",
    "jsonb_typeof(selected_answers) = 'array'",
    "max_points in (1, 2)",
    "earned_points between 0 and max_points",
    "not is_correct or earned_points = max_points",
    "revoke insert, update, delete on table exam_answers "
    "from public, anon, authenticated",
)

for marker in required_answer_integrity_markers:
    if marker not in exam_answers_integrity_compact:
        fail(f"Antwortintegritäts-Anweisung fehlt: {marker}")

if "alter table exam column" in exam_answers_integrity_compact:
    fail("Ungültige ALTER-TABLE-Anweisung in Antwortintegrität gefunden.")

if (
    exam_answers_integrity_compact.count(
        "add column if not exists attempt_question_id uuid"
    )
    != 1
):
    fail("attempt_question_id muss genau einmal ergänzt werden.")

if (
    exam_answers_integrity_compact.count(
        "drop column if exists correct_answers"
    )
    != 1
):
    fail("correct_answers muss genau einmal entfernt werden.")

if "create policy" in exam_answers_integrity_lower:
    fail("Antwortintegrität darf keine neue RLS-Policy erstellen.")

if "grant " in exam_answers_integrity_lower:
    fail("Antwortintegrität darf keine Direktrechte vergeben.")

exam_start_rpc_lower = exam_start_rpc.lower()
exam_start_rpc_compact = re.sub(
    r"\s+",
    " ",
    exam_start_rpc_lower,
)

required_exam_start_markers = (
    "uq_exam_attempts_open_full_simulation",
    "function public.accaoui_start_full_exam(",
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "v_auth_user_id := auth.uid()",
    "p.status = 'active'",
    "pg_catalog.pg_advisory_xact_lock(",
    "c.status = 'active'",
    "e.access_status = 'allowed'",
    "ea.finished_at is null",
    "for share of q, k",
    "v_question_count <> 82 or v_max_points <> 120",
    "insert into public.exam_attempts (",
    "insert into public.exam_attempt_questions (",
    "insert into public.exam_attempt_question_answer_keys (",
    "'per_correct_selection_no_penalty'",
    "v_inserted_questions <> 82",
    "v_inserted_keys <> 82",
    "grant execute on function "
    "public.accaoui_start_full_exam(uuid) to authenticated",
)

for marker in required_exam_start_markers:
    if marker not in exam_start_rpc_compact:
        fail(f"Prüfungsstart-RPC-Anweisung fehlt: {marker}")

return_match = re.search(
    r"returns\s+table\s*\((.*?)\)\s*language\s+plpgsql",
    exam_start_rpc,
    flags=re.IGNORECASE | re.DOTALL,
)

if not return_match:
    fail("Rückgabestruktur des Prüfungsstart-RPC fehlt.")

return_columns = re.sub(
    r"\s+",
    " ",
    return_match.group(1).strip().lower(),
)

expected_return_columns = (
    "exam_attempt_id uuid, question_count integer, "
    "max_points integer, resumed boolean"
)

if return_columns != expected_return_columns:
    fail(
        "Prüfungsstart-RPC gibt unerwartete Spalten zurück: "
        f"{return_columns}"
    )

if "p_participant_id" in exam_start_rpc_lower:
    fail("Teilnehmer-ID darf nicht als RPC-Parameter übergeben werden.")

for forbidden in (
    "create policy",
    "grant select",
    "grant insert",
    "grant update",
    "grant delete",
):
    if forbidden in exam_start_rpc_lower:
        fail(f"Unzulässige Prüfungsstart-RPC-Anweisung: {forbidden}")

exam_answer_save_rpc_lower = exam_answer_save_rpc.lower()
exam_answer_save_rpc_compact = re.sub(
    r"\s+",
    " ",
    exam_answer_save_rpc_lower,
)

required_answer_save_markers = (
    "function public.accaoui_save_exam_answer(",
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "v_auth_user_id := auth.uid()",
    "jsonb_typeof(p_selected_answers) <> 'array'",
    "and p.auth_user_id = v_auth_user_id",
    "and p.status = 'active'",
    "and ea.mode = 'full_simulation'",
    "and ea.finished_at is null",
    "for update of aq, ea",
    "c.status = 'active'",
    "e.access_status = 'allowed'",
    "e.access_starts_at is null",
    "e.access_ends_at is null",
    "aq.question_type_snapshot",
    "v_question_type in ('single', 'combination')",
    "v_answer_count > 1",
    "v_answer_count > v_option_count",
    "(item.value #>> '{}') !~ '^[0-9]+$'",
    "(item.value #>> '{}')::integer >= v_option_count",
    "count(distinct item.value #>> '{}')",
    "jsonb_agg(",
    "insert into public.exam_answers (",
    "on conflict (attempt_question_id)",
    "selected_answers = excluded.selected_answers",
    "earned_points = 0",
    "max_points = excluded.max_points",
    "is_correct = false",
    "revoke all on function "
    "public.accaoui_save_exam_answer(uuid, jsonb) from public",
    "revoke all on function "
    "public.accaoui_save_exam_answer(uuid, jsonb) from anon",
    "revoke all on function "
    "public.accaoui_save_exam_answer(uuid, jsonb) from authenticated",
    "grant execute on function "
    "public.accaoui_save_exam_answer(uuid, jsonb) to authenticated",
)

for marker in required_answer_save_markers:
    if marker not in exam_answer_save_rpc_compact:
        fail(f"Antwortspeicher-RPC-Anweisung fehlt: {marker}")

if "v_answer_count > v_max_points" in exam_answer_save_rpc_compact:
    fail(
        "Antwortanzahl darf nicht durch die erreichbaren Punkte "
        "begrenzt werden."
    )

signature_match = re.search(
    r"function\s+public\.accaoui_save_exam_answer\s*"
    r"\((.*?)\)\s*returns",
    exam_answer_save_rpc,
    flags=re.IGNORECASE | re.DOTALL,
)

if not signature_match:
    fail("Funktionsparameter des Antwortspeicher-RPC fehlen.")

signature_parameters = re.sub(
    r"\s+",
    " ",
    signature_match.group(1).strip().lower(),
)

expected_parameters = (
    "p_attempt_question_id uuid, "
    "p_selected_answers jsonb"
)

if signature_parameters != expected_parameters:
    fail(
        "Antwortspeicher-RPC besitzt unerwartete Parameter: "
        f"{signature_parameters}"
    )

return_match = re.search(
    r"returns\s+table\s*\((.*?)\)\s*language\s+plpgsql",
    exam_answer_save_rpc,
    flags=re.IGNORECASE | re.DOTALL,
)

if not return_match:
    fail("Rückgabestruktur des Antwortspeicher-RPC fehlt.")

return_columns = re.sub(
    r"\s+",
    " ",
    return_match.group(1).strip().lower(),
)

expected_return_columns = (
    "attempt_question_id uuid, "
    "selected_answers jsonb, "
    "saved boolean"
)

if return_columns != expected_return_columns:
    fail(
        "Antwortspeicher-RPC gibt unerwartete Spalten zurück: "
        f"{return_columns}"
    )

for forbidden_parameter in (
    "p_exam_attempt_id",
    "p_earned_points",
    "p_max_points",
    "p_is_correct",
    "p_correct_answers",
):
    if forbidden_parameter in signature_parameters:
        fail(
            "Verbotener Browserparameter im Antwortspeicher-RPC: "
            f"{forbidden_parameter}"
        )

for forbidden_content in (
    "exam_question_answer_keys",
    "exam_attempt_question_answer_keys",
    "score_points",
    "passed",
    "create policy",
    "grant select",
    "grant insert",
    "grant update",
    "grant delete",
):
    if forbidden_content in exam_answer_save_rpc_lower:
        fail(
            "Unzulässiger Inhalt im Antwortspeicher-RPC: "
            f"{forbidden_content}"
        )

exam_finish_rpc_lower = exam_finish_rpc.lower()
exam_finish_rpc_compact = re.sub(
    r"\s+",
    " ",
    exam_finish_rpc_lower,
)

required_exam_finish_markers = (
    "function public.accaoui_finish_full_exam(",
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "v_auth_user_id := auth.uid()",
    "and p.auth_user_id = v_auth_user_id",
    "and p.status = 'active'",
    "and ea.mode = 'full_simulation'",
    "for update of ea",
    "v_recorded_finished_at is not null",
    "c.status = 'active'",
    "e.access_status = 'allowed'",
    "v_snapshot_count <> 82",
    "v_key_count <> 82",
    "v_rule_count <> 82",
    "v_snapshot_max <> 120",
    "insert into public.exam_answers (",
    "'[]'::jsonb",
    "on conflict (attempt_question_id) do nothing",
    "with grades as (",
    "jsonb_array_elements_text(",
    "correct_answers_snapshot",
    "when g.is_exact then g.question_max_points",
    "else least(",
    "update public.exam_answers ans",
    "earned_points = calculated.earned_points",
    "is_correct = calculated.is_exact",
    "v_graded_count <> 82",
    "score_points = v_score",
    "passed = (v_score >= 60)",
    "finished_at = v_finished_at",
    "revoke all on function "
    "public.accaoui_finish_full_exam(uuid) from public",
    "revoke all on function "
    "public.accaoui_finish_full_exam(uuid) from anon",
    "revoke all on function "
    "public.accaoui_finish_full_exam(uuid) from authenticated",
    "grant execute on function "
    "public.accaoui_finish_full_exam(uuid) to authenticated",
)

for marker in required_exam_finish_markers:
    if marker not in exam_finish_rpc_compact:
        fail(f"Prüfungsabschluss-RPC-Anweisung fehlt: {marker}")

signature_match = re.search(
    r"function\s+public\.accaoui_finish_full_exam\s*"
    r"\((.*?)\)\s*returns",
    exam_finish_rpc,
    flags=re.IGNORECASE | re.DOTALL,
)

if not signature_match:
    fail("Funktionsparameter des Prüfungsabschluss-RPC fehlen.")

signature_parameters = re.sub(
    r"\s+",
    " ",
    signature_match.group(1).strip().lower(),
)

if signature_parameters != "p_exam_attempt_id uuid":
    fail(
        "Prüfungsabschluss-RPC besitzt unerwartete Parameter: "
        f"{signature_parameters}"
    )

return_match = re.search(
    r"returns\s+table\s*\((.*?)\)\s*language\s+plpgsql",
    exam_finish_rpc,
    flags=re.IGNORECASE | re.DOTALL,
)

if not return_match:
    fail("Rückgabestruktur des Prüfungsabschluss-RPC fehlt.")

return_columns = re.sub(
    r"\s+",
    " ",
    return_match.group(1).strip().lower(),
)

expected_return_columns = (
    "exam_attempt_id uuid, "
    "answered_questions integer, "
    "correct_questions integer, "
    "score_points integer, "
    "max_points integer, "
    "passed boolean, "
    "finished_at timestamptz, "
    "already_finished boolean"
)

if return_columns != expected_return_columns:
    fail(
        "Prüfungsabschluss-RPC gibt unerwartete Spalten zurück: "
        f"{return_columns}"
    )

for forbidden_parameter in (
    "p_selected_answers",
    "p_score_points",
    "p_max_points",
    "p_passed",
    "p_earned_points",
    "p_is_correct",
    "p_correct_answers",
):
    if forbidden_parameter in signature_parameters:
        fail(
            "Verbotener Browserparameter im Prüfungsabschluss-RPC: "
            f"{forbidden_parameter}"
        )

for forbidden_content in (
    "public.exam_question_answer_keys",
    "create policy",
    "grant select",
    "grant insert",
    "grant update",
    "grant delete",
):
    if forbidden_content in exam_finish_rpc_lower:
        fail(
            "Unzulässiger Inhalt im Prüfungsabschluss-RPC: "
            f"{forbidden_content}"
        )

selection_security_lower = exam_selection_limit_security.lower()
selection_security_compact = re.sub(
    r"\s+",
    " ",
    selection_security_lower,
)

required_selection_security_markers = (
    "function public.accaoui_save_exam_answer(",
    "function public.accaoui_finish_full_exam(",
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "v_selection_limit integer",
    "join public.exam_attempt_question_answer_keys ak",
    "jsonb_array_length(ak.correct_answers_snapshot)",
    "v_selection_limit < 1",
    "v_selection_limit > v_option_count",
    "v_answer_count > v_selection_limit",
    "es wurden zu viele antworten ausgewählt",
    "ungültige oder überhöhte auswahlen dürfen niemals bewertet werden",
    "jsonb_array_length(ans.selected_answers) > "
    "jsonb_array_length(ak.correct_answers_snapshot)",
    "mindestens eine prüfungsantwort enthält zu viele auswahlen",
    "grant execute on function "
    "public.accaoui_save_exam_answer(uuid, jsonb) to authenticated",
    "grant execute on function "
    "public.accaoui_finish_full_exam(uuid) to authenticated",
)

for marker in required_selection_security_markers:
    if marker not in selection_security_compact:
        fail(f"Auswahlbegrenzungs-Anweisung fehlt: {marker}")

if selection_security_lower.count(
    "create or replace function public.accaoui_save_exam_answer("
) != 1:
    fail("Antwortspeicher-Funktion muss genau einmal ersetzt werden.")

if selection_security_lower.count(
    "create or replace function public.accaoui_finish_full_exam("
) != 1:
    fail("Abschlussfunktion muss genau einmal ersetzt werden.")

if selection_security_compact.count("security definer") != 2:
    fail("Beide korrigierten Funktionen müssen Security Definer sein.")

if selection_security_compact.count(
    "set search_path = pg_catalog, public"
) != 2:
    fail("Beide korrigierten Funktionen brauchen festen search_path.")

if selection_security_compact.count("set row_security = off") != 2:
    fail("Beide korrigierten Funktionen brauchen row_security=off.")

if "v_answer_count > v_max_points" in selection_security_compact:
    fail("Punktewert darf die Auswahlzahl nicht begrenzen.")

save_match = re.search(
    r"function\s+public\.accaoui_save_exam_answer\s*"
    r"\((.*?)\)\s*returns\s+table\s*"
    r"\((.*?)\)\s*language\s+plpgsql",
    exam_selection_limit_security,
    flags=re.IGNORECASE | re.DOTALL,
)

if not save_match:
    fail("Korrigierte Antwortspeicher-Signatur fehlt.")

save_parameters = re.sub(
    r"\s+",
    " ",
    save_match.group(1).strip().lower(),
)
save_returns = re.sub(
    r"\s+",
    " ",
    save_match.group(2).strip().lower(),
)

if save_parameters != (
    "p_attempt_question_id uuid, p_selected_answers jsonb"
):
    fail(f"Unerwartete Antwortspeicher-Parameter: {save_parameters}")

if save_returns != (
    "attempt_question_id uuid, selected_answers jsonb, saved boolean"
):
    fail(f"Unerwartete Antwortspeicher-Rückgabe: {save_returns}")

finish_match = re.search(
    r"function\s+public\.accaoui_finish_full_exam\s*"
    r"\((.*?)\)\s*returns\s+table\s*"
    r"\((.*?)\)\s*language\s+plpgsql",
    exam_selection_limit_security,
    flags=re.IGNORECASE | re.DOTALL,
)

if not finish_match:
    fail("Korrigierte Abschlussfunktions-Signatur fehlt.")

finish_parameters = re.sub(
    r"\s+",
    " ",
    finish_match.group(1).strip().lower(),
)
finish_returns = re.sub(
    r"\s+",
    " ",
    finish_match.group(2).strip().lower(),
)

if finish_parameters != "p_exam_attempt_id uuid":
    fail(f"Unerwartete Abschlussparameter: {finish_parameters}")

expected_finish_returns = (
    "exam_attempt_id uuid, answered_questions integer, "
    "correct_questions integer, score_points integer, "
    "max_points integer, passed boolean, "
    "finished_at timestamptz, already_finished boolean"
)

if finish_returns != expected_finish_returns:
    fail(f"Unerwartete Abschlussrückgabe: {finish_returns}")

for forbidden in (
    "create policy",
    "grant select",
    "grant insert",
    "grant update",
    "grant delete",
    "service_role",
):
    if forbidden in selection_security_lower:
        fail(f"Unzulässiger Inhalt in v27.27e: {forbidden}")

exam_result_rpc_lower = exam_result_rpc.lower()
exam_result_rpc_compact = re.sub(
    r"\s+",
    " ",
    exam_result_rpc_lower,
)

required_exam_result_markers = (
    "function public.accaoui_get_full_exam_result(",
    "language plpgsql",
    "stable",
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "v_auth_user_id := auth.uid()",
    "and p.auth_user_id = v_auth_user_id",
    "p.status in ('active', 'expired', 'completed')",
    "and ea.mode = 'full_simulation'",
    "and ea.finished_at is not null",
    "v_snapshot_count <> 82",
    "v_snapshot_max <> 120",
    "v_answer_count <> 82",
    "v_answer_max <> 120",
    "v_score not between 0 and 120",
    "v_answer_score <> v_score",
    "v_passed <> (v_score >= 60)",
    "v_point_mismatch_count <> 0",
    "v_invalid_unanswered_count <> 0",
    "v_answered_count + v_unanswered_count <> 82",
    "v_correct_count + v_partial_count + v_wrong_count "
    "+ v_unanswered_count ) <> 82",
    "revoke all on function "
    "public.accaoui_get_full_exam_result(uuid) from public",
    "revoke all on function "
    "public.accaoui_get_full_exam_result(uuid) from anon",
    "revoke all on function "
    "public.accaoui_get_full_exam_result(uuid) from authenticated",
    "grant execute on function "
    "public.accaoui_get_full_exam_result(uuid) to authenticated",
)

for marker in required_exam_result_markers:
    if marker not in exam_result_rpc_compact:
        fail(f"Ergebnisabruf-RPC-Anweisung fehlt: {marker}")

result_match = re.search(
    r"function\s+public\.accaoui_get_full_exam_result\s*"
    r"\((.*?)\)\s*returns\s+table\s*"
    r"\((.*?)\)\s*language\s+plpgsql",
    exam_result_rpc,
    flags=re.IGNORECASE | re.DOTALL,
)

if not result_match:
    fail("Signatur des Ergebnisabruf-RPC fehlt.")

result_parameters = re.sub(
    r"\s+",
    " ",
    result_match.group(1).strip().lower(),
)

if result_parameters != "p_exam_attempt_id uuid":
    fail(
        "Ergebnisabruf-RPC besitzt unerwartete Parameter: "
        f"{result_parameters}"
    )

result_returns = re.sub(
    r"\s+",
    " ",
    result_match.group(2).strip().lower(),
)

expected_result_returns = (
    "exam_attempt_id uuid, course_id uuid, course_title text, "
    "score_points integer, max_points integer, passed boolean, "
    "started_at timestamptz, finished_at timestamptz, "
    "total_questions integer, answered_questions integer, "
    "correct_questions integer, partial_questions integer, "
    "wrong_questions integer, unanswered_questions integer"
)

if result_returns != expected_result_returns:
    fail(
        "Ergebnisabruf-RPC gibt unerwartete Spalten zurück: "
        f"{result_returns}"
    )

for forbidden_parameter in (
    "p_participant_id",
    "p_score_points",
    "p_max_points",
    "p_passed",
    "p_correct_answers",
    "p_selected_answers",
):
    if forbidden_parameter in result_parameters:
        fail(
            "Verbotener Browserparameter im Ergebnisabruf-RPC: "
            f"{forbidden_parameter}"
        )

for forbidden_content in (
    "exam_question_answer_keys",
    "exam_attempt_question_answer_keys",
    "correct_answers_snapshot",
    "explanation_snapshot",
    "answer_hash_snapshot",
    "insert into",
    "update public.",
    "delete from",
    "create policy",
    "grant select",
    "grant insert",
    "grant update",
    "grant delete",
    "service_role",
):
    if forbidden_content in exam_result_rpc_lower:
        fail(
            "Unzulässiger Inhalt im Ergebnisabruf-RPC: "
            f"{forbidden_content}"
        )

exam_attempt_integrity_lower = (
    exam_attempt_integrity.lower()
)
exam_attempt_integrity_compact = re.sub(
    r"\s+",
    " ",
    exam_attempt_integrity_lower,
)

required_exam_attempt_integrity_markers = (
    "where score_points > max_points",
    "where finished_at is not null",
    "started_at is null",
    "finished_at < started_at",
    "drop constraint if exists "
    "exam_attempts_score_within_max_check",
    "add constraint exam_attempts_score_within_max_check",
    "check (score_points <= max_points)",
    "drop constraint if exists "
    "exam_attempts_finished_after_started_check",
    "add constraint "
    "exam_attempts_finished_after_started_check",
    "finished_at >= started_at",
)

for marker in required_exam_attempt_integrity_markers:
    if marker not in exam_attempt_integrity_compact:
        fail(
            "Prüfungsversuch-Integritätsanweisung fehlt: "
            f"{marker}"
        )

for forbidden in (
    "create policy",
    "grant ",
    "service_role",
    "insert into",
    "update public.",
    "delete from",
):
    if forbidden in exam_attempt_integrity_lower:
        fail(
            "Unzulässiger Inhalt in "
            f"Prüfungsversuch-Integrität: {forbidden}"
        )


full_exam_state_integrity_lower = (
    full_exam_state_integrity.lower()
)
full_exam_state_integrity_compact = re.sub(
    r"\s+",
    " ",
    full_exam_state_integrity_lower,
)

required_full_exam_state_markers = (
    "where mode = 'full_simulation'",
    "max_points <> 120",
    "started_at is null",
    "score_points <> 0",
    "finished_at is not null",
    "passed <> (score_points >= 60)",
    "drop constraint if exists "
    "exam_attempts_full_simulation_state_check",
    "add constraint "
    "exam_attempts_full_simulation_state_check",
    "mode <> 'full_simulation'",
    "max_points = 120",
    "started_at is not null",
    "finished_at is null",
    "score_points = 0",
    "not passed",
    "passed = (score_points >= 60)",
)

for marker in required_full_exam_state_markers:
    if marker not in full_exam_state_integrity_compact:
        fail(
            "Vollsimulations-Zustandsanweisung fehlt: "
            f"{marker}"
        )

if full_exam_state_integrity_lower.count(
    "add constraint "
    "exam_attempts_full_simulation_state_check"
) != 1:
    fail(
        "Vollsimulations-Zustandsconstraint muss "
        "genau einmal ergänzt werden."
    )

for forbidden in (
    "create policy",
    "grant ",
    "service_role",
    "insert into",
    "update public.",
    "delete from",
):
    if forbidden in full_exam_state_integrity_lower:
        fail(
            "Unzulässiger Inhalt in "
            f"Vollsimulations-Zustandsintegrität: {forbidden}"
        )


exam_direct_write_lockdown_lower = (
    exam_direct_write_lockdown.lower()
)
exam_direct_write_lockdown_compact = re.sub(
    r"\s+",
    " ",
    exam_direct_write_lockdown_lower,
)

required_exam_direct_write_lockdown_markers = (
    'drop policy if exists "exam_attempts_staff_manage" '
    "on public.exam_attempts",
    'drop policy if exists "exam_answers_staff_manage" '
    "on public.exam_answers",
    "revoke insert, update, delete "
    "on table public.exam_attempts "
    "from public, anon, authenticated",
    "revoke insert, update, delete "
    "on table public.exam_answers "
    "from public, anon, authenticated",
)

for marker in required_exam_direct_write_lockdown_markers:
    if marker not in exam_direct_write_lockdown_compact:
        fail(
            "Direkte Prüfungs-Schreibsperre fehlt: "
            f"{marker}"
        )

for forbidden in (
    "create policy",
    "grant ",
    "service_role",
    "insert into",
    "update public.",
    "delete from",
):
    if forbidden in exam_direct_write_lockdown_lower:
        fail(
            "Unzulässiger Inhalt in direkter "
            f"Prüfungs-Schreibsperre: {forbidden}"
        )


staff_role_boundary_lower = staff_role_boundary.lower()
staff_role_boundary_compact = re.sub(
    r"\s+",
    " ",
    staff_role_boundary_lower,
)

required_staff_role_markers = (
    "function public.accaoui_is_active_staff()",
    "function public.accaoui_is_admin_or_dozent()",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "revoke all on function "
    "public.accaoui_is_active_staff() from public",
    "revoke all on function "
    "public.accaoui_is_active_staff() from anon",
    "grant execute on function "
    "public.accaoui_is_active_staff() to authenticated",
    "revoke all on function "
    "public.accaoui_is_admin_or_dozent() from public",
    "revoke all on function "
    "public.accaoui_is_admin_or_dozent() from anon",
    "grant execute on function "
    "public.accaoui_is_admin_or_dozent() to authenticated",
)

for marker in required_staff_role_markers:
    if marker not in staff_role_boundary_compact:
        fail(
            "Mitarbeiter-Rollentrennung fehlt: "
            f"{marker}"
        )


def get_role_helper_body(function_name: str) -> str:
    match = re.search(
        rf"function\s+public\.{function_name}\s*"
        rf"\(\)\s*returns\s+boolean.*?"
        rf"as\s+\$\$(.*?)\$\$;",
        staff_role_boundary,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        fail(f"Rollen-Helper fehlt: {function_name}")

    return re.sub(
        r"\s+",
        " ",
        match.group(1).strip().lower(),
    )


active_staff_body = get_role_helper_body(
    "accaoui_is_active_staff"
)
admin_dozent_body = get_role_helper_body(
    "accaoui_is_admin_or_dozent"
)

if "ap.role in ('admin', 'dozent', 'support')" not in active_staff_body:
    fail("Aktiver Mitarbeiter-Helper enthält nicht alle Leserollen.")

if "ap.role in ('admin', 'dozent')" not in admin_dozent_body:
    fail("Admin-/Dozent-Helper enthält nicht beide Verwaltungsrollen.")

if "'support'" in admin_dozent_body:
    fail("Support darf keine Verwaltungsrolle besitzen.")

expected_staff_select_policies = {
    ("participants_select_own_or_staff", "participants"),
    ("courses_select_authenticated", "courses"),
    ("enrollments_select_own_or_staff", "enrollments"),
    ("exam_attempts_select_own_or_staff", "exam_attempts"),
    ("exam_answers_select_own_or_staff", "exam_answers"),
    ("certificates_select_own_or_staff", "certificates"),
}

staff_select_policies = set(
    re.findall(
        r'create\s+policy\s+"([^"]+)"\s+'
        r'on\s+public\.([a-z_]+)\s+for\s+select',
        staff_role_boundary,
        flags=re.IGNORECASE,
    )
)

if staff_select_policies != expected_staff_select_policies:
    fail(
        "Unerwartete Mitarbeiter-Select-Policies: "
        f"{sorted(staff_select_policies)}"
    )

for policy_name, table_name in expected_staff_select_policies:
    policy_match = re.search(
        rf'create\s+policy\s+"{re.escape(policy_name)}"\s+'
        rf'on\s+public\.{re.escape(table_name)}\s+'
        rf'for\s+select\s+to\s+authenticated\s+'
        rf'using\s*\((.*?)\);',
        staff_role_boundary,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not policy_match:
        fail(
            "Mitarbeiter-Select-Policy fehlt oder ist nicht "
            f"rein lesend: {policy_name}"
        )

    if "public.accaoui_is_active_staff()" not in (
        policy_match.group(1).lower()
    ):
        fail(
            "Mitarbeiter-Select-Policy verwendet nicht den "
            f"reinen Lese-Helper: {policy_name}"
        )

for forbidden in (
    "for all",
    "for insert",
    "for update",
    "for delete",
    "grant select",
    "grant insert",
    "grant update",
    "grant delete",
    "service_role",
):
    if forbidden in staff_role_boundary_lower:
        fail(
            "Unzulässiger Inhalt in Mitarbeiter-Rollentrennung: "
            f"{forbidden}"
        )


question_rls_lower = question_rls.lower()

expected_question_policies = {
    (
        "exam_questions_content_manager_manage",
        "exam_questions",
    ),
    (
        "exam_question_answer_keys_content_manager_manage",
        "exam_question_answer_keys",
    ),
    (
        "exam_attempt_questions_select_own_or_content_manager",
        "exam_attempt_questions",
    ),
}

question_policies = set(
    re.findall(
        r'create\s+policy\s+"([^"]+)"\s+'
        r'on\s+(?:public\.)?([a-z_]+)',
        question_rls,
        flags=re.IGNORECASE,
    )
)

if question_policies != expected_question_policies:
    fail(
        f"Unerwartete Fragen-RLS-Policies: "
        f"{sorted(question_policies)}"
    )

required_rls_markers = (
    "public.accaoui_is_exam_content_manager()",
    "set search_path = pg_catalog, public",
    "ap.role in ('admin', 'dozent')",
    "grant execute",
    "grant select, insert, update, delete",
    "grant select\non table public.exam_attempt_questions",
)

for marker in required_rls_markers:
    if marker not in question_rls_lower:
        fail(f"Fragen-RLS-Anweisung fehlt: {marker}")

if "'support'" in question_rls_lower:
    fail("Support darf kein Prüfungsinhalts-Manager sein.")

attempt_policy_marker = (
    'create policy '
    '"exam_attempt_questions_select_own_or_content_manager"\n'
    "on public.exam_attempt_questions\n"
    "for select"
)

if attempt_policy_marker not in question_rls_lower:
    fail("Prüfungs-Snapshot-Policy ist nicht rein lesend.")

for forbidden_action in ("insert", "update", "delete"):
    pattern = (
        rf"on\s+(?:public\.)?exam_attempt_questions"
        rf"\s+for\s+{forbidden_action}"
    )
    if re.search(pattern, question_rls, flags=re.IGNORECASE):
        fail(
            "Teilnehmer-Schreibpolicy für Prüfungs-Snapshots gefunden: "
            f"{forbidden_action}"
        )

policies = re.findall(
    r'create\s+policy\s+"[^"]+"\s+on\s+([a-z_]+)',
    rls,
    flags=re.IGNORECASE,
)

if len(policies) != 17:
    fail(f"Erwartet: 17 Basis-Policies, gefunden: {len(policies)}")

required_drops = (
    'drop policy if exists "exam_attempts_insert_own"',
    'drop policy if exists "exam_answers_insert_own"',
)

for statement in required_drops:
    if statement not in lockdown.lower():
        fail(f"Lockdown-Anweisung fehlt: {statement}")

if "create policy" in lockdown.lower():
    fail("Lockdown darf keine neue Policy erstellen.")

direct_write_policy_drops = (
    'drop policy if exists "exam_attempts_staff_manage"',
    'drop policy if exists "exam_answers_staff_manage"',
)

for statement in direct_write_policy_drops:
    if statement not in exam_direct_write_lockdown_lower:
        fail(
            "Direkte Mitarbeiter-Schreibpolicy nicht entfernt: "
            f"{statement}"
        )

effective_policy_count = (
    len(policies)
    - len(required_drops)
    - len(direct_write_policy_drops)
)

if effective_policy_count != 13:
    fail(
        f"Erwartet: 13 effektive Policies, gefunden: "
        f"{effective_policy_count}"
    )

unknown_policy_tables = set(policies) - EXPECTED_TABLES
if unknown_policy_tables:
    fail(f"Policies verweisen auf unbekannte Tabellen: {sorted(unknown_policy_tables)}")

if rls.count("create or replace function public.accaoui_is_") != 2:
    fail("Die zwei Rollen-Helper-Funktionen fehlen oder sind doppelt.")

if len(re.findall(r"\bto\s+authenticated\b", rls, flags=re.IGNORECASE)) != 17:
    fail("Nicht alle 17 Policies sind auf authenticated begrenzt.")

if "auth.uid()" not in rls:
    fail("auth.uid()-Prüfung fehlt.")

all_sql = "\n".join(
    (MIGRATIONS / name).read_text(encoding="utf-8")
    for name in files
)

sql_without_comments = re.sub(
    r"--.*?$",
    "",
    all_sql,
    flags=re.MULTILINE,
)
for forbidden in ("service_role", "SUPABASE_SERVICE_ROLE_KEY", "postgresql://", "postgres://"):
    if forbidden.lower() in sql_without_comments.lower():
        fail(f"Verbotener sensitiver Inhalt gefunden: {forbidden}")

print("Supabase-Migrationsprüfung: OK")
print(f"SQL-Dateien: {len(files)}")
print(f"MVP-Tabellen: {len(EXPECTED_TABLES)}")
print(f"Sichere Prüfungstabellen: {len(QUESTION_TABLES)}")
print(
    f"Tabellen gesamt: "
    f"{len(EXPECTED_TABLES) + len(QUESTION_TABLES)}"
)
print(f"Basis-RLS-Policies: {len(policies)}")
print(f"Effektive RLS-Policies: {effective_policy_count}")
print(f"Fragen-RLS-Policies: {len(question_policies)}")
print(
    f"Effektive Policies gesamt: "
    f"{effective_policy_count + len(question_policies)}"
)
print("Direkte Prüfungs-Inserts für Teilnehmer: gesperrt")
print("Prüfungsinhalte: nur Admin/Dozent verwaltbar")
print("Prüfungs-Snapshots: Teilnehmer nur lesend für eigene Versuche")
print("Private Versuchsschlüssel: direkter Zugriff vollständig gesperrt")
print("Bewertungsregel: Teilpunkte ohne Punktabzug")
print("Antwortspeicher: private Lösungsschlüssel entfernt")
print("Antwortzuordnung: eindeutig und versuchsgebunden")
print("Prüfungsantworten: nur RPC-Schreibzugriff")
print("Prüfungsstart-RPC: atomar und idempotent vorbereitet")
print("Prüfungsstart-RPC: 82 Fragen und 120 Punkte erzwungen")
print("Prüfungsstart-RPC: keine Lösungsschlüssel in der Rückgabe")
print("Antwortspeicher-RPC: nur eigene offene Versuchsfragen")
print("Antwortspeicher-RPC: Browser liefert keine Punkte oder Schlüssel")
print("Antwortspeicher-RPC: Antwortindizes validiert und normalisiert")
print(
    "Reihenfolge: Schema vor RLS vor Lockdown "
    "vor Fragen-Schema vor Fragen-RLS "
    "vor Versuchsschlüssel-Snapshot "
    "vor Teilpunkte-Korrektur "
    "vor Antwortintegrität "
    "vor Prüfungsstart-RPC "
    "vor Antwortspeicher-RPC "
    "vor Prüfungsabschluss-RPC "
    "vor Auswahlbegrenzungs-Korrektur "
    "vor Ergebnisabruf-RPC "
    "vor Prüfungsversuch-Integrität "
    "vor Vollsimulations-Zustandsintegrität "
    "vor direkter Prüfungs-Schreibsperre "
    "vor Mitarbeiter-Rollentrennung"
)
print("Prüfungsabschluss-RPC: serverseitige Bewertung vorbereitet")
print("Prüfungsabschluss-RPC: Teilpunkte ohne Punktabzug")
print("Prüfungsabschluss-RPC: Bestehensgrenze 60 von 120 Punkten")
print("Prüfungsabschluss-RPC: idempotenter Abschluss")
print("Auswahlbegrenzung: aus privatem Versuchsschlüssel abgeleitet")
print("Auswahlbegrenzung: Überauswahl beim Speichern gesperrt")
print("Auswahlbegrenzung: Überauswahl vor Bewertung erneut gesperrt")
print("Ergebnisabruf-RPC: nur eigene abgeschlossene Vollsimulation")
print("Ergebnisabruf-RPC: gespeicherte 82/120-Daten gegengeprüft")
print("Ergebnisabruf-RPC: Antwortkategorien ergeben zusammen 82")
print("Ergebnisabruf-RPC: keine Lösungsschlüssel in der Rückgabe")
print("Ergebnisabruf-RPC: historische Ergebnisse sicher abrufbar")
print("Prüfungsversuch-Integrität: score_points <= max_points")
print("Prüfungsversuch-Integrität: Abschluss nicht vor Start")
print("Vollsimulation offen: 0 von 120 Punkten und nicht bestanden")
print("Vollsimulation abgeschlossen: Bestehen entspricht mindestens 60 Punkten")
print("Prüfungsdaten: direkte Schreibrechte für alle App-Rollen gesperrt")
print("Prüfungsdaten: Schreiben ausschließlich über geprüfte RPCs")
print("Mitarbeiterrollen: Support nur lesend")
print("Mitarbeiterrollen: Verwaltung nur Admin/Dozent")
print("Live-Ausführung: nein")
