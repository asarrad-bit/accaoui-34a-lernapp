from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-implementation-contract.json"
)
SOURCE = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-plan-acceptance-guard-contract.json"
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


contract = load_json(CONTRACT, "v27.33g-Vertrag")
source = load_json(SOURCE, "v27.33f-Quellvertrag")

if contract.get("version") != "v27.33g":
    fail("Implementierungsvertrag besitzt nicht v27.33g.")
if contract.get("contractVersion") != 1:
    fail("Implementierungsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_atomic_consumption_registry_adapter_implementation_"
    "fully_locked_not_implemented"
):
    fail("Implementierungsvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")

if source.get("version") != "v27.33f":
    fail("Quellvertrag besitzt nicht v27.33f.")
if source.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_execution_"
    "plan_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")

source_boundary = contract.get("sourceBoundary", {})
required_source = {
    "requiredSourceVersion": "v27.33f",
    "requiredSourceStatus": (
        "implemented_pure_atomic_consumption_registry_adapter_execution_"
        "plan_acceptance_execution_locked"
    ),
    "requiredAcceptedStatus": (
        "accepted_atomic_consumption_registry_adapter_execution_plan_"
        "execution_locked"
    ),
    "requiredAcceptedReason": (
        "authorization_atomic_consumption_registry_adapter_execution_"
        "plan_accepted_execution_locked"
    ),
    "requiredAccepted": True,
    "requiredExecutionGrant": False,
    "allSourceSecurityFlagsMustBeFalse": True,
}
for key, expected in required_source.items():
    if source_boundary.get(key) != expected:
        fail(f"Quellgrenze ist ungültig: {key}")

source_acceptance = source.get("acceptanceBoundary", {})
if source_acceptance.get("successStatus") != required_source[
    "requiredAcceptedStatus"
]:
    fail("Quell-Annahmestatus ist nicht gebunden.")
if source_acceptance.get("successReason") != required_source[
    "requiredAcceptedReason"
]:
    fail("Quell-Annahmegrund ist nicht gebunden.")
if source_acceptance.get("executionGrant") is not False:
    fail("Quell-Annahme öffnet den Grant.")

interface = contract.get("interfaceBoundary", {})
expected_inputs = [
    "operationId",
    "requestId",
    "authorizationNonce",
    "planFingerprint",
    "actorId",
    "purpose",
    "expectedState",
    "desiredState",
    "consumptionRecord",
    "evidenceTemplate",
]
expected_results = [
    "committed",
    "already_consumed",
    "parallel_conflict",
    "binding_conflict",
    "expired",
    "adapter_unavailable",
    "atomicity_unavailable",
    "commit_ambiguous",
    "operation_failed",
]
required_interface = {
    "adapterKind": "single_use_consumption_registry",
    "interfaceVersion": 1,
    "plannedModulePath": (
        "tools/accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_"
        "registry_adapter.py"
    ),
    "protocolName": "AtomicConsumptionRegistryAdapter",
    "factoryName": "build_atomic_consumption_registry_adapter",
    "operationName": "consume_materialization_authorization_atomically",
    "requiredCapability": (
        "atomic_compare_and_set_with_consumption_record"
    ),
    "expectedState": "unused",
    "desiredState": "consumed",
    "exactInputFields": expected_inputs,
    "exactResultKinds": expected_results,
    "singleAdapterInvocationRequired": True,
    "maximumParallelWinners": 1,
    "operationTimeoutMilliseconds": 15000,
    "connectTimeoutMilliseconds": 3000,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
    "rawErrorSuppressed": True,
    "executionGrant": False,
}
for key, expected in required_interface.items():
    if interface.get(key) != expected:
        fail(f"Adapter-Schnittstellengrenze ist ungültig: {key}")

atomicity = contract.get("atomicityBoundary", {})
for key in (
    "compareAndSetAndConsumptionRecordSingleTransactionRequired",
    "consumptionRecordRequiredOnCommitted",
    "evidenceDerivedOnlyFromConfirmedRecord",
    "alreadyConsumedIsTerminal",
    "bindingConflictIsTerminal",
    "expiredIsTerminal",
):
    if atomicity.get(key) is not True:
        fail(f"Atomaritätsgrenze fehlt: {key}")
if atomicity.get("resetConsumedToUnusedAllowed") is not False:
    fail("Consumed darf nicht auf unused zurückgesetzt werden.")
if atomicity.get("parallelWinnerCountMaximum") != 1:
    fail("Parallelgewinnergrenze ist ungültig.")

ambiguity = contract.get("ambiguityBoundary", {})
if ambiguity.get("commitAmbiguousTerminalForAutomaticRetry") is not True:
    fail("Unklarer Commit ist nicht für automatischen Retry terminal.")
if ambiguity.get("automaticRetryAfterAmbiguousAllowed") is not False:
    fail("Automatischer Retry nach unklarem Commit ist offen.")
if ambiguity.get("reconciliationRequired") is not True:
    fail("Reconciliation-Pflicht fehlt.")
if ambiguity.get("reconciliationMayReadByOperationIdLater") is not True:
    fail("Spätere Reconciliation per Operations-ID fehlt.")
for key in (
    "reconciliationMayWriteAllowed",
    "assumeCommittedAllowed",
    "assumeUnusedAllowed",
):
    if ambiguity.get(key) is not False:
        fail(f"Ambiguitätsgrenze ist offen: {key}")

dependency = contract.get("dependencyBoundary", {})
if dependency.get("dependencyInjectionRequired") is not True:
    fail("Dependency-Injection-Pflicht fehlt.")
for key, value in dependency.items():
    if key == "dependencyInjectionRequired":
        continue
    if value is not False:
        fail(f"Abhängigkeitsgrenze ist offen: {key}")

implementation = contract.get("implementationBoundary", {})
if implementation.get("implementationContractPrepared") is not True:
    fail("Implementierungsvertrag ist nicht markiert.")
for key, value in implementation.items():
    if key == "implementationContractPrepared":
        continue
    if value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

security = contract.get("securityBoundary", {})
if not isinstance(security, dict) or not security:
    fail("Sicherheitsgrenzen fehlen.")
for key, value in security.items():
    if value is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")

unresolved = contract.get("unresolvedRequirements", {})
if not isinstance(unresolved, dict) or not unresolved:
    fail("Offene Anforderungen fehlen.")
for key, value in unresolved.items():
    if value is not True:
        fail(f"Offene Anforderung wurde vorzeitig geschlossen: {key}")

if FUTURE_ADAPTER.exists():
    fail("v27.33g darf noch keinen Registry-Adapter implementieren.")
if FUTURE_EXECUTION.exists():
    fail("v27.33g darf noch keine Adapter-Ausführung umsetzen.")
if list(MIGRATIONS.glob("*v2733g*.sql")):
    fail("v27.33g darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Implementierungsvertrag: OK")
print("Quell-Annahme-Guard: v27.33f")
print("Schnittstelle und Ergebnisarten: geprüft")
print("Atomarität und Reconciliation: geprüft")
print("Adaptermodul erstellt: nein")
print("Adapter importiert: nein")
print("Adapter instanziiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.33g: keine")
print("Produktive Freigabe: nein")
