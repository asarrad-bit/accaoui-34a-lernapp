from pathlib import Path
import ast
import builtins
import copy
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-descriptor-acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-descriptor-contract.json"
)
EXECUTION_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-contract.json"
)
DESCRIPTOR = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor.py"
)
GUARD = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor_acceptance_guard.py"
)
FUTURE_READINESS = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness.py"
)
FUTURE_EXECUTION = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution.py"
)

SOURCE_STATUS = (
    "atomic_consumption_registry_adapter_execution_descriptor_"
    "ready_execution_locked"
)
SOURCE_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor_ready_execution_locked"
)
ACCEPTED_STATUS = (
    "accepted_atomic_consumption_registry_adapter_execution_"
    "descriptor_execution_locked"
)
ACCEPTED_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor_accepted_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_execution_descriptor_"
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
    if not path.is_file():
        fail(f"Modul fehlt: {path.name}")
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        fail(f"Modul ist nicht ladbar: {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clone(value):
    return copy.deepcopy(value)


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
    target[path[-1]] = mutate_scalar(target[path[-1]])


def assert_blocked(result, label):
    if result.get("status") != BLOCKED_STATUS:
        fail(f"Manipulation wurde nicht blockiert: {label}")
    if result.get("accepted") is not False:
        fail(f"Blockiertes Ergebnis wurde akzeptiert: {label}")
    if result.get("acceptedDescriptor") is not None:
        fail(f"Blockiertes Ergebnis enthält Descriptor: {label}")
    if result.get("executionGrant") is not False:
        fail(f"Blockiertes Ergebnis öffnet Grant: {label}")


contract = load_json(CONTRACT, "v27.33b-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.33a-Quellvertrag")
execution_contract = load_json(EXECUTION_CONTRACT, "v27.32z-Ausführungsvertrag")

descriptor_module = load_module(DESCRIPTOR, "v2733a_descriptor")
guard_module = load_module(GUARD, "v2733b_descriptor_acceptance")
resolver = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_execution_descriptor",
    None,
)
accept = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_execution_descriptor",
    None,
)
locked_flags = getattr(guard_module, "_LOCKED_FLAGS", None)

if not callable(resolver):
    fail("Quell-Descriptor-Resolver fehlt.")
if not callable(accept):
    fail("Descriptor-Annahmefunktion fehlt.")
if not isinstance(locked_flags, tuple):
    fail("Gesperrte Ergebnisfelder fehlen.")

if contract.get("version") != "v27.33b":
    fail("Annahmevertrag besitzt nicht v27.33b.")
if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "descriptor_acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")
if source_contract.get("version") != "v27.33a":
    fail("Quellvertrag besitzt nicht v27.33a.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "descriptor_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if execution_contract.get("version") != "v27.32z":
    fail("Ausführungsvertrag besitzt nicht v27.32z.")

implementation = contract.get("implementation", {})
if implementation.get("executionDescriptorAcceptanceGuardImplemented") is not True:
    fail("Descriptor-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == "executionDescriptorAcceptanceGuardImplemented":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

boundary = contract.get("acceptanceBoundary", {})
required = {
    "requiredSourceStatus": SOURCE_STATUS,
    "requiredSourceReason": SOURCE_REASON,
    "requiredReady": True,
    "requiredDescriptorVersion": 1,
    "requiredSourceContractVersion": "v27.32z",
    "requiredSourceContractStatus": (
        "planned_atomic_consumption_registry_adapter_execution_"
        "fully_locked_not_implemented"
    ),
    "successStatus": ACCEPTED_STATUS,
    "successReason": ACCEPTED_REASON,
    "accepted": True,
    "canonicalCopyRequired": True,
    "executionGrant": False,
}
for key, expected in required.items():
    if boundary.get(key) != expected:
        fail(f"Annahmegrenze ist ungültig: {key}")
for key, value in contract.get("securityBoundary", {}).items():
    if value is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")
for key, value in contract.get("futureBoundary", {}).items():
    if value is not False:
        fail(f"Zukunftsgrenze ist offen: {key}")

guard_source = GUARD.read_text(encoding="utf-8")
tree = ast.parse(guard_source)
allowed_imports = {"__future__", "copy", "json", "collections"}
seen = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen.add(alias.name.split(".", 1)[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        seen.add(node.module.split(".", 1)[0])
if seen - allowed_imports:
    fail(f"Annahme-Guard besitzt unerlaubte Importe: {seen - allowed_imports}")

for marker in (
    "open(",
    "read_text(",
    "read_bytes(",
    "write_text(",
    "write_bytes(",
    "subprocess",
    "socket",
    "psycopg",
    "supabase",
    "requests",
    "urllib",
    "sqlite3",
    ".connect(",
    "registry.read",
    "registry.write",
    "adapter.invoke",
):
    if marker in guard_source.lower():
        fail(f"Annahme-Guard enthält verbotenen Zugriff: {marker}")

source_result = resolver({"contractFacts": clone(execution_contract)})
if source_result.get("status") != SOURCE_STATUS:
    fail("Quell-Descriptor liefert keinen Erfolgsstatus.")

before = clone(source_result)
original_open = builtins.open


def forbidden_open(*args, **kwargs):
    raise AssertionError("Annahme-Guard darf keine Datei öffnen.")


builtins.open = forbidden_open
try:
    first = accept(source_result)
    second = accept(source_result)
finally:
    builtins.open = original_open

if source_result != before:
    fail("Annahme-Guard hat die Eingabe verändert.")
if first != second:
    fail("Annahme-Guard ist nicht deterministisch.")
if first.get("status") != ACCEPTED_STATUS:
    fail("Annahmestatus ist ungültig.")
if first.get("reason") != ACCEPTED_REASON:
    fail("Annahmegrund ist ungültig.")
if first.get("accepted") is not True:
    fail("Gültiger Descriptor wurde nicht akzeptiert.")
if first.get("executionGrant") is not False:
    fail("Annahme öffnet den Grant.")
accepted_descriptor = first.get("acceptedDescriptor")
if accepted_descriptor != source_result.get("descriptor"):
    fail("Descriptor wurde nicht kanonisch kopiert.")
if accepted_descriptor is source_result.get("descriptor"):
    fail("Descriptor wurde nicht tief kopiert.")
for key in locked_flags:
    if first.get(key) is not False:
        fail(f"Ergebnisgrenze ist offen: {key}")

source_result["descriptor"]["sourceContractVersion"] = "mutated_after_result"
if accepted_descriptor.get("sourceContractVersion") != "v27.32z":
    fail("Annahmekopie ist nicht von Eingabemutation getrennt.")

assert_blocked(accept(None), "nicht Mapping")
missing = clone(before)
missing.pop("descriptor")
assert_blocked(accept(missing), "fehlendes Feld")
unknown = clone(before)
unknown["unknown"] = True
assert_blocked(accept(unknown), "unbekanntes Feld")
status = clone(before)
status["status"] = "wrong"
assert_blocked(accept(status), "falscher Status")
reason = clone(before)
reason["reason"] = "wrong"
assert_blocked(accept(reason), "falscher Grund")
ready = clone(before)
ready["ready"] = False
assert_blocked(accept(ready), "ready false")
opened = clone(before)
opened["registryWritePerformed"] = True
assert_blocked(accept(opened), "offene Quellgrenze")
wrong_descriptor = clone(before)
wrong_descriptor["descriptor"] = []
assert_blocked(accept(wrong_descriptor), "falscher Descriptortyp")
missing_descriptor = clone(before)
missing_descriptor["descriptor"].pop("contractFacts")
assert_blocked(accept(missing_descriptor), "fehlendes Descriptorfeld")
unknown_descriptor = clone(before)
unknown_descriptor["descriptor"]["unknown"] = True
assert_blocked(accept(unknown_descriptor), "unbekanntes Descriptorfeld")
version = clone(before)
version["descriptor"]["descriptorVersion"] = 2
assert_blocked(accept(version), "falsche Descriptorversion")
source_version = clone(before)
source_version["descriptor"]["sourceContractVersion"] = "v27.32y"
assert_blocked(accept(source_version), "falsche Quellversion")
leaf_count = 0
for path in iter_scalar_paths(execution_contract):
    contract_facts = clone(before)
    set_path(contract_facts["descriptor"]["contractFacts"], path)
    assert_blocked(
        accept(contract_facts),
        "manipulierte Vertragsfakten " + ".".join(map(str, path)),
    )
    leaf_count += 1

descriptor_grant = clone(before)
descriptor_grant["descriptor"]["executionGrant"] = True
assert_blocked(accept(descriptor_grant), "offener Descriptorgrant")

if FUTURE_READINESS.exists():
    fail("v27.33b darf noch keine Ausführungs-Readiness umsetzen.")
if FUTURE_EXECUTION.exists():
    fail("v27.33b darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733b*.sql")):
    fail("v27.33b darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Ausführungsdescriptor-Annahme-Guard: OK")
print("Quell-Descriptor: v27.33a")
print("Kanonische Tiefenkopie: geprüft")
print(f"Manipulierte Vertragsblätter blockiert: {leaf_count}")
print("Eingabemutation: keine")
print("Dateizugriff des Guards: keiner")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33b: keine")
print("Produktive Freigabe: nein")
