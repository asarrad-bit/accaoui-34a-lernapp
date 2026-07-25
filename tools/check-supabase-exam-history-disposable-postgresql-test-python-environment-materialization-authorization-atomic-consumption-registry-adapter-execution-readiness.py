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
    "adapter-execution-readiness-contract.json"
)
SOURCE_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-descriptor-acceptance-guard-contract.json"
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
ACCEPTANCE_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "descriptor_acceptance_guard.py"
)
READINESS_MODULE = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness.py"
)
FUTURE_GUARD = ROOT / "tools" / (
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

LOCKED_FLAGS = ['adapterImplemented', 'adapterInvoked', 'registryReadPerformed', 'registryWritePerformed', 'atomicCompareAndSetPerformed', 'authorizationConsumed', 'authorizationGranted', 'authorizationTokenGenerated', 'trustedClockRead', 'filesystemReadPerformed', 'filesystemMutationPerformed', 'processExecuted', 'networkExecuted', 'driverImported', 'databaseConnectionCreated', 'databaseTestExecuted', 'sqlMigrationCreated', 'frontendIntegration', 'executionGrant']
EXPECTED_ADAPTER_FACTS = json.loads('{"adapterImplementationReportedAvailable":true,"adapterInvocationAllowed":false,"adapterKind":"single_use_consumption_registry","ambiguousCommitReconciliationReportedAvailable":true,"atomicCompareAndSetAllowed":false,"atomicCompareAndSetWithRecordReportedAvailable":true,"authorizationConsumptionAllowed":false,"automaticRetryAfterAmbiguousAllowed":false,"connectTimeoutMilliseconds":3000,"consumedResetReportedAllowed":false,"consumptionRecordInSameTransactionReportedSupported":true,"evidenceFromConfirmedRecordReportedSupported":true,"exactInputFieldsReportedSupported":["operationId","requestId","authorizationNonce","planFingerprint","actorId","purpose","expectedState","desiredState","consumptionRecord","evidenceTemplate"],"exactResultKindsReportedSupported":["committed","already_consumed","parallel_conflict","binding_conflict","expired","adapter_unavailable","atomicity_unavailable","commit_ambiguous","operation_failed"],"executionGrant":false,"lockTimeoutMilliseconds":2000,"maximumParallelWinnersReported":1,"operationName":"consume_materialization_authorization_atomically","operationTimeoutMilliseconds":15000,"rawErrorSuppressed":true,"reconciliationReadByOperationIdReportedAvailable":true,"registryReadAllowed":false,"registryWriteAllowed":false,"requiredCapabilityReportedAvailable":true,"singleAdapterInvocationReportedSupported":true,"statementTimeoutMilliseconds":5000}')
SUCCESS_STATUS = (
    "atomic_consumption_registry_adapter_execution_readiness_"
    "ready_execution_locked"
)
SUCCESS_REASON = (
    "authorization_atomic_consumption_registry_adapter_execution_"
    "readiness_ready_execution_locked"
)
BLOCKED_STATUS = (
    "atomic_consumption_registry_adapter_execution_readiness_"
    "blocked_execution_locked"
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
        fail(f"Modul kann nicht geladen werden: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clone(value):
    return copy.deepcopy(value)


def assert_blocked(result, label):
    if result.get("status") != BLOCKED_STATUS:
        fail(f"Manipulation nicht blockiert: {label}")
    if result.get("ready") is not False:
        fail(f"Manipulation meldet Readiness: {label}")
    if result.get("readiness") is not None:
        fail(f"Manipulation enthält Readiness: {label}")
    for key in LOCKED_FLAGS:
        if result.get(key) is not False:
            fail(f"Blockiertes Ergebnis öffnet Grenze {key}: {label}")


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
    target = value
    for key in path[:-1]:
        target = target[key]
    leaf = path[-1]
    old = target[leaf]
    if isinstance(old, bool):
        target[leaf] = not old
    elif isinstance(old, int):
        target[leaf] = old + 1
    elif isinstance(old, str):
        target[leaf] = old + "_mutated"
    elif old is None:
        target[leaf] = "mutated"
    else:
        target[leaf] = None


contract = load_json(CONTRACT, "v27.33c-Vertrag")
source_contract = load_json(SOURCE_CONTRACT, "v27.33b-Quellvertrag")
execution_contract = load_json(EXECUTION_CONTRACT, "v27.32z-Ausführungsvertrag")

if contract.get("version") != "v27.33c":
    fail("Readiness-Vertrag besitzt nicht v27.33c.")
if contract.get("contractVersion") != 1:
    fail("Readiness-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "readiness_execution_locked"
):
    fail("Readiness-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")
if source_contract.get("version") != "v27.33b":
    fail("Quellvertrag besitzt nicht v27.33b.")
if source_contract.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "descriptor_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if execution_contract.get("version") != "v27.32z":
    fail("Ausführungsvertrag besitzt nicht v27.32z.")

boundary = contract.get("readinessBoundary", {})
required = {
    "readinessVersion": 1,
    "successStatus": SUCCESS_STATUS,
    "successReason": SUCCESS_REASON,
    "blockedStatus": BLOCKED_STATUS,
    "ready": True,
    "sourceDescriptorVersion": 1,
    "sourceContractVersion": "v27.32z",
    "sourceContractStatus": (
        "planned_atomic_consumption_registry_adapter_execution_"
        "fully_locked_not_implemented"
    ),
    "adapterKind": "single_use_consumption_registry",
    "operationName": "consume_materialization_authorization_atomically",
    "requiredCapability": "atomic_compare_and_set_with_consumption_record",
    "expectedState": "unused",
    "desiredState": "consumed",
    "singleAdapterInvocationRequired": True,
    "maximumParallelWinners": 1,
    "operationTimeoutMilliseconds": 15000,
    "connectTimeoutMilliseconds": 3000,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
    "exactInputFields": ['operationId', 'requestId', 'authorizationNonce', 'planFingerprint', 'actorId', 'purpose', 'expectedState', 'desiredState', 'consumptionRecord', 'evidenceTemplate'],
    "exactResultKinds": ['committed', 'already_consumed', 'parallel_conflict', 'binding_conflict', 'expired', 'adapter_unavailable', 'atomicity_unavailable', 'commit_ambiguous', 'operation_failed'],
    "consumptionRecordInSameTransactionRequired": True,
    "evidenceFromConfirmedRecordRequired": True,
    "consumedResetAllowed": False,
    "reconciliationRequired": True,
    "automaticRetryAfterAmbiguousAllowed": False,
    "rawErrorSuppressed": True,
    "executionGrant": False,
}
for key, expected in required.items():
    if boundary.get(key) != expected:
        fail(f"Readiness-Grenze ist ungültig: {key}")
for key, value in contract.get("securityBoundary", {}).items():
    if value is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")
for key, value in contract.get("futureBoundary", {}).items():
    if value is not False:
        fail(f"Zukunftsgrenze ist offen: {key}")

source = READINESS_MODULE.read_text(encoding="utf-8")
tree = ast.parse(source)
allowed_imports = {"__future__", "copy", "json", "collections"}
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
    if marker in source.lower():
        fail(f"Readiness enthält verbotenen Zugriff: {marker}")

descriptor_module = load_module(DESCRIPTOR_MODULE, "v2733a_descriptor")
acceptance_module = load_module(ACCEPTANCE_MODULE, "v2733b_acceptance")
readiness_module = load_module(READINESS_MODULE, "v2733c_readiness")

descriptor = descriptor_module.resolve_atomic_consumption_registry_adapter_execution_descriptor(
    {"contractFacts": clone(execution_contract)}
)
accepted = acceptance_module.accept_atomic_consumption_registry_adapter_execution_descriptor(
    descriptor
)
if accepted.get("status") != (
    "accepted_atomic_consumption_registry_adapter_execution_"
    "descriptor_execution_locked"
):
    fail("Quell-Annahme liefert keinen Erfolgsstatus.")

candidate = {
    "acceptedExecutionDescriptorResult": accepted,
    "adapterFacts": clone(EXPECTED_ADAPTER_FACTS),
}
before = clone(candidate)
original_open = builtins.open


def forbidden_open(*args, **kwargs):
    raise AssertionError("Readiness darf keine Datei öffnen.")


builtins.open = forbidden_open
try:
    first = readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(
        candidate
    )
    second = readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(
        candidate
    )
finally:
    builtins.open = original_open

if candidate != before:
    fail("Readiness hat die Eingabe verändert.")
if first != second:
    fail("Readiness ist nicht deterministisch.")
if first.get("status") != SUCCESS_STATUS:
    fail("Readiness-Status ist ungültig.")
if first.get("reason") != SUCCESS_REASON:
    fail("Readiness-Grund ist ungültig.")
if first.get("ready") is not True:
    fail("Gültige Eingabe wurde nicht als bereit erkannt.")
if first.get("executionGrant") is not False:
    fail("Readiness öffnet den Grant.")
for key in LOCKED_FLAGS:
    if first.get(key) is not False:
        fail(f"Readiness-Ergebnis öffnet Grenze: {key}")

readiness = first.get("readiness")
if not isinstance(readiness, dict):
    fail("Readiness-Nutzlast fehlt.")
if readiness.get("readinessVersion") != 1:
    fail("Readiness-Version ist ungültig.")
if readiness.get("descriptor") != accepted.get("acceptedDescriptor"):
    fail("Descriptor wurde nicht kanonisch kopiert.")
if readiness.get("descriptor") is accepted.get("acceptedDescriptor"):
    fail("Descriptor wurde nicht tief kopiert.")
if readiness.get("adapterFacts") != EXPECTED_ADAPTER_FACTS:
    fail("Adapterfakten wurden nicht kanonisch kopiert.")
if readiness.get("adapterFacts") is candidate["adapterFacts"]:
    fail("Adapterfakten wurden nicht tief kopiert.")
if readiness.get("executionGrant") is not False:
    fail("Readiness-Nutzlast öffnet den Grant.")

candidate["acceptedExecutionDescriptorResult"]["acceptedDescriptor"][
    "sourceContractVersion"
] = "mutated_after_result"
candidate["adapterFacts"]["adapterKind"] = "mutated_after_result"
if readiness["descriptor"]["sourceContractVersion"] != "v27.32z":
    fail("Descriptor-Kopie ist nicht von Eingabemutation getrennt.")
if readiness["adapterFacts"]["adapterKind"] != "single_use_consumption_registry":
    fail("Adapterfakten-Kopie ist nicht von Eingabemutation getrennt.")

assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(None),
    "nicht Mapping",
)
missing = clone(before)
missing.pop("adapterFacts")
assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(missing),
    "fehlendes Feld",
)
unknown = clone(before)
unknown["unknown"] = True
assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(unknown),
    "unbekanntes Feld",
)
status = clone(before)
status["acceptedExecutionDescriptorResult"]["status"] = "wrong"
assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(status),
    "falscher Status",
)
reason = clone(before)
reason["acceptedExecutionDescriptorResult"]["reason"] = "wrong"
assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(reason),
    "falscher Grund",
)
accepted_flag = clone(before)
accepted_flag["acceptedExecutionDescriptorResult"]["accepted"] = False
assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(accepted_flag),
    "accepted false",
)
opened = clone(before)
opened["acceptedExecutionDescriptorResult"]["registryWritePerformed"] = True
assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(opened),
    "offene Quellgrenze",
)
wrong_descriptor = clone(before)
wrong_descriptor["acceptedExecutionDescriptorResult"]["acceptedDescriptor"] = []
assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(wrong_descriptor),
    "falscher Descriptor",
)
wrong_facts = clone(before)
wrong_facts["adapterFacts"] = []
assert_blocked(
    readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(wrong_facts),
    "falsche Adapterfakten",
)

contract_leaf_count = 0
for path in iter_scalar_paths(execution_contract):
    manipulated = clone(before)
    set_path(
        manipulated["acceptedExecutionDescriptorResult"]
        ["acceptedDescriptor"]["contractFacts"],
        path,
    )
    assert_blocked(
        readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(
            manipulated
        ),
        "manipulierte Vertragsfakten " + ".".join(map(str, path)),
    )
    contract_leaf_count += 1

adapter_leaf_count = 0
for path in iter_scalar_paths(EXPECTED_ADAPTER_FACTS):
    manipulated = clone(before)
    set_path(manipulated["adapterFacts"], path)
    assert_blocked(
        readiness_module.resolve_atomic_consumption_registry_adapter_execution_readiness(
            manipulated
        ),
        "manipulierte Adapterfakten " + ".".join(map(str, path)),
    )
    adapter_leaf_count += 1

if FUTURE_EXECUTION.exists():
    fail("v27.33c darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733c*.sql")):
    fail("v27.33c darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Ausführungs-Readiness: OK")
print("Quell-Annahme-Guard: v27.33b")
print("Descriptorbindung: v27.32z")
print(f"Manipulierte Vertragsblätter blockiert: {contract_leaf_count}")
print(f"Manipulierte Adapterfakten blockiert: {adapter_leaf_count}")
print("Kanonische Tiefenkopien: geprüft")
print("Eingabemutation: keine")
print("Dateizugriff der Readiness: keiner")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33c: keine")
print("Produktive Freigabe: nein")
