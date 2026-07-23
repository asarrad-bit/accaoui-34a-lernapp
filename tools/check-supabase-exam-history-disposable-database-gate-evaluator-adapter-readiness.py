from pathlib import Path
import ast
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

GATE_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-disposable-database-environment-gate-contract.json"
)
HARNESS_READINESS_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-harness-readiness-contract.json"
)
READINESS_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-disposable-database-gate-"
      "evaluator-adapter-readiness-contract.json"
)
EVALUATOR_PATH = (
    ROOT
    / "tools"
    / "accaoui_disposable_environment_gate.py"
)
ADAPTER_STATE_PATH = (
    ROOT
    / "tools"
    / "accaoui_disposable_connection_adapter_readiness.py"
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


def read_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")

    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


def load_module(path: Path, module_name: str):
    if not path.is_file():
        fail(f"Python-Modul fehlt: {path}")

    spec = importlib.util.spec_from_file_location(
        module_name,
        path,
    )
    if spec is None or spec.loader is None:
        fail(f"Python-Modul ist nicht ladbar: {path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contract = read_json(
    READINESS_CONTRACT_PATH,
    "Gate-Evaluator-/Adapter-Readiness-Vertrag",
)

if contract.get("version") != "v27.32a":
    fail("Readiness-Vertrag besitzt nicht v27.32a.")
if contract.get("contractVersion") != 1:
    fail("Readiness-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_connection_free_not_live"
):
    fail("Readiness-Vertrag besitzt falschen Status.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Readiness-Vertrag darf nicht produktiv sein.")

implementation = contract.get("implementation", {})
if implementation != {
    "sourceGateContractPath": (
        "docs/contracts/"
        "exam-history-disposable-database-"
        "environment-gate-contract.json"
    ),
    "harnessReadinessContractPath": (
        "docs/contracts/"
        "exam-history-outer-domain-mutation-"
        "harness-readiness-contract.json"
    ),
    "evaluatorPath": (
        "tools/accaoui_disposable_environment_gate.py"
    ),
    "adapterReadinessPath": (
        "tools/"
        "accaoui_disposable_connection_adapter_readiness.py"
    ),
    "checkerPath": (
        "tools/"
        "check-supabase-exam-history-disposable-database-"
        "gate-evaluator-adapter-readiness.py"
    ),
    "documentPath": (
        "docs/"
        "SUPABASE_EXAM_RESULT_HISTORY_"
        "DISPOSABLE_DATABASE_GATE_EVALUATOR_"
        "ADAPTER_READINESS.md"
    ),
    "environmentGateEvaluatorImplemented": True,
    "connectionAdapterReadinessStateImplemented": True,
    "harnessIntegrationImplemented": False,
    "databaseDriverPresent": False,
    "databaseConnectionCreated": False,
    "databaseTestExecuted": False,
    "sqlMigrationCreated": False,
    "frontendIntegration": False,
}:
    fail("Readiness-Implementierungsgrenze ist ungültig.")

expected_input_keys = [
    "ACCAOUI_DB_TEST_MODE",
    "ACCAOUI_DB_TEST_TARGET_KIND",
    "ACCAOUI_DB_TEST_HOST",
    "ACCAOUI_DB_TEST_PORT",
    "ACCAOUI_DB_TEST_DATABASE",
    "ACCAOUI_DB_TEST_CONFIRM",
]

if contract.get("evaluatorBoundary") != {
    "inputType": "mapping",
    "readsProcessEnvironmentDirectly": False,
    "allowedInputKeys": expected_input_keys,
    "unknownInputKeyDecision": "deny",
    "missingInputDecision": "deny",
    "defaultDecision": "deny",
    "dnsResolutionAllowed": False,
    "ipResolutionAllowed": False,
    "networkExecutionAllowed": False,
    "databaseDriverImportAllowed": False,
    "connectionOpenAllowed": False,
}:
    fail("Evaluatorgrenze ist ungültig.")

expected_decisions = {
    "noVariables": {
        "decision": "deny",
        "reason": "environment_gate_not_configured",
    },
    "modeOnly": {
        "decision": "deny",
        "reason": "environment_gate_incomplete",
    },
    "unknownField": {
        "decision": "deny",
        "reason": "unknown_environment_field",
    },
    "invalidMode": {
        "decision": "deny",
        "reason": "environment_mode_invalid",
    },
    "invalidTargetKind": {
        "decision": "deny",
        "reason": "target_kind_invalid",
    },
    "remoteHost": {
        "decision": "deny",
        "reason": "remote_target_forbidden",
    },
    "unknownHost": {
        "decision": "deny",
        "reason": "unknown_target_forbidden",
    },
    "forbiddenDatabaseName": {
        "decision": "deny",
        "reason": "protected_database_forbidden",
    },
    "invalidPort": {
        "decision": "deny",
        "reason": "invalid_local_port",
    },
    "confirmationMismatch": {
        "decision": "deny",
        "reason": "destructive_confirmation_required",
    },
    "urlOrConnectionString": {
        "decision": "deny",
        "reason": "connection_string_forbidden",
    },
    "completeLoopbackDescriptor": {
        "decision": "eligible_but_connection_locked",
        "reason": "adapter_not_implemented",
    },
}
if contract.get("decisionMatrix") != expected_decisions:
    fail("Evaluator-Entscheidungsmatrix ist ungültig.")

if contract.get("canonicalEligibleDescriptor") != {
    "mode": "disposable",
    "targetKind": "local_postgres",
    "host": "localhost",
    "port": 5432,
    "database": "accaoui_exam_history_disposable_test",
}:
    fail("Kanonischer lokaler Descriptor ist ungültig.")

if contract.get("adapterReadinessBoundary") != {
    "inputType": "evaluated_gate_result_only",
    "readsProcessEnvironmentDirectly": False,
    "acceptsRawConnectionParameters": False,
    "eligibleStatus": "descriptor_valid_connection_locked",
    "eligibleReason": "database_driver_not_selected",
    "deniedStatus": "blocked",
    "driverSelected": False,
    "connectionAllowed": False,
    "connectionCreated": False,
    "returnsConnection": False,
    "importsDatabaseDriver": False,
    "opensSocket": False,
    "appliesMigrations": False,
    "executesTests": False,
}:
    fail("Adapter-Readiness-Grenze ist ungültig.")

if contract.get("determinismBoundary") != {
    "sameInputSameResult": True,
    "inputMutationAllowed": False,
    "normalizesHostLowercase": True,
    "trimsTrailingHostDot": True,
    "normalizesDatabaseLowercase": True,
    "confirmationReturnedToAdapter": False,
}:
    fail("Determinismusgrenze ist ungültig.")

if contract.get("securityBoundary") != {
    "realParticipantDataAllowed": False,
    "realEmailAddressAllowed": False,
    "realNameAllowed": False,
    "productionSecretsAllowed": False,
    "databaseUrlStoredAllowed": False,
    "serviceRoleKeyStoredAllowed": False,
    "passwordInputAllowed": False,
    "networkExecutionAllowed": False,
    "frontendReferenceAllowed": False,
    "clientSelectableTargetAllowed": False,
    "clientSelectableFaultInjectionAllowed": False,
}:
    fail("Readiness-Sicherheitsgrenze ist ungültig.")

if contract.get("unresolvedRequirements") != {
    "harnessGateIntegration": True,
    "databaseDriverSelection": True,
    "databaseConnectionImplementation": True,
    "testOnlyFaultInjectionImplementation": True,
    "databaseTestExecution": True,
    "concurrencyTestExecution": True,
    "authorizationTestExecution": True,
    "directAppExecutionGrant": True,
    "frontendIntegration": True,
}:
    fail("Offene Readiness-Anforderungen sind ungültig.")

gate_contract = read_json(
    GATE_CONTRACT_PATH,
    "v27.31z-Umgebungs-Gate-Vertrag",
)
if gate_contract.get("version") != "v27.31z":
    fail("Quell-Gate-Vertrag besitzt nicht v27.31z.")
if gate_contract.get("productiveReleaseAllowed") is not False:
    fail("Quell-Gate-Vertrag ist unerwartet produktiv.")

harness_readiness = read_json(
    HARNESS_READINESS_CONTRACT_PATH,
    "v27.31y-Harness-Readiness-Vertrag",
)
if harness_readiness.get("version") != "v27.31y":
    fail("Harness-Readiness-Vertrag besitzt nicht v27.31y.")
if harness_readiness.get("implementation", {}).get(
    "databaseConnectionCreated"
) is not False:
    fail("Harness hat unerwartet eine Verbindung erstellt.")

evaluator = load_module(
    EVALUATOR_PATH,
    "accaoui_disposable_environment_gate_v2732a",
)
adapter_state = load_module(
    ADAPTER_STATE_PATH,
    "accaoui_disposable_connection_adapter_readiness_v2732a",
)

evaluate = getattr(evaluator, "evaluate_environment", None)
build_readiness = getattr(
    adapter_state,
    "build_connection_adapter_readiness",
    None,
)
if not callable(evaluate):
    fail("Gate-Evaluator-Funktion fehlt.")
if not callable(build_readiness):
    fail("Adapter-Readiness-Funktion fehlt.")

valid_environment = {
    "ACCAOUI_DB_TEST_MODE": "disposable",
    "ACCAOUI_DB_TEST_TARGET_KIND": "local_postgres",
    "ACCAOUI_DB_TEST_HOST": "LOCALHOST.",
    "ACCAOUI_DB_TEST_PORT": "5432",
    "ACCAOUI_DB_TEST_DATABASE": (
        "ACCAOUI_EXAM_HISTORY_DISPOSABLE_TEST"
    ),
    "ACCAOUI_DB_TEST_CONFIRM": "DESTROY_SYNTHETIC_TEST_DATA",
}

cases = [
    (
        "noVariables",
        {},
    ),
    (
        "modeOnly",
        {
            "ACCAOUI_DB_TEST_MODE": "disposable",
        },
    ),
    (
        "unknownField",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_UNKNOWN": "x",
        },
    ),
    (
        "invalidMode",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_MODE": "live",
        },
    ),
    (
        "invalidTargetKind",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_TARGET_KIND": "remote_postgres",
        },
    ),
    (
        "remoteHost",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_HOST": "db.supabase.co",
        },
    ),
    (
        "unknownHost",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_HOST": "internal-db",
        },
    ),
    (
        "forbiddenDatabaseName",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_DATABASE": "postgres",
        },
    ),
    (
        "invalidPort",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_PORT": "80",
        },
    ),
    (
        "confirmationMismatch",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_CONFIRM": "YES",
        },
    ),
    (
        "urlOrConnectionString",
        {
            **valid_environment,
            "ACCAOUI_DB_TEST_HOST": "postgresql://localhost",
        },
    ),
    (
        "completeLoopbackDescriptor",
        valid_environment,
    ),
]

for case_name, case_input in cases:
    snapshot = dict(case_input)
    first = evaluate(case_input)
    second = evaluate(case_input)

    if case_input != snapshot:
        fail(f"Evaluator verändert Eingabe: {case_name}")
    if first != second:
        fail(f"Evaluator ist nicht deterministisch: {case_name}")

    expected = expected_decisions[case_name]
    if first.get("decision") != expected["decision"]:
        fail(f"Falsche Entscheidung: {case_name}: {first}")
    if first.get("reason") != expected["reason"]:
        fail(f"Falscher Grund: {case_name}: {first}")
    if first.get("connectionAllowed") is not False:
        fail(f"Verbindung unerwartet erlaubt: {case_name}")

    readiness = build_readiness(first)

    if expected["decision"] == "deny":
        if readiness != {
            "status": "blocked",
            "reason": expected["reason"],
            "descriptor": None,
            "driverSelected": False,
            "connectionAllowed": False,
            "connectionCreated": False,
        }:
            fail(
                f"Denied-Adapterstatus ist ungültig: "
                f"{case_name}: {readiness}"
            )
    else:
        if first.get("descriptor") != {
            "mode": "disposable",
            "targetKind": "local_postgres",
            "host": "localhost",
            "port": 5432,
            "database": "accaoui_exam_history_disposable_test",
        }:
            fail(f"Normalisierter Descriptor ist ungültig: {first}")

        if "ACCAOUI_DB_TEST_CONFIRM" in first["descriptor"]:
            fail("Bestätigung wird unerwartet weitergegeben.")

        if readiness != {
            "status": "descriptor_valid_connection_locked",
            "reason": "database_driver_not_selected",
            "descriptor": first["descriptor"],
            "driverSelected": False,
            "connectionAllowed": False,
            "connectionCreated": False,
        }:
            fail(f"Eligible-Adapterstatus ist ungültig: {readiness}")

allowed_imports = {
    "__future__",
    "collections",
    "typing",
}

for module_path in (
    EVALUATOR_PATH,
    ADAPTER_STATE_PATH,
):
    source = module_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        fail(f"Readiness-Modul besitzt Syntaxfehler: {exc}")

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
            f"Readiness-Modul besitzt unerlaubte Importe: "
            f"{module_path.name}: {unexpected_imports}"
        )

    lower_source = source.lower()
    for forbidden_marker in (
        "psycopg",
        "asyncpg",
        "requests",
        "urllib",
        "http.client",
        "socket",
        "subprocess",
        ".connect(",
        "create_connection",
        "getaddrinfo",
        "postgres://",
        "postgresql://",
        "supabase.co",
        "service_role",
        "database_url",
        "password",
    ):
        if forbidden_marker in lower_source:
            fail(
                "Readiness-Modul enthält verbotenen Inhalt: "
                f"{module_path.name}: {forbidden_marker}"
            )

serialized = json.dumps(contract, ensure_ascii=False).lower()
for forbidden_marker in (
    "postgres://",
    "postgresql://",
    "eyj",
    "service_role",
    '"password"',
    '"secret"',
    '"token"',
    '"participant_id"',
    '"email"',
):
    if forbidden_marker in serialized:
        fail(
            "Readiness-Vertrag enthält verbotenen Inhalt: "
            f"{forbidden_marker}"
        )

v2732a_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2732a*.sql")
)
if v2732a_sql_files:
    fail(
        "v27.32a darf keine SQL-Migration erzeugen: "
        f"{v2732a_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend = frontend_path.read_text(encoding="utf-8").lower()

    for forbidden_reference in (
        EVALUATOR_PATH.name.lower(),
        ADAPTER_STATE_PATH.name.lower(),
        READINESS_CONTRACT_PATH.name.lower(),
    ):
        if forbidden_reference in frontend:
            fail(
                "v27.32a-Readiness wird im Frontend referenziert: "
                f"{frontend_path.name}: {forbidden_reference}"
            )

print("Disposable Gate-Evaluator und Adapter-Readiness: OK")
print("Evaluator: deterministisch und verbindungsfrei")
print("Standardentscheidung: deny")
print("Loopback-Descriptor: normalisiert, aber Verbindung gesperrt")
print("Remote, unbekannt, unvollständig und produktiv: abgelehnt")
print("Adapterstatus: descriptor_valid_connection_locked")
print("Datenbanktreiber: keiner")
print("DNS/Netzwerk/Socket: keiner")
print("Datenbankverbindung: keine")
print("Datenbanktest ausgeführt: nein")
print("SQL-Migration v27.32a: keine")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
