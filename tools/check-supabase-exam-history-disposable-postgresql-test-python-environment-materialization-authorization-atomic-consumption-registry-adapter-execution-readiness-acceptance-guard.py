from pathlib import Path
import ast
import copy
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-readiness-acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-readiness-contract.json"
)
EXECUTION_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-contract.json"
)
DESCRIPTOR_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor.py"
)
DESCRIPTOR_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor_acceptance_guard.py"
)
READINESS_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness.py"
)
GUARD_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness_acceptance_guard.py"
)
FUTURE_PLAN = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_plan.py"
)
FUTURE_EXECUTION = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution.py"
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
    if result.get("accepted") is not False:
        fail(f"Manipulation nicht blockiert: {label}")
    if result.get("acceptedReadiness") is not None:
        fail(f"Blockiertes Ergebnis enthält Readiness: {label}")
    if result.get("executionGrant") is not False:
        fail(f"Blockiertes Ergebnis öffnet Grant: {label}")


contract = load_json(CONTRACT, "v27.33d-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.33c-Quellvertrag")
execution_contract = load_json(EXECUTION_CONTRACT, "v27.32z-Vertrag")

if contract.get("version") != "v27.33d":
    fail("Annahmevertrag besitzt nicht v27.33d.")
if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "readiness_acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33c":
    fail("Quellvertrag besitzt nicht v27.33c.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "readiness_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if source_contract.get("implementation", {}).get(
    "executionReadinessImplemented"
) is not True:
    fail("Quell-Readiness ist nicht implementiert.")

implementation = contract.get("implementation", {})
if implementation.get("executionReadinessAcceptanceGuardImplemented") is not True:
    fail("Readiness-Annahme-Guard fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == "executionReadinessAcceptanceGuardImplemented":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

source = GUARD_MODULE.read_text(encoding="utf-8")
tree = ast.parse(source)
allowed_imports = {"__future__", "collections", "copy", "json"}
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
    "open(", "read_text(", "read_bytes(", "write_text(", "write_bytes(",
    "datetime.now(", "time.time(", "uuid4(", "urandom(",
    "compare_and_set(", "registry.read", "registry.write", "adapter.invoke",
    "subprocess", ".connect(", "postgres://", "postgresql://",
    "database_url", "service_role",
):
    if marker in source.lower():
        fail(f"Annahme-Guard enthält verbotenen Inhalt: {marker}")

descriptor_module = load_module(DESCRIPTOR_MODULE, "descriptor_v2733d")
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE_MODULE, "descriptor_acceptance_v2733d"
)
readiness_module = load_module(READINESS_MODULE, "readiness_v2733d")
guard_module = load_module(GUARD_MODULE, "readiness_acceptance_v2733d")

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_execution_descriptor",
    None,
)
accept_descriptor = getattr(
    descriptor_acceptance_module,
    "accept_atomic_consumption_registry_adapter_execution_descriptor",
    None,
)
resolve_readiness = getattr(
    readiness_module,
    "resolve_atomic_consumption_registry_adapter_execution_readiness",
    None,
)
expected_adapter_facts = getattr(
    readiness_module,
    "_EXPECTED_ADAPTER_FACTS",
    None,
)
accept_readiness = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_execution_readiness",
    None,
)
locked_flags = getattr(guard_module, "_LOCKED_FLAGS", None)

if not callable(resolve_descriptor):
    fail("Descriptor-Resolver fehlt.")
if not callable(accept_descriptor):
    fail("Descriptor-Annahme fehlt.")
if not callable(resolve_readiness) or not isinstance(expected_adapter_facts, dict):
    fail("Readiness-Resolver ist nicht nutzbar.")
if not callable(accept_readiness):
    fail("Readiness-Annahme fehlt.")
if not isinstance(locked_flags, tuple):
    fail("Gesperrte Ergebnisflags fehlen.")

resolved_descriptor = resolve_descriptor({"contractFacts": clone(execution_contract)})
accepted_descriptor = accept_descriptor(resolved_descriptor)
readiness_result = resolve_readiness({
    "acceptedExecutionDescriptorResult": accepted_descriptor,
    "adapterFacts": clone(expected_adapter_facts),
})

accepted = accept_readiness(readiness_result)
if accepted.get("status") != (
    "accepted_atomic_consumption_registry_adapter_execution_"
    "readiness_execution_locked"
):
    fail("Gültige Readiness wurde nicht angenommen.")
if accepted.get("reason") != (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness_accepted_execution_locked"
):
    fail("Annahmegrund ist ungültig.")
if accepted.get("accepted") is not True:
    fail("Annahmeflag fehlt.")
if accepted.get("acceptedReadiness") != readiness_result.get("readiness"):
    fail("Angenommene Readiness ist nicht kanonisch.")
if accepted.get("acceptedReadiness") is readiness_result.get("readiness"):
    fail("Angenommene Readiness ist keine Tiefenkopie.")
if readiness_result.get("executionGrant") is not False:
    fail("Quell-Readiness öffnet Grant.")
for key in locked_flags:
    if accepted.get(key) is not False:
        fail(f"Annahme-Ergebnisflag ist offen: {key}")

before = clone(readiness_result)
again = accept_readiness(readiness_result)
if again != accepted:
    fail("Readiness-Annahme ist nicht deterministisch.")
if readiness_result != before:
    fail("Readiness-Annahme verändert die Eingabe.")

assert_blocked(accept_readiness([]), "Nicht-Mapping")
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
opened["registryWritePerformed"] = True
assert_blocked(accept_readiness(opened), "offene Quellgrenze")
wrong_readiness = clone(readiness_result)
wrong_readiness["readiness"] = []
assert_blocked(accept_readiness(wrong_readiness), "falsche Readiness")

leaf_count = 0
for path in iter_scalar_paths(readiness_result["readiness"]):
    manipulated = clone(readiness_result)
    set_path(manipulated["readiness"], path)
    assert_blocked(accept_readiness(manipulated), "Manipulation " + ".".join(map(str, path)))
    leaf_count += 1

accepted_readiness = accepted["acceptedReadiness"]
first_path = next(iter(iter_scalar_paths(accepted_readiness)))
set_path(accepted_readiness, first_path)
if accepted_readiness == readiness_result["readiness"]:
    fail("Tiefenkopie ist mit Quelle gekoppelt.")

if FUTURE_PLAN.exists():
    fail("v27.33d darf noch keinen Ausführungsplan umsetzen.")
if FUTURE_EXECUTION.exists():
    fail("v27.33d darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733d*.sql")):
    fail("v27.33d darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Ausführungs-Readiness-Annahme-Guard: OK")
print("Quell-Readiness: v27.33c")
print(f"Manipulierte Readiness-Blätter blockiert: {leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33d: keine")
print("Produktive Freigabe: nein")
