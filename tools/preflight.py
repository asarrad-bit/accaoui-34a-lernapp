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

    for protected in sorted(changed_protected):
        if protected in allowed_protected:
            continue
        if protected == "app.js" and authorized_v2736d_app_scope:
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
    check_participant_access_browser_provider_v2736e()
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
