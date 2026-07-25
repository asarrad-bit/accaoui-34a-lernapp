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
    "adapter-implementation-readiness-acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-readiness-contract.json"
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
DESCRIPTOR_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_descriptor_acceptance_guard.py"
)
READINESS_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness.py"
)
GUARD_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness_acceptance_guard.py"
)
FUTURE_PLAN = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_plan.py"
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
    "readiness_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_"
    "implementation_readiness_accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_implementation_readiness_"
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
    if result.get("acceptedReadiness") is not None:
        fail(f"Blockiertes Ergebnis enthält Readiness: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockiertes Ergebnis öffnet Grenze {key}: {label}")


contract = load_json(CONTRACT, "v27.33k-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.33j-Quellvertrag")
implementation_contract = load_json(
    IMPLEMENTATION_CONTRACT,
    "v27.33g-Implementierungsvertrag",
)

if contract.get("version") != "v27.33k":
    fail("Readiness-Annahmevertrag besitzt nicht v27.33k.")
if contract.get("contractVersion") != 1:
    fail("Readiness-Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_readiness_acceptance_execution_locked"
):
    fail("Readiness-Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33j":
    fail("Quellvertrag besitzt nicht v27.33j.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_readiness_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if implementation_contract.get("version") != "v27.33g":
    fail("Implementierungsvertrag besitzt nicht v27.33g.")

implementation = contract.get("implementation", {})
if implementation.get(
    "implementationReadinessAcceptanceGuardImplemented"
) is not True:
    fail("Implementierungs-Readiness-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == (
        "implementationReadinessAcceptanceGuardImplemented"
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
    "implementation_descriptor_v2733k",
)
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE_MODULE,
    "implementation_descriptor_acceptance_v2733k",
)
readiness_module = load_module(
    READINESS_MODULE,
    "implementation_readiness_v2733k",
)
guard_module = load_module(
    GUARD_MODULE,
    "implementation_readiness_acceptance_v2733k",
)

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_implementation_descriptor",
    None,
)
accept_descriptor = getattr(
    descriptor_acceptance_module,
    "accept_atomic_consumption_registry_adapter_implementation_descriptor",
    None,
)
resolve_readiness = getattr(
    readiness_module,
    "resolve_atomic_consumption_registry_adapter_implementation_readiness",
    None,
)
accept_readiness = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_implementation_readiness",
    None,
)
if not callable(resolve_descriptor):
    fail("Implementierungsdescriptor-Resolver fehlt.")
if not callable(accept_descriptor):
    fail("Implementierungsdescriptor-Annahme fehlt.")
if not callable(resolve_readiness):
    fail("Implementierungs-Readiness-Resolver fehlt.")
if not callable(accept_readiness):
    fail("Implementierungs-Readiness-Annahme fehlt.")

descriptor_result = resolve_descriptor({
    "contractFacts": clone(implementation_contract),
})
accepted_descriptor = accept_descriptor(descriptor_result)
facts = clone(
    getattr(readiness_module, "_EXPECTED_IMPLEMENTATION_FACTS", None)
)
if not isinstance(facts, dict):
    fail("Kanonische Implementierungsfähigkeitsfakten fehlen.")

readiness_result = resolve_readiness({
    "acceptedImplementationDescriptorResult": accepted_descriptor,
    "implementationFacts": facts,
})
if readiness_result.get("status") != (
    "atomic_consumption_registry_adapter_implementation_readiness_"
    "ready_execution_locked"
):
    fail("Quell-Readiness liefert keinen Erfolgsstatus.")

before = clone(readiness_result)
original_open = builtins.open


def forbidden_open(*args, **kwargs):
    raise AssertionError("Readiness-Annahme darf keine Datei öffnen.")


builtins.open = forbidden_open
try:
    accepted = accept_readiness(readiness_result)
    again = accept_readiness(readiness_result)
finally:
    builtins.open = original_open

if readiness_result != before:
    fail("Readiness-Annahme hat die Eingabe verändert.")
if accepted != again:
    fail("Readiness-Annahme ist nicht deterministisch.")
if accepted.get("status") != SUCCESS_STATUS:
    fail("Gültige Readiness wurde nicht angenommen.")
if accepted.get("reason") != SUCCESS_REASON:
    fail("Annahmegrund ist ungültig.")
if accepted.get("accepted") is not True:
    fail("Annahmeflag fehlt.")
if accepted.get("acceptedReadiness") != readiness_result.get("readiness"):
    fail("Angenommene Readiness ist nicht kanonisch.")
if accepted.get("acceptedReadiness") is readiness_result.get("readiness"):
    fail("Angenommene Readiness ist keine Tiefenkopie.")
for key in LOCKED_FLAGS:
    if accepted.get(key) is not False:
        fail(f"Annahme-Ergebnisflag ist offen: {key}")

assert_blocked(accept_readiness(None), "Nicht-Mapping")
missing = clone(readiness_result)
missing.pop("readiness")
assert_blocked(accept_readiness(missing), "fehlendes Feld")
unknown = clone(readiness_result)
unknown["unknown"] = True
assert_blocked(accept_readiness(unknown), "unbekanntes Feld")
wrong_status = clone(readiness_result)
wrong_status["status"] = "wrong"
assert_blocked(accept_readiness(wrong_status), "falscher Status")
wrong_reason = clone(readiness_result)
wrong_reason["reason"] = "wrong"
assert_blocked(accept_readiness(wrong_reason), "falscher Grund")
not_ready = clone(readiness_result)
not_ready["ready"] = False
assert_blocked(accept_readiness(not_ready), "ready false")
opened = clone(readiness_result)
opened["adapterImported"] = True
assert_blocked(accept_readiness(opened), "offene Quellgrenze")
wrong_readiness = clone(readiness_result)
wrong_readiness["readiness"] = []
assert_blocked(accept_readiness(wrong_readiness), "falsche Readiness")

leaf_count = 0
for path in iter_scalar_paths(readiness_result["readiness"]):
    manipulated = clone(readiness_result)
    set_path(manipulated["readiness"], path)
    assert_blocked(
        accept_readiness(manipulated),
        "Readiness-Manipulation " + ".".join(map(str, path)),
    )
    leaf_count += 1

accepted_readiness = accepted["acceptedReadiness"]
first_path = next(iter(iter_scalar_paths(accepted_readiness)))
set_path(accepted_readiness, first_path)
if accepted_readiness == readiness_result["readiness"]:
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
        fail(f"Readiness-Annahme enthält verbotenen Zugriff: {forbidden}")

if FUTURE_PLAN.exists():
    fail("v27.33k darf noch keinen Implementierungsplan umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.33k darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33k darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733k*.sql")):
    fail("v27.33k darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungs-Readiness-Annahme-Guard: OK")
print("Quell-Readiness: v27.33j")
print(f"Manipulierte Readiness-Blätter blockiert: {leaf_count}")
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
print("SQL-Migration v27.33k: keine")
print("Produktive Freigabe: nein")
