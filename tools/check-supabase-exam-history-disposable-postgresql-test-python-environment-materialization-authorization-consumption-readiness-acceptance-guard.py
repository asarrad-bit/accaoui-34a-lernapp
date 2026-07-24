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
        "authorization-consumption-readiness-"
        "acceptance-guard-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-consumption-readiness-contract.json"
    )
)
SOURCE_STATE = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_consumption_readiness.py"
    )
)
GUARD = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_consumption_"
        "readiness_acceptance_guard.py"
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
    "v27.32q-Readiness-Annahmevertrag",
)
source = load_json(
    SOURCE,
    "v27.32p-Verbrauchs-Readiness-Vertrag",
)

if contract.get("version") != "v27.32q":
    fail("Annahmevertrag besitzt nicht v27.32q.")
if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_readiness_acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Annahmevertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32p":
    fail("Quellvertrag besitzt nicht v27.32p.")
if source.get("implementation", {}).get(
    "authorizationConsumptionReadinessImplemented"
) is not True:
    fail("Quell-Readiness-State ist nicht implementiert.")
if source.get("successBoundary", {}).get("status") != (
    "consumption_ready_execution_locked"
):
    fail("Quell-Readiness besitzt falschen Erfolgsstatus.")

implementation = contract.get("implementation", {})

if implementation.get(
    "consumptionReadinessAcceptanceGuardImplemented"
) is not True:
    fail("Readiness-Annahme-Guard fehlt.")

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

guard_source = GUARD.read_text(encoding="utf-8")
tree = ast.parse(guard_source)

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
    fail(f"Annahme-Guard besitzt unerlaubte Importe: {unexpected_imports}")

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
        fail(f"Annahme-Guard verwendet verbotenen Namen: {node.id}")

lower_source = guard_source.lower()

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
        fail(f"Annahme-Guard enthält verbotenen Inhalt: {marker}")

source_module = load_module(
    SOURCE_STATE,
    "accaoui_consumption_readiness_source_v2732q",
)
guard_module = load_module(
    GUARD,
    "accaoui_consumption_readiness_acceptance_v2732q",
)

evaluate = getattr(
    source_module,
    "evaluate_materialization_authorization_consumption_readiness",
    None,
)
accept = getattr(
    guard_module,
    "accept_materialization_authorization_consumption_readiness",
    None,
)

if not callable(evaluate):
    fail("Quell-Readiness-Funktion fehlt.")
if not callable(accept):
    fail("Readiness-Annahme-Funktion fehlt.")

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

transition_result = {
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

source_result = evaluate({
    "transitionResult": transition_result,
    "requestId": request["requestId"],
    "requestNonce": request["requestNonce"],
    "acceptedPlanFingerprint": request[
        "acceptedPlanFingerprint"
    ],
    "actor": request["actor"],
    "purpose": request["purpose"],
    "consumedAt": "2026-07-24T10:02:00Z",
    "registryState": "unused",
})

tampered_status = clone(source_result)
tampered_status["status"] = "ready"

tampered_flag = clone(source_result)
tampered_flag["registryWriteAllowed"] = True

tampered_extra = clone(source_result)
tampered_extra["readiness"]["unexpected"] = True

tampered_request = clone(source_result)
tampered_request["readiness"]["requestId"] = (
    "123e4567-e89b-42d3-a456-426614174001"
)

tampered_nonce_fingerprint = clone(source_result)
tampered_nonce_fingerprint["readiness"][
    "requestNonceFingerprint"
] = "0" * 64

tampered_plan = clone(source_result)
tampered_plan["readiness"]["registryKey"][
    "acceptedPlanFingerprint"
] = "b" * 64

tampered_actor = clone(source_result)
tampered_actor["readiness"]["actor"]["kind"] = "automatic"

tampered_time = clone(source_result)
tampered_time["readiness"]["consumedAt"] = (
    "2026-07-24T10:05:00Z"
)

tampered_registry = clone(source_result)
tampered_registry["readiness"]["registryState"] = "consumed"

tampered_compare = clone(source_result)
tampered_compare["readiness"]["compareState"] = "consumed"

tampered_grant = clone(source_result)
tampered_grant["readiness"]["executionGrant"] = True

cases = [
    (
        [],
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_invalid_input"
        ),
    ),
    (
        tampered_status,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_source_status_invalid"
        ),
    ),
    (
        tampered_flag,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_boundary_open"
        ),
    ),
    (
        tampered_extra,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_readiness_structure_invalid"
        ),
    ),
    (
        tampered_request,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_registry_invalid"
        ),
    ),
    (
        tampered_nonce_fingerprint,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_registry_invalid"
        ),
    ),
    (
        tampered_plan,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_registry_invalid"
        ),
    ),
    (
        tampered_actor,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_binding_invalid"
        ),
    ),
    (
        tampered_time,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_time_invalid"
        ),
    ),
    (
        tampered_registry,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_registry_invalid"
        ),
    ),
    (
        tampered_compare,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_registry_invalid"
        ),
    ),
    (
        tampered_grant,
        "blocked",
        (
            "materialization_authorization_consumption_"
            "readiness_acceptance_lock_invalid"
        ),
    ),
    (
        source_result,
        "accepted_consumption_ready_execution_locked",
        (
            "materialization_authorization_consumption_"
            "readiness_accepted_execution_locked"
        ),
    ),
]

for candidate, expected_status, expected_reason in cases:
    before = clone(candidate) if isinstance(candidate, dict) else candidate
    first = accept(candidate)
    second = accept(candidate)

    if first != second:
        fail("Readiness-Annahme ist nicht deterministisch.")

    if isinstance(candidate, dict) and candidate != before:
        fail("Readiness-Annahme verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Annahmestatus ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Annahmegrund ist ungültig: {first}")

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
            fail(f"Annahme-Ausführungsgrenze ist offen: {key}")

accepted_result = accept(source_result)

if accepted_result.get("accepted") is not True:
    fail("Gültiger Readiness-State wurde nicht angenommen.")

accepted_readiness = accepted_result.get("acceptedReadiness")

if not isinstance(accepted_readiness, dict):
    fail("Angenommene Readiness fehlt.")

if accepted_readiness != source_result["readiness"]:
    fail("Angenommene Readiness weicht von Quelle ab.")

if accepted_readiness is source_result["readiness"]:
    fail("Annahme-Guard darf keine Quellreferenz zurückgeben.")

if (
    accepted_readiness["actor"]
    is source_result["readiness"]["actor"]
):
    fail("Akteur muss kanonisch kopiert werden.")

if (
    accepted_readiness["registryKey"]
    is source_result["readiness"]["registryKey"]
):
    fail("Registry-Key muss kanonisch kopiert werden.")

if list(MIGRATIONS.glob("*v2732q*.sql")):
    fail("v27.32q darf keine SQL-Migration erzeugen.")

print("Disposable Verbrauchs-Readiness-Annahme-Guard: OK")
print("Quellvertrag: v27.32p")
print("Quellstatus: consumption_ready_execution_locked")
print("Struktur- und Sperrfeldprüfung: vollständig")
print("Request-, Nonce-, Akteur- und Planbindung: geprüft")
print("Zeitfenster und Registry-Key: geprüft")
print("Compare-/Set-Zustände: unused -> consumed")
print("Ergebnis: accepted_consumption_ready_execution_locked")
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
print("SQL-Migration v27.32q: keine")
print("Produktive Freigabe: nein")
