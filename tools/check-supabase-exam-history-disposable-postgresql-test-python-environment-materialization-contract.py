from pathlib import Path
import ast
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
        "test-python-environment-materialization-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-descriptor-resolver-contract.json"
    )
)
RESOLVER = (
    ROOT
    / "tools"
    / "accaoui_disposable_test_python_environment_descriptor.py"
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
    "v27.32i-Umgebungs-Materialisierungsvertrag",
)
source = load_json(
    SOURCE,
    "v27.32h-Descriptor-Resolver-Vertrag",
)

if contract.get("version") != "v27.32i":
    fail("Materialisierungsvertrag besitzt nicht v27.32i.")
if contract.get("contractVersion") != 1:
    fail("Materialisierungsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_materialization_fully_locked_not_executed"
):
    fail("Materialisierungsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Materialisierungsvertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32h":
    fail("Quellvertrag besitzt nicht v27.32h.")
if source.get("implementation", {}).get(
    "environmentDescriptorResolverImplemented"
) is not True:
    fail("Quellresolver ist nicht implementiert.")
if source.get("successBoundary", {}).get("status") != (
    "descriptor_ready_creation_locked"
):
    fail("Quellresolver besitzt falschen Erfolgsstatus.")

if MANIFEST.read_bytes() != b"psycopg[binary]==3.3.4\n":
    fail("Isoliertes Test-Dependency-Manifest ist ungültig.")

implementation = contract.get("implementation", {})
if implementation.get(
    "materializationContractImplemented"
) is not True:
    fail("Materialisierungsvertrag ist nicht implementiert.")

for key in (
    "materializationPlanBuilderImplemented",
    "materializerImplemented",
    "filesystemReadPerformed",
    "filesystemMutationPerformed",
    "virtualEnvironmentCreated",
    "interpreterExecuted",
    "dependencyInstalled",
    "driverImported",
    "databaseConnectionCreated",
    "databaseTestExecuted",
    "sqlMigrationCreated",
    "frontendIntegration",
):
    if implementation.get(key) is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

preconditions = contract.get("preconditionBoundary", {})
if preconditions.get("requiredDescriptorStatus") != (
    "descriptor_ready_creation_locked"
):
    fail("Descriptor-Vorbedingung ist ungültig.")
if preconditions.get("targetMustBeAbsentOrEmpty") is not True:
    fail("Leere Zielpflicht fehlt.")
if preconditions.get("existingNonEmptyTargetAllowed") is not False:
    fail("Nichtleeres Ziel darf nicht erlaubt sein.")
if preconditions.get("explicitHumanAuthorizationRequired") is not True:
    fail("Ausdrückliche menschliche Freigabe fehlt.")
if preconditions.get("executionAllowedInThisVersion") is not False:
    fail("v27.32i darf keine Ausführung erlauben.")

creation = contract.get("creationCommandBoundary", {})
expected_template = [
    "{basePythonExecutable}",
    "-I",
    "-m",
    "venv",
    "{environmentRoot}",
]
if creation.get("windowsArgvTemplate") != expected_template:
    fail("Windows-Erstellungsargumente sind ungültig.")
if creation.get("posixArgvTemplate") != expected_template:
    fail("POSIX-Erstellungsargumente sind ungültig.")
if creation.get("representation") != "structured_argv_only":
    fail("Erstellungsdarstellung ist ungültig.")
if creation.get("shellAllowed") is not False:
    fail("Shell darf nicht erlaubt sein.")
if creation.get("processExecutionAllowed") is not False:
    fail("Prozessausführung darf nicht erlaubt sein.")
if creation.get("timeoutSeconds") != 60:
    fail("Erstellungstimeout ist ungültig.")
if creation.get("upgradeExistingEnvironmentAllowed") is not False:
    fail("Upgrade bestehender Umgebung darf nicht erlaubt sein.")
if creation.get("clearExistingEnvironmentAllowed") is not False:
    fail("Löschen bestehender Umgebung darf nicht erlaubt sein.")

target = contract.get("targetBinding", {})
if target.get("environmentRootFromDescriptorOnly") is not True:
    fail("Ziel muss ausschließlich aus Descriptor stammen.")
for key in (
    "repositoryRelativeTargetAllowed",
    "repositoryTargetAllowed",
    "systemTargetAllowed",
    "globalSitePackagesTargetAllowed",
    "userSitePackagesTargetAllowed",
):
    if target.get(key) is not False:
        fail(f"Zielgrenze ist offen: {key}")

evidence = contract.get("postCreationEvidenceBoundary", {})
if evidence.get("evidenceCollectionImplemented") is not False:
    fail("Nachweiserfassung darf nicht implementiert sein.")
if evidence.get("pyvenvConfigIncludeSystemSitePackages") is not False:
    fail("System-Site-Packages-Nachweis ist ungültig.")
if evidence.get(
    "dependencyMustRemainUninstalledAtCreationStage"
) is not True:
    fail("Dependency muss beim Erstellen uninstalliert bleiben.")

rollback = contract.get("rollbackBoundary", {})
if rollback.get("rollbackImplemented") is not False:
    fail("Rollback darf noch nicht implementiert sein.")
if rollback.get("deleteOnlyExactDescriptorTarget") is not True:
    fail("Exakte Zielbindung für Rollback fehlt.")
for key in (
    "deleteRepositoryPathAllowed",
    "deleteParentPathAllowed",
    "deletePreexistingTargetAllowed",
):
    if rollback.get(key) is not False:
        fail(f"Rollbackgrenze ist offen: {key}")
if rollback.get("creationOwnershipProofRequired") is not True:
    fail("Rollback-Besitznachweis fehlt.")

security = contract.get("securityBoundary", {})
for key in (
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

resolver_source = RESOLVER.read_text(encoding="utf-8")
tree = ast.parse(resolver_source)
for node in ast.walk(tree):
    if isinstance(node, ast.Import):
        names = [alias.name for alias in node.names]
    elif isinstance(node, ast.ImportFrom) and node.module:
        names = [node.module]
    else:
        continue

    if any(name in {"venv", "subprocess", "shutil"} for name in names):
        fail("Quellresolver besitzt unerwartete Ausführungsimporte.")

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
    "shutil.rmtree",
):
    if marker in preflight:
        fail(
            "Preflight enthält unerlaubte Materialisierungsaktion: "
            f"{marker}"
        )

for relative in (
    ".venv-disposable-postgresql",
    "tools/test-environments/disposable-postgresql",
    "tools/test-environments/disposable-postgresql-venv",
):
    if (ROOT / relative).exists():
        fail(
            "v27.32i darf keine Test-Python-Umgebung "
            f"materialisieren: {relative}"
        )

if list(MIGRATIONS.glob("*v2732i*.sql")):
    fail("v27.32i darf keine SQL-Migration erzeugen.")

print("Disposable Test-Python-Materialisierungsvertrag: OK")
print("Quellstatus: descriptor_ready_creation_locked")
print("Erstellungsdarstellung: strukturierte argv-Liste")
print("Shell: verboten")
print("Ziel: ausschließlich externer Descriptorpfad")
print("Nachweisgrenzen: festgelegt")
print("Rollbackgrenzen: festgelegt")
print("Materialisierer implementiert: nein")
print("Dateisystemzugriff ausgeführt: nein")
print("Virtuelle Umgebung erstellt: nein")
print("Interpreter ausgeführt: nein")
print("Dependency installiert: nein")
print("Treiber importiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32i: keine")
print("Produktive Freigabe: nein")
