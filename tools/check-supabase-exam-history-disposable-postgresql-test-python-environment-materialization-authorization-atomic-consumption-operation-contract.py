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
        "authorization-atomic-consumption-operation-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-consumption-readiness-"
        "acceptance-guard-contract.json"
    )
)
FUTURE_PLAN = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_atomic_consumption_plan.py"
    )
)
FUTURE_ADAPTER = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_consumption_"
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
    "v27.32r-Atomarer-Verbrauchsoperationsvertrag",
)
source = load_json(
    SOURCE,
    "v27.32q-Readiness-Annahmevertrag",
)

if contract.get("version") != "v27.32r":
    fail("Operationsvertrag besitzt nicht v27.32r.")
if contract.get("contractVersion") != 1:
    fail("Operationsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_atomic_consumption_operation_"
    "fully_locked_not_executed"
):
    fail("Operationsvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Operationsvertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32q":
    fail("Quellvertrag besitzt nicht v27.32q.")
if source.get("implementation", {}).get(
    "consumptionReadinessAcceptanceGuardImplemented"
) is not True:
    fail("Quell-Annahme-Guard ist nicht implementiert.")
if source.get("acceptanceBoundary", {}).get(
    "successStatus"
) != "accepted_consumption_ready_execution_locked":
    fail("Quell-Annahme-Guard besitzt falschen Erfolgsstatus.")
if source.get("acceptanceBoundary", {}).get(
    "authorizationConsumptionAllowed"
) is not False:
    fail("Quell-Annahme-Guard erlaubt unerwartet Verbrauch.")

implementation = contract.get("implementation", {})

if implementation.get(
    "atomicConsumptionOperationContractImplemented"
) is not True:
    fail("Atomarer Verbrauchsoperationsvertrag fehlt.")

for key in (
    "atomicConsumptionPlanImplemented",
    "registryAdapterImplemented",
    "registryReadPerformed",
    "registryWritePerformed",
    "atomicCompareAndSetPerformed",
    "consumptionRecordCommitted",
    "consumptionReceiptImplemented",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
    "trustedClockRead",
    "filesystemReadPerformed",
    "filesystemMutationPerformed",
    "processExecuted",
    "virtualEnvironmentCreated",
    "dependencyInstalled",
    "driverImported",
    "databaseConnectionCreated",
    "databaseTestExecuted",
    "sqlMigrationCreated",
    "frontendIntegration",
):
    if implementation.get(key) is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

source_boundary = contract.get("sourceBoundary", {})

if source_boundary.get("requiredStatus") != (
    "accepted_consumption_ready_execution_locked"
):
    fail("Operations-Quellstatus ist ungültig.")
if source_boundary.get("requiredAccepted") is not True:
    fail("Annahmepflicht fehlt.")
if source_boundary.get("requiredRegistryState") != "unused":
    fail("Quell-Registryzustand ist ungültig.")
if source_boundary.get("requiredCompareState") != "unused":
    fail("Quell-Comparezustand ist ungültig.")
if source_boundary.get("requiredSetState") != "consumed":
    fail("Quell-Setzustand ist ungültig.")
if source_boundary.get("requiredSingleUse") is not True:
    fail("Einmalverwendungspflicht fehlt.")
if source_boundary.get("requiredExecutionGrant") is not False:
    fail("Quelle darf keine Ausführungsfreigabe besitzen.")

adapter = contract.get("adapterBoundary", {})

if adapter.get("adapterKind") != "single_use_consumption_registry":
    fail("Registry-Adaptertyp ist ungültig.")
if adapter.get("adapterCapabilityRequiredLater") != (
    "atomic_compare_and_set_with_consumption_record"
):
    fail("Registry-Adapterfähigkeit ist ungültig.")
if adapter.get("registryKeyFields") != [
    "requestId",
    "requestNonce",
    "acceptedPlanFingerprint",
]:
    fail("Registry-Schlüssel ist ungültig.")
if adapter.get("expectedState") != "unused":
    fail("Erwarteter Registryzustand ist ungültig.")
if adapter.get("desiredState") != "consumed":
    fail("Ziel-Registryzustand ist ungültig.")
if adapter.get("singleAttemptPerOperation") is not True:
    fail("Einzelversuchspflicht fehlt.")

for key in (
    "readThenWriteSplitAllowed",
    "unconditionalWriteAllowed",
    "upsertAllowed",
    "stateResetToUnusedAllowed",
    "adapterReadAllowed",
    "adapterWriteAllowed",
    "adapterInvocationAllowed",
):
    if adapter.get(key) is not False:
        fail(f"Adaptergrenze ist offen: {key}")

atomicity = contract.get("atomicityBoundary", {})

for key in (
    "compareAndSetRequired",
    "consumptionRecordSameAtomicUnitRequired",
    "receiptSourceMustBeCommittedRecord",
):
    if atomicity.get(key) is not True:
        fail(f"Atomaritätspflicht fehlt: {key}")

for key in (
    "partialCommitAllowed",
    "successWithoutConsumedStateAllowed",
    "consumedStateWithoutRecordAllowed",
    "automaticRetryAfterAmbiguousResultAllowed",
    "operationExecutionAllowed",
):
    if atomicity.get(key) is not False:
        fail(f"Atomaritätsgrenze ist offen: {key}")

if atomicity.get("parallelWinnerCountMaximum") != 1:
    fail("Maximale Gewinnerzahl ist ungültig.")

receipt = contract.get("receiptBoundary", {})

if receipt.get("receiptRequiredOnCommittedSuccess") is not True:
    fail("Verbrauchsnachweispflicht fehlt.")
if receipt.get("requestNonceStoredRaw") is not False:
    fail("Roh-Nonce darf nicht im Nachweis gespeichert werden.")
if receipt.get("requestNonceFingerprintAlgorithm") != "sha256":
    fail("Nonce-Fingerprint-Algorithmus ist ungültig.")
if receipt.get("status") != (
    "authorization_consumed_execution_locked"
):
    fail("Verbrauchsnachweisstatus ist ungültig.")
if receipt.get("singleUse") is not True:
    fail("Nachweis-Einmalverwendung fehlt.")
if receipt.get("executionGrant") is not False:
    fail("Nachweis darf keine Ausführungsfreigabe enthalten.")
if receipt.get("receiptImplemented") is not False:
    fail("Verbrauchsnachweis darf nicht implementiert sein.")

errors = contract.get("errorBoundary", {})

for key in (
    "rawAdapterErrorExposed",
    "rawRegistryValueExposed",
    "secretValueExposed",
    "automaticRetryAllowed",
    "retryAfterAmbiguousCommitAllowed",
):
    if errors.get(key) is not False:
        fail(f"Fehlergrenze ist offen: {key}")

if errors.get(
    "ambiguousCommitRequiresReconciliationLater"
) is not True:
    fail("Reconciliation-Pflicht bei unklarem Commit fehlt.")
if errors.get("closedFailureRequired") is not True:
    fail("Geschlossene Fehlerpflicht fehlt.")

rollback = contract.get("rollbackBoundary", {})

if rollback.get(
    "preCommitFailureLeavesUnusedRequired"
) is not True:
    fail("Pre-Commit-Fehlergrenze fehlt.")

for key in (
    "postCommitResetToUnusedAllowed",
    "compensatingReplayEnablementAllowed",
    "receiptFailureMayResetConsumedState",
    "rollbackRegistryWriteAllowed",
    "rollbackImplemented",
):
    if rollback.get(key) is not False:
        fail(f"Rollbackgrenze ist offen: {key}")

security = contract.get("securityBoundary", {})

for key in (
    "authorizationConsumptionAllowed",
    "authorizationGrantAllowed",
    "authorizationTokenAllowed",
    "registryAdapterAccessAllowed",
    "replayRegistryAccessAllowed",
    "trustedClockReadAllowed",
    "processEnvironmentReadAllowed",
    "filesystemReadAllowed",
    "filesystemMutationAllowed",
    "processExecutionAllowed",
    "networkExecutionAllowed",
    "installerInvocationAllowed",
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

for path, label in (
    (FUTURE_PLAN, "Operationsplan"),
    (FUTURE_ADAPTER, "Registry-Adapter"),
):
    if path.exists():
        fail(f"v27.32r darf noch keinen {label} umsetzen.")

if list(MIGRATIONS.glob("*v2732r*.sql")):
    fail("v27.32r darf keine SQL-Migration erzeugen.")

print("Atomarer Autorisierungsverbrauchsoperationsvertrag: OK")
print("Quellvertrag: v27.32q")
print("Quellstatus: accepted_consumption_ready_execution_locked")
print("Registry-Key: Request-ID, Nonce, Planfingerprint")
print("Atomarer Übergang: unused -> consumed")
print("Verbrauchsrecord: gleiche atomare Einheit erforderlich")
print("Parallelgewinner: höchstens einer")
print("Unklarer Commit: kein automatischer Retry")
print("Nachweisstatus: authorization_consumed_execution_locked")
print("Operationsplan implementiert: nein")
print("Registry-Adapter implementiert: nein")
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
print("SQL-Migration v27.32r: keine")
print("Produktive Freigabe: nein")
