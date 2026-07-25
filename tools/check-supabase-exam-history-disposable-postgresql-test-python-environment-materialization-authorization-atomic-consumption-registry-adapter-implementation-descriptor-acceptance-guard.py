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
    "adapter-implementation-descriptor-acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-descriptor-contract.json"
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
GUARD_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_acceptance_guard.py"
)
FUTURE_READINESS = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness.py"
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
    "accepted_atomic_consumption_registry_adapter_implementation_"
    "descriptor_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_descriptor_"
    "acceptance_blocked_execution_locked"
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
    if result.get("acceptedDescriptor") is not None:
        fail(f"Blockiertes Ergebnis enthält Descriptor: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockiertes Ergebnis öffnet Grenze {key}: {label}")


contract = load_json(CONTRACT, "v27.33i-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.33h-Quellvertrag")
implementation_contract = load_json(
    IMPLEMENTATION_CONTRACT,
    "v27.33g-Implementierungsvertrag",
)

if contract.get("version") != "v27.33i":
    fail("Annahmevertrag besitzt nicht v27.33i.")
if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_descriptor_acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33h":
    fail("Quellvertrag besitzt nicht v27.33h.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_descriptor_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if implementation_contract.get("version") != "v27.33g":
    fail("Implementierungsvertrag besitzt nicht v27.33g.")

implementation = contract.get("implementation", {})
if implementation.get(
    "implementationDescriptorAcceptanceGuardImplemented"
) is not True:
    fail("Implementierungsdescriptor-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == (
        "implementationDescriptorAcceptanceGuardImplemented"
    ):
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
    "implementation_descriptor_v2733i",
)
guard_module = load_module(
    GUARD_MODULE,
    "implementation_descriptor_acceptance_v2733i",
)

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_implementation_descriptor",
    None,
)
accept_descriptor = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_implementation_descriptor",
    None,
)
if not callable(resolve_descriptor):
    fail("Implementierungsdescriptor-Resolver fehlt.")
if not callable(accept_descriptor):
    fail("Implementierungsdescriptor-Annahme fehlt.")

descriptor_result = resolve_descriptor({
    "contractFacts": clone(implementation_contract),
})
if descriptor_result.get("status") != (
    "atomic_consumption_registry_adapter_implementation_descriptor_"
    "ready_execution_locked"
):
    fail("Quell-Descriptor liefert keinen Erfolgsstatus.")

before = clone(descriptor_result)
original_open = builtins.open


def forbidden_open(*args, **kwargs):
    raise AssertionError("Descriptor-Annahme darf keine Datei öffnen.")


builtins.open = forbidden_open
try:
    accepted = accept_descriptor(descriptor_result)
    again = accept_descriptor(descriptor_result)
finally:
    builtins.open = original_open

if descriptor_result != before:
    fail("Descriptor-Annahme hat die Eingabe verändert.")
if accepted != again:
    fail("Descriptor-Annahme ist nicht deterministisch.")
if accepted.get("status") != SUCCESS_STATUS:
    fail("Gültiger Descriptor wurde nicht angenommen.")
if accepted.get("reason") != SUCCESS_REASON:
    fail("Annahmegrund ist ungültig.")
if accepted.get("accepted") is not True:
    fail("Annahmeflag fehlt.")
if accepted.get("acceptedDescriptor") != descriptor_result.get("descriptor"):
    fail("Angenommener Descriptor ist nicht kanonisch.")
if accepted.get("acceptedDescriptor") is descriptor_result.get("descriptor"):
    fail("Angenommener Descriptor ist keine Tiefenkopie.")
for key in LOCKED_FLAGS:
    if accepted.get(key) is not False:
        fail(f"Annahme-Ergebnisflag ist offen: {key}")

assert_blocked(accept_descriptor(None), "Nicht-Mapping")
missing = clone(descriptor_result)
missing.pop("descriptor")
assert_blocked(accept_descriptor(missing), "fehlendes Feld")
unknown = clone(descriptor_result)
unknown["unknown"] = True
assert_blocked(accept_descriptor(unknown), "unbekanntes Feld")
wrong_status = clone(descriptor_result)
wrong_status["status"] = "wrong"
assert_blocked(accept_descriptor(wrong_status), "falscher Status")
wrong_reason = clone(descriptor_result)
wrong_reason["reason"] = "wrong"
assert_blocked(accept_descriptor(wrong_reason), "falscher Grund")
not_ready = clone(descriptor_result)
not_ready["ready"] = False
assert_blocked(accept_descriptor(not_ready), "ready false")
opened = clone(descriptor_result)
opened["adapterImported"] = True
assert_blocked(accept_descriptor(opened), "offene Quellgrenze")
wrong_descriptor = clone(descriptor_result)
wrong_descriptor["descriptor"] = []
assert_blocked(accept_descriptor(wrong_descriptor), "falscher Descriptor")

leaf_count = 0
for path in iter_scalar_paths(descriptor_result["descriptor"]):
    manipulated = clone(descriptor_result)
    set_path(manipulated["descriptor"], path)
    assert_blocked(
        accept_descriptor(manipulated),
        "Manipulation " + ".".join(map(str, path)),
    )
    leaf_count += 1

accepted_descriptor = accepted["acceptedDescriptor"]
first_path = next(iter(iter_scalar_paths(accepted_descriptor)))
set_path(accepted_descriptor, first_path)
if accepted_descriptor == descriptor_result["descriptor"]:
    fail("Tiefenkopie ist mit Quelle gekoppelt.")

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
        fail(f"Annahme-Guard enthält verbotenen Zugriff: {forbidden}")

if FUTURE_READINESS.exists():
    fail("v27.33i darf noch keine Implementierungs-Readiness umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.33i darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33i darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733i*.sql")):
    fail("v27.33i darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungsdescriptor-Annahme-Guard: OK")
print("Quell-Descriptor: v27.33h")
print(f"Manipulierte Descriptor-Blätter blockiert: {leaf_count}")
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
print("SQL-Migration v27.33i: keine")
print("Produktive Freigabe: nein")
