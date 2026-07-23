from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-idempotency-transactional-mutation-contract.json"
)

RESERVE_PATH = (
    ROOT
    / "supabase"
    / "migrations"
    / "20260722_v2731r_exam_history_idempotency_expected_version_reserve_rpc.sql"
)

COMPLETE_PATH = (
    ROOT
    / "supabase"
    / "migrations"
    / "20260722_v2731d_exam_history_idempotency_complete_rpc.sql"
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


if not CONTRACT_PATH.is_file():
    fail("Transaktionaler Fachmutationsvertrag fehlt.")

try:
    contract = json.loads(
        CONTRACT_PATH.read_text(encoding="utf-8")
    )
except Exception as exc:
    fail(f"Transaktionaler Fachmutationsvertrag ungültig: {exc}")

expected_top_level_keys = {
    "version",
    "contractVersion",
    "status",
    "productiveReleaseAllowed",
    "boundary",
    "identity",
    "phases",
    "decisionMatrix",
    "transactionRules",
    "securityRules",
    "unresolvedRequirements",
}

if set(contract) != expected_top_level_keys:
    fail(
        "Unerwartete Vertragsfelder: "
        f"{sorted(set(contract) - expected_top_level_keys)}"
    )

if contract["version"] != "v27.31r":
    fail("Vertragsversion ist nicht v27.31r.")

if contract["contractVersion"] != 1:
    fail("Vertragsschemaversion ist nicht 1.")

if contract["status"] != "prepared_not_live":
    fail("Vertragsstatus ist nicht vorbereitet.")

if contract["productiveReleaseAllowed"] is not False:
    fail("Produktive Freigabe darf noch nicht erlaubt sein.")

boundary = contract["boundary"]

expected_boundary = {
    "rpcType": "single_security_definer_mutation_rpc",
    "transactionScope": "single_database_transaction",
    "reserveHelper": (
        "public."
        "accaoui_reserve_exam_history_idempotency_operation"
    ),
    "completeHelper": (
        "public."
        "accaoui_complete_exam_history_idempotency_operation"
    ),
    "helperDirectExecutionAllowed": False,
    "directTableAccessAllowed": False,
    "directClientMutationAllowed": False,
    "liveExecution": False,
}

if boundary != expected_boundary:
    fail("Transaktionsgrenze ist nicht kanonisch.")

identity = contract["identity"]

expected_identity = {
    "source": "trusted_server_or_database_issued",
    "browserGeneratedAllowed": False,
    "operationIdentityInputAllowed": False,
    "verifiedNow": False,
    "requiredParameters": [
        "external_operation_id",
        "operation_scope",
        "operation",
        "resource_identity",
        "expected_storage_version",
        "payload_fingerprint",
    ],
}

if identity != expected_identity:
    fail("Operationsidentitätsvertrag ist nicht kanonisch.")

expected_phases = [
    (1, "authenticate_and_validate"),
    (2, "reserve_operation"),
    (3, "branch_on_reservation_status"),
    (4, "execute_domain_mutation"),
    (5, "complete_operation"),
    (6, "return_canonical_result"),
]

actual_phases = [
    (
        phase.get("order"),
        phase.get("name"),
    )
    for phase in contract["phases"]
]

if actual_phases != expected_phases:
    fail(
        "Transaktionale Phasenreihenfolge ist ungültig: "
        f"{actual_phases}"
    )

expected_matrix = [
    {
        "reservationStatus": "reserved_new",
        "executeDomainMutation": True,
        "completeOperation": True,
        "responseSource": "new_domain_result",
    },
    {
        "reservationStatus": "reserved_existing_pending",
        "executeDomainMutation": False,
        "completeOperation": False,
        "responseSource": "in_progress_no_reexecution",
    },
    {
        "reservationStatus": "reserved_existing_completed",
        "executeDomainMutation": False,
        "completeOperation": False,
        "responseSource": "stored_result",
    },
    {
        "reservationStatus": "reserved_existing_failed",
        "executeDomainMutation": False,
        "completeOperation": False,
        "responseSource": "stored_failure",
    },
]

if contract["decisionMatrix"] != expected_matrix:
    fail("Reservierungs-Entscheidungsmatrix ist ungültig.")

transaction_rules = contract["transactionRules"]

required_true_transaction_rules = (
    "successfulMutationAndCompletedStateCommitTogether",
    "expectedDomainFailureUsesSubtransactionRollback",
    "expectedDomainFailureCompletesFailedAfterRollback",
    "unexpectedInternalFailureReraises",
    "unexpectedInternalFailureRollsBackWholeTransaction",
)

required_false_transaction_rules = (
    "rawErrorStorageAllowed",
    "terminalOverwriteAllowed",
    "existingPendingReexecutionAllowed",
    "existingTerminalReexecutionAllowed",
    "completionWithoutReservationAllowed",
)

for name in required_true_transaction_rules:
    if transaction_rules.get(name) is not True:
        fail(f"Erforderliche Transaktionsregel fehlt: {name}")

for name in required_false_transaction_rules:
    if transaction_rules.get(name) is not False:
        fail(f"Verbotene Transaktionsregel ist erlaubt: {name}")

security_rules = contract["securityRules"]

expected_security_rules = {
    "authUserFromAuthUidOnly": True,
    "participantIdParameterAllowed": False,
    "authUserIdParameterAllowed": False,
    "serviceRoleInFrontendAllowed": False,
    "rawDatabaseErrorReturned": False,
    "directHelperGrantAllowed": False,
    "directIdempotencyTableGrantAllowed": False,
}

if security_rules != expected_security_rules:
    fail("Sicherheitsregeln sind nicht kanonisch.")

unresolved = contract["unresolvedRequirements"]

expected_unresolved = {
    "trustedOperationIdentityIssuance": True,
    "domainMutationRpcImplementation": True,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
}

if unresolved != expected_unresolved:
    fail("Offene produktive Anforderungen sind unvollständig.")

for path, function_name in (
    (
        RESERVE_PATH,
        "accaoui_reserve_exam_history_idempotency_operation",
    ),
    (
        COMPLETE_PATH,
        "accaoui_complete_exam_history_idempotency_operation",
    ),
):
    if not path.is_file():
        fail(f"Referenzierte RPC-Migration fehlt: {path.name}")

    sql = path.read_text(encoding="utf-8").lower()

    if function_name not in sql:
        fail(f"Referenzierter RPC fehlt: {function_name}")

    if "security definer" not in sql:
        fail(f"Security-Definer-Grenze fehlt: {function_name}")

    if "set search_path = pg_catalog, public" not in sql:
        fail(f"Fester search_path fehlt: {function_name}")

    if "set row_security = off" not in sql:
        fail(f"row_security-Grenze fehlt: {function_name}")


reserve_sql = RESERVE_PATH.read_text(encoding="utf-8").lower()
complete_sql = COMPLETE_PATH.read_text(encoding="utf-8").lower()

for marker in (
    "p_expected_storage_version bigint",
    "expected_storage_version,",
    "p_expected_storage_version,",
    "v_existing.expected_storage_version <>",
):
    if marker not in reserve_sql:
        fail(
            "Reservierungshelper bindet den erwarteten "
            f"Versionsstand nicht: {marker}"
        )

if "p_expected_storage_version bigint" in complete_sql:
    fail(
        "Abschlusshelper darf keinen neuen "
        "Browser-Versionsparameter besitzen."
    )

v2731f_sql_files = list(
    (ROOT / "supabase" / "migrations").glob(
        "*v2731f*.sql"
    )
)

if v2731f_sql_files:
    fail(
        "v27.31f darf noch keine SQL-Migration erzeugen: "
        f"{[path.name for path in v2731f_sql_files]}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
):
    frontend_text = frontend_path.read_text(
        encoding="utf-8"
    ).lower()

    if CONTRACT_PATH.name.lower() in frontend_text:
        fail(
            "Transaktionaler Vertrag darf nicht im Frontend "
            f"geladen werden: {frontend_path.name}"
        )

print("Transaktionaler Fachmutationsvertrag: OK")
print(
    "Reihenfolge: Authentifizieren, reservieren, verzweigen, "
    "mutieren, abschließen, zurückgeben"
)
print(
    "Fachmutation: ausschließlich bei reserved_new erlaubt"
)
print(
    "Existing Pending: keine parallele oder erneute Mutation"
)
print(
    "Existing Completed/Failed: gespeichertes Ergebnis "
    "wiederverwenden"
)
print(
    "Erwarteter Fachfehler: Teilmutation zurückrollen und "
    "stabilen Failed-Abschluss speichern"
)
print(
    "Unerwarteter Fehler: gesamte Datenbanktransaktion "
    "zurückrollen"
)
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
