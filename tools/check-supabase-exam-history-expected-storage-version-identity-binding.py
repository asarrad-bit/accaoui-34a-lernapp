from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-expected-storage-version-"
      "identity-binding-contract.json"
)

STORAGE_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-domain-storage-contract.json"
)

OUTER_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-outer-domain-mutation-rpc-interface-contract.json"
)

ISSUANCE_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-operation-identity-issuance-contract.json"
)

TRANSACTION_CONTRACT_PATH = (
    ROOT
    / "docs"
    / "contracts"
    / "exam-history-idempotency-transactional-mutation-contract.json"
)

CURRENT_SQL_FILES = [
    "20260722_v2731b_exam_history_idempotency_operations.sql",
    "20260722_v2731c_exam_history_idempotency_reserve_rpc.sql",
    "20260722_v2731d_exam_history_idempotency_complete_rpc.sql",
    "20260722_v2731h_exam_history_operation_identity_issuances.sql",
    "20260722_v2731i_exam_history_operation_identity_issue_rpc.sql",
]

SCHEMA_MIGRATION_PATH = (
    MIGRATIONS
    / "20260722_v2731p_"
      "exam_history_expected_storage_version_schema.sql"
)

ISSUANCE_VERSION_RPC_PATH = (
    MIGRATIONS
    / "20260722_v2731q_"
      "exam_history_operation_identity_expected_version_rpc.sql"
)

RESERVATION_VERSION_RPC_PATH = (
    MIGRATIONS
    / "20260722_v2731r_"
      "exam_history_idempotency_expected_version_reserve_rpc.sql"
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


def read_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


contract = read_json(
    CONTRACT_PATH,
    "Versionsbindungsvertrag",
)

if contract.get("version") != "v27.31r":
    fail("Versionsbindungsvertrag besitzt nicht v27.31r.")

if contract.get("contractVersion") != 1:
    fail("Versionsbindungsvertrag besitzt nicht Schema 1.")

if contract.get("status") != "prepared_not_live":
    fail("Versionsbindungsvertrag ist nicht vorbereitet.")

if contract.get("productiveReleaseAllowed") is not False:
    fail("Produktive Freigabe darf nicht erlaubt sein.")

if contract.get("implementationPresent") is not False:
    fail("Versionsbindung darf noch nicht umgesetzt sein.")

browser = contract.get("browserBoundary", {})

if browser != {
    "parameter": "p_expected_storage_version",
    "type": "bigint",
    "minimum": 0,
    "acceptedOnlyByOuterRpc": True,
    "directHelperAccessAllowed": False,
    "authUserIdParameterAllowed": False,
    "participantIdParameterAllowed": False,
    "externalOperationIdParameterAllowed": False,
}:
    fail("Browsergrenze für den Versionsstand ist ungültig.")

issuance = contract.get(
    "operationIdentityIssuanceBinding",
    {},
)

if issuance.get("lookupIdentityFields") != [
    "auth_user_id",
    "client_request_key_hash",
]:
    fail("Operations-ID-Lookup-Identität ist ungültig.")

if issuance.get("requestFingerprintFields") != [
    "operation_scope",
    "operation",
    "resource_identity",
    "expected_storage_version",
    "payload_fingerprint",
]:
    fail("Ausstellungs-Anfragefingerprint bindet Version nicht.")

for field in (
    "sameClientKeySameFingerprintReusesUuid",
    "sameClientKeyDifferentExpectedVersionConflicts",
    "expectedVersionStoredInIssuanceRow",
    "implementationPresent",
):
    if issuance.get(field) is not True:
        fail(f"Operations-ID-Versionsregel fehlt: {field}")

reservation = contract.get(
    "idempotencyReservationBinding",
    {},
)

if reservation.get("operationIdentityFields") != [
    "auth_user_id",
    "operation_scope",
    "operation",
    "resource_identity",
    "expected_storage_version",
    "payload_fingerprint",
]:
    fail("Idempotenzidentität bindet Version nicht.")

for field in (
    "expectedVersionStoredInReservationRow",
    "expectedVersionComparedOnExistingReservation",
    "sameUuidDifferentExpectedVersionConflicts",
    "sameIdentityDifferentExpectedVersionIsDistinct",
    "implementationPresent",
):
    if reservation.get(field) is not True:
        fail(f"Idempotenz-Versionsregel fehlt: {field}")

if reservation.get("expectedVersionMinimum") != 0:
    fail("Reservierungshelper erlaubt keinen Mindestwert 0.")

if reservation.get("migrationPath") != (
    "supabase/migrations/"
    "20260722_v2731r_"
    "exam_history_idempotency_expected_version_reserve_rpc.sql"
):
    fail("Reservierungs-Versionsbindungs-Migrationspfad ist ungültig.")

completion = contract.get("completionBinding", {})

if completion != {
    "expectedVersionAcceptedFromBrowser": False,
    "expectedVersionReadFromReservedOperation": True,
    "completionMayChangeExpectedVersion": False,
    "completionMayOverwriteIdentity": False,
}:
    fail("Abschluss-Versionsbindung ist ungültig.")

schema = contract.get("schemaRequirements", {})

for field in (
    "issuanceTableExpectedVersionColumnRequired",
    "idempotencyTableExpectedVersionColumnRequired",
    "columnNotNull",
    "existingRowsMigrationStrategyRequired",
    "schemaMigrationImplementationPresent",
):
    if schema.get(field) is not True:
        fail(f"Schema-Versionsanforderung fehlt: {field}")

if schema.get("columnType") != "bigint":
    fail("Speicher-Versionsspalte besitzt nicht bigint.")

if schema.get("columnMinimum") != 0:
    fail("Speicher-Versionsspalte erlaubt keinen Mindestwert 0.")

if schema.get("schemaMigrationPath") != (
    "supabase/migrations/"
    "20260722_v2731p_"
    "exam_history_expected_storage_version_schema.sql"
):
    fail("Schema-Migrationspfad ist ungültig.")

if schema.get("schemaMigrationLiveExecuted") is not False:
    fail("Schema-Migration darf nicht live ausgeführt sein.")

if schema.get("existingRowsMigrationStrategy") != (
    "abort_if_any_target_table_contains_rows"
):
    fail("Strategie für bestehende Zeilen ist nicht geschlossen.")

if schema.get("currentTablesAlreadyContainColumn") is not True:
    fail("Zieltabellen enthalten die neue Spalte nicht.")

expected_unresolved = {
    "issuanceTableMigration": False,
    "idempotencyTableMigration": False,
    "issuanceRpcMigration": False,
    "reserveRpcMigration": False,
    "storageTableImplementation": True,
    "outerDomainMutationRpcImplementation": True,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
    "authorizationTests": True,
}

if contract.get("unresolvedRequirements") != expected_unresolved:
    fail("Offene Versionsbindungsanforderungen sind ungültig.")


helpers = contract.get("helperRequirements", {})

for field in (
    "issuanceRpcExpectedVersionParameterRequired",
    "reserveRpcExpectedVersionParameterRequired",
    "issuanceRpcRequestFingerprintMustBindVersion",
    "reserveRpcOperationIdentityMustBindVersion",
    "outerRpcMustPassSameVersionToBothHelpers",
):
    if helpers.get(field) is not True:
        fail(f"Helper-Versionsanforderung fehlt: {field}")

if helpers.get(
    "completeRpcExpectedVersionParameterRequired"
) is not False:
    fail("Abschluss-RPC darf keinen neuen Versionsparameter verlangen.")

if helpers.get("currentHelpersAlreadyBindVersion") is not True:
    fail("Beide internen Helper binden Version nicht vollständig.")

if helpers.get(
    "currentIssuanceHelperBindsVersion"
) is not True:
    fail("Operations-ID-Ausstellungshelper bindet Version nicht.")

if helpers.get(
    "currentReservationHelperBindsVersion"
) is not True:
    fail("Reservierungshelper bindet Version nicht.")

storage = read_json(
    STORAGE_CONTRACT_PATH,
    "Domain-Speichervertrag",
)

if storage.get("version") != "v27.31s":
    fail("Domain-Speichervertrag besitzt nicht v27.31s.")

identity_binding = storage.get("identityBinding", {})

if identity_binding != {
    "expectedStorageVersionMustAffectRequestIdentity": True,
    "currentIssuanceHelperBindsExpectedVersion": True,
    "currentReservationHelperBindsExpectedVersion": True,
    "outerRpcMayBeImplementedBeforeBinding": False,
}:
    fail("Speichervertrag beschreibt die Versionslücke nicht exakt.")

outer = read_json(
    OUTER_CONTRACT_PATH,
    "Äußerer RPC-Vertrag",
)

if outer.get("version") != "v27.31n":
    fail("Äußerer RPC-Vertrag besitzt nicht v27.31n.")

outer_parameters = outer.get(
    "publicInterface",
    {},
).get("allowedParameters", [])

version_parameters = [
    parameter
    for parameter in outer_parameters
    if parameter.get("name") == "p_expected_storage_version"
]

if version_parameters != [
    {
        "name": "p_expected_storage_version",
        "type": "bigint",
    }
]:
    fail("Äußerer RPC-Vertrag besitzt keine eindeutige Version.")

if outer.get(
    "unresolvedRequirements",
    {},
).get(
    "expectedStorageVersionIdentityBinding"
) is not True:
    fail("Äußerer RPC-Vertrag markiert die Versionsbindung nicht offen.")

issuance_contract = read_json(
    ISSUANCE_CONTRACT_PATH,
    "Operations-ID-Ausstellungsvertrag",
)

transaction_contract = read_json(
    TRANSACTION_CONTRACT_PATH,
    "Transaktionaler Idempotenzvertrag",
)

if issuance_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail("Operations-ID-Ausstellungsvertrag ist produktiv.")

if transaction_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail("Transaktionaler Idempotenzvertrag ist produktiv.")

for filename in CURRENT_SQL_FILES:
    path = MIGRATIONS / filename

    if not path.is_file():
        fail(f"Bestehende Migration fehlt: {filename}")

    sql = path.read_text(encoding="utf-8").lower()

    if "expected_storage_version" in sql:
        fail(
            "Ältere Migration wurde rückwirkend verändert: "
            f"{filename}"
        )

if not SCHEMA_MIGRATION_PATH.is_file():
    fail("Speicher-Versionsstand-Schema-Migration fehlt.")

schema_sql = SCHEMA_MIGRATION_PATH.read_text(encoding="utf-8")
schema_without_comments = re.sub(
    r"--.*?$",
    "",
    schema_sql,
    flags=re.MULTILINE,
)
schema_lower = schema_without_comments.lower()

for table_name, failure_code in (
    (
        "exam_history_operation_identity_issuances",
        "exam_history_issuance_existing_rows_"
        "require_expected_storage_version_backfill",
    ),
    (
        "exam_history_idempotency_operations",
        "exam_history_idempotency_existing_rows_"
        "require_expected_storage_version_backfill",
    ),
):
    existing_rows_pattern = (
        r"if\s+exists\s*\(\s*"
        r"select\s+1\s+from\s+public\."
        + re.escape(table_name)
        + r"\s+limit\s+1\s*\)"
    )
    if not re.search(
        existing_rows_pattern,
        schema_sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(
            "Abbruchprüfung für bestehende Zeilen fehlt: "
            f"{table_name}"
        )
    if failure_code not in schema_lower:
        fail(
            "Stabiler Backfill-Abbruchcode fehlt: "
            f"{failure_code}"
        )

    column_pattern = (
        r"alter\s+table\s+public\."
        + re.escape(table_name)
        + r"\s+add\s+column\s+"
        r"expected_storage_version\s+"
        r"bigint\s+not\s+null\s+"
        r"constraint\s+[a-z0-9_]+\s+"
        r"check\s*\(\s*"
        r"expected_storage_version\s*>=\s*0\s*"
        r"\)\s*;"
    )
    if not re.search(
        column_pattern,
        schema_sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(
            "Sichere Speicher-Versionsspalte fehlt: "
            f"{table_name}"
        )

    for protection_pattern, label in (
        (
            r"alter\s+table\s+public\."
            + re.escape(table_name)
            + r"\s+enable\s+row\s+level\s+security\s*;",
            "RLS-Aktivierung",
        ),
        (
            r"alter\s+table\s+public\."
            + re.escape(table_name)
            + r"\s+force\s+row\s+level\s+security\s*;",
            "RLS-Erzwingung",
        ),
        (
            r"revoke\s+all\s+on\s+table\s+public\."
            + re.escape(table_name)
            + r"\s+from\s+public\s*,\s*anon\s*,\s*"
              r"authenticated\s*;",
            "Tabellen-Revoke",
        ),
    ):
        if not re.search(
            protection_pattern,
            schema_sql,
            flags=re.IGNORECASE | re.DOTALL,
        ):
            fail(f"{label} fehlt für: {table_name}")

if re.search(
    r"\bdefault\b",
    schema_without_comments,
    flags=re.IGNORECASE,
):
    fail("Speicher-Versionsspalte darf keinen Default besitzen.")

if re.search(
    r"\b(insert\s+into|update\s+public\.|delete\s+from)\b",
    schema_without_comments,
    flags=re.IGNORECASE,
):
    fail("Schema-Migration darf keine Daten verändern.")

for forbidden in (
    "create policy",
    "grant ",
    "create or replace function",
    "auth.uid()",
):
    if forbidden in schema_lower:
        fail(
            "Unzulässiger Inhalt in Schema-Migration: "
            f"{forbidden}"
        )

v2731p_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731p*.sql")
)
if v2731p_sql_files != [
    "20260722_v2731p_"
    "exam_history_expected_storage_version_schema.sql"
]:
    fail(
        "Unerwartete v27.31p-SQL-Dateien: "
        f"{v2731p_sql_files}"
    )

if not ISSUANCE_VERSION_RPC_PATH.is_file():
    fail("Operations-ID-Versionsbindungs-RPC fehlt.")

issuance_version_sql = ISSUANCE_VERSION_RPC_PATH.read_text(
    encoding="utf-8"
)
issuance_version_without_comments = re.sub(
    r"--.*?$",
    "",
    issuance_version_sql,
    flags=re.MULTILINE,
)
issuance_version_lower = issuance_version_without_comments.lower()
issuance_version_compact = re.sub(
    r"\s+",
    " ",
    issuance_version_lower,
).strip()

for marker in (
    "p_expected_storage_version bigint",
    "message = 'expected_storage_version_invalid'",
    "'expected_storage_version', p_expected_storage_version",
    "expected_storage_version, payload_fingerprint",
    "p_expected_storage_version, p_payload_fingerprint",
    "v_existing.expected_storage_version <> "
    "p_expected_storage_version",
):
    if marker not in issuance_version_compact:
        fail(
            "Operations-ID-Versionsbindungs-RPC-Anweisung "
            f"fehlt: {marker}"
        )

if (
    "'client_request_key', p_client_request_key"
    in issuance_version_compact
):
    fail(
        "Roher Client-Schlüssel liegt im kanonischen "
        "Anfragefingerprint."
    )

for role in (
    "public",
    "anon",
    "authenticated",
):
    revoke_pattern = (
        r"revoke\s+all\s+on\s+function\s+"
        r"public\.accaoui_issue_exam_history_operation_identity"
        r"\s*\(\s*text\s*,\s*text\s*,\s*text\s*,\s*"
        r"text\s*,\s*bigint\s*,\s*text\s*\)\s+from\s+"
        + re.escape(role)
        + r"\s*;"
    )
    if not re.search(
        revoke_pattern,
        issuance_version_sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(
            "Operations-ID-Versionsbindungs-RPC-Revoke "
            f"fehlt für: {role}"
        )

if not re.search(
    r"drop\s+function\s+if\s+exists\s+"
    r"public\.accaoui_issue_exam_history_operation_identity"
    r"\s*\(\s*text\s*,\s*text\s*,\s*text\s*,\s*"
    r"text\s*,\s*text\s*\)\s*;",
    issuance_version_sql,
    flags=re.IGNORECASE | re.DOTALL,
):
    fail("Alte Fünf-Parameter-Ausstellungsfunktion bleibt erhalten.")

for forbidden in (
    "grant execute",
    "create policy",
    "service_role",
    "exam_history_idempotency_operations",
    "exam_history_domain_resources",
):
    if forbidden in issuance_version_lower:
        fail(
            "Unzulässiger Inhalt im Operations-ID-"
            f"Versionsbindungs-RPC: {forbidden}"
        )

v2731q_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731q*.sql")
)
if v2731q_sql_files != [
    "20260722_v2731q_"
    "exam_history_operation_identity_expected_version_rpc.sql"
]:
    fail(
        "Unerwartete v27.31q-SQL-Dateien: "
        f"{v2731q_sql_files}"
    )


if not RESERVATION_VERSION_RPC_PATH.is_file():
    fail("Idempotenz-Reservierungs-Versionsbindungs-RPC fehlt.")

reservation_version_sql = RESERVATION_VERSION_RPC_PATH.read_text(
    encoding="utf-8"
)
reservation_version_without_comments = re.sub(
    r"--.*?$",
    "",
    reservation_version_sql,
    flags=re.MULTILINE,
)
reservation_version_lower = (
    reservation_version_without_comments.lower()
)
reservation_version_compact = re.sub(
    r"\s+",
    " ",
    reservation_version_lower,
).strip()

for marker in (
    "p_expected_storage_version bigint",
    "message = 'expected_storage_version_invalid'",
    "expected_storage_version, payload_fingerprint",
    "p_expected_storage_version, p_payload_fingerprint",
    "v_existing.expected_storage_version <> "
    "p_expected_storage_version",
    "message = 'idempotency_operation_identity_conflict'",
):
    if marker not in reservation_version_compact:
        fail(
            "Idempotenz-Reservierungs-Versionsbindungs-RPC-"
            f"Anweisung fehlt: {marker}"
        )

for role in (
    "public",
    "anon",
    "authenticated",
):
    revoke_pattern = (
        r"revoke\s+all\s+on\s+function\s+"
        r"public\.accaoui_reserve_exam_history_"
        r"idempotency_operation"
        r"\s*\(\s*uuid\s*,\s*text\s*,\s*text\s*,\s*"
        r"text\s*,\s*bigint\s*,\s*text\s*\)\s+from\s+"
        + re.escape(role)
        + r"\s*;"
    )
    if not re.search(
        revoke_pattern,
        reservation_version_sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(
            "Reservierungs-Versionsbindungs-RPC-Revoke "
            f"fehlt für: {role}"
        )

if not re.search(
    r"drop\s+function\s+if\s+exists\s+"
    r"public\.accaoui_reserve_exam_history_"
    r"idempotency_operation"
    r"\s*\(\s*uuid\s*,\s*text\s*,\s*text\s*,\s*"
    r"text\s*,\s*text\s*\)\s*;",
    reservation_version_sql,
    flags=re.IGNORECASE | re.DOTALL,
):
    fail("Alte Fünf-Parameter-Reservierungsfunktion bleibt erhalten.")

reservation_mutations = [
    (
        re.sub(r"\s+", " ", action.lower()),
        table.lower(),
    )
    for action, table in re.findall(
        r"\b(insert\s+into|update|delete\s+from)\s+"
        r"(?:public\.)?([a-z_]+)",
        reservation_version_without_comments,
        flags=re.IGNORECASE,
    )
]

if reservation_mutations != [
    (
        "insert into",
        "exam_history_idempotency_operations",
    ),
]:
    fail(
        "Reservierungs-Versionsbindungs-RPC verändert "
        f"unerwartete Tabellen: {reservation_mutations}"
    )

for forbidden in (
    "grant execute",
    "create policy",
    "service_role",
    "exam_history_domain_resources",
    "public.exam_attempts",
    "public.exam_answers",
):
    if forbidden in reservation_version_lower:
        fail(
            "Unzulässiger Inhalt im Reservierungs-"
            f"Versionsbindungs-RPC: {forbidden}"
        )

v2731r_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731r*.sql")
)

if v2731r_sql_files != [
    "20260722_v2731r_"
    "exam_history_idempotency_expected_version_reserve_rpc.sql"
]:
    fail(
        "Unerwartete v27.31r-SQL-Dateien: "
        f"{v2731r_sql_files}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
):
    frontend_text = frontend_path.read_text(
        encoding="utf-8"
    ).lower()

    if CONTRACT_PATH.name.lower() in frontend_text:
        fail(
            "Versionsbindungsvertrag darf nicht im Frontend "
            f"geladen werden: {frontend_path.name}"
        )

print("Speicher-Versionsstand-Identitätsbindung: OK")
print(
    "Operations-ID-Ausstellung: erwartete Version ist im "
    "Anfragefingerprint und in der Ausstellungszeile gebunden"
)
print(
    "Client-Retry: gleiche Version verwendet dieselbe UUID, "
    "abweichende Version kollidiert"
)
print(
    "Idempotenzreservierung: erwartete Version ist gespeichert, "
    "Teil der vollständigen Operationsidentität und Retry-Prüfung"
)
print(
    "Abschluss: liest Version aus der Reservierung und darf "
    "sie nicht verändern"
)
print(
    "Tabellenschema angepasst: ja; vorhandene Zeilen führen "
    "zum kontrollierten Abbruch"
)
print(
    "Helperstatus: Ausstellungs- und Reservierungshelper "
    "binden denselben erwarteten Versionsstand"
)
print("SQL-Migration in v27.31r: vorbereitet")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
