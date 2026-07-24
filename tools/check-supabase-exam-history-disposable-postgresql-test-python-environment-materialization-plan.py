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
        "test-python-environment-materialization-plan-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-materialization-contract.json"
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
    / "accaoui_disposable_test_python_environment_"
      "materialization_plan.py"
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


contract = load_json(
    CONTRACT,
    "v27.32j-Materialisierungsplan-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32i-Materialisierungsvertrag",
)

if contract.get("version") != "v27.32j":
    fail("Planvertrag besitzt nicht v27.32j.")
if contract.get("contractVersion") != 1:
    fail("Planvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_plan_execution_locked"
):
    fail("Planvertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Planvertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32i":
    fail("Quellvertrag besitzt nicht v27.32i.")
if source.get("implementation", {}).get(
    "materializationPlanBuilderImplemented"
) is not False:
    fail("Quellvertrag hatte unerwartet bereits einen Plan-Builder.")

implementation = contract.get("implementation", {})
if implementation.get(
    "materializationPlanBuilderImplemented"
) is not True:
    fail("Materialisierungsplan-Builder ist nicht implementiert.")

for key in (
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

plan_source = PLAN_BUILDER.read_text(encoding="utf-8")
try:
    tree = ast.parse(plan_source)
except SyntaxError as exc:
    fail(f"Plan-Builder besitzt Syntaxfehler: {exc}")

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
    fail(f"Plan-Builder besitzt unerlaubte Importe: {unexpected_imports}")

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
        fail(f"Plan-Builder verwendet verbotenen Namen: {node.id}")

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
                "Plan-Builder besitzt verbotenen "
                f"Dateisystemaufruf: {node.func.attr}"
            )

lower_source = plan_source.lower()
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
        fail(f"Plan-Builder enthält verbotenen Inhalt: {marker}")

descriptor_module = load_module(
    DESCRIPTOR_RESOLVER,
    "accaoui_descriptor_v2732j",
)
plan_module = load_module(
    PLAN_BUILDER,
    "accaoui_materialization_plan_v2732j",
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

if not callable(resolve_descriptor):
    fail("Quell-Descriptor-Resolver fehlt.")
if not callable(build_plan):
    fail("Materialisierungsplan-Builder fehlt.")

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

windows_descriptor = resolve_descriptor(windows_facts)
posix_descriptor = resolve_descriptor(posix_facts)

valid_windows_request = {
    "descriptorResult": windows_descriptor,
    "basePythonExecutable": (
        r"C:\Users\tester\AppData\Local\Programs\Python"
        r"\Python313\python.exe"
    ),
    "targetState": "absent",
    "humanAuthorizationRecorded": False,
}

valid_posix_request = {
    "descriptorResult": posix_descriptor,
    "basePythonExecutable": "/usr/bin/python3.13",
    "targetState": "empty",
    "humanAuthorizationRecorded": False,
}

cases = [
    (
        [],
        "blocked",
        "test_environment_materialization_plan_invalid_input",
    ),
    (
        {
            key: value
            for key, value in valid_windows_request.items()
            if key != "targetState"
        },
        "blocked",
        "test_environment_materialization_plan_missing_fields",
    ),
    (
        {
            **valid_windows_request,
            "unexpected": True,
        },
        "blocked",
        "test_environment_materialization_plan_unknown_fields",
    ),
    (
        {
            **valid_windows_request,
            "descriptorResult": {
                **windows_descriptor,
                "status": "blocked",
            },
        },
        "blocked",
        "test_environment_materialization_descriptor_invalid",
    ),
    (
        {
            **valid_windows_request,
            "basePythonExecutable": r"relative\python.exe",
        },
        "blocked",
        "test_environment_materialization_base_python_invalid",
    ),
    (
        {
            **valid_windows_request,
            "basePythonExecutable": (
                r"D:\accaoui-test-envs\postgresql"
                r"\Scripts\python.exe"
            ),
        },
        "blocked",
        "test_environment_materialization_base_python_invalid",
    ),
    (
        {
            **valid_windows_request,
            "targetState": "non_empty",
        },
        "blocked",
        "test_environment_target_not_empty",
    ),
    (
        {
            **valid_windows_request,
            "humanAuthorizationRecorded": True,
        },
        "blocked",
        (
            "test_environment_materialization_authorization_"
            "not_accepted_in_plan"
        ),
    ),
    (
        valid_windows_request,
        "plan_ready_execution_locked",
        (
            "test_environment_materialization_plan_"
            "ready_execution_locked"
        ),
    ),
    (
        valid_posix_request,
        "plan_ready_execution_locked",
        (
            "test_environment_materialization_plan_"
            "ready_execution_locked"
        ),
    ),
]

for request, expected_status, expected_reason in cases:
    before = dict(request) if isinstance(request, dict) else request
    first = build_plan(request)
    second = build_plan(request)

    if first != second:
        fail("Materialisierungsplan ist nicht deterministisch.")

    if isinstance(request, dict) and request != before:
        fail("Materialisierungsplan verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Planstatus ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Plangrund ist ungültig: {first}")

    for key in (
        "filesystemReadAllowed",
        "filesystemMutationAllowed",
        "processExecutionAllowed",
        "dependencyInstallationAllowed",
    ):
        if first.get(key) is not False:
            fail(f"Plan-Ausführungsgrenze ist offen: {key}")

for request, expected_interpreter in (
    (valid_windows_request, "Scripts/python.exe"),
    (valid_posix_request, "bin/python"),
):
    result = build_plan(request)
    plan = result.get("plan")

    if not isinstance(plan, dict):
        fail("Gültiger Materialisierungsplan fehlt.")

    argv = plan.get("creation", {}).get("argv")
    if argv != [
        request["basePythonExecutable"],
        "-I",
        "-m",
        "venv",
        request["descriptorResult"]["descriptor"][
            "environmentRoot"
        ],
    ]:
        fail("Materialisierungs-argv ist ungültig.")

    if plan.get("creation", {}).get("shell") is not False:
        fail("Materialisierungsplan darf keine Shell verwenden.")

    if plan.get("interpreter", {}).get(
        "relativePath"
    ) != expected_interpreter:
        fail("Plan-Interpreterpfad ist ungültig.")

    if plan.get("manifest", {}).get(
        "installationAllowed"
    ) is not False:
        fail("Plan darf keine Dependency-Installation erlauben.")

    if plan.get("evidence", {}).get(
        "collectionAllowed"
    ) is not False:
        fail("Plan darf keine Nachweiserfassung erlauben.")

    if plan.get("rollback", {}).get(
        "executionAllowed"
    ) is not False:
        fail("Plan darf keinen Rollback ausführen.")

    if plan.get("authorization") != {
        "requiredLater": True,
        "recorded": False,
    }:
        fail("Plan-Autorisierungsgrenze ist ungültig.")

for relative in (
    ".venv-disposable-postgresql",
    "tools/test-environments/disposable-postgresql",
    "tools/test-environments/disposable-postgresql-venv",
):
    if (ROOT / relative).exists():
        fail(
            "v27.32j darf keine Test-Python-Umgebung "
            f"materialisieren: {relative}"
        )

if list(MIGRATIONS.glob("*v2732j*.sql")):
    fail("v27.32j darf keine SQL-Migration erzeugen.")

print("Disposable Test-Python-Materialisierungsplan: OK")
print("Quellvertrag: v27.32i")
print("Eingabe: gültiger v27.32h-Descriptor plus Planfakten")
print("Ergebnis: plan_ready_execution_locked")
print("argv: strukturiert, ohne Shell")
print("Ziel- und Interpreterbindung: geprüft")
print("Nachweisplan: vorhanden, Ausführung gesperrt")
print("Rollbackplan: vorhanden, Ausführung gesperrt")
print("Menschliche Freigabe: später erforderlich, nicht erfasst")
print("Dateisystemzugriff: keiner")
print("Prozessausführung: keine")
print("Virtuelle Umgebung erstellt: nein")
print("Dependency installiert: nein")
print("Treiber importiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32j: keine")
print("Produktive Freigabe: nein")
