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
        "test-python-environment-readiness-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-dependency-manifest-materialization-contract.json"
    )
)
MANIFEST = (
    ROOT
    / "tools"
    / "test-dependencies"
    / "disposable-postgresql-requirements.txt"
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
    "v27.32g-Test-Python-Umgebungsvertrag",
)
source = load_json(
    SOURCE,
    "v27.32f-Manifest-Materialisierungsvertrag",
)

if contract.get("version") != "v27.32g":
    fail("Umgebungsvertrag besitzt nicht v27.32g.")
if contract.get("contractVersion") != 1:
    fail("Umgebungsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_readiness_not_created_not_live"
):
    fail("Umgebungsvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Umgebungsvertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32f":
    fail("Quellvertrag besitzt nicht v27.32f.")
if source.get("implementation", {}).get(
    "manifestMaterialized"
) is not True:
    fail("Quellmanifest ist nicht materialisiert.")

if MANIFEST.read_bytes() != b"psycopg[binary]==3.3.4\n":
    fail("Isoliertes Test-Dependency-Manifest ist ungültig.")

implementation = contract.get("implementation", {})
if implementation.get(
    "environmentReadinessContractImplemented"
) is not True:
    fail("Umgebungs-Readiness-Vertrag ist nicht implementiert.")

for key in (
    "environmentDescriptorResolverImplemented",
    "virtualEnvironmentCreated",
    "interpreterExecuted",
    "dependencyInstalled",
    "driverImported",
    "connectionAdapterImplemented",
    "databaseConnectionCreated",
    "databaseTestExecuted",
    "sqlMigrationCreated",
    "frontendIntegration",
):
    if implementation.get(key) is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

root_boundary = contract.get("environmentRootBoundary", {})
if root_boundary.get("selectorType") != "environment_variable":
    fail("Umgebungswurzel-Selektortyp ist ungültig.")
if root_boundary.get("selectorName") != (
    "ACCAOUI_DISPOSABLE_TEST_ENV_ROOT"
):
    fail("Umgebungswurzel-Selektor ist ungültig.")
if root_boundary.get("defaultPathAllowed") is not False:
    fail("Standardpfad darf nicht erlaubt sein.")
if root_boundary.get("absolutePathRequired") is not True:
    fail("Absolute Pfadpflicht fehlt.")
if root_boundary.get("insideRepositoryAllowed") is not False:
    fail("Umgebung darf nicht im Repository liegen.")
if root_boundary.get(
    "pathCreationAllowedInThisVersion"
) is not False:
    fail("v27.32g darf keinen Umgebungspfad erstellen.")

interpreter = contract.get("interpreterBoundary", {})
if interpreter.get("environmentType") != "python_venv":
    fail("Umgebungstyp ist ungültig.")
if interpreter.get("basePythonMinimum") != "3.10":
    fail("Python-Minimum ist ungültig.")
if interpreter.get("basePythonMaximum") != "3.14":
    fail("Python-Maximum ist ungültig.")
if interpreter.get(
    "sameMajorMinorAsInvokingInterpreterRequired"
) is not True:
    fail("Python-Major-/Minor-Bindung fehlt.")
if interpreter.get(
    "windowsRelativeInterpreterPath"
) != "Scripts/python.exe":
    fail("Windows-Interpreterpfad ist ungültig.")
if interpreter.get(
    "posixRelativeInterpreterPath"
) != "bin/python":
    fail("POSIX-Interpreterpfad ist ungültig.")
if interpreter.get(
    "interpreterExecutionAllowedInThisVersion"
) is not False:
    fail("v27.32g darf keinen Interpreter ausführen.")

isolation = contract.get("isolationBoundary", {})
for key in (
    "includeSystemSitePackages",
    "systemSitePackagesAllowed",
    "userSitePackagesAllowed",
    "inheritPythonPathAllowed",
    "inheritVirtualEnvAllowed",
    "productionRuntimeAllowed",
    "frontendRuntimeAllowed",
    "applicationStartupAllowed",
    "standardPreflightActivationAllowed",
    "standardPreflightInstallationAllowed",
    "automaticActivationAllowed",
    "automaticCreationAllowed",
    "automaticInstallationAllowed",
):
    if isolation.get(key) is not False:
        fail(f"Isolationsgrenze ist offen: {key}")

if isolation.get("pythonNoUserSiteRequiredLater") is not True:
    fail("PYTHONNOUSERSITE-Pflicht fehlt.")
if isolation.get(
    "explicitHumanAuthorizationRequiredLater"
) is not True:
    fail("Spätere ausdrückliche Freigabe fehlt.")

security = contract.get("securityBoundary", {})
for key in (
    "passwordAllowed",
    "databaseUrlAllowed",
    "connectionStringAllowed",
    "serviceRoleKeyAllowed",
    "productionSecretAllowed",
    "realParticipantDataAllowed",
    "filesystemMutationAllowed",
    "processExecutionAllowed",
    "networkExecutionAllowed",
    "driverImportAllowed",
    "databaseConnectionAllowed",
    "frontendReferenceAllowed",
):
    if security.get(key) is not False:
        fail(f"Sicherheitsgrenze ist offen: {key}")

for relative in (
    ".venv-disposable-postgresql",
    "tools/test-environments/disposable-postgresql",
    "tools/test-environments/disposable-postgresql-venv",
):
    if (ROOT / relative).exists():
        fail(
            "v27.32g darf keine Test-Python-Umgebung "
            f"materialisieren: {relative}"
        )

preflight = (ROOT / "tools" / "preflight.py").read_text(
    encoding="utf-8",
    errors="replace",
).lower()

for marker in (
    "python -m venv",
    "py -m venv",
    "venv.create",
    "pip install",
    "python -m pip",
    "py -m pip",
    "activate.bat",
    "scripts/activate",
    "bin/activate",
):
    if marker in preflight:
        fail(
            "Preflight enthält unerlaubte Umgebungsaktion: "
            f"{marker}"
        )

for runtime_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
    ROOT / "tools"
    / "run-supabase-exam-history-outer-domain-mutation-harness.py",
):
    content = runtime_path.read_text(
        encoding="utf-8",
        errors="replace",
    )

    if "ACCAOUI_DISPOSABLE_TEST_ENV_ROOT" in content:
        fail(
            "Umgebungsselektor wird unerwartet von Runtime "
            f"verwendet: {runtime_path.name}"
        )

if list(MIGRATIONS.glob("*v2732g*.sql")):
    fail("v27.32g darf keine SQL-Migration erzeugen.")

print("Disposable PostgreSQL-Test-Python-Umgebungsvertrag: OK")
print("Selektor: ACCAOUI_DISPOSABLE_TEST_ENV_ROOT")
print("Standardpfad: keiner")
print("Umgebung im Repository: verboten")
print("Python-Bereich: 3.10 bis 3.14")
print("System-/User-Site-Packages: verboten")
print("Virtuelle Umgebung erstellt: nein")
print("Interpreter ausgeführt: nein")
print("Dependency installiert: nein")
print("Treiber importiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32g: keine")
print("Produktive Freigabe: nein")
