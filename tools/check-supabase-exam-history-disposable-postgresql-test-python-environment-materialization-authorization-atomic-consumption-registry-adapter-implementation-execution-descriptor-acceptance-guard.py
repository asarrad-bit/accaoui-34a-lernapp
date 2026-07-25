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
    "adapter-implementation-execution-descriptor-acceptance-guard-"
    "contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-descriptor-contract.json"
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
GUARD_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_acceptance_guard.py"
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
    "execution_descriptor_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "descriptor_acceptance_blocked_execution_locked"
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
    if result.get("acceptedDescriptor") is not None:
        fail(f"Blockiertes Ergebnis enthält Descriptor: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockierte Grenze offen: {key} / {label}")


contract = load_json(CONTRACT, "v27.33p-Vertrag")
source_contract = load_json(
    SOURCE_CONTRACT,
    "v27.33o-Descriptorvertrag",
)
execution_contract = load_json(
    EXECUTION_CONTRACT,
    "v27.33n-Ausführungsvertrag",
)

if contract.get("version") != "v27.33p":
    fail("Descriptor-Annahmevertrag besitzt nicht v27.33p.")
if contract.get("contractVersion") != 1:
    fail("Descriptor-Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_acceptance_execution_locked"
):
    fail("Descriptor-Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33o":
    fail("Quellvertrag besitzt nicht v27.33o.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if execution_contract.get("version") != "v27.33n":
    fail("Ausführungsvertrag besitzt nicht v27.33n.")

implementation = contract.get("implementation", {})
if implementation.get(
    "executionDescriptorAcceptanceGuardImplemented"
) is not True:
    fail("Implementierungsausführungsdescriptor-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == (
        "executionDescriptorAcceptanceGuardImplemented"
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
    "v2733p_execution_descriptor",
)
guard_module = load_module(
    GUARD_MODULE,
    "v2733p_execution_descriptor_acceptance",
)

resolver = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor",
    None,
)
accept = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_"
    "implementation_execution_descriptor",
    None,
)
if not callable(resolver):
    fail("Implementierungsausführungsdescriptor-Resolver fehlt.")
if not callable(accept):
    fail("Implementierungsausführungsdescriptor-Annahme fehlt.")

descriptor_result = resolver({
    "contractFacts": clone(execution_contract),
})
if descriptor_result.get("ready") is not True:
    fail("Quell-Descriptor liefert keinen Erfolgsstatus.")

before = clone(descriptor_result)
original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError(
        "Descriptor-Annahme darf keine Datei öffnen."
    )

builtins.open = forbidden_open
try:
    first = accept(descriptor_result)
    second = accept(descriptor_result)
finally:
    builtins.open = original_open

if descriptor_result != before:
    fail("Descriptor-Annahme hat die Eingabe verändert.")
if first != second:
    fail("Descriptor-Annahme ist nicht deterministisch.")
if first.get("status") != ACCEPTED_STATUS:
    fail("Erfolgsstatus ist ungültig.")
if first.get("reason") != ACCEPTED_REASON:
    fail("Erfolgsgrund ist ungültig.")
if first.get("accepted") is not True:
    fail("Annahmeflag fehlt.")
if first.get("acceptedDescriptor") != descriptor_result["descriptor"]:
    fail("Angenommener Descriptor ist nicht kanonisch.")
if first.get("acceptedDescriptor") is descriptor_result["descriptor"]:
    fail("Angenommener Descriptor ist keine Tiefenkopie.")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Ergebnisgrenze ist offen: {key}")

assert_blocked(accept(None), "Nicht-Mapping")

missing = clone(descriptor_result)
missing.pop("descriptor")
assert_blocked(accept(missing), "fehlendes Feld")

unknown = clone(descriptor_result)
unknown["unknown"] = True
assert_blocked(accept(unknown), "unbekanntes Feld")

opened = clone(descriptor_result)
opened["adapterImported"] = True
assert_blocked(accept(opened), "offene Quellgrenze")

leaf_count = 0
for path in iter_scalar_paths(descriptor_result):
    manipulated = clone(descriptor_result)
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
        fail(f"Descriptor-Annahme enthält verbotenen Zugriff: {forbidden}")

if FUTURE_ADAPTER.exists():
    fail("v27.33p darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33p darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733p*.sql")):
    fail("v27.33p darf keine SQL-Migration erzeugen.")

print(
    "Registry-Adapter-Implementierungsausführungsdescriptor-"
    "Annahme-Guard: OK"
)
print("Quell-Descriptor: v27.33o")
print(f"Manipulierte Descriptorblätter blockiert: {leaf_count}")
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
print("SQL-Migration v27.33p: keine")
print("Produktive Freigabe: nein")
