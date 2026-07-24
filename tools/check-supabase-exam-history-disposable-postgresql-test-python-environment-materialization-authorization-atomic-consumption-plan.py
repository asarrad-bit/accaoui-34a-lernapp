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
        "authorization-atomic-consumption-plan-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-operation-contract.json"
    )
)
PLAN = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_plan.py"
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
    "v27.32s-Atomarer-Verbrauchsplan-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32r-Atomarer-Verbrauchsoperationsvertrag",
)

if contract.get("version") != "v27.32s":
    fail("Planvertrag besitzt nicht v27.32s.")
if contract.get("contractVersion") != 1:
    fail("Planvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_plan_execution_locked"
):
    fail("Planvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Planvertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32r":
    fail("Quellvertrag besitzt nicht v27.32r.")
if source.get("implementation", {}).get(
    "atomicConsumptionPlanImplemented"
) is not False:
    fail("Quellvertrag hatte unerwartet bereits einen Plan.")

implementation = contract.get("implementation", {})
if implementation.get("atomicConsumptionPlanImplemented") is not True:
    fail("Atomarer Verbrauchsplan fehlt.")

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

plan_source = PLAN.read_text(encoding="utf-8")
tree = ast.parse(plan_source)

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
    fail(f"Plan besitzt unerlaubte Importe: {unexpected_imports}")

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
        fail(f"Plan verwendet verbotenen Namen: {node.id}")

lower_source = plan_source.lower()

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
        fail(f"Plan enthält verbotenen Inhalt: {marker}")

module = load_module(
    PLAN,
    "accaoui_atomic_consumption_plan_v2732s",
)
build_plan = getattr(
    module,
    "build_materialization_authorization_atomic_consumption_plan",
    None,
)

if not callable(build_plan):
    fail("Atomare Verbrauchsplan-Funktion fehlt.")

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

accepted_result = {
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

valid_facts = {
    "acceptedReadinessResult": accepted_result,
    "operationId": "123e4567-e89b-42d3-a456-426614174999",
    "operationAttempt": 1,
    "adapterFacts": adapter_facts,
}

cases = [
    (
        [],
        "blocked",
        "authorization_atomic_consumption_plan_invalid_input",
    ),
    (
        {
            key: value
            for key, value in valid_facts.items()
            if key != "operationId"
        },
        "blocked",
        "authorization_atomic_consumption_plan_missing_fields",
    ),
    (
        {
            **valid_facts,
            "unexpected": True,
        },
        "blocked",
        "authorization_atomic_consumption_plan_unknown_fields",
    ),
    (
        {
            **valid_facts,
            "operationAttempt": 2,
        },
        "blocked",
        "authorization_atomic_consumption_plan_operation_invalid",
    ),
    (
        {
            **valid_facts,
            "adapterFacts": {
                **adapter_facts,
                "maximumParallelWinners": 2,
            },
        },
        "blocked",
        "authorization_atomic_consumption_plan_adapter_invalid",
    ),
    (
        valid_facts,
        "atomic_consumption_plan_ready_execution_locked",
        (
            "authorization_atomic_consumption_plan_"
            "ready_execution_locked"
        ),
    ),
]

for facts, expected_status, expected_reason in cases:
    before = clone(facts) if isinstance(facts, dict) else facts
    first = build_plan(facts)
    second = build_plan(facts)

    if first != second:
        fail("Atomarer Verbrauchsplan ist nicht deterministisch.")

    if isinstance(facts, dict) and facts != before:
        fail("Atomarer Verbrauchsplan verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Planstatus ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Plangrund ist ungültig: {first}")

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
            fail(f"Plan-Ausführungsgrenze ist offen: {key}")

result = build_plan(valid_facts)
plan = result.get("plan")

if not isinstance(plan, dict):
    fail("Gültiger atomarer Verbrauchsplan fehlt.")

if plan.get("operationAttempt") != 1:
    fail("Operationsversuch ist ungültig.")
if plan.get("adapter", {}).get("invocationAllowed") is not False:
    fail("Adapteraufruf darf nicht erlaubt sein.")
if plan.get("compareAndSet") != {
    "expectedState": "unused",
    "desiredState": "consumed",
    "atomic": True,
    "withConsumptionRecord": True,
    "executionAllowed": False,
}:
    fail("Compare-and-set-Plan ist ungültig.")
if plan.get("consumptionRecord", {}).get("executionGrant") is not False:
    fail("Verbrauchsrecord darf keine Freigabe enthalten.")
if plan.get("receiptTemplate", {}).get("status") != (
    "authorization_consumed_execution_locked"
):
    fail("Nachweisvorlagenstatus ist ungültig.")
if plan.get("errors", {}).get("automaticRetryAllowed") is not False:
    fail("Automatischer Retry darf nicht erlaubt sein.")
if plan.get("rollback", {}).get(
    "postCommitResetToUnusedAllowed"
) is not False:
    fail("Post-Commit-Reset darf nicht erlaubt sein.")

if list(MIGRATIONS.glob("*v2732s*.sql")):
    fail("v27.32s darf keine SQL-Migration erzeugen.")

print("Atomarer Autorisierungsverbrauchsoperations-Plan: OK")
print("Quellvertrag: v27.32r")
print("Quellstatus: accepted_consumption_ready_execution_locked")
print("Adapterfähigkeit: geprüft")
print("Registry-Key: strukturiert")
print("Compare-and-set: unused -> consumed")
print("Verbrauchsrecord und Nachweisvorlage: strukturiert")
print("Konflikt- und Fehlerregeln: strukturiert")
print("Ergebnis: atomic_consumption_plan_ready_execution_locked")
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
print("SQL-Migration v27.32s: keine")
print("Produktive Freigabe: nein")
