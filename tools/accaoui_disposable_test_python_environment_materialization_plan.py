from __future__ import annotations

from collections.abc import Mapping
from pathlib import PurePosixPath, PureWindowsPath

ALLOWED_KEYS = frozenset({
    "descriptorResult",
    "basePythonExecutable",
    "targetState",
    "humanAuthorizationRecorded",
})

REQUIRED_DESCRIPTOR_FIELDS = frozenset({
    "platform",
    "environmentRoot",
    "repositoryRoot",
    "environmentRootKind",
    "pythonVersion",
    "interpreterRelativePath",
    "includeSystemSitePackages",
    "allowUserSitePackages",
    "pythonNoUserSite",
    "inheritPythonPath",
    "inheritVirtualEnv",
    "manifestPath",
    "manifestRequirement",
})


def _result(
    status: str,
    reason: str,
    plan: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "plan": plan,
        "filesystemReadAllowed": False,
        "filesystemMutationAllowed": False,
        "processExecutionAllowed": False,
        "dependencyInstallationAllowed": False,
    }


def _blocked(reason: str) -> dict[str, object]:
    return _result("blocked", reason)


def _path_details(
    platform_name: str,
    raw_path: str,
) -> tuple[object, tuple[str, ...], str] | None:
    if platform_name == "windows":
        path = PureWindowsPath(raw_path)

        if not path.is_absolute():
            return None

        if str(path).startswith("\\\\"):
            return None

        parts = tuple(part.casefold() for part in path.parts)
        return path, parts, str(path)

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


def build_test_python_environment_materialization_plan(
    request: object,
) -> dict[str, object]:
    if not isinstance(request, Mapping):
        return _blocked(
            "test_environment_materialization_plan_invalid_input"
        )

    input_data = dict(request)
    input_keys = set(input_data)

    if input_keys - ALLOWED_KEYS:
        return _blocked(
            "test_environment_materialization_plan_unknown_fields"
        )

    if ALLOWED_KEYS - input_keys:
        return _blocked(
            "test_environment_materialization_plan_missing_fields"
        )

    descriptor_result = input_data["descriptorResult"]
    if not isinstance(descriptor_result, Mapping):
        return _blocked(
            "test_environment_materialization_descriptor_invalid"
        )

    descriptor_result_data = dict(descriptor_result)

    if descriptor_result_data.get("status") != (
        "descriptor_ready_creation_locked"
    ):
        return _blocked(
            "test_environment_materialization_descriptor_invalid"
        )

    if descriptor_result_data.get("reason") != (
        "test_environment_descriptor_ready_creation_locked"
    ):
        return _blocked(
            "test_environment_materialization_descriptor_invalid"
        )

    for field in (
        "environmentCreationAllowed",
        "processExecutionAllowed",
        "dependencyInstallationAllowed",
    ):
        if descriptor_result_data.get(field) is not False:
            return _blocked(
                "test_environment_materialization_descriptor_invalid"
            )

    descriptor = descriptor_result_data.get("descriptor")
    if not isinstance(descriptor, Mapping):
        return _blocked(
            "test_environment_materialization_descriptor_invalid"
        )

    descriptor_data = dict(descriptor)
    if set(descriptor_data) != REQUIRED_DESCRIPTOR_FIELDS:
        return _blocked(
            "test_environment_materialization_descriptor_invalid"
        )

    platform_name = descriptor_data["platform"]
    if platform_name not in {"windows", "posix"}:
        return _blocked(
            "test_environment_materialization_platform_invalid"
        )

    environment_root = descriptor_data["environmentRoot"]
    repository_root = descriptor_data["repositoryRoot"]

    if not isinstance(environment_root, str):
        return _blocked(
            "test_environment_materialization_target_invalid"
        )

    if not isinstance(repository_root, str):
        return _blocked(
            "test_environment_materialization_repository_invalid"
        )

    environment_details = _path_details(
        platform_name,
        environment_root,
    )
    repository_details = _path_details(
        platform_name,
        repository_root,
    )

    if environment_details is None:
        return _blocked(
            "test_environment_materialization_target_invalid"
        )

    if repository_details is None:
        return _blocked(
            "test_environment_materialization_repository_invalid"
        )

    environment_path, environment_parts, normalized_environment = (
        environment_details
    )
    _, repository_parts, normalized_repository = repository_details

    if ".." in environment_path.parts:
        return _blocked(
            "test_environment_materialization_target_invalid"
        )

    if _is_same_or_child(environment_parts, repository_parts):
        return _blocked(
            "test_environment_materialization_target_forbidden"
        )

    if descriptor_data["environmentRootKind"] != "dedicated_external":
        return _blocked(
            "test_environment_materialization_target_forbidden"
        )

    expected_interpreter = (
        "Scripts/python.exe"
        if platform_name == "windows"
        else "bin/python"
    )

    if descriptor_data["interpreterRelativePath"] != expected_interpreter:
        return _blocked(
            "test_environment_materialization_descriptor_invalid"
        )

    if descriptor_data["pythonVersion"] not in {
        "3.10",
        "3.11",
        "3.12",
        "3.13",
        "3.14",
    }:
        return _blocked(
            "test_environment_materialization_python_unsupported"
        )

    expected_isolation = {
        "includeSystemSitePackages": False,
        "allowUserSitePackages": False,
        "pythonNoUserSite": True,
        "inheritPythonPath": False,
        "inheritVirtualEnv": False,
        "manifestPath": (
            "tools/test-dependencies/"
            "disposable-postgresql-requirements.txt"
        ),
        "manifestRequirement": "psycopg[binary]==3.3.4",
    }

    for key, expected_value in expected_isolation.items():
        if descriptor_data.get(key) != expected_value:
            return _blocked(
                "test_environment_materialization_descriptor_invalid"
            )

    base_python = input_data["basePythonExecutable"]
    if not isinstance(base_python, str):
        return _blocked(
            "test_environment_materialization_base_python_invalid"
        )

    base_python = base_python.strip()
    base_details = _path_details(platform_name, base_python)

    if base_details is None:
        return _blocked(
            "test_environment_materialization_base_python_invalid"
        )

    base_path, base_parts, normalized_base = base_details

    if ".." in base_path.parts:
        return _blocked(
            "test_environment_materialization_base_python_invalid"
        )

    if _is_same_or_child(base_parts, environment_parts):
        return _blocked(
            "test_environment_materialization_base_python_invalid"
        )

    target_state = input_data["targetState"]
    if target_state not in {"absent", "empty", "non_empty"}:
        return _blocked(
            "test_environment_materialization_target_state_invalid"
        )

    if target_state == "non_empty":
        return _blocked(
            "test_environment_target_not_empty"
        )

    human_authorization = input_data["humanAuthorizationRecorded"]
    if not isinstance(human_authorization, bool):
        return _blocked(
            "test_environment_materialization_authorization_invalid"
        )

    if human_authorization:
        return _blocked(
            "test_environment_materialization_authorization_"
            "not_accepted_in_plan"
        )

    creation_argv = [
        normalized_base,
        "-I",
        "-m",
        "venv",
        normalized_environment,
    ]

    plan = {
        "platform": platform_name,
        "pythonVersion": descriptor_data["pythonVersion"],
        "basePythonExecutable": normalized_base,
        "environmentRoot": normalized_environment,
        "repositoryRoot": normalized_repository,
        "targetState": target_state,
        "creation": {
            "argv": creation_argv,
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
        },
        "interpreter": {
            "relativePath": expected_interpreter,
            "executionAllowed": False,
        },
        "manifest": {
            "path": descriptor_data["manifestPath"],
            "requirement": descriptor_data["manifestRequirement"],
            "installationAllowed": False,
        },
        "evidence": {
            "collectionAllowed": False,
            "requiredChecks": [
                "interpreter_exists",
                "pyvenv_config_exists",
                "include_system_site_packages_false",
                "sys_prefix_differs_from_base_prefix",
                "python_major_minor_matches_descriptor",
                "python_no_user_site_true",
                "system_site_packages_excluded",
                "user_site_packages_excluded",
                "dependency_uninstalled",
            ],
        },
        "rollback": {
            "executionAllowed": False,
            "requiredOnCreationFailure": True,
            "requiredOnEvidenceFailure": True,
            "deleteOnlyExactTarget": normalized_environment,
            "deleteParentAllowed": False,
            "deleteRepositoryAllowed": False,
            "deletePreexistingTargetAllowed": False,
            "creationOwnershipProofRequired": True,
        },
        "authorization": {
            "requiredLater": True,
            "recorded": False,
        },
    }

    return _result(
        "plan_ready_execution_locked",
        "test_environment_materialization_plan_"
        "ready_execution_locked",
        plan,
    )
