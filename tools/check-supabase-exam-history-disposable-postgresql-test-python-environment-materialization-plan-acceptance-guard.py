from pathlib import Path
import ast
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
        "test-python-environment-materialization-plan-"
        "acceptance-guard-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-plan-contract.json"
    )
)
DESCRIPTOR_RESOLVER = (
    ROOT
    / "tools"
    / "accaoui_disposable_test_python_environment_descriptor.py"
)
PLAN_BUILDER = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_plan.py"
    )
)
GUARD = (
    ROOT
    / "tools"
    / (
        "accaoui_disposable_test_python_environment_"
        "materialization_plan_acceptance_guard.py"
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
    "v27.32k-Materialisierungsplan-Annahmevertrag",
)
source = load_json(
    SOURCE,
    "v27.32j-Materialisierungsplan-Vertrag",
)

if contract.get("version") != "v27.32k":
    fail("Annahmevertrag besitzt nicht v27.32k.")
if contract.get("contractVersion") != 1:
    fail("Annahmevertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_acceptance_execution_locked"
):
    fail("Annahmevertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Annahmevertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32j":
    fail("Quellvertrag besitzt nicht v27.32j.")
if source.get("implementation", {}).get(
    "materializationPlanBuilderImplemented"
) is not True:
    fail("Quellplan-Builder ist nicht implementiert.")
if source.get("planBoundary", {}).get("successStatus") != (
    "plan_ready_execution_locked"
):
    fail("Quellplan besitzt falschen Erfolgsstatus.")

implementation = contract.get("implementation", {})
if implementation.get(
    "materializationPlanAcceptanceGuardImplemented"
) is not True:
    fail("Materialisierungsplan-Annahme-Guard fehlt.")

for key in (
    "executionAuthorizationImplemented",
    "materializerImplemented",
    "evidenceCollectorImplemented",
    "rollbackImplemented",
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
try:
    tree = ast.parse(guard_source)
except SyntaxError as exc:
    fail(f"Annahme-Guard besitzt Syntaxfehler: {exc}")

allowed_imports = {
    "__future__",
    "collections",
    "pathlib",
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
}

for node in ast.walk(tree):
    if isinstance(node, ast.Name) and node.id in forbidden_names:
        fail(f"Annahme-Guard verwendet verbotenen Namen: {node.id}")

for node in ast.walk(tree):
    if not isinstance(node, ast.Call):
        continue

    if isinstance(node.func, ast.Attribute):
        if node.func.attr in {
            "exists",
            "is_file",
            "is_dir",
            "mkdir",
            "resolve",
            "absolute",
            "open",
            "read_text",
            "read_bytes",
            "write_text",
            "write_bytes",
            "unlink",
            "rename",
            "replace",
        }:
            fail(
                "Annahme-Guard besitzt verbotenen "
                f"Dateisystemaufruf: {node.func.attr}"
            )

lower_source = guard_source.lower()
for marker in (
    "pip install",
    "python -m pip",
    "py -m pip",
    "subprocess",
    "venv.create",
    ".connect(",
    "postgres://",
    "postgresql://",
    "database_url",
    "service_role",
):
    if marker in lower_source:
        fail(f"Annahme-Guard enthält verbotenen Inhalt: {marker}")

descriptor_module = load_module(
    DESCRIPTOR_RESOLVER,
    "accaoui_descriptor_v2732k",
)
plan_module = load_module(
    PLAN_BUILDER,
    "accaoui_materialization_plan_v2732k",
)
guard_module = load_module(
    GUARD,
    "accaoui_materialization_plan_acceptance_v2732k",
)

resolve_descriptor = getattr(
    descriptor_module,
    "resolve_test_python_environment_descriptor",
    None,
)
build_plan = getattr(
    plan_module,
    "build_test_python_environment_materialization_plan",
    None,
)
accept_plan = getattr(
    guard_module,
    "accept_test_python_environment_materialization_plan",
    None,
)

if not callable(resolve_descriptor):
    fail("Quell-Descriptor-Resolver fehlt.")
if not callable(build_plan):
    fail("Quell-Plan-Builder fehlt.")
if not callable(accept_plan):
    fail("Materialisierungsplan-Annahme-Guard fehlt.")

windows_facts = {
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
}

posix_facts = {
    **windows_facts,
    "platform": "posix",
    "environmentRoot": "/tmp/accaoui-test-envs/postgresql",
    "repositoryRoot": "/srv/accaoui/v4-dashboard",
}

windows_plan = build_plan({
    "descriptorResult": resolve_descriptor(windows_facts),
    "basePythonExecutable": (
        r"C:\Users\tester\AppData\Local\Programs\Python"
        r"\Python313\python.exe"
    ),
    "targetState": "absent",
    "humanAuthorizationRecorded": False,
})

posix_plan = build_plan({
    "descriptorResult": resolve_descriptor(posix_facts),
    "basePythonExecutable": "/usr/bin/python3.13",
    "targetState": "empty",
    "humanAuthorizationRecorded": False,
})

tampered_status = clone(windows_plan)
tampered_status["status"] = "execution_ready"

tampered_reason = clone(windows_plan)
tampered_reason["reason"] = "unexpected"

tampered_flag = clone(windows_plan)
tampered_flag["processExecutionAllowed"] = True

tampered_plan_key = clone(windows_plan)
tampered_plan_key["plan"]["unexpected"] = True

tampered_argv = clone(windows_plan)
tampered_argv["plan"]["creation"]["argv"][1] = "-E"

tampered_shell = clone(windows_plan)
tampered_shell["plan"]["creation"]["shell"] = True

tampered_target = clone(windows_plan)
tampered_target["plan"]["creation"]["argv"][-1] = (
    r"D:\other-target"
)

tampered_interpreter = clone(windows_plan)
tampered_interpreter["plan"]["interpreter"][
    "executionAllowed"
] = True

tampered_manifest = clone(windows_plan)
tampered_manifest["plan"]["manifest"][
    "installationAllowed"
] = True

tampered_evidence = clone(windows_plan)
tampered_evidence["plan"]["evidence"][
    "collectionAllowed"
] = True

tampered_rollback = clone(windows_plan)
tampered_rollback["plan"]["rollback"][
    "executionAllowed"
] = True

tampered_rollback_target = clone(windows_plan)
tampered_rollback_target["plan"]["rollback"][
    "deleteOnlyExactTarget"
] = r"D:\parent"

tampered_authorization = clone(windows_plan)
tampered_authorization["plan"]["authorization"][
    "recorded"
] = True

cases = [
    (
        [],
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_invalid_input"
        ),
    ),
    (
        tampered_status,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_source_status_invalid"
        ),
    ),
    (
        tampered_reason,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_source_reason_invalid"
        ),
    ),
    (
        tampered_flag,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_execution_boundary_open"
        ),
    ),
    (
        tampered_plan_key,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_plan_structure_invalid"
        ),
    ),
    (
        tampered_argv,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_argv_invalid"
        ),
    ),
    (
        tampered_shell,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_creation_boundary_invalid"
        ),
    ),
    (
        tampered_target,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_argv_invalid"
        ),
    ),
    (
        tampered_interpreter,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_interpreter_invalid"
        ),
    ),
    (
        tampered_manifest,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_manifest_invalid"
        ),
    ),
    (
        tampered_evidence,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_evidence_invalid"
        ),
    ),
    (
        tampered_rollback,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_rollback_invalid"
        ),
    ),
    (
        tampered_rollback_target,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_rollback_invalid"
        ),
    ),
    (
        tampered_authorization,
        "blocked",
        (
            "test_environment_materialization_plan_"
            "acceptance_authorization_invalid"
        ),
    ),
    (
        windows_plan,
        "accepted_execution_locked",
        (
            "test_environment_materialization_plan_"
            "accepted_execution_locked"
        ),
    ),
    (
        posix_plan,
        "accepted_execution_locked",
        (
            "test_environment_materialization_plan_"
            "accepted_execution_locked"
        ),
    ),
]

for candidate, expected_status, expected_reason in cases:
    before = clone(candidate) if isinstance(candidate, dict) else candidate
    first = accept_plan(candidate)
    second = accept_plan(candidate)

    if first != second:
        fail("Materialisierungsplan-Annahme ist nicht deterministisch.")

    if isinstance(candidate, dict) and candidate != before:
        fail("Materialisierungsplan-Annahme verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Annahmestatus ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Annahmegrund ist ungültig: {first}")

    for key in (
        "environmentCreationAllowed",
        "filesystemReadAllowed",
        "filesystemMutationAllowed",
        "processExecutionAllowed",
        "dependencyInstallationAllowed",
        "evidenceCollectionAllowed",
        "rollbackExecutionAllowed",
        "authorizationGrantAccepted",
    ):
        if first.get(key) is not False:
            fail(f"Annahme-Ausführungsgrenze ist offen: {key}")

for source_plan in (windows_plan, posix_plan):
    result = accept_plan(source_plan)

    if result.get("accepted") is not True:
        fail("Gültiger Materialisierungsplan wurde nicht angenommen.")

    accepted_plan = result.get("acceptedPlan")
    if not isinstance(accepted_plan, dict):
        fail("Angenommener kanonischer Plan fehlt.")

    if accepted_plan != source_plan["plan"]:
        fail("Angenommener Plan weicht vom Quellplan ab.")

    if accepted_plan is source_plan["plan"]:
        fail("Annahme-Guard darf keine Quellplan-Referenz zurückgeben.")

for relative in (
    ".venv-disposable-postgresql",
    "tools/test-environments/disposable-postgresql",
    "tools/test-environments/disposable-postgresql-venv",
):
    if (ROOT / relative).exists():
        fail(
            "v27.32k darf keine Test-Python-Umgebung "
            f"materialisieren: {relative}"
        )

if list(MIGRATIONS.glob("*v2732k*.sql")):
    fail("v27.32k darf keine SQL-Migration erzeugen.")

print("Disposable Materialisierungsplan-Annahme-Guard: OK")
print("Quellvertrag: v27.32j")
print("Quellstatus: plan_ready_execution_locked")
print("Strukturprüfung: vollständig")
print("argv-, Ziel- und Interpreterbindung: geprüft")
print("Manifest-, Nachweis- und Rollbackgrenzen: geprüft")
print("Autorisierungsmanipulation: geschlossen blockiert")
print("Ergebnis: accepted_execution_locked")
print("Ausführungsfreigabe: keine")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Virtuelle Umgebung erstellt: nein")
print("Dependency installiert: nein")
print("Treiber importiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32k: keine")
print("Produktive Freigabe: nein")
