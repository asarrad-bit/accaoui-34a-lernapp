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
        "authorization-consumption-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-request-transition-guard-contract.json"
    )
)
FUTURE_STATE = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_consumption_state.py"
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
    "v27.32o-Autorisierungsverbrauchsvertrag",
)
source = load_json(
    SOURCE,
    "v27.32n-Autorisierungs-Transition-Vertrag",
)

if contract.get("version") != "v27.32o":
    fail("Verbrauchsvertrag besitzt nicht v27.32o.")
if contract.get("contractVersion") != 1:
    fail("Verbrauchsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_single_use_consumption_"
    "fully_locked_not_executed"
):
    fail("Verbrauchsvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Verbrauchsvertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32n":
    fail("Quellvertrag besitzt nicht v27.32n.")
if source.get("implementation", {}).get(
    "authorizationTransitionGuardImplemented"
) is not True:
    fail("Quell-Transition-Guard ist nicht implementiert.")
if source.get("transitionBoundary", {}).get(
    "approveTargetStatus"
) != "authorization_request_approved_locked":
    fail("Quell-Genehmigungsstatus ist ungültig.")
if source.get("transitionBoundary", {}).get(
    "approvalStillExecutionLocked"
) is not True:
    fail("Quell-Genehmigung ist nicht gesperrt.")
if source.get("transitionBoundary", {}).get(
    "executionGrant"
) is not False:
    fail("Quell-Genehmigung besitzt unerwartete Freigabe.")

implementation = contract.get("implementation", {})

if implementation.get(
    "authorizationConsumptionContractImplemented"
) is not True:
    fail("Autorisierungsverbrauchsvertrag fehlt.")

for key in (
    "authorizationConsumptionStateImplemented",
    "replayRegistryImplemented",
    "atomicCompareAndSetImplemented",
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

if source_boundary.get("requiredTransitionStatus") != (
    "transition_applied_execution_locked"
):
    fail("Verbrauchs-Quellstatus ist ungültig.")
if source_boundary.get("requiredRequestStatus") != (
    "authorization_request_approved_locked"
):
    fail("Verbrauchs-Anfragestatus ist ungültig.")
if source_boundary.get("requiredDecision") != "approve":
    fail("Verbrauchs-Entscheidungsgrenze ist ungültig.")
if source_boundary.get("requiredTerminal") is not False:
    fail("Genehmigte Quelle darf nicht terminal sein.")
if source_boundary.get("requiredExecutionGrant") is not False:
    fail("Verbrauchsquelle darf keine Freigabe enthalten.")

for key in (
    "rejectedSourceAllowed",
    "expiredSourceAllowed",
    "revokedSourceAllowed",
    "pendingSourceAllowed",
    "sourceMutationAllowed",
):
    if source_boundary.get(key) is not False:
        fail(f"Quellgrenze ist offen: {key}")

binding = contract.get("bindingBoundary", {})

if binding.get("requestVersion") != 1:
    fail("Request-Version ist ungültig.")
if binding.get("requestIdFormat") != "uuid_v4_lowercase":
    fail("Request-ID-Format ist ungültig.")
if binding.get("requestNonceDecodedLengthBytes") != 32:
    fail("Nonce-Länge ist ungültig.")
if binding.get("planFingerprintAlgorithm") != "sha256":
    fail("Plan-Fingerprint-Algorithmus ist ungültig.")
if binding.get("planFingerprintFormat") != (
    "lowercase_hex_64_characters"
):
    fail("Plan-Fingerprint-Format ist ungültig.")

for key in (
    "requestIdMustMatchApprovedRequest",
    "requestNonceMustMatchApprovedRequest",
    "planFingerprintMustMatchApprovedRequest",
    "actorMustMatchApprovedRequest",
    "purposeMustMatchApprovedRequest",
):
    if binding.get(key) is not True:
        fail(f"Bindungspflicht fehlt: {key}")

if binding.get("bindingMutationAllowed") is not False:
    fail("Bindungsmutation darf nicht erlaubt sein.")

approval = contract.get("approvalBoundary", {})

if approval.get("approvedStatus") != (
    "authorization_request_approved_locked"
):
    fail("Genehmigungsstatus ist ungültig.")
if approval.get("approvalStillExecutionLocked") is not True:
    fail("Genehmigung muss ausführungsgesperrt bleiben.")
if approval.get("approvalDirectlyGrantsExecution") is not False:
    fail("Genehmigung darf nicht direkt ausführen.")
if approval.get("executionGrant") is not False:
    fail("Genehmigung darf keine Freigabe besitzen.")
if approval.get("authorizationTokenAllowed") is not False:
    fail("Autorisierungstoken darf nicht erlaubt sein.")
if approval.get("approvalReusable") is not False:
    fail("Genehmigung darf nicht wiederverwendbar sein.")

expiry = contract.get("expiryBoundary", {})

if expiry.get("timestampFormat") != "rfc3339_utc_z_seconds":
    fail("Zeitstempelformat ist ungültig.")
if expiry.get("consumedAtMustBeBeforeExpiresAt") is not True:
    fail("Verbrauch muss vor Ablauf liegen.")
if expiry.get("atExpiresAtIsExpired") is not True:
    fail("Ablaufgrenze ist ungültig.")
if expiry.get("gracePeriodSeconds") != 0:
    fail("Kulanzzeit ist ungültig.")
if expiry.get("trustedClockRequiredLater") is not True:
    fail("Vertrauenswürdige Uhr fehlt.")
if expiry.get("clockReadImplemented") is not False:
    fail("Uhrabfrage darf nicht implementiert sein.")
if expiry.get("expiredApprovalConsumable") is not False:
    fail("Abgelaufene Genehmigung darf nicht verbrauchbar sein.")

single_use = contract.get("singleUseBoundary", {})

if single_use.get("singleUseRequired") is not True:
    fail("Einmalverwendungspflicht fehlt.")
if single_use.get("registryKeyFields") != [
    "requestId",
    "requestNonce",
    "acceptedPlanFingerprint",
]:
    fail("Registry-Schlüssel ist ungültig.")
if single_use.get("initialRegistryState") != "unused":
    fail("Registry-Initialstatus ist ungültig.")
if single_use.get("successRegistryState") != "consumed":
    fail("Registry-Erfolgsstatus ist ungültig.")
if single_use.get("atomicCompareAndSetRequired") is not True:
    fail("Atomare Compare-and-set-Pflicht fehlt.")
if single_use.get("compareState") != "unused":
    fail("Compare-Status ist ungültig.")
if single_use.get("setState") != "consumed":
    fail("Set-Status ist ungültig.")

for key in (
    "replayAllowed",
    "parallelConsumptionAllowed",
    "secondConsumptionAllowed",
    "consumedRequestReusable",
    "requestIdReuseAllowed",
    "requestNonceReuseAllowed",
    "differentPlanFingerprintReuseAllowed",
    "registryReadImplemented",
    "registryWriteImplemented",
    "consumptionImplemented",
):
    if single_use.get(key) is not False:
        fail(f"Einmalgrenze ist offen: {key}")

receipt = contract.get("receiptBoundary", {})

if receipt.get("receiptRequiredLater") is not True:
    fail("Späterer Verbrauchsnachweis fehlt.")
if receipt.get("requestNonceStoredRawInReceipt") is not False:
    fail("Roh-Nonce darf nicht im Nachweis stehen.")
if receipt.get("requestNonceFingerprintAlgorithm") != "sha256":
    fail("Nonce-Fingerprint-Algorithmus ist ungültig.")
if receipt.get("receiptStatus") != (
    "authorization_consumed_execution_locked"
):
    fail("Nachweisstatus ist ungültig.")
if receipt.get("executionGrant") is not False:
    fail("Verbrauchsnachweis darf keine Freigabe enthalten.")
if receipt.get("receiptImplemented") is not False:
    fail("Verbrauchsnachweis darf nicht implementiert sein.")

security = contract.get("securityBoundary", {})

for key in (
    "authorizationConsumptionAllowed",
    "authorizationGrantAllowed",
    "authorizationTokenAllowed",
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

if FUTURE_STATE.exists():
    fail(
        "v27.32o darf noch keinen "
        "Autorisierungsverbrauchs-State umsetzen."
    )

preflight = (ROOT / "tools" / "preflight.py").read_text(
    encoding="utf-8",
    errors="replace",
).lower()

for marker in (
    "compare_and_set(",
    "compare-and-set",
    "authorization_consumed_execution_locked",
    "python -m venv",
    "py -m venv",
    "pip install",
    "python -m pip",
    "py -m pip",
):
    if marker in preflight:
        fail(
            "Preflight enthält unerlaubte "
            f"Verbrauchs-/Ausführungsaktion: {marker}"
        )

if list(MIGRATIONS.glob("*v2732o*.sql")):
    fail("v27.32o darf keine SQL-Migration erzeugen.")

print("Disposable Autorisierungsverbrauchsvertrag: OK")
print("Quellvertrag: v27.32n")
print("Quellstatus: transition_applied_execution_locked")
print("Erforderliche Anfrage: approved_locked")
print("Plan-, Request-ID- und Nonce-Bindung: festgelegt")
print("Ablaufprüfung: vor expiresAt, ohne Kulanz")
print("Einmalverwendung: atomare Compare-and-set-Pflicht")
print("Replay und Parallelverbrauch: verboten")
print("Verbrauchs-State implementiert: nein")
print("Registry implementiert: nein")
print("Verbrauch ausgeführt: nein")
print("Freigabe erteilt: nein")
print("Token erzeugt: nein")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Virtuelle Umgebung erstellt: nein")
print("Dependency installiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32o: keine")
print("Produktive Freigabe: nein")
