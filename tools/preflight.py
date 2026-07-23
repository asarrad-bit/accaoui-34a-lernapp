from pathlib import Path
import json
import os
import subprocess
import sys

errors = []

def run_command(command):
    result = subprocess.run(
        command,
        shell=True,
        text=True,
        capture_output=True
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()

def check_file_exists(path):
    if not Path(path).exists():
        errors.append(f"Datei fehlt: {path}")

def check_json(path):
    try:
        json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"JSON ungültig: {path} – {exc}")

def check_index_versions():
    index = Path("index.html")
    if not index.exists():
        errors.append("index.html fehlt")
        return

    text = index.read_text(encoding="utf-8")

    required_scripts = [
        "app.js",
        "patch-v21.js",
        "data/oral-question-bank.js",
        "data/oral-sheets-bank.js",
        "oral-sheets.js",
        "oral-sheets-v23.js",
        "oral-exam.js",
    ]

    for script in required_scripts:
        if script not in text:
            errors.append(f"Script fehlt in index.html: {script}")

    required_styles = [
        "style.css",
        "oral-exam.css",
    ]

    for style in required_styles:
        if style not in text:
            errors.append(f"Stylesheet fehlt in index.html: {style}")

def check_category_audit():
    code, stdout, stderr = run_command(f'"{sys.executable}" tools/audit-categories.py')

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append("Kategorien-Audit fehlgeschlagen")

def check_exam_result_history_adapter():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-adapter.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Ergebnislisten-Adapterprüfung fehlgeschlagen"
        )


def check_exam_result_history_fixtures():
    code, stdout, stderr = run_command(
        "node tools/test-supabase-exam-history-fixtures.js"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Ergebnishistorie-Fixture-Test fehlgeschlagen"
        )


def check_exam_result_history_idempotency_flow():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-idempotency-flow.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Idempotenz-End-to-End-Audit fehlgeschlagen"
        )



def check_exam_result_history_transactional_mutation_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "transactional-mutation-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-transaktionaler "
            "Fachmutationsvertrag fehlgeschlagen"
        )



def check_exam_result_history_operation_identity_issuance_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "operation-identity-issuance-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Operations-ID-Ausstellungsvertrag "
            "fehlgeschlagen"
        )



def check_exam_result_history_operation_identity_idempotency_integration():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "operation-identity-idempotency-integration.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Operations-ID-/Idempotenz-"
            "Integrationsaudit fehlgeschlagen"
        )



def check_exam_result_history_outer_domain_mutation_rpc_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "outer-domain-mutation-rpc-interface-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-äußerer Fachmutations-RPC-Vertrag "
            "fehlgeschlagen"
        )



def check_exam_result_history_domain_payload_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "domain-payload-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Fach-Payload-Vertrag fehlgeschlagen"
        )



def check_exam_result_history_domain_storage_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "domain-storage-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Domain-Speichervertrag fehlgeschlagen"
        )



def check_exam_result_history_expected_storage_version_binding():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "expected-storage-version-identity-binding.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Speicher-Versionsstand-"
            "Identitätsbindung fehlgeschlagen"
        )



def check_exam_result_history_outer_domain_mutation_database_test_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "outer-domain-mutation-database-test-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-äußerer Fachmutations-"
            "Datenbank-Testvertrag fehlgeschlagen"
        )



def check_exam_result_history_outer_domain_mutation_fixture_harness_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "outer-domain-mutation-fixture-harness-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-synthetischer Fixture- und "
            "Harness-Vertrag fehlgeschlagen"
        )



def check_exam_result_history_outer_domain_mutation_harness_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-outer-domain-mutation-"
        "harness-readiness.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-synthetischer Fixture-Katalog und "
            "Harness-Readiness fehlgeschlagen"
        )


def check_git_diff_check():
    code, stdout, stderr = run_command("git diff --check")

    if stdout:
        errors.append("git diff --check meldet Probleme:\n" + stdout)

    if stderr:
        errors.append("git diff --check Fehler:\n" + stderr)

PROTECTED_CORE_FILES_V2356 = [
    "app.js",
    "patch-v21.js",
    "index.html",
    "style.css",
    "oral-exam.css",
    "oral-exam.js",
    "oral-sheets.js",
    "oral-sheets-v23.js",
    "questions.json",
    "data/oral-question-bank.js",
    "data/oral-sheets-bank.js",
]

def _parse_allowed_protected_v2356():
    raw = os.environ.get("ACCAOUI_ALLOW_PROTECTED", "").strip()
    if not raw:
        return set()

    allowed = set()
    for part in raw.split(","):
        path = part.strip().strip('"').replace("\\", "/")
        if path:
            allowed.add(path)
    return allowed

def check_protected_core_files_v2356():
    code, stdout, stderr = run_command("git status --short")

    if code != 0:
        errors.append("git status --short fehlgeschlagen")
        if stderr:
            errors.append(stderr)
        return

    allowed_protected = _parse_allowed_protected_v2356()
    changed_protected = set()

    for line in stdout.splitlines():
        line = line.strip()
        if not line:
            continue

        parts = line.split(maxsplit=1)
        if len(parts) < 2:
            continue

        path_part = parts[1].strip().strip('"')
        if " -> " in path_part:
            path_part = path_part.split(" -> ", 1)[1].strip().strip('"')

        path_part = path_part.replace("\\", "/")

        for protected in PROTECTED_CORE_FILES_V2356:
            if path_part == protected:
                changed_protected.add(protected)

    for protected in sorted(changed_protected):
        if protected in allowed_protected:
            continue
        errors.append(
            "KRITISCH: Geschützte Datei geändert: " + protected + "\n"
            "Nur committen, wenn diese Datei ausdrücklich für den aktuellen Task freigegeben wurde."
        )


def check_exam_result_history_outer_domain_mutation_e2e_audit():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-"
        "outer-domain-mutation-e2e-audit.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-äußerer Fachmutations-"
            "End-to-End-Audit fehlgeschlagen"
        )


def main():
    print("Accaoui Preflight läuft...\n")

    required_files = [
        "index.html",
        "app.js",
        "patch-v21.js",
        "style.css",
        "oral-exam.css",
        "oral-exam.js",
        "questions.json",
        "oral-sheets.js",
        "oral-sheets-v23.js",
        "data/oral-question-bank.js",
        "data/oral-sheets-bank.js",
        "tools/audit-categories.py",
        "tools/check-supabase-exam-history-adapter.py",
        "tools/test-supabase-exam-history-fixtures.js",
        "tools/check-supabase-exam-history-idempotency-flow.py",
        "tools/check-supabase-exam-history-transactional-mutation-contract.py",
        "docs/contracts/exam-history-idempotency-transactional-mutation-contract.json",
        "tools/check-supabase-exam-history-operation-identity-issuance-contract.py",
        "docs/contracts/exam-history-operation-identity-issuance-contract.json",
        "tools/check-supabase-exam-history-operation-identity-idempotency-integration.py",
        "tools/check-supabase-exam-history-outer-domain-mutation-rpc-interface-contract.py",
        "docs/contracts/exam-history-outer-domain-mutation-rpc-interface-contract.json",
        "tools/check-supabase-exam-history-outer-domain-mutation-e2e-audit.py",
        "docs/contracts/exam-history-outer-domain-mutation-e2e-audit-contract.json",
        "tools/check-supabase-exam-history-outer-domain-mutation-database-test-contract.py",
        "docs/contracts/exam-history-outer-domain-mutation-database-test-contract.json",
        "tools/check-supabase-exam-history-outer-domain-mutation-fixture-harness-contract.py",
        "docs/contracts/exam-history-outer-domain-mutation-fixture-harness-contract.json",
        "tools/fixtures/exam-history-outer-domain-mutation-fixtures.json",
        "tools/run-supabase-exam-history-outer-domain-mutation-harness.py",
        "docs/contracts/exam-history-outer-domain-mutation-harness-readiness-contract.json",
        "tools/check-supabase-exam-history-outer-domain-mutation-harness-readiness.py",
        "tools/check-supabase-exam-history-domain-payload-contract.py",
        "docs/contracts/exam-history-domain-payload-contract.json",
        "supabase/migrations/20260722_v2731m_exam_history_domain_payload_validate_rpc.sql",
        "tools/check-supabase-exam-history-domain-storage-contract.py",
        "docs/contracts/exam-history-domain-storage-contract.json",
        "tools/check-supabase-exam-history-expected-storage-version-identity-binding.py",
        "docs/contracts/exam-history-expected-storage-version-identity-binding-contract.json",
        "supabase/migrations/20260722_v2731p_exam_history_expected_storage_version_schema.sql",
        "supabase/migrations/20260722_v2731q_exam_history_operation_identity_expected_version_rpc.sql",
        "supabase/migrations/20260722_v2731r_exam_history_idempotency_expected_version_reserve_rpc.sql",
        "supabase/migrations/20260723_v2731s_exam_history_domain_resources.sql",
        "supabase/migrations/20260723_v2731t_exam_history_domain_resource_mutate_rpc.sql",
        "supabase/migrations/20260723_v2731u_exam_history_outer_domain_mutation_rpc.sql",
    ]

    for file_path in required_files:
        check_file_exists(file_path)

    check_json("questions.json")
    check_index_versions()
    check_category_audit()
    check_exam_result_history_adapter()
    check_exam_result_history_fixtures()
    check_exam_result_history_idempotency_flow()
    check_exam_result_history_transactional_mutation_contract()
    check_exam_result_history_operation_identity_issuance_contract()
    check_exam_result_history_operation_identity_idempotency_integration()
    check_exam_result_history_outer_domain_mutation_rpc_contract()
    check_exam_result_history_outer_domain_mutation_e2e_audit()
    check_exam_result_history_outer_domain_mutation_database_test_contract()
    check_exam_result_history_outer_domain_mutation_fixture_harness_contract()
    check_exam_result_history_outer_domain_mutation_harness_readiness()
    check_exam_result_history_domain_payload_contract()
    check_exam_result_history_domain_storage_contract()
    check_exam_result_history_expected_storage_version_binding()
    check_git_diff_check()
    check_protected_core_files_v2356()

    if errors:
        print("\nPRE-FLIGHT FEHLER:")
        for error in errors:
            print(f"- {error}")
        print("\nSTOPP: NICHT COMMITTEN UND NICHT PUSHEN.")
        sys.exit(1)

    print("\nOK: Preflight bestanden.")
    print("FREIGABE: JETZT COMMITTEN UND PUSHEN.")

if __name__ == "__main__":
    main()
