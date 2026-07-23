from pathlib import Path
import ast, importlib.util, json, sys
from importlib import metadata

ROOT=Path(__file__).resolve().parents[1]
CON=ROOT/"docs/contracts/exam-history-disposable-postgresql-driver-readiness-contract.json"
SRC=ROOT/"docs/contracts/exam-history-disposable-postgresql-driver-selection-contract.json"
RES=ROOT/"tools/accaoui_disposable_postgresql_driver_readiness.py"

def fail(m): print("FEHLER:",m); raise SystemExit(1)
def load(p):
    try:return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:fail(f"JSON ungültig: {p}: {e}")

c=load(CON); s=load(SRC)
if c.get("version")!="v27.32d":fail("Readiness-Vertrag besitzt nicht v27.32d.")
if s.get("version")!="v27.32c":fail("Quellvertrag besitzt nicht v27.32c.")
if c.get("productiveReleaseAllowed") is not False:fail("Produktive Freigabe offen.")
i=c.get("implementation",{})
for k in ("driverImported","driverInstalledByProject","dependencyFileModified",
          "connectionAdapterImplemented","databaseConnectionCreated",
          "databaseTestExecuted","sqlMigrationCreated","frontendIntegration"):
    if i.get(k) is not False:fail(f"Implementierungsgrenze offen: {k}")
if i.get("metadataResolverImplemented") is not True:fail("Resolver nicht implementiert.")

src=RES.read_text(encoding="utf-8")
tree=ast.parse(src)
allowed={"__future__","importlib","typing"}
seen=set()
for n in ast.walk(tree):
    if isinstance(n,ast.Import):
        for a in n.names:seen.add(a.name.split(".",1)[0])
    elif isinstance(n,ast.ImportFrom) and n.module:
        seen.add(n.module.split(".",1)[0])
if seen-allowed:fail(f"Unerlaubte Importe: {seen-allowed}")
for n in ast.walk(tree):
    if isinstance(n,ast.Import):
        names=[a.name for a in n.names]
    elif isinstance(n,ast.ImportFrom) and n.module:
        names=[n.module]
    else:
        continue
    if any(x=="psycopg" or x.startswith("psycopg.") for x in names):
        fail("Treiber wird unerwartet importiert.")

spec=importlib.util.spec_from_file_location("v2732d",RES)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
resolve=m.resolve_driver_readiness

def missing(_): raise metadata.PackageNotFoundError("psycopg")
def badmeta(_): raise RuntimeError("synthetic")
def wrong(_): return "3.3.3"
def exact(_): return "3.3.4"

cases=[
 (missing,"blocked","driver_not_installed",None),
 (badmeta,"blocked","driver_metadata_unavailable",None),
 (wrong,"blocked","driver_version_mismatch","3.3.3"),
 (exact,"metadata_ready_import_locked","driver_import_not_authorized","3.3.4"),
]
for reader,status,reason,installed in cases:
    a=resolve(reader); b=resolve(reader)
    if a!=b:fail("Resolver ist nicht deterministisch.")
    if a.get("status")!=status or a.get("reason")!=reason:fail(f"Falsches Ergebnis: {a}")
    if a.get("installedVersion")!=installed:fail(f"Falsche Version: {a}")
    if a.get("driverImportAttempted") is not False:fail("Treiberimport versucht.")
    if a.get("connectionAllowed") is not False:fail("Verbindung erlaubt.")

for p in ("requirements.txt","requirements-dev.txt","pyproject.toml","Pipfile","poetry.lock","setup.cfg"):
    q=ROOT/p
    if q.is_file() and "psycopg" in q.read_text(encoding="utf-8",errors="replace").lower():
        fail(f"Dependency unerwartet deklariert: {p}")

if list((ROOT/"supabase/migrations").glob("*v2732d*.sql")):
    fail("v27.32d darf keine SQL-Migration erzeugen.")

print("Disposable PostgreSQL-Treiber-Readiness: OK")
print("Metadatenquelle: importlib.metadata.version")
print("Zielversion: 3.3.4")
print("Treiber importiert: nein")
print("Dependency installiert oder deklariert: nein")
print("Datenbankverbindung: keine")
print("Produktive Freigabe: nein")
