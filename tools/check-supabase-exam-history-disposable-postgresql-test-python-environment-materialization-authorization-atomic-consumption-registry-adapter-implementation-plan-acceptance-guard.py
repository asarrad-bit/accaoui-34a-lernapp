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
    "adapter-implementation-plan-acceptance-guard-contract.json"
)
PLAN_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-plan-contract.json"
)
IMPLEMENTATION_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-contract.json"
)

DESCRIPTOR = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor.py"
)
DESCRIPTOR_ACCEPTANCE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_acceptance_guard.py"
)
READINESS = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness.py"
)
READINESS_ACCEPTANCE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness_acceptance_guard.py"
)
PLAN = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_plan.py"
)
GUARD = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_plan_acceptance_guard.py"
)
FUTURE_ADAPTER = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
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


def fail(message):
    print(f"FEHLER: {message}")
    raise SystemExit(1)


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


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
    else:
        current[key] = str(old) + "_tampered"


def assert_blocked(result, label):
    if result.get("accepted") is not False:
        fail(f"Manipulation nicht blockiert: {label}")
    if result.get("acceptedPlan") is not None:
        fail(f"Blockiertes Ergebnis enthält Plan: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockierte Grenze offen: {key} / {label}")


contract = load_json(CONTRACT)
plan_contract = load_json(PLAN_CONTRACT)
implementation_contract = load_json(IMPLEMENTATION_CONTRACT)

if contract.get("version") != "v27.33m":
    fail("Plan-Annahmevertrag besitzt nicht v27.33m.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_plan_acceptance_execution_locked"
):
    fail("Plan-Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")
if plan_contract.get("version") != "v27.33l":
    fail("Quellvertrag besitzt nicht v27.33l.")

for block in ("securityBoundary", "futureBoundary"):
    for key, value in contract.get(block, {}).items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

descriptor_module = load_module(DESCRIPTOR, "v2733m_descriptor")
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE, "v2733m_descriptor_acceptance"
)
readiness_module = load_module(READINESS, "v2733m_readiness")
readiness_acceptance_module = load_module(
    READINESS_ACCEPTANCE, "v2733m_readiness_acceptance"
)
plan_module = load_module(PLAN, "v2733m_plan")
guard_module = load_module(GUARD, "v2733m_guard")

descriptor_result = (
    descriptor_module
    .resolve_atomic_consumption_registry_adapter_implementation_descriptor({
        "contractFacts": clone(implementation_contract),
    })
)
accepted_descriptor = (
    descriptor_acceptance_module
    .accept_atomic_consumption_registry_adapter_implementation_descriptor(
        descriptor_result
    )
)
readiness_result = (
    readiness_module
    .resolve_atomic_consumption_registry_adapter_implementation_readiness({
        "acceptedImplementationDescriptorResult": accepted_descriptor,
        "implementationFacts": clone(
            readiness_module._EXPECTED_IMPLEMENTATION_FACTS
        ),
    })
)
accepted_readiness = (
    readiness_acceptance_module
    .accept_atomic_consumption_registry_adapter_implementation_readiness(
        readiness_result
    )
)
plan_result = (
    plan_module
    .resolve_atomic_consumption_registry_adapter_implementation_plan({
        "acceptedImplementationReadinessResult": accepted_readiness,
        "implementationPlanFacts": clone(
            plan_module.EXPECTED_PLAN_FACTS
        ),
    })
)

original = clone(plan_result)
original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError("Plan-Annahme darf keine Datei öffnen.")

builtins.open = forbidden_open
try:
    first = (
        guard_module
        .accept_atomic_consumption_registry_adapter_implementation_plan(
            plan_result
        )
    )
    second = (
        guard_module
        .accept_atomic_consumption_registry_adapter_implementation_plan(
            plan_result
        )
    )
finally:
    builtins.open = original_open

if plan_result != original:
    fail("Plan-Annahme hat die Eingabe verändert.")
if first != second:
    fail("Plan-Annahme ist nicht deterministisch.")
if first.get("status") != guard_module.ACCEPTED_STATUS:
    fail("Erfolgsstatus ist ungültig.")
if first.get("reason") != guard_module.ACCEPTED_REASON:
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

assert_blocked(
    guard_module
    .accept_atomic_consumption_registry_adapter_implementation_plan(None),
    "Nicht-Mapping",
)

wrong = clone(plan_result)
wrong["status"] = "wrong"
assert_blocked(
    guard_module
    .accept_atomic_consumption_registry_adapter_implementation_plan(wrong),
    "falscher Status",
)

opened = clone(plan_result)
opened["adapterImported"] = True
assert_blocked(
    guard_module
    .accept_atomic_consumption_registry_adapter_implementation_plan(opened),
    "offene Quellgrenze",
)

leaf_count = 0
for path in iter_scalar_paths(plan_result["plan"]):
    manipulated = clone(plan_result)
    set_path(manipulated["plan"], path)
    assert_blocked(
        guard_module
        .accept_atomic_consumption_registry_adapter_implementation_plan(
            manipulated
        ),
        ".".join(map(str, path)),
    )
    leaf_count += 1

source_text = GUARD.read_text(encoding="utf-8").lower()
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
):
    if forbidden in source_text:
        fail(f"Plan-Annahme enthält verbotenen Zugriff: {forbidden}")

if FUTURE_ADAPTER.exists():
    fail("v27.33m darf noch keinen Registry-Adapter implementieren.")
if list(MIGRATIONS.glob("*v2733m*.sql")):
    fail("v27.33m darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungsplan-Annahme-Guard: OK")
print(f"Manipulierte Planblätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Datenbankverbindung: keine")
print("Produktive Freigabe: nein")
