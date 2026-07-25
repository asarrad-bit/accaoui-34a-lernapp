from __future__ import annotations

import builtins
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-plan-acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-plan-contract.json"
)
EXECUTION_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-contract.json"
)

DESCRIPTOR_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor.py"
)
DESCRIPTOR_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_acceptance_guard.py"
)
READINESS_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness.py"
)
READINESS_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_acceptance_guard.py"
)
PLAN_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_plan.py"
)
GUARD_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_acceptance_guard.py"
)

FUTURE_ADAPTER = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
)
FUTURE_EXECUTION = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution.py"
)

LOCKED_FLAGS = (
    "adapterModuleCreated",
    "adapterInterfaceImplemented",
    "adapterFactoryImplemented",
    "adapterImported",
    "adapterInstantiated",
    "adapterInvoked",
    "registryReadPerformed",
    "registryWritePerformed",
    "atomicCompareAndSetPerformed",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
    "trustedClockRead",
    "filesystemReadPerformed",
    "filesystemMutationPerformed",
    "processExecuted",
    "networkExecuted",
    "driverImported",
    "databaseConnectionCreated",
    "databaseTestExecuted",
    "sqlMigrationCreated",
    "frontendIntegration",
    "executionGrant",
)

ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "execution_plan_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "plan_acceptance_blocked_execution_locked"
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
        fail(f"Modul nicht ladbar: {path.name}")
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
            fail(f"Blockierte Grenze offen: {key} / {label}")


contract = load_json(CONTRACT, "v27.33t-Vertrag")
source_contract = load_json(
    SOURCE_CONTRACT,
    "v27.33s-Quellvertrag",
)
execution_contract = load_json(
    EXECUTION_CONTRACT,
    "v27.33n-Ausführungsvertrag",
)

if contract.get("version") != "v27.33t":
    fail("Plan-Annahmevertrag besitzt nicht v27.33t.")
if contract.get("contractVersion") != 1:
    fail("Plan-Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_acceptance_execution_locked"
):
    fail("Plan-Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33s":
    fail("Quellvertrag besitzt nicht v27.33s.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")

implementation = contract.get("implementation", {})
if implementation.get(
    "implementationExecutionPlanAcceptanceGuardImplemented"
) is not True:
    fail("Implementierungsausführungsplan-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == (
        "implementationExecutionPlanAcceptanceGuardImplemented"
    ):
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

boundary = contract.get("acceptanceBoundary", {})
if boundary.get("requiredPlanVersion") != 1:
    fail("Planversion ist nicht gebunden.")
if boundary.get("requiredStepCount") != 12:
    fail("Zwölf Ausführungsschritte sind nicht gebunden.")
if boundary.get("executionGrant") is not False:
    fail("Annahmegrenze öffnet den Grant.")

for block in ("securityBoundary", "futureBoundary"):
    values = contract.get(block, {})
    if not isinstance(values, dict) or not values:
        fail(f"{block} fehlt.")
    for key, value in values.items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

descriptor_module = load_module(
    DESCRIPTOR_MODULE,
    "v2733t_descriptor",
)
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE_MODULE,
    "v2733t_descriptor_acceptance",
)
readiness_module = load_module(
    READINESS_MODULE,
    "v2733t_readiness",
)
readiness_acceptance_module = load_module(
    READINESS_ACCEPTANCE_MODULE,
    "v2733t_readiness_acceptance",
)
plan_module = load_module(
    PLAN_MODULE,
    "v2733t_execution_plan",
)
guard_module = load_module(
    GUARD_MODULE,
    "v2733t_execution_plan_acceptance",
)

descriptor_result = (
    descriptor_module
    .resolve_atomic_consumption_registry_adapter_implementation_execution_descriptor({
        "contractFacts": clone(execution_contract),
    })
)
accepted_descriptor = (
    descriptor_acceptance_module
    .accept_atomic_consumption_registry_adapter_implementation_execution_descriptor(
        descriptor_result
    )
)
readiness_result = (
    readiness_module
    .resolve_atomic_consumption_registry_adapter_implementation_execution_readiness({
        "acceptedExecutionDescriptorResult": accepted_descriptor,
        "executionCapabilityFacts": clone(
            readiness_module.EXPECTED_EXECUTION_CAPABILITY_FACTS
        ),
    })
)
accepted_readiness = (
    readiness_acceptance_module
    .accept_atomic_consumption_registry_adapter_implementation_execution_readiness(
        readiness_result
    )
)
plan_result = (
    plan_module
    .resolve_atomic_consumption_registry_adapter_implementation_execution_plan({
        "acceptedExecutionReadinessResult": accepted_readiness,
        "executionPlanFacts": clone(
            plan_module.EXPECTED_EXECUTION_PLAN_FACTS
        ),
    })
)

accept = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_"
    "implementation_execution_plan",
    None,
)
if not callable(accept):
    fail("Implementierungsausführungsplan-Annahme fehlt.")
if plan_result.get("ready") is not True:
    fail("Quell-Plan liefert keinen Erfolgsstatus.")

before = clone(plan_result)
original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError(
        "Ausführungsplan-Annahme darf keine Datei öffnen."
    )

builtins.open = forbidden_open
try:
    first = accept(plan_result)
    second = accept(plan_result)
finally:
    builtins.open = original_open

if plan_result != before:
    fail("Plan-Annahme hat die Eingabe verändert.")
if first != second:
    fail("Plan-Annahme ist nicht deterministisch.")
if first.get("status") != ACCEPTED_STATUS:
    fail("Erfolgsstatus ist ungültig.")
if first.get("reason") != ACCEPTED_REASON:
    fail("Erfolgsgrund ist ungültig.")
if first.get("accepted") is not True:
    fail("Annahmeflag fehlt.")
if first.get("acceptedPlan") != plan_result["plan"]:
    fail("Angenommener Plan ist nicht kanonisch.")
if first.get("acceptedPlan") is plan_result["plan"]:
    fail("Angenommener Plan ist keine Tiefenkopie.")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Ergebnisgrenze ist offen: {key}")

assert_blocked(accept(None), "Nicht-Mapping")

missing = clone(plan_result)
missing.pop("plan")
assert_blocked(accept(missing), "fehlendes Feld")

unknown = clone(plan_result)
unknown["unknown"] = True
assert_blocked(accept(unknown), "unbekanntes Feld")

opened = clone(plan_result)
opened["adapterImported"] = True
assert_blocked(accept(opened), "offene Quellgrenze")

leaf_count = 0
for path in iter_scalar_paths(plan_result):
    manipulated = clone(plan_result)
    set_path(manipulated, path)
    assert_blocked(
        accept(manipulated),
        ".".join(map(str, path)),
    )
    leaf_count += 1

source_text = GUARD_MODULE.read_text(encoding="utf-8").lower()
for forbidden in (
    "subprocess",
    "socket",
    "psycopg",
    "supabase",
    "requests",
    "urllib",
    "sqlite3",
    "os.environ",
    ".connect(",
    "registry.read",
    "registry.write",
    "adapter.invoke",
):
    if forbidden in source_text:
        fail(f"Plan-Annahme enthält verbotenen Zugriff: {forbidden}")

if FUTURE_ADAPTER.exists():
    fail("v27.33t darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33t darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733t*.sql")):
    fail("v27.33t darf keine SQL-Migration erzeugen.")

print(
    "Registry-Adapter-Implementierungsausführungsplan-"
    "Annahme-Guard: OK"
)
print("Quell-Ausführungsplan: v27.33s")
print(f"Manipulierte Planblätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff des Guards: keiner")
print("Adaptermodul erstellt: nein")
print("Adapter importiert: nein")
print("Adapter instanziiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33t: keine")
print("Produktive Freigabe: nein")
