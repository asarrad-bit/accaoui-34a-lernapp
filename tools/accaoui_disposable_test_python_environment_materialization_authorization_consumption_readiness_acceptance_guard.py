from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import base64
import hashlib
import re

TOP_LEVEL_KEYS = frozenset({
    "status",
    "reason",
    "readiness",
    "authorizationConsumptionAllowed",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "trustedClockReadAllowed",
    "environmentCreationAllowed",
    "filesystemReadAllowed",
    "filesystemMutationAllowed",
    "processExecutionAllowed",
    "dependencyInstallationAllowed",
})

READINESS_KEYS = frozenset({
    "requestId",
    "requestNonceFingerprint",
    "acceptedPlanFingerprint",
    "actor",
    "purpose",
    "issuedAt",
    "approvedAt",
    "expiresAt",
    "consumedAt",
    "registryKey",
    "registryState",
    "compareState",
    "setState",
    "singleUse",
    "executionGrant",
})

REGISTRY_KEY_FIELDS = frozenset({
    "requestId",
    "requestNonce",
    "acceptedPlanFingerprint",
})

ACTOR_FIELDS = frozenset({
    "kind",
    "id",
})

UUID_V4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
NONCE_PATTERN = re.compile(r"^[A-Za-z0-9_-]{43}$")
FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{64}$")
ACTOR_PATTERN = re.compile(r"^[^\x00-\x1f\x7f]{1,128}$")
RFC3339_UTC_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
)

EXPECTED_PURPOSE = (
    "disposable_test_python_environment_materialization"
)

FALSE_SOURCE_FLAGS = (
    "authorizationConsumptionAllowed",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "trustedClockReadAllowed",
    "environmentCreationAllowed",
    "filesystemReadAllowed",
    "filesystemMutationAllowed",
    "processExecutionAllowed",
    "dependencyInstallationAllowed",
)


def _result(
    status: str,
    reason: str,
    accepted: bool,
    accepted_readiness: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "accepted": accepted,
        "acceptedReadiness": accepted_readiness,
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
    return _result("blocked", reason, False)


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


def accept_materialization_authorization_consumption_readiness(
    candidate: object,
) -> dict[str, object]:
    if not isinstance(candidate, Mapping):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_invalid_input"
        )

    candidate_data = dict(candidate)

    if set(candidate_data) != TOP_LEVEL_KEYS:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_structure_invalid"
        )

    if candidate_data["status"] != (
        "consumption_ready_execution_locked"
    ):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_source_status_invalid"
        )

    if candidate_data["reason"] != (
        "materialization_authorization_"
        "consumption_ready_execution_locked"
    ):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_source_reason_invalid"
        )

    for flag in FALSE_SOURCE_FLAGS:
        if candidate_data[flag] is not False:
            return _blocked(
                "materialization_authorization_"
                "consumption_readiness_acceptance_boundary_open"
            )

    readiness = candidate_data["readiness"]

    if not isinstance(readiness, Mapping):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_readiness_invalid"
        )

    readiness_data = dict(readiness)

    if set(readiness_data) != READINESS_KEYS:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_readiness_structure_invalid"
        )

    request_id = readiness_data["requestId"]

    if (
        not isinstance(request_id, str)
        or not UUID_V4_PATTERN.fullmatch(request_id)
    ):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_binding_invalid"
        )

    plan_fingerprint = readiness_data[
        "acceptedPlanFingerprint"
    ]

    if (
        not isinstance(plan_fingerprint, str)
        or not FINGERPRINT_PATTERN.fullmatch(plan_fingerprint)
    ):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_binding_invalid"
        )

    nonce_fingerprint = readiness_data[
        "requestNonceFingerprint"
    ]

    if (
        not isinstance(nonce_fingerprint, str)
        or not FINGERPRINT_PATTERN.fullmatch(nonce_fingerprint)
    ):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_binding_invalid"
        )

    actor = readiness_data["actor"]

    if not isinstance(actor, Mapping):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_binding_invalid"
        )

    actor_data = dict(actor)

    if set(actor_data) != ACTOR_FIELDS:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_binding_invalid"
        )

    if actor_data.get("kind") != "human_operator":
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_binding_invalid"
        )

    actor_id = actor_data.get("id")

    if (
        not isinstance(actor_id, str)
        or actor_id != actor_id.strip()
        or not ACTOR_PATTERN.fullmatch(actor_id)
    ):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_binding_invalid"
        )

    if readiness_data["purpose"] != EXPECTED_PURPOSE:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_binding_invalid"
        )

    registry_key = readiness_data["registryKey"]

    if not isinstance(registry_key, Mapping):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    registry_key_data = dict(registry_key)

    if set(registry_key_data) != REGISTRY_KEY_FIELDS:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    request_nonce = registry_key_data["requestNonce"]

    if not _valid_nonce(request_nonce):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    if registry_key_data["requestId"] != request_id:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    if (
        registry_key_data["acceptedPlanFingerprint"]
        != plan_fingerprint
    ):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    if _nonce_fingerprint(request_nonce) != nonce_fingerprint:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    issued_at = _parse_utc(readiness_data["issuedAt"])
    approved_at = _parse_utc(readiness_data["approvedAt"])
    expires_at = _parse_utc(readiness_data["expiresAt"])
    consumed_at = _parse_utc(readiness_data["consumedAt"])

    if (
        issued_at is None
        or approved_at is None
        or expires_at is None
        or consumed_at is None
    ):
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_time_invalid"
        )

    if int((expires_at - issued_at).total_seconds()) != 300:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_time_invalid"
        )

    if approved_at < issued_at:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_time_invalid"
        )

    if consumed_at < approved_at:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_time_invalid"
        )

    if consumed_at >= expires_at:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_time_invalid"
        )

    if readiness_data["registryState"] != "unused":
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    if readiness_data["compareState"] != "unused":
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    if readiness_data["setState"] != "consumed":
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_registry_invalid"
        )

    if readiness_data["singleUse"] is not True:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_lock_invalid"
        )

    if readiness_data["executionGrant"] is not False:
        return _blocked(
            "materialization_authorization_"
            "consumption_readiness_acceptance_lock_invalid"
        )

    canonical_readiness = {
        "requestId": request_id,
        "requestNonceFingerprint": nonce_fingerprint,
        "acceptedPlanFingerprint": plan_fingerprint,
        "actor": {
            "kind": "human_operator",
            "id": actor_id,
        },
        "purpose": EXPECTED_PURPOSE,
        "issuedAt": readiness_data["issuedAt"],
        "approvedAt": readiness_data["approvedAt"],
        "expiresAt": readiness_data["expiresAt"],
        "consumedAt": readiness_data["consumedAt"],
        "registryKey": {
            "requestId": request_id,
            "requestNonce": request_nonce,
            "acceptedPlanFingerprint": plan_fingerprint,
        },
        "registryState": "unused",
        "compareState": "unused",
        "setState": "consumed",
        "singleUse": True,
        "executionGrant": False,
    }

    return _result(
        "accepted_consumption_ready_execution_locked",
        "materialization_authorization_consumption_"
        "readiness_accepted_execution_locked",
        True,
        canonical_readiness,
    )
