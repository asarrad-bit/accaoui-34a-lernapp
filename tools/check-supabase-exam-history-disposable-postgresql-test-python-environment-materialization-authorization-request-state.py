from pathlib import Path
import ast
import base64
from datetime import datetime, timezone
import hashlib
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
        "authorization-request-state-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-request-contract.json"
    )
)
DESCRIPTOR = (
    ROOT
    / "tools"
    / "accaoui_disposable_test_python_environment_descriptor.py"
)
PLAN = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_plan.py"
    )
)
ACCEPTANCE = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_plan_acceptance_guard.py"
    )
)
STATE = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_request_state.py"
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
    "v27.32m-Autorisierungsanfrage-State-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32l-Autorisierungsanfrage-Vertrag",
)

if contract.get("version") != "v27.32m":
    fail("Anfrage-State-Vertrag besitzt nicht v27.32m.")
if contract.get("contractVersion") != 1:
    fail("Anfrage-State-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_request_state_execution_locked"
):
    fail("Anfrage-State-Status ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Anfrage-State darf nicht produktiv sein.")

if source.get("version") != "v27.32l":
    fail("Quellvertrag besitzt nicht v27.32l.")
if source.get("implementation", {}).get(
    "authorizationRequestBuilderImplemented"
) is not False:
    fail("Quellvertrag hatte unerwartet bereits einen Builder.")

implementation = contract.get("implementation", {})
if implementation.get(
    "authorizationRequestStateImplemented"
) is not True:
    fail("Autorisierungsanfrage-State fehlt.")

for key in (
    "randomSourceRead",
    "clockRead",
    "authorizationTokenGenerated",
    "authorizationGranted",
    "authorizationConsumed",
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
    "json",
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
    fail(f"Anfrage-State besitzt unerlaubte Importe: {unexpected_imports}")

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
        fail(f"Anfrage-State verwendet verbotenen Namen: {node.id}")

lower_source = state_source.lower()

for marker in (
    "uuid4(",
    "token_bytes(",
    "token_urlsafe(",
    "urandom(",
    "datetime.now(",
    "datetime.utcnow(",
    "time.time(",
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
        fail(f"Anfrage-State enthält verbotenen Inhalt: {marker}")

descriptor_module = load_module(
    DESCRIPTOR,
    "accaoui_descriptor_v2732m",
)
plan_module = load_module(
    PLAN,
    "accaoui_plan_v2732m",
)
acceptance_module = load_module(
    ACCEPTANCE,
    "accaoui_acceptance_v2732m",
)
state_module = load_module(
    STATE,
    "accaoui_authorization_request_state_v2732m",
)

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_test_python_environment_descriptor",
)
build_plan = getattr(
    plan_module,
    "build_test_python_environment_materialization_plan",
)
accept_plan = getattr(
    acceptance_module,
    "accept_test_python_environment_materialization_plan",
)
build_request = getattr(
    state_module,
    "build_materialization_authorization_request_state",
    None,
)

if not callable(build_request):
    fail("Autorisierungsanfrage-State-Funktion fehlt.")

descriptor_result = resolve_descriptor({
    "platform": "windows",
    "environmentRoot": r"D:\accaoui-test-envs\postgresql",
    "repositoryRoot": r"C:\xampp\htdocs\accaoui\v4-dashboard",
    "environmentRootKind": "dedicated_external",
    "invokingPythonVersion": "3.13",
    "requestedPythonVersion": "3.13",
    "includeSystemSitePackages": False,
    "allowUserSitePackages": False,
    "pythonNoUserSite": True,
    "inheritPythonPath": False,
    "inheritVirtualEnv": False,
})

plan_result = build_plan({
    "descriptorResult": descriptor_result,
    "basePythonExecutable": (
        r"C:\Users\tester\AppData\Local\Programs\Python"
        r"\Python313\python.exe"
    ),
    "targetState": "absent",
    "humanAuthorizationRecorded": False,
})

accepted_result = accept_plan(plan_result)

fingerprint = hashlib.sha256(
    json.dumps(
        accepted_result["acceptedPlan"],
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
).hexdigest()

nonce = base64.urlsafe_b64encode(bytes(range(32))).decode(
    "ascii"
).rstrip("=")

valid_facts = {
    "acceptedPlanResult": accepted_result,
    "requestId": "123e4567-e89b-42d3-a456-426614174000",
    "requestNonce": nonce,
    "actorId": "local-test-operator",
    "acceptedPlanFingerprint": fingerprint,
    "issuedAt": "2026-07-24T10:00:00Z",
    "expiresAt": "2026-07-24T10:05:00Z",
}

cases = [
    (
        [],
        "blocked",
        "materialization_authorization_request_invalid_input",
    ),
    (
        {
            key: value
            for key, value in valid_facts.items()
            if key != "requestId"
        },
        "blocked",
        "materialization_authorization_request_missing_fields",
    ),
    (
        {
            **valid_facts,
            "unexpected": True,
        },
        "blocked",
        "materialization_authorization_request_unknown_fields",
    ),
    (
        {
            **valid_facts,
            "requestId": "not-a-uuid",
        },
        "blocked",
        "materialization_authorization_identity_invalid",
    ),
    (
        {
            **valid_facts,
            "requestNonce": "short",
        },
        "blocked",
        "materialization_authorization_identity_invalid",
    ),
    (
        {
            **valid_facts,
            "actorId": " actor ",
        },
        "blocked",
        "materialization_authorization_identity_invalid",
    ),
    (
        {
            **valid_facts,
            "acceptedPlanFingerprint": "0" * 64,
        },
        "blocked",
        (
            "materialization_authorization_"
            "plan_fingerprint_invalid"
        ),
    ),
    (
        {
            **valid_facts,
            "expiresAt": "2026-07-24T10:04:59Z",
        },
        "blocked",
        "materialization_authorization_time_invalid",
    ),
    (
        valid_facts,
        "authorization_request_ready_locked",
        "materialization_authorization_request_ready_locked",
    ),
]

for facts, expected_status, expected_reason in cases:
    before = clone(facts) if isinstance(facts, dict) else facts
    first = build_request(facts)
    second = build_request(facts)

    if first != second:
        fail("Autorisierungsanfrage-State ist nicht deterministisch.")

    if isinstance(facts, dict) and facts != before:
        fail("Autorisierungsanfrage-State verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Anfragestatus ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Anfragegrund ist ungültig: {first}")

    for key in (
        "authorizationGranted",
        "authorizationTokenGenerated",
        "authorizationConsumed",
        "environmentCreationAllowed",
        "filesystemReadAllowed",
        "filesystemMutationAllowed",
        "processExecutionAllowed",
        "dependencyInstallationAllowed",
    ):
        if first.get(key) is not False:
            fail(f"Anfrage-Ausführungsgrenze ist offen: {key}")

result = build_request(valid_facts)
request = result.get("request")

if not isinstance(request, dict):
    fail("Gültige Autorisierungsanfrage fehlt.")

if request.get("status") != (
    "authorization_request_pending_locked"
):
    fail("Anfrage-Initialstatus ist ungültig.")
if request.get("executionGrant") is not False:
    fail("Anfrage darf keine Ausführungsfreigabe enthalten.")
if request.get("singleUse") is not True:
    fail("Anfrage ist nicht als einmalig markiert.")
if request.get("acceptedPlanFingerprint") != fingerprint:
    fail("Anfrage-Planfingerprint ist ungültig.")
if "acceptedPlan" in request:
    fail("Anfrage darf den Rohplan nicht enthalten.")
if result.get("authorizationRequestIssued") is not True:
    fail("Gültige Fakten müssen eine gesperrte Anfrage ergeben.")

if list(MIGRATIONS.glob("*v2732m*.sql")):
    fail("v27.32m darf keine SQL-Migration erzeugen.")

print("Disposable Autorisierungsanfrage-State: OK")
print("Quellvertrag: v27.32l")
print("Eingabe: ausschließlich übergebene Fakten")
print("UUID-v4-, Nonce- und Akteurprüfung: OK")
print("Planfingerprint: kanonisch geprüft")
print("Zeitfenster: exakt 300 Sekunden")
print("Zufallsquelle gelesen: nein")
print("Uhr gelesen: nein")
print("Ergebnis: authorization_request_ready_locked")
print("Requeststatus: authorization_request_pending_locked")
print("Freigabe erteilt: nein")
print("Token erzeugt: nein")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Virtuelle Umgebung erstellt: nein")
print("Dependency installiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32m: keine")
print("Produktive Freigabe: nein")
