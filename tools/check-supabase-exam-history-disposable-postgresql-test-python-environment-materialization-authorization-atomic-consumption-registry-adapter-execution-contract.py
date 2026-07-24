from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"
CONTRACT = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-execution-contract.json"
)
SOURCE = ROOT / "docs" / "contracts" / (
    "exam-history-disposable-postgresql-test-python-environment-"
    "materialization-authorization-atomic-consumption-registry-"
    "adapter-readiness-acceptance-guard-contract.json"
)
FUTURE_EXECUTION = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution.py"
)
FUTURE_PLAN = ROOT / "tools" / (
    "accaoui_disposable_test_python_environment_materialization_"
    "authorization_atomic_consumption_registry_adapter_execution_plan.py"
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

contract = load_json(CONTRACT, "v27.32z-Vertrag")
source = load_json(SOURCE, "v27.32y-Quellvertrag")

if contract.get("version") != "v27.32z":
    fail("Ausführungsvertrag besitzt nicht v27.32z.")
if contract.get("contractVersion") != 1:
    fail("Ausführungsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_atomic_consumption_registry_adapter_execution_"
    "fully_locked_not_implemented"
):
    fail("Ausführungsvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe ist offen.")
if source.get("version") != "v27.32y":
    fail("Quellvertrag besitzt nicht v27.32y.")
if source.get("status") != (
    "implemented_pure_atomic_consumption_registry_adapter_"
    "readiness_acceptance_execution_locked"
):
    fail("Quellvertragsstatus ist ungültig.")

source_boundary = contract.get("sourceBoundary", {})
required_source = {
    "requiredSourceVersion":"v27.32y",
    "requiredAcceptedStatus":"accepted_atomic_consumption_registry_adapter_readiness_execution_locked",
    "requiredAcceptedReason":"authorization_atomic_consumption_registry_adapter_readiness_accepted_execution_locked",
    "requiredAccepted":True,
    "requiredExecutionGrant":False,
    "allSourceSecurityFlagsMustBeFalse":True,
}
for key, expected in required_source.items():
    if source_boundary.get(key) != expected:
        fail(f"Quellgrenze ist ungültig: {key}")

execution = contract.get("executionBoundary", {})
expected_results = [
    "committed","already_consumed","parallel_conflict","binding_conflict",
    "expired","adapter_unavailable","atomicity_unavailable",
    "commit_ambiguous","operation_failed",
]
required_execution = {
    "adapterKind":"single_use_consumption_registry",
    "requiredCapability":"atomic_compare_and_set_with_consumption_record",
    "expectedState":"unused","desiredState":"consumed",
    "singleAdapterInvocationRequired":True,"maximumParallelWinners":1,
    "operationTimeoutMilliseconds":15000,"connectTimeoutMilliseconds":3000,
    "statementTimeoutMilliseconds":5000,"lockTimeoutMilliseconds":2000,
    "exactResultKinds":expected_results,"rawErrorSuppressed":True,
    "executionGrant":False,
}
for key, expected in required_execution.items():
    if execution.get(key) != expected:
        fail(f"Ausführungsgrenze ist ungültig: {key}")

atomicity = contract.get("atomicityBoundary", {})
for key in (
    "compareAndSetAndConsumptionRecordSingleTransactionRequired",
    "consumptionRecordRequiredOnCommitted",
    "evidenceDerivedOnlyFromConfirmedRecord",
    "alreadyConsumedIsTerminal","bindingConflictIsTerminal","expiredIsTerminal",
):
    if atomicity.get(key) is not True:
        fail(f"Atomaritätsgrenze fehlt: {key}")
if atomicity.get("resetConsumedToUnusedAllowed") is not False:
    fail("Consumed darf nicht zurückgesetzt werden.")
if atomicity.get("parallelWinnerCountMaximum") != 1:
    fail("Atomare Parallelgrenze ist ungültig.")

ambiguity = contract.get("ambiguityBoundary", {})
if ambiguity.get("commitAmbiguousTerminalForAutomaticRetry") is not True:
    fail("Unklarer Commit ist nicht terminal.")
if ambiguity.get("automaticRetryAfterAmbiguousAllowed") is not False:
    fail("Automatischer Retry ist offen.")
if ambiguity.get("reconciliationRequired") is not True:
    fail("Reconciliation-Pflicht fehlt.")
for key in ("reconciliationMayWriteAllowed","assumeCommittedAllowed","assumeUnusedAllowed"):
    if ambiguity.get(key) is not False:
        fail(f"Ambiguitätsgrenze ist offen: {key}")

implementation = contract.get("implementationBoundary", {})
if implementation.get("executionContractPrepared") is not True:
    fail("Ausführungsvertrag ist nicht markiert.")
for key, value in implementation.items():
    if key != "executionContractPrepared" and value is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

security = contract.get("securityBoundary", {})
if not isinstance(security, dict) or not security:
    fail("Sicherheitsgrenzen fehlen.")
for key, value in security.items():
    if value is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")

if FUTURE_EXECUTION.exists():
    fail("v27.32z darf noch keine Adapter-Ausführung umsetzen.")
if FUTURE_PLAN.exists():
    fail("v27.32z darf noch keinen Ausführungsplan umsetzen.")
if list(MIGRATIONS.glob("*v2732z*.sql")):
    fail("v27.32z darf keine SQL-Migration erzeugen.")

print("Registry-Adapter-Ausführungsvertrag: OK")
print("Quellvertrag: v27.32y")
print("Atomare Einzelaufruf- und Parallelgrenze: geprüft")
print("Zeitlimits und Ergebnisarten: geprüft")
print("Ambiguität und Reconciliation: geprüft")
print("Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registryzugriff: keiner")
print("Verbrauch ausgeführt: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32z: keine")
print("Produktive Freigabe: nein")
