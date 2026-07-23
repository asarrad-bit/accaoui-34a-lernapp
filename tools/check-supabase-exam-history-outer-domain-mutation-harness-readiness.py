from pathlib import Path
import ast
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

SOURCE_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-fixture-harness-contract.json"
)
DATABASE_TEST_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-database-test-contract.json"
)
FIXTURE_CATALOG_PATH = (
    ROOT
    / "tools"
    / "fixtures"
    / "exam-history-outer-domain-mutation-fixtures.json"
)
HARNESS_PATH = (
    ROOT
    / "tools"
    / "run-supabase-exam-history-outer-domain-mutation-harness.py"
)
READINESS_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-harness-readiness-contract.json"
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


def canonical_sha256(value: object) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def source_projection(source: dict) -> dict:
    keys = (
        "users",
        "resources",
        "clientRequestKeys",
        "payloads",
        "expectedVersions",
        "scenarios",
        "concurrencyBarriers",
        "harnessLifecycle",
        "faultInjectionContract",
    )

    for key in keys:
        if key not in source:
            fail(f"v27.31x-Quellvertrag enthält nicht: {key}")

    return {
        "version": "v27.31y",
        "catalogVersion": 1,
        "status": "synthetic_not_executed",
        "sourceContractPath": (
            "docs/contracts/"
            "exam-history-outer-domain-mutation-"
            "fixture-harness-contract.json"
        ),
        "sourceContractVersion": "v27.31x",
        "syntheticOnly": True,
        "databaseExecutionAllowed": False,
        "users": source["users"],
        "resources": source["resources"],
        "clientRequestKeys": source["clientRequestKeys"],
        "payloads": source["payloads"],
        "expectedVersions": source["expectedVersions"],
        "scenarios": source["scenarios"],
        "concurrencyBarriers": source["concurrencyBarriers"],
        "harnessLifecycle": source["harnessLifecycle"],
        "faultInjectionContract": source["faultInjectionContract"],
    }


readiness = read_json(
    READINESS_CONTRACT_PATH,
    "Verbindungsfreier Harness-Readiness-Vertrag",
)

if readiness.get("version") != "v27.31y":
    fail("Harness-Readiness-Vertrag besitzt nicht v27.31y.")
if readiness.get("contractVersion") != 1:
    fail("Harness-Readiness-Vertrag besitzt nicht Schema 1.")
if readiness.get("status") != (
    "implemented_connection_free_not_live"
):
    fail("Harness-Readiness-Status ist ungültig.")
if readiness.get("productiveReleaseAllowed") is not False:
    fail("Harness-Readiness darf nicht produktiv sein.")

implementation = readiness.get("implementation", {})
if implementation != {
    "sourceContractPath": (
        "docs/contracts/"
        "exam-history-outer-domain-mutation-fixture-harness-contract.json"
    ),
    "databaseTestContractPath": (
        "docs/contracts/"
        "exam-history-outer-domain-mutation-database-test-contract.json"
    ),
    "fixtureCatalogPath": (
        "tools/fixtures/"
        "exam-history-outer-domain-mutation-fixtures.json"
    ),
    "harnessPath": (
        "tools/"
        "run-supabase-exam-history-outer-domain-mutation-harness.py"
    ),
    "checkerPath": (
        "tools/"
        "check-supabase-exam-history-outer-domain-mutation-"
        "harness-readiness.py"
    ),
    "documentPath": (
        "docs/"
        "SUPABASE_EXAM_RESULT_HISTORY_"
        "OUTER_DOMAIN_MUTATION_HARNESS_READINESS.md"
    ),
    "fixtureCatalogImplemented": True,
    "connectionFreeHarnessScaffoldImplemented": True,
    "databaseDriverPresent": False,
    "databaseConnectionCreated": False,
    "databaseTestExecuted": False,
    "sqlMigrationCreated": False,
    "frontendIntegration": False,
}:
    fail("Harness-Readiness-Implementierung ist ungültig.")

if readiness.get("harnessModes") != {
    "defaultMode": "validate_only",
    "validateOnlyExitCode": 0,
    "databaseRunFlag": "--run-database",
    "explicitEnvironmentVariable": "ACCAOUI_DB_TEST_MODE",
    "requiredFutureEnvironmentValue": "disposable",
    "databaseRunImplemented": False,
    "databaseRunClosedExitCode": 2,
}:
    fail("Harness-Modusgrenze ist ungültig.")

if readiness.get("safetyBoundary") != {
    "networkCodeAllowed": False,
    "databaseDriverAllowed": False,
    "databaseUrlAllowed": False,
    "productionSecretAllowed": False,
    "serviceRoleKeyAllowed": False,
    "realParticipantDataAllowed": False,
    "realEmailAddressAllowed": False,
    "realNameAllowed": False,
    "frontendReferenceAllowed": False,
    "clientSelectableFaultInjectionAllowed": False,
}:
    fail("Harness-Sicherheitsgrenze ist ungültig.")

if readiness.get("validationBoundary") != {
    "loadsSourceContract": True,
    "loadsFixtureCatalog": True,
    "verifiesSourceProjection": True,
    "verifiesCanonicalCatalogFingerprint": True,
    "verifiesSyntheticIdentifiers": True,
    "verifiesClientKeyWidth": True,
    "verifiesScenarioReferences": True,
    "verifiesConcurrencyBarrierReferences": True,
    "opensDatabaseConnection": False,
    "executesDatabaseTest": False,
}:
    fail("Harness-Validierungsgrenze ist ungültig.")

if readiness.get("unresolvedRequirements") != {
    "disposableEnvironmentGateImplementation": True,
    "databaseConnectionAdapterImplementation": True,
    "testOnlyFaultInjectionImplementation": True,
    "databaseTestExecution": True,
    "concurrencyTestExecution": True,
    "authorizationTestExecution": True,
    "directAppExecutionGrant": True,
    "frontendIntegration": True,
}:
    fail("Offene Harness-Anforderungen sind ungültig.")

source = read_json(
    SOURCE_CONTRACT_PATH,
    "v27.31x-Fixture-/Harness-Quellvertrag",
)
if source.get("version") != "v27.31x":
    fail("Fixture-/Harness-Quellvertrag besitzt nicht v27.31x.")

database_test = read_json(
    DATABASE_TEST_CONTRACT_PATH,
    "v27.31w-Datenbank-Testvertrag",
)
if database_test.get("version") != "v27.31w":
    fail("Datenbank-Testvertrag besitzt nicht v27.31w.")
if database_test.get("implementation", {}).get(
    "databaseTestExecuted"
) is not False:
    fail("Datenbanktest wurde unerwartet ausgeführt.")

catalog = read_json(
    FIXTURE_CATALOG_PATH,
    "synthetischer Fixture-Katalog",
)
expected_catalog = source_projection(source)
if catalog != expected_catalog:
    fail("Fixture-Katalog ist keine exakte v27.31x-Projektion.")

integrity = readiness.get("catalogIntegrity", {})
expected_integrity = {
    "canonicalSha256": canonical_sha256(catalog),
    "userCount": len(catalog["users"]),
    "resourceCount": len(catalog["resources"]),
    "clientRequestKeyCount": len(
        catalog["clientRequestKeys"]
    ),
    "payloadCount": len(catalog["payloads"]),
    "scenarioCount": len(catalog["scenarios"]),
    "concurrencyBarrierCount": len(
        catalog["concurrencyBarriers"]
    ),
}
if integrity != expected_integrity:
    fail("Fixture-Katalog-Integrität ist ungültig.")

if not HARNESS_PATH.is_file():
    fail("Verbindungsfreies Harness-Gerüst fehlt.")

harness_source = HARNESS_PATH.read_text(encoding="utf-8")
try:
    tree = ast.parse(harness_source)
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
}
seen_imports = set()

for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        for alias in node.names:
            seen_imports.add(alias.name.split(".", 1)[0])
    elif isinstance(node, ast.ImportFrom):
        if node.module:
            seen_imports.add(node.module.split(".", 1)[0])

unexpected_imports = seen_imports - allowed_imports
if unexpected_imports:
    fail(f"Harness besitzt unerlaubte Importe: {unexpected_imports}")

lower_source = harness_source.lower()
for forbidden in (
    "psycopg",
    "asyncpg",
    "requests",
    "urllib",
    "http.client",
    "socket",
    "subprocess",
    "create_connection",
    ".connect(",
    "postgres://",
    "postgresql://",
    "supabase.co",
    "service_role",
    "database_url",
    "participant_id",
):
    if forbidden in lower_source:
        fail(f"Harness enthält verbotenen Inhalt: {forbidden}")

required_harness_markers = (
    "ACCAOUI_DB_TEST_MODE",
    "--validate-only",
    "--run-database",
    "validate_catalog(source, catalog, readiness)",
    "Datenbankverbindung geöffnet: nein",
    "Datenbanktest ausgeführt: nein",
    "return 2",
)
for marker in required_harness_markers:
    if marker not in harness_source:
        fail(f"Harness-Anweisung fehlt: {marker}")

validate = subprocess.run(
    [sys.executable, str(HARNESS_PATH), "--validate-only"],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
)
if validate.returncode != 0:
    fail(
        "Harness-Validate-only-Lauf fehlgeschlagen:\n"
        + validate.stdout
        + "\n"
        + validate.stderr
    )
for marker in (
    "Synthetischer Fixture-Katalog: OK",
    "Harness-Modus: validate_only",
    "Datenbankverbindung geöffnet: nein",
    "Netzwerkzugriff: nein",
    "Datenbanktest ausgeführt: nein",
):
    if marker not in validate.stdout:
        fail(f"Validate-only-Ausgabe fehlt: {marker}")

closed_env = dict(os.environ)
closed_env["ACCAOUI_DB_TEST_MODE"] = "disposable"

closed = subprocess.run(
    [sys.executable, str(HARNESS_PATH), "--run-database"],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=False,
    env=closed_env,
)
if closed.returncode != 2:
    fail(
        "Gesperrter Datenbankmodus besitzt nicht Exitcode 2:\n"
        + closed.stdout
        + "\n"
        + closed.stderr
    )
for marker in (
    "noch nicht implementiert",
    "Datenbankverbindung geöffnet: nein",
    "Datenbanktest ausgeführt: nein",
):
    if marker not in closed.stdout:
        fail(f"Gesperrte Datenbankmodus-Ausgabe fehlt: {marker}")

v2731y_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2731y*.sql")
)
if v2731y_sql_files:
    fail(
        "v27.31y darf keine SQL-Migration erzeugen: "
        f"{v2731y_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend = frontend_path.read_text(encoding="utf-8").lower()
    for forbidden_reference in (
        FIXTURE_CATALOG_PATH.name.lower(),
        HARNESS_PATH.name.lower(),
        READINESS_CONTRACT_PATH.name.lower(),
    ):
        if forbidden_reference in frontend:
            fail(
                "Harness-Readiness wird im Frontend referenziert: "
                f"{frontend_path.name}: {forbidden_reference}"
            )

print("Synthetischer Fixture-Katalog und Harness-Readiness: OK")
print("Fixture-Katalog: implementiert und kanonisch gebunden")
print("Harness-Gerüst: lokal ausführbar, verbindungsfrei")
print("Validate-only: erfolgreich")
print("Datenbankmodus: geschlossen, Exitcode 2")
print("Datenbanktreiber: keiner")
print("Netzwerkcode: keiner")
print("Datenbankverbindung: keine")
print("Datenbanktest ausgeführt: nein")
print("SQL-Migration v27.31y: keine")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
