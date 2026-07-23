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
    / "exam-history-outer-domain-mutation-database-test-contract.json"
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
E2E_AUDIT_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-e2e-audit-contract.json"
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


contract = read_json(
    CONTRACT_PATH,
    "Äußerer Fachmutations-Datenbank-Testvertrag",
)

if contract.get("version") != "v27.31w":
    fail("Datenbank-Testvertrag besitzt nicht v27.31w.")
if contract.get("contractVersion") != 1:
    fail("Datenbank-Testvertrag besitzt nicht Schema 1.")
if contract.get("status") != "prepared_not_live":
    fail("Datenbank-Testvertrag ist nicht vorbereitet.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Datenbank-Testvertrag darf nicht produktiv sein.")
if contract.get("testType") != (
    "future_disposable_database_contract"
):
    fail("Datenbank-Testvertrag besitzt falschen Testtyp.")

implementation = contract.get("implementation", {})
if implementation != {
    "outerRpc": "public.accaoui_mutate_exam_history_domain",
    "outerRpcMigrationPath": (
        "supabase/migrations/"
        "20260723_v2731u_"
        "exam_history_outer_domain_mutation_rpc.sql"
    ),
    "sourceAuditContractPath": (
        "docs/contracts/"
        "exam-history-outer-domain-mutation-e2e-audit-contract.json"
    ),
    "databaseTestCheckerPath": (
        "tools/"
        "check-supabase-exam-history-"
        "outer-domain-mutation-database-test-contract.py"
    ),
    "databaseTestDocumentPath": (
        "docs/"
        "SUPABASE_EXAM_RESULT_HISTORY_"
        "OUTER_DOMAIN_MUTATION_DATABASE_TEST_CONTRACT.md"
    ),
    "sqlMigrationCreated": False,
    "databaseTestExecuted": False,
    "liveDatabaseExecution": False,
    "frontendIntegration": False,
}:
    fail("Datenbank-Testvertragsimplementierung ist ungültig.")

environment = contract.get("environmentBoundary", {})
if environment != {
    "dedicatedDisposableDatabaseRequired": True,
    "productionDatabaseAllowed": False,
    "realParticipantDataAllowed": False,
    "syntheticUsersOnly": True,
    "migrationsAppliedInRepositoryOrder": True,
    "databaseResetBetweenCases": True,
    "testOwnerOrControlledHarnessRequired": True,
    "permanentGrantChangesAllowed": False,
    "serviceRoleInFrontendAllowed": False,
}:
    fail("Testumgebungsgrenze ist ungültig.")

authorization = contract.get("authorizationMatrix", {})
if authorization != {
    "publicDirectExecute": "permission_denied",
    "anonDirectExecute": "permission_denied",
    "authenticatedDirectExecute": "permission_denied",
    "controlledHarnessWithoutAuthUid": "authentication_required",
    "controlledHarnessWithSyntheticAuthUid": (
        "scenario_execution_allowed"
    ),
    "authUserIdInputParameterAllowed": False,
    "participantIdInputParameterAllowed": False,
    "crossUserMutationAllowed": False,
}:
    fail("Autorisierungsmatrix ist ungültig.")

retry = contract.get("retryMatrix", {})
if retry != {
    "sameClientKeySameCompletedRequest": {
        "sameTerminalResultRequired": True,
        "newDomainMutationAllowed": False,
        "newStorageVersionAllowed": False,
        "newIssuanceRowAllowed": False,
        "newReservationRowAllowed": False,
    },
    "sameClientKeyPendingRequest": {
        "outcome": "in_progress",
        "operationStatus": "pending",
        "retryable": True,
        "newDomainMutationAllowed": False,
        "completionAllowed": False,
    },
    "sameClientKeyDifferentExpectedVersion": {
        "failureCode": (
            "client_request_key_reused_with_different_request"
        ),
        "domainMutationAllowed": False,
    },
    "existingFailedRequest": {
        "sameStableFailureRequired": True,
        "newDomainMutationAllowed": False,
        "newCompletionAllowed": False,
    },
}:
    fail("Retry-Matrix ist ungültig.")

version = contract.get("versionMatrix", {})
if version != {
    "createExpectedZero": {
        "outcome": "created",
        "storedVersion": 1,
    },
    "secondIndependentCreateExpectedZero": {
        "failureCode": "domain_storage_version_conflict",
        "storedVersionUnchanged": True,
    },
    "updateExactCurrentVersion": {
        "outcome": "updated",
        "incrementsVersionBy": 1,
    },
    "staleUpdate": {
        "failureCode": "domain_storage_version_conflict",
        "storedVersionUnchanged": True,
    },
    "deleteExactCurrentVersion": {
        "outcome": "deleted",
        "incrementsVersionBy": 1,
        "tombstoneRequired": True,
    },
    "staleDelete": {
        "failureCode": "domain_storage_version_conflict",
        "storedVersionUnchanged": True,
    },
    "alreadyDeletedExactVersion": {
        "outcome": "already_deleted",
        "storedVersionUnchanged": True,
    },
}:
    fail("Versionskonfliktmatrix ist ungültig.")

concurrency = contract.get("concurrencyMatrix", {})
if concurrency != {
    "twoIndependentWritesSameExpectedVersion": {
        "exactlyOneMutationSucceeds": True,
        "exactlyOneVersionConflict": True,
        "finalVersionIncrementsBy": 1,
        "silentLastWriteWinsAllowed": False,
    },
    "twoIndependentCreatesSameIdentity": {
        "exactlyOneCreateSucceeds": True,
        "exactlyOneClosedConflict": True,
        "finalRowCount": 1,
        "uniqueConflictReevaluationRequired": True,
    },
}:
    fail("Konkurrenzmatrix ist ungültig.")

rollback = contract.get("rollbackMatrix", {})
if rollback != {
    "expectedDomainFailure": {
        "innerMutationRolledBack": True,
        "failedIdempotencyStatePersisted": True,
        "stableFailureCodeRequired": True,
        "retryReturnsSameFailure": True,
        "rawDatabaseErrorAllowed": False,
    },
    "unexpectedInjectedFailure": {
        "wholeOuterCallRolledBack": True,
        "issuanceRowPersisted": False,
        "reservationRowPersisted": False,
        "domainRowChangePersisted": False,
        "failedTerminalStatePersisted": False,
        "productionFaultHookAllowed": False,
        "testOnlyFaultInjectionRequired": True,
    },
}:
    fail("Rollback-Testmatrix ist ungültig.")

observation = contract.get("observationBoundary", {})
if observation != {
    "internalTableInspectionAllowedOnlyInHarness": True,
    "clientMayReceiveInternalRows": False,
    "allowedClientColumns": [
        "outcome",
        "operation_status",
        "result",
        "failure_code",
        "retryable",
    ],
    "internalUuidExposureAllowed": False,
    "fingerprintExposureAllowed": False,
    "rawDatabaseErrorExposureAllowed": False,
}:
    fail("Testbeobachtungsgrenze ist ungültig.")

if contract.get("unresolvedRequirements") != {
    "disposableDatabaseHarness": True,
    "syntheticFixtureCatalog": True,
    "testOnlyFaultInjectionMechanism": True,
    "databaseTestExecution": True,
    "concurrencyTestExecution": True,
    "authorizationTestExecution": True,
    "directAppExecutionGrant": True,
    "frontendIntegration": True,
}:
    fail("Offene Datenbank-Testanforderungen sind ungültig.")

outer = read_json(
    OUTER_CONTRACT_PATH,
    "Äußerer Fachmutations-RPC-Vertrag",
)
if outer.get("version") != "v27.31u":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31u.")
if outer.get("implementationPresent") is not True:
    fail("Äußerer RPC ist nicht vorbereitet.")
if outer.get("productiveReleaseAllowed") is not False:
    fail("Äußerer RPC ist unerwartet produktiv.")

transaction = read_json(
    TRANSACTION_CONTRACT_PATH,
    "Transaktionaler Fachmutationsvertrag",
)
if transaction.get("version") != "v27.31u":
    fail("Transaktionsvertrag besitzt nicht v27.31u.")
if transaction.get("productiveReleaseAllowed") is not False:
    fail("Transaktionsvertrag ist unerwartet produktiv.")

audit = read_json(
    E2E_AUDIT_CONTRACT_PATH,
    "Äußerer Fachmutations-End-to-End-Auditvertrag",
)
if audit.get("version") != "v27.31v":
    fail("End-to-End-Auditvertrag besitzt nicht v27.31v.")
if audit.get("auditType") != "static_source_audit":
    fail("End-to-End-Audit ist nicht statisch.")
if audit.get("productiveReleaseAllowed") is not False:
    fail("End-to-End-Audit ist unerwartet produktiv.")

if not OUTER_SQL_PATH.is_file():
    fail("Äußerer Fachmutations-RPC fehlt.")

sql = OUTER_SQL_PATH.read_text(encoding="utf-8")
sql_without_comments = re.sub(
    r"--.*?$",
    "",
    sql,
    flags=re.MULTILINE,
)
sql_compact = re.sub(
    r"\s+",
    " ",
    sql_without_comments.lower(),
).strip()

required_sql_markers = (
    "v_auth_user_id := auth.uid()",
    "message = 'authentication_required'",
    "public.accaoui_issue_exam_history_operation_identity(",
    "public.accaoui_reserve_exam_history_idempotency_operation(",
    "public.accaoui_mutate_exam_history_domain_resource(",
    "public.accaoui_complete_exam_history_idempotency_operation(",
    "'reserved_existing_pending'",
    "'reserved_existing_completed'",
    "'reserved_existing_failed'",
    "'reserved_new'",
    "'domain_storage_version_conflict'",
    "get stacked diagnostics v_failure_code = message_text",
)
for marker in required_sql_markers:
    if marker not in sql_compact:
        fail(f"Testvertragsgrundlage fehlt im äußeren RPC: {marker}")

if "when others" in sql_compact:
    fail("Unerwartete Fehler werden im äußeren RPC abgefangen.")
if "grant execute" in sql_compact:
    fail("Äußerer RPC besitzt bereits eine Ausführungsfreigabe.")
if "service_role" in sql_compact:
    fail("Service-Role ist im äußeren RPC referenziert.")

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

v2731w_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2731w*.sql")
)
if v2731w_sql_files:
    fail(
        "v27.31w ist nur ein Datenbank-Testvertrag und darf "
        f"keine SQL-Migration erzeugen: {v2731w_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend = frontend_path.read_text(encoding="utf-8").lower()

    for forbidden_reference in (
        "accaoui_mutate_exam_history_domain",
        CONTRACT_PATH.name.lower(),
    ):
        if forbidden_reference in frontend:
            fail(
                "Datenbank-Testvertrag oder äußerer RPC wird "
                f"im Frontend referenziert: "
                f"{frontend_path.name}: {forbidden_reference}"
            )

print("Äußerer Fachmutations-Datenbank-Testvertrag: OK")
print("Umgebung: ausschließlich disposable und synthetisch")
print("App-Rollen: direkte Ausführung weiterhin gesperrt")
print("Authentifizierung: auth.uid ausschließlich intern")
print("Retry: Pending, Completed und Failed eindeutig festgelegt")
print("Versionskonflikte: Create, Update und Delete vollständig")
print("Konkurrenz: genau ein Gewinner, geschlossener Verlierer")
print("Rollback: erwarteter Teilrollback, unerwarteter Gesamtrollback")
print("Interne Beobachtung: ausschließlich kontrollierter Test-Harness")
print("SQL-Migration v27.31w: keine")
print("Datenbanktest ausgeführt: nein")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
