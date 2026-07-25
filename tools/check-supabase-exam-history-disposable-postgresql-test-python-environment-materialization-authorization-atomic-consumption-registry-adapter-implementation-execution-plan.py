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
    "adapter-implementation-execution-plan-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-readiness-acceptance-guard-"
    "contract.json"
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
FUTURE_GUARD = ROOT / "tools" / (
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

SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "plan_ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "plan_blocked_execution_locked"
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
    if result.get("ready") is not False:
        fail(f"Manipulation meldet Readiness: {label}")
    if result.get("plan") is not None:
        fail(f"Blockiertes Ergebnis enthält Plan: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockierte Grenze offen: {key} / {label}")


contract = load_json(CONTRACT, "v27.33s-Vertrag")
source_contract = load_json(
    SOURCE_CONTRACT,
    "v27.33r-Quellvertrag",
)
execution_contract = load_json(
    EXECUTION_CONTRACT,
    "v27.33n-Ausführungsvertrag",
)

if contract.get("version") != "v27.33s":
    fail("Ausführungsplan-Vertrag besitzt nicht v27.33s.")
if contract.get("contractVersion") != 1:
    fail("Ausführungsplan-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_plan_execution_locked"
):
    fail("Ausführungsplan-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33r":
    fail("Quellvertrag besitzt nicht v27.33r.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")

implementation = contract.get("implementation", {})
if implementation.get(
    "implementationExecutionPlanImplemented"
) is not True:
    fail("Implementierungsausführungsplan fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == (
        "implementationExecutionPlanImplemented"
    ):
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

boundary = contract.get("planBoundary", {})
if boundary.get("requiredStepCount") != 12:
    fail("Ausführungsplan besitzt nicht zwölf Schritte.")
if boundary.get("implementationSequence") != [
    "validate_accepted_readiness_boundary",
    "validate_dependency_injection_boundary",
    "prepare_protocol_and_result_types",
    "prepare_factory_without_default_credentials",
    "prepare_single_transaction_boundary",
    "prepare_atomic_compare_and_set_with_consumption_record",
    "prepare_exact_result_mapping",
    "prepare_timeout_configuration",
    "prepare_commit_ambiguity_terminal_handling",
    "prepare_operation_id_reconciliation",
    "prepare_pure_adapter_unit_fixtures",
    "keep_adapter_unimplemented_uninstantiated_and_uninvoked",
]:
    fail("Ausführungsreihenfolge ist ungültig.")

for block in ("securityBoundary", "futureBoundary"):
    values = contract.get(block, {})
    if not isinstance(values, dict) or not values:
        fail(f"{block} fehlt.")
    for key, value in values.items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

descriptor_module = load_module(
    DESCRIPTOR_MODULE,
    "v2733s_descriptor",
)
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE_MODULE,
    "v2733s_descriptor_acceptance",
)
readiness_module = load_module(
    READINESS_MODULE,
    "v2733s_readiness",
)
readiness_acceptance_module = load_module(
    READINESS_ACCEPTANCE_MODULE,
    "v2733s_readiness_acceptance",
)
plan_module = load_module(
    PLAN_MODULE,
    "v2733s_execution_plan",
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

plan_facts = clone(
    plan_module.EXPECTED_EXECUTION_PLAN_FACTS
)
input_value = {
    "acceptedExecutionReadinessResult": accepted_readiness,
    "executionPlanFacts": plan_facts,
}
before = clone(input_value)
resolver = (
    plan_module
    .resolve_atomic_consumption_registry_adapter_implementation_execution_plan
)

original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError(
        "Ausführungsplan darf keine Datei öffnen."
    )

builtins.open = forbidden_open
try:
    first = resolver(input_value)
    second = resolver(input_value)
finally:
    builtins.open = original_open

if input_value != before:
    fail("Ausführungsplan hat die Eingabe verändert.")
if first != second:
    fail("Ausführungsplan ist nicht deterministisch.")
if first.get("status") != SUCCESS_STATUS:
    fail("Gültige Eingaben liefern keinen Erfolgsstatus.")
if first.get("reason") != SUCCESS_REASON:
    fail("Ausführungsplan-Grund ist ungültig.")
if first.get("ready") is not True:
    fail("Gültiger Ausführungsplan ist nicht bereit.")

plan = first.get("plan")
if not isinstance(plan, dict):
    fail("Kanonischer Ausführungsplan fehlt.")
if plan.get("planVersion") != 1:
    fail("Planversion ist ungültig.")
if plan.get("implementationSequence") != (
    plan_module.IMPLEMENTATION_SEQUENCE
):
    fail("Planreihenfolge ist nicht kanonisch.")
if plan.get("acceptedReadiness") != (
    accepted_readiness["acceptedReadiness"]
):
    fail("Angenommene Readiness wurde nicht gebunden.")
if plan.get("acceptedReadiness") is (
    accepted_readiness["acceptedReadiness"]
):
    fail("Angenommene Readiness wurde nicht tief kopiert.")
if plan.get("executionPlanFacts") != plan_facts:
    fail("Ausführungsplanfakten wurden nicht gebunden.")
if plan.get("executionPlanFacts") is plan_facts:
    fail("Ausführungsplanfakten wurden nicht tief kopiert.")

for key in (
    "adapterImplementationAllowed",
    "adapterImportAllowed",
    "adapterInstantiationAllowed",
    "adapterInvocationAllowed",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "authorizationConsumptionAllowed",
    "reconciliationReadAllowed",
    "executionGrant",
):
    if plan.get(key) is not False:
        fail(f"Plan öffnet Grenze {key}")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Plan-Ergebnisflag ist offen: {key}")

assert_blocked(resolver(None), "Nicht-Mapping")

missing = clone(input_value)
missing.pop("executionPlanFacts")
assert_blocked(resolver(missing), "fehlendes Feld")

unknown = clone(input_value)
unknown["unknown"] = True
assert_blocked(resolver(unknown), "unbekanntes Feld")

opened = clone(input_value)
opened["acceptedExecutionReadinessResult"]["adapterImported"] = True
assert_blocked(resolver(opened), "offene Quellgrenze")

source_leaf_count = 0
for path in iter_scalar_paths(
    input_value["acceptedExecutionReadinessResult"]
):
    manipulated = clone(input_value)
    set_path(
        manipulated["acceptedExecutionReadinessResult"],
        path,
    )
    assert_blocked(
        resolver(manipulated),
        "Quellmanipulation " + ".".join(map(str, path)),
    )
    source_leaf_count += 1

fact_leaf_count = 0
for path in iter_scalar_paths(input_value["executionPlanFacts"]):
    manipulated = clone(input_value)
    set_path(manipulated["executionPlanFacts"], path)
    assert_blocked(
        resolver(manipulated),
        "Faktenmanipulation " + ".".join(map(str, path)),
    )
    fact_leaf_count += 1

source_text = PLAN_MODULE.read_text(encoding="utf-8").lower()
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
        fail(f"Ausführungsplan enthält verbotenen Zugriff: {forbidden}")

if FUTURE_GUARD.exists():
    fail("v27.33s darf noch keinen Plan-Annahme-Guard umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.33s darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33s darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733s*.sql")):
    fail("v27.33s darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungsausführungsplan: OK")
print("Quell-Readiness-Annahme: v27.33r")
print(f"Manipulierte Quellblätter blockiert: {source_leaf_count}")
print(f"Manipulierte Faktenblätter blockiert: {fact_leaf_count}")
print("Deterministische Reihenfolge: zwölf Schritte")
print("Kanonische Tiefenkopien: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff des Resolvers: keiner")
print("Adaptermodul erstellt: nein")
print("Adapter importiert: nein")
print("Adapter instanziiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33s: keine")
print("Produktive Freigabe: nein")
