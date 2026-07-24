from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import base64
import hashlib
import re

ALLOWED_KEYS = frozenset({
    "transitionResult",
    "requestId",
    "requestNonce",
    "acceptedPlanFingerprint",
    "actor",
    "purpose",
    "consumedAt",
    "registryState",
})

UUID_V4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
NONCE_PATTERN = re.compile(r"^[A-Za-z0-9_-]{43}$")
FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{64}$")
RFC3339_UTC_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)

SOURCE_FALSE_FLAGS = (
    "authorizationGranted",
    "authorizationTokenGenerated",
    "authorizationConsumed",
    "environmentCreationAllowed",
    "filesystemReadAllowed",
    "filesystemMutationAllowed",
    "processExecutionAllowed",
    "dependencyInstallationAllowed",
)

EXPECTED_PURPOSE = (
    "disposable_test_python_environment_materialization"
)


def _result(
    status: str,
    reason: str,
    readiness: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "readiness": readiness,
        "authorizationConsumptionAllowed": False,
        "authorizationConsumed": False,
        "authorizationGranted": False,
        "authorizationTokenGenerated": False,
        "registryReadAllowed": False,
        "registryWriteAllowed": False,
        "atomicCompareAndSetAllowed": False,
        "trustedClockReadAllowed": False,
        "environmentCreationAllowed": False,
        "filesystemReadAllowed": False,
        "filesystemMutationAllowed": False,
        "processExecutionAllowed": False,
        "dependencyInstallationAllowed": False,
    }


def _blocked(reason: str) -> dict[str, object]:
    return _result("blocked", reason)


def _parse_utc(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None

    if not RFC3339_UTC_PATTERN.fullmatch(value):
        return None

    try:
        parsed = datetime.strptime(
            value,
            "%Y-%m-%dT%H:%M:%SZ",
        )
    except ValueError:
        return None

    return parsed.replace(tzinfo=timezone.utc)


def _valid_nonce(value: object) -> bool:
    if not isinstance(value, str):
        return False

    if not NONCE_PATTERN.fullmatch(value):
        return False

    try:
        decoded = base64.urlsafe_b64decode(value + "=")
    except Exception:
        return False

    return len(decoded) == 32


def _nonce_fingerprint(value: str) -> str:
    return hashlib.sha256(value.encode("ascii")).hexdigest()


def evaluate_materialization_authorization_consumption_readiness(
    facts: object,
) -> dict[str, object]:
    if not isinstance(facts, Mapping):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_invalid_input"
        )

    input_data = dict(facts)
    input_keys = set(input_data)

    if input_keys - ALLOWED_KEYS:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_unknown_fields"
        )

    if ALLOWED_KEYS - input_keys:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_missing_fields"
        )

    transition_result = input_data["transitionResult"]

    if not isinstance(transition_result, Mapping):
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    transition_data = dict(transition_result)

    if transition_data.get("status") != (
        "transition_applied_execution_locked"
    ):
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    for flag in SOURCE_FALSE_FLAGS:
        if transition_data.get(flag) is not False:
            return _blocked(
                "materialization_authorization_consumption_source_invalid"
            )

    transition = transition_data.get("transition")

    if not isinstance(transition, Mapping):
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    transition = dict(transition)

    if transition.get("decision") != "approve":
        return _blocked(
            "materialization_authorization_consumption_not_approved"
        )

    if transition.get("sourceStatus") != (
        "authorization_request_pending_locked"
    ):
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    if transition.get("targetStatus") != (
        "authorization_request_approved_locked"
    ):
        return _blocked(
            "materialization_authorization_consumption_not_approved"
        )

    if transition.get("terminal") is not False:
        return _blocked(
            "materialization_authorization_consumption_not_approved"
        )

    if transition.get("executionGrant") is not False:
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    request = transition.get("request")

    if not isinstance(request, Mapping):
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    request = dict(request)

    if request.get("version") != 1:
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    if request.get("status") != (
        "authorization_request_approved_locked"
    ):
        return _blocked(
            "materialization_authorization_consumption_not_approved"
        )

    if request.get("singleUse") is not True:
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    if request.get("executionGrant") is not False:
        return _blocked(
            "materialization_authorization_consumption_source_invalid"
        )

    request_id = input_data["requestId"]
    request_nonce = input_data["requestNonce"]
    plan_fingerprint = input_data["acceptedPlanFingerprint"]
    actor = input_data["actor"]
    purpose = input_data["purpose"]

    if (
        not isinstance(request_id, str)
        or not UUID_V4_PATTERN.fullmatch(request_id)
        or request.get("requestId") != request_id
    ):
        return _blocked(
            "materialization_authorization_consumption_binding_invalid"
        )

    if (
        not _valid_nonce(request_nonce)
        or request.get("requestNonce") != request_nonce
    ):
        return _blocked(
            "materialization_authorization_consumption_binding_invalid"
        )

    if (
        not isinstance(plan_fingerprint, str)
        or not FINGERPRINT_PATTERN.fullmatch(plan_fingerprint)
        or request.get("acceptedPlanFingerprint") != plan_fingerprint
    ):
        return _blocked(
            "materialization_authorization_consumption_binding_invalid"
        )

    if (
        not isinstance(actor, Mapping)
        or dict(actor) != request.get("actor")
    ):
        return _blocked(
            "materialization_authorization_consumption_binding_invalid"
        )

    if (
        purpose != EXPECTED_PURPOSE
        or request.get("purpose") != purpose
    ):
        return _blocked(
            "materialization_authorization_consumption_binding_invalid"
        )

    issued_at = _parse_utc(request.get("issuedAt"))
    expires_at = _parse_utc(request.get("expiresAt"))
    approved_at = _parse_utc(transition.get("evaluatedAt"))
    consumed_at = _parse_utc(input_data["consumedAt"])

    if (
        issued_at is None
        or expires_at is None
        or approved_at is None
        or consumed_at is None
    ):
        return _blocked(
            "materialization_authorization_consumption_time_invalid"
        )

    if consumed_at < issued_at or consumed_at < approved_at:
        return _blocked(
            "materialization_authorization_consumption_time_invalid"
        )

    if consumed_at >= expires_at:
        return _blocked(
            "materialization_authorization_consumption_expired"
        )

    registry_state = input_data["registryState"]

    if registry_state == "consumed":
        return _blocked(
            "materialization_authorization_"
            "consumption_already_consumed"
        )

    if registry_state == "in_flight":
        return _blocked(
            "materialization_authorization_"
            "consumption_parallel_conflict"
        )

    if registry_state != "unused":
        return _blocked(
            "materialization_authorization_"
            "consumption_registry_state_invalid"
        )

    registry_key = {
        "requestId": request_id,
        "requestNonce": request_nonce,
        "acceptedPlanFingerprint": plan_fingerprint,
    }

    readiness = {
        "requestId": request_id,
        "requestNonceFingerprint": _nonce_fingerprint(
            request_nonce
        ),
        "acceptedPlanFingerprint": plan_fingerprint,
        "actor": dict(actor),
        "purpose": purpose,
        "issuedAt": request["issuedAt"],
        "approvedAt": transition["evaluatedAt"],
        "expiresAt": request["expiresAt"],
        "consumedAt": input_data["consumedAt"],
        "registryKey": registry_key,
        "registryState": "unused",
        "compareState": "unused",
        "setState": "consumed",
        "singleUse": True,
        "executionGrant": False,
    }

    return _result(
        "consumption_ready_execution_locked",
        "materialization_authorization_"
        "consumption_ready_execution_locked",
        readiness,
    )
