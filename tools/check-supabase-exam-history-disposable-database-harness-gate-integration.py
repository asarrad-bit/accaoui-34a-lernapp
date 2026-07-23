from pathlib import Path
import ast, json, os, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
HARNESS=ROOT/"tools"/"run-supabase-exam-history-outer-domain-mutation-harness.py"
CONTRACT=ROOT/"docs"/"contracts"/"exam-history-disposable-database-harness-gate-integration-contract.json"
SOURCE=ROOT/"docs"/"contracts"/"exam-history-disposable-database-gate-evaluator-adapter-readiness-contract.json"
def fail(m): print("FEHLER:",m); raise SystemExit(1)
def load(p):
    try:return json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:fail(f"JSON ungültig: {p}: {e}")
c=load(CONTRACT); s=load(SOURCE)
if c.get("version")!="v27.32b":fail("Integrationsvertrag besitzt nicht v27.32b.")
if s.get("version")!="v27.32a":fail("Quellvertrag besitzt nicht v27.32a.")
if c.get("productiveReleaseAllowed") is not False:fail("Produktive Freigabe offen.")
i=c.get("implementation",{})
if i.get("harnessGateIntegrationImplemented") is not True:fail("Integration fehlt.")
for k in ("databaseDriverPresent","databaseConnectionCreated","databaseTestExecuted","sqlMigrationCreated","frontendIntegration"):
    if i.get(k) is not False:fail(f"Implementierungsgrenze offen: {k}")
src=HARNESS.read_text(encoding="utf-8")
ast.parse(src)
for m in ("DISPOSABLE_GATE_KEYS","evaluate_environment","build_connection_adapter_readiness",
          "Gate-Entscheidung:","Gate-Grund:","Adapterstatus:","Adaptergrund:",
          "Datenbanktreiber geladen: nein","Datenbankverbindung geöffnet: nein",
          "Netzwerkzugriff: nein","Datenbanktest ausgeführt: nein"):
    if m not in src:fail(f"Harness-Marker fehlt: {m}")
for m in ("psycopg","asyncpg","requests","urllib","http.client","socket",".connect(",
          "create_connection","getaddrinfo","postgres://","postgresql://","service_role","database_url"):
    if m in src.lower():fail(f"Verbotener Verbindungsinhalt: {m}")
base={k:v for k,v in os.environ.items() if not k.startswith("ACCAOUI_DB_TEST_")}
def run(args,env):
    return subprocess.run([sys.executable,str(HARNESS),*args],cwd=ROOT,text=True,capture_output=True,env=env)
def require(result,code,markers,label):
    if result.returncode!=code:fail(f"{label}: Exitcode {result.returncode} statt {code}\n{result.stdout}\n{result.stderr}")
    for m in markers:
        if m not in result.stdout:fail(f"{label}: Ausgabe fehlt: {m}")
require(run(["--validate-only"],base),0,["Harness-Modus: validate_only"],"validate")
require(run(["--run-database"],base),2,[
 "Gate-Entscheidung: deny","Gate-Grund: environment_gate_not_configured",
 "Adapterstatus: blocked","Adaptergrund: environment_gate_not_configured"],"leer")
valid={**base,"ACCAOUI_DB_TEST_MODE":"disposable","ACCAOUI_DB_TEST_TARGET_KIND":"local_postgres",
 "ACCAOUI_DB_TEST_HOST":"localhost","ACCAOUI_DB_TEST_PORT":"5432",
 "ACCAOUI_DB_TEST_DATABASE":"accaoui_exam_history_disposable_test",
 "ACCAOUI_DB_TEST_CONFIRM":"DESTROY_SYNTHETIC_TEST_DATA"}
require(run(["--run-database"],valid),2,[
 "Gate-Entscheidung: eligible_but_connection_locked","Gate-Grund: adapter_not_implemented",
 "Adapterstatus: descriptor_valid_connection_locked","Adaptergrund: database_driver_not_selected"],"gültig")
remote={**valid,"ACCAOUI_DB_TEST_HOST":"remote.example"}
require(run(["--run-database"],remote),2,[
 "Gate-Entscheidung: deny","Gate-Grund: remote_target_forbidden",
 "Adapterstatus: blocked","Adaptergrund: remote_target_forbidden"],"remote")
if list((ROOT/"supabase"/"migrations").glob("*v2732b*.sql")):fail("v27.32b darf keine SQL-Migration erzeugen.")
print("Disposable Harness-Gate-Integration: OK")
print("Validate-only: erfolgreich")
print("Leere Umgebung: geschlossen abgelehnt")
print("Loopback: klassifiziert, Verbindung gesperrt")
print("Remote: geschlossen abgelehnt")
print("Datenbanktreiber/Verbindung/Test: nein")
