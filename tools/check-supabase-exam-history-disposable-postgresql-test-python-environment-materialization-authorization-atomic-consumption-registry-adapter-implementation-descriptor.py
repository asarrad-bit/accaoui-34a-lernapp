from __future__ import annotations

import builtins
import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor.py"
)
CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-descriptor-contract.json"
)
SOURCE = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-contract.json"
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
    "atomic_consumption_registry_adapter_implementation_descriptor_"
    "ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_descriptor_"
    "blocked_execution_locked"
)
BLOCKED_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_contract_invalid"
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


def load_module():
    if not MODULE.is_file():
        fail("v27.33h-Descriptor fehlt.")
    spec = importlib.util.spec_from_file_location(
        "v2733h_implementation_descriptor",
        MODULE,
    )
    if spec is None or spec.loader is None:
        fail("v27.33h-Descriptor kann nicht geladen werden.")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def iter_scalar_paths(value, path=()):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from iter_scalar_paths(item, path + (key,))
        return
    if isinstance(value, list):
        for index, item in enumerate(value):
            yield from iter_scalar_paths(item, path + (index,))
        return
    yield path


def mutate_scalar(value):
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, str):
        return value + "_tampered"
    if value is None:
        return "tampered"
    return {"tampered": True}


def set_path(value, path):
    target = value
    for part in path[:-1]:
        target = target[part]
    leaf = path[-1]
    target[leaf] = mutate_scalar(target[leaf])


def assert_blocked(result, label):
    if result.get("status") != BLOCKED_STATUS:
        fail(f"Manipulation wurde nicht blockiert: {label}")
    if result.get("reason") != BLOCKED_REASON:
        fail(f"Blockgrund ist ungültig: {label}")
    if result.get("ready") is not False:
        fail(f"Blockiertes Ergebnis ist bereit: {label}")
    if result.get("descriptor") is not None:
        fail(f"Blockiertes Ergebnis enthält Descriptor: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockiertes Ergebnis öffnet Grenze {key}: {label}")


contract = load_json(CONTRACT, "v27.33h-Vertrag")
source = load_json(SOURCE, "v27.33g-Quellvertrag")
module = load_module()
resolver = getattr(
    module,
    "resolve_atomic_consumption_registry_adapter_implementation_descriptor",
    None,
)
if not callable(resolver):
    fail("Implementierungsdescriptor-Resolver fehlt.")

if contract.get("version") != "v27.33h":
    fail("Descriptorvertrag besitzt nicht v27.33h.")
if contract.get("contractVersion") != 1:
    fail("Descriptorvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_descriptor_execution_locked"
):
    fail("Descriptorvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source.get("version") != "v27.33g":
    fail("Quellvertrag besitzt nicht v27.33g.")
if source.get("status") != (
    "planned_atomic_consumption_registry_adapter_implementation_"
    "fully_locked_not_implemented"
):
    fail("Quellvertragsstatus ist ungültig.")

implementation = contract.get("implementation", {})
if implementation.get("implementationDescriptorImplemented") is not True:
    fail("Implementierungsdescriptor ist nicht markiert.")
for key, value in implementation.items():
    if key.endswith("Path") or key == "implementationDescriptorImplemented":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

input_boundary = contract.get("inputBoundary", {})
required_input = {
    "mappingOnly": True,
    "exactFields": ["contractFacts"],
    "requiredSourceVersion": "v27.33g",
    "requiredSourceStatus": (
        "planned_atomic_consumption_registry_adapter_implementation_"
        "fully_locked_not_implemented"
    ),
    "exactContractFactsRequired": True,
    "unknownFieldsAllowed": False,
    "missingFieldsAllowed": False,
    "inputMutationAllowed": False,
}
for key, expected in required_input.items():
    if input_boundary.get(key) != expected:
        fail(f"Eingabegrenze ist ungültig: {key}")

descriptor_boundary = contract.get("descriptorBoundary", {})
required_descriptor = {
    "descriptorVersion": 1,
    "successStatus": SUCCESS_STATUS,
    "successReason": SUCCESS_REASON,
    "blockedStatus": BLOCKED_STATUS,
    "blockedReason": BLOCKED_REASON,
    "ready": True,
    "canonicalCopyRequired": True,
    "sourceContractVersion": "v27.33g",
    "sourceContractStatus": source["status"],
    "executionGrant": False,
}
for key, expected in required_descriptor.items():
    if descriptor_boundary.get(key) != expected:
        fail(f"Descriptorgrenze ist ungültig: {key}")

for key, value in contract.get("securityBoundary", {}).items():
    if value is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")
for key, value in contract.get("futureBoundary", {}).items():
    if value is not False:
        fail(f"Zukunftsgrenze ist offen: {key}")

valid_input = {"contractFacts": copy.deepcopy(source)}
before = copy.deepcopy(valid_input)
original_open = builtins.open


def forbidden_open(*args, **kwargs):
    raise AssertionError("Descriptor darf keine Datei öffnen.")


builtins.open = forbidden_open
try:
    first = resolver(valid_input)
    second = resolver(valid_input)
finally:
    builtins.open = original_open

if valid_input != before:
    fail("Descriptor hat die Eingabe verändert.")
if first != second:
    fail("Descriptor ist nicht deterministisch.")
if first.get("status") != SUCCESS_STATUS:
    fail("Erfolgsstatus ist ungültig.")
if first.get("reason") != SUCCESS_REASON:
    fail("Erfolgsgrund ist ungültig.")
if first.get("ready") is not True:
    fail("Gültiger Descriptor ist nicht bereit.")

descriptor = first.get("descriptor")
if not isinstance(descriptor, dict):
    fail("Kanonischer Descriptor fehlt.")
if descriptor.get("descriptorVersion") != 1:
    fail("Descriptorversion ist ungültig.")
if descriptor.get("sourceContractVersion") != "v27.33g":
    fail("Descriptor-Quellversion ist ungültig.")
if descriptor.get("sourceContractStatus") != source.get("status"):
    fail("Descriptor-Quellstatus ist ungültig.")
if descriptor.get("contractFacts") != source:
    fail("Vertragsfakten wurden nicht kanonisch kopiert.")
if descriptor.get("contractFacts") is valid_input["contractFacts"]:
    fail("Vertragsfakten wurden nicht tief kopiert.")
if descriptor.get("executionGrant") is not False:
    fail("Kanonischer Descriptor öffnet den Grant.")

for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Ergebnisgrenze ist offen: {key}")

valid_input["contractFacts"]["version"] = "mutated_after_result"
if descriptor["contractFacts"] != source:
    fail("Descriptor ist nicht von späterer Eingabemutation getrennt.")

assert_blocked(resolver(None), "nicht Mapping")
assert_blocked(resolver({}), "fehlendes Feld")
assert_blocked(
    resolver({"contractFacts": copy.deepcopy(source), "unknown": True}),
    "unbekanntes Feld",
)
assert_blocked(resolver({"contractFacts": []}), "falscher Faktentyp")

for key in source:
    candidate = copy.deepcopy(source)
    candidate.pop(key)
    assert_blocked(
        resolver({"contractFacts": candidate}),
        f"fehlender Vertragsblock {key}",
    )

unknown = copy.deepcopy(source)
unknown["unknownContractFact"] = True
assert_blocked(
    resolver({"contractFacts": unknown}),
    "unbekannter Vertragsblock",
)

leaf_count = 0
for path in iter_scalar_paths(source):
    candidate = copy.deepcopy(source)
    set_path(candidate, path)
    assert_blocked(
        resolver({"contractFacts": candidate}),
        "manipulierter Pfad " + ".".join(map(str, path)),
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
    fail("v27.33h darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33h darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733h*.sql")):
    fail("v27.33h darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungsdescriptor: OK")
print("Quellvertrag: v27.33g")
print(f"Manipulierte Vertragsblätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff des Resolvers: keiner")
print("Adaptermodul erstellt: nein")
print("Adapter importiert: nein")
print("Adapter instanziiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33h: keine")
print("Produktive Freigabe: nein")
