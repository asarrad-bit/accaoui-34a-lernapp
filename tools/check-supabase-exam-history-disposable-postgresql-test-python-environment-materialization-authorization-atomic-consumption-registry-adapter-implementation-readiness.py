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
    "adapter-implementation-readiness-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-descriptor-acceptance-guard-contract.json"
)
IMPLEMENTATION_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-contract.json"
)
DESCRIPTOR_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor.py"
)
ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_acceptance_guard.py"
)
READINESS_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness.py"
)
FUTURE_GUARD = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness_acceptance_guard.py"
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
    "atomic_consumption_registry_adapter_implementation_readiness_"
    "ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_readiness_"
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
    if result.get("ready") is not False:
        fail(f"Manipulation meldet Readiness: {label}")
    if result.get("readiness") is not None:
        fail(f"Blockiertes Ergebnis enthält Readiness: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockiertes Ergebnis öffnet Grenze {key}: {label}")


contract = load_json(CONTRACT, "v27.33j-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.33i-Quellvertrag")
implementation_contract = load_json(
    IMPLEMENTATION_CONTRACT,
    "v27.33g-Implementierungsvertrag",
)

if contract.get("version") != "v27.33j":
    fail("Readiness-Vertrag besitzt nicht v27.33j.")
if contract.get("contractVersion") != 1:
    fail("Readiness-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_readiness_execution_locked"
):
    fail("Readiness-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33i":
    fail("Quellvertrag besitzt nicht v27.33i.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_descriptor_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if implementation_contract.get("version") != "v27.33g":
    fail("Implementierungsvertrag besitzt nicht v27.33g.")

implementation = contract.get("implementation", {})
if implementation.get("implementationReadinessImplemented") is not True:
    fail("Implementierungs-Readiness fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == "implementationReadinessImplemented":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

for key, value in contract.get("securityBoundary", {}).items():
    if value is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")
for key, value in contract.get("futureBoundary", {}).items():
    if value is not False:
        fail(f"Zukunftsgrenze ist offen: {key}")

descriptor_module = load_module(
    DESCRIPTOR_MODULE,
    "implementation_descriptor_v2733j",
)
acceptance_module = load_module(
    ACCEPTANCE_MODULE,
    "implementation_descriptor_acceptance_v2733j",
)
readiness_module = load_module(
    READINESS_MODULE,
    "implementation_readiness_v2733j",
)

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_implementation_descriptor",
    None,
)
accept_descriptor = getattr(
    acceptance_module,
    "accept_atomic_consumption_registry_adapter_implementation_descriptor",
    None,
)
resolve_readiness = getattr(
    readiness_module,
    "resolve_atomic_consumption_registry_adapter_implementation_readiness",
    None,
)
if not callable(resolve_descriptor):
    fail("Implementierungsdescriptor-Resolver fehlt.")
if not callable(accept_descriptor):
    fail("Implementierungsdescriptor-Annahme fehlt.")
if not callable(resolve_readiness):
    fail("Implementierungs-Readiness-Resolver fehlt.")

descriptor_result = resolve_descriptor({
    "contractFacts": clone(implementation_contract),
})
accepted_result = accept_descriptor(descriptor_result)
if accepted_result.get("status") != (
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "descriptor_execution_locked"
):
    fail("Quell-Annahme liefert keinen Erfolgsstatus.")

facts = clone(
    getattr(readiness_module, "_EXPECTED_IMPLEMENTATION_FACTS", None)
)
if not isinstance(facts, dict):
    fail("Kanonische Implementierungsfähigkeitsfakten fehlen.")

input_value = {
    "acceptedImplementationDescriptorResult": accepted_result,
    "implementationFacts": facts,
}
before = clone(input_value)
original_open = builtins.open


def forbidden_open(*args, **kwargs):
    raise AssertionError("Readiness darf keine Datei öffnen.")


builtins.open = forbidden_open
try:
    first = resolve_readiness(input_value)
    second = resolve_readiness(input_value)
finally:
    builtins.open = original_open

if input_value != before:
    fail("Readiness hat die Eingabe verändert.")
if first != second:
    fail("Readiness ist nicht deterministisch.")
if first.get("status") != SUCCESS_STATUS:
    fail("Gültige Fakten liefern keinen Erfolgsstatus.")
if first.get("reason") != SUCCESS_REASON:
    fail("Readiness-Grund ist ungültig.")
if first.get("ready") is not True:
    fail("Gültige Implementierungs-Readiness ist nicht bereit.")

readiness = first.get("readiness")
if not isinstance(readiness, dict):
    fail("Kanonische Readiness fehlt.")
if readiness.get("readinessVersion") != 1:
    fail("Readiness-Version ist ungültig.")
if readiness.get("acceptedDescriptor") != (
    accepted_result["acceptedDescriptor"]
):
    fail("Descriptor wurde nicht kanonisch gebunden.")
if readiness.get("acceptedDescriptor") is (
    accepted_result["acceptedDescriptor"]
):
    fail("Descriptor wurde nicht tief kopiert.")
if readiness.get("implementationFacts") != facts:
    fail("Implementierungsfakten wurden nicht kanonisch gebunden.")
if readiness.get("implementationFacts") is facts:
    fail("Implementierungsfakten wurden nicht tief kopiert.")
for key in (
    "adapterImplementationAllowed",
    "adapterImportAllowed",
    "adapterInstantiationAllowed",
    "adapterInvocationAllowed",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "authorizationConsumptionAllowed",
    "executionGrant",
):
    if readiness.get(key) is not False:
        fail(f"Readiness öffnet Grenze {key}")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Readiness-Ergebnisflag ist offen: {key}")

assert_blocked(resolve_readiness(None), "Nicht-Mapping")
missing = clone(input_value)
missing.pop("implementationFacts")
assert_blocked(resolve_readiness(missing), "fehlendes Feld")
unknown = clone(input_value)
unknown["unknown"] = True
assert_blocked(resolve_readiness(unknown), "unbekanntes Feld")
wrong_source = clone(input_value)
wrong_source["acceptedImplementationDescriptorResult"]["status"] = "wrong"
assert_blocked(resolve_readiness(wrong_source), "falscher Quellstatus")
opened = clone(input_value)
opened["acceptedImplementationDescriptorResult"]["adapterImported"] = True
assert_blocked(resolve_readiness(opened), "offene Quellgrenze")
wrong_descriptor = clone(input_value)
wrong_descriptor["acceptedImplementationDescriptorResult"][
    "acceptedDescriptor"
] = []
assert_blocked(resolve_readiness(wrong_descriptor), "falscher Descriptor")
wrong_facts = clone(input_value)
wrong_facts["implementationFacts"]["interfaceVersion"] = 2
assert_blocked(resolve_readiness(wrong_facts), "falsche Fakten")

leaf_count = 0
for path in iter_scalar_paths(
    input_value["acceptedImplementationDescriptorResult"]
):
    manipulated = clone(input_value)
    set_path(
        manipulated["acceptedImplementationDescriptorResult"],
        path,
    )
    assert_blocked(
        resolve_readiness(manipulated),
        "Quellmanipulation " + ".".join(map(str, path)),
    )
    leaf_count += 1

fact_leaf_count = 0
for path in iter_scalar_paths(input_value["implementationFacts"]):
    manipulated = clone(input_value)
    set_path(manipulated["implementationFacts"], path)
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
    fail("v27.33j darf noch keinen Readiness-Annahme-Guard umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.33j darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33j darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733j*.sql")):
    fail("v27.33j darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungs-Readiness: OK")
print("Quell-Annahme-Guard: v27.33i")
print(f"Manipulierte Quellblätter blockiert: {leaf_count}")
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
print("SQL-Migration v27.33j: keine")
print("Produktive Freigabe: nein")
