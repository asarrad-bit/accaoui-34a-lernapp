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
    "adapter-implementation-execution-authorization-readiness-"
    "acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-authorization-readiness-"
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
DESCRIPTOR_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor_"
    "acceptance_guard.py"
)
READINESS_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness.py"
)
GUARD_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness_"
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
    "execution_authorization_readiness_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness_"
    "accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "authorization_readiness_acceptance_blocked_execution_locked"
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
    if result.get("acceptedReadiness") is not None:
        fail(f"Blockiertes Ergebnis enthält Readiness: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockierte Grenze offen: {key} / {label}")


contract = load_json(CONTRACT, "v27.33y-Vertrag")
source_contract = load_json(
    SOURCE_CONTRACT,
    "v27.33x-Quellvertrag",
)
authorization_contract = load_json(
    AUTHORIZATION_CONTRACT,
    "v27.33u-Autorisierungsvertrag",
)

if contract.get("version") != "v27.33y":
    fail("Autorisierungs-Readiness-Annahmevertrag besitzt nicht v27.33y.")
if contract.get("contractVersion") != 1:
    fail("Autorisierungs-Readiness-Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness_acceptance_"
    "execution_locked"
):
    fail("Autorisierungs-Readiness-Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33x":
    fail("Quellvertrag besitzt nicht v27.33x.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if authorization_contract.get("version") != "v27.33u":
    fail("Autorisierungsvertrag besitzt nicht v27.33u.")

implementation = contract.get("implementation", {})
if implementation.get(
    "authorizationReadinessAcceptanceGuardImplemented"
) is not True:
    fail("Autorisierungs-Readiness-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == (
        "authorizationReadinessAcceptanceGuardImplemented"
    ):
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

expected_input_boundary = {
    "mappingOnly": True,
    "exactSourceFieldsRequired": True,
    "requiredSourceStatus": (
        "atomic_consumption_registry_adapter_implementation_execution_"
        "authorization_readiness_ready_execution_locked"
    ),
    "requiredSourceReason": (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_execution_authorization_readiness_"
        "ready_execution_locked"
    ),
    "requiredReady": True,
    "allSourceExecutionFlagsMustBeFalse": True,
    "exactCanonicalReadinessRequired": True,
    "unknownFieldsAllowed": False,
    "missingFieldsAllowed": False,
    "inputMutationAllowed": False,
}
if contract.get("inputBoundary") != expected_input_boundary:
    fail("Eingabegrenze ist nicht exakt gebunden.")

expected_acceptance_boundary = {
    "requiredReadinessVersion": 1,
    "requiredSourceStatus": (
        "accepted_atomic_consumption_registry_adapter_implementation_"
        "execution_authorization_descriptor_execution_locked"
    ),
    "requiredSourceReason": (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_execution_authorization_descriptor_"
        "accepted_execution_locked"
    ),
    "requiredExactAcceptedDescriptor": True,
    "requiredExactAuthorizationCapabilityFacts": True,
    "requiredAuthorizationGrantCreated": False,
    "requiredAuthorizationTokenGenerated": False,
    "requiredAuthorizationMayBeConsumed": False,
    "successStatus": ACCEPTED_STATUS,
    "successReason": ACCEPTED_REASON,
    "blockedStatus": BLOCKED_STATUS,
    "accepted": True,
    "canonicalCopyRequired": True,
    "executionGrant": False,
}
if contract.get("acceptanceBoundary") != expected_acceptance_boundary:
    fail("Annahmegrenze ist nicht exakt gebunden.")

for block in ("securityBoundary", "futureBoundary"):
    values = contract.get(block, {})
    if not isinstance(values, dict) or not values:
        fail(f"{block} fehlt.")
    for key, value in values.items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

descriptor_module = load_module(
    DESCRIPTOR_MODULE,
    "v2733y_authorization_descriptor",
)
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE_MODULE,
    "v2733y_authorization_descriptor_acceptance",
)
readiness_module = load_module(
    READINESS_MODULE,
    "v2733y_authorization_readiness",
)
guard_module = load_module(
    GUARD_MODULE,
    "v2733y_authorization_readiness_acceptance",
)

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor",
    None,
)
accept_descriptor = getattr(
    descriptor_acceptance_module,
    "accept_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor",
    None,
)
resolve_readiness = getattr(
    readiness_module,
    "resolve_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness",
    None,
)
accept_readiness = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_readiness",
    None,
)
if not all(map(callable, (
    resolve_descriptor,
    accept_descriptor,
    resolve_readiness,
    accept_readiness,
))):
    fail("Erforderliche Resolver- oder Guard-Funktion fehlt.")

descriptor_result = resolve_descriptor({
    "contractFacts": clone(authorization_contract),
})
accepted_descriptor = accept_descriptor(descriptor_result)
readiness_result = resolve_readiness({
    "acceptedAuthorizationDescriptorResult": accepted_descriptor,
    "authorizationCapabilityFacts": clone(
        readiness_module.EXPECTED_AUTHORIZATION_CAPABILITY_FACTS
    ),
})
if readiness_result.get("status") != (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "authorization_readiness_ready_execution_locked"
):
    fail("Quell-Readiness liefert keinen Erfolgsstatus.")

before = clone(readiness_result)
original_open = builtins.open


def forbidden_open(*args, **kwargs):
    raise AssertionError(
        "Autorisierungs-Readiness-Annahme darf keine Datei öffnen."
    )


builtins.open = forbidden_open
try:
    first = accept_readiness(readiness_result)
    second = accept_readiness(readiness_result)
finally:
    builtins.open = original_open

if readiness_result != before:
    fail("Autorisierungs-Readiness-Annahme hat die Eingabe verändert.")
if first != second:
    fail("Autorisierungs-Readiness-Annahme ist nicht deterministisch.")
if first.get("status") != ACCEPTED_STATUS:
    fail("Erfolgsstatus ist ungültig.")
if first.get("reason") != ACCEPTED_REASON:
    fail("Erfolgsgrund ist ungültig.")
if first.get("accepted") is not True:
    fail("Annahmeflag fehlt.")
if first.get("acceptedReadiness") != readiness_result["readiness"]:
    fail("Angenommene Autorisierungs-Readiness ist nicht kanonisch.")
if first.get("acceptedReadiness") is readiness_result["readiness"]:
    fail("Angenommene Autorisierungs-Readiness ist keine Tiefenkopie.")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Ergebnisgrenze ist offen: {key}")

assert_blocked(accept_readiness(None), "Nicht-Mapping")

missing = clone(readiness_result)
missing.pop("readiness")
assert_blocked(accept_readiness(missing), "fehlendes Feld")

unknown = clone(readiness_result)
unknown["unknown"] = True
assert_blocked(accept_readiness(unknown), "unbekanntes Feld")

opened = clone(readiness_result)
opened["authorizationGranted"] = True
assert_blocked(accept_readiness(opened), "offene Quellgrenze")

leaf_count = 0
for path in iter_scalar_paths(readiness_result):
    manipulated = clone(readiness_result)
    set_path(manipulated, path)
    assert_blocked(
        accept_readiness(manipulated),
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
        fail(
            "Autorisierungs-Readiness-Annahme enthält verbotenen "
            f"Zugriff: {forbidden}"
        )

if FUTURE_ADAPTER.exists():
    fail("v27.33y darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33y darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733y*.sql")):
    fail("v27.33y darf keine SQL-Migration erzeugen.")

print(
    "Registry-Adapter-Implementierungsausführungs-"
    "Autorisierungs-Readiness-Annahme-Guard: OK"
)
print("Quell-Readiness: v27.33x")
print(f"Manipulierte Readiness-Blätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff des Guards: keiner")
print("Autorisierungsgrant erstellt: nein")
print("Autorisierungstoken erzeugt: nein")
print("Autorisierung verbrauchbar: nein")
print("Adaptermodul erstellt: nein")
print("Adapter importiert: nein")
print("Adapter instanziiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33y: keine")
print("Produktive Freigabe: nein")
