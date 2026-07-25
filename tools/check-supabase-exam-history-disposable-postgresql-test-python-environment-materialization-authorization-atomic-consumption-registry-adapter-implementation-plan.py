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
FUTURE_GUARD = ROOT / "tools" / (
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
    if result.get("ready") is not False:
        fail(f"Manipulation nicht blockiert: {label}")
    if result.get("plan") is not None:
        fail(f"Blockiertes Ergebnis enthält Plan: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockierte Grenze offen: {key} / {label}")


contract = load_json(CONTRACT)
implementation_contract = load_json(IMPLEMENTATION_CONTRACT)

if contract.get("version") != "v27.33l":
    fail("Implementierungsplanvertrag besitzt nicht v27.33l.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_plan_execution_locked"
):
    fail("Implementierungsplanvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

for block in ("securityBoundary", "futureBoundary"):
    for key, value in contract.get(block, {}).items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

descriptor_module = load_module(DESCRIPTOR, "v2733l_descriptor")
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE, "v2733l_descriptor_acceptance"
)
readiness_module = load_module(READINESS, "v2733l_readiness")
readiness_acceptance_module = load_module(
    READINESS_ACCEPTANCE, "v2733l_readiness_acceptance"
)
plan_module = load_module(PLAN, "v2733l_plan")

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
readiness_facts = clone(
    readiness_module._EXPECTED_IMPLEMENTATION_FACTS
)
readiness_result = (
    readiness_module
    .resolve_atomic_consumption_registry_adapter_implementation_readiness({
        "acceptedImplementationDescriptorResult": accepted_descriptor,
        "implementationFacts": readiness_facts,
    })
)
accepted_readiness = (
    readiness_acceptance_module
    .accept_atomic_consumption_registry_adapter_implementation_readiness(
        readiness_result
    )
)

plan_facts = clone(plan_module.EXPECTED_PLAN_FACTS)
input_value = {
    "acceptedImplementationReadinessResult": accepted_readiness,
    "implementationPlanFacts": plan_facts,
}
before = clone(input_value)

original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError("Plan darf keine Datei öffnen.")

builtins.open = forbidden_open
try:
    first = (
        plan_module
        .resolve_atomic_consumption_registry_adapter_implementation_plan(
            input_value
        )
    )
    second = (
        plan_module
        .resolve_atomic_consumption_registry_adapter_implementation_plan(
            input_value
        )
    )
finally:
    builtins.open = original_open

if input_value != before:
    fail("Implementierungsplan hat die Eingabe verändert.")
if first != second:
    fail("Implementierungsplan ist nicht deterministisch.")
if first.get("status") != plan_module.SUCCESS_STATUS:
    fail("Erfolgsstatus ist ungültig.")
if first.get("reason") != plan_module.SUCCESS_REASON:
    fail("Erfolgsgrund ist ungültig.")
if first.get("ready") is not True:
    fail("Gültiger Plan ist nicht bereit.")

plan = first.get("plan")
if not isinstance(plan, dict):
    fail("Kanonischer Plan fehlt.")
if plan.get("planVersion") != 1:
    fail("Planversion ist ungültig.")
if plan.get("implementationSequence") != (
    plan_module.IMPLEMENTATION_SEQUENCE
):
    fail("Implementierungsreihenfolge ist ungültig.")
if len(plan["implementationSequence"]) != 10:
    fail("Implementierungsreihenfolge besitzt nicht zehn Schritte.")
if plan.get("acceptedReadiness") is (
    accepted_readiness["acceptedReadiness"]
):
    fail("Readiness wurde nicht tief kopiert.")
if plan.get("implementationPlanFacts") is plan_facts:
    fail("Planfakten wurden nicht tief kopiert.")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Ergebnisgrenze ist offen: {key}")

assert_blocked(
    plan_module
    .resolve_atomic_consumption_registry_adapter_implementation_plan(None),
    "Nicht-Mapping",
)

wrong = clone(input_value)
wrong["implementationPlanFacts"]["maximumParallelWinners"] = 2
assert_blocked(
    plan_module
    .resolve_atomic_consumption_registry_adapter_implementation_plan(wrong),
    "falsche Planfakten",
)

leaf_count = 0
for path in iter_scalar_paths(input_value["implementationPlanFacts"]):
    manipulated = clone(input_value)
    set_path(manipulated["implementationPlanFacts"], path)
    assert_blocked(
        plan_module
        .resolve_atomic_consumption_registry_adapter_implementation_plan(
            manipulated
        ),
        ".".join(map(str, path)),
    )
    leaf_count += 1

source_text = PLAN.read_text(encoding="utf-8").lower()
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
        fail(f"Plan enthält verbotenen Zugriff: {forbidden}")

if FUTURE_GUARD.exists():
    fail("v27.33l darf noch keinen Plan-Annahme-Guard umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.33l darf noch keinen Registry-Adapter implementieren.")
if list(MIGRATIONS.glob("*v2733l*.sql")):
    fail("v27.33l darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungsplan: OK")
print(f"Manipulierte Planfaktenblätter blockiert: {leaf_count}")
print("Deterministische Reihenfolge: zehn Schritte")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Datenbankverbindung: keine")
print("Produktive Freigabe: nein")
