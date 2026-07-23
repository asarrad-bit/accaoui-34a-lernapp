from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-e2e-audit-contract.json"
)
OUTER_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-rpc-interface-contract.json"
)
TRANSACTION_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-idempotency-transactional-mutation-contract.json"
)
OUTER_SQL_PATH = (
    MIGRATIONS
    / "20260723_v2731u_"
      "exam_history_outer_domain_mutation_rpc.sql"
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


def read_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


def strip_comments(text: str) -> str:
    return re.sub(
        r"--.*?$",
        "",
        text,
        flags=re.MULTILINE,
    )


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


contract = read_json(
    CONTRACT_PATH,
    "Äußerer Fachmutations-End-to-End-Auditvertrag",
)

if contract.get("version") != "v27.31v":
    fail("End-to-End-Auditvertrag besitzt nicht v27.31v.")
if contract.get("contractVersion") != 1:
    fail("End-to-End-Auditvertrag besitzt nicht Schema 1.")
if contract.get("status") != "prepared_not_live":
    fail("End-to-End-Auditvertrag ist nicht vorbereitet.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("End-to-End-Audit darf noch nicht produktiv sein.")
if contract.get("auditType") != "static_source_audit":
    fail("End-to-End-Audit ist kein reiner statischer Audit.")

implementation = contract.get("implementation", {})
if implementation != {
    "outerRpc": "public.accaoui_mutate_exam_history_domain",
    "outerRpcMigrationPath": (
        "supabase/migrations/"
        "20260723_v2731u_"
        "exam_history_outer_domain_mutation_rpc.sql"
    ),
    "auditCheckerPath": (
        "tools/"
        "check-supabase-exam-history-"
        "outer-domain-mutation-e2e-audit.py"
    ),
    "auditDocumentPath": (
        "docs/"
        "SUPABASE_EXAM_RESULT_HISTORY_"
        "OUTER_DOMAIN_MUTATION_E2E_AUDIT.md"
    ),
    "sqlMigrationCreated": False,
    "liveDatabaseExecution": False,
    "frontendIntegration": False,
}:
    fail("End-to-End-Auditimplementierung ist ungültig.")

expected_scenarios = {
    "reservedNew": {
        "domainMutationExecutedExactlyOnce": True,
        "completedExactlyOnce": True,
        "returnsTerminalCompleted": True,
    },
    "reservedExistingPending": {
        "domainMutationExecuted": False,
        "completionExecuted": False,
        "outcome": "in_progress",
        "operationStatus": "pending",
        "retryable": True,
    },
    "reservedExistingCompleted": {
        "domainMutationExecuted": False,
        "completionExecuted": False,
        "storedResultReturned": True,
        "operationStatus": "completed",
        "retryable": False,
    },
    "reservedExistingFailed": {
        "domainMutationExecuted": False,
        "completionExecuted": False,
        "storedFailureReturned": True,
        "operationStatus": "failed",
        "retryable": False,
    },
}
if contract.get("scenarioMatrix") != expected_scenarios:
    fail("Retry-Szenariomatrix ist ungültig.")

rollback = contract.get("rollbackMatrix", {})
if rollback != {
    "expectedDomainFailure": {
        "innerSubtransactionRollbackRequired": True,
        "idempotencyCompletionAfterRollback": "failed",
        "stableFailureCodeRequired": True,
        "rawDatabaseErrorAllowed": False,
    },
    "unexpectedFailure": {
        "caughtByWhenOthers": False,
        "reraised": True,
        "wholeOuterCallRollbackRequired": True,
        "failedTerminalStatePersisted": False,
    },
}:
    fail("Rollback-Matrix ist ungültig.")

response = contract.get("responseBoundary", {})
if response != {
    "allowedColumns": [
        "outcome",
        "operation_status",
        "result",
        "failure_code",
        "retryable",
    ],
    "internalOperationIdAllowed": False,
    "operationIdentityAllowed": False,
    "payloadFingerprintAllowed": False,
    "requestFingerprintAllowed": False,
    "clientRequestKeyHashAllowed": False,
    "authUserIdAllowed": False,
    "rawDatabaseErrorAllowed": False,
}:
    fail("Clientantwortgrenze ist ungültig.")

security = contract.get("securityBoundary", {})
if security != {
    "directPublicExecutionAllowed": False,
    "directAnonExecutionAllowed": False,
    "directAuthenticatedExecutionAllowed": False,
    "grantExecutePresent": False,
    "directTableMutationInOuterRpc": False,
    "frontendReferenceAllowed": False,
    "serviceRoleInFrontendAllowed": False,
}:
    fail("Sicherheitsgrenze ist ungültig.")

if contract.get("unresolvedRequirements") != {
    "liveDatabaseTests": True,
    "concurrencyTests": True,
    "authorizationTests": True,
    "directAppExecutionGrant": True,
    "frontendIntegration": True,
}:
    fail("Offene End-to-End-Anforderungen sind ungültig.")

outer_contract = read_json(
    OUTER_CONTRACT_PATH,
    "Äußerer Fachmutations-RPC-Vertrag",
)
if outer_contract.get("version") != "v27.31u":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31u.")
if outer_contract.get("implementationPresent") is not True:
    fail("Äußerer RPC ist nicht als vorbereitet markiert.")
if outer_contract.get("productiveReleaseAllowed") is not False:
    fail("Äußerer RPC ist unerwartet produktiv.")

transaction_contract = read_json(
    TRANSACTION_CONTRACT_PATH,
    "Transaktionaler Fachmutationsvertrag",
)
if transaction_contract.get("version") != "v27.31u":
    fail("Transaktionsvertrag besitzt nicht v27.31u.")
if transaction_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail("Transaktionsvertrag ist unerwartet produktiv.")

if not OUTER_SQL_PATH.is_file():
    fail("Äußerer Fachmutations-RPC fehlt.")

sql = OUTER_SQL_PATH.read_text(encoding="utf-8")
clean = strip_comments(sql)
sql_compact = compact(clean)

signature = re.search(
    r"function\s+"
    r"public\.accaoui_mutate_exam_history_domain"
    r"\s*\((.*?)\)\s*returns\s+table\s*"
    r"\((.*?)\)\s*language\s+plpgsql",
    sql,
    flags=re.IGNORECASE | re.DOTALL,
)
if not signature:
    fail("Äußere RPC-Signatur fehlt.")

return_columns = []
for raw_column in signature.group(2).split(","):
    parts = re.sub(
        r"\s+",
        " ",
        raw_column.strip().lower(),
    ).split()
    if len(parts) != 2:
        fail(f"Unerwartete Rückgabespalte: {raw_column}")
    return_columns.append(parts[0])

if return_columns != response["allowedColumns"]:
    fail(f"Clientantwortspalten sind ungültig: {return_columns}")

helper_markers = [
    "public.accaoui_validate_exam_history_domain_payload(",
    "public.accaoui_issue_exam_history_operation_identity(",
    "public.accaoui_reserve_exam_history_idempotency_operation(",
    "public.accaoui_mutate_exam_history_domain_resource(",
    "public.accaoui_complete_exam_history_idempotency_operation(",
]
positions = [sql_compact.find(marker) for marker in helper_markers]
if any(position < 0 for position in positions):
    fail("Helperkette ist unvollständig.")
if positions != sorted(positions):
    fail(f"Helperkette ist falsch angeordnet: {positions}")

branch_markers = {
    "pending": "if v_reservation_status = 'reserved_existing_pending' then",
    "completed": (
        "if v_reservation_status = "
        "'reserved_existing_completed' then"
    ),
    "failed": (
        "if v_reservation_status = "
        "'reserved_existing_failed' then"
    ),
    "new": "if v_reservation_status <> 'reserved_new' then",
}
branch_positions = {
    name: sql_compact.find(marker)
    for name, marker in branch_markers.items()
}
if any(position < 0 for position in branch_positions.values()):
    fail(f"Reservierungszweige fehlen: {branch_positions}")

mutation_position = sql_compact.find(
    "public.accaoui_mutate_exam_history_domain_resource("
)
if mutation_position < 0:
    fail("Domain-Mutationsaufruf fehlt.")

for terminal_name in ("pending", "completed", "failed"):
    if branch_positions[terminal_name] >= mutation_position:
        fail(
            f"{terminal_name}-Zweig liegt nicht vor "
            "der Domain-Mutation."
        )

pending_block = re.search(
    r"if\s+v_reservation_status\s*=\s*"
    r"'reserved_existing_pending'\s+then(.*?)"
    r"end\s+if\s*;",
    clean,
    flags=re.IGNORECASE | re.DOTALL,
)
if not pending_block:
    fail("Pending-Zweig ist nicht isolierbar.")
pending_compact = compact(pending_block.group(1))
for marker in (
    "'in_progress'::text",
    "'pending'::text",
    "true",
    "return;",
):
    if marker not in pending_compact:
        fail(f"Pending-Antwort fehlt: {marker}")
for forbidden in (
    "accaoui_mutate_exam_history_domain_resource",
    "accaoui_complete_exam_history_idempotency_operation",
):
    if forbidden in pending_compact:
        fail(f"Pending-Zweig führt verbotenen Helper aus: {forbidden}")

completed_block = re.search(
    r"if\s+v_reservation_status\s*=\s*"
    r"'reserved_existing_completed'\s+then(.*?)"
    r"end\s+if\s*;",
    clean,
    flags=re.IGNORECASE | re.DOTALL,
)
if not completed_block:
    fail("Completed-Zweig ist nicht isolierbar.")
completed_compact = compact(completed_block.group(1))
for marker in (
    "v_reserved_result",
    "'completed'::text",
    "false",
    "return;",
):
    if marker not in completed_compact:
        fail(f"Completed-Antwort fehlt: {marker}")
for forbidden in (
    "accaoui_mutate_exam_history_domain_resource",
    "accaoui_complete_exam_history_idempotency_operation",
):
    if forbidden in completed_compact:
        fail(f"Completed-Zweig führt verbotenen Helper aus: {forbidden}")

failed_block = re.search(
    r"if\s+v_reservation_status\s*=\s*"
    r"'reserved_existing_failed'\s+then(.*?)"
    r"end\s+if\s*;",
    clean,
    flags=re.IGNORECASE | re.DOTALL,
)
if not failed_block:
    fail("Failed-Zweig ist nicht isolierbar.")
failed_compact = compact(failed_block.group(1))
for marker in (
    "'failed'::text",
    "v_reserved_failure",
    "false",
    "return;",
):
    if marker not in failed_compact:
        fail(f"Failed-Antwort fehlt: {marker}")
for forbidden in (
    "accaoui_mutate_exam_history_domain_resource",
    "accaoui_complete_exam_history_idempotency_operation",
):
    if forbidden in failed_compact:
        fail(f"Failed-Zweig führt verbotenen Helper aus: {forbidden}")

expected_exception = re.search(
    r"begin\s+select\s+mutation\.outcome.*?"
    r"exception\s+when\s+sqlstate\s+'22023'\s+"
    r"or\s+sqlstate\s+'40001'\s+"
    r"or\s+sqlstate\s+'23514'\s+then(.*?)"
    r"end\s*;",
    clean,
    flags=re.IGNORECASE | re.DOTALL,
)
if not expected_exception:
    fail("Erwarteter Domain-Fehlerblock ist nicht eindeutig.")

exception_compact = compact(expected_exception.group(1))
for marker in (
    "get stacked diagnostics v_failure_code = message_text",
    "if v_failure_code not in (",
    "public.accaoui_complete_exam_history_idempotency_operation(",
    "'failed'",
    "v_failure_code",
    "return;",
):
    if marker not in exception_compact:
        fail(f"Erwarteter Fehlerweg ist unvollständig: {marker}")

stable_domain_failures = (
    "domain_storage_expected_version_invalid",
    "domain_storage_version_conflict",
    "domain_storage_resource_identity_invalid",
    "domain_storage_scope_invalid",
    "domain_storage_payload_invalid",
    "domain_storage_state_invalid",
)
for failure_code in stable_domain_failures:
    if f"'{failure_code}'" not in exception_compact:
        fail(f"Stabiler Domain-Fehler fehlt: {failure_code}")

if "when others" in sql_compact:
    fail("Unerwartete Fehler werden pauschal abgefangen.")
if "sqlerrm" in sql_compact:
    fail("Roher SQL-Fehlertext wird verwendet.")

completion_count = sql_compact.count(
    "public.accaoui_complete_exam_history_idempotency_operation("
)
if completion_count != 2:
    fail(
        "Idempotenzabschluss muss exakt im Expected-Failed- "
        f"und Erfolgsweg vorkommen: {completion_count}"
    )

result_object = re.search(
    r"v_domain_result\s*:=\s*jsonb_build_object\s*\((.*?)\)\s*;",
    clean,
    flags=re.IGNORECASE | re.DOTALL,
)
if not result_object:
    fail("Domain-Clientresultat ist nicht eindeutig.")
result_compact = compact(result_object.group(1))

required_result_keys = (
    "'outcome'",
    "'storage_version'",
    "'is_deleted'",
    "'created_at'",
    "'updated_at'",
)
for marker in required_result_keys:
    if marker not in result_compact:
        fail(f"Erlaubtes Ergebnisfeld fehlt: {marker}")

for forbidden in (
    "'external_operation_id'",
    "'operation_identity'",
    "'payload_fingerprint'",
    "'request_fingerprint'",
    "'client_request_key_hash'",
    "'auth_user_id'",
    "'canonical_byte_length'",
):
    if forbidden in result_compact:
        fail(f"Internes Ergebnisfeld wird ausgegeben: {forbidden}")

for forbidden_return_name in (
    "external_operation_id",
    "operation_identity",
    "payload_fingerprint",
    "request_fingerprint",
    "client_request_key_hash",
    "auth_user_id",
):
    if forbidden_return_name in return_columns:
        fail(
            "Internes Rückgabefeld ist erlaubt: "
            f"{forbidden_return_name}"
        )

for role in ("public", "anon", "authenticated"):
    revoke_pattern = (
        r"revoke\s+all\s+on\s+function\s+"
        r"public\.accaoui_mutate_exam_history_domain"
        r"\s*\(\s*text\s*,\s*text\s*,\s*text\s*,\s*"
        r"text\s*,\s*bigint\s*,\s*jsonb\s*\)\s+from\s+"
        + re.escape(role)
        + r"\s*;"
    )
    if not re.search(
        revoke_pattern,
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(f"Äußerer RPC-Revoke fehlt: {role}")

for forbidden in (
    "grant execute",
    "create policy",
    "service_role",
    "insert into public.",
    "update public.",
    "delete from public.",
    "exam_history_domain_resources",
    "exam_history_idempotency_operations",
    "exam_history_operation_identity_issuances",
):
    if forbidden in sql_compact:
        fail(f"Unzulässiger äußerer RPC-Inhalt: {forbidden}")

v2731v_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2731v*.sql")
)
if v2731v_sql_files:
    fail(
        "v27.31v ist ein statischer Audit und darf keine "
        f"SQL-Migration erzeugen: {v2731v_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend = frontend_path.read_text(encoding="utf-8").lower()
    if "accaoui_mutate_exam_history_domain" in frontend:
        fail(
            "Äußerer RPC ist vor Freigabe im Frontend "
            f"referenziert: {frontend_path.name}"
        )
    if CONTRACT_PATH.name.lower() in frontend:
        fail(
            "End-to-End-Auditvertrag wird im Frontend geladen: "
            f"{frontend_path.name}"
        )

print("Äußerer Fachmutations-End-to-End-Audit: OK")
print("Reserved New: genau eine Domain-Mutation und Abschluss")
print("Reserved Pending: in_progress ohne Mutation oder Abschluss")
print("Reserved Completed: gespeichertes Ergebnis ohne Mutation")
print("Reserved Failed: gespeicherter Fehler ohne Mutation")
print(
    "Erwartete Domain-Fehler: innerer Teilrollback und "
    "stabiler Failed-Abschluss"
)
print(
    "Unerwartete Fehler: kein when others; vollständiger "
    "Datenbankaufruf rollt zurück"
)
print(
    "Clientantwort: keine UUIDs, Identitäten, Hashes oder "
    "Fingerprints"
)
print("Direkte Ausführung: vollständig gesperrt")
print("SQL-Migration v27.31v: keine")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
