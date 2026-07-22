from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIGRATIONS = ROOT / "supabase" / "migrations"

ISSUANCE_TABLE_PATH = (
    MIGRATIONS
    / "20260722_v2731h_"
    "exam_history_operation_identity_issuances.sql"
)

ISSUE_RPC_PATH = (
    MIGRATIONS
    / "20260722_v2731i_"
    "exam_history_operation_identity_issue_rpc.sql"
)

RESERVE_RPC_PATH = (
    MIGRATIONS
    / "20260722_v2731c_"
    "exam_history_idempotency_reserve_rpc.sql"
)

COMPLETE_RPC_PATH = (
    MIGRATIONS
    / "20260722_v2731d_"
    "exam_history_idempotency_complete_rpc.sql"
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

ISSUE_FUNCTION = (
    "public."
    "accaoui_issue_exam_history_operation_identity"
)

RESERVE_FUNCTION = (
    "public."
    "accaoui_reserve_exam_history_idempotency_operation"
)

COMPLETE_FUNCTION = (
    "public."
    "accaoui_complete_exam_history_idempotency_operation"
)


def fail(message: str) -> None:
    print(f"FEHLER: {message}")
    sys.exit(1)


def read_text(path: Path, label: str) -> str:
    if not path.is_file():
        fail(f"{label} fehlt: {path.name}")

    return (
        path.read_text(encoding="utf-8")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )


def read_json(path: Path, label: str):
    if not path.is_file():
        fail(f"{label} fehlt.")

    try:
        return json.loads(
            path.read_text(encoding="utf-8")
        )
    except Exception as exc:
        fail(f"{label} ungültig: {exc}")


def without_comments(text: str) -> str:
    return re.sub(
        r"--.*?$",
        "",
        text,
        flags=re.MULTILINE,
    )


def compact(text: str) -> str:
    return re.sub(
        r"\s+",
        " ",
        text.lower(),
    ).strip()


def parse_parameters(
    sql: str,
    function_name: str,
) -> list[tuple[str, str]]:
    match = re.search(
        r"function\s+"
        + re.escape(function_name)
        + r"\s*\((.*?)\)\s*returns",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        fail(f"Funktionssignatur fehlt: {function_name}")

    parameters = []

    for raw_parameter in match.group(1).split(","):
        parameter = re.sub(
            r"\s+",
            " ",
            raw_parameter.strip().lower(),
        )

        if not parameter:
            continue

        parameter = re.sub(
            r"\s+default\s+.+$",
            "",
            parameter,
        )

        parts = parameter.split()

        if len(parts) != 2:
            fail(
                "Unerwarteter Parameter in "
                f"{function_name}: {parameter}"
            )

        parameters.append((parts[0], parts[1]))

    return parameters


def parse_returns(
    sql: str,
    function_name: str,
) -> list[tuple[str, str]]:
    match = re.search(
        r"function\s+"
        + re.escape(function_name)
        + r"\s*\(.*?\)\s*returns\s+table\s*"
        r"\((.*?)\)\s*language\s+plpgsql",
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    )

    if not match:
        fail(f"Rückgabesignatur fehlt: {function_name}")

    columns = []

    for raw_column in match.group(1).split(","):
        column = re.sub(
            r"\s+",
            " ",
            raw_column.strip().lower(),
        )

        parts = column.split()

        if len(parts) != 2:
            fail(
                "Unerwartete Rückgabespalte in "
                f"{function_name}: {column}"
            )

        columns.append((parts[0], parts[1]))

    return columns


def require_revoke(
    sql: str,
    function_name: str,
    role: str,
) -> None:
    pattern = (
        r"revoke\s+all\s+on\s+function\s+"
        + re.escape(function_name)
        + r"\s*\(.*?\)\s+from\s+"
        + re.escape(role)
        + r"\s*;"
    )

    if not re.search(
        pattern,
        sql,
        flags=re.IGNORECASE | re.DOTALL,
    ):
        fail(
            f"Revoke fehlt für {function_name}: {role}"
        )


issuance_table_sql = read_text(
    ISSUANCE_TABLE_PATH,
    "Operations-ID-Ausstellungstabelle",
)

issue_sql = read_text(
    ISSUE_RPC_PATH,
    "Operations-ID-Ausstellungs-RPC",
)

reserve_sql = read_text(
    RESERVE_RPC_PATH,
    "Idempotenz-Reservierungs-RPC",
)

complete_sql = read_text(
    COMPLETE_RPC_PATH,
    "Idempotenz-Abschluss-RPC",
)

issuance_table_clean = without_comments(
    issuance_table_sql.lower()
)

issue_clean = without_comments(issue_sql.lower())
reserve_clean = without_comments(reserve_sql.lower())
complete_clean = without_comments(complete_sql.lower())

issuance_table_compact = compact(issuance_table_clean)
issue_compact = compact(issue_clean)
reserve_compact = compact(reserve_clean)
complete_compact = compact(complete_clean)

issuance_contract = read_json(
    ISSUANCE_CONTRACT_PATH,
    "Operations-ID-Ausstellungsvertrag",
)

transaction_contract = read_json(
    TRANSACTION_CONTRACT_PATH,
    "Transaktionaler Fachmutationsvertrag",
)

if issuance_contract.get("version") != "v27.31i":
    fail(
        "Operations-ID-Ausstellungsvertrag besitzt "
        "nicht v27.31i."
    )

if issuance_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail(
        "Operations-ID-Ausstellungsvertrag darf noch "
        "nicht produktiv freigegeben sein."
    )

issuance_unresolved = issuance_contract.get(
    "unresolvedRequirements",
    {},
)

if issuance_unresolved != {
    "issuanceTableImplementation": False,
    "issuanceRpcImplementation": False,
    "domainMutationRpcImplementation": True,
    "liveDatabaseTests": True,
    "concurrencyTests": True,
}:
    fail(
        "Offene Operations-ID-Anforderungen sind "
        "nicht kanonisch."
    )

identity_authority = issuance_contract.get(
    "identityAuthority",
    {},
)

if identity_authority.get(
    "clientSuppliedOperationIdTrusted"
) is not False:
    fail(
        "Browserseitige Operations-ID darf nicht "
        "als vertrauenswürdig gelten."
    )

if identity_authority.get(
    "clientSuppliedOperationIdAcceptedAsAuthority"
) is not False:
    fail(
        "Browserseitige Operations-ID darf keine "
        "Identitätsautorität sein."
    )

if identity_authority.get(
    "operationIdAloneSufficientForVerification"
) is not False:
    fail(
        "Operations-ID allein darf nicht zur "
        "Verifikation ausreichen."
    )

if transaction_contract.get(
    "productiveReleaseAllowed"
) is not False:
    fail(
        "Transaktionaler Vertrag darf noch nicht "
        "produktiv freigegeben sein."
    )

transaction_identity = transaction_contract.get(
    "identity",
    {},
)

if transaction_identity.get(
    "operationIdentityInputAllowed"
) is not False:
    fail(
        "Äußerer Fachmutationsweg darf keine "
        "Operations-ID als Eingabe akzeptieren."
    )

if transaction_identity.get(
    "browserGeneratedAllowed"
) is not False:
    fail(
        "Browsergenerierte Operations-ID ist im "
        "Transaktionsvertrag erlaubt."
    )

if transaction_identity.get(
    "verifiedNow"
) is not False:
    fail(
        "Operations-ID-Integration darf noch nicht "
        "als vollständig verifiziert gelten."
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
        "muss bis zur äußeren Integration offen bleiben."
    )

if transaction_unresolved.get(
    "domainMutationRpcImplementation"
) is not True:
    fail(
        "Äußerer Fachmutations-RPC muss noch offen sein."
    )

issue_parameters = parse_parameters(
    issue_sql,
    ISSUE_FUNCTION,
)

reserve_parameters = parse_parameters(
    reserve_sql,
    RESERVE_FUNCTION,
)

complete_parameters = parse_parameters(
    complete_sql,
    COMPLETE_FUNCTION,
)

expected_issue_parameters = [
    ("p_client_request_key", "text"),
    ("p_operation_scope", "text"),
    ("p_operation", "text"),
    ("p_resource_identity", "text"),
    ("p_payload_fingerprint", "text"),
]

expected_reserve_parameters = [
    ("p_external_operation_id", "uuid"),
    ("p_operation_scope", "text"),
    ("p_operation", "text"),
    ("p_resource_identity", "text"),
    ("p_payload_fingerprint", "text"),
]

expected_complete_prefix = expected_reserve_parameters

if issue_parameters != expected_issue_parameters:
    fail(
        "Operations-ID-Ausstellungs-RPC besitzt "
        "unerwartete Eingaben: "
        f"{issue_parameters}"
    )

if reserve_parameters != expected_reserve_parameters:
    fail(
        "Idempotenz-Reservierungs-RPC besitzt "
        "unerwartete Eingaben: "
        f"{reserve_parameters}"
    )

if complete_parameters[:5] != expected_complete_prefix:
    fail(
        "Idempotenz-Abschluss-RPC besitzt keine "
        "identische Operationsschnittstelle."
    )

if issue_parameters[1:] != reserve_parameters[1:]:
    fail(
        "Ausstellung und Reservierung verwenden "
        "abweichende kanonische Fachparameter."
    )

if issue_parameters[1:] != complete_parameters[1:5]:
    fail(
        "Ausstellung und Abschluss verwenden "
        "abweichende kanonische Fachparameter."
    )

if any(
    name == "p_external_operation_id"
    for name, _ in issue_parameters
):
    fail(
        "Ausstellungs-RPC akzeptiert eine "
        "browserseitige Operations-ID."
    )

if any(
    name == "p_client_request_key"
    for name, _ in reserve_parameters
):
    fail(
        "Reservierungs-RPC akzeptiert den rohen "
        "Client-Wiederholungsschlüssel."
    )

issue_returns = parse_returns(
    issue_sql,
    ISSUE_FUNCTION,
)

if issue_returns != [
    ("external_operation_id", "uuid"),
    ("issuance_status", "text"),
    ("issued_at", "timestamptz"),
    ("is_new", "boolean"),
]:
    fail(
        "Operations-ID-Ausstellungs-RPC besitzt "
        "unerwartete Rückgabedaten."
    )

insert_match = re.search(
    r"insert\s+into\s+"
    r"public\.exam_history_operation_identity_issuances"
    r"\s+as\s+issuance\s*\((.*?)\)\s*values",
    issue_sql,
    flags=re.IGNORECASE | re.DOTALL,
)

if not insert_match:
    fail(
        "Ausstellungs-RPC besitzt keinen eindeutig "
        "prüfbaren Insert."
    )

insert_columns = [
    re.sub(
        r"\s+",
        "",
        column.lower(),
    )
    for column in insert_match.group(1).split(",")
    if column.strip()
]

expected_insert_columns = [
    "auth_user_id",
    "client_request_key_hash",
    "request_fingerprint",
    "operation_scope",
    "operation",
    "resource_identity",
    "payload_fingerprint",
]

if insert_columns != expected_insert_columns:
    fail(
        "Ausstellungs-RPC schreibt unerwartete Spalten: "
        f"{insert_columns}"
    )

if "external_operation_id" in insert_columns:
    fail(
        "Operations-UUID wird durch den RPC direkt "
        "eingefügt statt durch die Datenbank erzeugt."
    )

for marker in (
    "external_operation_id uuid not null "
    "default gen_random_uuid()",
    "unique ( external_operation_id )",
):
    if marker not in issuance_table_compact:
        fail(
            "Datenbankseitige UUID-Ausstellung fehlt: "
            f"{marker}"
        )

for marker in (
    "issuance.external_operation_id",
    "'issued_new'::text",
    "'issued_existing'::text",
):
    if marker not in issue_compact:
        fail(
            "Operations-ID-Ausstellungs-RPC-Anweisung "
            f"fehlt: {marker}"
        )

for marker in (
    "p_external_operation_id::text",
    "external_operation_id,",
    "p_external_operation_id,",
    "'exam_history_idempotency:' || "
    "p_operation_scope || ':' || "
    "p_operation || ':' || "
    "p_external_operation_id::text",
):
    if marker not in reserve_compact:
        fail(
            "Ausgestellte UUID ist nicht vollständig mit "
            f"der Reservierung verbunden: {marker}"
        )

for marker in (
    "p_external_operation_id::text",
    "v_existing.external_operation_id <> "
    "p_external_operation_id",
):
    if marker not in complete_compact:
        fail(
            "Ausgestellte UUID ist nicht vollständig mit "
            f"dem Abschluss verbunden: {marker}"
        )

for role in (
    "public",
    "anon",
    "authenticated",
):
    require_revoke(
        issue_sql,
        ISSUE_FUNCTION,
        role,
    )

    require_revoke(
        reserve_sql,
        RESERVE_FUNCTION,
        role,
    )

    require_revoke(
        complete_sql,
        COMPLETE_FUNCTION,
        role,
    )

for label, sql_clean in (
    ("Ausstellungs-RPC", issue_clean),
    ("Reservierungs-RPC", reserve_clean),
    ("Abschluss-RPC", complete_clean),
):
    if "grant execute" in sql_clean:
        fail(
            f"{label} besitzt eine direkte "
            "Ausführungsfreigabe."
        )

frontend_paths = (
    ROOT / "index.html",
    ROOT / "app.js",
    ROOT / "patch-v21.js",
    ROOT / "data" / "supabase-client-adapter.js",
)

helper_names = (
    ISSUE_FUNCTION.split(".", 1)[1],
    RESERVE_FUNCTION.split(".", 1)[1],
    COMPLETE_FUNCTION.split(".", 1)[1],
)

for frontend_path in frontend_paths:
    frontend_text = read_text(
        frontend_path,
        f"Frontenddatei {frontend_path.name}",
    ).lower()

    for helper_name in helper_names:
        if helper_name in frontend_text:
            fail(
                "Interner Helper wird direkt im Frontend "
                f"referenziert: {frontend_path.name}: "
                f"{helper_name}"
            )

integrated_sql_files = []

for sql_path in MIGRATIONS.glob("*.sql"):
    sql_clean = without_comments(
        sql_path.read_text(
            encoding="utf-8"
        ).lower()
    )

    if (
        ISSUE_FUNCTION in sql_clean
        and RESERVE_FUNCTION in sql_clean
    ):
        integrated_sql_files.append(sql_path.name)

if integrated_sql_files:
    fail(
        "Äußerer Integrations-RPC wurde in v27.31j "
        "unerwartet bereits ergänzt: "
        f"{integrated_sql_files}"
    )

v2731j_sql_files = sorted(
    path.name
    for path in MIGRATIONS.glob("*v2731j*.sql")
)

if v2731j_sql_files:
    fail(
        "v27.31j darf keine SQL-Migration erzeugen: "
        f"{v2731j_sql_files}"
    )

print("Operations-ID-/Idempotenz-Integrationsaudit: OK")
print(
    "Browsergrenze: nur unvertrauenswürdiger "
    "Client-Wiederholungsschlüssel"
)
print(
    "Operations-UUID: intern erzeugt, gespeichert und "
    "erst danach zurückgegeben"
)
print(
    "Schnittstelle: ausgestellte UUID passt exakt zur "
    "Reservierungs- und Abschlussgrenze"
)
print(
    "Direkte Helper-Ausführung: für public, anon und "
    "authenticated gesperrt"
)
print(
    "Frontendzugriff: keine direkte Referenz auf interne "
    "Ausstellungs-, Reservierungs- oder Abschluss-RPCs"
)
print(
    "Äußerer Fachmutations-RPC: noch nicht implementiert"
)
print("Produktive Freigabe: nein")
print("Live-Ausführung: nein")
