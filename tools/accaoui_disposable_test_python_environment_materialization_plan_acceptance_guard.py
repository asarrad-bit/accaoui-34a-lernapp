from __future__ import annotations

from collections.abc import Mapping
from pathlib import PurePosixPath, PureWindowsPath

TOP_LEVEL_KEYS = frozenset({
    "status",
    "reason",
    "plan",
    "filesystemReadAllowed",
    "filesystemMutationAllowed",
    "processExecutionAllowed",
    "dependencyInstallationAllowed",
})

PLAN_KEYS = frozenset({
    "platform",
    "pythonVersion",
    "basePythonExecutable",
    "environmentRoot",
    "repositoryRoot",
    "targetState",
    "creation",
    "interpreter",
    "manifest",
    "evidence",
    "rollback",
    "authorization",
})

CREATION_KEYS = frozenset({
    "argv",
    "shell",
    "workingDirectory",
    "timeoutSeconds",
    "environmentOverrides",
    "environmentRemovals",
    "includeSystemSitePackages",
    "upgradeExistingEnvironment",
    "clearExistingEnvironment",
    "withPipExpected",
})

INTERPRETER_KEYS = frozenset({
    "relativePath",
    "executionAllowed",
})

MANIFEST_KEYS = frozenset({
    "path",
    "requirement",
    "installationAllowed",
})

EVIDENCE_KEYS = frozenset({
    "collectionAllowed",
    "requiredChecks",
})

ROLLBACK_KEYS = frozenset({
    "executionAllowed",
    "requiredOnCreationFailure",
    "requiredOnEvidenceFailure",
    "deleteOnlyExactTarget",
    "deleteParentAllowed",
    "deleteRepositoryAllowed",
    "deletePreexistingTargetAllowed",
    "creationOwnershipProofRequired",
})

AUTHORIZATION_KEYS = frozenset({
    "requiredLater",
    "recorded",
})

SUPPORTED_VERSIONS = frozenset({
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
})

REQUIRED_EVIDENCE_CHECKS = [
    "interpreter_exists",
    "pyvenv_config_exists",
    "include_system_site_packages_false",
    "sys_prefix_differs_from_base_prefix",
    "python_major_minor_matches_descriptor",
    "python_no_user_site_true",
    "system_site_packages_excluded",
    "user_site_packages_excluded",
    "dependency_uninstalled",
]


def _result(
    status: str,
    reason: str,
    accepted: bool,
    accepted_plan: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "accepted": accepted,
        "acceptedPlan": accepted_plan,
        "environmentCreationAllowed": False,
        "filesystemReadAllowed": False,
        "filesystemMutationAllowed": False,
        "processExecutionAllowed": False,
        "dependencyInstallationAllowed": False,
        "evidenceCollectionAllowed": False,
        "rollbackExecutionAllowed": False,
        "authorizationGrantAccepted": False,
    }


def _blocked(reason: str) -> dict[str, object]:
    return _result("blocked", reason, False)


def _path_details(
    platform_name: str,
    raw_path: object,
) -> tuple[object, tuple[str, ...], str] | None:
    if not isinstance(raw_path, str):
        return None

    raw_path = raw_path.strip()
    if not raw_path:
        return None

    if platform_name == "windows":
        path = PureWindowsPath(raw_path)

        if not path.is_absolute():
            return None

        if str(path).startswith("\\\\"):
            return None

        return (
            path,
            tuple(part.casefold() for part in path.parts),
            str(path),
        )

    if platform_name == "posix":
        path = PurePosixPath(raw_path)

        if not path.is_absolute():
            return None

        if str(path).startswith("//"):
            return None

        return path, tuple(path.parts), str(path)

    return None


def _is_same_or_child(
    child_parts: tuple[str, ...],
    parent_parts: tuple[str, ...],
) -> bool:
    if len(child_parts) < len(parent_parts):
        return False

    return child_parts[:len(parent_parts)] == parent_parts


def accept_test_python_environment_materialization_plan(
    candidate: object,
) -> dict[str, object]:
    if not isinstance(candidate, Mapping):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_invalid_input"
        )

    candidate_data = dict(candidate)

    if set(candidate_data) != TOP_LEVEL_KEYS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_structure_invalid"
        )

    if candidate_data["status"] != "plan_ready_execution_locked":
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_source_status_invalid"
        )

    if candidate_data["reason"] != (
        "test_environment_materialization_plan_"
        "ready_execution_locked"
    ):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_source_reason_invalid"
        )

    for field in (
        "filesystemReadAllowed",
        "filesystemMutationAllowed",
        "processExecutionAllowed",
        "dependencyInstallationAllowed",
    ):
        if candidate_data[field] is not False:
            return _blocked(
                "test_environment_materialization_plan_"
                "acceptance_execution_boundary_open"
            )

    plan = candidate_data["plan"]
    if not isinstance(plan, Mapping):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_plan_invalid"
        )

    plan_data = dict(plan)
    if set(plan_data) != PLAN_KEYS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_plan_structure_invalid"
        )

    platform_name = plan_data["platform"]
    if platform_name not in {"windows", "posix"}:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_platform_invalid"
        )

    python_version = plan_data["pythonVersion"]
    if python_version not in SUPPORTED_VERSIONS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_python_invalid"
        )

    environment_details = _path_details(
        platform_name,
        plan_data["environmentRoot"],
    )
    repository_details = _path_details(
        platform_name,
        plan_data["repositoryRoot"],
    )
    base_python_details = _path_details(
        platform_name,
        plan_data["basePythonExecutable"],
    )

    if environment_details is None:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_target_invalid"
        )

    if repository_details is None:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_repository_invalid"
        )

    if base_python_details is None:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_base_python_invalid"
        )

    environment_path, environment_parts, environment_root = (
        environment_details
    )
    _, repository_parts, repository_root = repository_details
    base_python_path, base_python_parts, base_python = (
        base_python_details
    )

    if ".." in environment_path.parts:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_target_invalid"
        )

    if ".." in base_python_path.parts:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_base_python_invalid"
        )

    if _is_same_or_child(environment_parts, repository_parts):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_target_forbidden"
        )

    if _is_same_or_child(base_python_parts, environment_parts):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_base_python_invalid"
        )

    target_state = plan_data["targetState"]
    if target_state not in {"absent", "empty"}:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_target_state_invalid"
        )

    creation = plan_data["creation"]
    if not isinstance(creation, Mapping):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_creation_invalid"
        )

    creation_data = dict(creation)
    if set(creation_data) != CREATION_KEYS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_creation_structure_invalid"
        )

    expected_argv = [
        base_python,
        "-I",
        "-m",
        "venv",
        environment_root,
    ]

    if creation_data["argv"] != expected_argv:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_argv_invalid"
        )

    expected_creation = {
        "shell": False,
        "workingDirectory": None,
        "timeoutSeconds": 60,
        "environmentOverrides": {
            "PYTHONNOUSERSITE": "1",
        },
        "environmentRemovals": [
            "PYTHONPATH",
            "VIRTUAL_ENV",
        ],
        "includeSystemSitePackages": False,
        "upgradeExistingEnvironment": False,
        "clearExistingEnvironment": False,
        "withPipExpected": True,
    }

    for key, expected_value in expected_creation.items():
        if creation_data[key] != expected_value:
            return _blocked(
                "test_environment_materialization_plan_"
                "acceptance_creation_boundary_invalid"
            )

    interpreter = plan_data["interpreter"]
    if not isinstance(interpreter, Mapping):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_interpreter_invalid"
        )

    interpreter_data = dict(interpreter)
    if set(interpreter_data) != INTERPRETER_KEYS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_interpreter_invalid"
        )

    expected_interpreter = (
        "Scripts/python.exe"
        if platform_name == "windows"
        else "bin/python"
    )

    if interpreter_data != {
        "relativePath": expected_interpreter,
        "executionAllowed": False,
    }:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_interpreter_invalid"
        )

    manifest = plan_data["manifest"]
    if not isinstance(manifest, Mapping):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_manifest_invalid"
        )

    manifest_data = dict(manifest)
    if set(manifest_data) != MANIFEST_KEYS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_manifest_invalid"
        )

    if manifest_data != {
        "path": (
            "tools/test-dependencies/"
            "disposable-postgresql-requirements.txt"
        ),
        "requirement": "psycopg[binary]==3.3.4",
        "installationAllowed": False,
    }:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_manifest_invalid"
        )

    evidence = plan_data["evidence"]
    if not isinstance(evidence, Mapping):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_evidence_invalid"
        )

    evidence_data = dict(evidence)
    if set(evidence_data) != EVIDENCE_KEYS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_evidence_invalid"
        )

    if evidence_data != {
        "collectionAllowed": False,
        "requiredChecks": REQUIRED_EVIDENCE_CHECKS,
    }:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_evidence_invalid"
        )

    rollback = plan_data["rollback"]
    if not isinstance(rollback, Mapping):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_rollback_invalid"
        )

    rollback_data = dict(rollback)
    if set(rollback_data) != ROLLBACK_KEYS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_rollback_invalid"
        )

    if rollback_data != {
        "executionAllowed": False,
        "requiredOnCreationFailure": True,
        "requiredOnEvidenceFailure": True,
        "deleteOnlyExactTarget": environment_root,
        "deleteParentAllowed": False,
        "deleteRepositoryAllowed": False,
        "deletePreexistingTargetAllowed": False,
        "creationOwnershipProofRequired": True,
    }:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_rollback_invalid"
        )

    authorization = plan_data["authorization"]
    if not isinstance(authorization, Mapping):
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_authorization_invalid"
        )

    authorization_data = dict(authorization)
    if set(authorization_data) != AUTHORIZATION_KEYS:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_authorization_invalid"
        )

    if authorization_data != {
        "requiredLater": True,
        "recorded": False,
    }:
        return _blocked(
            "test_environment_materialization_plan_"
            "acceptance_authorization_invalid"
        )

    canonical_plan = {
        "platform": platform_name,
        "pythonVersion": python_version,
        "basePythonExecutable": base_python,
        "environmentRoot": environment_root,
        "repositoryRoot": repository_root,
        "targetState": target_state,
        "creation": {
            "argv": list(expected_argv),
            **expected_creation,
        },
        "interpreter": dict(interpreter_data),
        "manifest": dict(manifest_data),
        "evidence": {
            "collectionAllowed": False,
            "requiredChecks": list(REQUIRED_EVIDENCE_CHECKS),
        },
        "rollback": dict(rollback_data),
        "authorization": dict(authorization_data),
    }

    return _result(
        "accepted_execution_locked",
        "test_environment_materialization_plan_"
        "accepted_execution_locked",
        True,
        canonical_plan,
    )
