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
    / "exam-history-disposable-postgresql-"
    / "driver-selection-contract.json"
)
SOURCE_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-disposable-database-harness-"
    / "gate-integration-contract.json"
)

# Path joins above intentionally keep names readable; normalize them.
CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-disposable-postgresql-driver-selection-contract.json"
)
SOURCE_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-disposable-database-harness-gate-integration-contract.json"
)

RUNTIME_PATHS = (
    ROOT / "tools" / "run-supabase-exam-history-outer-domain-mutation-harness.py",
    ROOT / "tools" / "accaoui_disposable_environment_gate.py",
    ROOT / "tools" / "accaoui_disposable_connection_adapter_readiness.py",
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
    CONTRACT_PATH,
    "Disposable PostgreSQL-Treiberauswahlvertrag",
)
source = load_json(
    SOURCE_CONTRACT_PATH,
    "v27.32b-Harness-Integrationsvertrag",
)

if contract.get("version") != "v27.32c":
    fail("Treiberauswahlvertrag besitzt nicht v27.32c.")
if contract.get("contractVersion") != 1:
    fail("Treiberauswahlvertrag besitzt nicht Schema 1.")
if contract.get("status") != "selected_not_installed_not_live":
    fail("Treiberauswahlstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Treiberauswahl darf nicht produktiv sein.")

if source.get("version") != "v27.32b":
    fail("Quellvertrag besitzt nicht v27.32b.")
if source.get("implementation", {}).get(
    "databaseConnectionCreated"
) is not False:
    fail("Quell-Harness hat unerwartet eine Verbindung erstellt.")

implementation = contract.get("implementation", {})
expected_implementation = {
    "sourceHarnessIntegrationContractPath": (
        "docs/contracts/"
        "exam-history-disposable-database-harness-"
        "gate-integration-contract.json"
    ),
    "harnessPath": (
        "tools/"
        "run-supabase-exam-history-outer-domain-mutation-harness.py"
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
        "check-supabase-exam-history-disposable-postgresql-"
        "driver-selection-contract.py"
    ),
    "documentPath": (
        "docs/"
        "SUPABASE_EXAM_RESULT_HISTORY_"
        "DISPOSABLE_POSTGRESQL_DRIVER_SELECTION_CONTRACT.md"
    ),
    "driverSelectedByContract": True,
    "driverDependencyDeclared": False,
    "driverInstalledByProject": False,
    "driverImportedByRuntime": False,
    "connectionAdapterImplemented": False,
    "databaseConnectionCreated": False,
    "databaseTestExecuted": False,
    "sqlMigrationCreated": False,
    "frontendIntegration": False,
}
if implementation != expected_implementation:
    fail("Treiberauswahl-Implementierungsgrenze ist ungültig.")

if contract.get("selectedDriver") != {
    "distributionName": "psycopg",
    "extra": "binary",
    "installSpecification": "psycopg[binary]==3.3.4",
    "importName": "psycopg",
    "pinnedVersion": "3.3.4",
    "majorGeneration": 3,
    "binaryDistributionRequired": True,
    "systemLibpqRequired": False,
    "sourceBuildAllowed": False,
    "purePythonFallbackAllowed": False,
    "poolExtraSelected": False,
    "asyncModeSelected": False,
}:
    fail("Ausgewählter PostgreSQL-Treiber ist ungültig.")

if contract.get("compatibilityBoundary") != {
    "pythonMinimum": "3.10",
    "pythonMaximum": "3.14",
    "postgresqlMinimum": 10,
    "postgresqlMaximum": 18,
    "operatingSystems": [
        "windows",
        "linux",
        "macos",
    ],
    "projectPrimaryRuntime": "python",
    "localDisposableOnly": True,
    "productionUseAllowed": False,
}:
    fail("Treiber-Kompatibilitätsgrenze ist ungültig.")

if contract.get("importBoundary") != {
    "moduleLevelImportAllowed": False,
    "harnessImportAllowed": False,
    "evaluatorImportAllowed": False,
    "adapterReadinessImportAllowed": False,
    "frontendImportAllowed": False,
    "futureAdapterFunctionOnly": True,
    "requiresEligibleGateResult": True,
    "requiresExactVersionMatch": True,
    "requiresExplicitDisposableMode": True,
    "importFailureDecision": "deny",
    "versionMismatchDecision": "deny",
    "implementationMismatchDecision": "deny",
}:
    fail("Treiber-Importgrenze ist ungültig.")

if contract.get("timeoutBoundary") != {
    "connectTimeoutSeconds": 3,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
    "idleInTransactionTimeoutMilliseconds": 10000,
    "scenarioTimeoutSeconds": 15,
    "timeoutDecision": "rollback_and_fail_closed",
    "retryOnConnectionTimeout": False,
    "retryOnStatementTimeout": False,
    "retryOnLockTimeout": False,
}:
    fail("Treiber-Timeoutgrenze ist ungültig.")

if contract.get("transactionBoundary") != {
    "autocommit": False,
    "explicitTransactionRequired": True,
    "oneScenarioPerTransaction": True,
    "rollbackAfterAssertions": True,
    "commitFixtureDataAllowed": False,
    "savepointForExpectedDomainFailure": True,
    "unexpectedFailureFullRollback": True,
    "connectionReuseAcrossScenariosAllowed": False,
    "resetDatabaseBetweenScenarios": True,
}:
    fail("Treiber-Transaktionsgrenze ist ungültig.")

expected_failures = {
    "driverMissing": "driver_not_installed",
    "driverVersionMismatch": "driver_version_mismatch",
    "driverImplementationMismatch": (
        "binary_driver_implementation_required"
    ),
    "gateDenied": "environment_gate_denied",
    "descriptorInvalid": "validated_descriptor_invalid",
    "connectionTimeout": "database_connection_timeout",
    "connectionRefused": "database_connection_refused",
    "authenticationFailure": "database_authentication_failed",
    "databaseMissing": "disposable_database_missing",
    "statementTimeout": "database_statement_timeout",
    "lockTimeout": "database_lock_timeout",
    "unexpectedDriverFailure": (
        "unexpected_database_driver_failure"
    ),
    "rawDriverErrorExposed": False,
    "retryableByDefault": False,
}
if contract.get("closedFailureMatrix") != expected_failures:
    fail("Geschlossene Treiber-Fehlermatrix ist ungültig.")

if contract.get("credentialBoundary") != {
    "passwordInContractAllowed": False,
    "passwordInRepositoryAllowed": False,
    "databaseUrlAllowed": False,
    "connectionStringAllowed": False,
    "serviceRoleKeyAllowed": False,
    "productionSecretAllowed": False,
    "credentialResolutionImplemented": False,
}:
    fail("Treiber-Credentialgrenze ist ungültig.")

if contract.get("installationBoundary") != {
    "installationCommandExecuted": False,
    "requirementsFileModified": False,
    "pyprojectModified": False,
    "lockFileModified": False,
    "virtualEnvironmentModified": False,
    "systemPackageInstalled": False,
    "networkDownloadExecuted": False,
}:
    fail("Treiber-Installationsgrenze ist ungültig.")

if contract.get("unresolvedRequirements") != {
    "isolatedTestDependencyManifest": True,
    "driverAvailabilityReadinessProbe": True,
    "connectionAdapterImplementation": True,
    "credentialResolutionContract": True,
    "testOnlyFaultInjectionImplementation": True,
    "databaseTestExecution": True,
    "concurrencyTestExecution": True,
    "authorizationTestExecution": True,
    "directAppExecutionGrant": True,
    "frontendIntegration": True,
}:
    fail("Offene Treiberanforderungen sind ungültig.")

for runtime_path in RUNTIME_PATHS:
    if not runtime_path.is_file():
        fail(f"Runtime-Datei fehlt: {runtime_path.name}")

    source_text = runtime_path.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source_text)
    except SyntaxError as exc:
        fail(f"Runtime-Datei besitzt Syntaxfehler: {exc}")

    imported_roots = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imported_roots.add(alias.name.split(".", 1)[0])
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported_roots.add(node.module.split(".", 1)[0])

    if "psycopg" in imported_roots:
        fail(
            "PostgreSQL-Treiber wird unerwartet importiert: "
            f"{runtime_path.name}"
        )

    lower_text = source_text.lower()
    for marker in (
        "psycopg.connect",
        "connection.connect",
        "create_connection",
        "postgres://",
        "postgresql://",
        "database_url",
        "service_role",
    ):
        if marker in lower_text:
            fail(
                "Runtime-Datei enthält unerlaubten "
                f"Verbindungsinhalt: {runtime_path.name}: {marker}"
            )

dependency_files = (
    ROOT / "requirements.txt",
    ROOT / "requirements-dev.txt",
    ROOT / "pyproject.toml",
    ROOT / "Pipfile",
    ROOT / "poetry.lock",
    ROOT / "setup.cfg",
)

for dependency_path in dependency_files:
    if not dependency_path.is_file():
        continue

    content = dependency_path.read_text(
        encoding="utf-8",
        errors="replace",
    )
    if re.search(r"(?i)\bpsycopg(?:-binary)?\b", content):
        fail(
            "Treiberabhängigkeit wurde unerwartet deklariert: "
            f"{dependency_path.name}"
        )

v2732c_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2732c*.sql")
)
if v2732c_sql_files:
    fail(
        "v27.32c darf keine SQL-Migration erzeugen: "
        f"{v2732c_sql_files}"
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
            "Treiberauswahlvertrag wird im Frontend referenziert: "
            f"{frontend_path.name}"
        )

print("Disposable PostgreSQL-Treiberauswahlvertrag: OK")
print("Auswahl: psycopg[binary]==3.3.4")
print("Importname: psycopg")
print("Python-Kompatibilität: 3.10 bis 3.14")
print("PostgreSQL-Kompatibilität: 10 bis 18")
print("Importgrenze: nur späterer Adapter nach Gate-Freigabe")
print("Timeout- und Transaktionsgrenze: festgelegt")
print("Geschlossene Fehlermatrix: festgelegt")
print("Treiberabhängigkeit deklariert: nein")
print("Treiber installiert: nein")
print("Treiber importiert: nein")
print("Datenbankverbindung: keine")
print("Datenbanktest ausgeführt: nein")
print("SQL-Migration v27.32c: keine")
print("Produktive Freigabe: nein")
