from pathlib import Path
import ast
import base64
import importlib.util
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
        "authorization-consumption-readiness-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-consumption-contract.json"
    )
)
STATE = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_consumption_readiness.py"
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


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)

    if spec is None or spec.loader is None:
        fail(f"Modul ist nicht ladbar: {path.name}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def clone(value):
    return json.loads(json.dumps(value))


contract = load_json(
    CONTRACT,
    "v27.32p-Verbrauchs-Readiness-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32o-Autorisierungsverbrauchsvertrag",
)

if contract.get("version") != "v27.32p":
    fail("Readiness-Vertrag besitzt nicht v27.32p.")
if contract.get("contractVersion") != 1:
    fail("Readiness-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_consumption_readiness_execution_locked"
):
    fail("Readiness-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Readiness-Vertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32o":
    fail("Quellvertrag besitzt nicht v27.32o.")
if source.get("implementation", {}).get(
    "authorizationConsumptionContractImplemented"
) is not True:
    fail("Quell-Verbrauchsvertrag ist nicht implementiert.")
if source.get("implementation", {}).get(
    "authorizationConsumptionStateImplemented"
) is not False:
    fail("Quellvertrag hatte unerwartet bereits einen State.")

implementation = contract.get("implementation", {})

if implementation.get(
    "authorizationConsumptionReadinessImplemented"
) is not True:
    fail("Verbrauchs-Readiness-State fehlt.")

for key in (
    "replayRegistryImplemented",
    "registryReadPerformed",
    "registryWritePerformed",
    "atomicCompareAndSetPerformed",
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

state_source = STATE.read_text(encoding="utf-8")
tree = ast.parse(state_source)

allowed_imports = {
    "__future__",
    "collections",
    "datetime",
    "base64",
    "hashlib",
    "re",
}
seen_imports = set()

for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen_imports.add(alias.name.split(".", 1)[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        seen_imports.add(node.module.split(".", 1)[0])

unexpected_imports = seen_imports - allowed_imports

if unexpected_imports:
    fail(f"Readiness-State besitzt unerlaubte Importe: {unexpected_imports}")

forbidden_names = {
    "Path",
    "os",
    "sys",
    "subprocess",
    "shutil",
    "venv",
    "socket",
    "requests",
    "urllib",
    "uuid",
    "secrets",
    "time",
}

for node in ast.walk(tree):
    if isinstance(node, ast.Name) and node.id in forbidden_names:
        fail(f"Readiness-State verwendet verbotenen Namen: {node.id}")

lower_source = state_source.lower()

for marker in (
    "datetime.now(",
    "datetime.utcnow(",
    "time.time(",
    "uuid4(",
    "urandom(",
    "token_bytes(",
    "compare_and_set(",
    "registry.read",
    "registry.write",
    "pip install",
    "python -m venv",
    "py -m venv",
    "subprocess",
    ".connect(",
    "postgres://",
    "postgresql://",
    "database_url",
    "service_role",
):
    if marker in lower_source:
        fail(f"Readiness-State enthält verbotenen Inhalt: {marker}")

module = load_module(
    STATE,
    "accaoui_consumption_readiness_v2732p",
)
evaluate = getattr(
    module,
    "evaluate_materialization_authorization_consumption_readiness",
    None,
)

if not callable(evaluate):
    fail("Verbrauchs-Readiness-Funktion fehlt.")

nonce = base64.urlsafe_b64encode(bytes(range(32))).decode(
    "ascii"
).rstrip("=")

request = {
    "version": 1,
    "requestId": "123e4567-e89b-42d3-a456-426614174000",
    "requestNonce": nonce,
    "actor": {
        "kind": "human_operator",
        "id": "local-test-operator",
    },
    "purpose": (
        "disposable_test_python_environment_materialization"
    ),
    "acceptedPlanStatus": "accepted_execution_locked",
    "acceptedPlanReason": (
        "test_environment_materialization_plan_"
        "accepted_execution_locked"
    ),
    "acceptedPlanFingerprint": "a" * 64,
    "issuedAt": "2026-07-24T10:00:00Z",
    "expiresAt": "2026-07-24T10:05:00Z",
    "singleUse": True,
    "executionGrant": False,
    "status": "authorization_request_approved_locked",
}

valid_transition = {
    "status": "transition_applied_execution_locked",
    "reason": (
        "materialization_authorization_"
        "transition_applied_execution_locked"
    ),
    "transition": {
        "request": request,
        "decision": "approve",
        "evaluatedAt": "2026-07-24T10:01:00Z",
        "sourceStatus": (
            "authorization_request_pending_locked"
        ),
        "targetStatus": (
            "authorization_request_approved_locked"
        ),
        "terminal": False,
        "executionGrant": False,
    },
    "authorizationGranted": False,
    "authorizationTokenGenerated": False,
    "authorizationConsumed": False,
    "environmentCreationAllowed": False,
    "filesystemReadAllowed": False,
    "filesystemMutationAllowed": False,
    "processExecutionAllowed": False,
    "dependencyInstallationAllowed": False,
}

valid_facts = {
    "transitionResult": valid_transition,
    "requestId": request["requestId"],
    "requestNonce": request["requestNonce"],
    "acceptedPlanFingerprint": request[
        "acceptedPlanFingerprint"
    ],
    "actor": request["actor"],
    "purpose": request["purpose"],
    "consumedAt": "2026-07-24T10:02:00Z",
    "registryState": "unused",
}

cases = [
    (
        [],
        "blocked",
        (
            "materialization_authorization_"
            "consumption_readiness_invalid_input"
        ),
    ),
    (
        {
            key: value
            for key, value in valid_facts.items()
            if key != "registryState"
        },
        "blocked",
        (
            "materialization_authorization_"
            "consumption_readiness_missing_fields"
        ),
    ),
    (
        {
            **valid_facts,
            "unexpected": True,
        },
        "blocked",
        (
            "materialization_authorization_"
            "consumption_readiness_unknown_fields"
        ),
    ),
    (
        {
            **valid_facts,
            "requestId": (
                "123e4567-e89b-42d3-a456-426614174001"
            ),
        },
        "blocked",
        (
            "materialization_authorization_"
            "consumption_binding_invalid"
        ),
    ),
    (
        {
            **valid_facts,
            "registryState": "consumed",
        },
        "blocked",
        (
            "materialization_authorization_"
            "consumption_already_consumed"
        ),
    ),
    (
        {
            **valid_facts,
            "registryState": "in_flight",
        },
        "blocked",
        (
            "materialization_authorization_"
            "consumption_parallel_conflict"
        ),
    ),
    (
        {
            **valid_facts,
            "consumedAt": "2026-07-24T10:05:00Z",
        },
        "blocked",
        (
            "materialization_authorization_"
            "consumption_expired"
        ),
    ),
    (
        valid_facts,
        "consumption_ready_execution_locked",
        (
            "materialization_authorization_"
            "consumption_ready_execution_locked"
        ),
    ),
]

for facts, expected_status, expected_reason in cases:
    before = clone(facts) if isinstance(facts, dict) else facts
    first = evaluate(facts)
    second = evaluate(facts)

    if first != second:
        fail("Verbrauchs-Readiness ist nicht deterministisch.")

    if isinstance(facts, dict) and facts != before:
        fail("Verbrauchs-Readiness verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Readiness-Status ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Readiness-Grund ist ungültig: {first}")

    for key in (
        "authorizationConsumptionAllowed",
        "authorizationConsumed",
        "authorizationGranted",
        "authorizationTokenGenerated",
        "registryReadAllowed",
        "registryWriteAllowed",
        "atomicCompareAndSetAllowed",
        "trustedClockReadAllowed",
        "environmentCreationAllowed",
        "filesystemReadAllowed",
        "filesystemMutationAllowed",
        "processExecutionAllowed",
        "dependencyInstallationAllowed",
    ):
        if first.get(key) is not False:
            fail(f"Readiness-Ausführungsgrenze ist offen: {key}")

result = evaluate(valid_facts)
readiness = result.get("readiness")

if not isinstance(readiness, dict):
    fail("Gültiger Readiness-State fehlt.")
if readiness.get("registryState") != "unused":
    fail("Readiness-Registryzustand ist ungültig.")
if readiness.get("compareState") != "unused":
    fail("Readiness-Compare-Zustand ist ungültig.")
if readiness.get("setState") != "consumed":
    fail("Readiness-Set-Zustand ist ungültig.")
if readiness.get("singleUse") is not True:
    fail("Readiness-Einmalverwendung fehlt.")
if readiness.get("executionGrant") is not False:
    fail("Readiness darf keine Freigabe enthalten.")
if readiness.get("requestNonceFingerprint") == nonce:
    fail("Readiness darf Roh-Nonce nicht als Fingerprint verwenden.")

if list(MIGRATIONS.glob("*v2732p*.sql")):
    fail("v27.32p darf keine SQL-Migration erzeugen.")

print("Disposable Verbrauchs-Readiness-State: OK")
print("Quellvertrag: v27.32o")
print("Genehmigter Übergang: geprüft")
print("Request-, Nonce-, Akteur- und Planbindung: geprüft")
print("Zeitgrenze: nach Genehmigung und vor expiresAt")
print("Registryzustand: ausschließlich unused")
print("Ergebnis: consumption_ready_execution_locked")
print("Registry gelesen: nein")
print("Registry geschrieben: nein")
print("Compare-and-set ausgeführt: nein")
print("Verbrauch ausgeführt: nein")
print("Freigabe erteilt: nein")
print("Token erzeugt: nein")
print("Uhr gelesen: nein")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Virtuelle Umgebung erstellt: nein")
print("Dependency installiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32p: keine")
print("Produktive Freigabe: nein")
