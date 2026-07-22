from pathlib import Path
import json
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

if contract.get("version") != "v27.31o":
    fail("Versionsbindungsvertrag besitzt nicht v27.31o.")

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
):
    if reservation.get(field) is not True:
        fail(f"Idempotenz-Versionsregel fehlt: {field}")

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
):
    if schema.get(field) is not True:
        fail(f"Schema-Versionsanforderung fehlt: {field}")

if schema.get("currentTablesAlreadyContainColumn") is not False:
    fail("Bestehende Tabellen dürfen Version noch nicht enthalten.")

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

if helpers.get("currentHelpersAlreadyBindVersion") is not False:
    fail("Bestehende Helper dürfen Version noch nicht binden.")

storage = read_json(
    STORAGE_CONTRACT_PATH,
    "Domain-Speichervertrag",
)

if storage.get("version") != "v27.31n":
    fail("Domain-Speichervertrag besitzt nicht v27.31n.")

identity_binding = storage.get("identityBinding", {})

if identity_binding != {
    "expectedStorageVersionMustAffectRequestIdentity": True,
    "currentIssuanceHelperBindsExpectedVersion": False,
    "currentReservationHelperBindsExpectedVersion": False,
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
            "Bestehende Migration bindet den Versionsstand "
            f"unerwartet bereits: {filename}"
        )

v2731o_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731o*.sql")
)

if v2731o_sql_files:
    fail(
        "v27.31o darf keine SQL-Migration erzeugen: "
        f"{v2731o_sql_files}"
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
    "Operations-ID-Ausstellung: erwartete Version muss in "
    "den Anfragefingerprint"
)
print(
    "Client-Retry: gleiche Version verwendet dieselbe UUID, "
    "abweichende Version kollidiert"
)
print(
    "Idempotenzreservierung: erwartete Version wird Teil der "
    "vollständigen Operationsidentität"
)
print(
    "Abschluss: liest Version aus der Reservierung und darf "
    "sie nicht verändern"
)
print(
    "Bestehende Tabellen und Helper bereits angepasst: nein"
)
print("SQL-Migration in v27.31o: nein")
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
