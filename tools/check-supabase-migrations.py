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

if "create policy" in exam_answers_integrity_lower:
    fail("Antwortintegrität darf keine neue RLS-Policy erstellen.")

if "grant " in exam_answers_integrity_lower:
    fail("Antwortintegrität darf keine Direktrechte vergeben.")

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

effective_policy_count = len(policies) - len(required_drops)

if effective_policy_count != 15:
    fail(
        f"Erwartet: 15 effektive Policies, gefunden: "
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
print(
    "Reihenfolge: Schema vor RLS vor Lockdown "
    "vor Fragen-Schema vor Fragen-RLS "
    "vor Versuchsschlüssel-Snapshot "
    "vor Teilpunkte-Korrektur "
    "vor Antwortintegrität"
)
print("Live-Ausführung: nein")
