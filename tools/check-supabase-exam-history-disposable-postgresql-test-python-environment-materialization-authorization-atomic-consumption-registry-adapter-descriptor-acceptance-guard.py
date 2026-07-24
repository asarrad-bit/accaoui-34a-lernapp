from pathlib import Path
import ast
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = (
    ROOT / "docs" / "contracts"
    / (
        "exam-history-disposable-postgresql-test-python-environment-"
        "materialization-authorization-atomic-consumption-registry-"
        "adapter-descriptor-acceptance-guard-contract.json"
    )
)
SOURCE_CONTRACT = (
    ROOT / "docs" / "contracts"
    / (
        "exam-history-disposable-postgresql-test-python-environment-"
        "materialization-authorization-atomic-consumption-registry-"
        "adapter-descriptor-contract.json"
    )
)
SOURCE_DESCRIPTOR = (
    ROOT / "tools"
    / (
        "accaoui_disposable_test_python_environment_materialization_"
        "authorization_atomic_consumption_registry_adapter_descriptor.py"
    )
)
GUARD = (
    ROOT / "tools"
    / (
        "accaoui_disposable_test_python_environment_materialization_"
        "authorization_atomic_consumption_registry_adapter_"
        "descriptor_acceptance_guard.py"
    )
)
FUTURE_READINESS = (
    ROOT / "tools"
    / (
        "accaoui_disposable_test_python_environment_materialization_"
        "authorization_atomic_consumption_registry_adapter_readiness.py"
    )
)
FUTURE_ADAPTER = (
    ROOT / "tools"
    / (
        "accaoui_disposable_test_python_environment_materialization_"
        "authorization_atomic_consumption_registry_adapter.py"
    )
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


contract = load_json(CONTRACT, "v27.32w-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.32v-Quellvertrag")

if contract.get("version") != "v27.32w":
    fail("Annahmevertrag besitzt nicht v27.32w.")

if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")

if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_"
    "adapter_descriptor_acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")

if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source_contract.get("version") != "v27.32v":
    fail("Quellvertrag besitzt nicht v27.32v.")

if source_contract.get("implementation", {}).get(
    "registryAdapterDescriptorImplemented"
) is not True:
    fail("Quell-Descriptor ist nicht implementiert.")

if source_contract.get("resultBoundary", {}).get(
    "successStatus"
) != (
    "atomic_consumption_registry_adapter_descriptor_"
    "ready_execution_locked"
):
    fail("Quell-Descriptor besitzt falschen Erfolgsstatus.")

implementation = contract.get("implementation", {})

if implementation.get(
    "descriptorAcceptanceGuardImplemented"
) is not True:
    fail("Descriptor-Annahme-Guard fehlt.")

for key in (
    "registryAdapterReadinessImplemented",
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

allowed_imports = {
    "__future__",
    "collections",
}
seen_imports = set()

for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen_imports.add(alias.name.split(".", 1)[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        seen_imports.add(node.module.split(".", 1)[0])

unexpected = seen_imports - allowed_imports

if unexpected:
    fail(f"Annahme-Guard besitzt unerlaubte Importe: {unexpected}")

forbidden_names = {
    "Path",
    "os",
    "sys",
    "subprocess",
    "shutil",
    "socket",
    "requests",
    "urllib",
    "uuid",
    "secrets",
    "time",
    "datetime",
}

for node in ast.walk(tree):
    if isinstance(node, ast.Name) and node.id in forbidden_names:
        fail(f"Annahme-Guard verwendet verbotenen Namen: {node.id}")

lower_source = guard_source.lower()

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
    if marker in lower_source:
        fail(f"Annahme-Guard enthält verbotenen Inhalt: {marker}")

source_module = load_module(
    SOURCE_DESCRIPTOR,
    "accaoui_registry_descriptor_source_v2732w",
)
guard_module = load_module(
    GUARD,
    "accaoui_registry_descriptor_acceptance_v2732w",
)

resolve = getattr(
    source_module,
    "resolve_atomic_consumption_registry_adapter_descriptor",
    None,
)
expected_facts = getattr(source_module, "EXPECTED_FACTS", None)
accept = getattr(
    guard_module,
    "accept_atomic_consumption_registry_adapter_descriptor",
    None,
)
security_keys = getattr(guard_module, "SECURITY_KEYS", None)

if not callable(resolve):
    fail("Quell-Descriptor-Resolver fehlt.")

if not isinstance(expected_facts, dict):
    fail("Quell-Descriptor-Fakten fehlen.")

if not callable(accept):
    fail("Descriptor-Annahme-Funktion fehlt.")

if not isinstance(security_keys, tuple):
    fail("Sicherheitsfelder fehlen.")

source_result = resolve(clone(expected_facts))

if source_result.get("status") != (
    "atomic_consumption_registry_adapter_descriptor_"
    "ready_execution_locked"
):
    fail("Quell-Descriptor konnte nicht erzeugt werden.")

tampered_status = clone(source_result)
tampered_status["status"] = "ready"

tampered_reason = clone(source_result)
tampered_reason["reason"] = "wrong"

tampered_boundary = clone(source_result)
tampered_boundary["registryWriteAllowed"] = True

tampered_descriptor_version = clone(source_result)
tampered_descriptor_version["descriptor"]["version"] = 2

tampered_source = clone(source_result)
tampered_source["descriptor"]["sourceVersion"] = "v27.32t"

tampered_adapter = clone(source_result)
tampered_adapter["descriptor"]["adapterCapabilities"][
    "adapterInvocationAllowed"
] = True

tampered_timeout = clone(source_result)
tampered_timeout["descriptor"]["timeouts"][
    "operationTimeoutMilliseconds"
] = 16000

tampered_results = clone(source_result)
tampered_results["descriptor"]["results"][
    "exactResultKinds"
].append("unknown")

tampered_reconciliation = clone(source_result)
tampered_reconciliation["descriptor"]["reconciliation"][
    "automaticRetryAfterAmbiguousAllowed"
] = True

tampered_security = clone(source_result)
tampered_security["descriptor"]["security"][
    "databaseConnectionAllowed"
] = True

tampered_execution = clone(source_result)
tampered_execution["descriptor"]["executionGrant"] = True

missing_descriptor = clone(source_result)
missing_descriptor.pop("descriptor")

unknown_field = clone(source_result)
unknown_field["unknown"] = True

cases = [
    (
        [],
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_invalid_input",
    ),
    (
        missing_descriptor,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_structure_invalid",
    ),
    (
        unknown_field,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_structure_invalid",
    ),
    (
        tampered_status,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_source_status_invalid",
    ),
    (
        tampered_reason,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_source_reason_invalid",
    ),
    (
        tampered_boundary,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_source_boundary_open",
    ),
    (
        tampered_descriptor_version,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_descriptor_version_invalid",
    ),
    (
        tampered_source,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_descriptor_source_invalid",
    ),
    (
        tampered_adapter,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_descriptor_adapter_invalid",
    ),
    (
        tampered_timeout,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_descriptor_timeouts_invalid",
    ),
    (
        tampered_results,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_descriptor_results_invalid",
    ),
    (
        tampered_reconciliation,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_descriptor_reconciliation_invalid",
    ),
    (
        tampered_security,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_descriptor_security_invalid",
    ),
    (
        tampered_execution,
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_"
        "acceptance_descriptor_execution_invalid",
    ),
    (
        source_result,
        (
            "accepted_atomic_consumption_registry_adapter_"
            "descriptor_execution_locked"
        ),
        (
            "authorization_atomic_consumption_registry_adapter_"
            "descriptor_accepted_execution_locked"
        ),
    ),
]

for candidate, expected_status, expected_reason in cases:
    before = clone(candidate) if isinstance(candidate, dict) else candidate
    first = accept(candidate)
    second = accept(candidate)

    if first != second:
        fail("Descriptor-Annahme ist nicht deterministisch.")

    if isinstance(candidate, dict) and candidate != before:
        fail("Descriptor-Annahme verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Annahmestatus ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Annahmegrund ist ungültig: {first}")

    if first.get("executionGrant") is not False:
        fail("Annahme-Ausführungsgrant ist offen.")

    for key in security_keys:
        if first.get(key) is not False:
            fail(f"Annahme-Sicherheitsgrenze ist offen: {key}")

accepted = accept(source_result)

if accepted.get("accepted") is not True:
    fail("Gültiger Descriptor wurde nicht angenommen.")

accepted_descriptor = accepted.get("acceptedDescriptor")
source_descriptor = source_result.get("descriptor")

if not isinstance(accepted_descriptor, dict):
    fail("Angenommener Descriptor fehlt.")

if accepted_descriptor != source_descriptor:
    fail("Angenommener Descriptor weicht von Quelle ab.")

if accepted_descriptor is source_descriptor:
    fail("Annahme darf keine Quellreferenz zurückgeben.")

for nested in (
    "adapterCapabilities",
    "timeouts",
    "results",
    "reconciliation",
    "security",
):
    if accepted_descriptor[nested] is source_descriptor[nested]:
        fail(f"Descriptorbereich wurde nicht kopiert: {nested}")

if FUTURE_READINESS.exists():
    fail("v27.32w darf noch keine Adapter-Readiness umsetzen.")

if FUTURE_ADAPTER.exists():
    fail("v27.32w darf noch keinen Registry-Adapter umsetzen.")

if list(MIGRATIONS.glob("*v2732w*.sql")):
    fail("v27.32w darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Descriptor-Annahme-Guard: OK")
print("Quellvertrag: v27.32v")
print("Quellstatus und -grund: geprüft")
print("Descriptorstruktur und Bindungen: geprüft")
print("Adapter-, Zeitlimit- und Ergebnisgrenzen: geprüft")
print("Reconciliation und Sicherheitsgrenzen: geprüft")
print("Ergebnis: accepted_atomic_consumption_registry_adapter_descriptor_execution_locked")
print("Adapter-Readiness umgesetzt: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32w: keine")
print("Produktive Freigabe: nein")
