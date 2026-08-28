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
        "tools/check-supabase-participant-access-adapter.py",
        "tools/check-supabase-participant-access-bootstrap-bridge.py",
        "docs/SUPABASE_PARTICIPANT_ACCESS_ADAPTER_V2736B.md",
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
    check_participant_access_app_entry_v2736d()
    check_v2736f_regression_profile_scope_logic()
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
