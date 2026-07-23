from pathlib import Path
import ast
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-disposable-database-environment-gate-contract.json"
)
READINESS_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-harness-readiness-contract.json"
)
DATABASE_TEST_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-database-test-contract.json"
)
HARNESS_PATH = (
    ROOT
    / "tools"
    / "run-supabase-exam-history-outer-domain-mutation-harness.py"
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


contract = read_json(
    CONTRACT_PATH,
    "Disposable Datenbank-Umgebungs-Gate-Vertrag",
)

if contract.get("version") != "v27.31z":
    fail("Umgebungs-Gate-Vertrag besitzt nicht v27.31z.")
if contract.get("contractVersion") != 1:
    fail("Umgebungs-Gate-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != "prepared_locked_not_live":
    fail("Umgebungs-Gate-Vertrag ist nicht gesperrt vorbereitet.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Umgebungs-Gate-Vertrag darf nicht produktiv sein.")

implementation = contract.get("implementation", {})
if implementation != {
    "harnessReadinessContractPath": (
        "docs/contracts/"
        "exam-history-outer-domain-mutation-"
        "harness-readiness-contract.json"
    ),
    "databaseTestContractPath": (
        "docs/contracts/"
        "exam-history-outer-domain-mutation-"
        "database-test-contract.json"
    ),
    "harnessPath": (
        "tools/"
        "run-supabase-exam-history-"
        "outer-domain-mutation-harness.py"
    ),
    "checkerPath": (
        "tools/"
        "check-supabase-exam-history-disposable-"
        "database-environment-gate-contract.py"
    ),
    "documentPath": (
        "docs/"
        "SUPABASE_EXAM_RESULT_HISTORY_"
        "DISPOSABLE_DATABASE_ENVIRONMENT_GATE_CONTRACT.md"
    ),
    "environmentGateImplemented": False,
    "databaseConnectionAdapterImplemented": False,
    "databaseDriverPresent": False,
    "databaseConnectionCreated": False,
    "databaseTestExecuted": False,
    "sqlMigrationCreated": False,
    "frontendIntegration": False,
}:
    fail("Umgebungs-Gate-Implementierungsgrenze ist ungültig.")

required = contract.get("requiredEnvironment", {})
if required != {
    "modeVariable": "ACCAOUI_DB_TEST_MODE",
    "modeValue": "disposable",
    "targetKindVariable": "ACCAOUI_DB_TEST_TARGET_KIND",
    "targetKindValue": "local_postgres",
    "hostVariable": "ACCAOUI_DB_TEST_HOST",
    "portVariable": "ACCAOUI_DB_TEST_PORT",
    "databaseVariable": "ACCAOUI_DB_TEST_DATABASE",
    "confirmationVariable": "ACCAOUI_DB_TEST_CONFIRM",
    "confirmationValue": "DESTROY_SYNTHETIC_TEST_DATA",
    "allFieldsRequired": True,
    "missingFieldDecision": "deny",
    "unknownFieldDecision": "deny",
}:
    fail("Pflichtumgebungsgrenze ist ungültig.")

classification = contract.get("targetClassification", {})
if classification != {
    "allowedHosts": [
        "127.0.0.1",
        "localhost",
        "::1",
    ],
    "hostnameNormalization": "lowercase_trim_trailing_dot",
    "loopbackOnly": True,
    "dnsResolutionAllowed": False,
    "ipResolutionAllowed": False,
    "allowedDatabaseName": (
        "accaoui_exam_history_disposable_test"
    ),
    "portMinimum": 1024,
    "portMaximum": 65535,
    "urlInputAllowed": False,
    "connectionStringInputAllowed": False,
    "remoteAddressAllowed": False,
    "productionTargetAllowed": False,
    "unknownTargetAllowed": False,
}:
    fail("Zielklassifikationsgrenze ist ungültig.")

forbidden = contract.get("forbiddenTargets", {})
if forbidden != {
    "databaseNames": [
        "postgres",
        "template0",
        "template1",
        "production",
        "prod",
        "main",
        "default",
    ],
    "hostnameSuffixes": [
        ".supabase.co",
        ".supabase.com",
        ".amazonaws.com",
        ".azure.com",
        ".googleusercontent.com",
    ],
    "hostTokens": [
        "prod",
        "production",
        "live",
        "remote",
        "cloud",
    ],
    "databaseTokens": [
        "prod",
        "production",
        "live",
        "customer",
        "participant",
    ],
}:
    fail("Verbotene Zielklassifikation ist ungültig.")

expected_decisions = {
    "noVariables": {
        "decision": "deny",
        "reason": "environment_gate_not_configured",
    },
    "modeOnly": {
        "decision": "deny",
        "reason": "environment_gate_incomplete",
    },
    "completeLoopbackDescriptor": {
        "decision": "eligible_but_connection_locked",
        "reason": "adapter_not_implemented",
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
}
if contract.get("decisionMatrix") != expected_decisions:
    fail("Umgebungs-Gate-Entscheidungsmatrix ist ungültig.")

adapter = contract.get("connectionAdapterBoundary", {})
if adapter != {
    "adapterPurpose": (
        "future_disposable_local_postgres_test_connection"
    ),
    "inputSource": "validated_gate_descriptor_only",
    "readsRawProcessEnvironmentDirectly": False,
    "acceptsUrl": False,
    "acceptsConnectionString": False,
    "acceptsPassword": False,
    "acceptsServiceRoleKey": False,
    "acceptsProductionSecret": False,
    "performsDnsLookup": False,
    "opensSocket": False,
    "importsDatabaseDriver": False,
    "appliesMigrations": False,
    "executesTests": False,
    "returnsConnection": False,
    "defaultDecision": "deny",
}:
    fail("Datenbank-Verbindungsadaptergrenze ist ungültig.")

security = contract.get("securityBoundary", {})
if security != {
    "realParticipantDataAllowed": False,
    "realEmailAddressAllowed": False,
    "realNameAllowed": False,
    "productionSecretsAllowed": False,
    "databaseUrlStoredAllowed": False,
    "serviceRoleKeyStoredAllowed": False,
    "networkExecutionAllowed": False,
    "frontendReferenceAllowed": False,
    "clientSelectableTargetAllowed": False,
    "clientSelectableFaultInjectionAllowed": False,
}:
    fail("Umgebungs-Gate-Sicherheitsgrenze ist ungültig.")

if contract.get("unresolvedRequirements") != {
    "environmentGateImplementation": True,
    "connectionAdapterReadinessState": True,
    "databaseDriverSelection": True,
    "databaseConnectionImplementation": True,
    "testOnlyFaultInjectionImplementation": True,
    "databaseTestExecution": True,
    "concurrencyTestExecution": True,
    "authorizationTestExecution": True,
    "directAppExecutionGrant": True,
    "frontendIntegration": True,
}:
    fail("Offene Umgebungs-Gate-Anforderungen sind ungültig.")

readiness = read_json(
    READINESS_CONTRACT_PATH,
    "v27.31y-Harness-Readiness-Vertrag",
)
if readiness.get("version") != "v27.31y":
    fail("Harness-Readiness-Vertrag besitzt nicht v27.31y.")
if readiness.get("productiveReleaseAllowed") is not False:
    fail("Harness-Readiness ist unerwartet produktiv.")
if readiness.get("implementation", {}).get(
    "databaseConnectionCreated"
) is not False:
    fail("Harness hat unerwartet eine Datenbankverbindung erstellt.")
if readiness.get("implementation", {}).get(
    "databaseDriverPresent"
) is not False:
    fail("Harness besitzt unerwartet einen Datenbanktreiber.")

database_test = read_json(
    DATABASE_TEST_CONTRACT_PATH,
    "v27.31w-Datenbank-Testvertrag",
)
if database_test.get("version") != "v27.31w":
    fail("Datenbank-Testvertrag besitzt nicht v27.31w.")
if database_test.get("productiveReleaseAllowed") is not False:
    fail("Datenbank-Testvertrag ist unerwartet produktiv.")

if not HARNESS_PATH.is_file():
    fail("v27.31y-Harness-Gerüst fehlt.")

harness_source = HARNESS_PATH.read_text(encoding="utf-8")
try:
    harness_tree = ast.parse(harness_source)
except SyntaxError as exc:
    fail(f"Harness-Gerüst besitzt Syntaxfehler: {exc}")

allowed_imports = {
    "__future__",
    "argparse",
    "hashlib",
    "json",
    "os",
    "re",
    "sys",
    "uuid",
    "pathlib",
    "accaoui_disposable_connection_adapter_readiness",
    "accaoui_disposable_environment_gate",
}
seen_imports = set()

for node in ast.walk(harness_tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen_imports.add(alias.name.split(".", 1)[0])
    elif isinstance(node, ast.ImportFrom) and node.module:
        seen_imports.add(node.module.split(".", 1)[0])

unexpected_imports = seen_imports - allowed_imports
if unexpected_imports:
    fail(f"Harness besitzt unerlaubte Importe: {unexpected_imports}")

harness_lower = harness_source.lower()
for marker in (
    "psycopg",
    "asyncpg",
    "requests",
    "urllib",
    "http.client",
    "socket",
    "subprocess",
    ".connect(",
    "create_connection",
    "postgres://",
    "postgresql://",
    "supabase.co",
    "service_role",
    "database_url",
):
    if marker in harness_lower:
        fail(f"Harness enthält verbotenen Verbindungsinhalt: {marker}")

serialized = json.dumps(contract, ensure_ascii=False).lower()
for marker in (
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
    if marker in serialized:
        fail(f"Gate-Vertrag enthält verbotenen Inhalt: {marker}")

v2731z_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2731z*.sql")
)
if v2731z_sql_files:
    fail(
        "v27.31z darf keine SQL-Migration erzeugen: "
        f"{v2731z_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend = frontend_path.read_text(encoding="utf-8").lower()

    if CONTRACT_PATH.name.lower() in frontend:
        fail(
            "Umgebungs-Gate-Vertrag wird im Frontend referenziert: "
            f"{frontend_path.name}"
        )

print("Disposable Datenbank-Umgebungs-Gate-Vertrag: OK")
print("Standardentscheidung: deny")
print("Zielklasse: ausschließlich explizites lokales Loopback")
print("Remote, unbekannt und produktiv: geschlossen abgelehnt")
print("URL und Connection-String: verboten")
print("Destruktive Bestätigung: zwingend")
print("Verbindungsadapter: nur spätere validierte Descriptor-Eingabe")
print("Datenbanktreiber: keiner")
print("Netzwerkcode: keiner")
print("Datenbankverbindung: keine")
print("Datenbanktest ausgeführt: nein")
print("SQL-Migration v27.31z: keine")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
