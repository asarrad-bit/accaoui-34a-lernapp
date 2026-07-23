from pathlib import Path
import json
import re
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT_PATH = (
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


contract = read_json(
    CONTRACT_PATH,
    "Synthetischer Fixture- und Harness-Vertrag",
)

if contract.get("version") != "v27.31x":
    fail("Fixture-/Harness-Vertrag besitzt nicht v27.31x.")
if contract.get("contractVersion") != 1:
    fail("Fixture-/Harness-Vertrag besitzt nicht Schema 1.")
if contract.get("status") != "prepared_not_live":
    fail("Fixture-/Harness-Vertrag ist nicht vorbereitet.")
if contract.get("productiveReleaseAllowed") is not False:
    fail("Fixture-/Harness-Vertrag darf nicht produktiv sein.")
if contract.get("fixtureType") != (
    "deterministic_synthetic_fixture_harness_contract"
):
    fail("Fixture-/Harness-Vertrag besitzt falschen Typ.")

implementation = contract.get("implementation", {})
if implementation != {
    "databaseTestContractPath": (
        "docs/contracts/"
        "exam-history-outer-domain-mutation-database-test-contract.json"
    ),
    "fixtureHarnessCheckerPath": (
        "tools/"
        "check-supabase-exam-history-"
        "outer-domain-mutation-fixture-harness-contract.py"
    ),
    "fixtureHarnessDocumentPath": (
        "docs/"
        "SUPABASE_EXAM_RESULT_HISTORY_"
        "OUTER_DOMAIN_MUTATION_FIXTURE_HARNESS_CONTRACT.md"
    ),
    "fixtureCatalogImplemented": False,
    "databaseHarnessImplemented": False,
    "databaseConnectionCreated": False,
    "databaseTestExecuted": False,
    "sqlMigrationCreated": False,
    "frontendIntegration": False,
}:
    fail("Fixture-/Harness-Implementierungsgrenze ist ungültig.")

safety = contract.get("safetyBoundary", {})
if safety != {
    "syntheticValuesOnly": True,
    "realParticipantDataAllowed": False,
    "realEmailAddressesAllowed": False,
    "realNamesAllowed": False,
    "productionSecretsAllowed": False,
    "databaseUrlStoredAllowed": False,
    "serviceRoleKeyStoredAllowed": False,
    "frontendReferenceAllowed": False,
    "networkExecutionAllowed": False,
}:
    fail("Fixture-/Harness-Sicherheitsgrenze ist ungültig.")

users = contract.get("users")
expected_users = [
    {
        "id": "user_alpha",
        "authUserId": "00000000-0000-4000-8000-000000000101",
        "purpose": "primary_owner",
    },
    {
        "id": "user_beta",
        "authUserId": "00000000-0000-4000-8000-000000000102",
        "purpose": "cross_user_isolation",
    },
]
if users != expected_users:
    fail("Synthetische Testnutzer sind nicht deterministisch.")

user_ids = set()
auth_user_ids = set()
for user in users:
    user_id = user["id"]
    auth_user_id = user["authUserId"]

    if user_id in user_ids:
        fail(f"Doppelte Fixture-Nutzer-ID: {user_id}")
    user_ids.add(user_id)

    try:
        parsed = uuid.UUID(auth_user_id)
    except ValueError:
        fail(f"Ungültige synthetische Nutzer-UUID: {auth_user_id}")

    if parsed.version != 4:
        fail(f"Synthetische Nutzer-UUID ist nicht Version 4: {auth_user_id}")
    if auth_user_id in auth_user_ids:
        fail(f"Doppelte synthetische Nutzer-UUID: {auth_user_id}")
    auth_user_ids.add(auth_user_id)

resources = contract.get("resources")
if not isinstance(resources, list) or len(resources) != 5:
    fail("Ressourcenfixture-Katalog ist unvollständig.")

resource_ids = set()
resource_identities = set()
allowed_scopes = {"snapshot", "cycle_registry"}
for resource in resources:
    resource_id = resource.get("id")
    identity = resource.get("resourceIdentity")
    scope = resource.get("operationScope")
    owner = resource.get("ownerUserId")

    if resource_id in resource_ids:
        fail(f"Doppelte Ressourcen-ID: {resource_id}")
    resource_ids.add(resource_id)

    if identity in resource_identities:
        fail(f"Doppelte Ressourcenidentität: {identity}")
    resource_identities.add(identity)

    if not isinstance(identity, str) or not identity.startswith("fixture:"):
        fail(f"Nicht synthetische Ressourcenidentität: {identity}")
    if scope not in allowed_scopes:
        fail(f"Ungültiger Fixture-Bereich: {scope}")
    if owner not in user_ids:
        fail(f"Unbekannter Fixture-Eigentümer: {owner}")

client_keys = contract.get("clientRequestKeys")
expected_key_names = {
    "snapshot_create",
    "snapshot_retry",
    "snapshot_update",
    "snapshot_delete",
    "snapshot_failed",
    "registry_create",
    "concurrent_write_a",
    "concurrent_write_b",
    "concurrent_create_a",
    "concurrent_create_b",
    "unexpected_failure",
}
if set(client_keys) != expected_key_names:
    fail("Client-Wiederholungsschlüssel-Katalog ist unvollständig.")

client_key_values = list(client_keys.values())
if len(client_key_values) != len(set(client_key_values)):
    fail("Client-Wiederholungsschlüssel sind nicht eindeutig.")
for name, value in client_keys.items():
    if not re.fullmatch(r"[0-9a-f]{64}", value):
        fail(f"Client-Wiederholungsschlüssel ist nicht 256 Bit: {name}")

payloads = contract.get("payloads")
expected_payload_ids = {
    "snapshot_v1",
    "snapshot_v2",
    "snapshot_concurrent_a",
    "snapshot_concurrent_b",
    "cycle_registry_v1",
    "delete",
}
if set(payloads) != expected_payload_ids:
    fail("Fixture-Payload-Katalog ist unvollständig.")
if payloads["delete"] is not None:
    fail("Delete-Fixture muss null sein.")

for payload_id, payload in payloads.items():
    if payload_id == "delete":
        continue

    if payload.get("schema_version") != 1:
        fail(f"Fixture-Schema-Version ist ungültig: {payload_id}")

    keys = set(payload)
    if payload_id.startswith("snapshot"):
        if keys != {"schema_version", "snapshot"}:
            fail(f"Snapshot-Fixture-Hülle ist ungültig: {payload_id}")
    elif payload_id == "cycle_registry_v1":
        if keys != {"schema_version", "registry"}:
            fail("Zyklusregister-Fixture-Hülle ist ungültig.")

    canonical_bytes = len(
        json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        ).encode("utf-8")
    )
    if canonical_bytes > 131072:
        fail(f"Fixture-Payload ist unerwartet groß: {payload_id}")

versions = contract.get("expectedVersions")
if versions != {
    "create": 0,
    "afterCreate": 1,
    "afterUpdate": 2,
    "afterDelete": 3,
    "stale": 0,
}:
    fail("Deterministische Versionsfixture-Werte sind ungültig.")

scenarios = contract.get("scenarios")
if not isinstance(scenarios, list) or len(scenarios) != 7:
    fail("Fixture-Szenariokatalog ist unvollständig.")

scenario_ids = set()
for scenario in scenarios:
    scenario_id = scenario.get("id")
    if scenario_id in scenario_ids:
        fail(f"Doppelte Szenario-ID: {scenario_id}")
    scenario_ids.add(scenario_id)

    if scenario.get("userId") not in user_ids:
        fail(f"Unbekannter Szenarionutzer: {scenario_id}")
    if scenario.get("resourceId") not in resource_ids:
        fail(f"Unbekannte Szenarioressource: {scenario_id}")
    if scenario.get("clientKeyId") not in client_keys:
        fail(f"Unbekannter Szenario-Clientschlüssel: {scenario_id}")
    if scenario.get("payloadId") not in payloads:
        fail(f"Unbekannter Szenario-Payload: {scenario_id}")
    if scenario.get("operation") not in {"write", "delete"}:
        fail(f"Ungültige Szenariooperation: {scenario_id}")

    expected_version = scenario.get("expectedStorageVersion")
    if not isinstance(expected_version, int) or expected_version < 0:
        fail(f"Ungültiger Szenario-Versionsstand: {scenario_id}")

    has_outcome = "expectedOutcome" in scenario
    has_failure = "expectedFailureCode" in scenario
    if has_outcome == has_failure:
        fail(
            "Szenario muss exakt Ergebnis oder Fehler besitzen: "
            f"{scenario_id}"
        )

required_scenarios = {
    "snapshot_create_completed",
    "snapshot_identical_retry",
    "snapshot_update_exact",
    "snapshot_stale_update",
    "snapshot_delete_exact",
    "cycle_registry_create",
    "cross_user_isolation",
}
if scenario_ids != required_scenarios:
    fail("Fixture-Szenariomatrix ist nicht kanonisch.")

barriers = contract.get("concurrencyBarriers")
if not isinstance(barriers, list) or len(barriers) != 2:
    fail("Konkurrenzbarrieren sind unvollständig.")

barrier_ids = set()
for barrier in barriers:
    barrier_id = barrier.get("id")
    if barrier_id in barrier_ids:
        fail(f"Doppelte Konkurrenzbarriere: {barrier_id}")
    barrier_ids.add(barrier_id)

    if barrier.get("parties") != 2:
        fail(f"Konkurrenzbarriere besitzt nicht zwei Parteien: {barrier_id}")
    if barrier.get("resourceId") not in resource_ids:
        fail(f"Unbekannte Barrierenressource: {barrier_id}")
    if barrier.get("releaseMode") != "simultaneous":
        fail(f"Barriere ist nicht gleichzeitig: {barrier_id}")
    if barrier.get("timeoutSeconds") != 10:
        fail(f"Barrieren-Timeout ist nicht deterministisch: {barrier_id}")
    if barrier.get("expectedWinnerCount") != 1:
        fail(f"Barriere besitzt falsche Gewinnerzahl: {barrier_id}")
    if barrier.get("expectedConflictCount") != 1:
        fail(f"Barriere besitzt falsche Konfliktzahl: {barrier_id}")

    key_ids = barrier.get("clientKeyIds")
    payload_ids = barrier.get("payloadIds")
    if len(key_ids) != 2 or len(set(key_ids)) != 2:
        fail(f"Barrieren-Clientschlüssel sind ungültig: {barrier_id}")
    if len(payload_ids) != 2:
        fail(f"Barrieren-Payloads sind ungültig: {barrier_id}")
    if any(key_id not in client_keys for key_id in key_ids):
        fail(f"Barriere referenziert unbekannten Clientschlüssel: {barrier_id}")
    if any(payload_id not in payloads for payload_id in payload_ids):
        fail(f"Barriere referenziert unbekannten Payload: {barrier_id}")

if barrier_ids != {
    "same_version_write_barrier",
    "same_identity_create_barrier",
}:
    fail("Konkurrenzbarrieren sind nicht kanonisch.")

lifecycle = contract.get("harnessLifecycle")
if lifecycle != {
    "migrationOrderSource": "supabase/migrations_filename_order",
    "resetBeforeEachScenario": True,
    "seedSyntheticAuthUsers": True,
    "setAuthUidOnlyInsideTransaction": True,
    "inspectInternalTablesOnlyAfterClientResponse": True,
    "rollbackScenarioTransactionAfterAssertions": True,
    "persistFixtureRowsBetweenScenarios": False,
    "parallelWorkersForBarrier": 2,
}:
    fail("Harness-Lebenszyklus ist ungültig.")

fault = contract.get("faultInjectionContract")
if fault != {
    "label": "after_domain_mutation_before_idempotency_completion",
    "clientSelectable": False,
    "productionCodeHookAllowed": False,
    "testHarnessOnly": True,
    "mechanismImplemented": False,
}:
    fail("Test-Fehlerinjektionsvertrag ist ungültig.")

if contract.get("unresolvedRequirements") != {
    "fixtureCatalogImplementation": True,
    "databaseHarnessImplementation": True,
    "testOnlyFaultInjectionImplementation": True,
    "databaseTestExecution": True,
    "concurrencyTestExecution": True,
    "authorizationTestExecution": True,
    "directAppExecutionGrant": True,
    "frontendIntegration": True,
}:
    fail("Offene Fixture-/Harness-Anforderungen sind ungültig.")

database_test = read_json(
    DATABASE_TEST_CONTRACT_PATH,
    "Äußerer Fachmutations-Datenbank-Testvertrag",
)
if database_test.get("version") != "v27.31w":
    fail("Datenbank-Testvertrag besitzt nicht v27.31w.")
if database_test.get("productiveReleaseAllowed") is not False:
    fail("Datenbank-Testvertrag ist unerwartet produktiv.")
if database_test.get("implementation", {}).get(
    "databaseTestExecuted"
) is not False:
    fail("Datenbanktest wurde unerwartet ausgeführt.")

serialized = json.dumps(contract, ensure_ascii=False).lower()
for forbidden in (
    "postgres://",
    "postgresql://",
    "supabase.co",
    "service_role",
    "eyj",
    "@",
    "participant_id",
    '"email"',
    '"name"',
):
    if forbidden in serialized:
        fail(f"Fixture-Vertrag enthält verbotenen Inhalt: {forbidden}")

v2731x_sql_files = sorted(
    path.name for path in MIGRATIONS.glob("*v2731x*.sql")
)
if v2731x_sql_files:
    fail(
        "v27.31x ist nur ein Fixture-/Harness-Vertrag und darf "
        f"keine SQL-Migration erzeugen: {v2731x_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend = frontend_path.read_text(encoding="utf-8").lower()
    if CONTRACT_PATH.name.lower() in frontend:
        fail(
            "Fixture-/Harness-Vertrag wird im Frontend geladen: "
            f"{frontend_path.name}"
        )

print("Synthetischer Fixture- und Harness-Vertrag: OK")
print("Testnutzer: zwei feste synthetische UUID-v4-Identitäten")
print("Ressourcen: Snapshot und Zyklusregister deterministisch")
print("Client-Schlüssel: eindeutig und 256 Bit")
print("Payloads: kanonische Snapshot-, Register- und Delete-Fixtures")
print("Versionsstände: Create, Update, Delete und stale festgelegt")
print("Konkurrenz: zwei deterministische Zwei-Parteien-Barrieren")
print("Harness: Reset, Transaktion und interne Beobachtung festgelegt")
print("Fehlerinjektion: ausschließlich testseitig, noch nicht umgesetzt")
print("SQL-Migration v27.31x: keine")
print("Datenbankverbindung: keine")
print("Datenbanktest ausgeführt: nein")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
