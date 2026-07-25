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
    "adapter-implementation-execution-readiness-contract.json"
)
SOURCE_ACCEPTANCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-descriptor-acceptance-guard-"
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
FUTURE_GUARD = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_acceptance_guard.py"
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
    "readiness_ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "readiness_blocked_execution_locked"
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
    if result.get("readiness") is not None:
        fail(f"Blockiertes Ergebnis enthält Readiness: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockierte Grenze offen: {key} / {label}")


contract = load_json(CONTRACT, "v27.33q-Vertrag")
source_acceptance_contract = load_json(
    SOURCE_ACCEPTANCE_CONTRACT,
    "v27.33p-Quellvertrag",
)
execution_contract = load_json(
    EXECUTION_CONTRACT,
    "v27.33n-Ausführungsvertrag",
)

if contract.get("version") != "v27.33q":
    fail("Ausführungs-Readiness-Vertrag besitzt nicht v27.33q.")
if contract.get("contractVersion") != 1:
    fail("Ausführungs-Readiness-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness_execution_locked"
):
    fail("Ausführungs-Readiness-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_acceptance_contract.get("version") != "v27.33p":
    fail("Quellvertrag besitzt nicht v27.33p.")
if source_acceptance_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if execution_contract.get("version") != "v27.33n":
    fail("Ausführungsvertrag besitzt nicht v27.33n.")

implementation = contract.get("implementation", {})
if implementation.get(
    "implementationExecutionReadinessImplemented"
) is not True:
    fail("Implementierungsausführungs-Readiness fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == (
        "implementationExecutionReadinessImplemented"
    ):
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

for block in ("securityBoundary", "futureBoundary"):
    values = contract.get(block, {})
    if not isinstance(values, dict) or not values:
        fail(f"{block} fehlt.")
    for key, value in values.items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

descriptor_module = load_module(
    DESCRIPTOR_MODULE,
    "v2733q_execution_descriptor",
)
acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE_MODULE,
    "v2733q_execution_descriptor_acceptance",
)
readiness_module = load_module(
    READINESS_MODULE,
    "v2733q_execution_readiness",
)

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor",
    None,
)
accept_descriptor = getattr(
    acceptance_module,
    "accept_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor",
    None,
)
resolve_readiness = getattr(
    readiness_module,
    "resolve_atomic_consumption_registry_adapter_"
    "implementation_execution_readiness",
    None,
)
if not callable(resolve_descriptor):
    fail("Implementierungsausführungsdescriptor-Resolver fehlt.")
if not callable(accept_descriptor):
    fail("Implementierungsausführungsdescriptor-Annahme fehlt.")
if not callable(resolve_readiness):
    fail("Implementierungsausführungs-Readiness-Resolver fehlt.")

descriptor_result = resolve_descriptor({
    "contractFacts": clone(execution_contract),
})
accepted_descriptor = accept_descriptor(descriptor_result)
if accepted_descriptor.get("status") != (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "execution_descriptor_execution_locked"
):
    fail("Quell-Descriptor-Annahme liefert keinen Erfolgsstatus.")

capability_facts = clone(
    getattr(
        readiness_module,
        "EXPECTED_EXECUTION_CAPABILITY_FACTS",
        None,
    )
)
if not isinstance(capability_facts, dict):
    fail("Kanonische Ausführungsfähigkeitsfakten fehlen.")

input_value = {
    "acceptedExecutionDescriptorResult": accepted_descriptor,
    "executionCapabilityFacts": capability_facts,
}
before = clone(input_value)
original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError(
        "Ausführungs-Readiness darf keine Datei öffnen."
    )

builtins.open = forbidden_open
try:
    first = resolve_readiness(input_value)
    second = resolve_readiness(input_value)
finally:
    builtins.open = original_open

if input_value != before:
    fail("Ausführungs-Readiness hat die Eingabe verändert.")
if first != second:
    fail("Ausführungs-Readiness ist nicht deterministisch.")
if first.get("status") != SUCCESS_STATUS:
    fail("Gültige Eingaben liefern keinen Erfolgsstatus.")
if first.get("reason") != SUCCESS_REASON:
    fail("Ausführungs-Readiness-Grund ist ungültig.")
if first.get("ready") is not True:
    fail("Gültige Ausführungs-Readiness ist nicht bereit.")

readiness = first.get("readiness")
if not isinstance(readiness, dict):
    fail("Kanonische Ausführungs-Readiness fehlt.")
if readiness.get("readinessVersion") != 1:
    fail("Readiness-Version ist ungültig.")
if readiness.get("acceptedDescriptor") != (
    accepted_descriptor["acceptedDescriptor"]
):
    fail("Descriptor wurde nicht kanonisch gebunden.")
if readiness.get("acceptedDescriptor") is (
    accepted_descriptor["acceptedDescriptor"]
):
    fail("Descriptor wurde nicht tief kopiert.")
if readiness.get("executionCapabilityFacts") != capability_facts:
    fail("Ausführungsfähigkeitsfakten wurden nicht kanonisch gebunden.")
if readiness.get("executionCapabilityFacts") is capability_facts:
    fail("Ausführungsfähigkeitsfakten wurden nicht tief kopiert.")

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
    if readiness.get(key) is not False:
        fail(f"Readiness öffnet Grenze {key}")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Readiness-Ergebnisflag ist offen: {key}")

assert_blocked(resolve_readiness(None), "Nicht-Mapping")

missing = clone(input_value)
missing.pop("executionCapabilityFacts")
assert_blocked(resolve_readiness(missing), "fehlendes Feld")

unknown = clone(input_value)
unknown["unknown"] = True
assert_blocked(resolve_readiness(unknown), "unbekanntes Feld")

opened = clone(input_value)
opened["acceptedExecutionDescriptorResult"]["adapterImported"] = True
assert_blocked(resolve_readiness(opened), "offene Quellgrenze")

source_leaf_count = 0
for path in iter_scalar_paths(
    input_value["acceptedExecutionDescriptorResult"]
):
    manipulated = clone(input_value)
    set_path(
        manipulated["acceptedExecutionDescriptorResult"],
        path,
    )
    assert_blocked(
        resolve_readiness(manipulated),
        "Quellmanipulation " + ".".join(map(str, path)),
    )
    source_leaf_count += 1

fact_leaf_count = 0
for path in iter_scalar_paths(
    input_value["executionCapabilityFacts"]
):
    manipulated = clone(input_value)
    set_path(manipulated["executionCapabilityFacts"], path)
    assert_blocked(
        resolve_readiness(manipulated),
        "Faktenmanipulation " + ".".join(map(str, path)),
    )
    fact_leaf_count += 1

source_text = READINESS_MODULE.read_text(encoding="utf-8").lower()
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
        fail(f"Readiness enthält verbotenen Zugriff: {forbidden}")

if FUTURE_GUARD.exists():
    fail("v27.33q darf noch keinen Readiness-Annahme-Guard umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.33q darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33q darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733q*.sql")):
    fail("v27.33q darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungsausführungs-Readiness: OK")
print("Quell-Descriptor-Annahme: v27.33p")
print(f"Manipulierte Quellblätter blockiert: {source_leaf_count}")
print(f"Manipulierte Faktenblätter blockiert: {fact_leaf_count}")
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
print("SQL-Migration v27.33q: keine")
print("Produktive Freigabe: nein")
