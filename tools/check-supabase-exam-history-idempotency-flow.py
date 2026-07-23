from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

OPERATIONS_FILE = (
    "20260722_v2731b_exam_history_idempotency_operations.sql"
)
RESERVE_FILE = (
    "20260722_v2731r_"
    "exam_history_idempotency_expected_version_reserve_rpc.sql"
)
COMPLETE_FILE = (
    "20260722_v2731d_exam_history_idempotency_complete_rpc.sql"
)

TABLE_NAME = "exam_history_idempotency_operations"


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


def read_sql(filename: str) -> str:
    path = MIGRATIONS / filename

    if not path.is_file():
        fail(f"Idempotenz-Datei fehlt: {filename}")

    return (
        path.read_text(encoding="utf-8")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )


def without_comments(text: str) -> str:
    return re.sub(
        r"--.*?$",
        "",
        text,
        flags=re.MULTILINE,
    )


def compact(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text.lower(),
    ).strip()


def require_markers(
    text: str,
    markers: tuple[str, ...],
    label: str,
) -> None:
    for marker in markers:
        if marker not in text:
            fail(f"{label}: Anweisung fehlt: {marker}")


def function_count(
    sql: str,
    function_name: str,
) -> int:
    return len(
        re.findall(
            r"create\s+or\s+replace\s+function\s+"
            + re.escape(function_name)
            + r"\s*\(",
            sql,
            flags=re.IGNORECASE,
        )
    )


def function_parameters(
    sql: str,
    function_name: str,
) -> list[tuple[str, str]]:
    match = re.search(
        r"function\s+"
        + re.escape(function_name)
        + r"\s*\((.*?)\)\s*returns",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        fail(f"Funktionssignatur fehlt: {function_name}")

    raw_parameters = [
        re.sub(r"\s+", " ", item.strip().lower())
        for item in match.group(1).split(",")
        if item.strip()
    ]

    parsed = []

    for parameter in raw_parameters:
        parameter = re.sub(
            r"\s+default\s+.+$",
            "",
            parameter,
        )

        parts = parameter.split()

        if len(parts) != 2:
            fail(
                f"Unerwarteter Funktionsparameter in "
                f"{function_name}: {parameter}"
            )

        parsed.append((parts[0], parts[1]))

    return parsed


def mutation_targets(sql_without_comments: str):
    return [
        (
            re.sub(r"\s+", " ", action.lower()),
            table.lower(),
        )
        for action, table in re.findall(
            r"\b(insert\s+into|update|delete\s+from)\s+"
            r"(?:public\.)?([a-z_]+)",
            sql_without_comments,
            flags=re.IGNORECASE,
        )
    ]


operations_sql = read_sql(OPERATIONS_FILE)
reserve_sql = read_sql(RESERVE_FILE)
complete_sql = read_sql(COMPLETE_FILE)

operations_clean = without_comments(operations_sql)
reserve_clean = without_comments(reserve_sql)
complete_clean = without_comments(complete_sql)

operations_compact = compact(operations_clean)
reserve_compact = compact(reserve_clean)
complete_compact = compact(complete_clean)

require_markers(
    operations_compact,
    (
        "create table if not exists "
        "public.exam_history_idempotency_operations",
        "unique (operation_identity)",
        "unique ( operation_scope, operation, "
        "external_operation_id )",
        "operation_identity = "
        "'exam_history_idempotency:' || "
        "operation_scope || ':' || operation || ':' || "
        "external_operation_id::text",
        "status in ( 'pending', 'completed', 'failed' )",
        "status = 'pending'",
        "status = 'completed'",
        "status = 'failed'",
        "payload_fingerprint ~ '^[0-9a-f]{64}$'",
        "jsonb_typeof(result_payload) = 'object'",
        "alter table "
        "public.exam_history_idempotency_operations "
        "enable row level security",
        "alter table "
        "public.exam_history_idempotency_operations "
        "force row level security",
        "revoke all on table "
        "public.exam_history_idempotency_operations "
        "from public, anon, authenticated",
    ),
    "Idempotenz-Operationstabelle",
)

for forbidden in (
    "create policy",
    "grant ",
    "service_role",
):
    if forbidden in operations_compact:
        fail(
            "Idempotenz-Operationstabelle enthält "
            f"unzulässigen Inhalt: {forbidden}"
        )

reserve_name = (
    "public."
    "accaoui_reserve_exam_history_idempotency_operation"
)
complete_name = (
    "public."
    "accaoui_complete_exam_history_idempotency_operation"
)

if function_count(reserve_sql, reserve_name) != 1:
    fail(
        "Idempotenz-Reservierungs-RPC muss genau einmal "
        "vorhanden sein."
    )

if function_count(complete_sql, complete_name) != 1:
    fail(
        "Idempotenz-Abschluss-RPC muss genau einmal "
        "vorhanden sein."
    )

common_rpc_markers = (
    "language plpgsql",
    "security definer",
    "set search_path = pg_catalog, public",
    "set row_security = off",
    "v_auth_user_id := auth.uid()",
    "message = 'authentication_required'",
    "'exam_history_idempotency:' || "
    "p_operation_scope || ':' || "
    "p_operation || ':' || "
    "p_external_operation_id::text",
    "p_operation_scope not in ( 'snapshot', 'cycle_registry' )",
    "p_operation not in ( 'write', 'delete' )",
    "p_resource_identity <> trim(p_resource_identity)",
    "p_payload_fingerprint !~ '^[0-9a-f]{64}$'",
    "p_operation = 'delete' "
    "and p_payload_fingerprint is not null",
)

require_markers(
    reserve_compact,
    common_rpc_markers,
    "Idempotenz-Reservierungs-RPC",
)

require_markers(
    complete_compact,
    common_rpc_markers,
    "Idempotenz-Abschluss-RPC",
)

require_markers(
    reserve_compact,
    (
        "insert into "
        "public.exam_history_idempotency_operations",
        "on conflict do nothing",
        "returning id into v_inserted_id",
        "for update",
        "'reserved_new'::text",
        "'reserved_existing_pending'",
        "'reserved_existing_completed'",
        "'reserved_existing_failed'",
        "message = "
        "'idempotency_operation_resource_conflict'",
        "message = "
        "'idempotency_operation_payload_conflict'",
        "p_expected_storage_version bigint",
        "message = 'expected_storage_version_invalid'",
        "expected_storage_version, payload_fingerprint",
        "p_expected_storage_version, p_payload_fingerprint",
        "v_existing.expected_storage_version <> "
        "p_expected_storage_version",
    ),
    "Idempotenz-Reservierungs-RPC",
)

require_markers(
    complete_compact,
    (
        "select io.* into v_existing from "
        "public.exam_history_idempotency_operations io",
        "for update",
        "if v_existing.status = 'pending'",
        "update "
        "public.exam_history_idempotency_operations",
        "where id = v_operation_id and status = 'pending'",
        "'completed_new'",
        "'failed_new'",
        "'already_completed'",
        "'already_failed'",
        "message = "
        "'idempotency_operation_terminal_conflict'",
        "message = "
        "'idempotency_completion_concurrent_conflict'",
    ),
    "Idempotenz-Abschluss-RPC",
)

reserve_identity_parameters = [
    ("p_external_operation_id", "uuid"),
    ("p_operation_scope", "text"),
    ("p_operation", "text"),
    ("p_resource_identity", "text"),
    ("p_expected_storage_version", "bigint"),
    ("p_payload_fingerprint", "text"),
]

complete_identity_parameters = [
    ("p_external_operation_id", "uuid"),
    ("p_operation_scope", "text"),
    ("p_operation", "text"),
    ("p_resource_identity", "text"),
    ("p_payload_fingerprint", "text"),
]

reserve_parameters = function_parameters(
    reserve_sql,
    reserve_name,
)
complete_parameters = function_parameters(
    complete_sql,
    complete_name,
)

if reserve_parameters != reserve_identity_parameters:
    fail(
        "Reservierungs-RPC besitzt keine versionierte "
        "Identitätsparameterschnittstelle."
    )

if complete_parameters[:5] != complete_identity_parameters:
    fail(
        "Abschluss-RPC verwendet nicht die kanonische "
        "gespeicherte Identität."
    )

if any(
    name == "p_expected_storage_version"
    for name, _ in complete_parameters
):
    fail(
        "Abschluss-RPC darf keinen Browser-Versionsparameter "
        "akzeptieren."
    )

expected_complete_suffix = [
    ("p_terminal_status", "text"),
    ("p_result_payload", "jsonb"),
    ("p_failure_code", "text"),
]

if complete_parameters[5:] != expected_complete_suffix:
    fail(
        "Abschluss-RPC besitzt unerwartete "
        "Terminalparameter."
    )

reserve_mutations = mutation_targets(reserve_clean)
complete_mutations = mutation_targets(complete_clean)

if reserve_mutations != [
    ("insert into", TABLE_NAME),
]:
    fail(
        "Reservierungs-RPC verändert unerwartete Tabellen: "
        f"{reserve_mutations}"
    )

if complete_mutations != [
    ("update", TABLE_NAME),
]:
    fail(
        "Abschluss-RPC verändert unerwartete Tabellen: "
        f"{complete_mutations}"
    )

for label, rpc_compact in (
    ("Reservierungs-RPC", reserve_compact),
    ("Abschluss-RPC", complete_compact),
):
    for forbidden in (
        "grant execute",
        "create policy",
        "service_role",
        "sqlerrm",
        "stacked diagnostics",
        "public.exam_attempts",
        "public.exam_answers",
        "public.exam_attempt_questions",
        "public.exam_question_answer_keys",
        "public.exam_attempt_question_answer_keys",
        "localstorage",
        "sessionstorage",
    ):
        if forbidden in rpc_compact:
            fail(
                f"{label} enthält unzulässigen Inhalt: "
                f"{forbidden}"
            )

for role in (
    "public",
    "anon",
    "authenticated",
):
    for function_name, sql in (
        (reserve_name, reserve_sql),
        (complete_name, complete_sql),
    ):
        pattern = (
            r"revoke\s+all\s+on\s+function\s+"
            + re.escape(function_name)
            + r"\s*\(.*?\)\s+from\s+"
            + re.escape(role)
            + r"\s*;"
        )

        if not re.search(
            pattern,
            sql,
            flags=re.IGNORECASE | re.DOTALL,
        ):
            fail(
                f"Revoke fehlt für {function_name}: {role}"
            )

print("Idempotenz-End-to-End-Audit: OK")
print("Operationstabelle: RLS-erzwungen und direkt gesperrt")
print(
    "Operationsidentität: Reservierung bindet erwarteten "
    "Versionsstand; Abschluss liest die gespeicherte Zeile"
)
print(
    "Reservierung: atomar über Unique Constraints und "
    "exakten Versionsvergleich vorbereitet"
)
print("Abschluss: nur Pending und ohne terminales Überschreiben")
print("Direkte App-Ausführung: für beide internen RPCs gesperrt")
print("Fremde Fachmutationen: in beiden Helfern ausgeschlossen")
print(
    "Transaktionale Fachintegration: noch nicht verbunden; "
    "späterer Mutations-RPC erforderlich"
)
print("Live-Ausführung: nein")
