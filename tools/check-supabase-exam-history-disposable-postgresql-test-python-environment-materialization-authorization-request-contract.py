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
        "authorization-request-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-plan-"
        "acceptance-guard-contract.json"
    )
)
FUTURE_BUILDER = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_request.py"
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
    "v27.32l-Autorisierungsanfrage-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32k-Plan-Annahme-Guard-Vertrag",
)

if contract.get("version") != "v27.32l":
    fail("Autorisierungsanfrage-Vertrag besitzt nicht v27.32l.")
if contract.get("contractVersion") != 1:
    fail("Autorisierungsanfrage-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_authorization_request_fully_locked_not_issued"
):
    fail("Autorisierungsanfrage-Status ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Autorisierungsanfrage darf nicht produktiv sein.")

if source.get("version") != "v27.32k":
    fail("Quellvertrag besitzt nicht v27.32k.")
if source.get("implementation", {}).get(
    "materializationPlanAcceptanceGuardImplemented"
) is not True:
    fail("Quell-Annahme-Guard ist nicht implementiert.")
if source.get("acceptanceBoundary", {}).get("successStatus") != (
    "accepted_execution_locked"
):
    fail("Quell-Annahme-Guard besitzt falschen Erfolgsstatus.")
if source.get("acceptanceBoundary", {}).get(
    "authorizationGrantAccepted"
) is not False:
    fail("Quell-Annahme-Guard hat unerwartet Freigabe akzeptiert.")

implementation = contract.get("implementation", {})
if implementation.get(
    "authorizationRequestContractImplemented"
) is not True:
    fail("Autorisierungsanfrage-Vertrag fehlt.")

for key in (
    "authorizationRequestBuilderImplemented",
    "authorizationRequestStateImplemented",
    "authorizationRequestIssued",
    "authorizationTokenGenerated",
    "authorizationGranted",
    "authorizationConsumed",
    "expiryEvaluated",
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

binding = contract.get("planBindingBoundary", {})
if binding.get("bindingType") != "canonical_plan_fingerprint":
    fail("Planbindungstyp ist ungültig.")
if binding.get("algorithm") != "sha256":
    fail("Plan-Fingerprint-Algorithmus ist ungültig.")
if binding.get("canonicalJsonSortKeys") is not True:
    fail("Kanonische Schlüsselreihenfolge fehlt.")
if binding.get("canonicalJsonSeparators") != [",", ":"]:
    fail("Kanonische JSON-Trennzeichen sind ungültig.")
if binding.get("fingerprintFormat") != (
    "lowercase_hex_64_characters"
):
    fail("Plan-Fingerprint-Format ist ungültig.")
if binding.get("rawAcceptedPlanStoredInRequest") is not False:
    fail("Rohplan darf nicht in Anfrage gespeichert werden.")
if binding.get("planMutationInvalidatesRequest") is not True:
    fail("Planänderung muss Anfrage ungültig machen.")

identity = contract.get("identityBoundary", {})
if identity.get("requestIdFormat") != "uuid_v4_lowercase":
    fail("Request-ID-Format ist ungültig.")
if identity.get("requestNonceEntropyBytes") != 32:
    fail("Nonce-Entropie ist ungültig.")
if identity.get("requestNonceEncoding") != (
    "base64url_without_padding"
):
    fail("Nonce-Encoding ist ungültig.")
if identity.get("actorKind") != "human_operator":
    fail("Akteurtyp ist ungültig.")

request = contract.get("requestBoundary", {})
if request.get("requestVersion") != 1:
    fail("Anfrageversion ist ungültig.")
if request.get("singleUse") is not True:
    fail("Einmalverwendung fehlt.")
if request.get("executionGrant") is not False:
    fail("Anfrage darf keine Freigabe enthalten.")
if request.get("initialStatus") != (
    "authorization_request_pending_locked"
):
    fail("Initialer Anfragestatus ist ungültig.")
if request.get("unknownFieldsAllowed") is not False:
    fail("Unbekannte Anfragefelder dürfen nicht erlaubt sein.")
if request.get("missingFieldsAllowed") is not False:
    fail("Fehlende Anfragefelder dürfen nicht erlaubt sein.")
if request.get("requestMutationAllowed") is not False:
    fail("Anfragemutation darf nicht erlaubt sein.")

flow = contract.get("flowBoundary", {})
if flow.get("approvalStillExecutionLocked") is not True:
    fail("Genehmigung muss ausführungsgesperrt bleiben.")
if flow.get("approvalDirectlyGrantsExecution") is not False:
    fail("Genehmigung darf nicht direkt ausführen.")
if flow.get("requestStateImplemented") is not False:
    fail("Anfragestate darf nicht implementiert sein.")
if flow.get("transitionGuardImplemented") is not False:
    fail("Transition-Guard darf nicht implementiert sein.")

one_time = contract.get("oneTimeBoundary", {})
if one_time.get("singleUseRequired") is not True:
    fail("Einmalverwendungspflicht fehlt.")
if one_time.get(
    "consumptionRequiredBeforeExecutionLater"
) is not True:
    fail("Spätere Verbrauchspflicht fehlt.")

for key in (
    "replayAllowed",
    "requestIdReuseAllowed",
    "requestNonceReuseAllowed",
    "consumedRequestReusable",
    "parallelConsumptionAllowed",
    "consumptionImplemented",
):
    if one_time.get(key) is not False:
        fail(f"Einmalgrenze ist offen: {key}")

expiry = contract.get("expiryBoundary", {})
if expiry.get("timestampFormat") != "rfc3339_utc_z":
    fail("Zeitstempelformat ist ungültig.")
if expiry.get("timeToLiveSeconds") != 300:
    fail("Gültigkeitsdauer ist ungültig.")
if expiry.get("minimumTimeToLiveSeconds") != 300:
    fail("Minimale Gültigkeitsdauer ist ungültig.")
if expiry.get("maximumTimeToLiveSeconds") != 300:
    fail("Maximale Gültigkeitsdauer ist ungültig.")
if expiry.get("gracePeriodSeconds") != 0:
    fail("Kulanzzeit ist ungültig.")
if expiry.get("trustedClockRequiredLater") is not True:
    fail("Spätere vertrauenswürdige Uhr fehlt.")

for key in (
    "renewalAllowed",
    "extensionAllowed",
    "expiredRequestUsable",
    "clockReadImplemented",
    "expiryEvaluationImplemented",
):
    if expiry.get(key) is not False:
        fail(f"Ablaufgrenze ist offen: {key}")

security = contract.get("securityBoundary", {})
for key in (
    "authorizationRequestCreationAllowed",
    "authorizationGrantAllowed",
    "authorizationTokenAllowed",
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

if FUTURE_BUILDER.exists():
    fail(
        "v27.32l darf noch keinen "
        "Autorisierungsanfrage-Builder umsetzen."
    )

preflight = (ROOT / "tools" / "preflight.py").read_text(
    encoding="utf-8",
    errors="replace",
).lower()

for marker in (
    "uuid.uuid4(",
    "secrets.token",
    "os.urandom(",
    "datetime.now(",
    "time.time(",
    "python -m venv",
    "py -m venv",
    "pip install",
    "python -m pip",
    "py -m pip",
):
    if marker in preflight:
        fail(
            "Preflight enthält unerlaubte "
            f"Autorisierungs-/Ausführungsaktion: {marker}"
        )

if list(MIGRATIONS.glob("*v2732l*.sql")):
    fail("v27.32l darf keine SQL-Migration erzeugen.")

print("Disposable Materialisierungs-Autorisierungsanfrage: OK")
print("Quellvertrag: v27.32k")
print("Planbindung: kanonischer SHA-256-Fingerprint")
print("Request-ID: spätere UUID v4")
print("Nonce: später 32 Byte Base64url")
print("Akteur: späterer menschlicher Operator")
print("Gültigkeit: exakt 300 Sekunden")
print("Einmalverwendung: verpflichtend")
print("Request-Builder implementiert: nein")
print("Anfrage ausgestellt: nein")
print("Token erzeugt: nein")
print("Freigabe erteilt: nein")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Virtuelle Umgebung erstellt: nein")
print("Dependency installiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32l: keine")
print("Produktive Freigabe: nein")
