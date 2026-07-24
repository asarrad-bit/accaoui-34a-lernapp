from pathlib import Path
import ast
import base64
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
        "authorization-request-transition-guard-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-request-state-contract.json"
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
REQUEST_STATE = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_request_state.py"
    )
)
TRANSITION_GUARD = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_authorization_request_transition_guard.py"
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
    "v27.32n-Autorisierungs-Transition-Guard-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32m-Autorisierungsanfrage-State-Vertrag",
)

if contract.get("version") != "v27.32n":
    fail("Transition-Guard-Vertrag besitzt nicht v27.32n.")
if contract.get("contractVersion") != 1:
    fail("Transition-Guard-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_transition_guard_execution_locked"
):
    fail("Transition-Guard-Status ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Transition-Guard darf nicht produktiv sein.")

if source.get("version") != "v27.32m":
    fail("Quellvertrag besitzt nicht v27.32m.")
if source.get("implementation", {}).get(
    "authorizationRequestStateImplemented"
) is not True:
    fail("Quell-Anfrage-State ist nicht implementiert.")

implementation = contract.get("implementation", {})
if implementation.get(
    "authorizationTransitionGuardImplemented"
) is not True:
    fail("Autorisierungs-Transition-Guard fehlt.")

for key in (
    "authorizationTokenGenerated",
    "authorizationGranted",
    "authorizationConsumed",
    "randomSourceRead",
    "clockRead",
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

transition = contract.get("transitionBoundary", {})
if transition.get("successStatus") != (
    "transition_applied_execution_locked"
):
    fail("Transition-Erfolgsstatus ist ungültig.")
if transition.get("approveTargetStatus") != (
    "authorization_request_approved_locked"
):
    fail("Genehmigungsziel ist ungültig.")
if transition.get("approvalStillExecutionLocked") is not True:
    fail("Genehmigung muss ausführungsgesperrt bleiben.")
if transition.get("executionGrant") is not False:
    fail("Transition darf keine Ausführungsfreigabe enthalten.")

source_code = TRANSITION_GUARD.read_text(encoding="utf-8")
tree = ast.parse(source_code)

allowed_imports = {
    "__future__",
    "collections",
    "datetime",
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
    fail(
        "Transition-Guard besitzt unerlaubte Importe: "
        f"{unexpected_imports}"
    )

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
        fail(
            "Transition-Guard verwendet verbotenen Namen: "
            f"{node.id}"
        )

lower_source = source_code.lower()

for marker in (
    "datetime.now(",
    "datetime.utcnow(",
    "time.time(",
    "uuid4(",
    "token_bytes(",
    "urandom(",
    "subprocess",
    "pip install",
    "python -m venv",
    "py -m venv",
    ".connect(",
    "postgres://",
    "postgresql://",
    "database_url",
    "service_role",
):
    if marker in lower_source:
        fail(f"Transition-Guard enthält verbotenen Inhalt: {marker}")

descriptor_module = load_module(
    DESCRIPTOR,
    "accaoui_descriptor_v2732n",
)
plan_module = load_module(
    PLAN,
    "accaoui_plan_v2732n",
)
acceptance_module = load_module(
    ACCEPTANCE,
    "accaoui_acceptance_v2732n",
)
request_module = load_module(
    REQUEST_STATE,
    "accaoui_request_state_v2732n",
)
transition_module = load_module(
    TRANSITION_GUARD,
    "accaoui_transition_guard_v2732n",
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
    request_module,
    "build_materialization_authorization_request_state",
)
apply_transition = getattr(
    transition_module,
    "transition_materialization_authorization_request",
    None,
)

if not callable(apply_transition):
    fail("Autorisierungs-Transition-Guard-Funktion fehlt.")

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
request_state = build_request({
    "acceptedPlanResult": accepted_result,
    "requestId": "123e4567-e89b-42d3-a456-426614174000",
    "requestNonce": nonce,
    "actorId": "local-test-operator",
    "acceptedPlanFingerprint": fingerprint,
    "issuedAt": "2026-07-24T10:00:00Z",
    "expiresAt": "2026-07-24T10:05:00Z",
})

valid_approve = {
    "requestStateResult": request_state,
    "decision": "approve",
    "evaluatedAt": "2026-07-24T10:02:00Z",
}

cases = [
    (
        [],
        "blocked",
        "materialization_authorization_transition_invalid_input",
    ),
    (
        {
            key: value
            for key, value in valid_approve.items()
            if key != "decision"
        },
        "blocked",
        "materialization_authorization_transition_missing_fields",
    ),
    (
        {
            **valid_approve,
            "unexpected": True,
        },
        "blocked",
        "materialization_authorization_transition_unknown_fields",
    ),
    (
        {
            **valid_approve,
            "decision": "execute",
        },
        "blocked",
        "materialization_authorization_transition_decision_invalid",
    ),
    (
        {
            **valid_approve,
            "evaluatedAt": "2026-07-24T09:59:59Z",
        },
        "blocked",
        "materialization_authorization_transition_time_invalid",
    ),
    (
        valid_approve,
        "transition_applied_execution_locked",
        "materialization_authorization_request_approved_locked",
    ),
    (
        {
            **valid_approve,
            "decision": "reject",
        },
        "transition_applied_execution_locked",
        "materialization_authorization_request_rejected",
    ),
    (
        {
            **valid_approve,
            "decision": "revoke",
        },
        "transition_applied_execution_locked",
        "materialization_authorization_request_revoked",
    ),
    (
        {
            **valid_approve,
            "decision": "approve",
            "evaluatedAt": "2026-07-24T10:05:00Z",
        },
        "transition_applied_execution_locked",
        "materialization_authorization_request_expired",
    ),
]

for facts, expected_status, expected_reason in cases:
    before = clone(facts) if isinstance(facts, dict) else facts
    first = apply_transition(facts)
    second = apply_transition(facts)

    if first != second:
        fail("Autorisierungs-Transition ist nicht deterministisch.")

    if isinstance(facts, dict) and facts != before:
        fail("Autorisierungs-Transition verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Transition-Status ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Transition-Grund ist ungültig: {first}")

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
            fail(f"Transition-Ausführungsgrenze ist offen: {key}")

expected_targets = {
    "approve": (
        "authorization_request_approved_locked",
        False,
    ),
    "reject": (
        "authorization_request_rejected",
        True,
    ),
    "revoke": (
        "authorization_request_revoked",
        True,
    ),
}

for decision, (target_status, terminal) in expected_targets.items():
    result = apply_transition({
        **valid_approve,
        "decision": decision,
    })
    transitioned_request = result.get("transitionedRequest")
    transition_data = result.get("transition")

    if not isinstance(transitioned_request, dict):
        fail("Transitionierte Anfrage fehlt.")
    if not isinstance(transition_data, dict):
        fail("Transition-Metadaten fehlen.")
    if transitioned_request.get("status") != target_status:
        fail("Transition-Zielstatus ist ungültig.")
    if transitioned_request.get("executionGrant") is not False:
        fail("Transitionierte Anfrage darf keine Freigabe enthalten.")
    if transition_data.get("terminal") is not terminal:
        fail("Transition-Terminalgrenze ist ungültig.")
    if transition_data.get("executionGrant") is not False:
        fail("Transition darf keine Freigabe enthalten.")

expired = apply_transition({
    **valid_approve,
    "decision": "approve",
    "evaluatedAt": "2026-07-24T10:05:00Z",
})

if expired.get("transition", {}).get("effectiveDecision") != "expire":
    fail("Ablauf muss Entscheidung übersteuern.")
if expired.get("transition", {}).get("terminal") is not True:
    fail("Ablauf muss terminal sein.")

if list(MIGRATIONS.glob("*v2732n*.sql")):
    fail("v27.32n darf keine SQL-Migration erzeugen.")

print("Disposable Autorisierungs-Transition-Guard: OK")
print("Quellvertrag: v27.32m")
print("Eingabe: Anfrage-, Entscheidungs- und Zeitfakten")
print("Genehmigung: approved_locked")
print("Ablehnung: terminal")
print("Ablauf: terminal und mit Vorrang")
print("Widerruf: terminal")
print("Zufallsquelle gelesen: nein")
print("Uhr gelesen: nein")
print("Freigabe erteilt: nein")
print("Token erzeugt: nein")
print("Verbrauch ausgeführt: nein")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Virtuelle Umgebung erstellt: nein")
print("Dependency installiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32n: keine")
print("Produktive Freigabe: nein")
