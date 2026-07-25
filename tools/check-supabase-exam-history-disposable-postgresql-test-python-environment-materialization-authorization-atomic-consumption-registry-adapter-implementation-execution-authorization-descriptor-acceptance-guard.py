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
    "adapter-implementation-execution-authorization-descriptor-"
    "acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-authorization-descriptor-"
    "contract.json"
)
AUTHORIZATION_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-authorization-contract.json"
)
DESCRIPTOR_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor.py"
)
GUARD_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor_"
    "acceptance_guard.py"
)

FUTURE_READINESS = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness.py"
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
    "execution_authorization_descriptor_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor_"
    "accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "authorization_descriptor_acceptance_blocked_execution_locked"
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


contract = load_json(CONTRACT, "v27.33w-Vertrag")
source_contract = load_json(
    SOURCE_CONTRACT,
    "v27.33v-Descriptorvertrag",
)
authorization_contract = load_json(
    AUTHORIZATION_CONTRACT,
    "v27.33u-Autorisierungsvertrag",
)

if contract.get("version") != "v27.33w":
    fail("Descriptor-Annahmevertrag besitzt nicht v27.33w.")
if contract.get("contractVersion") != 1:
    fail("Descriptor-Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor_"
    "acceptance_execution_locked"
):
    fail("Descriptor-Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33v":
    fail("Quellvertrag besitzt nicht v27.33v.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor_"
    "execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if authorization_contract.get("version") != "v27.33u":
    fail("Autorisierungsvertrag besitzt nicht v27.33u.")

implementation = contract.get("implementation", {})
if implementation.get(
    "authorizationDescriptorAcceptanceGuardImplemented"
) is not True:
    fail("Autorisierungsdescriptor-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == (
        "authorizationDescriptorAcceptanceGuardImplemented"
    ):
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

input_boundary = contract.get("inputBoundary", {})
expected_input = {
    "mappingOnly": True,
    "exactSourceFieldsRequired": True,
    "requiredSourceStatus": (
        "atomic_consumption_registry_adapter_implementation_execution_"
        "authorization_descriptor_ready_execution_locked"
    ),
    "requiredSourceReason": (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_execution_authorization_descriptor_"
        "ready_execution_locked"
    ),
    "requiredReady": True,
    "allSourceExecutionFlagsMustBeFalse": True,
    "exactCanonicalDescriptorRequired": True,
    "unknownFieldsAllowed": False,
    "missingFieldsAllowed": False,
    "inputMutationAllowed": False,
}
for key, expected in expected_input.items():
    if input_boundary.get(key) != expected:
        fail(f"Eingabegrenze ist ungültig: {key}")

acceptance = contract.get("acceptanceBoundary", {})
if acceptance.get("requiredDescriptorVersion") != 1:
    fail("Descriptorversion ist nicht gebunden.")
if acceptance.get("requiredSourceContractVersion") != "v27.33u":
    fail("Descriptor-Quellversion ist nicht gebunden.")
if acceptance.get("requiredSourceContractStatus") != (
    "planned_atomic_consumption_registry_adapter_implementation_"
    "execution_authorization_fully_locked_not_implemented"
):
    fail("Descriptor-Quellstatus ist nicht gebunden.")
for key in (
    "requiredExactContractFacts",
    "canonicalCopyRequired",
    "accepted",
):
    if acceptance.get(key) is not True:
        fail(f"Annahmegrenze fehlt: {key}")
for key in (
    "requiredAuthorizationGrantCreated",
    "requiredAuthorizationTokenGenerated",
    "requiredAuthorizationMayBeConsumed",
    "executionGrant",
):
    if acceptance.get(key) is not False:
        fail(f"Annahmegrenze ist offen: {key}")
if acceptance.get("successStatus") != ACCEPTED_STATUS:
    fail("Annahmestatus ist ungültig.")
if acceptance.get("successReason") != ACCEPTED_REASON:
    fail("Annahmegrund ist ungültig.")
if acceptance.get("blockedStatus") != BLOCKED_STATUS:
    fail("Blockstatus ist ungültig.")

for block in ("securityBoundary", "futureBoundary"):
    values = contract.get(block, {})
    if not isinstance(values, dict) or not values:
        fail(f"{block} fehlt.")
    for key, value in values.items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

descriptor_module = load_module(
    DESCRIPTOR_MODULE,
    "v2733w_authorization_descriptor",
)
guard_module = load_module(
    GUARD_MODULE,
    "v2733w_authorization_descriptor_acceptance",
)

resolver = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor",
    None,
)
accept = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor",
    None,
)
if not callable(resolver):
    fail("Autorisierungsdescriptor-Resolver fehlt.")
if not callable(accept):
    fail("Autorisierungsdescriptor-Annahme fehlt.")

descriptor_result = resolver({
    "contractFacts": clone(authorization_contract),
})
if descriptor_result.get("ready") is not True:
    fail("Quell-Descriptor liefert keinen Erfolgsstatus.")

before = clone(descriptor_result)
original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError(
        "Autorisierungsdescriptor-Annahme darf keine Datei öffnen."
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

for key in (
    "authorizationGrantCreated",
    "authorizationTokenGenerated",
    "authorizationMayBeConsumed",
    "executionGrant",
):
    if first["acceptedDescriptor"].get(key) is not False:
        fail(f"Angenommener Descriptor öffnet Grenze: {key}")

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
opened["authorizationGranted"] = True
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

if FUTURE_READINESS.exists():
    fail("v27.33w darf noch keine Autorisierungs-Readiness umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.33w darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33w darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733w*.sql")):
    fail("v27.33w darf keine SQL-Migration erzeugen.")

print(
    "Registry-Adapter-Implementierungsausführungs-"
    "Autorisierungsdescriptor-Annahme-Guard: OK"
)
print("Quell-Autorisierungsdescriptor: v27.33v")
print(f"Manipulierte Descriptorblätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff des Guards: keiner")
print("Autorisierungsgrant erstellt: nein")
print("Autorisierungstoken erzeugt: nein")
print("Autorisierung verbrauchbar: nein")
print("Adaptermodul erstellt: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33w: keine")
print("Produktive Freigabe: nein")
