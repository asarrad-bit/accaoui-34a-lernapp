from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import base64
import hashlib
import json
import re

ALLOWED_KEYS = frozenset({
    "acceptedPlanResult",
    "requestId",
    "requestNonce",
    "actorId",
    "acceptedPlanFingerprint",
    "issuedAt",
    "expiresAt",
})

UUID_V4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ACTOR_PATTERN = re.compile(r"^[^\x00-\x1f\x7f]{1,128}$")
RFC3339_UTC_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)
NONCE_PATTERN = re.compile(r"^[A-Za-z0-9_-]{43}$")


def _result(
    status: str,
    reason: str,
    request: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "request": request,
        "authorizationRequestIssued": request is not None,
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


def _parse_rfc3339_utc(value: object) -> datetime | None:
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


def _canonical_plan_fingerprint(plan: object) -> str | None:
    if not isinstance(plan, Mapping):
        return None

    try:
        payload = json.dumps(
            dict(plan),
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError):
        return None

    return hashlib.sha256(payload).hexdigest()


def build_materialization_authorization_request_state(
    facts: object,
) -> dict[str, object]:
    if not isinstance(facts, Mapping):
        return _blocked(
            "materialization_authorization_request_invalid_input"
        )

    input_data = dict(facts)
    input_keys = set(input_data)

    if input_keys - ALLOWED_KEYS:
        return _blocked(
            "materialization_authorization_request_unknown_fields"
        )

    if ALLOWED_KEYS - input_keys:
        return _blocked(
            "materialization_authorization_request_missing_fields"
        )

    accepted_result = input_data["acceptedPlanResult"]

    if not isinstance(accepted_result, Mapping):
        return _blocked(
            "materialization_authorization_source_invalid"
        )

    accepted_data = dict(accepted_result)

    required_source = {
        "status": "accepted_execution_locked",
        "reason": (
            "test_environment_materialization_plan_"
            "accepted_execution_locked"
        ),
        "accepted": True,
        "environmentCreationAllowed": False,
        "filesystemReadAllowed": False,
        "filesystemMutationAllowed": False,
        "processExecutionAllowed": False,
        "dependencyInstallationAllowed": False,
        "evidenceCollectionAllowed": False,
        "rollbackExecutionAllowed": False,
        "authorizationGrantAccepted": False,
    }

    for key, expected_value in required_source.items():
        if accepted_data.get(key) != expected_value:
            return _blocked(
                "materialization_authorization_source_invalid"
            )

    accepted_plan = accepted_data.get("acceptedPlan")
    derived_fingerprint = _canonical_plan_fingerprint(
        accepted_plan
    )

    if derived_fingerprint is None:
        return _blocked(
            "materialization_authorization_source_invalid"
        )

    supplied_fingerprint = input_data[
        "acceptedPlanFingerprint"
    ]

    if (
        not isinstance(supplied_fingerprint, str)
        or not FINGERPRINT_PATTERN.fullmatch(
            supplied_fingerprint
        )
        or supplied_fingerprint != derived_fingerprint
    ):
        return _blocked(
            "materialization_authorization_plan_fingerprint_invalid"
        )

    request_id = input_data["requestId"]

    if (
        not isinstance(request_id, str)
        or not UUID_V4_PATTERN.fullmatch(request_id)
    ):
        return _blocked(
            "materialization_authorization_identity_invalid"
        )

    request_nonce = input_data["requestNonce"]

    if (
        not isinstance(request_nonce, str)
        or not NONCE_PATTERN.fullmatch(request_nonce)
    ):
        return _blocked(
            "materialization_authorization_identity_invalid"
        )

    try:
        nonce_bytes = base64.urlsafe_b64decode(
            request_nonce + "="
        )
    except Exception:
        return _blocked(
            "materialization_authorization_identity_invalid"
        )

    if len(nonce_bytes) != 32:
        return _blocked(
            "materialization_authorization_identity_invalid"
        )

    actor_id = input_data["actorId"]

    if (
        not isinstance(actor_id, str)
        or actor_id != actor_id.strip()
        or not ACTOR_PATTERN.fullmatch(actor_id)
    ):
        return _blocked(
            "materialization_authorization_identity_invalid"
        )

    issued_at_text = input_data["issuedAt"]
    expires_at_text = input_data["expiresAt"]
    issued_at = _parse_rfc3339_utc(issued_at_text)
    expires_at = _parse_rfc3339_utc(expires_at_text)

    if issued_at is None or expires_at is None:
        return _blocked(
            "materialization_authorization_time_invalid"
        )

    if int((expires_at - issued_at).total_seconds()) != 300:
        return _blocked(
            "materialization_authorization_time_invalid"
        )

    if expires_at <= issued_at:
        return _blocked(
            "materialization_authorization_time_invalid"
        )

    request = {
        "version": 1,
        "requestId": request_id,
        "requestNonce": request_nonce,
        "actor": {
            "kind": "human_operator",
            "id": actor_id,
        },
        "purpose": (
            "disposable_test_python_"
            "environment_materialization"
        ),
        "acceptedPlanStatus": "accepted_execution_locked",
        "acceptedPlanReason": (
            "test_environment_materialization_plan_"
            "accepted_execution_locked"
        ),
        "acceptedPlanFingerprint": derived_fingerprint,
        "issuedAt": issued_at_text,
        "expiresAt": expires_at_text,
        "singleUse": True,
        "executionGrant": False,
        "status": "authorization_request_pending_locked",
    }

    return _result(
        "authorization_request_ready_locked",
        "materialization_authorization_request_ready_locked",
        request,
    )
