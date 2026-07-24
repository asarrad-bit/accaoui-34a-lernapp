from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import base64
import hashlib
import re

ALLOWED_KEYS = frozenset({
    "acceptedReadinessResult",
    "operationId",
    "operationAttempt",
    "adapterFacts",
})

ADAPTER_FACT_KEYS = frozenset({
    "adapterKind",
    "atomicCompareAndSetWithRecord",
    "definitiveAlreadyConsumedOutcome",
    "definitiveParallelConflictOutcome",
    "ambiguousCommitOutcome",
    "reconciliationRequiredOnAmbiguous",
    "rawErrorSuppressed",
    "maximumParallelWinners",
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

UUID_V4_PATTERN = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-"
    r"[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
)
NONCE_PATTERN = re.compile(r"^[A-Za-z0-9_-]{43}$")
FINGERPRINT_PATTERN = re.compile(r"^[0-9a-f]{64}$")
RFC3339_UTC_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
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

EXPECTED_PURPOSE = (
    "disposable_test_python_environment_materialization"
)


def _result(
    status: str,
    reason: str,
    plan: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "plan": plan,
        "registryAdapterInvocationAllowed": False,
        "registryReadAllowed": False,
        "registryWriteAllowed": False,
        "atomicCompareAndSetAllowed": False,
        "authorizationConsumptionAllowed": False,
        "authorizationConsumed": False,
        "authorizationGranted": False,
        "authorizationTokenGenerated": False,
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


def build_materialization_authorization_atomic_consumption_plan(
    facts: object,
) -> dict[str, object]:
    if not isinstance(facts, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_invalid_input"
        )

    input_data = dict(facts)
    input_keys = set(input_data)

    if input_keys - ALLOWED_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_unknown_fields"
        )

    if ALLOWED_KEYS - input_keys:
        return _blocked(
            "authorization_atomic_consumption_plan_missing_fields"
        )

    accepted_result = input_data["acceptedReadinessResult"]

    if not isinstance(accepted_result, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_source_invalid"
        )

    accepted_data = dict(accepted_result)

    if accepted_data.get("status") != (
        "accepted_consumption_ready_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_source_invalid"
        )

    if accepted_data.get("reason") != (
        "materialization_authorization_consumption_"
        "readiness_accepted_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_source_invalid"
        )

    if accepted_data.get("accepted") is not True:
        return _blocked(
            "authorization_atomic_consumption_plan_source_invalid"
        )

    for flag in FALSE_SOURCE_FLAGS:
        if accepted_data.get(flag) is not False:
            return _blocked(
                "authorization_atomic_consumption_plan_source_invalid"
            )

    readiness = accepted_data.get("acceptedReadiness")

    if not isinstance(readiness, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_source_invalid"
        )

    readiness_data = dict(readiness)

    if set(readiness_data) != READINESS_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_source_invalid"
        )

    request_id = readiness_data["requestId"]
    nonce_fingerprint = readiness_data["requestNonceFingerprint"]
    plan_fingerprint = readiness_data["acceptedPlanFingerprint"]

    if (
        not isinstance(request_id, str)
        or not UUID_V4_PATTERN.fullmatch(request_id)
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    for fingerprint in (
        nonce_fingerprint,
        plan_fingerprint,
    ):
        if (
            not isinstance(fingerprint, str)
            or not FINGERPRINT_PATTERN.fullmatch(fingerprint)
        ):
            return _blocked(
                "authorization_atomic_consumption_plan_binding_invalid"
            )

    registry_key = readiness_data["registryKey"]

    if not isinstance(registry_key, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    registry_key_data = dict(registry_key)

    if set(registry_key_data) != REGISTRY_KEY_FIELDS:
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    request_nonce = registry_key_data["requestNonce"]

    if not _valid_nonce(request_nonce):
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    if registry_key_data["requestId"] != request_id:
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    if (
        registry_key_data["acceptedPlanFingerprint"]
        != plan_fingerprint
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    if _nonce_fingerprint(request_nonce) != nonce_fingerprint:
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    if readiness_data["purpose"] != EXPECTED_PURPOSE:
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    actor = readiness_data["actor"]

    if not isinstance(actor, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
        )

    actor_data = dict(actor)

    if (
        actor_data.get("kind") != "human_operator"
        or not isinstance(actor_data.get("id"), str)
        or not actor_data["id"]
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_binding_invalid"
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
            "authorization_atomic_consumption_plan_time_invalid"
        )

    if int((expires_at - issued_at).total_seconds()) != 300:
        return _blocked(
            "authorization_atomic_consumption_plan_time_invalid"
        )

    if approved_at < issued_at or consumed_at < approved_at:
        return _blocked(
            "authorization_atomic_consumption_plan_time_invalid"
        )

    if consumed_at >= expires_at:
        return _blocked(
            "authorization_atomic_consumption_plan_time_invalid"
        )

    if readiness_data["registryState"] != "unused":
        return _blocked(
            "authorization_atomic_consumption_plan_registry_invalid"
        )

    if readiness_data["compareState"] != "unused":
        return _blocked(
            "authorization_atomic_consumption_plan_registry_invalid"
        )

    if readiness_data["setState"] != "consumed":
        return _blocked(
            "authorization_atomic_consumption_plan_registry_invalid"
        )

    if readiness_data["singleUse"] is not True:
        return _blocked(
            "authorization_atomic_consumption_plan_lock_invalid"
        )

    if readiness_data["executionGrant"] is not False:
        return _blocked(
            "authorization_atomic_consumption_plan_lock_invalid"
        )

    operation_id = input_data["operationId"]

    if (
        not isinstance(operation_id, str)
        or not UUID_V4_PATTERN.fullmatch(operation_id)
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_operation_invalid"
        )

    if input_data["operationAttempt"] != 1:
        return _blocked(
            "authorization_atomic_consumption_plan_operation_invalid"
        )

    adapter_facts = input_data["adapterFacts"]

    if not isinstance(adapter_facts, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_adapter_invalid"
        )

    adapter_data = dict(adapter_facts)

    if set(adapter_data) != ADAPTER_FACT_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_adapter_invalid"
        )

    expected_adapter = {
        "adapterKind": "single_use_consumption_registry",
        "atomicCompareAndSetWithRecord": True,
        "definitiveAlreadyConsumedOutcome": True,
        "definitiveParallelConflictOutcome": True,
        "ambiguousCommitOutcome": True,
        "reconciliationRequiredOnAmbiguous": True,
        "rawErrorSuppressed": True,
        "maximumParallelWinners": 1,
    }

    if adapter_data != expected_adapter:
        return _blocked(
            "authorization_atomic_consumption_plan_adapter_invalid"
        )

    receipt_template = {
        "version": 1,
        "requestId": request_id,
        "requestNonceFingerprint": nonce_fingerprint,
        "acceptedPlanFingerprint": plan_fingerprint,
        "actor": {
            "kind": "human_operator",
            "id": actor_data["id"],
        },
        "purpose": EXPECTED_PURPOSE,
        "consumedAt": readiness_data["consumedAt"],
        "singleUse": True,
        "executionGrant": False,
        "status": "authorization_consumed_execution_locked",
    }

    plan = {
        "version": 1,
        "operationId": operation_id,
        "operationAttempt": 1,
        "sourceStatus": (
            "accepted_consumption_ready_execution_locked"
        ),
        "adapter": {
            "kind": "single_use_consumption_registry",
            "requiredCapability": (
                "atomic_compare_and_set_with_consumption_record"
            ),
            "invocationAllowed": False,
        },
        "registryKey": {
            "requestId": request_id,
            "requestNonce": request_nonce,
            "acceptedPlanFingerprint": plan_fingerprint,
        },
        "compareAndSet": {
            "expectedState": "unused",
            "desiredState": "consumed",
            "atomic": True,
            "withConsumptionRecord": True,
            "executionAllowed": False,
        },
        "consumptionRecord": dict(receipt_template),
        "receiptTemplate": dict(receipt_template),
        "conflicts": {
            "alreadyConsumed": (
                "authorization_consumption_already_consumed"
            ),
            "parallelConflict": (
                "authorization_consumption_parallel_conflict"
            ),
            "maximumParallelWinners": 1,
        },
        "errors": {
            "adapterUnavailable": (
                "authorization_consumption_adapter_unavailable"
            ),
            "atomicityUnavailable": (
                "authorization_consumption_atomicity_unavailable"
            ),
            "ambiguousCommit": (
                "authorization_consumption_commit_ambiguous"
            ),
            "operationFailed": (
                "authorization_consumption_operation_failed"
            ),
            "rawErrorExposed": False,
            "automaticRetryAllowed": False,
            "reconciliationRequiredOnAmbiguous": True,
        },
        "rollback": {
            "preCommitFailureLeavesUnused": True,
            "postCommitResetToUnusedAllowed": False,
            "rollbackWriteAllowed": False,
        },
        "execution": {
            "registryReadAllowed": False,
            "registryWriteAllowed": False,
            "atomicCompareAndSetAllowed": False,
            "authorizationConsumptionAllowed": False,
            "authorizationConsumed": False,
            "executionGrant": False,
        },
    }

    return _result(
        "atomic_consumption_plan_ready_execution_locked",
        "authorization_atomic_consumption_plan_"
        "ready_execution_locked",
        plan,
    )
