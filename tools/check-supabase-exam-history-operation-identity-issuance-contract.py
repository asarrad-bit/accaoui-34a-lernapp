from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]

CONTRACT_PATH = (
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
    "Operations-ID-Ausstellungsvertrag",
)

expected_top_level_keys = {
    "version",
    "contractVersion",
    "status",
    "productiveReleaseAllowed",
    "identityAuthority",
    "clientCorrelation",
    "issuanceRequest",
    "verifiedIdentityRecord",
    "reuseRules",
    "conflictRules",
    "securityRules",
    "unresolvedRequirements",
}

if set(contract) != expected_top_level_keys:
    fail(
        "Unerwartete Ausstellungsvertragsfelder: "
        f"{sorted(set(contract) - expected_top_level_keys)}"
    )

if contract["version"] != "v27.31g":
    fail("Ausstellungsvertragsversion ist nicht v27.31g.")

if contract["contractVersion"] != 1:
    fail("Ausstellungsvertragsschema ist nicht Version 1.")

if contract["status"] != "prepared_not_live":
    fail("Ausstellungsvertrag ist nicht als vorbereitet markiert.")

if contract["productiveReleaseAllowed"] is not False:
    fail("Produktive Freigabe darf noch nicht erlaubt sein.")

expected_authority = {
    "authority": "database_persisted_issuance_record",
    "issuer": "trusted_security_definer_rpc",
    "externalOperationIdAlgorithm": "uuid_v4",
    "generatedInsideDatabase": True,
    "clientSuppliedOperationIdTrusted": False,
    "clientSuppliedOperationIdAcceptedAsAuthority": False,
    "operationIdAloneSufficientForVerification": False,
    "verificationNow": False,
    "liveExecution": False,
}

if contract["identityAuthority"] != expected_authority:
    fail("Operations-ID-Autoritätsgrenze ist nicht kanonisch.")

expected_client_correlation = {
    "fieldName": "client_request_key",
    "source": "untrusted_client_correlation_hint",
    "browserGeneratedAllowed": True,
    "trusted": False,
    "purpose": "retry_lookup_only",
    "minimumEntropyBits": 128,
    "rawStorageAllowed": False,
    "storedRepresentation": "sha256_hash",
    "mayAuthorizeMutation": False,
    "becomesOperationIdentity": False,
    "reuseRequiredForRetry": True,
}

if contract["clientCorrelation"] != expected_client_correlation:
    fail("Client-Wiederholungsschlüssel ist nicht sicher begrenzt.")

expected_issuance_request = {
    "authUserSource": "auth_uid_only",
    "authorizationRequiredBeforeIssuance": True,
    "canonicalFields": [
        "client_request_key",
        "operation_scope",
        "operation",
        "resource_identity",
        "payload_fingerprint",
    ],
    "requestFingerprintAlgorithm": "sha256_canonical_json",
    "requestFingerprintGeneratedBy": (
        "database_or_trusted_server"
    ),
    "operationIdReturnedOnlyAfterPersistence": True,
}

if contract["issuanceRequest"] != expected_issuance_request:
    fail("Operations-ID-Ausstellungsanfrage ist nicht kanonisch.")

expected_record = {
    "requiredFields": [
        "auth_user_id",
        "client_request_key_hash",
        "request_fingerprint",
        "external_operation_id",
        "operation_scope",
        "operation",
        "resource_identity",
        "payload_fingerprint",
        "issued_at",
    ],
    "lookupRequiresFullCanonicalRequest": True,
    "foreignUserLookupAllowed": False,
    "missingRecordMeansUnverified": True,
}

if contract["verifiedIdentityRecord"] != expected_record:
    fail("Verifizierter Operations-ID-Datensatz ist unvollständig.")

expected_reuse_rules = {
    "sameUserSameClientRequestKeySameFingerprintReturnsSameOperationId": True,
    "sameUserSameClientRequestKeyDifferentFingerprintAllowed": False,
    "sameOperationIdWithoutIssuanceRecordAllowed": False,
    "retryMayExecuteDomainMutationWithoutReservation": False,
    "identityReuseAcrossUsersAllowed": False,
}

if contract["reuseRules"] != expected_reuse_rules:
    fail("Operations-ID-Wiederverwendungsregeln sind unsicher.")

expected_conflict_rules = {
    "sameRequestKeyDifferentRequestFingerprint": (
        "reject_request_key_conflict"
    ),
    "suppliedOperationIdWithoutRecord": (
        "reject_unverified_operation_id"
    ),
    "suppliedOperationIdRecordMismatch": (
        "reject_operation_identity_mismatch"
    ),
    "foreignUserRecord": "reject_operation_owner_conflict",
    "rawExistingValuesReturned": False,
}

if contract["conflictRules"] != expected_conflict_rules:
    fail("Operations-ID-Konfliktregeln sind nicht kanonisch.")

expected_security_rules = {
    "authUserFromAuthUidOnly": True,
    "participantIdParameterAllowed": False,
    "authUserIdParameterAllowed": False,
    "serviceRoleInFrontendAllowed": False,
    "directIssuanceTableGrantAllowed": False,
    "directIssuanceHelperGrantAllowed": False,
    "rawDatabaseErrorReturned": False,
}

if contract["securityRules"] != expected_security_rules:
    fail("Operations-ID-Sicherheitsregeln sind nicht kanonisch.")

expected_unresolved = {
    "issuanceTableImplementation": True,
    "issuanceRpcImplementation": True,
    "domainMutationRpcImplementation": True,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
}

if contract["unresolvedRequirements"] != expected_unresolved:
    fail("Offene Operations-ID-Anforderungen sind unvollständig.")

transaction_contract = read_json(
    TRANSACTION_CONTRACT_PATH,
    "Transaktionaler Fachmutationsvertrag",
)

if transaction_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail(
        "Transaktionaler Vertrag darf noch nicht "
        "produktiv freigegeben sein."
    )

transaction_unresolved = transaction_contract.get(
    "unresolvedRequirements",
    {},
)

if transaction_unresolved.get(
    "trustedOperationIdentityIssuance"
) is not True:
    fail(
        "Vertrauenswürdige Operations-ID-Ausstellung "
        "darf noch nicht als umgesetzt gelten."
    )

v2731g_sql_files = list(
    (ROOT / "supabase" / "migrations").glob(
        "*v2731g*.sql"
    )
)

if v2731g_sql_files:
    fail(
        "v27.31g darf noch keine SQL-Migration erzeugen: "
        f"{[path.name for path in v2731g_sql_files]}"
    )

for frontend_path in (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
):
    frontend_text = frontend_path.read_text(
        encoding="utf-8"
    ).lower()

    if CONTRACT_PATH.name.lower() in frontend_text:
        fail(
            "Operations-ID-Vertrag darf nicht im Frontend "
            f"geladen werden: {frontend_path.name}"
        )

print("Operations-ID-Ausstellungsvertrag: OK")
print(
    "Browser-Schlüssel: erlaubt, aber ausschließlich "
    "unvertrauenswürdiger Wiederholungshinweis"
)
print(
    "Operations-UUID: nur serverseitig ausgestellt und "
    "persistiert vertrauenswürdig"
)
print(
    "Wiederholung: gleicher Nutzer, Schlüssel und Fingerprint "
    "erhalten dieselbe UUID"
)
print(
    "Konflikt: gleicher Schlüssel mit anderem Vorgang "
    "geschlossen abgelehnt"
)
print(
    "Operations-ID allein: kein ausreichender "
    "Vertrauensnachweis"
)
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
