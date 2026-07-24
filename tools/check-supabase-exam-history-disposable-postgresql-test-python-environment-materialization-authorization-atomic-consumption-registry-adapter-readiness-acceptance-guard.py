from pathlib import Path
import ast
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-readiness-acceptance-guard-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-readiness-contract.json"
)
DESCRIPTOR = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_descriptor.py"
)
DESCRIPTOR_ACCEPTANCE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_"
    "descriptor_acceptance_guard.py"
)
READINESS = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_readiness.py"
)
GUARD = ROOT / "tools" / (
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


contract = load_json(CONTRACT, "v27.32y-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.32x-Quellvertrag")

if contract.get("version") != "v27.32y":
    fail("Annahmevertrag besitzt nicht v27.32y.")
if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "readiness_acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.32x":
    fail("Quellvertrag besitzt nicht v27.32x.")
if source_contract.get("implementation", {}).get(
    "registryAdapterReadinessImplemented"
) is not True:
    fail("Quell-Readiness ist nicht implementiert.")

implementation = contract.get("implementation", {})
if implementation.get("readinessAcceptanceGuardImplemented") is not True:
    fail("Readiness-Annahme-Guard fehlt.")
for key in (
    "registryAdapterImplemented",
    "registryAdapterInvoked",
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
):
    if implementation.get(key) is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

guard_source = GUARD.read_text(encoding="utf-8")
tree = ast.parse(guard_source)
allowed_imports = {"__future__", "collections"}
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
    "datetime.now(",
    "time.time(",
    "uuid4(",
    "urandom(",
    "compare_and_set(",
    "registry.read",
    "registry.write",
    "adapter.invoke",
    "subprocess",
    ".connect(",
    "postgres://",
    "postgresql://",
    "database_url",
    "service_role",
):
    if marker in guard_source.lower():
        fail(f"Annahme-Guard enthält verbotenen Inhalt: {marker}")

descriptor_module = load_module(DESCRIPTOR, "accaoui_descriptor_v2732y")
descriptor_acceptance_module = load_module(
    DESCRIPTOR_ACCEPTANCE,
    "accaoui_descriptor_acceptance_v2732y",
)
readiness_module = load_module(READINESS, "accaoui_readiness_v2732y")
guard_module = load_module(GUARD, "accaoui_readiness_acceptance_v2732y")

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_atomic_consumption_registry_adapter_descriptor",
    None,
)
expected_descriptor_facts = getattr(descriptor_module, "EXPECTED_FACTS", None)
accept_descriptor = getattr(
    descriptor_acceptance_module,
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
accept_readiness = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_readiness",
    None,
)
security_keys = getattr(guard_module, "SECURITY_KEYS", None)

if not callable(resolve_descriptor) or not isinstance(expected_descriptor_facts, dict):
    fail("Quell-Descriptor ist nicht nutzbar.")
if not callable(accept_descriptor):
    fail("Descriptor-Annahme-Guard ist nicht nutzbar.")
if not callable(resolve_readiness) or not isinstance(expected_adapter_facts, dict):
    fail("Quell-Readiness ist nicht nutzbar.")
if not callable(accept_readiness):
    fail("Readiness-Annahme-Funktion fehlt.")
if not isinstance(security_keys, tuple):
    fail("Sicherheitsfelder fehlen.")

resolved = resolve_descriptor(clone(expected_descriptor_facts))
accepted_descriptor = accept_descriptor(resolved)
readiness_result = resolve_readiness({
    "acceptedDescriptorResult": accepted_descriptor,
    "adapterFacts": clone(expected_adapter_facts),
})

cases = [
    (
        [],
        "blocked",
        "atomic_consumption_registry_adapter_readiness_"
        "acceptance_invalid_input",
    ),
]
missing = clone(readiness_result)
missing.pop("readiness")
cases.append((
    missing,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_structure_invalid",
))
unknown = clone(readiness_result)
unknown["unknown"] = True
cases.append((
    unknown,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_structure_invalid",
))
status = clone(readiness_result)
status["status"] = "ready"
cases.append((
    status,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_source_status_invalid",
))
reason = clone(readiness_result)
reason["reason"] = "wrong"
cases.append((
    reason,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_source_reason_invalid",
))
ready = clone(readiness_result)
ready["ready"] = False
cases.append((
    ready,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_source_ready_invalid",
))
boundary = clone(readiness_result)
boundary["registryWriteAllowed"] = True
cases.append((
    boundary,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_source_boundary_open",
))
version = clone(readiness_result)
version["readiness"]["version"] = 2
cases.append((
    version,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_readiness_version_invalid",
))
source = clone(readiness_result)
source["readiness"]["sourceStatus"] = "wrong"
cases.append((
    source,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_readiness_source_invalid",
))
descriptor = clone(readiness_result)
descriptor["readiness"]["descriptor"]["sourceVersion"] = "v27.32t"
cases.append((
    descriptor,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_readiness_descriptor_invalid",
))
facts = clone(readiness_result)
facts["readiness"]["adapterFacts"][
    "adapterImplementationReportedAvailable"
] = False
cases.append((
    facts,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_readiness_adapter_facts_invalid",
))
execution = clone(readiness_result)
execution["readiness"]["adapterInvocationAllowed"] = True
cases.append((
    execution,
    "blocked",
    "atomic_consumption_registry_adapter_readiness_"
    "acceptance_readiness_boundary_open",
))
cases.append((
    readiness_result,
    "accepted_atomic_consumption_registry_adapter_"
    "readiness_execution_locked",
    "authorization_atomic_consumption_registry_adapter_"
    "readiness_accepted_execution_locked",
))

for candidate, expected_status, expected_reason in cases:
    before = clone(candidate) if isinstance(candidate, dict) else candidate
    first = accept_readiness(candidate)
    second = accept_readiness(candidate)
    if first != second:
        fail("Readiness-Annahme ist nicht deterministisch.")
    if isinstance(candidate, dict) and candidate != before:
        fail("Readiness-Annahme verändert die Eingabe.")
    if (
        first.get("status") != expected_status
        or first.get("reason") != expected_reason
    ):
        fail(f"Readiness-Annahme-Ergebnis ist ungültig: {first}")
    if first.get("executionGrant") is not False:
        fail("Readiness-Annahme-Ausführungsgrant ist offen.")
    for key in security_keys:
        if first.get(key) is not False:
            fail(f"Readiness-Annahme-Sicherheitsgrenze ist offen: {key}")

accepted = accept_readiness(readiness_result)
if accepted.get("accepted") is not True:
    fail("Gültige Readiness wurde nicht angenommen.")
accepted_readiness = accepted.get("acceptedReadiness")
source_readiness = readiness_result.get("readiness")
if not isinstance(accepted_readiness, dict):
    fail("Angenommene Readiness fehlt.")
if accepted_readiness != source_readiness:
    fail("Angenommene Readiness weicht von Quelle ab.")
if accepted_readiness is source_readiness:
    fail("Readiness wurde nicht kopiert.")
for nested in ("descriptor", "adapterFacts"):
    if accepted_readiness[nested] is source_readiness[nested]:
        fail(f"Readinessbereich wurde nicht kopiert: {nested}")

if FUTURE_ADAPTER.exists():
    fail("v27.32y darf noch keinen Registry-Adapter umsetzen.")
if list(MIGRATIONS.glob("*v2732y*.sql")):
    fail("v27.32y darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Readiness-Annahme-Guard: OK")
print("Quellvertrag: v27.32x")
print("Readiness-Status und -Grund: geprüft")
print("Descriptor- und Adapterfaktenbindung: geprüft")
print(
    "Ergebnis: accepted_atomic_consumption_registry_adapter_"
    "readiness_execution_locked"
)
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32y: keine")
print("Produktive Freigabe: nein")
