from pathlib import Path
import ast
import builtins
import copy
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-plan-acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-plan-contract.json"
)
PLAN_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_plan.py"
)
GUARD_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_plan_"
    "acceptance_guard.py"
)
FUTURE_ADAPTER = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
)
FUTURE_EXECUTION = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution.py"
)

LOCKED_FLAGS = ['adapterImplemented', 'adapterInvoked', 'registryReadPerformed', 'registryWritePerformed', 'atomicCompareAndSetPerformed', 'authorizationConsumed', 'authorizationGranted', 'authorizationTokenGenerated', 'trustedClockRead', 'filesystemReadPerformed', 'filesystemMutationPerformed', 'processExecuted', 'networkExecuted', 'driverImported', 'databaseConnectionCreated', 'databaseTestExecuted', 'sqlMigrationCreated', 'frontendIntegration', 'executionGrant']
SUCCESS_STATUS = (
    "accepted_atomic_consumption_registry_adapter_execution_plan_"
    "execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_plan_"
    "accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_execution_plan_acceptance_"
    "blocked_execution_locked"
)


def fail(message):
    print(f"FEHLER: {message}")
    raise SystemExit(1)


def load_json(path, label):
    if not path.is_file():
        fail(f"{label} fehlt.")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"Modul ist nicht ladbar: {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clone(value):
    return copy.deepcopy(value)


def iter_scalar_paths(value, prefix=()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from iter_scalar_paths(item, prefix + (key,))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_scalar_paths(item, prefix + (index,))
    else:
        yield prefix


def set_path(value, path):
    current = value
    for part in path[:-1]:
        current = current[part]
    key = path[-1]
    old = current[key]
    if isinstance(old, bool):
        current[key] = not old
    elif isinstance(old, int):
        current[key] = old + 1
    elif old is None:
        current[key] = "tampered"
    else:
        current[key] = str(old) + "_tampered"


def assert_blocked(result, label):
    if result.get("status") != BLOCKED_STATUS:
        fail(f"Manipulation nicht blockiert: {label}")
    if result.get("accepted") is not False:
        fail(f"Manipulation meldet Annahme: {label}")
    if result.get("acceptedPlan") is not None:
        fail(f"Blockiertes Ergebnis enthält Plan: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockiertes Ergebnis öffnet Grenze {key}: {label}")


contract = load_json(CONTRACT, "v27.33f-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.33e-Quellvertrag")

if contract.get("version") != "v27.33f":
    fail("Annahmevertrag besitzt nicht v27.33f.")
if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "plan_acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")
if source_contract.get("version") != "v27.33e":
    fail("Quellvertrag besitzt nicht v27.33e.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "plan_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if source_contract.get("implementation", {}).get(
    "executionPlanImplemented"
) is not True:
    fail("Quell-Ausführungsplan ist nicht implementiert.")

implementation = contract.get("implementation", {})
if implementation.get("executionPlanAcceptanceGuardImplemented") is not True:
    fail("Plan-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == "executionPlanAcceptanceGuardImplemented":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")
for key, value in contract.get("securityBoundary", {}).items():
    if value is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")
for key, value in contract.get("futureBoundary", {}).items():
    if value is not False:
        fail(f"Zukunftsgrenze ist offen: {key}")

source = GUARD_MODULE.read_text(encoding="utf-8")
tree = ast.parse(source)
allowed_imports = {"__future__", "collections", "copy", "json"}
seen = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen.add(alias.name.split(".", 1)[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        seen.add(node.module.split(".", 1)[0])
if seen - allowed_imports:
    fail(f"Annahme-Guard besitzt unerlaubte Importe: {seen - allowed_imports}")
for marker in (
    "open(", "read_text(", "read_bytes(", "write_text(", "write_bytes(",
    "datetime.now(", "time.time(", "uuid4(", "urandom(",
    "compare_and_set(", "registry.read", "registry.write", "adapter.invoke",
    "subprocess", ".connect(", "postgres://", "postgresql://",
    "database_url", "service_role",
):
    if marker in source.lower():
        fail(f"Annahme-Guard enthält verbotenen Inhalt: {marker}")

plan_module = load_module(PLAN_MODULE, "execution_plan_v2733f")
guard_module = load_module(GUARD_MODULE, "plan_acceptance_v2733f")
resolve_plan = getattr(
    plan_module,
    "resolve_atomic_consumption_registry_adapter_execution_plan",
    None,
)
accept_plan = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_execution_plan",
    None,
)
expected_readiness = getattr(plan_module, "_EXPECTED_READINESS", None)
locked_flags = getattr(plan_module, "_LOCKED_FLAGS", None)
if not callable(resolve_plan):
    fail("Plan-Resolver fehlt.")
if not callable(accept_plan):
    fail("Plan-Annahme fehlt.")
if not isinstance(expected_readiness, dict):
    fail("Kanonische Quell-Readiness fehlt.")
if not isinstance(locked_flags, tuple):
    fail("Gesperrte Ergebnisflags fehlen.")

accepted_readiness = {
    "status": (
        "accepted_atomic_consumption_registry_adapter_execution_"
        "readiness_execution_locked"
    ),
    "reason": (
        "authorization_atomic_consumption_registry_adapter_execution_"
        "readiness_accepted_execution_locked"
    ),
    "accepted": True,
    "acceptedReadiness": clone(expected_readiness),
    **{key: False for key in locked_flags},
}
operation = {
    "operationId": "operation-v2733f-001",
    "requestId": "request-v2733f-001",
    "authorizationNonce": "nonce-v2733f-001",
    "planFingerprint": "fingerprint-v2733f-001",
    "actorId": "actor-v2733f-001",
    "purpose": "materialize-disposable-postgresql-test-environment",
    "expectedState": "unused",
    "desiredState": "consumed",
    "consumptionRecord": {
        "recordVersion": 1,
        "operationId": "operation-v2733f-001",
        "requestId": "request-v2733f-001",
        "authorizationNonce": "nonce-v2733f-001",
        "planFingerprint": "fingerprint-v2733f-001",
        "actorId": "actor-v2733f-001",
        "purpose": "materialize-disposable-postgresql-test-environment",
        "expectedState": "unused",
        "desiredState": "consumed",
        "confirmed": False,
    },
    "evidenceTemplate": {
        "evidenceVersion": 1,
        "operationId": "operation-v2733f-001",
        "recordSource": "confirmed_consumption_record_only",
        "confirmedRecordRequired": True,
        "unconfirmedEvidenceAllowed": False,
    },
}
plan_result = resolve_plan({
    "acceptedExecutionReadinessResult": accepted_readiness,
    "operationFacts": clone(operation),
})
if plan_result.get("status") != (
    "atomic_consumption_registry_adapter_execution_plan_"
    "ready_execution_locked"
):
    fail("Quell-Plan liefert keinen Erfolgsstatus.")

before = clone(plan_result)
original_open = builtins.open


def forbidden_open(*args, **kwargs):
    raise AssertionError("Plan-Annahme darf keine Datei öffnen.")


builtins.open = forbidden_open
try:
    accepted = accept_plan(plan_result)
    again = accept_plan(plan_result)
finally:
    builtins.open = original_open

if plan_result != before:
    fail("Plan-Annahme hat die Eingabe verändert.")
if accepted != again:
    fail("Plan-Annahme ist nicht deterministisch.")
if accepted.get("status") != SUCCESS_STATUS:
    fail("Gültiger Plan wurde nicht angenommen.")
if accepted.get("reason") != SUCCESS_REASON:
    fail("Annahmegrund ist ungültig.")
if accepted.get("accepted") is not True:
    fail("Annahmeflag fehlt.")
if accepted.get("acceptedPlan") != plan_result.get("plan"):
    fail("Angenommener Plan ist nicht kanonisch.")
if accepted.get("acceptedPlan") is plan_result.get("plan"):
    fail("Angenommener Plan ist keine Tiefenkopie.")
for key in LOCKED_FLAGS:
    if accepted.get(key) is not False:
        fail(f"Annahme-Ergebnisflag ist offen: {key}")

assert_blocked(accept_plan(None), "Nicht-Mapping")
missing = clone(plan_result)
missing.pop("plan")
assert_blocked(accept_plan(missing), "fehlendes Feld")
unknown = clone(plan_result)
unknown["unknown"] = True
assert_blocked(accept_plan(unknown), "unbekanntes Feld")
wrong_status = clone(plan_result)
wrong_status["status"] = "wrong"
assert_blocked(accept_plan(wrong_status), "falscher Status")
wrong_reason = clone(plan_result)
wrong_reason["reason"] = "wrong"
assert_blocked(accept_plan(wrong_reason), "falscher Grund")
not_ready = clone(plan_result)
not_ready["ready"] = False
assert_blocked(accept_plan(not_ready), "ready false")
opened = clone(plan_result)
opened["registryWritePerformed"] = True
assert_blocked(accept_plan(opened), "offene Quellgrenze")
wrong_plan = clone(plan_result)
wrong_plan["plan"] = []
assert_blocked(accept_plan(wrong_plan), "falscher Plan")

leaf_count = 0
for path in iter_scalar_paths(plan_result["plan"]):
    manipulated = clone(plan_result)
    set_path(manipulated["plan"], path)
    assert_blocked(accept_plan(manipulated), "Manipulation " + ".".join(map(str, path)))
    leaf_count += 1

accepted_plan = accepted["acceptedPlan"]
first_path = next(iter(iter_scalar_paths(accepted_plan)))
set_path(accepted_plan, first_path)
if accepted_plan == plan_result["plan"]:
    fail("Tiefenkopie ist mit Quelle gekoppelt.")

if FUTURE_ADAPTER.exists():
    fail("v27.33f darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33f darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733f*.sql")):
    fail("v27.33f darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Ausführungsplan-Annahme-Guard: OK")
print("Quell-Ausführungsplan: v27.33e")
print(f"Manipulierte Plan-Blätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff der Annahme: keiner")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33f: keine")
print("Produktive Freigabe: nein")
