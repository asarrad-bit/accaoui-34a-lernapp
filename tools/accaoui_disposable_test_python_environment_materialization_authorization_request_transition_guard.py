from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import re

ALLOWED_KEYS = frozenset({
    "requestStateResult",
    "decision",
    "evaluatedAt",
})

REQUEST_KEYS = frozenset({
    "version",
    "requestId",
    "requestNonce",
    "actor",
    "purpose",
    "acceptedPlanStatus",
    "acceptedPlanReason",
    "acceptedPlanFingerprint",
    "issuedAt",
    "expiresAt",
    "singleUse",
    "executionGrant",
    "status",
})

ACTOR_KEYS = frozenset({"kind", "id"})
DECISIONS = frozenset({"approve", "reject", "revoke"})
RFC3339_UTC_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)
UUID_V4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
NONCE_PATTERN = re.compile(r"^[A-Za-z0-9_-]{43}$")
FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def _result(
    status: str,
    reason: str,
    transitioned_request: dict[str, object] | None = None,
    transition: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "transitionedRequest": transitioned_request,
        "transition": transition,
        "authorizationGranted": False,
        "authorizationTokenGenerated": False,
        "authorizationConsumed": False,
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


def _validate_request_state(
    request_state_result: object,
) -> dict[str, object] | None:
    if not isinstance(request_state_result, Mapping):
        return None

    state_data = dict(request_state_result)

    expected_state_values = {
        "status": "authorization_request_ready_locked",
        "reason": "materialization_authorization_request_ready_locked",
        "authorizationRequestIssued": True,
        "authorizationGranted": False,
        "authorizationTokenGenerated": False,
        "authorizationConsumed": False,
        "environmentCreationAllowed": False,
        "filesystemReadAllowed": False,
        "filesystemMutationAllowed": False,
        "processExecutionAllowed": False,
        "dependencyInstallationAllowed": False,
    }

    for key, expected_value in expected_state_values.items():
        if state_data.get(key) != expected_value:
            return None

    request = state_data.get("request")

    if not isinstance(request, Mapping):
        return None

    request_data = dict(request)

    if set(request_data) != REQUEST_KEYS:
        return None

    if request_data.get("version") != 1:
        return None

    if request_data.get("status") != (
        "authorization_request_pending_locked"
    ):
        return None

    if request_data.get("purpose") != (
        "disposable_test_python_environment_materialization"
    ):
        return None

    if request_data.get("acceptedPlanStatus") != (
        "accepted_execution_locked"
    ):
        return None

    if request_data.get("acceptedPlanReason") != (
        "test_environment_materialization_plan_"
        "accepted_execution_locked"
    ):
        return None

    if request_data.get("singleUse") is not True:
        return None

    if request_data.get("executionGrant") is not False:
        return None

    request_id = request_data.get("requestId")
    nonce = request_data.get("requestNonce")
    fingerprint = request_data.get("acceptedPlanFingerprint")

    if not isinstance(request_id, str):
        return None
    if not UUID_V4_PATTERN.fullmatch(request_id):
        return None
    if not isinstance(nonce, str):
        return None
    if not NONCE_PATTERN.fullmatch(nonce):
        return None
    if not isinstance(fingerprint, str):
        return None
    if not FINGERPRINT_PATTERN.fullmatch(fingerprint):
        return None

    actor = request_data.get("actor")

    if not isinstance(actor, Mapping):
        return None

    actor_data = dict(actor)

    if set(actor_data) != ACTOR_KEYS:
        return None

    if actor_data.get("kind") != "human_operator":
        return None

    actor_id = actor_data.get("id")

    if (
        not isinstance(actor_id, str)
        or actor_id != actor_id.strip()
        or not 1 <= len(actor_id) <= 128
    ):
        return None

    issued_at = _parse_utc(request_data.get("issuedAt"))
    expires_at = _parse_utc(request_data.get("expiresAt"))

    if issued_at is None or expires_at is None:
        return None

    if int((expires_at - issued_at).total_seconds()) != 300:
        return None

    return {
        **request_data,
        "actor": dict(actor_data),
    }


def transition_materialization_authorization_request(
    facts: object,
) -> dict[str, object]:
    if not isinstance(facts, Mapping):
        return _blocked(
            "materialization_authorization_transition_invalid_input"
        )

    input_data = dict(facts)
    input_keys = set(input_data)

    if input_keys - ALLOWED_KEYS:
        return _blocked(
            "materialization_authorization_transition_unknown_fields"
        )

    if ALLOWED_KEYS - input_keys:
        return _blocked(
            "materialization_authorization_transition_missing_fields"
        )

    request = _validate_request_state(
        input_data["requestStateResult"]
    )

    if request is None:
        return _blocked(
            "materialization_authorization_transition_source_invalid"
        )

    decision = input_data["decision"]

    if decision not in DECISIONS:
        return _blocked(
            "materialization_authorization_transition_decision_invalid"
        )

    evaluated_at_text = input_data["evaluatedAt"]
    evaluated_at = _parse_utc(evaluated_at_text)
    issued_at = _parse_utc(request["issuedAt"])
    expires_at = _parse_utc(request["expiresAt"])

    if (
        evaluated_at is None
        or issued_at is None
        or expires_at is None
        or evaluated_at < issued_at
    ):
        return _blocked(
            "materialization_authorization_transition_time_invalid"
        )

    if evaluated_at >= expires_at:
        target_status = "authorization_request_expired"
        reason = "materialization_authorization_request_expired"
        effective_decision = "expire"
    elif decision == "reject":
        target_status = "authorization_request_rejected"
        reason = "materialization_authorization_request_rejected"
        effective_decision = "reject"
    elif decision == "revoke":
        target_status = "authorization_request_revoked"
        reason = "materialization_authorization_request_revoked"
        effective_decision = "revoke"
    else:
        target_status = "authorization_request_approved_locked"
        reason = "materialization_authorization_request_approved_locked"
        effective_decision = "approve"

    transitioned_request = {
        **request,
        "actor": dict(request["actor"]),
        "executionGrant": False,
        "status": target_status,
    }

    transition = {
        "fromStatus": "authorization_request_pending_locked",
        "toStatus": target_status,
        "requestedDecision": decision,
        "effectiveDecision": effective_decision,
        "evaluatedAt": evaluated_at_text,
        "terminal": target_status in {
            "authorization_request_rejected",
            "authorization_request_expired",
            "authorization_request_revoked",
        },
        "executionGrant": False,
    }

    return _result(
        "transition_applied_execution_locked",
        reason,
        transitioned_request,
        transition,
    )
