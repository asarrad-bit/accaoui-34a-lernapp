from pathlib import Path
import hashlib
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
        "test-dependency-manifest-materialization-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "test-dependency-manifest-contract.json"
    )
)
MANIFEST = (
    ROOT
    / "tools"
    / "test-dependencies"
    / "disposable-postgresql-requirements.txt"
)

EXPECTED = b"psycopg[binary]==3.3.4\n"


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
    "v27.32f-Manifest-Materialisierungsvertrag",
)
source = load_json(
    SOURCE,
    "v27.32e-Manifest-Vertrag",
)

if contract.get("version") != "v27.32f":
    fail("Materialisierungsvertrag besitzt nicht v27.32f.")
if contract.get("contractVersion") != 1:
    fail("Materialisierungsvertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "materialized_isolated_not_installed_not_live"
):
    fail("Materialisierungsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Materialisierung darf nicht produktiv sein.")
if source.get("version") != "v27.32e":
    fail("Quellvertrag besitzt nicht v27.32e.")

implementation = contract.get("implementation", {})
if implementation.get("manifestMaterialized") is not True:
    fail("Manifest ist nicht als materialisiert markiert.")
if implementation.get(
    "dependencyDeclaredInIsolatedManifest"
) is not True:
    fail("Isolierte Dependency ist nicht deklariert.")

for key in (
    "dependencyInstalled",
    "installerImplemented",
    "driverImported",
    "connectionAdapterImplemented",
    "databaseConnectionCreated",
    "databaseTestExecuted",
    "sqlMigrationCreated",
    "frontendIntegration",
):
    if implementation.get(key) is not False:
        fail(f"Implementierungsgrenze ist offen: {key}")

if not MANIFEST.is_file():
    fail("Isoliertes Test-Dependency-Manifest fehlt.")

raw = MANIFEST.read_bytes()
if raw != EXPECTED:
    fail("Manifestinhalt ist nicht exakt freigegeben.")
if raw.startswith(b"\xef\xbb\xbf"):
    fail("Manifest darf keine UTF-8-BOM enthalten.")
if b"\r" in raw:
    fail("Manifest darf keine CR/CRLF-Zeilenenden enthalten.")
if hashlib.sha256(raw).hexdigest() != contract.get(
    "manifestIntegrity", {}
).get("sha256"):
    fail("Manifest-SHA-256 stimmt nicht.")

lines = raw.decode("utf-8").splitlines()
if lines != ["psycopg[binary]==3.3.4"]:
    fail("Manifest muss exakt eine nichtleere Dependency enthalten.")

for relative in (
    "requirements.txt",
    "requirements-dev.txt",
    "pyproject.toml",
    "Pipfile",
    "poetry.lock",
    "setup.cfg",
    "package.json",
    "package-lock.json",
):
    path = ROOT / relative
    if not path.is_file():
        continue

    if "psycopg" in path.read_text(
        encoding="utf-8",
        errors="replace",
    ).lower():
        fail(
            "Treiber wurde außerhalb des isolierten Manifests "
            f"deklariert: {relative}"
        )

runtime_paths = (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
    ROOT / "tools"
    / "run-supabase-exam-history-outer-domain-mutation-harness.py",
)

for path in runtime_paths:
    content = path.read_text(
        encoding="utf-8",
        errors="replace",
    ).lower()

    if MANIFEST.name.lower() in content:
        fail(
            "Isoliertes Manifest wird unerwartet von Runtime "
            f"referenziert: {path.name}"
        )

preflight = (ROOT / "tools" / "preflight.py").read_text(
    encoding="utf-8",
    errors="replace",
).lower()

for marker in (
    "pip install",
    "python -m pip",
    "py -m pip",
    "-r tools/test-dependencies",
    "--requirement tools/test-dependencies",
):
    if marker in preflight:
        fail(f"Preflight enthält unerlaubte Installation: {marker}")

if list(MIGRATIONS.glob("*v2732f*.sql")):
    fail("v27.32f darf keine SQL-Migration erzeugen.")

print("Disposable PostgreSQL-Test-Manifest-Materialisierung: OK")
print("Manifest: exakt eine Dependency")
print("Dependency: psycopg[binary]==3.3.4")
print("UTF-8-BOM: nein")
print("Zeilenende: LF")
print("Automatische Installation: nein")
print("Treiber installiert: nein")
print("Treiber importiert: nein")
print("Runtime-/Frontend-Nutzung: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32f: keine")
print("Produktive Freigabe: nein")
