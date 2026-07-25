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
    "contract.json"
)
SOURCE = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-authorization-contract.json"
)
MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor.py"
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
    "authorization_descriptor_ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor_"
    "ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_execution_"
    "authorization_descriptor_blocked_execution_locked"
)
BLOCKED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor_contract_invalid"
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
    if result.get("reason") != BLOCKED_REASON:
        fail(f"Blockgrund ist ungültig: {label}")
    if result.get("ready") is not False:
        fail(f"Blockiertes Ergebnis meldet Readiness: {label}")
    if result.get("descriptor") is not None:
        fail(f"Blockiertes Ergebnis enthält Descriptor: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockierte Grenze offen: {key} / {label}")


contract = load_json(CONTRACT, "v27.33v-Vertrag")
source = load_json(SOURCE, "v27.33u-Quellvertrag")
module = load_module(MODULE, "v2733v_authorization_descriptor")

resolver = getattr(
    module,
    "resolve_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor",
    None,
)
if not callable(resolver):
    fail("Implementierungsausführungs-Autorisierungsdescriptor fehlt.")

if contract.get("version") != "v27.33v":
    fail("Descriptorvertrag besitzt nicht v27.33v.")
if contract.get("contractVersion") != 1:
    fail("Descriptorvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_execution_authorization_descriptor_"
    "execution_locked"
):
    fail("Descriptorvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source.get("version") != "v27.33u":
    fail("Quellvertrag besitzt nicht v27.33u.")
if source.get("status") != (
    "planned_atomic_consumption_registry_adapter_implementation_"
    "execution_authorization_fully_locked_not_implemented"
):
    fail("Quellvertragsstatus ist ungültig.")

implementation = contract.get("implementation", {})
if implementation.get("authorizationDescriptorImplemented") is not True:
    fail("Autorisierungsdescriptor fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == "authorizationDescriptorImplemented":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

input_boundary = contract.get("inputBoundary", {})
expected_input = {
    "mappingOnly": True,
    "exactFields": ["contractFacts"],
    "requiredSourceVersion": "v27.33u",
    "requiredSourceStatus": source["status"],
    "exactContractFactsRequired": True,
    "unknownFieldsAllowed": False,
    "missingFieldsAllowed": False,
    "inputMutationAllowed": False,
}
for key, expected in expected_input.items():
    if input_boundary.get(key) != expected:
        fail(f"Eingabegrenze ist ungültig: {key}")

descriptor_boundary = contract.get("descriptorBoundary", {})
expected_descriptor = {
    "descriptorVersion": 1,
    "successStatus": SUCCESS_STATUS,
    "successReason": SUCCESS_REASON,
    "blockedStatus": BLOCKED_STATUS,
    "blockedReason": BLOCKED_REASON,
    "ready": True,
    "canonicalCopyRequired": True,
    "sourceContractVersion": "v27.33u",
    "sourceContractStatus": source["status"],
    "authorizationGrantCreated": False,
    "authorizationTokenGenerated": False,
    "authorizationMayBeConsumed": False,
    "executionGrant": False,
}
for key, expected in expected_descriptor.items():
    if descriptor_boundary.get(key) != expected:
        fail(f"Descriptorgrenze ist ungültig: {key}")

for block in ("securityBoundary", "futureBoundary"):
    values = contract.get(block, {})
    if not isinstance(values, dict) or not values:
        fail(f"{block} fehlt.")
    for key, value in values.items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

input_value = {"contractFacts": clone(source)}
before = clone(input_value)
original_open = builtins.open

def forbidden_open(*args, **kwargs):
    raise AssertionError(
        "Autorisierungsdescriptor darf keine Datei öffnen."
    )

builtins.open = forbidden_open
try:
    first = resolver(input_value)
    second = resolver(input_value)
finally:
    builtins.open = original_open

if input_value != before:
    fail("Autorisierungsdescriptor hat die Eingabe verändert.")
if first != second:
    fail("Autorisierungsdescriptor ist nicht deterministisch.")
if first.get("status") != SUCCESS_STATUS:
    fail("Erfolgsstatus ist ungültig.")
if first.get("reason") != SUCCESS_REASON:
    fail("Erfolgsgrund ist ungültig.")
if first.get("ready") is not True:
    fail("Gültiger Autorisierungsdescriptor ist nicht bereit.")

descriptor = first.get("descriptor")
if not isinstance(descriptor, dict):
    fail("Kanonischer Autorisierungsdescriptor fehlt.")
if descriptor.get("descriptorVersion") != 1:
    fail("Descriptorversion ist ungültig.")
if descriptor.get("sourceContractVersion") != "v27.33u":
    fail("Descriptor-Quellversion ist ungültig.")
if descriptor.get("sourceContractStatus") != source["status"]:
    fail("Descriptor-Quellstatus ist ungültig.")
if descriptor.get("contractFacts") != source:
    fail("Vertragsfakten wurden nicht kanonisch kopiert.")
if descriptor.get("contractFacts") is input_value["contractFacts"]:
    fail("Vertragsfakten wurden nicht tief kopiert.")

for key in (
    "authorizationGrantCreated",
    "authorizationTokenGenerated",
    "authorizationMayBeConsumed",
    "executionGrant",
):
    if descriptor.get(key) is not False:
        fail(f"Descriptor öffnet Grenze: {key}")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Ergebnisgrenze ist offen: {key}")

assert_blocked(resolver(None), "Nicht-Mapping")
assert_blocked(resolver({}), "fehlendes Feld")
assert_blocked(
    resolver({"contractFacts": clone(source), "unknown": True}),
    "unbekanntes Feld",
)
assert_blocked(
    resolver({"contractFacts": []}),
    "falscher Faktentyp",
)

leaf_count = 0
for path in iter_scalar_paths(source):
    manipulated = clone(source)
    set_path(manipulated, path)
    assert_blocked(
        resolver({"contractFacts": manipulated}),
        ".".join(map(str, path)),
    )
    leaf_count += 1

source_text = MODULE.read_text(encoding="utf-8").lower()
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
        fail(f"Descriptor enthält verbotenen Zugriff: {forbidden}")

if FUTURE_ADAPTER.exists():
    fail("v27.33v darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33v darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733v*.sql")):
    fail("v27.33v darf keine SQL-Migration erzeugen.")

print(
    "Registry-Adapter-Implementierungsausführungs-"
    "Autorisierungsdescriptor: OK"
)
print("Quellvertrag: v27.33u")
print(f"Manipulierte Vertragsblätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff des Resolvers: keiner")
print("Autorisierungsgrant erstellt: nein")
print("Autorisierungstoken erzeugt: nein")
print("Autorisierung verbrauchbar: nein")
print("Adaptermodul erstellt: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33v: keine")
print("Produktive Freigabe: nein")
