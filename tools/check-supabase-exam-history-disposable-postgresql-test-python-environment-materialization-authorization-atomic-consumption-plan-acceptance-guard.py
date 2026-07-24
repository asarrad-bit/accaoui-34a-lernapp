from pathlib import Path
import ast
import base64
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-plan-"
        "acceptance-guard-contract.json"
    )
)
SOURCE_CONTRACT = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-plan-contract.json"
    )
)
SOURCE_PLAN = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_plan.py"
    )
)
GUARD = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_"
        "plan_acceptance_guard.py"
    )
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    raise SystemExit(1)


def load_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        fail(f"Modul ist nicht ladbar: {path.name}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clone(value):
    return json.loads(json.dumps(value))


contract = load_json(
    CONTRACT,
    "v27.32t-Atomarer-Plan-Annahmevertrag",
)
source_contract = load_json(
    SOURCE_CONTRACT,
    "v27.32s-Atomarer-Verbrauchsplan-Vertrag",
)

if contract.get("version") != "v27.32t":
    fail("Annahmevertrag besitzt nicht v27.32t.")
if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_plan_"
    "acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Annahmevertrag darf nicht produktiv sein.")

if source_contract.get("version") != "v27.32s":
    fail("Quellvertrag besitzt nicht v27.32s.")
if source_contract.get("implementation", {}).get(
    "atomicConsumptionPlanImplemented"
) is not True:
    fail("Quell-Operationsplan ist nicht implementiert.")
if source_contract.get("planBoundary", {}).get(
    "successStatus"
) != "atomic_consumption_plan_ready_execution_locked":
    fail("Quellplan besitzt falschen Erfolgsstatus.")

implementation = contract.get("implementation", {})

if implementation.get(
    "atomicConsumptionPlanAcceptanceGuardImplemented"
) is not True:
    fail("Atomarer Plan-Annahme-Guard fehlt.")

for key in (
    "registryAdapterImplemented",
    "registryReadPerformed",
    "registryWritePerformed",
    "atomicCompareAndSetPerformed",
    "consumptionRecordCommitted",
    "consumptionReceiptCommitted",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
    "trustedClockRead",
    "filesystemReadPerformed",
    "filesystemMutationPerformed",
    "processExecuted",
    "virtualEnvironmentCreated",
    "dependencyInstalled",
    "driverImported",
    "databaseConnectionCreated",
    "databaseTestExecuted",
    "sqlMigrationCreated",
    "frontendIntegration",
):
    if implementation.get(key) is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

guard_source = GUARD.read_text(encoding="utf-8")
tree = ast.parse(guard_source)

allowed_imports = {
    "__future__",
    "collections",
    "datetime",
    "base64",
    "hashlib",
    "re",
}
seen_imports = set()

for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen_imports.add(alias.name.split(".", 1)[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        seen_imports.add(node.module.split(".", 1)[0])

unexpected_imports = seen_imports - allowed_imports

if unexpected_imports:
    fail(f"Annahme-Guard besitzt unerlaubte Importe: {unexpected_imports}")

forbidden_names = {
    "Path",
    "os",
    "sys",
    "subprocess",
    "shutil",
    "venv",
    "socket",
    "requests",
    "urllib",
    "uuid",
    "secrets",
    "time",
}

for node in ast.walk(tree):
    if isinstance(node, ast.Name) and node.id in forbidden_names:
        fail(f"Annahme-Guard verwendet verbotenen Namen: {node.id}")

lower_source = guard_source.lower()

for marker in (
    "datetime.now(",
    "datetime.utcnow(",
    "time.time(",
    "uuid4(",
    "urandom(",
    "compare_and_set(",
    "registry.read",
    "registry.write",
    "adapter.invoke",
    "pip install",
    "python -m venv",
    "py -m venv",
    "subprocess",
    ".connect(",
    "postgres://",
    "postgresql://",
    "database_url",
    "service_role",
):
    if marker in lower_source:
        fail(f"Annahme-Guard enthält verbotenen Inhalt: {marker}")

plan_module = load_module(
    SOURCE_PLAN,
    "accaoui_atomic_plan_source_v2732t",
)
guard_module = load_module(
    GUARD,
    "accaoui_atomic_plan_acceptance_v2732t",
)

build_plan = getattr(
    plan_module,
    "build_materialization_authorization_atomic_consumption_plan",
    None,
)
accept_plan = getattr(
    guard_module,
    "accept_materialization_authorization_atomic_consumption_plan",
    None,
)

if not callable(build_plan):
    fail("Quell-Operationsplan-Funktion fehlt.")
if not callable(accept_plan):
    fail("Plan-Annahme-Funktion fehlt.")

nonce = base64.urlsafe_b64encode(bytes(range(32))).decode(
    "ascii"
).rstrip("=")
nonce_fingerprint = hashlib.sha256(
    nonce.encode("ascii")
).hexdigest()

readiness = {
    "requestId": "123e4567-e89b-42d3-a456-426614174000",
    "requestNonceFingerprint": nonce_fingerprint,
    "acceptedPlanFingerprint": "a" * 64,
    "actor": {
        "kind": "human_operator",
        "id": "local-test-operator",
    },
    "purpose": (
        "disposable_test_python_environment_materialization"
    ),
    "issuedAt": "2026-07-24T10:00:00Z",
    "approvedAt": "2026-07-24T10:01:00Z",
    "expiresAt": "2026-07-24T10:05:00Z",
    "consumedAt": "2026-07-24T10:02:00Z",
    "registryKey": {
        "requestId": "123e4567-e89b-42d3-a456-426614174000",
        "requestNonce": nonce,
        "acceptedPlanFingerprint": "a" * 64,
    },
    "registryState": "unused",
    "compareState": "unused",
    "setState": "consumed",
    "singleUse": True,
    "executionGrant": False,
}

accepted_readiness_result = {
    "status": "accepted_consumption_ready_execution_locked",
    "reason": (
        "materialization_authorization_consumption_"
        "readiness_accepted_execution_locked"
    ),
    "accepted": True,
    "acceptedReadiness": readiness,
    "authorizationConsumptionAllowed": False,
    "authorizationConsumed": False,
    "authorizationGranted": False,
    "authorizationTokenGenerated": False,
    "registryReadAllowed": False,
    "registryWriteAllowed": False,
    "atomicCompareAndSetAllowed": False,
    "trustedClockReadAllowed": False,
    "environmentCreationAllowed": False,
    "filesystemReadAllowed": False,
    "filesystemMutationAllowed": False,
    "processExecutionAllowed": False,
    "dependencyInstallationAllowed": False,
}

adapter_facts = {
    "adapterKind": "single_use_consumption_registry",
    "atomicCompareAndSetWithRecord": True,
    "definitiveAlreadyConsumedOutcome": True,
    "definitiveParallelConflictOutcome": True,
    "ambiguousCommitOutcome": True,
    "reconciliationRequiredOnAmbiguous": True,
    "rawErrorSuppressed": True,
    "maximumParallelWinners": 1,
}

source_result = build_plan({
    "acceptedReadinessResult": accepted_readiness_result,
    "operationId": "123e4567-e89b-42d3-a456-426614174999",
    "operationAttempt": 1,
    "adapterFacts": adapter_facts,
})

tampered_status = clone(source_result)
tampered_status["status"] = "ready"

tampered_flag = clone(source_result)
tampered_flag["registryWriteAllowed"] = True

tampered_operation = clone(source_result)
tampered_operation["plan"]["operationAttempt"] = 2

tampered_adapter = clone(source_result)
tampered_adapter["plan"]["adapter"]["invocationAllowed"] = True

tampered_registry = clone(source_result)
tampered_registry["plan"]["registryKey"][
    "acceptedPlanFingerprint"
] = "b" * 64

tampered_compare = clone(source_result)
tampered_compare["plan"]["compareAndSet"][
    "executionAllowed"
] = True

tampered_record = clone(source_result)
tampered_record["plan"]["consumptionRecord"][
    "executionGrant"
] = True

tampered_receipt = clone(source_result)
tampered_receipt["plan"]["receiptTemplate"][
    "consumedAt"
] = "2026-07-24T10:03:00Z"

tampered_conflict = clone(source_result)
tampered_conflict["plan"]["conflicts"][
    "maximumParallelWinners"
] = 2

tampered_error = clone(source_result)
tampered_error["plan"]["errors"][
    "automaticRetryAllowed"
] = True

tampered_rollback = clone(source_result)
tampered_rollback["plan"]["rollback"][
    "postCommitResetToUnusedAllowed"
] = True

tampered_execution = clone(source_result)
tampered_execution["plan"]["execution"][
    "authorizationConsumed"
] = True

cases = [
    (
        [],
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_invalid_input",
    ),
    (
        tampered_status,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_source_status_invalid",
    ),
    (
        tampered_flag,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_boundary_open",
    ),
    (
        tampered_operation,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_operation_invalid",
    ),
    (
        tampered_adapter,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_adapter_invalid",
    ),
    (
        tampered_registry,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_record_invalid",
    ),
    (
        tampered_compare,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_compare_and_set_invalid",
    ),
    (
        tampered_record,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_record_invalid",
    ),
    (
        tampered_receipt,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_receipt_invalid",
    ),
    (
        tampered_conflict,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_conflicts_invalid",
    ),
    (
        tampered_error,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_errors_invalid",
    ),
    (
        tampered_rollback,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_rollback_invalid",
    ),
    (
        tampered_execution,
        "blocked",
        "authorization_atomic_consumption_plan_"
        "acceptance_execution_invalid",
    ),
    (
        source_result,
        "accepted_atomic_consumption_plan_execution_locked",
        "authorization_atomic_consumption_plan_"
        "accepted_execution_locked",
    ),
]

for candidate, expected_status, expected_reason in cases:
    before = clone(candidate) if isinstance(candidate, dict) else candidate
    first = accept_plan(candidate)
    second = accept_plan(candidate)

    if first != second:
        fail("Plan-Annahme ist nicht deterministisch.")

    if isinstance(candidate, dict) and candidate != before:
        fail("Plan-Annahme verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Annahmestatus ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Annahmegrund ist ungültig: {first}")

    for key in (
        "registryAdapterInvocationAllowed",
        "registryReadAllowed",
        "registryWriteAllowed",
        "atomicCompareAndSetAllowed",
        "authorizationConsumptionAllowed",
        "authorizationConsumed",
        "authorizationGranted",
        "authorizationTokenGenerated",
        "trustedClockReadAllowed",
        "environmentCreationAllowed",
        "filesystemReadAllowed",
        "filesystemMutationAllowed",
        "processExecutionAllowed",
        "dependencyInstallationAllowed",
    ):
        if first.get(key) is not False:
            fail(f"Annahme-Ausführungsgrenze ist offen: {key}")

accepted = accept_plan(source_result)

if accepted.get("accepted") is not True:
    fail("Gültiger Operationsplan wurde nicht angenommen.")

accepted_plan = accepted.get("acceptedPlan")

if not isinstance(accepted_plan, dict):
    fail("Angenommener Operationsplan fehlt.")

if accepted_plan != source_result["plan"]:
    fail("Angenommener Operationsplan weicht von Quelle ab.")

if accepted_plan is source_result["plan"]:
    fail("Annahme-Guard darf keine Quellreferenz zurückgeben.")

for nested in (
    "adapter",
    "registryKey",
    "compareAndSet",
    "consumptionRecord",
    "receiptTemplate",
    "conflicts",
    "errors",
    "rollback",
    "execution",
):
    if accepted_plan[nested] is source_result["plan"][nested]:
        fail(f"Planbereich wurde nicht kanonisch kopiert: {nested}")

if list(MIGRATIONS.glob("*v2732t*.sql")):
    fail("v27.32t darf keine SQL-Migration erzeugen.")

print("Atomarer Verbrauchsoperationsplan-Annahme-Guard: OK")
print("Quellvertrag: v27.32s")
print("Quellstatus: atomic_consumption_plan_ready_execution_locked")
print("Operations-ID und Versuch: geprüft")
print("Adapterfähigkeit und Registry-Key: geprüft")
print("Compare-and-set: unused -> consumed")
print("Record und Nachweisvorlage: geprüft")
print("Konflikt-, Fehler- und Rollbackgrenzen: geprüft")
print("Ergebnis: accepted_atomic_consumption_plan_execution_locked")
print("Adapter aufgerufen: nein")
print("Registry gelesen: nein")
print("Registry geschrieben: nein")
print("Compare-and-set ausgeführt: nein")
print("Verbrauch ausgeführt: nein")
print("Freigabe erteilt: nein")
print("Token erzeugt: nein")
print("Uhr gelesen: nein")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32t: keine")
print("Produktive Freigabe: nein")
