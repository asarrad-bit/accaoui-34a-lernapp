from __future__ import annotations

from collections.abc import Mapping
from typing import Any

MODE_KEY = "ACCAOUI_DB_TEST_MODE"
TARGET_KIND_KEY = "ACCAOUI_DB_TEST_TARGET_KIND"
HOST_KEY = "ACCAOUI_DB_TEST_HOST"
PORT_KEY = "ACCAOUI_DB_TEST_PORT"
DATABASE_KEY = "ACCAOUI_DB_TEST_DATABASE"
CONFIRM_KEY = "ACCAOUI_DB_TEST_CONFIRM"

REQUIRED_KEYS = (
    MODE_KEY,
    TARGET_KIND_KEY,
    HOST_KEY,
    PORT_KEY,
    DATABASE_KEY,
    CONFIRM_KEY,
)

ALLOWED_HOSTS = {
    "127.0.0.1",
    "localhost",
    "::1",
}
ALLOWED_DATABASE = "accaoui_exam_history_disposable_test"

FORBIDDEN_DATABASE_NAMES = {
    "postgres",
    "template0",
    "template1",
    "production",
    "prod",
    "main",
    "default",
}
FORBIDDEN_HOST_SUFFIXES = ()
FORBIDDEN_HOST_TOKENS = (
    "prod",
    "production",
    "live",
    "remote",
    "cloud",
)
FORBIDDEN_DATABASE_TOKENS = (
    "prod",
    "production",
    "live",
    "customer",
    "participant",
)


def _deny(reason: str) -> dict[str, Any]:
    return {
        "decision": "deny",
        "reason": reason,
        "descriptor": None,
        "connectionAllowed": False,
    }


def _normalize_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_host(value: object) -> str:
    return _normalize_text(value).lower().rstrip(".")


def _contains_connection_string_shape(value: str) -> bool:
    lowered = value.lower()
    return any(
        marker in lowered
        for marker in (
            "://",
            "@",
            "/",
            "\\",
            "?",
            "#",
        )
    )


def _looks_remote_host(host: str) -> bool:
    if any(token in host for token in FORBIDDEN_HOST_TOKENS):
        return True

    if "." in host or ":" in host:
        return host not in ALLOWED_HOSTS

    return False


def evaluate_environment(
    values: Mapping[str, object],
) -> dict[str, Any]:
    if not isinstance(values, Mapping):
        return _deny("environment_descriptor_invalid")

    supplied_keys = {
        str(key)
        for key in values.keys()
    }
    allowed_keys = set(REQUIRED_KEYS)

    if not supplied_keys:
        return _deny("environment_gate_not_configured")

    if supplied_keys - allowed_keys:
        return _deny("unknown_environment_field")

    normalized = {
        key: _normalize_text(values.get(key))
        for key in REQUIRED_KEYS
    }

    if any(not normalized[key] for key in REQUIRED_KEYS):
        return _deny("environment_gate_incomplete")

    if normalized[MODE_KEY] != "disposable":
        return _deny("environment_mode_invalid")

    if normalized[TARGET_KIND_KEY] != "local_postgres":
        return _deny("target_kind_invalid")

    raw_host = normalized[HOST_KEY]
    raw_database = normalized[DATABASE_KEY]

    if (
        _contains_connection_string_shape(raw_host)
        or _contains_connection_string_shape(raw_database)
    ):
        return _deny("connection_string_forbidden")

    host = _normalize_host(raw_host)
    database = raw_database.lower()

    if normalized[CONFIRM_KEY] != "DESTROY_SYNTHETIC_TEST_DATA":
        return _deny("destructive_confirmation_required")

    try:
        port = int(normalized[PORT_KEY], 10)
    except (TypeError, ValueError):
        return _deny("invalid_local_port")

    if port < 1024 or port > 65535:
        return _deny("invalid_local_port")

    if (
        database in FORBIDDEN_DATABASE_NAMES
        or any(
            token in database
            for token in FORBIDDEN_DATABASE_TOKENS
        )
    ):
        return _deny("protected_database_forbidden")

    if database != ALLOWED_DATABASE:
        return _deny("unknown_target_forbidden")

    if host not in ALLOWED_HOSTS:
        if _looks_remote_host(host):
            return _deny("remote_target_forbidden")
        return _deny("unknown_target_forbidden")

    descriptor = {
        "mode": "disposable",
        "targetKind": "local_postgres",
        "host": host,
        "port": port,
        "database": ALLOWED_DATABASE,
    }

    return {
        "decision": "eligible_but_connection_locked",
        "reason": "adapter_not_implemented",
        "descriptor": descriptor,
        "connectionAllowed": False,
    }
