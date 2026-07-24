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
        "test-python-environment-descriptor-resolver-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-python-environment-readiness-contract.json"
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


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(
        "accaoui_disposable_test_python_environment_descriptor_v2732h",
        path,
    )

    if spec is None or spec.loader is None:
        fail("Descriptor-Resolver ist nicht ladbar.")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


contract = load_json(
    CONTRACT,
    "v27.32h-Descriptor-Resolver-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32g-Test-Python-Umgebungsvertrag",
)

if contract.get("version") != "v27.32h":
    fail("Descriptor-Vertrag besitzt nicht v27.32h.")
if contract.get("contractVersion") != 1:
    fail("Descriptor-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "implemented_pure_descriptor_creation_locked"
):
    fail("Descriptor-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Descriptor-Vertrag darf nicht produktiv sein.")

if source.get("version") != "v27.32g":
    fail("Quellvertrag besitzt nicht v27.32g.")
if source.get("implementation", {}).get(
    "virtualEnvironmentCreated"
) is not False:
    fail("Quellvertrag hat unerwartet eine Umgebung erstellt.")

if MANIFEST.read_bytes() != b"psycopg[binary]==3.3.4\n":
    fail("Isoliertes Manifest ist ungültig.")

implementation = contract.get("implementation", {})
if implementation.get(
    "environmentDescriptorResolverImplemented"
) is not True:
    fail("Descriptor-Resolver ist nicht implementiert.")

for key in (
    "environmentMaterializationImplemented",
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

resolver_source = RESOLVER.read_text(encoding="utf-8")
try:
    tree = ast.parse(resolver_source)
except SyntaxError as exc:
    fail(f"Descriptor-Resolver besitzt Syntaxfehler: {exc}")

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
    fail(f"Descriptor-Resolver besitzt unerlaubte Importe: {unexpected_imports}")

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
        fail(f"Descriptor-Resolver verwendet verbotenen Namen: {node.id}")

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
                "Descriptor-Resolver besitzt verbotenen "
                f"Dateisystemaufruf: {node.func.attr}"
            )

lower_source = resolver_source.lower()
for marker in (
    "pip install",
    "python -m pip",
    "py -m pip",
    "python -m venv",
    "py -m venv",
    ".connect(",
    "postgres://",
    "postgresql://",
    "database_url",
    "service_role",
):
    if marker in lower_source:
        fail(f"Descriptor-Resolver enthält verbotenen Inhalt: {marker}")

module = load_module(RESOLVER)
resolve = getattr(
    module,
    "resolve_test_python_environment_descriptor",
    None,
)

if not callable(resolve):
    fail("Descriptor-Resolver-Funktion fehlt.")

valid_windows = {
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

valid_posix = {
    **valid_windows,
    "platform": "posix",
    "environmentRoot": "/tmp/accaoui-test-envs/postgresql",
    "repositoryRoot": "/srv/accaoui/v4-dashboard",
}

cases = [
    (
        [],
        "blocked",
        "test_environment_descriptor_invalid_input",
    ),
    (
        {
            key: value
            for key, value in valid_windows.items()
            if key != "platform"
        },
        "blocked",
        "test_environment_descriptor_missing_fields",
    ),
    (
        {
            **valid_windows,
            "unexpected": True,
        },
        "blocked",
        "test_environment_descriptor_unknown_fields",
    ),
    (
        {
            **valid_windows,
            "environmentRoot": r"relative\env",
        },
        "blocked",
        "test_environment_root_not_absolute",
    ),
    (
        {
            **valid_windows,
            "environmentRoot": (
                r"C:\xampp\htdocs\accaoui\v4-dashboard\test-env"
            ),
        },
        "blocked",
        "test_environment_inside_repository_forbidden",
    ),
    (
        {
            **valid_windows,
            "environmentRootKind": "system",
        },
        "blocked",
        "test_environment_system_location_forbidden",
    ),
    (
        {
            **valid_windows,
            "requestedPythonVersion": "3.15",
        },
        "blocked",
        "test_environment_python_version_unsupported",
    ),
    (
        {
            **valid_windows,
            "requestedPythonVersion": "3.12",
        },
        "blocked",
        "test_environment_python_version_mismatch",
    ),
    (
        {
            **valid_windows,
            "includeSystemSitePackages": True,
        },
        "blocked",
        "test_environment_system_site_packages_forbidden",
    ),
    (
        {
            **valid_windows,
            "allowUserSitePackages": True,
        },
        "blocked",
        "test_environment_user_site_packages_forbidden",
    ),
    (
        {
            **valid_windows,
            "pythonNoUserSite": False,
        },
        "blocked",
        "test_environment_python_no_user_site_required",
    ),
    (
        {
            **valid_windows,
            "inheritPythonPath": True,
        },
        "blocked",
        "test_environment_python_path_inheritance_forbidden",
    ),
    (
        {
            **valid_windows,
            "inheritVirtualEnv": True,
        },
        "blocked",
        "test_environment_virtual_env_inheritance_forbidden",
    ),
    (
        valid_windows,
        "descriptor_ready_creation_locked",
        "test_environment_descriptor_ready_creation_locked",
    ),
    (
        valid_posix,
        "descriptor_ready_creation_locked",
        "test_environment_descriptor_ready_creation_locked",
    ),
]

for facts, expected_status, expected_reason in cases:
    before = dict(facts) if isinstance(facts, dict) else facts
    first = resolve(facts)
    second = resolve(facts)

    if first != second:
        fail("Descriptor-Resolver ist nicht deterministisch.")

    if isinstance(facts, dict) and facts != before:
        fail("Descriptor-Resolver verändert die Eingabe.")

    if first.get("status") != expected_status:
        fail(f"Descriptor-Status ist ungültig: {first}")

    if first.get("reason") != expected_reason:
        fail(f"Descriptor-Grund ist ungültig: {first}")

    for key in (
        "environmentCreationAllowed",
        "processExecutionAllowed",
        "dependencyInstallationAllowed",
    ):
        if first.get(key) is not False:
            fail(f"Descriptor-Ausführungsgrenze ist offen: {key}")

for facts in (valid_windows, valid_posix):
    result = resolve(facts)
    descriptor = result.get("descriptor")

    if not isinstance(descriptor, dict):
        fail("Gültiger Descriptor fehlt.")

    expected_interpreter = (
        "Scripts/python.exe"
        if facts["platform"] == "windows"
        else "bin/python"
    )

    if descriptor.get(
        "interpreterRelativePath"
    ) != expected_interpreter:
        fail("Descriptor-Interpreterpfad ist ungültig.")

    if descriptor.get("pythonVersion") != "3.13":
        fail("Descriptor-Pythonversion ist ungültig.")

    if descriptor.get(
        "manifestRequirement"
    ) != "psycopg[binary]==3.3.4":
        fail("Descriptor-Manifestbindung ist ungültig.")

for relative in (
    ".venv-disposable-postgresql",
    "tools/test-environments/disposable-postgresql",
    "tools/test-environments/disposable-postgresql-venv",
):
    if (ROOT / relative).exists():
        fail(
            "v27.32h darf keine Test-Python-Umgebung "
            f"materialisieren: {relative}"
        )

if list(MIGRATIONS.glob("*v2732h*.sql")):
    fail("v27.32h darf keine SQL-Migration erzeugen.")

print("Disposable Test-Python-Umgebungsdescriptor: OK")
print("Eingabe: ausschließlich übergebenes Mapping")
print("Plattformen: Windows und POSIX")
print("Pfadprüfung: rein lexikalisch")
print("Dateisystemzugriff: keiner")
print("Eingabemutation: nein")
print("Gültiger Status: descriptor_ready_creation_locked")
print("Umgebung erstellt: nein")
print("Interpreter ausgeführt: nein")
print("Dependency installiert: nein")
print("Treiber importiert: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32h: keine")
print("Produktive Freigabe: nein")
