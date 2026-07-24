from pathlib import Path
import ast
import copy
import importlib.util
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = (
    ROOT / "docs" / "contracts"
    / (
        "exam-history-disposable-postgresql-test-python-environment-"
        "materialization-authorization-atomic-consumption-registry-"
        "adapter-descriptor-contract.json"
    )
)

SOURCE_CONTRACT = (
    ROOT / "docs" / "contracts"
    / (
        "exam-history-disposable-postgresql-test-python-environment-"
        "materialization-authorization-atomic-consumption-registry-"
        "adapter-contract.json"
    )
)

DESCRIPTOR = (
    ROOT / "tools"
    / (
        "accaoui_disposable_test_python_environment_materialization_"
        "authorization_atomic_consumption_registry_adapter_descriptor.py"
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


def load_module(path):
    spec = importlib.util.spec_from_file_location(
        "accaoui_registry_adapter_descriptor_v2732v",
        path,
    )

    if spec is None or spec.loader is None:
        fail("Descriptor ist nicht ladbar.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contract = load_json(CONTRACT, "v27.32v-Vertrag")
source = load_json(SOURCE_CONTRACT, "v27.32u-Quellvertrag")

if contract.get("version") != "v27.32v":
    fail("Vertrag besitzt nicht v27.32v.")

if contract.get("contractVersion") != 1:
    fail("Vertrag besitzt nicht Schema 1.")

if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source.get("version") != "v27.32u":
    fail("Quellvertrag besitzt nicht v27.32u.")

if source.get("status") != (
    "planned_atomic_consumption_registry_adapter_"
    "fully_locked_not_implemented"
):
    fail("Quellvertrag besitzt falschen Status.")

implementation = contract.get("implementation", {})

if implementation.get(
    "registryAdapterDescriptorImplemented"
) is not True:
    fail("Descriptor ist nicht als umgesetzt markiert.")

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
        fail(f"Implementierungsgrenze offen: {key}")

source_code = DESCRIPTOR.read_text(encoding="utf-8")
tree = ast.parse(source_code)

allowed_imports = {"__future__", "collections"}
seen_imports = set()

for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen_imports.add(alias.name.split(".", 1)[0])

    if isinstance(node, ast.ImportFrom) and node.module:
        seen_imports.add(node.module.split(".", 1)[0])

unexpected = seen_imports - allowed_imports

if unexpected:
    fail(f"Unerlaubte Importe: {sorted(unexpected)}")

for marker in (
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "psycopg",
    "postgres://",
    "postgresql://",
    "database_url",
    "service_role",
    ".connect(",
    "open(",
    "read_text(",
    "read_bytes(",
    "write_text(",
    "write_bytes(",
):
    if marker in source_code.lower():
        fail(f"Verbotener Descriptor-Inhalt: {marker}")

module = load_module(DESCRIPTOR)

resolve = getattr(
    module,
    "resolve_atomic_consumption_registry_adapter_descriptor",
    None,
)

expected = getattr(module, "EXPECTED_FACTS", None)

if not callable(resolve):
    fail("Descriptor-Resolver fehlt.")

if not isinstance(expected, dict):
    fail("EXPECTED_FACTS fehlen.")

valid = copy.deepcopy(expected)

cases = [
    (
        [],
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_invalid_input",
    ),
    (
        {key: value for key, value in valid.items() if key != "timeouts"},
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_structure_invalid",
    ),
    (
        {**copy.deepcopy(valid), "unexpected": True},
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_structure_invalid",
    ),
    (
        {**copy.deepcopy(valid), "sourceVersion": "v27.32t"},
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_sourceVersion_invalid",
    ),
    (
        {
            **copy.deepcopy(valid),
            "adapterCapabilities": {
                **copy.deepcopy(valid["adapterCapabilities"]),
                "adapterInvocationAllowed": True,
            },
        },
        "blocked",
        (
            "atomic_consumption_registry_adapter_descriptor_"
            "adapterCapabilities_invalid"
        ),
    ),
    (
        {
            **copy.deepcopy(valid),
            "timeouts": {
                **copy.deepcopy(valid["timeouts"]),
                "operationTimeoutMilliseconds": 16000,
            },
        },
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_timeouts_invalid",
    ),
    (
        {
            **copy.deepcopy(valid),
            "results": {
                **copy.deepcopy(valid["results"]),
                "executionGrant": True,
            },
        },
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_results_invalid",
    ),
    (
        {
            **copy.deepcopy(valid),
            "reconciliation": {
                **copy.deepcopy(valid["reconciliation"]),
                "automaticRetryAfterAmbiguousAllowed": True,
            },
        },
        "blocked",
        (
            "atomic_consumption_registry_adapter_descriptor_"
            "reconciliation_invalid"
        ),
    ),
    (
        {
            **copy.deepcopy(valid),
            "security": {
                **copy.deepcopy(valid["security"]),
                "databaseConnectionAllowed": True,
            },
        },
        "blocked",
        "atomic_consumption_registry_adapter_descriptor_security_invalid",
    ),
    (
        valid,
        (
            "atomic_consumption_registry_adapter_descriptor_"
            "ready_execution_locked"
        ),
        (
            "authorization_atomic_consumption_registry_adapter_"
            "descriptor_ready_execution_locked"
        ),
    ),
]

for facts, expected_status, expected_reason in cases:
    before = copy.deepcopy(facts)

    first = resolve(facts)
    second = resolve(facts)

    if first != second:
        fail("Descriptor ist nicht deterministisch.")

    if facts != before:
        fail("Descriptor verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Falscher Status: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Falscher Grund: {first}")

    for key, value in first.items():
        if key.endswith("Allowed") and value is not False:
            fail(f"Ausführungsgrenze offen: {key}")

result = resolve(valid)
descriptor = result.get("descriptor")

if not isinstance(descriptor, dict):
    fail("Gültiger Descriptor fehlt.")

if descriptor.get("version") != 1:
    fail("Descriptor-Version ist ungültig.")

if descriptor.get("sourceVersion") != "v27.32u":
    fail("Descriptor-Quellversion ist ungültig.")

if descriptor.get("executionGrant") is not False:
    fail("Descriptor besitzt einen Ausführungsgrant.")

adapter = descriptor.get("adapterCapabilities", {})

if adapter.get("kind") != "single_use_consumption_registry":
    fail("Adapterart ist ungültig.")

if adapter.get("requiredCapability") != (
    "atomic_compare_and_set_with_consumption_record"
):
    fail("Adapterfähigkeit ist ungültig.")

timeouts = descriptor.get("timeouts", {})

expected_timeouts = {
    "operationTimeoutMilliseconds": 15000,
    "connectTimeoutMilliseconds": 3000,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
}

for key, value in expected_timeouts.items():
    if timeouts.get(key) != value:
        fail(f"Zeitlimit ist ungültig: {key}")

if FUTURE_ADAPTER.exists():
    fail("v27.32v darf noch keinen Registry-Adapter umsetzen.")

if list(MIGRATIONS.glob("*v2732v*.sql")):
    fail("v27.32v darf keine SQL-Migration erzeugen.")

print("Atomarer Verbrauchs-Registry-Adapter-Descriptor: OK")
print("Quellvertrag: v27.32u")
print("Descriptor: deterministisch und kanonisch")
print("Adapter implementiert: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32v: keine")
print("Produktive Freigabe: nein")
