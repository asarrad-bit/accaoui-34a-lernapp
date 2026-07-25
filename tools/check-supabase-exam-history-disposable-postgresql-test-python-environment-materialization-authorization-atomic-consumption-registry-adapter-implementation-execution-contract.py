from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-execution-contract.json"
)
SOURCE = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-plan-acceptance-guard-contract.json"
)
PLAN_CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-plan-contract.json"
)

FUTURE_ADAPTER = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter.py"
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


contract = load_json(CONTRACT, "v27.33n-Vertrag")
source = load_json(SOURCE, "v27.33m-Quellvertrag")
plan_contract = load_json(PLAN_CONTRACT, "v27.33l-Planvertrag")

if contract.get("version") != "v27.33n":
    fail("Ausführungsvertrag besitzt nicht v27.33n.")
if contract.get("contractVersion") != 1:
    fail("Ausführungsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_atomic_consumption_registry_adapter_implementation_"
    "execution_fully_locked_not_implemented"
):
    fail("Ausführungsvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source.get("version") != "v27.33m":
    fail("Quellvertrag besitzt nicht v27.33m.")
if source.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "implementation_plan_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")
if plan_contract.get("version") != "v27.33l":
    fail("Planvertrag besitzt nicht v27.33l.")

source_boundary = contract.get("sourceBoundary", {})
expected_source = {
    "requiredSourceVersion": "v27.33m",
    "requiredSourceStatus": source["status"],
    "requiredAcceptedStatus": (
        "accepted_atomic_consumption_registry_adapter_"
        "implementation_plan_execution_locked"
    ),
    "requiredAcceptedReason": (
        "authorization_atomic_consumption_registry_adapter_"
        "implementation_plan_accepted_execution_locked"
    ),
    "requiredAccepted": True,
    "requiredPlanVersion": 1,
    "requiredStepCount": 10,
    "requiredExecutionGrant": False,
    "allSourceSecurityFlagsMustBeFalse": True,
    "exactCanonicalAcceptedPlanRequired": True,
}
for key, expected in expected_source.items():
    if source_boundary.get(key) != expected:
        fail(f"Quellgrenze ist ungültig: {key}")

acceptance = source.get("acceptanceBoundary", {})
if acceptance.get("successStatus") != expected_source[
    "requiredAcceptedStatus"
]:
    fail("Quell-Annahmestatus ist nicht gebunden.")
if acceptance.get("successReason") != expected_source[
    "requiredAcceptedReason"
]:
    fail("Quell-Annahmegrund ist nicht gebunden.")
if acceptance.get("executionGrant") is not False:
    fail("Quell-Annahme öffnet den Grant.")

interface = contract.get("executionInterfaceBoundary", {})
required_interface = {
    "adapterKind": "single_use_consumption_registry",
    "protocolName": "AtomicConsumptionRegistryAdapter",
    "factoryName": "build_atomic_consumption_registry_adapter",
    "operationName": (
        "consume_materialization_authorization_atomically"
    ),
    "requiredCapability": (
        "atomic_compare_and_set_with_consumption_record"
    ),
    "expectedState": "unused",
    "desiredState": "consumed",
    "singleAdapterInvocationRequired": True,
    "maximumParallelWinners": 1,
    "operationTimeoutMilliseconds": 15000,
    "connectTimeoutMilliseconds": 3000,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
    "dependencyInjectionRequired": True,
    "hardCodedCredentialsAllowed": False,
    "environmentVariableReadAllowed": False,
    "driverImportAllowed": False,
    "databaseConnectionAllowed": False,
    "rawErrorSuppressed": True,
    "automaticRetryAfterAmbiguousAllowed": False,
    "reconciliationRequired": True,
    "reconciliationMayReadByOperationIdLater": True,
    "reconciliationMayWriteAllowed": False,
    "executionGrant": False,
}
for key, expected in required_interface.items():
    if interface.get(key) != expected:
        fail(f"Ausführungsschnittstelle ist ungültig: {key}")

if len(interface.get("exactInputFields", [])) != 10:
    fail("Ausführungsschnittstelle besitzt nicht zehn Eingabefelder.")
if len(interface.get("exactResultKinds", [])) != 9:
    fail("Ausführungsschnittstelle besitzt nicht neun Ergebnisarten.")

atomicity = contract.get("atomicityBoundary", {})
for key in (
    "singleTransactionRequired",
    "compareAndSetAndConsumptionRecordSingleTransactionRequired",
    "consumptionRecordRequiredOnCommitted",
    "evidenceDerivedOnlyFromConfirmedRecord",
    "alreadyConsumedIsTerminal",
    "bindingConflictIsTerminal",
    "expiredIsTerminal",
    "commitAmbiguousTerminalForAutomaticRetry",
):
    if atomicity.get(key) is not True:
        fail(f"Atomaritätsgrenze fehlt: {key}")

if atomicity.get("maximumParallelWinners") != 1:
    fail("Parallelgewinnergrenze ist ungültig.")
for key in (
    "resetConsumedToUnusedAllowed",
    "assumeCommittedAllowed",
    "assumeUnusedAllowed",
):
    if atomicity.get(key) is not False:
        fail(f"Atomaritätsgrenze ist offen: {key}")

implementation = contract.get("implementationBoundary", {})
if implementation.get("implementationExecutionContractPrepared") is not True:
    fail("Ausführungsvertrag ist nicht als vorbereitet markiert.")
for key, value in implementation.items():
    if key == "implementationExecutionContractPrepared":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

for block in ("securityBoundary", "futureBoundary"):
    values = contract.get(block, {})
    if not isinstance(values, dict) or not values:
        fail(f"{block} fehlt.")
    for key, value in values.items():
        if value is not False:
            fail(f"{block} ist offen: {key}")

if FUTURE_ADAPTER.exists():
    fail("v27.33n darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33n darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733n*.sql")):
    fail("v27.33n darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungsausführungsvertrag: OK")
print("Quell-Plan-Annahme-Guard: v27.33m")
print("Schnittstelle und Ergebnisarten: geprüft")
print("Zeitlimits und Dependency Injection: geprüft")
print("Atomarität und Reconciliation: geprüft")
print("Adaptermodul erstellt: nein")
print("Adapter importiert: nein")
print("Adapter instanziiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33n: keine")
print("Produktive Freigabe: nein")
