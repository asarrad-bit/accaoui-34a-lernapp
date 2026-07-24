from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-registry-"
        "adapter-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-plan-"
        "acceptance-guard-contract.json"
    )
)
FUTURE_ADAPTER = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_"
        "registry_adapter.py"
    )
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    raise SystemExit(1)


def load_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


contract = load_json(
    CONTRACT,
    "v27.32u-Registry-Adapter-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32t-Operationsplan-Annahmevertrag",
)

if contract.get("version") != "v27.32u":
    fail("Registry-Adapter-Vertrag besitzt nicht v27.32u.")
if contract.get("contractVersion") != 1:
    fail("Registry-Adapter-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_atomic_consumption_registry_adapter_"
    "fully_locked_not_implemented"
):
    fail("Registry-Adapter-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Registry-Adapter-Vertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32t":
    fail("Quellvertrag besitzt nicht v27.32t.")
if source.get("implementation", {}).get(
    "atomicConsumptionPlanAcceptanceGuardImplemented"
) is not True:
    fail("Quell-Operationsplan-Annahme-Guard fehlt.")
if source.get("acceptanceBoundary", {}).get(
    "successStatus"
) != "accepted_atomic_consumption_plan_execution_locked":
    fail("Quell-Annahme-Guard besitzt falschen Erfolgsstatus.")

implementation = contract.get("implementation", {})

if implementation.get(
    "registryAdapterContractImplemented"
) is not True:
    fail("Registry-Adapter-Vertrag fehlt.")

for key in (
    "registryAdapterImplemented",
    "registryAdapterInvoked",
    "registryReadPerformed",
    "registryWritePerformed",
    "atomicCompareAndSetPerformed",
    "consumptionRecordCommitted",
    "consumptionReceiptCommitted",
    "reconciliationImplemented",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
    "trustedClockRead",
    "filesystemReadPerformed",
    "filesystemMutationPerformed",
    "processExecuted",
    "networkExecuted",
    "databaseConnectionCreated",
    "databaseTestExecuted",
    "sqlMigrationCreated",
    "frontendIntegration",
):
    if implementation.get(key) is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

source_boundary = contract.get("sourceBoundary", {})

if source_boundary.get("requiredStatus") != (
    "accepted_atomic_consumption_plan_execution_locked"
):
    fail("Adapter-Quellstatus ist ungültig.")
if source_boundary.get("requiredAccepted") is not True:
    fail("Adapter-Annahmepflicht fehlt.")
if source_boundary.get("requiredOperationAttempt") != 1:
    fail("Operationsversuch ist ungültig.")
if source_boundary.get("requiredAdapterKind") != (
    "single_use_consumption_registry"
):
    fail("Adapterart ist ungültig.")
if source_boundary.get("requiredAdapterCapability") != (
    "atomic_compare_and_set_with_consumption_record"
):
    fail("Adapterfähigkeit ist ungültig.")
if source_boundary.get("requiredExpectedState") != "unused":
    fail("Erwarteter Zustand ist ungültig.")
if source_boundary.get("requiredDesiredState") != "consumed":
    fail("Zielzustand ist ungültig.")
if source_boundary.get("requiredExecutionGrant") is not False:
    fail("Quelle darf keinen Ausführungsgrant besitzen.")

adapter_input = contract.get("adapterInputBoundary", {})

if adapter_input.get("operationAttempt") != 1:
    fail("Adapter-Operationsversuch ist ungültig.")
if adapter_input.get("registryKeyFields") != [
    "requestId",
    "requestNonce",
    "acceptedPlanFingerprint",
]:
    fail("Adapter-Registry-Key ist ungültig.")
if adapter_input.get("requestNonceDecodedLengthBytes") != 32:
    fail("Adapter-Nonce-Länge ist ungültig.")
if adapter_input.get("expectedState") != "unused":
    fail("Adapter-Comparezustand ist ungültig.")
if adapter_input.get("desiredState") != "consumed":
    fail("Adapter-Setzustand ist ungültig.")
if adapter_input.get("timeoutMilliseconds") != 15000:
    fail("Adapter-Zeitlimit ist ungültig.")

atomic = contract.get("atomicOperationBoundary", {})

if atomic.get("operationKind") != (
    "atomic_compare_and_set_with_consumption_record"
):
    fail("Atomare Operationsart ist ungültig.")
if atomic.get("singleAdapterCallRequired") is not True:
    fail("Einzelaufrufspflicht fehlt.")
if atomic.get("maximumParallelWinners") != 1:
    fail("Maximale Parallelgewinnerzahl ist ungültig.")

for key in (
    "readThenWriteSplitAllowed",
    "unconditionalWriteAllowed",
    "upsertAllowed",
    "partialCommitAllowed",
    "consumedWithoutRecordAllowed",
    "recordWithoutConsumedAllowed",
    "automaticRetryAllowed",
    "adapterInvocationAllowed",
):
    if atomic.get(key) is not False:
        fail(f"Atomare Grenze ist offen: {key}")

results = contract.get("resultBoundary", {})

if results.get("exactResultKinds") != [
    "committed",
    "already_consumed",
    "parallel_conflict",
    "binding_conflict",
    "expired",
    "adapter_unavailable",
    "atomicity_unavailable",
    "commit_ambiguous",
    "operation_failed",
]:
    fail("Adapter-Ergebnisarten sind ungültig.")
if results.get("committedStatus") != (
    "authorization_consumed_execution_locked"
):
    fail("Commit-Ergebnisstatus ist ungültig.")
if results.get("executionGrant") is not False:
    fail("Adapter-Ergebnis darf keinen Grant besitzen.")

ambiguity = contract.get("ambiguityBoundary", {})

if ambiguity.get(
    "ambiguousCommitTerminalForAutomaticRetry"
) is not True:
    fail("Ambiguitäts-Retry-Grenze fehlt.")
if ambiguity.get("reconciliationRequired") is not True:
    fail("Reconciliation-Pflicht fehlt.")

for key in (
    "automaticRetryAfterAmbiguousAllowed",
    "reconciliationMayWriteAllowed",
    "assumeCommittedAllowed",
    "assumeUnusedAllowed",
    "rawAdapterErrorExposed",
    "rawRegistryValueExposed",
):
    if ambiguity.get(key) is not False:
        fail(f"Ambiguitätsgrenze ist offen: {key}")

receipt = contract.get("receiptBoundary", {})

if receipt.get("receiptFromCommittedRecordOnly") is not True:
    fail("Nachweis-Commitbindung fehlt.")
if receipt.get("requestNonceStoredRaw") is not False:
    fail("Roh-Nonce darf nicht im Nachweis gespeichert werden.")
if receipt.get("requestNonceFingerprintAlgorithm") != "sha256":
    fail("Nonce-Fingerprint-Algorithmus ist ungültig.")
if receipt.get("status") != (
    "authorization_consumed_execution_locked"
):
    fail("Nachweisstatus ist ungültig.")
if receipt.get("singleUse") is not True:
    fail("Nachweis-Einmalverwendung fehlt.")
if receipt.get("executionGrant") is not False:
    fail("Nachweis darf keinen Grant besitzen.")
if receipt.get("receiptWithoutCommitAllowed") is not False:
    fail("Nachweis ohne Commit darf nicht erlaubt sein.")

timeout = contract.get("timeoutBoundary", {})

if timeout.get("operationTimeoutMilliseconds") != 15000:
    fail("Operationszeitlimit ist ungültig.")
if timeout.get("connectTimeoutMillisecondsMaximum") != 3000:
    fail("Connect-Zeitlimit ist ungültig.")
if timeout.get("statementTimeoutMillisecondsMaximum") != 5000:
    fail("Statement-Zeitlimit ist ungültig.")
if timeout.get("lockTimeoutMillisecondsMaximum") != 2000:
    fail("Lock-Zeitlimit ist ungültig.")
if timeout.get("timeoutIsClosedFailure") is not True:
    fail("Timeout muss geschlossen fehlschlagen.")
if timeout.get("timeoutAutomaticRetryAllowed") is not False:
    fail("Timeout-Retry darf nicht erlaubt sein.")

rollback = contract.get("rollbackBoundary", {})

if rollback.get("preCommitFailureMustLeaveUnused") is not True:
    fail("Pre-Commit-Rollbackgrenze fehlt.")

for key in (
    "postCommitResetToUnusedAllowed",
    "rollbackWriteAllowed",
    "compensatingReplayEnablementAllowed",
    "receiptFailureMayResetConsumedState",
):
    if rollback.get(key) is not False:
        fail(f"Rollbackgrenze ist offen: {key}")

security = contract.get("securityBoundary", {})

for key in (
    "adapterImplementationAllowed",
    "adapterInvocationAllowed",
    "authorizationConsumptionAllowed",
    "authorizationGrantAllowed",
    "authorizationTokenAllowed",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "reconciliationReadAllowed",
    "trustedClockReadAllowed",
    "processEnvironmentReadAllowed",
    "filesystemReadAllowed",
    "filesystemMutationAllowed",
    "processExecutionAllowed",
    "networkExecutionAllowed",
    "driverImportAllowed",
    "databaseConnectionAllowed",
    "passwordAllowed",
    "databaseUrlAllowed",
    "connectionStringAllowed",
    "serviceRoleKeyAllowed",
    "productionSecretAllowed",
    "realParticipantDataAllowed",
    "frontendReferenceAllowed",
):
    if security.get(key) is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")

if FUTURE_ADAPTER.exists():
    fail("v27.32u darf noch keinen Registry-Adapter umsetzen.")

if list(MIGRATIONS.glob("*v2732u*.sql")):
    fail("v27.32u darf keine SQL-Migration erzeugen.")

print("Atomarer Verbrauchs-Registry-Adapter-Vertrag: OK")
print("Quellvertrag: v27.32t")
print("Quellstatus: accepted_atomic_consumption_plan_execution_locked")
print("Adapterart: single_use_consumption_registry")
print("Atomare Fähigkeit: compare-and-set mit Record")
print("Operationszeitlimit: 15000 ms")
print("Definitive Konflikte: festgelegt")
print("Unklarer Commit: Reconciliation erforderlich")
print("Nachweis: nur aus bestätigtem Commit")
print("Registry-Adapter implementiert: nein")
print("Adapter aufgerufen: nein")
print("Registry gelesen: nein")
print("Registry geschrieben: nein")
print("Compare-and-set ausgeführt: nein")
print("Verbrauch ausgeführt: nein")
print("Freigabe erteilt: nein")
print("Token erzeugt: nein")
print("Uhr gelesen: nein")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32u: keine")
print("Produktive Freigabe: nein")
