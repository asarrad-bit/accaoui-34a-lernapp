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
    "adapter-execution-plan-contract.json"
)
SOURCE_ACCEPTANCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-readiness-acceptance-guard-contract.json"
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
READINESS_ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness_acceptance_guard.py"
)
PLAN_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_plan.py"
)
FUTURE_ACCEPTANCE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_plan_"
    "acceptance_guard.py"
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
    if result.get("ready") is not False:
        fail(f"Manipulation nicht blockiert: {label}")
    if result.get("plan") is not None:
        fail(f"Blockiertes Ergebnis enthält Plan: {label}")
    if result.get("executionGrant") is not False:
        fail(f"Blockiertes Ergebnis öffnet Grant: {label}")


contract = load_json(CONTRACT, "v27.33e-Vertrag")
source_contract = load_json(
    SOURCE_ACCEPTANCE_CONTRACT,
    "v27.33d-Quellvertrag",
)
execution_contract = load_json(EXECUTION_CONTRACT, "v27.32z-Vertrag")

if contract.get("version") != "v27.33e":
    fail("Ausführungsplanvertrag besitzt nicht v27.33e.")
if contract.get("contractVersion") != 1:
    fail("Ausführungsplanvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "plan_execution_locked"
):
    fail("Ausführungsplanvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.33d":
    fail("Quellvertrag besitzt nicht v27.33d.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "readiness_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if source_contract.get("implementation", {}).get(
    "executionReadinessAcceptanceGuardImplemented"
) is not True:
    fail("Quell-Readiness-Annahme fehlt.")

implementation = contract.get("implementation", {})
if implementation.get("executionPlanImplemented") is not True:
    fail("Ausführungsplan fehlt.")
for key, value in implementation.items():
    if key.endswith("Path") or key == "executionPlanImplemented":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

source = PLAN_MODULE.read_text(encoding="utf-8")
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
    fail(f"Ausführungsplan besitzt unerlaubte Importe: {seen - allowed_imports}")

for marker in (
    "open(", "read_text(", "read_bytes(", "write_text(", "write_bytes(",
    "datetime.now(", "time.time(", "uuid4(", "urandom(",
    "compare_and_set(", "registry.read", "registry.write", "adapter.invoke",
    "subprocess", ".connect(", "postgres://", "postgresql://",
    "database_url", "service_role",
):
    if marker in source.lower():
        fail(f"Ausführungsplan enthält verbotenen Inhalt: {marker}")

descriptor_module = load_module(DESCRIPTOR_MODULE, "descriptor_v2733e")
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE_MODULE,
    "descriptor_acceptance_v2733e",
)
readiness_module = load_module(READINESS_MODULE, "readiness_v2733e")
readiness_acceptance_module = load_module(
    READINESS_ACCEPTANCE_MODULE,
    "readiness_acceptance_v2733e",
)
plan_module = load_module(PLAN_MODULE, "execution_plan_v2733e")

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
    readiness_acceptance_module,
    "accept_atomic_consumption_registry_adapter_execution_readiness",
    None,
)
resolve_plan = getattr(
    plan_module,
    "resolve_atomic_consumption_registry_adapter_execution_plan",
    None,
)
valid_operation_facts = getattr(plan_module, "_VALID_OPERATION_FACTS", None)
plan_steps = getattr(plan_module, "_PLAN_STEPS", None)
locked_flags = getattr(plan_module, "_LOCKED_FLAGS", None)

if not callable(resolve_descriptor) or not callable(accept_descriptor):
    fail("Descriptor-Kette ist nicht nutzbar.")
if not callable(resolve_readiness) or not isinstance(expected_adapter_facts, dict):
    fail("Readiness-Resolver ist nicht nutzbar.")
if not callable(accept_readiness):
    fail("Readiness-Annahme ist nicht nutzbar.")
if not callable(resolve_plan):
    fail("Ausführungsplan-Resolver fehlt.")
if not isinstance(valid_operation_facts, dict):
    fail("Gültige Operationsfakten fehlen.")
if not isinstance(plan_steps, tuple) or not isinstance(locked_flags, tuple):
    fail("Plan- oder Sperrkonstanten fehlen.")

resolved_descriptor = resolve_descriptor({"contractFacts": clone(execution_contract)})
accepted_descriptor = accept_descriptor(resolved_descriptor)
readiness_result = resolve_readiness({
    "acceptedExecutionDescriptorResult": accepted_descriptor,
    "adapterFacts": clone(expected_adapter_facts),
})
accepted_readiness = accept_readiness(readiness_result)

candidate = {
    "acceptedExecutionReadinessResult": accepted_readiness,
    "operationFacts": clone(valid_operation_facts),
}
result = resolve_plan(candidate)
if result.get("status") != (
    "atomic_consumption_registry_adapter_execution_plan_"
    "ready_execution_locked"
):
    fail("Gültiger Ausführungsplan wurde nicht erzeugt.")
if result.get("reason") != (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "plan_ready_execution_locked"
):
    fail("Ausführungsplangrund ist ungültig.")
if result.get("ready") is not True:
    fail("Ausführungsplan-Readiness fehlt.")
plan = result.get("plan")
if not isinstance(plan, dict):
    fail("Ausführungsplan fehlt im Ergebnis.")
if plan.get("planVersion") != 1:
    fail("Ausführungsplanversion ist ungültig.")
if plan.get("operationFacts") != valid_operation_facts:
    fail("Operationsfakten wurden nicht kanonisch übernommen.")
if plan.get("operationFacts") is candidate["operationFacts"]:
    fail("Operationsfakten sind keine Tiefenkopie.")
if [step.get("name") for step in plan.get("steps", [])] != list(plan_steps):
    fail("Ausführungsschritte sind nicht exakt geordnet.")
if [step.get("position") for step in plan.get("steps", [])] != list(
    range(1, len(plan_steps) + 1)
):
    fail("Ausführungsschrittpositionen sind ungültig.")
if any(step.get("executionAllowed") is not False for step in plan["steps"]):
    fail("Ein Ausführungsschritt ist freigegeben.")
for key in locked_flags:
    if result.get(key) is not False:
        fail(f"Ausführungsplan-Ergebnisflag ist offen: {key}")

before = clone(candidate)
again = resolve_plan(candidate)
if again != result:
    fail("Ausführungsplan ist nicht deterministisch.")
if candidate != before:
    fail("Ausführungsplan verändert die Eingabe.")

assert_blocked(resolve_plan([]), "Nicht-Mapping")
missing = clone(candidate)
missing.pop("operationFacts")
assert_blocked(resolve_plan(missing), "fehlendes Feld")
unknown = clone(candidate)
unknown["unknown"] = True
assert_blocked(resolve_plan(unknown), "unbekanntes Feld")
wrong_source = clone(candidate)
wrong_source["acceptedExecutionReadinessResult"]["status"] = "wrong"
assert_blocked(resolve_plan(wrong_source), "falscher Quellstatus")
opened = clone(candidate)
opened["acceptedExecutionReadinessResult"]["registryWritePerformed"] = True
assert_blocked(resolve_plan(opened), "offene Quellgrenze")
wrong_facts = clone(candidate)
wrong_facts["operationFacts"] = []
assert_blocked(resolve_plan(wrong_facts), "falsche Operationsfakten")
whitespace = clone(candidate)
whitespace["operationFacts"]["operationId"] += " "
assert_blocked(resolve_plan(whitespace), "nicht kanonische Zeichenkette")
mismatch_record = clone(candidate)
mismatch_record["operationFacts"]["consumptionRecord"]["requestId"] = "wrong"
assert_blocked(resolve_plan(mismatch_record), "Record-Bindung")
mismatch_evidence = clone(candidate)
mismatch_evidence["operationFacts"]["evidenceTemplate"]["operationId"] = "wrong"
assert_blocked(resolve_plan(mismatch_evidence), "Evidence-Bindung")

source_leaf_count = 0
for path in iter_scalar_paths(
    candidate["acceptedExecutionReadinessResult"]["acceptedReadiness"]
):
    manipulated = clone(candidate)
    set_path(
        manipulated["acceptedExecutionReadinessResult"]["acceptedReadiness"],
        path,
    )
    assert_blocked(resolve_plan(manipulated), "Readiness-Manipulation")
    source_leaf_count += 1

operation_leaf_count = 0
for path in iter_scalar_paths(candidate["operationFacts"]):
    manipulated = clone(candidate)
    set_path(manipulated["operationFacts"], path)
    assert_blocked(resolve_plan(manipulated), "Operations-Manipulation")
    operation_leaf_count += 1

plan_copy = result["plan"]
plan_copy["operationFacts"]["operationId"] = "mutated-copy"
if candidate["operationFacts"]["operationId"] == "mutated-copy":
    fail("Ausführungsplan-Tiefenkopie ist mit der Quelle gekoppelt.")

if FUTURE_ACCEPTANCE.exists():
    fail("v27.33e darf noch keinen Plan-Annahme-Guard umsetzen.")
if FUTURE_EXECUTION.exists():
    fail("v27.33e darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733e*.sql")):
    fail("v27.33e darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Ausführungsplan: OK")
print("Quell-Readiness-Annahme: v27.33d")
print(f"Deterministische Schritte: {len(plan_steps)}")
print(f"Manipulierte Readiness-Blätter blockiert: {source_leaf_count}")
print(f"Manipulierte Operations-Blätter blockiert: {operation_leaf_count}")
print("Kanonische Tiefenkopie: geprüft")
print("Eingabemutation: keine")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33e: keine")
print("Produktive Freigabe: nein")
