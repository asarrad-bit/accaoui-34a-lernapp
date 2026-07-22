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
    / "exam-history-outer-domain-mutation-rpc-interface-contract.json"
)

ISSUANCE_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-operation-identity-issuance-contract.json"
)

TRANSACTION_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-idempotency-transactional-mutation-contract.json"
)

HELPER_MIGRATIONS = {
    (
        "public."
        "accaoui_issue_exam_history_operation_identity"
    ): (
        "20260722_v2731i_"
        "exam_history_operation_identity_issue_rpc.sql"
    ),
    (
        "public."
        "accaoui_reserve_exam_history_idempotency_operation"
    ): (
        "20260722_v2731c_"
        "exam_history_idempotency_reserve_rpc.sql"
    ),
    (
        "public."
        "accaoui_complete_exam_history_idempotency_operation"
    ): (
        "20260722_v2731d_"
        "exam_history_idempotency_complete_rpc.sql"
    ),
}


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


def read_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


contract = read_json(
    CONTRACT_PATH,
    "Äußerer Fachmutations-RPC-Vertrag",
)

expected_top_level_keys = {
    "version",
    "contractVersion",
    "status",
    "productiveReleaseAllowed",
    "implementationPresent",
    "publicInterface",
    "serverDerivedValues",
    "internalHelpers",
    "executionOrder",
    "payloadRules",
    "reservationDecisionMatrix",
    "transactionRules",
    "clientResponse",
    "securityRules",
    "unresolvedRequirements",
}

if set(contract) != expected_top_level_keys:
    fail(
        "Unerwartete äußere RPC-Vertragsfelder: "
        f"{sorted(set(contract) - expected_top_level_keys)}"
    )

if contract["version"] != "v27.31k":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31k.")

if contract["contractVersion"] != 1:
    fail("Äußerer RPC-Vertrag besitzt nicht Schema 1.")

if contract["status"] != "prepared_not_live":
    fail("Äußerer RPC-Vertrag ist nicht vorbereitet.")

if contract["productiveReleaseAllowed"] is not False:
    fail("Produktive Freigabe darf noch nicht erlaubt sein.")

if contract["implementationPresent"] is not False:
    fail("Äußerer RPC darf in v27.31k noch nicht umgesetzt sein.")

expected_allowed_parameters = [
    {
        "name": "p_client_request_key",
        "type": "text",
    },
    {
        "name": "p_operation_scope",
        "type": "text",
    },
    {
        "name": "p_operation",
        "type": "text",
    },
    {
        "name": "p_resource_identity",
        "type": "text",
    },
    {
        "name": "p_domain_payload",
        "type": "jsonb",
        "default": None,
    },
]

public_interface = contract["publicInterface"]

if public_interface.get(
    "rpcType"
) != "single_security_definer_domain_mutation_rpc":
    fail("Äußerer RPC-Typ ist nicht kanonisch.")

if public_interface.get(
    "allowedParameters"
) != expected_allowed_parameters:
    fail("Erlaubte äußere RPC-Parameter sind nicht kanonisch.")

expected_forbidden_parameters = [
    "p_external_operation_id",
    "p_operation_identity",
    "p_payload_fingerprint",
    "p_client_request_key_hash",
    "p_request_fingerprint",
    "p_auth_user_id",
    "p_participant_id",
    "p_result_payload",
    "p_failure_code",
    "p_status",
]

if public_interface.get(
    "forbiddenParameters"
) != expected_forbidden_parameters:
    fail("Verbotene äußere RPC-Parameter sind unvollständig.")

for parameter in expected_allowed_parameters:
    if parameter["name"] in expected_forbidden_parameters:
        fail(
            "Parameter gleichzeitig erlaubt und verboten: "
            f"{parameter['name']}"
        )

for field in (
    "authenticatedExecutionOnly",
):
    if public_interface.get(field) is not True:
        fail(f"Äußere RPC-Regel fehlt: {field}")

for field in (
    "publicExecutionAllowed",
    "anonExecutionAllowed",
):
    if public_interface.get(field) is not False:
        fail(f"Unsichere äußere RPC-Regel: {field}")

expected_server_values = {
    "authUserId": "auth_uid_only",
    "payloadFingerprint": "sha256_canonical_json",
    "externalOperationId": (
        "internal_operation_identity_issuance_helper"
    ),
    "operationIdentity": (
        "internal_idempotency_reservation_helper"
    ),
    "clientMaySupplyDerivedValues": False,
    "externalOperationIdReturnedToClient": False,
    "internalFingerprintsReturnedToClient": False,
}

if contract["serverDerivedValues"] != expected_server_values:
    fail("Serverseitig abgeleitete Werte sind nicht kanonisch.")

expected_helpers = {
    "issuance": (
        "public."
        "accaoui_issue_exam_history_operation_identity"
    ),
    "reservation": (
        "public."
        "accaoui_reserve_exam_history_idempotency_operation"
    ),
    "completion": (
        "public."
        "accaoui_complete_exam_history_idempotency_operation"
    ),
    "directClientExecutionAllowed": False,
}

if contract["internalHelpers"] != expected_helpers:
    fail("Interne Helper-Zuordnung ist nicht kanonisch.")

expected_order = [
    "authenticate_and_validate",
    "canonicalize_domain_payload",
    "derive_payload_fingerprint",
    "issue_or_reuse_operation_identity",
    "reserve_idempotency_operation",
    "branch_on_reservation_status",
    "execute_domain_mutation_only_when_reserved_new",
    "complete_operation",
    "return_canonical_client_response",
]

if contract["executionOrder"] != expected_order:
    fail("Äußere RPC-Ausführungsreihenfolge ist ungültig.")

expected_payload_rules = {
    "writeRequiresJsonObject": True,
    "deleteRequiresNullPayload": True,
    "writeFingerprintDerivedServerSide": True,
    "deleteFingerprintIsNull": True,
    "rawPayloadStoredInIssuanceTable": False,
    "rawPayloadStoredInIdempotencyTable": False,
    "scopeSpecificSchemaStillRequired": True,
}

if contract["payloadRules"] != expected_payload_rules:
    fail("Äußere RPC-Payload-Regeln sind nicht kanonisch.")

expected_matrix = [
    {
        "status": "reserved_new",
        "executeDomainMutation": True,
        "completeOperation": True,
        "responseSource": "new_canonical_domain_result",
    },
    {
        "status": "reserved_existing_pending",
        "executeDomainMutation": False,
        "completeOperation": False,
        "responseSource": "canonical_in_progress_response",
    },
    {
        "status": "reserved_existing_completed",
        "executeDomainMutation": False,
        "completeOperation": False,
        "responseSource": "stored_canonical_result",
    },
    {
        "status": "reserved_existing_failed",
        "executeDomainMutation": False,
        "completeOperation": False,
        "responseSource": "stored_stable_failure",
    },
]

if contract["reservationDecisionMatrix"] != expected_matrix:
    fail("Äußere RPC-Reservierungslogik ist ungültig.")

expected_transaction_rules = {
    "singleDatabaseTransactionRequired": True,
    "successfulMutationAndCompletionCommitTogether": True,
    "expectedDomainFailureRollsBackMutationBeforeFailedCompletion": True,
    "unexpectedFailureRollsBackEntireTransaction": True,
    "terminalOverwriteAllowed": False,
    "pendingReexecutionAllowed": False,
    "terminalReexecutionAllowed": False,
    "completionWithoutReservationAllowed": False,
}

if contract["transactionRules"] != expected_transaction_rules:
    fail("Äußere RPC-Transaktionsregeln sind nicht kanonisch.")

expected_response = {
    "allowedFields": [
        "outcome",
        "operation_status",
        "result",
        "failure_code",
        "retryable",
    ],
    "forbiddenFields": [
        "external_operation_id",
        "operation_identity",
        "auth_user_id",
        "participant_id",
        "client_request_key_hash",
        "request_fingerprint",
        "payload_fingerprint",
        "raw_database_error",
    ],
    "rawDatabaseErrorsAllowed": False,
}

if contract["clientResponse"] != expected_response:
    fail("Äußere RPC-Clientantwort ist nicht kanonisch.")

expected_security = {
    "authUserFromAuthUidOnly": True,
    "directHelperGrantAllowed": False,
    "directTableGrantAllowed": False,
    "serviceRoleInFrontendAllowed": False,
    "browserOperationIdAllowed": False,
    "browserFingerprintAllowed": False,
    "liveExecution": False,
}

if contract["securityRules"] != expected_security:
    fail("Äußere RPC-Sicherheitsregeln sind nicht kanonisch.")

expected_unresolved = {
    "scopeSpecificPayloadSchemas": True,
    "outerDomainMutationRpcImplementation": True,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
    "authorizationTests": True,
}

if contract["unresolvedRequirements"] != expected_unresolved:
    fail("Offene äußere RPC-Anforderungen sind unvollständig.")

issuance_contract = read_json(
    ISSUANCE_CONTRACT_PATH,
    "Operations-ID-Ausstellungsvertrag",
)

transaction_contract = read_json(
    TRANSACTION_CONTRACT_PATH,
    "Transaktionaler Fachmutationsvertrag",
)

if issuance_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail("Ausstellungsvertrag ist unerwartet produktiv.")

if transaction_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail("Transaktionsvertrag ist unerwartet produktiv.")

if transaction_contract.get(
    "identity",
    {},
).get(
    "operationIdentityInputAllowed"
) is not False:
    fail(
        "Transaktionsvertrag erlaubt externe Operations-ID."
    )

if transaction_contract.get(
    "identity",
    {},
).get(
    "browserGeneratedAllowed"
) is not False:
    fail(
        "Transaktionsvertrag erlaubt browsergenerierte UUID."
    )

if transaction_contract.get(
    "unresolvedRequirements",
    {},
).get(
    "domainMutationRpcImplementation"
) is not True:
    fail("Äußerer Fachmutations-RPC darf noch nicht umgesetzt sein.")

for helper_name, migration_name in HELPER_MIGRATIONS.items():
    migration_path = MIGRATIONS / migration_name

    if not migration_path.is_file():
        fail(f"Interne Helper-Migration fehlt: {migration_name}")

    sql = migration_path.read_text(
        encoding="utf-8"
    )

    sql_without_comments = re.sub(
        r"--.*?$",
        "",
        sql.lower(),
        flags=re.MULTILINE,
    )

    if helper_name not in sql_without_comments:
        fail(f"Interner Helper fehlt: {helper_name}")

    if "security definer" not in sql_without_comments:
        fail(f"Security Definer fehlt: {helper_name}")

    if "set search_path = pg_catalog, public" not in sql_without_comments:
        fail(f"Fester search_path fehlt: {helper_name}")

    if "grant execute" in sql_without_comments:
        fail(f"Direktes Helper-Grant gefunden: {helper_name}")

v2731k_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731k*.sql")
)

if v2731k_sql_files:
    fail(
        "v27.31k darf keine SQL-Migration erzeugen: "
        f"{v2731k_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend_text = frontend_path.read_text(
        encoding="utf-8"
    ).lower()

    if CONTRACT_PATH.name.lower() in frontend_text:
        fail(
            "Äußerer RPC-Vertrag darf nicht im Frontend "
            f"geladen werden: {frontend_path.name}"
        )

print("Äußerer Fachmutations-RPC-Schnittstellenvertrag: OK")
print(
    "Browserparameter: Client-Schlüssel, Bereich, Operation, "
    "Ressource und Fach-Payload"
)
print(
    "Browser-Operations-ID und Browser-Fingerprint: "
    "vollständig ausgeschlossen"
)
print(
    "Serverableitung: Nutzer, Payload-Fingerprint und "
    "Operations-UUID intern"
)
print(
    "Reihenfolge: ausstellen, reservieren, verzweigen, "
    "mutieren und abschließen"
)
print(
    "Fachmutation: ausschließlich bei reserved_new erlaubt"
)
print(
    "Clientantwort: keine UUID, internen Fingerprints oder "
    "rohen Datenbankfehler"
)
print("Äußerer RPC implementiert: nein")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
