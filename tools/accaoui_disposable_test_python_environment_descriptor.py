from __future__ import annotations

from collections.abc import Mapping
from pathlib import PurePosixPath, PureWindowsPath

ALLOWED_KEYS = frozenset({
    "platform",
    "environmentRoot",
    "repositoryRoot",
    "environmentRootKind",
    "invokingPythonVersion",
    "requestedPythonVersion",
    "includeSystemSitePackages",
    "allowUserSitePackages",
    "pythonNoUserSite",
    "inheritPythonPath",
    "inheritVirtualEnv",
})

REQUIRED_KEYS = ALLOWED_KEYS
SUPPORTED_VERSIONS = frozenset({
    "3.10",
    "3.11",
    "3.12",
    "3.13",
    "3.14",
})


def _result(
    status: str,
    reason: str,
    descriptor: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "descriptor": descriptor,
        "environmentCreationAllowed": False,
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

        parts = tuple(path.parts)
        return path, parts, str(path)

    return None


def _is_same_or_child(
    child_parts: tuple[str, ...],
    parent_parts: tuple[str, ...],
) -> bool:
    if len(child_parts) < len(parent_parts):
        return False

    return child_parts[:len(parent_parts)] == parent_parts


def resolve_test_python_environment_descriptor(
    facts: object,
) -> dict[str, object]:
    if not isinstance(facts, Mapping):
        return _blocked(
            "test_environment_descriptor_invalid_input"
        )

    input_data = dict(facts)
    input_keys = set(input_data)

    if input_keys - ALLOWED_KEYS:
        return _blocked(
            "test_environment_descriptor_unknown_fields"
        )

    if REQUIRED_KEYS - input_keys:
        return _blocked(
            "test_environment_descriptor_missing_fields"
        )

    platform_name = input_data["platform"]
    if platform_name not in {"windows", "posix"}:
        return _blocked(
            "test_environment_platform_invalid"
        )

    environment_root = input_data["environmentRoot"]
    repository_root = input_data["repositoryRoot"]

    if not isinstance(environment_root, str):
        return _blocked(
            "test_environment_root_not_configured"
        )

    environment_root = environment_root.strip()
    if not environment_root:
        return _blocked(
            "test_environment_root_not_configured"
        )

    if not isinstance(repository_root, str):
        return _blocked(
            "test_environment_repository_root_invalid"
        )

    repository_root = repository_root.strip()
    if not repository_root:
        return _blocked(
            "test_environment_repository_root_invalid"
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
            "test_environment_root_not_absolute"
        )

    if repository_details is None:
        return _blocked(
            "test_environment_repository_root_invalid"
        )

    environment_path, environment_parts, normalized_environment = (
        environment_details
    )
    _, repository_parts, normalized_repository = repository_details

    if ".." in environment_path.parts:
        return _blocked(
            "test_environment_root_traversal_forbidden"
        )

    if _is_same_or_child(
        environment_parts,
        repository_parts,
    ):
        return _blocked(
            "test_environment_inside_repository_forbidden"
        )

    if input_data["environmentRootKind"] != "dedicated_external":
        return _blocked(
            "test_environment_system_location_forbidden"
        )

    invoking_version = input_data["invokingPythonVersion"]
    requested_version = input_data["requestedPythonVersion"]

    if invoking_version not in SUPPORTED_VERSIONS:
        return _blocked(
            "test_environment_python_version_unsupported"
        )

    if requested_version not in SUPPORTED_VERSIONS:
        return _blocked(
            "test_environment_python_version_unsupported"
        )

    if requested_version != invoking_version:
        return _blocked(
            "test_environment_python_version_mismatch"
        )

    boolean_fields = (
        "includeSystemSitePackages",
        "allowUserSitePackages",
        "pythonNoUserSite",
        "inheritPythonPath",
        "inheritVirtualEnv",
    )

    if any(
        not isinstance(input_data[field], bool)
        for field in boolean_fields
    ):
        return _blocked(
            "test_environment_isolation_facts_invalid"
        )

    if input_data["includeSystemSitePackages"]:
        return _blocked(
            "test_environment_system_site_packages_forbidden"
        )

    if input_data["allowUserSitePackages"]:
        return _blocked(
            "test_environment_user_site_packages_forbidden"
        )

    if not input_data["pythonNoUserSite"]:
        return _blocked(
            "test_environment_python_no_user_site_required"
        )

    if input_data["inheritPythonPath"]:
        return _blocked(
            "test_environment_python_path_inheritance_forbidden"
        )

    if input_data["inheritVirtualEnv"]:
        return _blocked(
            "test_environment_virtual_env_inheritance_forbidden"
        )

    interpreter_path = (
        "Scripts/python.exe"
        if platform_name == "windows"
        else "bin/python"
    )

    descriptor = {
        "platform": platform_name,
        "environmentRoot": normalized_environment,
        "repositoryRoot": normalized_repository,
        "environmentRootKind": "dedicated_external",
        "pythonVersion": requested_version,
        "interpreterRelativePath": interpreter_path,
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

    return _result(
        "descriptor_ready_creation_locked",
        "test_environment_descriptor_ready_creation_locked",
        descriptor,
    )
