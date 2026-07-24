from pathlib import Path
import ast
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-readiness-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-descriptor-acceptance-guard-contract.json"
)
DESCRIPTOR = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_descriptor.py"
)
ACCEPTANCE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "descriptor_acceptance_guard.py"
)
READINESS = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_readiness.py"
)
FUTURE_GUARD = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "readiness_acceptance_guard.py"
)
FUTURE_ADAPTER = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
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
    return json.loads(json.dumps(value))


contract = load_json(CONTRACT, "v27.32x-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.32w-Quellvertrag")

if contract.get("version") != "v27.32x":
    fail("Readiness-Vertrag besitzt nicht v27.32x.")
if contract.get("contractVersion") != 1:
    fail("Readiness-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "readiness_execution_locked"
):
    fail("Readiness-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.32w":
    fail("Quellvertrag besitzt nicht v27.32w.")
if source_contract.get("implementation", {}).get(
    "descriptorAcceptanceGuardImplemented"
) is not True:
    fail("Quell-Annahme-Guard ist nicht implementiert.")

implementation = contract.get("implementation", {})
if implementation.get("registryAdapterReadinessImplemented") is not True:
    fail("Registry-Adapter-Readiness fehlt.")
for key in (
    "registryAdapterImplemented", "registryAdapterInvoked",
    "registryReadPerformed", "registryWritePerformed",
    "atomicCompareAndSetPerformed", "authorizationConsumed",
    "authorizationGranted", "authorizationTokenGenerated",
    "trustedClockRead", "filesystemReadPerformed",
    "filesystemMutationPerformed", "processExecuted", "networkExecuted",
    "driverImported", "databaseConnectionCreated", "databaseTestExecuted",
    "sqlMigrationCreated", "frontendIntegration",
):
    if implementation.get(key) is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

source_text = READINESS.read_text(encoding="utf-8")
tree = ast.parse(source_text)
allowed_imports = {"__future__", "collections"}
seen = set()
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen.add(alias.name.split(".", 1)[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        seen.add(node.module.split(".", 1)[0])
if seen - allowed_imports:
    fail(f"Readiness besitzt unerlaubte Importe: {seen - allowed_imports}")

for marker in (
    "open(", "read_text(", "read_bytes(", "write_text(", "write_bytes(",
    "datetime.now(", "time.time(", "uuid4(", "urandom(",
    "compare_and_set(", "registry.read", "registry.write",
    "adapter.invoke", "subprocess", ".connect(", "postgres://",
    "postgresql://", "database_url", "service_role",
):
    if marker in source_text.lower():
        fail(f"Readiness enthält verbotenen Inhalt: {marker}")

source_module = load_module(DESCRIPTOR, "accaoui_descriptor_v2732x")
acceptance_module = load_module(ACCEPTANCE, "accaoui_acceptance_v2732x")
readiness_module = load_module(READINESS, "accaoui_readiness_v2732x")

resolve_descriptor = getattr(
    source_module,
    "resolve_atomic_consumption_registry_adapter_descriptor",
    None,
)
expected_descriptor_facts = getattr(source_module, "EXPECTED_FACTS", None)
accept_descriptor = getattr(
    acceptance_module,
    "accept_atomic_consumption_registry_adapter_descriptor",
    None,
)
resolve_readiness = getattr(
    readiness_module,
    "resolve_atomic_consumption_registry_adapter_readiness",
    None,
)
expected_adapter_facts = getattr(
    readiness_module,
    "EXPECTED_ADAPTER_FACTS",
    None,
)
security_keys = getattr(readiness_module, "SECURITY_KEYS", None)

if not callable(resolve_descriptor) or not isinstance(expected_descriptor_facts, dict):
    fail("Quell-Descriptor ist nicht nutzbar.")
if not callable(accept_descriptor):
    fail("Quell-Annahme-Guard ist nicht nutzbar.")
if not callable(resolve_readiness):
    fail("Readiness-Resolver fehlt.")
if not isinstance(expected_adapter_facts, dict):
    fail("Adapterfakten fehlen.")
if not isinstance(security_keys, tuple):
    fail("Sicherheitsfelder fehlen.")

resolved = resolve_descriptor(clone(expected_descriptor_facts))
accepted = accept_descriptor(resolved)
source_input = {
    "acceptedDescriptorResult": accepted,
    "adapterFacts": clone(expected_adapter_facts),
}

cases = []
cases.append(([], "blocked", "atomic_consumption_registry_adapter_readiness_invalid_input"))
missing = clone(source_input); missing.pop("adapterFacts")
cases.append((missing, "blocked", "atomic_consumption_registry_adapter_readiness_structure_invalid"))
unknown = clone(source_input); unknown["unknown"] = True
cases.append((unknown, "blocked", "atomic_consumption_registry_adapter_readiness_structure_invalid"))
status = clone(source_input); status["acceptedDescriptorResult"]["status"] = "ready"
cases.append((status, "blocked", "atomic_consumption_registry_adapter_readiness_accepted_descriptor_status_invalid"))
reason = clone(source_input); reason["acceptedDescriptorResult"]["reason"] = "wrong"
cases.append((reason, "blocked", "atomic_consumption_registry_adapter_readiness_accepted_descriptor_reason_invalid"))
boundary = clone(source_input); boundary["acceptedDescriptorResult"]["registryWriteAllowed"] = True
cases.append((boundary, "blocked", "atomic_consumption_registry_adapter_readiness_accepted_descriptor_boundary_open"))
descriptor = clone(source_input); descriptor["acceptedDescriptorResult"]["acceptedDescriptor"]["version"] = 2
cases.append((descriptor, "blocked", "atomic_consumption_registry_adapter_readiness_descriptor_version_invalid"))
facts = clone(source_input); facts["adapterFacts"]["adapterImplementationReportedAvailable"] = False
cases.append((facts, "blocked", "atomic_consumption_registry_adapter_readiness_adapter_facts_invalid"))
cases.append((source_input, "atomic_consumption_registry_adapter_readiness_ready_execution_locked", "authorization_atomic_consumption_registry_adapter_readiness_ready_execution_locked"))

for candidate, expected_status, expected_reason in cases:
    before = clone(candidate) if isinstance(candidate, dict) else candidate
    first = resolve_readiness(candidate)
    second = resolve_readiness(candidate)
    if first != second:
        fail("Readiness ist nicht deterministisch.")
    if isinstance(candidate, dict) and candidate != before:
        fail("Readiness verändert die Eingabe.")
    if first.get("status") != expected_status or first.get("reason") != expected_reason:
        fail(f"Readiness-Ergebnis ist ungültig: {first}")
    if first.get("executionGrant") is not False:
        fail("Readiness-Ausführungsgrant ist offen.")
    for key in security_keys:
        if first.get(key) is not False:
            fail(f"Readiness-Sicherheitsgrenze ist offen: {key}")

result = resolve_readiness(source_input)
if result.get("ready") is not True:
    fail("Gültige Adapterfakten wurden nicht als ready bewertet.")
readiness = result.get("readiness")
if not isinstance(readiness, dict):
    fail("Readiness-State fehlt.")
if readiness.get("version") != 1:
    fail("Readiness-Version ist ungültig.")
if readiness.get("adapterFacts") != expected_adapter_facts:
    fail("Readiness-Adapterfakten weichen ab.")
if readiness["adapterFacts"] is source_input["adapterFacts"]:
    fail("Adapterfakten wurden nicht kopiert.")
if readiness["descriptor"] is accepted["acceptedDescriptor"]:
    fail("Descriptor wurde nicht kopiert.")

if FUTURE_GUARD.exists():
    fail("v27.32x darf noch keinen Readiness-Annahme-Guard umsetzen.")
if FUTURE_ADAPTER.exists():
    fail("v27.32x darf noch keinen Registry-Adapter umsetzen.")
if list(MIGRATIONS.glob("*v2732x*.sql")):
    fail("v27.32x darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Readiness-State: OK")
print("Quellvertrag: v27.32w")
print("Angenommener Descriptor: geprüft")
print("Adapterfähigkeits- und Verfügbarkeitsfakten: geprüft")
print("Ergebnis: atomic_consumption_registry_adapter_readiness_ready_execution_locked")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32x: keine")
print("Produktive Freigabe: nein")
