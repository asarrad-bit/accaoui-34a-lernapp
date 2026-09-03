from pathlib import Path
import json
import os
import re
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



def check_exam_result_history_disposable_database_environment_gate_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-"
        "database-environment-gate-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable Datenbank-"
            "Umgebungs-Gate-Vertrag fehlgeschlagen"
        )



def check_exam_result_history_disposable_database_gate_evaluator_adapter_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-database-"
        "gate-evaluator-adapter-readiness.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable Gate-Evaluator- und "
            "Adapter-Readiness-Prüfung fehlgeschlagen"
        )



def check_exam_result_history_disposable_database_harness_gate_integration():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-database-"
        "harness-gate-integration.py"
    )
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    if code != 0:
        errors.append("Supabase-disposable Harness-Gate-Integration fehlgeschlagen")



def check_exam_result_history_disposable_postgresql_driver_selection_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "driver-selection-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Treiberauswahlvertrag fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_driver_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-"
        "driver-readiness.py"
    )
    if stdout:
        print(stdout)
    if stderr:
        print(stderr)
    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Treiber-Readiness "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_dependency_manifest_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-dependency-manifest-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Test-Dependency-Manifest-Vertrag fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_dependency_manifest_materialization():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-dependency-manifest-materialization.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Test-Manifest-Materialisierung fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_readiness_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-readiness-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Test-Python-Umgebungsvertrag fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_descriptor_resolver():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-descriptor-resolver.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Test-Python-Umgebungsdescriptor fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Test-Python-Materialisierungsvertrag fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_plan():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-plan.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Test-Python-Materialisierungsplan fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_plan_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-plan-"
        "acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Materialisierungsplan-Annahme-Guard fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_request_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-request-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Materialisierungs-Autorisierungsanfrage-"
            "Vertrag fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_request_state():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-request-state.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Materialisierungs-Autorisierungsanfrage-State "
            "fehlgeschlagen"
        )




def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_request_transition_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-request-transition-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Autorisierungsanfrage-Transition-Guard "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_consumption_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-consumption-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Materialisierungs-Autorisierungsverbrauchsvertrag "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_consumption_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-consumption-readiness.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Materialisierungs-Autorisierungsverbrauchs-"
            "Readiness fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_consumption_readiness_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-consumption-readiness-"
        "acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Verbrauchs-Readiness-Annahme-Guard fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_operation_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-operation-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Atomarer Autorisierungsverbrauchsoperationsvertrag "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_plan():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-plan.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Atomarer Autorisierungsverbrauchsoperations-Plan "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_plan_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-plan-"
        "acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Atomarer Verbrauchsoperationsplan-Annahme-Guard "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-registry-"
        "adapter-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Atomarer Verbrauchs-Registry-Adapter-Vertrag "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_descriptor():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-registry-"
        "adapter-descriptor.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Atomarer Verbrauchs-Registry-Adapter-Descriptor "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_descriptor_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-registry-"
        "adapter-descriptor-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Registry-Adapter-Descriptor-Annahme-Guard "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-registry-"
        "adapter-readiness.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Registry-Adapter-Readiness fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_readiness_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/"
        "check-supabase-exam-history-disposable-postgresql-"
        "test-python-environment-materialization-"
        "authorization-atomic-consumption-registry-"
        "adapter-readiness-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-"
            "Registry-Adapter-Readiness-Annahme-Guard fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Ausführungsvertrag fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_descriptor():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-descriptor.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Ausführungsdescriptor fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_descriptor_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-descriptor-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Ausführungsdescriptor-Annahme-Guard fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-readiness.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Ausführungs-Readiness fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_readiness_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-readiness-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Ausführungs-Readiness-Annahme-Guard fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_plan():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-plan.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Ausführungsplan fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_plan_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-plan-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Ausführungsplan-Annahme-Guard fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsvertrag fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_descriptor():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-descriptor.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsdescriptor fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_descriptor_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-descriptor-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsdescriptor-Annahme-Guard fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-readiness.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungs-Readiness fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_readiness_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-readiness-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungs-Readiness-Annahme-Guard fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_plan():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-plan.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsplan fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_plan_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-plan-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsplan-Annahme-Guard fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungsvertrag fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_descriptor():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-descriptor.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungsdescriptor fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_descriptor_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-descriptor-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungsdescriptor-Annahme-Guard "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-readiness.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungs-Readiness fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_readiness_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-readiness-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungs-Readiness-Annahme-Guard "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_plan():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-plan.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungsplan fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_plan_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-plan-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungsplan-Annahme-Guard "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungs-Autorisierungsvertrag "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_descriptor():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-descriptor.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungs-Autorisierungsdescriptor "
            "fehlgeschlagen"
        )



def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_descriptor_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-descriptor-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungs-Autorisierungsdescriptor-"
            "Annahme-Guard fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-readiness.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungs-Autorisierungs-Readiness "
            "fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness_acceptance_guard():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-readiness-acceptance-guard.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Registry-Adapter-"
            "Implementierungsausführungs-Autorisierungs-Readiness-"
            "Annahme-Guard fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_local_fake_driver_interface_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver-interface-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Local-Fake-Registry-"
            "Treiber-Schnittstellenvertrag fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_local_fake_driver():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Local-Fake-Registry-"
            "Treiber v27.34b fehlgeschlagen"
        )


def check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_local_fake_driver_adapter_contract():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver-adapter-contract.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-disposable PostgreSQL-Local-Fake-Registry-"
            "Adapter-Verhaltensvertrag v27.34e fehlgeschlagen"
        )


def check_supabase_participant_access_adapter():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-participant-access-adapter.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Teilnehmerzugangs-Adapterprüfung v27.36b "
            "fehlgeschlagen"
        )


def check_supabase_participant_access_bootstrap_bridge():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-participant-access-bootstrap-bridge.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Teilnehmerzugangs-Bootstrap-Brückenprüfung v27.36c "
            "fehlgeschlagen"
        )


def check_supabase_participant_auth_session_adapter_v2737a():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-supabase-participant-auth-session-adapter.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Supabase-Teilnehmer-Auth-/Session-Adapterprüfung v27.37a "
            "fehlgeschlagen"
        )


V2736E_AUTHORIZED_IMPLEMENTATION_FILES = (
    "data/supabase-participant-access-adapter.js",
    "data/supabase-participant-access-bootstrap-bridge.js",
    "data/supabase-participant-access-browser-provider.js",
    "tools/check-participant-access-browser-provider-v2736e.py",
    "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md",
    "tools/preflight.py",
)
V2736E_AUTHORIZATION_HEAD = "ad6ccd8b8e010167f303cf0a24edfe8d8036fb81"


def _git_paths(arguments):
    code, stdout, _stderr = run_command("git " + " ".join(arguments))
    if code != 0:
        return None
    return {
        line.strip().replace("\\", "/")
        for line in stdout.splitlines()
        if line.strip()
    }


def _is_authorized_v2736e_participant_access_scope():
    try:
        task_text = Path("docs/tasks/CURRENT_TASK.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False

    task_lines = task_text.splitlines()

    def single_value(prefix):
        values = [
            line[len(prefix):].strip()
            for line in task_lines
            if line.startswith(prefix)
        ]
        return values[0] if len(values) == 1 else None

    expected_allowed_files = ", ".join(
        f"`{path}`" for path in V2736E_AUTHORIZED_IMPLEMENTATION_FILES
    )
    if not (
        single_value("Task-ID:") == "v27.36e"
        and single_value("Status:") == "AUTHORIZED"
        and single_value("Autorisiert:") == "JA"
        and single_value("Erlaubte Implementierungsdateien:")
        == expected_allowed_files
        and single_value("Commit erlaubt:") == "NEIN"
        and single_value("Push erlaubt:") == "NEIN"
    ):
        return False

    expected_paths = set(V2736E_AUTHORIZED_IMPLEMENTATION_FILES)
    working_paths = _git_paths(["diff", "--name-only"])
    untracked_paths = _git_paths(["ls-files", "--others", "--exclude-standard"])
    if working_paths is None or untracked_paths is None:
        return False
    working_paths.update(untracked_paths)
    if working_paths:
        return working_paths == expected_paths

    committed_paths = _git_paths([
        "diff",
        "--name-only",
        V2736E_AUTHORIZATION_HEAD,
        "HEAD",
    ])
    return committed_paths == expected_paths


def _has_v2736e_participant_access_regression_profile():
    required_paths = (
        Path("data/supabase-participant-access-browser-provider.js"),
        Path("tools/check-participant-access-browser-provider-v2736e.py"),
        Path("docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md"),
    )
    if not all(path.is_file() for path in required_paths):
        return False

    try:
        provider_text = required_paths[0].read_text(encoding="utf-8")
        checker_text = required_paths[1].read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False

    return (
        "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER" in provider_text
        and "resolveAccess" in provider_text
        and "require_v2736d_regression" in checker_text
    )


def check_participant_access_app_entry_v2736d():
    if (
        _is_authorized_v2736e_participant_access_scope()
        or _has_v2736e_participant_access_regression_profile()
    ):
        print(
            "v27.36d-App-Einstieg: PASS über das enge autorisierte "
            "v27.36e-Regressionsprofil"
        )
        return

    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-participant-access-app-entry-v2736d.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Teilnehmerzugangs-App-Einstiegsprüfung v27.36d fehlgeschlagen"
        )


def check_participant_access_browser_provider_v2736e():
    working_paths = _git_paths(["diff", "--name-only"])
    staged_paths = _git_paths(["diff", "--cached", "--name-only"])
    untracked_paths = _git_paths(["ls-files", "--others", "--exclude-standard"])
    if (
        working_paths is not None
        and staged_paths is not None
        and untracked_paths is not None
    ):
        working_paths.update(staged_paths)
        working_paths.update(untracked_paths)
        v2737b_phase = _detect_v2737b_successor_profile_phase(
            working_paths
        )
        if v2737b_phase is not None:
            print(
                "v27.36e-Browser-Provider: PASS über das enge "
                "v27.37b-Nachfolge-Regressionsprofil "
                f"({v2737b_phase})"
            )
            return
        successor_phase = _detect_v2737a_successor_profile_phase(
            working_paths
        )
        if successor_phase is not None:
            print(
                "v27.36e-Browser-Provider: PASS über das enge "
                "v27.37a-Nachfolge-Regressionsprofil "
                f"({successor_phase})"
            )
            return
        post_implementation_phase = (
            _detect_v2736f_post_implementation_profile_phase(working_paths)
        )
        if (
            _is_prepared_v2736f_browser_loader_scope(working_paths)
            or _is_committed_v2736f_browser_loader_scope(working_paths)
            or post_implementation_phase is not None
        ):
            print(
                "v27.36e-Browser-Provider: PASS über das enge autorisierte "
                "v27.36f-Regressionsprofil"
                + (
                    f" ({post_implementation_phase})"
                    if post_implementation_phase is not None
                    else ""
                )
            )
            return

    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-participant-access-browser-provider-v2736e.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Teilnehmerzugangs-Browser-Provider-Prüfung v27.36e "
            "fehlgeschlagen"
        )


def check_participant_access_browser_loader_v2736f():
    working_paths = _git_paths(["diff", "--name-only"])
    staged_paths = _git_paths(["diff", "--cached", "--name-only"])
    untracked_paths = _git_paths(["ls-files", "--others", "--exclude-standard"])
    if (
        working_paths is not None
        and staged_paths is not None
        and untracked_paths is not None
    ):
        working_paths.update(staged_paths)
        working_paths.update(untracked_paths)
        v2737b_phase = _detect_v2737b_successor_profile_phase(
            working_paths
        )
        if v2737b_phase is not None:
            print(
                "v27.36f-Browser-Loader: PASS über das enge "
                "v27.37b-Nachfolge-Regressionsprofil "
                f"({v2737b_phase})"
            )
            return
        successor_phase = _detect_v2737a_successor_profile_phase(
            working_paths
        )
        if successor_phase is not None:
            print(
                "v27.36f-Browser-Loader: PASS über das enge "
                "v27.37a-Nachfolge-Regressionsprofil "
                f"({successor_phase})"
            )
            return

    code, stdout, stderr = run_command(
        f'"{sys.executable}" '
        "tools/check-participant-access-browser-loader-v2736f.py"
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Teilnehmerzugangs-Browser-Loader-Prüfung v27.36f "
            "fehlgeschlagen"
        )


def check_project_continuity_control():
    code, stdout, stderr = run_command(
        f'"{sys.executable}" tools/check-project-continuity-control.py'
    )

    if stdout:
        print(stdout)

    if stderr:
        print(stderr)

    if code != 0:
        errors.append(
            "Projektkontinuitäts- und Task-Steuerungsprüfung v27.34e "
            "fehlgeschlagen"
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

V2736D_AUTHORIZED_IMPLEMENTATION_FILES = (
    "app.js",
    "tools/check-participant-access-app-entry-v2736d.py",
    "docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md",
    "tools/preflight.py",
)

V2736F_AUTHORIZED_IMPLEMENTATION_FILES = (
    "index.html",
    "app.js",
    "data/supabase-participant-access-browser-loader.js",
    "tools/check-participant-access-browser-loader-v2736f.py",
    "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md",
    "tools/preflight.py",
)
V2736F_AUTHORIZATION_HEAD = "88337d5951bffdb3b1591ea5d6d9e5741a4c7477"
V2736F_IMPLEMENTATION_HEAD = "a68dd9e81f26c3a887e668b90e9f5e8973c7ddfa"
V2736F_GATE_FILES = {
    "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
    "docs/PROJECT_MASTERLIST.md",
    "docs/PROJECT_STATE_CURRENT.md",
    "docs/tasks/CURRENT_TASK.md",
    "tools/check-project-continuity-control.py",
}
V2736F_REPAIR_IMPLEMENTATION_FILES = {
    "tools/preflight.py",
    "tools/check-participant-access-browser-loader-v2736f.py",
}
V2736F_REGRESSION_FROZEN_FILES = (
    "data/supabase-participant-access-adapter.js",
    "data/supabase-participant-access-bootstrap-bridge.js",
    "data/supabase-participant-access-browser-provider.js",
)
V2736F_POST_IMPLEMENTATION_FROZEN_FILES = (
    "index.html",
    "app.js",
    "data/supabase-participant-access-browser-loader.js",
    "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md",
    *V2736F_REGRESSION_FROZEN_FILES,
)


def _is_authorized_v2736d_app_scope(changed_paths):
    expected_paths = set(V2736D_AUTHORIZED_IMPLEMENTATION_FILES)
    if changed_paths != expected_paths:
        return False

    try:
        task_text = Path("docs/tasks/CURRENT_TASK.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False

    task_lines = task_text.splitlines()

    def single_value(prefix):
        values = [
            line[len(prefix):].strip()
            for line in task_lines
            if line.startswith(prefix)
        ]
        return values[0] if len(values) == 1 else None

    expected_allowed_files = ", ".join(
        f"`{path}`" for path in V2736D_AUTHORIZED_IMPLEMENTATION_FILES
    )
    return (
        single_value("Task-ID:") == "v27.36d"
        and single_value("Status:") == "AUTHORIZED"
        and single_value("Autorisiert:") == "JA"
        and single_value("Erlaubte Implementierungsdateien:")
        == expected_allowed_files
        and single_value("Commit erlaubt:") == "NEIN"
        and single_value("Push erlaubt:") == "NEIN"
    )


def _is_authorized_v2736f_browser_loader_scope(changed_paths):
    expected_paths = set(V2736F_AUTHORIZED_IMPLEMENTATION_FILES)
    if changed_paths != expected_paths:
        return False

    try:
        task_text = Path("docs/tasks/CURRENT_TASK.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False

    task_lines = task_text.splitlines()

    def single_value(prefix):
        values = [
            line[len(prefix):].strip()
            for line in task_lines
            if line.startswith(prefix)
        ]
        return values[0] if len(values) == 1 else None

    expected_allowed_files = ", ".join(
        f"`{path}`" for path in V2736F_AUTHORIZED_IMPLEMENTATION_FILES
    )
    return (
        single_value("Task-ID:") == "v27.36f"
        and single_value("Status:") == "AUTHORIZED"
        and single_value("Autorisiert:") == "JA"
        and single_value("Erlaubte Implementierungsdateien:")
        == expected_allowed_files
        and single_value("Commit erlaubt:") == "NEIN"
        and single_value("Push erlaubt:") == "NEIN"
    )


def _has_v2736f_v2736e_regression_profile():
    checker_path = Path(
        "tools/check-participant-access-browser-loader-v2736f.py"
    )
    if not checker_path.is_file():
        return False

    try:
        checker_text = checker_path.read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return False

    required_contract = (
        "def require_v2736e_regression()",
        "validate_v2736e_regression_sources",
        V2736F_AUTHORIZATION_HEAD,
        V2736F_IMPLEMENTATION_HEAD,
        "baseline_bytes(relative_path)",
        "data/supabase-participant-access-adapter.js",
        "data/supabase-participant-access-bootstrap-bridge.js",
        "data/supabase-participant-access-browser-provider.js",
        "resolveAccess entfernt",
        "Überschreibschutz entfernt",
        "fail-closed zu allow",
        "initializeClient eingeschleust",
        "createClient eingeschleust",
        "Auth-Abfrage eingeschleust",
        "Tabellenabfrage eingeschleust",
        "manipulations += require_v2736e_regression()",
    )
    return all(marker in checker_text for marker in required_contract)


def _v2736f_regression_scope_facts_are_valid(
    *,
    phase,
    task_authorized,
    working_paths,
    committed_paths,
    boundary_matches,
    frozen_modules_unchanged,
    profile_available,
):
    expected_paths = set(V2736F_AUTHORIZED_IMPLEMENTATION_FILES)
    if not (
        task_authorized
        and boundary_matches
        and frozen_modules_unchanged
        and profile_available
    ):
        return False
    if phase == "implementation_prepared":
        return working_paths == expected_paths and committed_paths is None
    if phase == "implementation_committed":
        return not working_paths and committed_paths == expected_paths
    return False


def _read_v2736f_head_and_parent():
    code, stdout, _stderr = run_command("git rev-list --parents -n 1 HEAD")
    if code != 0:
        return None
    lineage = stdout.split()
    if len(lineage) != 2:
        return None
    return lineage[0], lineage[1]


def _v2736f_frozen_modules_unchanged(revision):
    changed = _git_paths([
        "diff",
        "--name-only",
        V2736F_AUTHORIZATION_HEAD,
        revision,
        "--",
        *V2736F_REGRESSION_FROZEN_FILES,
    ])
    return changed == set()


def _is_prepared_v2736f_browser_loader_scope(working_paths):
    lineage = _read_v2736f_head_and_parent()
    if lineage is None:
        return False
    head, _parent = lineage
    return _v2736f_regression_scope_facts_are_valid(
        phase="implementation_prepared",
        task_authorized=_is_authorized_v2736f_browser_loader_scope(
            working_paths
        ),
        working_paths=working_paths,
        committed_paths=None,
        boundary_matches=head == V2736F_AUTHORIZATION_HEAD,
        frozen_modules_unchanged=_v2736f_frozen_modules_unchanged(head),
        profile_available=_has_v2736f_v2736e_regression_profile(),
    )


def _is_committed_v2736f_browser_loader_scope(working_paths):
    if working_paths:
        return False
    lineage = _read_v2736f_head_and_parent()
    if lineage is None:
        return False
    head, parent = lineage
    committed_paths = _git_paths(["diff", "--name-only", parent, head])
    if committed_paths is None:
        return False
    return _v2736f_regression_scope_facts_are_valid(
        phase="implementation_committed",
        task_authorized=_is_authorized_v2736f_browser_loader_scope(
            committed_paths
        ),
        working_paths=working_paths,
        committed_paths=committed_paths,
        boundary_matches=parent == V2736F_AUTHORIZATION_HEAD,
        frozen_modules_unchanged=_v2736f_frozen_modules_unchanged(head),
        profile_available=_has_v2736f_v2736e_regression_profile(),
    )


def _read_v2736f_control_fields(text):
    lines = text.splitlines()

    def single_value(prefix):
        values = [
            line[len(prefix):].strip()
            for line in lines
            if line.startswith(prefix)
        ]
        return values[0] if len(values) == 1 else None

    return {
        "task_id": single_value("Task-ID:"),
        "status": single_value("Status:"),
        "authorized": single_value("Autorisiert:"),
        "allowed": single_value("Erlaubte Implementierungsdateien:"),
        "commit_allowed": single_value("Commit erlaubt:"),
        "push_allowed": single_value("Push erlaubt:"),
    }


def _v2736f_task_kind_from_text(text):
    fields = _read_v2736f_control_fields(text)
    original_allowed = ", ".join(
        f"`{path}`" for path in V2736F_AUTHORIZED_IMPLEMENTATION_FILES
    )
    repair_allowed = ", ".join(
        f"`{path}`" for path in (
            "tools/preflight.py",
            "tools/check-participant-access-browser-loader-v2736f.py",
        )
    )
    common_locked = (
        fields["commit_allowed"] == "NEIN"
        and fields["push_allowed"] == "NEIN"
    )
    if (
        fields["task_id"] == "v27.36f"
        and fields["status"] == "AUTHORIZED"
        and fields["authorized"] == "JA"
        and fields["allowed"] == original_allowed
        and common_locked
    ):
        return "v2736f_authorized"
    if (
        fields["task_id"] == "v27.36f-REPAIR"
        and fields["status"] == "AUTHORIZED"
        and fields["authorized"] == "JA"
        and fields["allowed"] == repair_allowed
        and common_locked
    ):
        return "repair_authorized"
    if (
        fields["task_id"] == "NONE"
        and fields["status"] == "BLOCKED"
        and fields["authorized"] == "NEIN"
        and fields["allowed"] == "KEINE"
        and common_locked
    ):
        return "closed"
    return "invalid"


def _read_v2736f_current_task_kind():
    try:
        task_text = Path("docs/tasks/CURRENT_TASK.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return "invalid"
    return _v2736f_task_kind_from_text(task_text)


def _read_git_text_at_revision(revision, relative_path):
    code, stdout, _stderr = run_command(
        f'git show "{revision}:{relative_path}"'
    )
    return stdout if code == 0 else None


def _git_is_ancestor(ancestor, descendant):
    code, _stdout, _stderr = run_command(
        f"git merge-base --is-ancestor {ancestor} {descendant}"
    )
    return code == 0


def _v2736f_closure_kind_from_state_text(state_text):
    if (
        "Abgeschlossener technischer Schritt v27.36f" in state_text
        and "v27.36f abgeschlossen." in state_text
    ):
        return "original"
    if (
        "Abgeschlossener Repair-Task v27.36f-REPAIR" in state_text
        and "v27.36f-REPAIR abgeschlossen." in state_text
    ):
        return "repair"
    return None


def _read_current_v2736f_closure_kind():
    try:
        state_text = Path("docs/PROJECT_STATE_CURRENT.md").read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeError):
        return None
    return _v2736f_closure_kind_from_state_text(state_text)


def _read_v2736f_post_implementation_history():
    code, stdout, _stderr = run_command(
        "git rev-list --reverse " + V2736F_IMPLEMENTATION_HEAD + "..HEAD"
    )
    if code != 0:
        return None
    commits = [line.strip() for line in stdout.splitlines() if line.strip()]
    previous = V2736F_IMPLEMENTATION_HEAD
    roles = []
    repair_gate_seen = False
    repair_implementation_seen = False
    repair_implementation_parent_is_authorization = False
    repair_closure_seen = False
    original_closure_seen = False
    for commit in commits:
        code, lineage_text, _stderr = run_command(
            "git rev-list --parents -n 1 " + commit
        )
        lineage = lineage_text.split() if code == 0 else []
        if len(lineage) != 2 or lineage[1] != previous:
            return None
        files = _git_paths(["diff", "--name-only", previous, commit])
        task_text = _read_git_text_at_revision(
            commit, "docs/tasks/CURRENT_TASK.md"
        )
        if not files or task_text is None:
            return None
        task_kind = _v2736f_task_kind_from_text(task_text)
        if (
            task_kind == "repair_authorized"
            and files.issubset(V2736F_GATE_FILES)
        ):
            if repair_closure_seen or original_closure_seen:
                return None
            repair_gate_seen = True
            roles.append("repair_gate")
        elif (
            task_kind == "repair_authorized"
            and files == V2736F_REPAIR_IMPLEMENTATION_FILES
        ):
            if (
                not repair_gate_seen
                or repair_implementation_seen
                or repair_closure_seen
                or original_closure_seen
            ):
                return None
            repair_implementation_parent_is_authorization = (
                bool(roles) and roles[-1] == "repair_gate"
            )
            if not repair_implementation_parent_is_authorization:
                return None
            repair_implementation_seen = True
            roles.append("repair_implementation")
        elif task_kind == "closed" and files == V2736F_GATE_FILES:
            state_text = _read_git_text_at_revision(
                commit, "docs/PROJECT_STATE_CURRENT.md"
            )
            if state_text is None:
                return None
            closure_kind = _v2736f_closure_kind_from_state_text(state_text)
            if closure_kind == "repair":
                if (
                    not repair_implementation_seen
                    or repair_closure_seen
                    or original_closure_seen
                ):
                    return None
                repair_closure_seen = True
                roles.append("repair_closure")
            elif closure_kind == "original":
                if original_closure_seen or (
                    repair_gate_seen and not repair_closure_seen
                ):
                    return None
                original_closure_seen = True
                roles.append("original_closure")
            else:
                return None
        else:
            return None
        previous = commit
    return {
        "valid": True,
        "roles": tuple(roles),
        "last_role": roles[-1] if roles else None,
        "repair_gate_seen": repair_gate_seen,
        "repair_implementation_seen": repair_implementation_seen,
        "repair_implementation_parent_is_authorization": (
            repair_implementation_parent_is_authorization
        ),
        "repair_closure_seen": repair_closure_seen,
        "original_closure_seen": original_closure_seen,
    }


def _v2736f_post_implementation_files_unchanged():
    if not _git_is_ancestor(V2736F_IMPLEMENTATION_HEAD, "HEAD"):
        return False
    changed = _git_paths([
        "diff",
        "--name-only",
        V2736F_IMPLEMENTATION_HEAD,
        "--",
        *V2736F_POST_IMPLEMENTATION_FROZEN_FILES,
    ])
    return changed == set()


def _v2736f_post_implementation_scope_facts_are_valid(
    *,
    phase,
    task_kind,
    working_paths,
    history,
    closure_kind,
    implementation_is_ancestor,
    frozen_files_unchanged,
    profile_available,
):
    if not (
        isinstance(history, dict)
        and history.get("valid") is True
        and implementation_is_ancestor
        and frozen_files_unchanged
        and profile_available
    ):
        return False
    last_role = history.get("last_role")
    if phase == "repair_authorization_committed":
        return (
            task_kind == "repair_authorized"
            and not working_paths
            and history.get("repair_gate_seen") is True
            and history.get("repair_implementation_seen") is False
            and last_role == "repair_gate"
        )
    if phase == "repair_implementation_prepared":
        return (
            task_kind == "repair_authorized"
            and working_paths == V2736F_REPAIR_IMPLEMENTATION_FILES
            and history.get("repair_gate_seen") is True
            and history.get("repair_implementation_seen") is False
            and last_role == "repair_gate"
        )
    if phase == "repair_implementation_committed":
        return (
            task_kind == "repair_authorized"
            and not working_paths
            and history.get("repair_implementation_seen") is True
            and history.get("repair_implementation_parent_is_authorization") is True
            and last_role == "repair_implementation"
        )
    if phase == "repair_closure_prepared":
        return (
            task_kind == "closed"
            and working_paths == V2736F_GATE_FILES
            and closure_kind == "repair"
            and history.get("repair_implementation_seen") is True
            and history.get("repair_closure_seen") is False
            and last_role == "repair_implementation"
        )
    if phase == "repair_closure_committed":
        return (
            task_kind == "closed"
            and not working_paths
            and history.get("repair_closure_seen") is True
            and last_role == "repair_closure"
        )
    if phase == "closure_prepared":
        repair_path_complete = (
            history.get("repair_gate_seen") is False
            or history.get("repair_closure_seen") is True
        )
        return (
            task_kind == "closed"
            and working_paths == V2736F_GATE_FILES
            and closure_kind == "original"
            and history.get("original_closure_seen") is False
            and repair_path_complete
            and last_role in {None, "repair_closure"}
        )
    if phase == "closure_committed":
        return (
            task_kind == "closed"
            and not working_paths
            and history.get("original_closure_seen") is True
            and last_role == "original_closure"
        )
    return False


def _detect_v2736f_post_implementation_profile_phase(working_paths):
    history = _read_v2736f_post_implementation_history()
    task_kind = _read_v2736f_current_task_kind()
    closure_kind = _read_current_v2736f_closure_kind()
    shared = {
        "task_kind": task_kind,
        "working_paths": working_paths,
        "history": history,
        "closure_kind": closure_kind,
        "implementation_is_ancestor": _git_is_ancestor(
            V2736F_IMPLEMENTATION_HEAD, "HEAD"
        ),
        "frozen_files_unchanged": (
            _v2736f_post_implementation_files_unchanged()
        ),
        "profile_available": _has_v2736f_v2736e_regression_profile(),
    }
    for phase in (
        "repair_authorization_committed",
        "repair_implementation_prepared",
        "repair_implementation_committed",
        "repair_closure_prepared",
        "repair_closure_committed",
        "closure_prepared",
        "closure_committed",
    ):
        if _v2736f_post_implementation_scope_facts_are_valid(
            phase=phase, **shared
        ):
            return phase
    return None


V2737A_GATE_REPAIR_BASE_SHA = "ac997149fe9600d735dcc237b0a30232d279cc52"
V2737A_GATE_REPAIR_FOLLOWUP_BASE_SHA = "ec8f20216d8dcb13417cca27699febc998d6dcd9"
V2737A_GATE_FILES = set(V2736F_GATE_FILES)
V2737A_GATE_REPAIR_FILES = {
    *V2737A_GATE_FILES,
    "tools/preflight.py",
}
V2737A_AUTHORIZED_IMPLEMENTATION_FILES = (
    "data/supabase-participant-auth-session-adapter.js",
    "tools/check-supabase-participant-auth-session-adapter.py",
    "docs/SUPABASE_PARTICIPANT_AUTH_SESSION_ADAPTER_V2737A.md",
    "tools/preflight.py",
)
V2737A_FROZEN_PRODUCT_FILES = (
    "index.html",
    "app.js",
    "style.css",
    "questions.json",
    "data/supabase-client-adapter.js",
    "data/supabase-client-bootstrap.js",
    "data/supabase-participant-access-adapter.js",
    "data/supabase-participant-access-bootstrap-bridge.js",
    "data/supabase-participant-access-browser-provider.js",
    "data/supabase-participant-access-browser-loader.js",
)
V2737A_HISTORY_ATOMIC_REPAIR = ("atomic_repair",)
V2737A_HISTORY_ATOMIC_FOLLOWUP = (
    "atomic_repair",
    "atomic_followup",
)
V2737A_HISTORY_AUTHORIZED = (
    "atomic_repair",
    "atomic_followup",
    "v2737a_gate",
)
V2737A_HISTORY_IMPLEMENTED = (
    "atomic_repair",
    "atomic_followup",
    "v2737a_gate",
    "v2737a_implementation",
)
V2737A_HISTORY_CLOSED = (
    "atomic_repair",
    "atomic_followup",
    "v2737a_gate",
    "v2737a_implementation",
    "v2737a_closure",
)


def _v2737a_task_kind_from_text(text):
    fields = _read_v2736f_control_fields(text)
    lines = text.splitlines()

    def single_value(prefix):
        values = [
            line[len(prefix):].strip()
            for line in lines
            if line.startswith(prefix)
        ]
        return values[0] if len(values) == 1 else None

    locked = (
        fields["commit_allowed"] == "NEIN"
        and fields["push_allowed"] == "NEIN"
    )
    if (
        fields["task_id"] == "NONE"
        and fields["status"] == "BLOCKED"
        and fields["authorized"] == "NEIN"
        and fields["allowed"] == "KEINE"
        and locked
    ):
        last_step = single_value("Letzter abgeschlossener Kontrollschritt:")
        if last_step == "v27.37a-GATE-REPAIR":
            return "repair_closed"
        if last_step == "v27.37a-GATE-REPAIR-FOLLOWUP":
            return "followup_closed"
        if last_step == "v27.37a":
            return "v2737a_closed"
        return "other_closed"
    expected_allowed = ", ".join(
        f"`{path}`" for path in V2737A_AUTHORIZED_IMPLEMENTATION_FILES
    )
    if (
        fields["task_id"] == "v27.37a"
        and fields["status"] == "AUTHORIZED"
        and fields["authorized"] == "JA"
        and fields["allowed"] == expected_allowed
        and locked
    ):
        return "v2737a_authorized"
    return "invalid"


def _read_v2737a_current_task_kind():
    try:
        text = Path("docs/tasks/CURRENT_TASK.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return "invalid"
    return _v2737a_task_kind_from_text(text)


def _v2737a_gate_repair_document_contract_is_valid(text):
    return all(marker in text for marker in (
        "Abgeschlossener atomarer Bootstrap-Repair v27.37a-GATE-REPAIR",
        "v27.37a-GATE-REPAIR abgeschlossen.",
        "Unbekannte zukünftige Tasks werden nicht pauschal zugelassen.",
        "Supabase bleibt NICHT LIVE.",
        "Keine echten Keys.",
        "Keine echten Teilnehmerdaten.",
        "v2737a_gate_repair_atomic_prepared",
        "v2737a_gate_repair_atomic_committed",
    ))


def _v2737a_gate_repair_followup_document_contract_is_valid(text):
    return all(marker in text for marker in (
        "Abgeschlossener atomarer Follow-up-Repair v27.37a-GATE-REPAIR-FOLLOWUP",
        "v27.37a-GATE-REPAIR-FOLLOWUP abgeschlossen.",
        "v2737a_gate_repair_followup_atomic_prepared",
        "v2737a_gate_repair_followup_atomic_committed",
        "Supabase bleibt NICHT LIVE.",
        "Keine echten Keys.",
        "Keine echten Teilnehmerdaten.",
    ))


def _v2737a_product_texts():
    texts = {}
    try:
        for relative_path in V2737A_FROZEN_PRODUCT_FILES:
            texts[relative_path] = Path(relative_path).read_text(encoding="utf-8")
    except (OSError, UnicodeError):
        return None
    return texts


def _read_v2737a_git_blob_utf8(revision, relative_path):
    try:
        result = subprocess.run(
            [
                "git",
                "show",
                f"{revision}:{relative_path}",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0:
        return None
    try:
        return result.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _v2737a_git_blob_reader_selftest():
    index_text = _read_v2737a_git_blob_utf8(
        V2737A_GATE_REPAIR_BASE_SHA,
        "index.html",
    )
    if (
        not isinstance(index_text, str)
        or "🏠" not in index_text
        or "\ufffd" in index_text
    ):
        return False
    if _read_v2737a_git_blob_utf8("0" * 40, "index.html") is not None:
        return False
    return _read_v2737a_git_blob_utf8(
        V2737A_GATE_REPAIR_BASE_SHA,
        "missing/v2737a-frozen-product.js",
    ) is None


def _v2737a_baseline_product_texts():
    texts = {}
    for relative_path in V2737A_FROZEN_PRODUCT_FILES:
        text = _read_v2737a_git_blob_utf8(
            V2737A_GATE_REPAIR_BASE_SHA,
            relative_path,
        )
        if text is None:
            return None
        texts[relative_path] = text
    return texts


def _v2737a_product_semantic_contract_is_valid(texts):
    if not isinstance(texts, dict) or set(texts) != set(V2737A_FROZEN_PRODUCT_FILES):
        return False
    index_text = texts["index.html"]
    app_text = texts["app.js"]
    adapter_text = texts["data/supabase-participant-access-adapter.js"]
    bridge_text = texts["data/supabase-participant-access-bootstrap-bridge.js"]
    provider_text = texts["data/supabase-participant-access-browser-provider.js"]
    loader_text = texts["data/supabase-participant-access-browser-loader.js"]
    loader_tag = (
        '<script id="accaoui-participant-access-browser-loader" '
        'src="data/supabase-participant-access-browser-loader.js" '
        'data-enabled="false"></script>'
    )
    if index_text.count(loader_tag) != 1 or 'data-enabled="true"' in index_text:
        return False
    if index_text.index(loader_tag) > index_text.index('<script src="app.js?v=24.8"></script>'):
        return False
    required_by_source = {
        "app": (
            "isParticipantAccessBrowserLoaderRequestedV2736F",
            "awaitParticipantAccessBrowserLoaderV2736F",
            'createParticipantAccessNoticeStateV2736D("access_error")',
            "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
            "provider.resolveAccess",
        ),
        "adapter": (
            "createParticipantAccessAdapter",
            "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY",
            "async function resolveAccess()",
        ),
        "bridge": (
            "createParticipantAccessBootstrapBridge",
            "bootstrap.getClient",
            "createParticipantAccessAdapter",
            "async function resolveAccess()",
        ),
        "provider": (
            "ACCAOUI_PARTICIPANT_ACCESS_ADAPTER_FACTORY",
            "ACCAOUI_PARTICIPANT_ACCESS_BOOTSTRAP_BRIDGE_FACTORY",
            "ACCAOUI_PARTICIPANT_ACCESS_APP_PROVIDER",
            "async function resolveAccess()",
        ),
        "loader": (
            'enabled !== "true"',
            "ACCAOUI_PARTICIPANT_ACCESS_BROWSER_LOADER_READY",
            'status: "ready"',
            'status: "error"',
            "provider.resolveAccess",
        ),
    }
    sources = {
        "app": app_text,
        "adapter": adapter_text,
        "bridge": bridge_text,
        "provider": provider_text,
        "loader": loader_text,
    }
    if any(
        marker not in sources[name]
        for name, markers in required_by_source.items()
        for marker in markers
    ):
        return False
    forbidden_composition_tokens = (
        "supabase.createClient",
        "initializeClient()",
        "client.auth.getSession",
        "client.from(",
    )
    if any(token in provider_text or token in loader_text for token in forbidden_composition_tokens):
        return False
    forbidden_app_tokens = (
        "client.auth.getSession()",
        "client.from(",
        "bootstrap.initializeClient()",
        "supabase.createClient()",
    )
    return not any(token in app_text for token in forbidden_app_tokens)


def _v2737a_frozen_product_contract_is_valid(
    baseline_texts,
    candidate_texts,
):
    expected_paths = set(V2737A_FROZEN_PRODUCT_FILES)
    if not isinstance(baseline_texts, dict) or set(baseline_texts) != expected_paths:
        return False
    if not isinstance(candidate_texts, dict) or set(candidate_texts) != expected_paths:
        return False
    if any(
        not isinstance(baseline_texts[path], str)
        or not isinstance(candidate_texts[path], str)
        or candidate_texts[path] != baseline_texts[path]
        for path in V2737A_FROZEN_PRODUCT_FILES
    ):
        return False
    return _v2737a_product_semantic_contract_is_valid(candidate_texts)


def _v2737a_frozen_products_unchanged():
    if not _git_is_ancestor(V2737A_GATE_REPAIR_BASE_SHA, "HEAD"):
        return False
    return _v2737a_frozen_product_contract_is_valid(
        _v2737a_baseline_product_texts(),
        _v2737a_product_texts(),
    )


def _read_v2737a_successor_history():
    code, stdout, _stderr = run_command(
        "git rev-list --reverse " + V2737A_GATE_REPAIR_BASE_SHA + "..HEAD"
    )
    if code != 0:
        return None
    commits = [line.strip() for line in stdout.splitlines() if line.strip()]
    previous = V2737A_GATE_REPAIR_BASE_SHA
    roles = []
    followup_seen = False
    gate_seen = False
    implementation_seen = False
    closure_seen = False
    for index, commit in enumerate(commits):
        code, lineage_text, _stderr = run_command(
            "git rev-list --parents -n 1 " + commit
        )
        lineage = lineage_text.split() if code == 0 else []
        if len(lineage) != 2 or lineage[1] != previous:
            return None
        files = _git_paths(["diff", "--name-only", previous, commit])
        task_text = _read_v2737a_git_blob_utf8(
            commit, "docs/tasks/CURRENT_TASK.md"
        )
        if not files or task_text is None:
            return None
        task_kind = _v2737a_task_kind_from_text(task_text)
        if index == 0:
            state_text = _read_v2737a_git_blob_utf8(
                commit, "docs/PROJECT_STATE_CURRENT.md"
            )
            if not (
                files == V2737A_GATE_REPAIR_FILES
                and task_kind == "repair_closed"
                and state_text is not None
                and _v2737a_gate_repair_document_contract_is_valid(state_text)
            ):
                return None
            roles.append("atomic_repair")
        elif (
            task_kind == "followup_closed"
            and files == V2737A_GATE_REPAIR_FILES
        ):
            state_text = _read_v2737a_git_blob_utf8(
                commit, "docs/PROJECT_STATE_CURRENT.md"
            )
            if not (
                roles == list(V2737A_HISTORY_ATOMIC_REPAIR)
                and not followup_seen
                and state_text is not None
                and _v2737a_gate_repair_followup_document_contract_is_valid(
                    state_text
                )
            ):
                return None
            followup_seen = True
            roles.append("atomic_followup")
        elif task_kind == "v2737a_authorized" and files == V2737A_GATE_FILES:
            if (
                roles != list(V2737A_HISTORY_ATOMIC_FOLLOWUP)
                or gate_seen
                or implementation_seen
                or closure_seen
            ):
                return None
            gate_seen = True
            roles.append("v2737a_gate")
        elif (
            task_kind == "v2737a_authorized"
            and files == set(V2737A_AUTHORIZED_IMPLEMENTATION_FILES)
        ):
            if not gate_seen or implementation_seen or closure_seen:
                return None
            implementation_seen = True
            roles.append("v2737a_implementation")
        elif task_kind == "v2737a_closed" and files == V2737A_GATE_FILES:
            if not implementation_seen or closure_seen:
                return None
            closure_seen = True
            roles.append("v2737a_closure")
        else:
            return None
        previous = commit
    return {
        "valid": True,
        "roles": tuple(roles),
        "last_role": roles[-1] if roles else None,
        "repair_seen": bool(roles) and roles[0] == "atomic_repair",
        "followup_seen": followup_seen,
        "gate_seen": gate_seen,
        "implementation_seen": implementation_seen,
        "closure_seen": closure_seen,
    }


def _v2737a_successor_scope_facts_are_valid(
    *,
    phase,
    task_kind,
    working_paths,
    history,
    products_unchanged,
    repair_documented,
    followup_documented,
):
    if not (
        isinstance(history, dict)
        and history.get("valid") is True
        and products_unchanged
        and repair_documented
    ):
        return False
    last_role = history.get("last_role")
    implementation_files = set(V2737A_AUTHORIZED_IMPLEMENTATION_FILES)
    if phase == "v2737a_gate_repair_atomic_committed":
        return (
            task_kind == "repair_closed"
            and not working_paths
            and history.get("roles") == V2737A_HISTORY_ATOMIC_REPAIR
            and history.get("followup_seen") is False
            and history.get("gate_seen") is False
            and history.get("implementation_seen") is False
            and history.get("closure_seen") is False
        )
    if phase == "v2737a_gate_repair_followup_atomic_prepared":
        return (
            task_kind == "followup_closed"
            and working_paths == V2737A_GATE_REPAIR_FILES
            and history.get("roles") == V2737A_HISTORY_ATOMIC_REPAIR
            and history.get("followup_seen") is False
            and history.get("gate_seen") is False
            and history.get("implementation_seen") is False
            and history.get("closure_seen") is False
            and followup_documented
        )
    if phase == "v2737a_gate_repair_followup_atomic_committed":
        return (
            task_kind == "followup_closed"
            and not working_paths
            and history.get("roles") == V2737A_HISTORY_ATOMIC_FOLLOWUP
            and history.get("followup_seen") is True
            and history.get("gate_seen") is False
            and history.get("implementation_seen") is False
            and history.get("closure_seen") is False
            and last_role == "atomic_followup"
            and followup_documented
        )
    if phase == "v2737a_authorization_prepared":
        return (
            task_kind == "v2737a_authorized"
            and bool(working_paths)
            and working_paths <= V2737A_GATE_FILES
            and history.get("roles") == V2737A_HISTORY_ATOMIC_FOLLOWUP
            and history.get("followup_seen") is True
            and history.get("gate_seen") is False
            and history.get("implementation_seen") is False
            and history.get("closure_seen") is False
            and followup_documented
        )
    if phase == "v2737a_authorization_committed":
        return (
            task_kind == "v2737a_authorized"
            and not working_paths
            and history.get("roles") == V2737A_HISTORY_AUTHORIZED
            and history.get("followup_seen") is True
            and history.get("gate_seen") is True
            and history.get("implementation_seen") is False
            and history.get("closure_seen") is False
            and last_role == "v2737a_gate"
            and followup_documented
        )
    if phase == "v2737a_implementation_prepared":
        return (
            task_kind == "v2737a_authorized"
            and working_paths == implementation_files
            and history.get("roles") == V2737A_HISTORY_AUTHORIZED
            and history.get("followup_seen") is True
            and history.get("gate_seen") is True
            and history.get("implementation_seen") is False
            and history.get("closure_seen") is False
            and last_role == "v2737a_gate"
            and followup_documented
        )
    if phase == "v2737a_implementation_committed":
        return (
            task_kind == "v2737a_authorized"
            and not working_paths
            and history.get("roles") == V2737A_HISTORY_IMPLEMENTED
            and history.get("followup_seen") is True
            and history.get("gate_seen") is True
            and history.get("implementation_seen") is True
            and history.get("closure_seen") is False
            and last_role == "v2737a_implementation"
            and followup_documented
        )
    if phase == "v2737a_closure_prepared":
        return (
            task_kind == "v2737a_closed"
            and working_paths == V2737A_GATE_FILES
            and history.get("roles") == V2737A_HISTORY_IMPLEMENTED
            and history.get("followup_seen") is True
            and history.get("gate_seen") is True
            and history.get("implementation_seen") is True
            and history.get("closure_seen") is False
            and last_role == "v2737a_implementation"
            and followup_documented
        )
    if phase == "v2737a_closure_committed":
        return (
            task_kind == "v2737a_closed"
            and not working_paths
            and history.get("roles") == V2737A_HISTORY_CLOSED
            and history.get("followup_seen") is True
            and history.get("gate_seen") is True
            and history.get("implementation_seen") is True
            and history.get("closure_seen") is True
            and last_role == "v2737a_closure"
            and followup_documented
        )
    return False


def _v2737a_atomic_prepared_scope_facts_are_valid(
    *,
    head_is_base,
    task_kind,
    working_paths,
    products_unchanged,
    repair_documented,
):
    return (
        head_is_base
        and task_kind == "repair_closed"
        and working_paths == V2737A_GATE_REPAIR_FILES
        and products_unchanged
        and repair_documented
    )


def _detect_v2737a_successor_profile_phase(working_paths):
    task_kind = _read_v2737a_current_task_kind()
    products_unchanged = _v2737a_frozen_products_unchanged()
    try:
        state_text = Path("docs/PROJECT_STATE_CURRENT.md").read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeError):
        return None
    repair_documented = _v2737a_gate_repair_document_contract_is_valid(
        state_text
    )
    followup_documented = (
        _v2737a_gate_repair_followup_document_contract_is_valid(state_text)
    )
    code, head, _stderr = run_command("git rev-parse HEAD")
    if code != 0:
        return None
    head = head.strip()
    if head == V2737A_GATE_REPAIR_BASE_SHA:
        if _v2737a_atomic_prepared_scope_facts_are_valid(
            head_is_base=True,
            task_kind=task_kind,
            working_paths=working_paths,
            products_unchanged=products_unchanged,
            repair_documented=repair_documented,
        ):
            return "v2737a_gate_repair_atomic_prepared"
        return None
    history = _read_v2737a_successor_history()
    shared = {
        "task_kind": task_kind,
        "working_paths": working_paths,
        "history": history,
        "products_unchanged": products_unchanged,
        "repair_documented": repair_documented,
        "followup_documented": followup_documented,
    }
    for phase in (
        "v2737a_gate_repair_atomic_committed",
        "v2737a_gate_repair_followup_atomic_prepared",
        "v2737a_gate_repair_followup_atomic_committed",
        "v2737a_authorization_prepared",
        "v2737a_authorization_committed",
        "v2737a_implementation_prepared",
        "v2737a_implementation_committed",
        "v2737a_closure_prepared",
        "v2737a_closure_committed",
    ):
        if _v2737a_successor_scope_facts_are_valid(phase=phase, **shared):
            return phase
    return None


def check_v2737a_successor_profile_scope_logic():
    if not _v2737a_git_blob_reader_selftest():
        errors.append(
            "v27.37a-Git-UTF-8-Baseline-Selbstprüfung fehlgeschlagen"
        )
        return
    print("v27.37a-Git-UTF-8-Baseline-Selbstprüfung: PASS")
    base_history = {
        "valid": True,
        "roles": V2737A_HISTORY_ATOMIC_REPAIR,
        "last_role": "atomic_repair",
        "repair_seen": True,
        "followup_seen": False,
        "gate_seen": False,
        "implementation_seen": False,
        "closure_seen": False,
    }
    followup_history = {
        **base_history,
        "roles": V2737A_HISTORY_ATOMIC_FOLLOWUP,
        "last_role": "atomic_followup",
        "followup_seen": True,
    }
    gate_history = {
        **followup_history,
        "roles": V2737A_HISTORY_AUTHORIZED,
        "last_role": "v2737a_gate",
        "gate_seen": True,
    }
    implementation_history = {
        **gate_history,
        "roles": V2737A_HISTORY_IMPLEMENTED,
        "last_role": "v2737a_implementation",
        "implementation_seen": True,
    }
    closure_history = {
        **implementation_history,
        "roles": V2737A_HISTORY_CLOSED,
        "last_role": "v2737a_closure",
        "closure_seen": True,
    }
    if not _v2737a_atomic_prepared_scope_facts_are_valid(
        head_is_base=True,
        task_kind="repair_closed",
        working_paths=V2737A_GATE_REPAIR_FILES,
        products_unchanged=True,
        repair_documented=True,
    ):
        errors.append(
            "v27.37a-Nachfolgeprofil-Positivprüfung fehlgeschlagen: "
            "v2737a_gate_repair_atomic_prepared"
        )
        return
    gate_paths = tuple(sorted(V2737A_GATE_FILES))
    authorization_subsets = (
        {"docs/tasks/CURRENT_TASK.md"},
        {"docs/PROJECT_STATE_CURRENT.md"},
        set(gate_paths[:2]),
        set(gate_paths[:4]),
        set(gate_paths),
    )
    positive_cases = (
        ("v2737a_gate_repair_atomic_committed", "repair_closed", set(), base_history, False),
        ("v2737a_gate_repair_followup_atomic_prepared", "followup_closed", V2737A_GATE_REPAIR_FILES, base_history, True),
        ("v2737a_gate_repair_followup_atomic_committed", "followup_closed", set(), followup_history, True),
        *(("v2737a_authorization_prepared", "v2737a_authorized", subset, followup_history, True) for subset in authorization_subsets),
        ("v2737a_authorization_committed", "v2737a_authorized", set(), gate_history, True),
        ("v2737a_implementation_prepared", "v2737a_authorized", set(V2737A_AUTHORIZED_IMPLEMENTATION_FILES), gate_history, True),
        ("v2737a_implementation_committed", "v2737a_authorized", set(), implementation_history, True),
        ("v2737a_closure_prepared", "v2737a_closed", V2737A_GATE_FILES, implementation_history, True),
        ("v2737a_closure_committed", "v2737a_closed", set(), closure_history, True),
    )
    for phase, task_kind, working_paths, history, followup_documented in positive_cases:
        if not _v2737a_successor_scope_facts_are_valid(
            phase=phase,
            task_kind=task_kind,
            working_paths=working_paths,
            history=history,
            products_unchanged=True,
            repair_documented=True,
            followup_documented=followup_documented,
        ):
            errors.append(
                "v27.37a-Nachfolgeprofil-Positivprüfung fehlgeschlagen: "
                + phase
            )
            return
    implementation_files = set(V2737A_AUTHORIZED_IMPLEMENTATION_FILES)
    authorization_empty = set()
    authorization_implementation_file = {"data/supabase-participant-auth-session-adapter.js"}
    authorization_preflight_file = {"tools/preflight.py"}
    authorization_app_file = {"app.js"}
    authorization_unknown_file = {"unknown/future-task.txt"}
    authorization_gate_plus_product = {
        "docs/tasks/CURRENT_TASK.md",
        "index.html",
    }
    implementation_extra_file = implementation_files | {"index.html"}
    implementation_missing_file = implementation_files - {"tools/preflight.py"}
    authorization_prepared_wrong_history = (
        "atomic_repair",
        "unexpected",
    )
    authorization_committed_extra_history = (
        *V2737A_HISTORY_ATOMIC_FOLLOWUP,
        "extra_gate",
    )
    authorization_committed_duplicate_gate = (
        *V2737A_HISTORY_AUTHORIZED,
        "v2737a_gate",
    )
    implementation_prepared_extra_history = (
        *V2737A_HISTORY_ATOMIC_FOLLOWUP,
        "unexpected",
    )
    implementation_prepared_wrong_order = (
        "v2737a_gate",
        "atomic_repair",
        "atomic_followup",
    )
    implementation_committed_extra_history = (
        *V2737A_HISTORY_AUTHORIZED,
        "unexpected",
    )
    implementation_committed_gate_after = (
        *V2737A_HISTORY_IMPLEMENTED,
        "v2737a_gate",
    )
    closure_prepared_extra_history = (
        *V2737A_HISTORY_AUTHORIZED,
        "unexpected",
    )
    closure_prepared_already_closed = V2737A_HISTORY_CLOSED
    closure_committed_extra_history = (
        *V2737A_HISTORY_IMPLEMENTED,
        "unexpected",
    )
    closure_committed_implementation_after = (
        *V2737A_HISTORY_CLOSED,
        "v2737a_implementation",
    )
    changed_mutations = (
        ("authorization_prepared_empty", {"docs/tasks/CURRENT_TASK.md"}, authorization_empty),
        ("authorization_prepared_implementation_file", {"docs/tasks/CURRENT_TASK.md"}, authorization_implementation_file),
        ("authorization_prepared_preflight_file", {"docs/tasks/CURRENT_TASK.md"}, authorization_preflight_file),
        ("authorization_prepared_app_file", {"docs/tasks/CURRENT_TASK.md"}, authorization_app_file),
        ("authorization_prepared_unknown_file", {"docs/tasks/CURRENT_TASK.md"}, authorization_unknown_file),
        ("authorization_prepared_gate_plus_product", {"docs/tasks/CURRENT_TASK.md"}, authorization_gate_plus_product),
        ("implementation_prepared_extra_file", implementation_files, implementation_extra_file),
        ("implementation_prepared_missing_file", implementation_files, implementation_missing_file),
        ("authorization_prepared_wrong_history", V2737A_HISTORY_ATOMIC_FOLLOWUP, authorization_prepared_wrong_history),
        ("authorization_committed_extra_history", V2737A_HISTORY_AUTHORIZED, authorization_committed_extra_history),
        ("authorization_committed_duplicate_gate", V2737A_HISTORY_AUTHORIZED, authorization_committed_duplicate_gate),
        ("implementation_prepared_extra_history", V2737A_HISTORY_AUTHORIZED, implementation_prepared_extra_history),
        ("implementation_prepared_wrong_order", V2737A_HISTORY_AUTHORIZED, implementation_prepared_wrong_order),
        ("implementation_committed_extra_history", V2737A_HISTORY_IMPLEMENTED, implementation_committed_extra_history),
        ("implementation_committed_gate_after", V2737A_HISTORY_IMPLEMENTED, implementation_committed_gate_after),
        ("closure_prepared_extra_history", V2737A_HISTORY_IMPLEMENTED, closure_prepared_extra_history),
        ("closure_prepared_already_closed", V2737A_HISTORY_IMPLEMENTED, closure_prepared_already_closed),
        ("closure_committed_extra_history", V2737A_HISTORY_CLOSED, closure_committed_extra_history),
        ("closure_committed_implementation_after", V2737A_HISTORY_CLOSED, closure_committed_implementation_after),
    )
    for label, baseline, mutated in changed_mutations:
        if mutated == baseline:
            errors.append(
                "v27.37a-Nachfolgeprofil-Selbsttest ist wirkungslos: " + label
            )
            return

    def with_roles(history, roles):
        return {**history, "roles": roles}

    negative_cases = (
        ("followup_prepared_wrong_scope", "v2737a_gate_repair_followup_atomic_prepared", "followup_closed", V2737A_GATE_REPAIR_FILES | {"app.js"}, base_history, True, True, True),
        ("followup_prepared_repeat", "v2737a_gate_repair_followup_atomic_prepared", "followup_closed", V2737A_GATE_REPAIR_FILES, followup_history, True, True, True),
        ("followup_prepared_products_changed", "v2737a_gate_repair_followup_atomic_prepared", "followup_closed", V2737A_GATE_REPAIR_FILES, base_history, False, True, True),
        ("followup_prepared_document_missing", "v2737a_gate_repair_followup_atomic_prepared", "followup_closed", V2737A_GATE_REPAIR_FILES, base_history, True, True, False),
        ("followup_committed_missing_followup", "v2737a_gate_repair_followup_atomic_committed", "followup_closed", set(), base_history, True, True, True),
        ("authorization_prepared_empty", "v2737a_authorization_prepared", "v2737a_authorized", authorization_empty, followup_history, True, True, True),
        ("authorization_prepared_implementation_file", "v2737a_authorization_prepared", "v2737a_authorized", authorization_implementation_file, followup_history, True, True, True),
        ("authorization_prepared_preflight_file", "v2737a_authorization_prepared", "v2737a_authorized", authorization_preflight_file, followup_history, True, True, True),
        ("authorization_prepared_app_file", "v2737a_authorization_prepared", "v2737a_authorized", authorization_app_file, followup_history, True, True, True),
        ("authorization_prepared_unknown_file", "v2737a_authorization_prepared", "v2737a_authorized", authorization_unknown_file, followup_history, True, True, True),
        ("authorization_prepared_gate_plus_product", "v2737a_authorization_prepared", "v2737a_authorized", authorization_gate_plus_product, followup_history, True, True, True),
        ("authorization_prepared_wrong_task_id", "v2737a_authorization_prepared", "invalid", {"docs/tasks/CURRENT_TASK.md"}, followup_history, True, True, True),
        ("authorization_prepared_wrong_status", "v2737a_authorization_prepared", "invalid", {"docs/tasks/CURRENT_TASK.md"}, followup_history, True, True, True),
        ("authorization_prepared_not_authorized", "v2737a_authorization_prepared", "invalid", {"docs/tasks/CURRENT_TASK.md"}, followup_history, True, True, True),
        ("authorization_prepared_wrong_history", "v2737a_authorization_prepared", "v2737a_authorized", {"docs/tasks/CURRENT_TASK.md"}, with_roles(followup_history, authorization_prepared_wrong_history), True, True, True),
        ("authorization_committed_extra_history", "v2737a_authorization_committed", "v2737a_authorized", set(), with_roles(gate_history, authorization_committed_extra_history), True, True, True),
        ("authorization_committed_duplicate_gate", "v2737a_authorization_committed", "v2737a_authorized", set(), with_roles(gate_history, authorization_committed_duplicate_gate), True, True, True),
        ("implementation_prepared_extra_file", "v2737a_implementation_prepared", "v2737a_authorized", implementation_extra_file, gate_history, True, True, True),
        ("implementation_prepared_missing_file", "v2737a_implementation_prepared", "v2737a_authorized", implementation_missing_file, gate_history, True, True, True),
        ("implementation_prepared_extra_history", "v2737a_implementation_prepared", "v2737a_authorized", implementation_files, with_roles(gate_history, implementation_prepared_extra_history), True, True, True),
        ("implementation_prepared_wrong_order", "v2737a_implementation_prepared", "v2737a_authorized", implementation_files, with_roles(gate_history, implementation_prepared_wrong_order), True, True, True),
        ("implementation_committed_extra_history", "v2737a_implementation_committed", "v2737a_authorized", set(), with_roles(implementation_history, implementation_committed_extra_history), True, True, True),
        ("implementation_committed_gate_after", "v2737a_implementation_committed", "v2737a_authorized", set(), with_roles(implementation_history, implementation_committed_gate_after), True, True, True),
        ("closure_prepared_wrong_history", "v2737a_closure_prepared", "v2737a_closed", V2737A_GATE_FILES, gate_history, True, True, True),
        ("closure_prepared_wrong_task", "v2737a_closure_prepared", "v2737a_authorized", V2737A_GATE_FILES, implementation_history, True, True, True),
        ("closure_prepared_extra_history", "v2737a_closure_prepared", "v2737a_closed", V2737A_GATE_FILES, with_roles(implementation_history, closure_prepared_extra_history), True, True, True),
        ("closure_prepared_already_closed", "v2737a_closure_prepared", "v2737a_closed", V2737A_GATE_FILES, with_roles(implementation_history, closure_prepared_already_closed), True, True, True),
        ("closure_committed_missing_closure", "v2737a_closure_committed", "v2737a_closed", set(), implementation_history, True, True, True),
        ("closure_committed_extra_history", "v2737a_closure_committed", "v2737a_closed", set(), with_roles(closure_history, closure_committed_extra_history), True, True, True),
        ("closure_committed_implementation_after", "v2737a_closure_committed", "v2737a_closed", set(), with_roles(closure_history, closure_committed_implementation_after), True, True, True),
        ("atomic_repair_products_changed", "v2737a_gate_repair_atomic_committed", "repair_closed", set(), base_history, False, True, False),
        ("atomic_repair_document_missing", "v2737a_gate_repair_atomic_committed", "repair_closed", set(), base_history, True, False, False),
        ("unknown_future_task", "unknown_future_task", "v2737a_authorized", set(), followup_history, True, True, True),
        ("authorization_committed_wrong_task", "v2737a_authorization_committed", "other_closed", set(), gate_history, True, True, True),
    )
    for label, phase, task_kind, working_paths, history, products_unchanged, repair_documented, followup_documented in negative_cases:
        if _v2737a_successor_scope_facts_are_valid(
            phase=phase,
            task_kind=task_kind,
            working_paths=working_paths,
            history=history,
            products_unchanged=products_unchanged,
            repair_documented=repair_documented,
            followup_documented=followup_documented,
        ):
            errors.append(
                "v27.37a-Nachfolgeprofil-Manipulation nicht blockiert: "
                + label
            )
            return
    baseline_texts = _v2737a_baseline_product_texts()
    candidate_texts = dict(baseline_texts) if baseline_texts is not None else None
    if not _v2737a_frozen_product_contract_is_valid(
        baseline_texts,
        candidate_texts,
    ):
        errors.append("v27.37a-Nachfolgeprofil erkennt den gültigen Frozen-Produktvertrag nicht")
        return
    frozen_content_mutations = (
        ("app_access_error_single", "app.js", 'createParticipantAccessNoticeStateV2736D("access_error")', 'createParticipantAccessNoticeStateV2736D("blocked")'),
        ("index_marker_neutral", "index.html", "</body>", "<!-- v2737a mutation --></body>"),
        ("app_marker_neutral", "app.js", "async function initAuthFlow()", "async function initAuthFlow() /* v2737a mutation */"),
        ("style_marker_neutral", "style.css", "ACCAOUI §34a LERN-APP", "ACCAOUI §34a LERN-APP MUTATED"),
        ("questions_marker_neutral", "questions.json", '"id": "roso_001"', '"id": "roso_001_mutated"'),
        ("client_adapter_marker_neutral", "data/supabase-client-adapter.js", "Supabase Client Adapter", "Supabase Client Adapter Mutated"),
        ("client_bootstrap_marker_neutral", "data/supabase-client-bootstrap.js", "Supabase Client Bootstrap", "Supabase Client Bootstrap Mutated"),
        ("adapter_marker_neutral", "data/supabase-participant-access-adapter.js", '"use strict";', '"use strict"; /* v2737a mutation */'),
        ("bridge_marker_neutral", "data/supabase-participant-access-bootstrap-bridge.js", '"use strict";', '"use strict"; /* v2737a mutation */'),
        ("provider_marker_neutral", "data/supabase-participant-access-browser-provider.js", '"use strict";', '"use strict"; /* v2737a mutation */'),
        ("loader_marker_neutral", "data/supabase-participant-access-browser-loader.js", '"use strict";', '"use strict"; /* v2737a mutation */'),
        ("adapter_factory_suffix", "data/supabase-participant-access-adapter.js", "createParticipantAccessAdapter", "createParticipantAccessAdapterRemoved"),
        ("bridge_get_client_suffix", "data/supabase-participant-access-bootstrap-bridge.js", "bootstrap.getClient", "bootstrap.getClientRemoved"),
        ("loader_resolve_access_suffix", "data/supabase-participant-access-browser-loader.js", "provider.resolveAccess", "provider.resolveAccessRemoved"),
        ("provider_resolve_access_removed", "data/supabase-participant-access-browser-provider.js", "async function resolveAccess()", "async function resolveAccessRemoved()"),
        ("data_enabled_true", "index.html", 'data-enabled="false"', 'data-enabled="true"'),
        ("create_client_injected", "data/supabase-participant-access-browser-provider.js", '"use strict";', '"use strict"; supabase.createClient();'),
        ("initialize_client_injected", "data/supabase-participant-access-browser-provider.js", '"use strict";', '"use strict"; bootstrap.initializeClient();'),
        ("auth_query_injected", "app.js", "async function initAuthFlow()", "async function initAuthFlow(){ client.auth.getSession(); }"),
        ("table_query_injected", "data/supabase-participant-access-browser-loader.js", '"use strict";', '"use strict"; client.from("participants");'),
    )
    for label, relative_path, needle, replacement in frozen_content_mutations:
        baseline_value = baseline_texts[relative_path]
        if needle not in baseline_value:
            errors.append(
                "v27.37a-Nachfolgeprofil-Selbstprüfung benötigt Quellmarker: "
                + label
            )
            return
        mutated = dict(baseline_texts)
        mutated[relative_path] = baseline_value.replace(needle, replacement, 1)
        if (
            mutated == baseline_texts
            or mutated[relative_path] == baseline_texts[relative_path]
        ):
            errors.append(
                "v27.37a-Nachfolgeprofil-Produktmanipulation ist wirkungslos: "
                + label
            )
            return
        if _v2737a_frozen_product_contract_is_valid(
            baseline_texts,
            mutated,
        ):
            errors.append(
                "v27.37a-Nachfolgeprofil-Produktmanipulation nicht blockiert: "
                + label
            )
            return
    missing_file = dict(baseline_texts)
    missing_file.pop("app.js")
    extra_file = {**baseline_texts, "unexpected.js": "synthetic"}
    wrong_filename = dict(baseline_texts)
    wrong_filename["wrong-index.html"] = wrong_filename.pop("index.html")
    frozen_map_mutations = (
        ("frozen_file_missing", baseline_texts, missing_file),
        ("seventh_file_added", baseline_texts, extra_file),
        ("wrong_filename", baseline_texts, wrong_filename),
        ("empty_candidate", baseline_texts, {}),
        ("empty_baseline", {}, baseline_texts),
    )
    for label, manipulated_baseline, manipulated_candidate in frozen_map_mutations:
        if manipulated_baseline == manipulated_candidate:
            errors.append(
                "v27.37a-Nachfolgeprofil-Dateimengenmanipulation ist wirkungslos: "
                + label
            )
            return
        if _v2737a_frozen_product_contract_is_valid(
            manipulated_baseline,
            manipulated_candidate,
        ):
            errors.append(
                "v27.37a-Nachfolgeprofil-Dateimengenmanipulation nicht blockiert: "
                + label
            )
            return
    print(
        "v27.37a-Nachfolgeprofil-Selbstprüfung: "
        f"{len(positive_cases) + 1} Positiv-, {len(negative_cases)} Scope- und "
        f"{len(frozen_content_mutations) + len(frozen_map_mutations)} "
        "Produktmanipulationsfälle PASS"
    )


V2737B_GATE_BOOTSTRAP_BASE_SHA = "b5d676d226891b4f53e9e614e015c433c2616ad1"
V2737B_GATE_BOOTSTRAP_REPAIR_BASE_SHA = "b83581612fa25b73f62c4b146e8df782d67c869c"
V2737B_TITLE = "v27.37b – Isolierte Teilnehmer-Auth-/Session-Bootstrap-Brücke"
V2737B_GATE_FILES = set(V2737A_GATE_FILES)
V2737B_BOOTSTRAP_FILE_ORDER = (
    "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
    "docs/PROJECT_MASTERLIST.md",
    "docs/PROJECT_STATE_CURRENT.md",
    "docs/tasks/CURRENT_TASK.md",
    "tools/check-project-continuity-control.py",
    "tools/preflight.py",
)
V2737B_BOOTSTRAP_FILES = set(V2737B_BOOTSTRAP_FILE_ORDER)
V2737B_GATE_BOOTSTRAP_REPAIR_FILES = set(V2737B_BOOTSTRAP_FILE_ORDER)
V2737B_IMPLEMENTATION_FILES = (
    "data/supabase-participant-auth-session-bootstrap-bridge.js",
    "tools/check-supabase-participant-auth-session-bootstrap-bridge.py",
    "docs/SUPABASE_PARTICIPANT_AUTH_SESSION_BOOTSTRAP_BRIDGE_V2737B.md",
    "tools/preflight.py",
)
V2737B_ALLOWED_FILES_VALUE = ", ".join(
    f"`{path}`" for path in V2737B_IMPLEMENTATION_FILES
)
V2737B_FROZEN_PRODUCT_FILES = (
    *V2737A_FROZEN_PRODUCT_FILES,
    "data/supabase-participant-auth-session-adapter.js",
)
V2737B_BOOTSTRAP_SECTION_HEADING = (
    "## v27.37b-GATE-BOOTSTRAP – Kontrollinfrastruktur"
)
V2737B_GATE_BOOTSTRAP_REPAIR_SECTION_HEADING = (
    "## v27.37b-GATE-BOOTSTRAP-REPAIR – Kontrollinfrastruktur"
)
V2737B_GATE_BOOTSTRAP_REPAIR_REQUIRED_MARKERS = (
    "v27.37b-GATE-BOOTSTRAP-REPAIR korrigiert ausschließlich den phasenfesten und strukturellen CURRENT_TASK-Vertrag in Continuity und Preflight.",
    f"Repair-Basis: `{V2737B_GATE_BOOTSTRAP_REPAIR_BASE_SHA}`.",
    "Der einmalige atomare Repair umfasst exakt:",
    "Keine siebte Datei und keine Produktdatei sind zulässig.",
    f"Der Bootstrap-Commit `{V2737B_GATE_BOOTSTRAP_REPAIR_BASE_SHA}` bleibt korrekt.",
    "phasenfremde reale Manipulationsbaselines",
    "unvollständige Kopfstrukturprüfungen",
    "fehlende CURRENT_TASK-Negativtests",
    "verpflichtenden ersten `## `-Abschnitt",
    "exakt die neun bekannten Felder in definierter Reihenfolge",
    "fehlende, doppelte, unbekannte oder ungeordnete Kopffelder bleiben blockiert",
    "Historische Abschnitte dürfen einen ungültigen aktuellen Kopf weder retten noch einen gültigen Kopf beschädigen.",
    "Die drei kanonischen Taskzustände bleiben BASE_CLOSED, AUTHORIZED und CLOSED.",
    "Bootstrap-Phasen verwenden BASE_CLOSED",
    "Authorization- und Implementation-Phasen verwenden AUTHORIZED",
    "Closure-Phasen verwenden CLOSED",
    "niemals den realen CURRENT_TASK als Test-Baseline",
    V2737B_TITLE,
    "exakt zwei Dependencies",
    "exakt drei öffentliche Methoden",
    "`getClient()` exakt einmal pro Operation",
    "kein Client-Cache",
    "ausschließlich `client.auth` als `{ auth }`",
    "Object.freeze({ ok: false, code: \"auth_error\" })",
    "`v2737b_gate_bootstrap_repair_prepared`",
    "`v2737b_gate_bootstrap_repair_committed`",
    "Keine zukünftige Repair-Commit-SHA wird hartcodiert",
    "der Repair darf nur einmal vorkommen.",
    "`CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`",
    "v27.37b wird durch diesen Repair NICHT autorisiert.",
    "frisches separates v27.37b-Autorisierungs-Gate",
    "`.git/v2737b-authorization-preflight-blocked.patch` wird nicht angewendet, nicht verändert und nicht als Implementierungsquelle verwendet.",
    "Kein Produktcode wird geändert.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
)
V2737B_CANONICAL_CONTRACT_FACTS = (
    "v27.37b-GATE-BOOTSTRAP ist ausschließlich Kontrollinfrastruktur.",
    f"Stabile Bootstrap-Basis: `{V2737B_GATE_BOOTSTRAP_BASE_SHA}`.",
    "Keine siebte Datei und keine Produktdatei sind zulässig.",
    "v27.37a bleibt vollständig abgeschlossen und wird nicht wieder geöffnet.",
    f"Der spätere Task heißt exakt `{V2737B_TITLE}`",
    "ist nach diesem Bootstrap aber NICHT autorisiert.",
    "`CURRENT_TASK` bleibt `NONE / BLOCKED / Autorisiert NEIN`.",
    "separates ausdrückliches v27.37b-Autorisierungs-Gate",
    "createParticipantAuthSessionBootstrapBridge({ bootstrap, createParticipantAuthSessionAdapter })",
    "Die Dependencies sind exakt `bootstrap` und `createParticipantAuthSessionAdapter`; eine dritte Dependency ist ausgeschlossen.",
    "Ihre öffentliche Oberfläche enthält exakt `resolveSession()`, `signIn({ email, password })` und `signOut()`.",
    "`resolveSession()`",
    "`signIn({ email, password })`",
    "`signOut()`",
    "Eine vierte öffentliche Methode ist ausgeschlossen.",
    "Pro öffentlicher Operation wird `bootstrap.getClient` sicher genau einmal gelesen",
    "`getClient()` genau einmal aufgerufen",
    "der Client wird nicht dauerhaft gecacht.",
    "Ausschließlich `client.auth` wird als exakt `{ auth }` an `createParticipantAuthSessionAdapter({ auth })` weitergegeben.",
    "Object.freeze({ ok: false, code: \"auth_error\" })",
    "Session-, User-, ID-, E-Mail-, Passwort-, Token-, Config- und Rohfehlerdaten bleiben ausgeschlossen.",
    "Verboten bleiben `initializeClient()`, `getState()`, `createClient()`",
    "Browser-Globals, `window`, `document`, DOM, `localStorage`, `sessionStorage`, Cookies, IndexedDB, Config-Lesen, eigener Netzwerkcode, `.from(...)`, Teilnehmer-, Enrollment- oder Kurslogik, SQL und Migrationen.",
    "`initializeClient()`",
    "`getState()`",
    "`createClient()`",
    "Browser-Globals",
    "`window`",
    "`document`",
    "DOM",
    "`localStorage`",
    "`sessionStorage`",
    "Cookies",
    "IndexedDB",
    "Config-Lesen",
    "eigener Netzwerkcode",
    "`.from(...)`",
    "Teilnehmer-, Enrollment- oder Kurslogik",
    "SQL und Migrationen",
    "Bestehende Produktdateien bleiben frozen.",
    "`v2737b_gate_bootstrap_prepared`",
    "`v2737b_gate_bootstrap_committed`",
    "`authorization_prepared`",
    "`authorization_committed`",
    "`implementation_prepared`",
    "`implementation_committed`",
    "`closure_prepared`",
    "`closure_committed`",
    "Keine zukünftige Bootstrap-, Gate-, Implementierungs- oder Closure-SHA wird hartcodiert",
    "eine Wiederholung und eine allgemeine zukünftige Taskfreigabe bleiben blockiert.",
    "Kein Produktcode wurde geändert.",
    "Supabase bleibt NICHT LIVE.",
    "Keine echten Keys.",
    "Keine echten Teilnehmerdaten.",
)
V2737B_BOOTSTRAP_REQUIRED_MARKERS = V2737B_CANONICAL_CONTRACT_FACTS
V2737B_FACTORY_CONTRACT = (
    "Die spätere Factory ist "
    "`createParticipantAuthSessionBootstrapBridge({ bootstrap, "
    "createParticipantAuthSessionAdapter })`. Die Dependencies sind exakt "
    "`bootstrap` und `createParticipantAuthSessionAdapter`; eine dritte "
    "Dependency ist ausgeschlossen. Ihre öffentliche Oberfläche enthält "
    "exakt `resolveSession()`, `signIn({ email, password })` und `signOut()`. "
    "Eine vierte öffentliche Methode ist ausgeschlossen. Pro öffentlicher "
    "Operation wird `bootstrap.getClient` sicher genau einmal gelesen und "
    "`getClient()` genau einmal aufgerufen; der Client wird nicht dauerhaft "
    "gecacht. Ausschließlich `client.auth` wird als exakt `{ auth }` an "
    "`createParticipantAuthSessionAdapter({ auth })` weitergegeben."
)
V2737B_CANONICAL_CONTRACT_MUTATIONS = (
    (
        "falscher v27.37b-Titel",
        V2737B_TITLE,
        "v27.37b – Manipulierter Titel",
    ),
    (
        "getClient-Vertrag",
        "Pro öffentlicher Operation wird `bootstrap.getClient` sicher genau einmal gelesen",
        "Pro öffentlicher Operation darf `bootstrap.getClient` mehrfach gelesen werden",
    ),
    (
        "client.auth-Vertrag",
        "Ausschließlich `client.auth` wird als exakt `{ auth }` an `createParticipantAuthSessionAdapter({ auth })` weitergegeben.",
        "Der gesamte Client wird an die Adapter-Factory weitergegeben.",
    ),
    (
        "auth_error-Vertrag",
        "Object.freeze({ ok: false, code: \"auth_error\" })",
        "Object.freeze({ ok: false, code: \"other_error\" })",
    ),
    ("Browser-Wiring", "Browser-Globals", "Browser-Wiring erlaubt"),
    ("initializeClient", "`initializeClient()`", "`initializeClientAllowed()`"),
    ("createClient", "`createClient()`", "`createClientAllowed()`"),
    ("getState", "`getState()`", "`getStateAllowed()`"),
    ("Tabellenzugriff", "`.from(...)`", "`.from(\"participants\")` erlaubt"),
    (
        "Domainlogik",
        "Teilnehmer-, Enrollment- oder Kurslogik",
        "Teilnehmer-, Enrollment- und Kurslogik erlaubt",
    ),
    (
        "Live-Supabase",
        "Supabase bleibt NICHT LIVE.",
        "Supabase ist LIVE.",
    ),
)
V2737B_CANONICAL_ADDITIVE_MUTATIONS = (
    (
        "dritte Dependency",
        "Die spätere Factory ist `createParticipantAuthSessionBootstrapBridge({ bootstrap, createParticipantAuthSessionAdapter })`.",
        " Zusätzliche Dependency: `thirdDependency`.",
    ),
    (
        "vierte öffentliche Methode",
        "Eine vierte öffentliche Methode ist ausgeschlossen.",
        " Zusätzliche öffentliche Methode: `debug()`.",
    ),
)
V2737B_BASE_TASK_FIELDS = {
    "Task-ID": "NONE",
    "Status": "BLOCKED",
    "Autorisiert": "NEIN",
    "Titel": "Kein Task autorisiert",
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.37a",
    "Erlaubte Implementierungsdateien": "KEINE",
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2737B_AUTHORIZED_TASK_FIELDS = {
    "Task-ID": "v27.37b",
    "Status": "AUTHORIZED",
    "Autorisiert": "JA",
    "Titel": V2737B_TITLE,
    "Funktionaler Ausgangsstand": "v27.35g",
    "Letzter abgeschlossener Kontrollschritt": "v27.37b-GATE-BOOTSTRAP",
    "Erlaubte Implementierungsdateien": V2737B_ALLOWED_FILES_VALUE,
    "Commit erlaubt": "NEIN",
    "Push erlaubt": "NEIN",
}
V2737B_CLOSED_TASK_FIELDS = {
    **V2737B_BASE_TASK_FIELDS,
    "Letzter abgeschlossener Kontrollschritt": "v27.37b",
}


def _v2737b_current_task_header(text):
    heading = "# Verbindlicher aktueller Task"
    heading_matches = re.findall(rf"(?m)^{re.escape(heading)}$", text)
    if len(heading_matches) != 1 or not text.startswith(heading + "\n"):
        return None
    tail = text[len(heading):]
    match = re.search(r"(?m)^## ", tail)
    if match is None:
        return None
    return heading + tail[:match.start()]


def _v2737b_current_task_header_fields(text):
    header = _v2737b_current_task_header(text)
    if header is None:
        return None
    field_names = []
    fields = {}
    for line in header.splitlines()[1:]:
        if not line:
            continue
        match = re.fullmatch(r"([^:\r\n]+): ([^\r\n]+)", line)
        if match is None:
            return None
        field_names.append(match.group(1))
        fields[match.group(1)] = match.group(2)
    if tuple(field_names) != tuple(V2737B_BASE_TASK_FIELDS):
        return None
    return fields


def _v2737b_replace_in_current_task_header(text, needle, replacement):
    header = _v2737b_current_task_header(text)
    if header is None:
        return None
    mutated_header = _v2737b_replace_exact_once(
        header, needle, replacement
    )
    if mutated_header is None:
        return None
    return mutated_header + text[len(header):]


def _v2737b_task_kind_from_text(text):
    fields = _v2737b_current_task_header_fields(text)
    if fields == V2737B_BASE_TASK_FIELDS:
        return "v2737a_closed"
    if fields == V2737B_AUTHORIZED_TASK_FIELDS:
        return "v2737b_authorized"
    if fields == V2737B_CLOSED_TASK_FIELDS:
        return "v2737b_closed"
    return "invalid"


def _v2737b_expected_current_task_fields_for_phase(phase):
    phase_groups = {
        "v2737b_gate_bootstrap_prepared": V2737B_BASE_TASK_FIELDS,
        "v2737b_gate_bootstrap_committed": V2737B_BASE_TASK_FIELDS,
        "v2737b_gate_bootstrap_repair_prepared": V2737B_BASE_TASK_FIELDS,
        "v2737b_gate_bootstrap_repair_committed": V2737B_BASE_TASK_FIELDS,
        "v2737b_authorization_prepared": V2737B_AUTHORIZED_TASK_FIELDS,
        "v2737b_authorization_committed": V2737B_AUTHORIZED_TASK_FIELDS,
        "v2737b_implementation_prepared": V2737B_AUTHORIZED_TASK_FIELDS,
        "v2737b_implementation_committed": V2737B_AUTHORIZED_TASK_FIELDS,
        "v2737b_closure_prepared": V2737B_CLOSED_TASK_FIELDS,
        "v2737b_closure_committed": V2737B_CLOSED_TASK_FIELDS,
    }
    fields = phase_groups.get(phase)
    return dict(fields) if fields is not None else None


def _build_v2737b_synthetic_current_task(fields):
    if tuple(fields) != tuple(V2737B_BASE_TASK_FIELDS):
        return None
    return (
        "# Verbindlicher aktueller Task\n\n"
        + "\n".join(f"{name}: {value}" for name, value in fields.items())
        + "\n\n## Synthetischer Folgeabschnitt\n\n"
        + "Dieser Abschnitt gehört nicht zum kanonischen CURRENT_TASK-Kopf.\n"
    )


def _v2737b_replace_exact_once(text, needle, replacement):
    if text.count(needle) != 1:
        return None
    mutated = text.replace(needle, replacement, 1)
    if mutated == text or needle in mutated:
        return None
    return mutated


def _v2737b_insert_after_exact_once(text, anchor, addition):
    if text.count(anchor) != 1 or not addition or addition in text:
        return None
    mutated = text.replace(anchor, anchor + addition, 1)
    if (
        mutated == text
        or mutated.count(anchor) != 1
        or mutated.count(addition) != 1
    ):
        return None
    return mutated


def _v2737b_duplicate_exact_once(text, needle):
    if text.count(needle) != 1:
        return None
    mutated = text.replace(needle, needle + "\n" + needle, 1)
    if mutated == text or mutated.count(needle) != 2:
        return None
    return mutated


def _v2737b_replace_in_delimited_block(
    text, block_start, block_end, needle, replacement
):
    if text.count(block_start) != 1 or text.count(block_end) != 1:
        return None
    prefix, tail = text.split(block_start, 1)
    block, suffix = tail.split(block_end, 1)
    mutated_block = _v2737b_replace_exact_once(block, needle, replacement)
    if mutated_block is None:
        return None
    return prefix + block_start + mutated_block + block_end + suffix


def _v2737b_insert_after_in_delimited_block(
    text, block_start, block_end, anchor, addition
):
    if text.count(block_start) != 1 or text.count(block_end) != 1:
        return None
    prefix, tail = text.split(block_start, 1)
    block, suffix = tail.split(block_end, 1)
    mutated_block = _v2737b_insert_after_exact_once(block, anchor, addition)
    if mutated_block is None:
        return None
    return prefix + block_start + mutated_block + block_end + suffix


def _v2737b_bootstrap_section(text):
    if text.count(V2737B_BOOTSTRAP_SECTION_HEADING) != 1:
        return None
    tail = text.split(V2737B_BOOTSTRAP_SECTION_HEADING, 1)[1]
    match = re.search(r"(?m)^## ", tail)
    return tail[:match.start()] if match else tail


def _v2737b_bootstrap_section_is_valid(section):
    if not isinstance(section, str) or not all(
        marker in section for marker in V2737B_BOOTSTRAP_REQUIRED_MARKERS
    ):
        return False
    bootstrap_start = "Der einmalige atomare Bootstrap umfasst exakt:"
    bootstrap_end = "Keine siebte Datei und keine Produktdatei sind zulässig."
    implementation_start = "Der spätere Implementierungsscope umfasst exakt:"
    implementation_end = "Die spätere Factory ist"
    if not (
        section.count(bootstrap_start) == 1
        and section.count(bootstrap_end) == 1
        and section.count(implementation_start) == 1
        and section.count(implementation_end) == 1
    ):
        return False
    bootstrap_list = section.split(bootstrap_start, 1)[1].split(
        bootstrap_end, 1
    )[0].strip()
    implementation_list = section.split(implementation_start, 1)[1].split(
        implementation_end, 1
    )[0].strip()
    if bootstrap_list != "\n".join(
        f"- `{path}`" for path in V2737B_BOOTSTRAP_FILE_ORDER
    ):
        return False
    if implementation_list != "\n".join(
        f"- `{path}`" for path in V2737B_IMPLEMENTATION_FILES
    ):
        return False
    factory_contract_end = "Gültige methodenspezifische v27.37a-Ergebnisse"
    if section.count(factory_contract_end) != 1:
        return False
    factory_contract = (
        implementation_end
        + section.split(implementation_end, 1)[1].split(
            factory_contract_end, 1
        )[0]
    ).strip()
    if factory_contract != V2737B_FACTORY_CONTRACT:
        return False
    shas = set(re.findall(r"\b[0-9a-f]{40}\b", section))
    return shas == {V2737B_GATE_BOOTSTRAP_BASE_SHA}


def _v2737b_bootstrap_document_is_valid(text):
    return _v2737b_bootstrap_section_is_valid(
        _v2737b_bootstrap_section(text)
    )


def _v2737b_current_documents_are_valid():
    paths = (
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
        "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
        "docs/PROJECT_MASTERLIST.md",
    )
    try:
        return all(
            _v2737b_bootstrap_document_is_valid(
                Path(path).read_text(encoding="utf-8")
            )
            for path in paths
        )
    except (OSError, UnicodeError):
        return False


def _v2737b_gate_bootstrap_repair_section(text):
    if text.count(V2737B_GATE_BOOTSTRAP_REPAIR_SECTION_HEADING) != 1:
        return None
    tail = text.split(V2737B_GATE_BOOTSTRAP_REPAIR_SECTION_HEADING, 1)[1]
    match = re.search(r"(?m)^## ", tail)
    return tail[:match.start()] if match else tail


def _v2737b_gate_bootstrap_repair_section_is_valid(section):
    if not isinstance(section, str) or not all(
        marker in section
        for marker in V2737B_GATE_BOOTSTRAP_REPAIR_REQUIRED_MARKERS
    ):
        return False
    file_list_start = "Der einmalige atomare Repair umfasst exakt:"
    file_list_end = "Keine siebte Datei und keine Produktdatei sind zulässig."
    if not (
        section.count(file_list_start) == 1
        and section.count(file_list_end) == 1
    ):
        return False
    file_list = section.split(file_list_start, 1)[1].split(
        file_list_end, 1
    )[0].strip()
    if file_list != "\n".join(
        f"- `{path}`" for path in V2737B_BOOTSTRAP_FILE_ORDER
    ):
        return False
    shas = set(re.findall(r"\b[0-9a-f]{40}\b", section))
    return shas == {V2737B_GATE_BOOTSTRAP_REPAIR_BASE_SHA}


def _v2737b_gate_bootstrap_repair_document_is_valid(text):
    return _v2737b_gate_bootstrap_repair_section_is_valid(
        _v2737b_gate_bootstrap_repair_section(text)
    )


def _v2737b_current_repair_documents_are_valid():
    paths = (
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
        "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
        "docs/PROJECT_MASTERLIST.md",
    )
    try:
        return all(
            _v2737b_gate_bootstrap_repair_document_is_valid(
                Path(path).read_text(encoding="utf-8")
            )
            for path in paths
        )
    except (OSError, UnicodeError):
        return False


def _v2737b_commit_repair_documents_are_valid(commit):
    paths = (
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
        "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
        "docs/PROJECT_MASTERLIST.md",
    )
    texts = [_read_v2737a_git_blob_utf8(commit, path) for path in paths]
    return all(
        isinstance(text, str)
        and _v2737b_gate_bootstrap_repair_document_is_valid(text)
        for text in texts
    )


def _v2737b_commit_documents_are_valid(commit):
    paths = (
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
        "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
        "docs/PROJECT_MASTERLIST.md",
    )
    texts = [
        _read_v2737a_git_blob_utf8(commit, path)
        for path in paths
    ]
    return all(
        isinstance(text, str) and _v2737b_bootstrap_document_is_valid(text)
        for text in texts
    )


def _v2737b_product_texts_at(revision=None):
    texts = {}
    try:
        for path in V2737B_FROZEN_PRODUCT_FILES:
            text = (
                _read_v2737a_git_blob_utf8(revision, path)
                if revision is not None
                else Path(path).read_text(encoding="utf-8")
            )
            if not isinstance(text, str):
                return None
            texts[path] = text
    except (OSError, UnicodeError):
        return None
    return texts


def _v2737b_frozen_product_contract_is_valid(baseline, candidate):
    expected = set(V2737B_FROZEN_PRODUCT_FILES)
    if not isinstance(baseline, dict) or set(baseline) != expected:
        return False
    if not isinstance(candidate, dict) or set(candidate) != expected:
        return False
    if any(candidate[path] != baseline[path] for path in expected):
        return False
    v2737a_baseline = {
        path: baseline[path] for path in V2737A_FROZEN_PRODUCT_FILES
    }
    v2737a_candidate = {
        path: candidate[path] for path in V2737A_FROZEN_PRODUCT_FILES
    }
    return _v2737a_frozen_product_contract_is_valid(
        v2737a_baseline,
        v2737a_candidate,
    )


def _v2737b_frozen_products_unchanged():
    if not _git_is_ancestor(V2737B_GATE_BOOTSTRAP_BASE_SHA, "HEAD"):
        return False
    return _v2737b_frozen_product_contract_is_valid(
        _v2737b_product_texts_at(V2737B_GATE_BOOTSTRAP_BASE_SHA),
        _v2737b_product_texts_at(),
    )


def _read_v2737b_history():
    code, stdout, _stderr = run_command(
        "git rev-list --reverse "
        + V2737B_GATE_BOOTSTRAP_BASE_SHA
        + "..HEAD"
    )
    if code != 0:
        return None
    previous = V2737B_GATE_BOOTSTRAP_BASE_SHA
    roles = []
    for commit in (line.strip() for line in stdout.splitlines() if line.strip()):
        code, lineage_text, _stderr = run_command(
            "git rev-list --parents -n 1 " + commit
        )
        lineage = lineage_text.split() if code == 0 else []
        if len(lineage) != 2 or lineage[1] != previous:
            return None
        files = _git_paths(["diff", "--name-only", previous, commit])
        task_text = _read_v2737a_git_blob_utf8(
            commit, "docs/tasks/CURRENT_TASK.md"
        )
        if files is None or task_text is None:
            return None
        task_kind = _v2737b_task_kind_from_text(task_text)
        if (
            not roles
            and files == V2737B_BOOTSTRAP_FILES
            and task_kind == "v2737a_closed"
            and commit == V2737B_GATE_BOOTSTRAP_REPAIR_BASE_SHA
            and _v2737b_commit_documents_are_valid(commit)
        ):
            roles.append("v2737b_bootstrap")
        elif (
            roles == ["v2737b_bootstrap"]
            and files == V2737B_GATE_BOOTSTRAP_REPAIR_FILES
            and task_kind == "v2737a_closed"
            and _v2737b_commit_repair_documents_are_valid(commit)
        ):
            roles.append("v2737b_bootstrap_repair")
        elif (
            roles == ["v2737b_bootstrap", "v2737b_bootstrap_repair"]
            and files == V2737B_GATE_FILES
            and task_kind == "v2737b_authorized"
        ):
            roles.append("v2737b_gate")
        elif (
            roles
            == ["v2737b_bootstrap", "v2737b_bootstrap_repair", "v2737b_gate"]
            and files == set(V2737B_IMPLEMENTATION_FILES)
            and task_kind == "v2737b_authorized"
        ):
            roles.append("v2737b_implementation")
        elif (
            roles
            == [
                "v2737b_bootstrap",
                "v2737b_bootstrap_repair",
                "v2737b_gate",
                "v2737b_implementation",
            ]
            and files == V2737B_GATE_FILES
            and task_kind == "v2737b_closed"
        ):
            roles.append("v2737b_closure")
        else:
            return None
        previous = commit
    return tuple(roles)


def _v2737b_scope_facts_are_valid(
    *, phase, task_kind, working_paths, history_roles,
    products_unchanged
):
    if not products_unchanged:
        return False
    implementation_files = set(V2737B_IMPLEMENTATION_FILES)
    exact = {
        "v2737b_gate_bootstrap_prepared": (
            "v2737a_closed", V2737B_BOOTSTRAP_FILES, (),
        ),
        "v2737b_gate_bootstrap_committed": (
            "v2737a_closed", set(), ("v2737b_bootstrap",),
        ),
        "v2737b_gate_bootstrap_repair_prepared": (
            "v2737a_closed",
            V2737B_GATE_BOOTSTRAP_REPAIR_FILES,
            ("v2737b_bootstrap",),
        ),
        "v2737b_gate_bootstrap_repair_committed": (
            "v2737a_closed",
            set(),
            ("v2737b_bootstrap", "v2737b_bootstrap_repair"),
        ),
        "v2737b_authorization_committed": (
            "v2737b_authorized", set(),
            ("v2737b_bootstrap", "v2737b_bootstrap_repair", "v2737b_gate"),
        ),
        "v2737b_implementation_prepared": (
            "v2737b_authorized", implementation_files,
            ("v2737b_bootstrap", "v2737b_bootstrap_repair", "v2737b_gate"),
        ),
        "v2737b_implementation_committed": (
            "v2737b_authorized", set(),
            (
                "v2737b_bootstrap", "v2737b_bootstrap_repair",
                "v2737b_gate", "v2737b_implementation",
            ),
        ),
        "v2737b_closure_prepared": (
            "v2737b_closed", V2737B_GATE_FILES,
            (
                "v2737b_bootstrap", "v2737b_bootstrap_repair",
                "v2737b_gate", "v2737b_implementation",
            ),
        ),
        "v2737b_closure_committed": (
            "v2737b_closed", set(),
            (
                "v2737b_bootstrap", "v2737b_bootstrap_repair",
                "v2737b_gate", "v2737b_implementation",
                "v2737b_closure",
            ),
        ),
    }
    if phase == "v2737b_authorization_prepared":
        return (
            task_kind == "v2737b_authorized"
            and bool(working_paths)
            and working_paths <= V2737B_GATE_FILES
            and history_roles
            == ("v2737b_bootstrap", "v2737b_bootstrap_repair")
        )
    return exact.get(phase) == (task_kind, working_paths, history_roles)


def _detect_v2737b_successor_profile_phase(working_paths):
    if not (
        _v2737b_current_documents_are_valid()
        and _v2737b_frozen_products_unchanged()
    ):
        return None
    try:
        task_text = Path("docs/tasks/CURRENT_TASK.md").read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeError):
        return None
    task_kind = _v2737b_task_kind_from_text(task_text)
    code, head, _stderr = run_command("git rev-parse HEAD")
    if code != 0:
        return None
    history_roles = _read_v2737b_history()
    if history_roles is None:
        return None
    head = head.strip()
    candidates = (
        "v2737b_gate_bootstrap_prepared",
        "v2737b_gate_bootstrap_committed",
        "v2737b_gate_bootstrap_repair_prepared",
        "v2737b_gate_bootstrap_repair_committed",
        "v2737b_authorization_prepared",
        "v2737b_authorization_committed",
        "v2737b_implementation_prepared",
        "v2737b_implementation_committed",
        "v2737b_closure_prepared",
        "v2737b_closure_committed",
    )
    if head == V2737B_GATE_BOOTSTRAP_BASE_SHA and history_roles:
        return None
    for phase in candidates:
        if _v2737b_scope_facts_are_valid(
            phase=phase,
            task_kind=task_kind,
            working_paths=working_paths,
            history_roles=history_roles,
            products_unchanged=True,
        ):
            if phase in {
                "v2737b_gate_bootstrap_repair_prepared",
                "v2737b_gate_bootstrap_repair_committed",
                "v2737b_authorization_prepared",
                "v2737b_authorization_committed",
                "v2737b_implementation_prepared",
                "v2737b_implementation_committed",
                "v2737b_closure_prepared",
                "v2737b_closure_committed",
            } and not _v2737b_current_repair_documents_are_valid():
                return None
            return phase
    return None


def check_v2737b_successor_profile_scope_logic():
    repair_history = ("v2737b_bootstrap", "v2737b_bootstrap_repair")
    authorization_history = (*repair_history, "v2737b_gate")
    implementation_history = (*authorization_history, "v2737b_implementation")
    positive_cases = (
        ("v2737b_gate_bootstrap_prepared", "v2737a_closed", V2737B_BOOTSTRAP_FILES, ()),
        ("v2737b_gate_bootstrap_committed", "v2737a_closed", set(), ("v2737b_bootstrap",)),
        ("v2737b_gate_bootstrap_repair_prepared", "v2737a_closed", V2737B_GATE_BOOTSTRAP_REPAIR_FILES, ("v2737b_bootstrap",)),
        ("v2737b_gate_bootstrap_repair_committed", "v2737a_closed", set(), repair_history),
        ("v2737b_authorization_prepared", "v2737b_authorized", {"docs/tasks/CURRENT_TASK.md"}, repair_history),
        ("v2737b_authorization_committed", "v2737b_authorized", set(), authorization_history),
        ("v2737b_implementation_prepared", "v2737b_authorized", set(V2737B_IMPLEMENTATION_FILES), authorization_history),
        ("v2737b_implementation_committed", "v2737b_authorized", set(), implementation_history),
        ("v2737b_closure_prepared", "v2737b_closed", V2737B_GATE_FILES, implementation_history),
        ("v2737b_closure_committed", "v2737b_closed", set(), (*implementation_history, "v2737b_closure")),
    )
    for phase, task_kind, working_paths, history_roles in positive_cases:
        if not _v2737b_scope_facts_are_valid(
            phase=phase,
            task_kind=task_kind,
            working_paths=set(working_paths),
            history_roles=history_roles,
            products_unchanged=True,
        ):
            errors.append(
                "v27.37b-Nachfolgeprofil-Positivprüfung fehlgeschlagen: " + phase
            )
            return
    negative_cases = (
        ("unknown_future_task", "v2737b_authorized", set(), repair_history),
        ("v2737b_gate_bootstrap_prepared", "v2737a_closed", V2737B_BOOTSTRAP_FILES | {"app.js"}, ()),
        ("v2737b_gate_bootstrap_prepared", "v2737a_closed", V2737B_BOOTSTRAP_FILES - {"tools/preflight.py"}, ()),
        ("v2737b_gate_bootstrap_prepared", "v2737b_authorized", V2737B_BOOTSTRAP_FILES, ()),
        ("v2737b_gate_bootstrap_committed", "v2737a_closed", set(), ("v2737b_bootstrap", "v2737b_bootstrap")),
        ("v2737b_gate_bootstrap_repair_prepared", "v2737a_closed", V2737B_GATE_BOOTSTRAP_REPAIR_FILES | {"app.js"}, ("v2737b_bootstrap",)),
        ("v2737b_gate_bootstrap_repair_prepared", "v2737a_closed", V2737B_GATE_BOOTSTRAP_REPAIR_FILES - {"tools/preflight.py"}, ("v2737b_bootstrap",)),
        ("v2737b_gate_bootstrap_repair_prepared", "v2737b_authorized", V2737B_GATE_BOOTSTRAP_REPAIR_FILES, ("v2737b_bootstrap",)),
        ("v2737b_gate_bootstrap_repair_prepared", "v2737a_closed", V2737B_GATE_BOOTSTRAP_REPAIR_FILES, ()),
        ("v2737b_gate_bootstrap_repair_committed", "v2737a_closed", set(), (*repair_history, "v2737b_bootstrap_repair")),
        ("v2737b_authorization_prepared", "v2737b_authorized", {"docs/tasks/CURRENT_TASK.md"}, ("v2737b_bootstrap",)),
        ("v2737b_authorization_prepared", "v2737b_authorized", set(), repair_history),
        ("v2737b_authorization_prepared", "v2737b_authorized", {"app.js"}, repair_history),
        ("v2737b_authorization_prepared", "invalid", {"docs/tasks/CURRENT_TASK.md"}, repair_history),
        ("v2737b_authorization_committed", "v2737b_authorized", set(), (*authorization_history, "v2737b_gate")),
        ("v2737b_implementation_prepared", "v2737b_authorized", set(V2737B_IMPLEMENTATION_FILES) | {"index.html"}, authorization_history),
        ("v2737b_implementation_prepared", "v2737b_authorized", set(V2737B_IMPLEMENTATION_FILES) - {"tools/preflight.py"}, authorization_history),
        ("v2737b_implementation_committed", "v2737b_authorized", set(), authorization_history),
        ("v2737b_closure_prepared", "v2737b_authorized", V2737B_GATE_FILES, implementation_history),
        ("v2737b_closure_prepared", "v2737b_closed", V2737B_GATE_FILES | {"app.js"}, implementation_history),
        ("v2737b_closure_committed", "v2737b_closed", set(), implementation_history),
    )
    for phase, task_kind, working_paths, history_roles in negative_cases:
        if _v2737b_scope_facts_are_valid(
            phase=phase,
            task_kind=task_kind,
            working_paths=set(working_paths),
            history_roles=history_roles,
            products_unchanged=True,
        ):
            errors.append(
                "v27.37b-Nachfolgeprofil-Manipulation nicht blockiert: " + phase
            )
            return
    document_paths = (
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
        "docs/CURSOR_MASTER_CONTEXT_ACCAOUI.md",
        "docs/PROJECT_MASTERLIST.md",
    )
    try:
        document_texts = {
            path: Path(path).read_text(encoding="utf-8")
            for path in document_paths
        }
    except (OSError, UnicodeError) as exc:
        errors.append(f"v27.37b-Dokumentprüfung nicht lesbar: {exc}")
        return
    document_sections = {}
    repair_document_sections = {}
    for path, text in document_texts.items():
        section = _v2737b_bootstrap_section(text)
        if not _v2737b_bootstrap_section_is_valid(section):
            errors.append(
                "v27.37b-Nachfolgeprofil-Dokumentvertrag ungültig: " + path
            )
            return
        document_sections[path] = section
        repair_section = _v2737b_gate_bootstrap_repair_section(text)
        if not _v2737b_gate_bootstrap_repair_section_is_valid(repair_section):
            errors.append(
                "v27.37b-Repair-Nachfolgeprofil-Dokumentvertrag ungültig: "
                + path
            )
            return
        repair_document_sections[path] = repair_section
    document_mutations = 0
    for path, section in document_sections.items():
        for fact in V2737B_CANONICAL_CONTRACT_FACTS:
            mutated = _v2737b_replace_exact_once(section, fact, "")
            if mutated is None or fact in mutated:
                errors.append(
                    "v27.37b-Dokumentmutation hat kein exaktes Ziel: "
                    + path
                    + " / "
                    + fact
                )
                return
            if _v2737b_bootstrap_section_is_valid(mutated):
                errors.append(
                    "v27.37b-Dokumentmutation nicht blockiert: "
                    + path
                    + " / "
                    + fact
                )
                return
            document_mutations += 1
    canonical_section = document_sections["docs/PROJECT_STATE_CURRENT.md"]
    bootstrap_start = "Der einmalige atomare Bootstrap umfasst exakt:"
    bootstrap_end = "Keine siebte Datei und keine Produktdatei sind zulässig."
    implementation_start = "Der spätere Implementierungsscope umfasst exakt:"
    implementation_end = "Die spätere Factory ist"
    for label, paths, block_start, block_end in (
        (
            "Bootstrap",
            V2737B_BOOTSTRAP_FILE_ORDER,
            bootstrap_start,
            bootstrap_end,
        ),
        (
            "Implementierung",
            V2737B_IMPLEMENTATION_FILES,
            implementation_start,
            implementation_end,
        ),
    ):
        for path in paths:
            needle = f"- `{path}`\n"
            mutated = _v2737b_replace_in_delimited_block(
                canonical_section, block_start, block_end, needle, ""
            )
            if mutated is None:
                errors.append(
                    f"v27.37b-{label}smutation hat kein exaktes Dateiziel: {path}"
                )
                return
            if _v2737b_bootstrap_section_is_valid(mutated):
                errors.append(
                    f"v27.37b-{label}smutation nicht blockiert: {path}"
                )
                return
            document_mutations += 1
    added_file_anchor = f"- `{V2737B_IMPLEMENTATION_FILES[0]}`\n"
    added_file_addition = "- `app.js`\n"
    added_file = _v2737b_insert_after_in_delimited_block(
        canonical_section,
        implementation_start,
        implementation_end,
        added_file_anchor,
        added_file_addition,
    )
    if (
        added_file is None
        or added_file.count(added_file_anchor) != 1
        or added_file.count(added_file_addition) != 1
        or _v2737b_bootstrap_section_is_valid(added_file)
    ):
        errors.append(
            "v27.37b-zusätzliche Implementierungsdatei nicht blockiert"
        )
        return
    document_mutations += 1
    for label, needle, replacement in V2737B_CANONICAL_CONTRACT_MUTATIONS:
        mutated = _v2737b_replace_exact_once(
            canonical_section, needle, replacement
        )
        if mutated is None or needle in mutated:
            errors.append(
                "v27.37b-Vertragsmutation hat kein exaktes Ziel: " + label
            )
            return
        if _v2737b_bootstrap_section_is_valid(mutated):
            errors.append(
                "v27.37b-Vertragsmutation nicht blockiert: " + label
            )
            return
        document_mutations += 1
    for label, anchor, addition in V2737B_CANONICAL_ADDITIVE_MUTATIONS:
        mutated = _v2737b_insert_after_exact_once(
            canonical_section, anchor, addition
        )
        if (
            mutated is None
            or mutated.count(anchor) != 1
            or mutated.count(addition) != 1
        ):
            errors.append(
                "v27.37b-additive Vertragsmutation hat kein exaktes Ziel: "
                + label
            )
            return
        if _v2737b_bootstrap_section_is_valid(mutated):
            errors.append(
                "v27.37b-additive Vertragsmutation nicht blockiert: " + label
            )
            return
        document_mutations += 1
    future_sha_anchor = "Keine echten Teilnehmerdaten."
    future_sha_addition = "\nZukünftige SHA: `" + ("a" * 40) + "`"
    future_sha_section = _v2737b_insert_after_exact_once(
        canonical_section, future_sha_anchor, future_sha_addition
    )
    if (
        future_sha_section is None
        or future_sha_section.count(future_sha_anchor) != 1
        or future_sha_section.count(future_sha_addition) != 1
        or _v2737b_bootstrap_section_is_valid(future_sha_section)
    ):
        errors.append("v27.37b-zukünftige-SHA-Mutation nicht blockiert")
        return
    document_mutations += 1
    for path, section in repair_document_sections.items():
        for fact in V2737B_GATE_BOOTSTRAP_REPAIR_REQUIRED_MARKERS:
            mutated = _v2737b_replace_exact_once(section, fact, "")
            if mutated is None or fact in mutated:
                errors.append(
                    "v27.37b-Repair-Dokumentmutation hat kein exaktes Ziel: "
                    + path
                    + " / "
                    + fact
                )
                return
            if _v2737b_gate_bootstrap_repair_section_is_valid(mutated):
                errors.append(
                    "v27.37b-Repair-Dokumentmutation nicht blockiert: "
                    + path
                    + " / "
                    + fact
                )
                return
            document_mutations += 1
    repair_section = repair_document_sections["docs/PROJECT_STATE_CURRENT.md"]
    repair_file_list_start = "Der einmalige atomare Repair umfasst exakt:"
    repair_file_list_end = "Keine siebte Datei und keine Produktdatei sind zulässig."
    for path in V2737B_BOOTSTRAP_FILE_ORDER:
        mutated = _v2737b_replace_in_delimited_block(
            repair_section,
            repair_file_list_start,
            repair_file_list_end,
            f"- `{path}`\n",
            "",
        )
        if mutated is None:
            errors.append(
                "v27.37b-Repair-Dateimanipulation hat kein exaktes Ziel: " + path
            )
            return
        if _v2737b_gate_bootstrap_repair_section_is_valid(mutated):
            errors.append(
                "v27.37b-Repair-Dateimanipulation nicht blockiert: " + path
            )
            return
        document_mutations += 1
    repair_with_product_file = _v2737b_insert_after_in_delimited_block(
        repair_section,
        repair_file_list_start,
        repair_file_list_end,
        f"- `{V2737B_BOOTSTRAP_FILE_ORDER[0]}`\n",
        "- `app.js`\n",
    )
    if (
        repair_with_product_file is None
        or _v2737b_gate_bootstrap_repair_section_is_valid(
            repair_with_product_file
        )
    ):
        errors.append("v27.37b-Repair-Produktdateimanipulation nicht blockiert")
        return
    document_mutations += 1
    repair_with_future_sha = _v2737b_insert_after_exact_once(
        repair_section,
        "Keine echten Teilnehmerdaten.",
        "\nZukünftige Repair-SHA: `" + ("b" * 40) + "`",
    )
    if (
        repair_with_future_sha is None
        or _v2737b_gate_bootstrap_repair_section_is_valid(
            repair_with_future_sha
        )
    ):
        errors.append("v27.37b-zukünftige-Repair-SHA-Mutation nicht blockiert")
        return
    document_mutations += 1
    expected_fields_by_state = (
        ("BASE_CLOSED", V2737B_BASE_TASK_FIELDS, "v2737a_closed"),
        ("AUTHORIZED", V2737B_AUTHORIZED_TASK_FIELDS, "v2737b_authorized"),
        ("CLOSED", V2737B_CLOSED_TASK_FIELDS, "v2737b_closed"),
    )
    expected_state_by_fields = {
        tuple(fields.items()): state
        for _label, fields, state in expected_fields_by_state
    }
    phase_names = (
        "v2737b_gate_bootstrap_prepared",
        "v2737b_gate_bootstrap_committed",
        "v2737b_gate_bootstrap_repair_prepared",
        "v2737b_gate_bootstrap_repair_committed",
        "v2737b_authorization_prepared",
        "v2737b_authorization_committed",
        "v2737b_implementation_prepared",
        "v2737b_implementation_committed",
        "v2737b_closure_prepared",
        "v2737b_closure_committed",
    )
    for phase in phase_names:
        phase_fields = _v2737b_expected_current_task_fields_for_phase(phase)
        phase_task = _build_v2737b_synthetic_current_task(phase_fields)
        expected_state = expected_state_by_fields[tuple(phase_fields.items())]
        if _v2737b_task_kind_from_text(phase_task) != expected_state:
            errors.append(
                "v27.37b-Phase nutzt nicht den kanonischen CURRENT_TASK-Vertrag: "
                + phase
            )
            return
    if _v2737b_expected_current_task_fields_for_phase("unknown_future_task") is not None:
        errors.append("Unbekannte v27.37b-Phase erhielt einen CURRENT_TASK-Vertrag")
        return
    document_mutations += 1
    invalid_field_values = {
        "Task-ID": "unknown_future_task",
        "Status": "INVALID_STATUS",
        "Autorisiert": "UNBEKANNT",
        "Titel": "Manipulierter Titel",
        "Funktionaler Ausgangsstand": "v0.0",
        "Letzter abgeschlossener Kontrollschritt": "manipuliert",
        "Erlaubte Implementierungsdateien": "`app.js`",
        "Commit erlaubt": "JA",
        "Push erlaubt": "JA",
    }
    for baseline_label, fields, expected_state in expected_fields_by_state:
        baseline_task = _build_v2737b_synthetic_current_task(dict(fields))
        if _v2737b_task_kind_from_text(baseline_task) != expected_state:
            errors.append(
                "v27.37b-CURRENT_TASK-Positivvertrag fehlt: " + baseline_label
            )
            return
        for field, replacement_value in invalid_field_values.items():
            mutated = _v2737b_replace_in_current_task_header(
                baseline_task,
                f"{field}: {fields[field]}",
                f"{field}: {replacement_value}",
            )
            if mutated is None or _v2737b_task_kind_from_text(mutated) != "invalid":
                errors.append(
                    "v27.37b-CURRENT_TASK-Feldmanipulation nicht blockiert: "
                    + baseline_label
                    + " / "
                    + field
                )
                return
            document_mutations += 1
        missing_field = _v2737b_replace_in_current_task_header(
            baseline_task,
            f"Commit erlaubt: {fields['Commit erlaubt']}\n",
            "",
        )
        duplicate_field = _v2737b_duplicate_exact_once(
            baseline_task,
            f"Push erlaubt: {fields['Push erlaubt']}",
        )
        unknown_field = _v2737b_insert_after_exact_once(
            baseline_task,
            f"Push erlaubt: {fields['Push erlaubt']}",
            "\nUnbekanntes Steuerfeld: verboten",
        )
        missing_main_header = _v2737b_replace_exact_once(
            baseline_task,
            "# Verbindlicher aktueller Task",
            "# Manipulierter aktueller Task",
        )
        duplicate_main_header = _v2737b_duplicate_exact_once(
            baseline_task,
            "# Verbindlicher aktueller Task",
        )
        missing_first_section = _v2737b_replace_exact_once(
            baseline_task,
            "## Synthetischer Folgeabschnitt",
            "Synthetischer Folgeabschnitt",
        )
        for label, mutated in (
            ("fehlendes Kopffeld", missing_field),
            ("doppeltes Kopffeld", duplicate_field),
            ("unbekanntes Kopffeld", unknown_field),
            ("fehlender Hauptheader", missing_main_header),
            ("doppelter Hauptheader", duplicate_main_header),
            ("fehlender erster Abschnitt", missing_first_section),
        ):
            if mutated is None or _v2737b_task_kind_from_text(mutated) != "invalid":
                errors.append(
                    "v27.37b-CURRENT_TASK-Strukturmanipulation nicht blockiert: "
                    + baseline_label
                    + " / "
                    + label
                )
                return
            document_mutations += 1
        historical_fields = next(
            other_fields
            for other_label, other_fields, _other_state in expected_fields_by_state
            if other_label != baseline_label
        )
        historical_block = (
            "\n## Historischer v27.37b-Beleg\n\n"
            + "\n".join(
                f"{field}: {value}" for field, value in historical_fields.items()
            )
            + "\n"
        )
        if _v2737b_task_kind_from_text(
            baseline_task + historical_block
        ) != expected_state:
            errors.append(
                "Historische Felder beschädigen den gültigen CURRENT_TASK-Kopf: "
                + baseline_label
            )
            return
        document_mutations += 1
        invalid_current = _v2737b_replace_in_current_task_header(
            baseline_task,
            f"Status: {fields['Status']}",
            "Status: INVALID_STATUS",
        )
        if (
            invalid_current is None
            or _v2737b_task_kind_from_text(invalid_current + historical_block)
            != "invalid"
        ):
            errors.append(
                "Historische Felder retten einen ungültigen CURRENT_TASK-Kopf: "
                + baseline_label
            )
            return
        document_mutations += 1
    baseline = _v2737b_product_texts_at(V2737B_GATE_BOOTSTRAP_BASE_SHA)
    candidate = dict(baseline) if isinstance(baseline, dict) else None
    if not _v2737b_frozen_product_contract_is_valid(baseline, candidate):
        errors.append("v27.37b-Nachfolgeprofil erkennt Frozen-Produkte nicht")
        return
    product_mutations = 0
    for path in V2737B_FROZEN_PRODUCT_FILES:
        mutated = dict(baseline)
        mutated[path] = baseline[path] + "\n/* v2737b mutation */\n"
        if _v2737b_frozen_product_contract_is_valid(baseline, mutated):
            errors.append(
                "v27.37b-Nachfolgeprofil-Produktmanipulation nicht blockiert: "
                + path
            )
            return
        product_mutations += 1
    print(
        "v27.37b-Nachfolgeprofil-Selbstprüfung: "
        f"{len(positive_cases)} Positiv-, {len(negative_cases)} Scope- und "
        f"{document_mutations} Vertrags-/Dokument- sowie "
        f"{product_mutations} Produktmanipulationsfälle PASS"
    )


def check_v2736f_regression_profile_scope_logic():
    expected = set(V2736F_AUTHORIZED_IMPLEMENTATION_FILES)
    extra = expected | {"style.css"}
    missing = expected - {"tools/preflight.py"}
    cases = (
        ("implementation_prepared", True, expected, None, True, True, True, True),
        ("implementation_committed", True, set(), expected, True, True, True, True),
        ("implementation_committed", True, set(), extra, True, True, True, False),
        ("implementation_committed", True, set(), missing, True, True, True, False),
        ("implementation_committed", True, set(), expected, False, True, True, False),
        ("implementation_committed", True, {"tools/preflight.py"}, expected, True, True, True, False),
        ("implementation_committed", False, set(), expected, True, True, True, False),
        ("implementation_committed", True, set(), expected, True, False, True, False),
        ("implementation_committed", True, set(), expected, True, True, False, False),
    )
    for (
        phase,
        task_authorized,
        working_paths,
        committed_paths,
        boundary_matches,
        frozen_modules_unchanged,
        profile_available,
        expected_result,
    ) in cases:
        actual = _v2736f_regression_scope_facts_are_valid(
            phase=phase,
            task_authorized=task_authorized,
            working_paths=working_paths,
            committed_paths=committed_paths,
            boundary_matches=boundary_matches,
            frozen_modules_unchanged=frozen_modules_unchanged,
            profile_available=profile_available,
        )
        if actual != expected_result:
            errors.append(
                "v27.36f-Regressionsprofil-Scope-Selbstprüfung "
                f"fehlgeschlagen: {phase}"
            )
            return

    empty_history = {
        "valid": True,
        "last_role": None,
        "repair_gate_seen": False,
        "repair_implementation_seen": False,
        "repair_implementation_parent_is_authorization": False,
        "repair_closure_seen": False,
        "original_closure_seen": False,
    }
    repair_authorized_history = {
        **empty_history,
        "last_role": "repair_gate",
        "repair_gate_seen": True,
    }
    repair_implemented_history = {
        **repair_authorized_history,
        "last_role": "repair_implementation",
        "repair_implementation_seen": True,
        "repair_implementation_parent_is_authorization": True,
    }
    repair_closed_history = {
        **repair_implemented_history,
        "last_role": "repair_closure",
        "repair_closure_seen": True,
    }
    original_closed_history = {
        **repair_closed_history,
        "last_role": "original_closure",
        "original_closure_seen": True,
    }
    post_cases = (
        ("repair_authorization_committed", "repair_authorized", set(), repair_authorized_history, None, True),
        ("repair_implementation_prepared", "repair_authorized", V2736F_REPAIR_IMPLEMENTATION_FILES, repair_authorized_history, None, True),
        ("repair_implementation_committed", "repair_authorized", set(), repair_implemented_history, None, True),
        ("repair_closure_prepared", "closed", V2736F_GATE_FILES, repair_implemented_history, "repair", True),
        ("repair_closure_committed", "closed", set(), repair_closed_history, "repair", True),
        ("closure_prepared", "closed", V2736F_GATE_FILES, repair_closed_history, "original", True),
        ("closure_committed", "closed", set(), original_closed_history, "original", True),
        ("closure_prepared", "closed", V2736F_GATE_FILES | {"style.css"}, repair_closed_history, "original", False),
        ("closure_prepared", "closed", V2736F_GATE_FILES - {"tools/check-project-continuity-control.py"}, repair_closed_history, "original", False),
        ("closure_prepared", "invalid", V2736F_GATE_FILES, repair_closed_history, "original", False),
        ("closure_prepared", "repair_authorized", V2736F_GATE_FILES, repair_closed_history, "original", False),
        ("repair_implementation_prepared", "repair_authorized", V2736F_REPAIR_IMPLEMENTATION_FILES | {"app.js"}, repair_authorized_history, None, False),
        ("repair_implementation_committed", "repair_authorized", set(), {**repair_implemented_history, "repair_implementation_parent_is_authorization": False}, None, False),
        ("repair_closure_prepared", "closed", V2736F_GATE_FILES - {"docs/PROJECT_STATE_CURRENT.md"}, repair_implemented_history, "repair", False),
        ("closure_prepared", "closed", V2736F_GATE_FILES, repair_closed_history, "original", False, False, True),
        ("closure_prepared", "closed", V2736F_GATE_FILES, repair_closed_history, "original", False, True, False),
        ("closure_prepared", "closed", V2736F_GATE_FILES, {**repair_closed_history, "valid": False}, "original", False),
    )
    for case in post_cases:
        phase, task_kind, working_paths, history, closure_kind, expected_result, *overrides = case
        frozen_files_unchanged = overrides[0] if len(overrides) >= 1 else True
        profile_available = overrides[1] if len(overrides) >= 2 else True
        actual = _v2736f_post_implementation_scope_facts_are_valid(
            phase=phase,
            task_kind=task_kind,
            working_paths=working_paths,
            history=history,
            closure_kind=closure_kind,
            implementation_is_ancestor=True,
            frozen_files_unchanged=frozen_files_unchanged,
            profile_available=profile_available,
        )
        if actual != expected_result:
            errors.append(
                "v27.36f-Post-Implementation-Scope-Selbstprüfung "
                f"fehlgeschlagen: {phase}"
            )
            return

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
    changed_paths = set()
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
        changed_paths.add(path_part)

        for protected in PROTECTED_CORE_FILES_V2356:
            if path_part == protected:
                changed_protected.add(protected)

    authorized_v2736d_app_scope = _is_authorized_v2736d_app_scope(
        changed_paths
    )
    authorized_v2736f_browser_loader_scope = (
        _is_authorized_v2736f_browser_loader_scope(changed_paths)
    )

    for protected in sorted(changed_protected):
        if protected in allowed_protected:
            continue
        if protected == "app.js" and authorized_v2736d_app_scope:
            continue
        if (
            protected in {"app.js", "index.html"}
            and authorized_v2736f_browser_loader_scope
        ):
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
        "docs/contracts/exam-history-disposable-database-environment-gate-contract.json",
        "tools/accaoui_disposable_environment_gate.py",
        "tools/accaoui_disposable_connection_adapter_readiness.py",
        "docs/contracts/exam-history-disposable-database-gate-evaluator-adapter-readiness-contract.json",
        "docs/contracts/exam-history-disposable-database-harness-gate-integration-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-driver-selection-contract.json",
        "tools/accaoui_disposable_postgresql_driver_readiness.py",
        "docs/contracts/exam-history-disposable-postgresql-driver-readiness-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-test-dependency-manifest-contract.json",
        "tools/test-dependencies/disposable-postgresql-requirements.txt",
        "docs/contracts/exam-history-disposable-postgresql-test-dependency-manifest-materialization-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-readiness-contract.json",
        "tools/accaoui_disposable_test_python_environment_descriptor.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-descriptor-resolver-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_plan.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-plan-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_plan_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-plan-acceptance-guard-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-request-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_request_state.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-request-state-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_request_transition_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-request-transition-guard-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-consumption-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_consumption_readiness.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-consumption-readiness-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_consumption_readiness_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-consumption-readiness-acceptance-guard-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-operation-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_plan.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-plan-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_plan_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-plan-acceptance-guard-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-contract.py",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_descriptor.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-descriptor-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_descriptor_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-descriptor-acceptance-guard-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_readiness.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-readiness-contract.json",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_readiness_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-readiness-acceptance-guard-contract.json",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-contract.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_EXECUTION_CONTRACT.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_descriptor.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-descriptor-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-descriptor.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_EXECUTION_DESCRIPTOR.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_descriptor_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-descriptor-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-descriptor-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_EXECUTION_DESCRIPTOR_ACCEPTANCE_GUARD.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_readiness.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-readiness-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-readiness.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_EXECUTION_READINESS.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_readiness_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-readiness-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-readiness-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_EXECUTION_READINESS_ACCEPTANCE_GUARD.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_plan.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-plan-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-plan.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_EXECUTION_PLAN.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_plan_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-plan-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-execution-plan-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_EXECUTION_PLAN_ACCEPTANCE_GUARD.md",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-contract.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_CONTRACT.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_descriptor.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-descriptor-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-descriptor.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_DESCRIPTOR.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_descriptor_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-descriptor-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-descriptor-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_DESCRIPTOR_ACCEPTANCE_GUARD.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_readiness.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-readiness-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-readiness.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_READINESS.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_readiness_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-readiness-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-readiness-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_READINESS_ACCEPTANCE_GUARD.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_plan.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-plan-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-plan.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_PLAN.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_plan_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-plan-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-plan-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_PLAN_ACCEPTANCE_GUARD.md",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-contract.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_CONTRACT.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_descriptor.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-descriptor-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-descriptor.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_DESCRIPTOR.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_descriptor_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-descriptor-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-descriptor-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_DESCRIPTOR_ACCEPTANCE_GUARD.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_readiness.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-readiness-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-readiness.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_READINESS.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_readiness_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-readiness-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-readiness-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_READINESS_ACCEPTANCE_GUARD.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_plan.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-plan-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-plan.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_PLAN.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_plan_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-plan-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-plan-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_PLAN_ACCEPTANCE_GUARD.md",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-contract.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_AUTHORIZATION_CONTRACT.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_descriptor.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-descriptor-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-descriptor.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_AUTHORIZATION_DESCRIPTOR.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_descriptor_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-descriptor-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-descriptor-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_AUTHORIZATION_DESCRIPTOR_ACCEPTANCE_GUARD.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-readiness-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-readiness.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_AUTHORIZATION_READINESS.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness_acceptance_guard.py",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-readiness-acceptance-guard-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-implementation-execution-authorization-readiness-acceptance-guard.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_IMPLEMENTATION_EXECUTION_AUTHORIZATION_READINESS_ACCEPTANCE_GUARD.md",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver-interface-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver-interface-contract.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER_INTERFACE_CONTRACT.md",
        "tools/accaoui_disposable_test_python_environment_materialization_authorization_atomic_consumption_registry_local_fake_driver.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER.md",
        "docs/contracts/exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver-adapter-contract.json",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-local-fake-driver-adapter-contract.py",
        "docs/SUPABASE_EXAM_RESULT_HISTORY_DISPOSABLE_POSTGRESQL_TEST_PYTHON_ENVIRONMENT_MATERIALIZATION_AUTHORIZATION_ATOMIC_CONSUMPTION_REGISTRY_ADAPTER_LOCAL_FAKE_DRIVER_ADAPTER_CONTRACT.md",
        "data/supabase-participant-access-adapter.js",
        "data/supabase-participant-access-bootstrap-bridge.js",
        "data/supabase-participant-access-browser-provider.js",
        "data/supabase-participant-auth-session-adapter.js",
        "tools/check-supabase-participant-access-adapter.py",
        "tools/check-supabase-participant-access-bootstrap-bridge.py",
        "tools/check-supabase-participant-auth-session-adapter.py",
        "docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md",
        "docs/SUPABASE_PARTICIPANT_AUTH_SESSION_ADAPTER_V2737A.md",
        "tools/check-participant-access-app-entry-v2736d.py",
        "docs/PARTICIPANT_ACCESS_APP_ENTRY_V2736D.md",
        "tools/check-participant-access-browser-provider-v2736e.py",
        "docs/PARTICIPANT_ACCESS_BROWSER_PROVIDER_V2736E.md",
        "data/supabase-participant-access-browser-loader.js",
        "tools/check-participant-access-browser-loader-v2736f.py",
        "docs/PARTICIPANT_ACCESS_BROWSER_LOADER_V2736F.md",
        "docs/PROJECT_STATE_CURRENT.md",
        "docs/tasks/CURRENT_TASK.md",
        "tools/check-project-continuity-control.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-readiness-acceptance-guard.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-readiness.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-descriptor-acceptance-guard.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-registry-adapter-descriptor.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-plan-acceptance-guard.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-plan.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-atomic-consumption-operation-contract.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-consumption-readiness-acceptance-guard.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-consumption-readiness.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-consumption-contract.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-request-transition-guard.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-request-state.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-authorization-request-contract.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-plan-acceptance-guard.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-plan.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-materialization-contract.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-descriptor-resolver.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-python-environment-readiness-contract.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-dependency-manifest-materialization.py",
        "tools/check-supabase-exam-history-disposable-postgresql-test-dependency-manifest-contract.py",
        "tools/check-supabase-exam-history-disposable-postgresql-driver-readiness.py",
        "tools/check-supabase-exam-history-disposable-postgresql-driver-selection-contract.py",
        "tools/check-supabase-exam-history-disposable-database-harness-gate-integration.py",
        "tools/check-supabase-exam-history-disposable-database-gate-evaluator-adapter-readiness.py",
        "tools/check-supabase-exam-history-disposable-database-environment-gate-contract.py",
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
    check_exam_result_history_disposable_database_environment_gate_contract()
    check_exam_result_history_disposable_database_gate_evaluator_adapter_readiness()
    check_exam_result_history_disposable_database_harness_gate_integration()
    check_exam_result_history_disposable_postgresql_driver_selection_contract()
    check_exam_result_history_disposable_postgresql_driver_readiness()
    check_exam_result_history_disposable_postgresql_test_dependency_manifest_contract()
    check_exam_result_history_disposable_postgresql_test_dependency_manifest_materialization()
    check_exam_result_history_disposable_postgresql_test_python_environment_readiness_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_descriptor_resolver()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_plan()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_plan_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_request_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_request_state()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_request_transition_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_consumption_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_consumption_readiness()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_consumption_readiness_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_operation_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_plan()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_plan_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_descriptor()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_descriptor_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_readiness()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_readiness_acceptance_guard()
    check_exam_result_history_domain_payload_contract()
    check_exam_result_history_domain_storage_contract()
    check_exam_result_history_expected_storage_version_binding()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_descriptor()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_descriptor_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_readiness()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_readiness_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_plan()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_execution_plan_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_descriptor()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_descriptor_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_readiness()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_readiness_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_plan()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_plan_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_descriptor()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_descriptor_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_readiness()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_readiness_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_plan()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_plan_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_descriptor()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_descriptor_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_implementation_execution_authorization_readiness_acceptance_guard()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_local_fake_driver_interface_contract()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_local_fake_driver()
    check_exam_result_history_disposable_postgresql_test_python_environment_materialization_authorization_atomic_consumption_registry_adapter_local_fake_driver_adapter_contract()
    check_supabase_participant_access_adapter()
    check_supabase_participant_access_bootstrap_bridge()
    check_supabase_participant_auth_session_adapter_v2737a()
    check_participant_access_app_entry_v2736d()
    check_v2736f_regression_profile_scope_logic()
    check_v2737a_successor_profile_scope_logic()
    check_v2737b_successor_profile_scope_logic()
    check_participant_access_browser_provider_v2736e()
    check_participant_access_browser_loader_v2736f()
    check_project_continuity_control()
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
