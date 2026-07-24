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
        "test-dependency-manifest-contract.json"
    )
)
SOURCE = (
    ROOT
    / "docs"
    / "contracts"
    / (
        "exam-history-disposable-postgresql-"
        "driver-readiness-contract.json"
    )
)
FUTURE_MANIFEST = (
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
    "v27.32e-Test-Dependency-Manifest-Vertrag",
)
source = load_json(
    SOURCE,
    "v27.32d-Treiber-Readiness-Vertrag",
)

if contract.get("version") != "v27.32e":
    fail("Manifest-Vertrag besitzt nicht v27.32e.")
if contract.get("contractVersion") != 1:
    fail("Manifest-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != (
    "planned_isolated_not_materialized_not_live"
):
    fail("Manifest-Vertragsstatus ist ungültig.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Manifest-Vertrag darf nicht produktiv sein.")
if source.get("version") != "v27.32d":
    fail("Quellvertrag besitzt nicht v27.32d.")

implementation = contract.get("implementation", {})
for key in (
    "manifestMaterialized",
    "dependencyDeclared",
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

if implementation.get("manifestContractImplemented") is not True:
    fail("Manifest-Vertrag ist nicht als implementiert markiert.")

manifest = contract.get("manifestBoundary", {})
if manifest.get("futurePath") != (
    "tools/test-dependencies/"
    "disposable-postgresql-requirements.txt"
):
    fail("Zukünftiger Manifestpfad ist ungültig.")
if manifest.get("requiredDependency") != (
    "psycopg[binary]==3.3.4"
):
    fail("Erlaubte Dependency ist ungültig.")
if manifest.get("allowedDependencyCount") != 1:
    fail("Dependency-Anzahl ist ungültig.")
if manifest.get("exactPinRequired") is not True:
    fail("Exakte Versionsbindung fehlt.")

if FUTURE_MANIFEST.exists():
    fail(
        "v27.32e darf das zukünftige Manifest "
        "noch nicht materialisieren."
    )

for relative in contract.get("forbiddenDeclarationPaths", []):
    path = ROOT / relative
    if not path.is_file():
        continue

    content = path.read_text(
        encoding="utf-8",
        errors="replace",
    ).lower()

    if "psycopg" in content:
        fail(
            "Treiber wurde in verbotenem Dependency-Pfad "
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

    if FUTURE_MANIFEST.name.lower() in content:
        fail(
            "Zukünftiges Test-Manifest wird unerwartet "
            f"referenziert: {path.name}"
        )

if list(MIGRATIONS.glob("*v2732e*.sql")):
    fail("v27.32e darf keine SQL-Migration erzeugen.")

serialized = json.dumps(contract, ensure_ascii=False).lower()
for marker in (
    "postgres://",
    "postgresql://",
    "service_role",
    '"password"',
    '"secret"',
    '"databaseurl"',
):
    if marker in serialized:
        fail(f"Manifest-Vertrag enthält verbotenen Inhalt: {marker}")

print("Disposable PostgreSQL-Test-Dependency-Manifest-Vertrag: OK")
print("Zukünftiger Pfad: tools/test-dependencies/")
print("Exakte Dependency: psycopg[binary]==3.3.4")
print("Manifest materialisiert: nein")
print("Standard-Dependencies verändert: nein")
print("Treiber installiert: nein")
print("Treiber importiert: nein")
print("Netzwerkzugriff: nein")
print("Datenbankverbindung: keine")
print("SQL-Migration v27.32e: keine")
print("Produktive Freigabe: nein")
