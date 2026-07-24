from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime, timezone
import base64
import hashlib
import re

TOP_LEVEL_KEYS = frozenset({
    "status",
    "reason",
    "plan",
    "registryAdapterInvocationAllowed",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "authorizationConsumptionAllowed",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
    "trustedClockReadAllowed",
    "environmentCreationAllowed",
    "filesystemReadAllowed",
    "filesystemMutationAllowed",
    "processExecutionAllowed",
    "dependencyInstallationAllowed",
})

PLAN_KEYS = frozenset({
    "version",
    "operationId",
    "operationAttempt",
    "sourceStatus",
    "adapter",
    "registryKey",
    "compareAndSet",
    "consumptionRecord",
    "receiptTemplate",
    "conflicts",
    "errors",
    "rollback",
    "execution",
})

ADAPTER_KEYS = frozenset({
    "kind",
    "requiredCapability",
    "invocationAllowed",
})

REGISTRY_KEY_KEYS = frozenset({
    "requestId",
    "requestNonce",
    "acceptedPlanFingerprint",
})

COMPARE_AND_SET_KEYS = frozenset({
    "expectedState",
    "desiredState",
    "atomic",
    "withConsumptionRecord",
    "executionAllowed",
})

RECORD_KEYS = frozenset({
    "version",
    "requestId",
    "requestNonceFingerprint",
    "acceptedPlanFingerprint",
    "actor",
    "purpose",
    "consumedAt",
    "singleUse",
    "executionGrant",
    "status",
})

ACTOR_KEYS = frozenset({
    "kind",
    "id",
})

CONFLICT_KEYS = frozenset({
    "alreadyConsumed",
    "parallelConflict",
    "maximumParallelWinners",
})

ERROR_KEYS = frozenset({
    "adapterUnavailable",
    "atomicityUnavailable",
    "ambiguousCommit",
    "operationFailed",
    "rawErrorExposed",
    "automaticRetryAllowed",
    "reconciliationRequiredOnAmbiguous",
})

ROLLBACK_KEYS = frozenset({
    "preCommitFailureLeavesUnused",
    "postCommitResetToUnusedAllowed",
    "rollbackWriteAllowed",
})

EXECUTION_KEYS = frozenset({
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "authorizationConsumptionAllowed",
    "authorizationConsumed",
    "executionGrant",
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
    "registryAdapterInvocationAllowed",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "authorizationConsumptionAllowed",
    "authorizationConsumed",
    "authorizationGranted",
    "authorizationTokenGenerated",
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
    accepted_plan: dict[str, object] | None = None,
) -> dict[str, object]:
    return {
        "status": status,
        "reason": reason,
        "accepted": accepted,
        "acceptedPlan": accepted_plan,
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


def _validate_record(
    value: object,
    *,
    request_id: str,
    nonce_fingerprint: str,
    plan_fingerprint: str,
) -> dict[str, object] | None:
    if not isinstance(value, Mapping):
        return None

    data = dict(value)

    if set(data) != RECORD_KEYS:
        return None

    if data["version"] != 1:
        return None

    if data["requestId"] != request_id:
        return None

    if data["requestNonceFingerprint"] != nonce_fingerprint:
        return None

    if data["acceptedPlanFingerprint"] != plan_fingerprint:
        return None

    actor = data["actor"]

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
        or not ACTOR_PATTERN.fullmatch(actor_id)
    ):
        return None

    if data["purpose"] != EXPECTED_PURPOSE:
        return None

    if _parse_utc(data["consumedAt"]) is None:
        return None

    if data["singleUse"] is not True:
        return None

    if data["executionGrant"] is not False:
        return None

    if data["status"] != (
        "authorization_consumed_execution_locked"
    ):
        return None

    return {
        "version": 1,
        "requestId": request_id,
        "requestNonceFingerprint": nonce_fingerprint,
        "acceptedPlanFingerprint": plan_fingerprint,
        "actor": {
            "kind": "human_operator",
            "id": actor_id,
        },
        "purpose": EXPECTED_PURPOSE,
        "consumedAt": data["consumedAt"],
        "singleUse": True,
        "executionGrant": False,
        "status": "authorization_consumed_execution_locked",
    }


def accept_materialization_authorization_atomic_consumption_plan(
    candidate: object,
) -> dict[str, object]:
    if not isinstance(candidate, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_invalid_input"
        )

    candidate_data = dict(candidate)

    if set(candidate_data) != TOP_LEVEL_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_structure_invalid"
        )

    if candidate_data["status"] != (
        "atomic_consumption_plan_ready_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_source_status_invalid"
        )

    if candidate_data["reason"] != (
        "authorization_atomic_consumption_plan_"
        "ready_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_source_reason_invalid"
        )

    for flag in FALSE_SOURCE_FLAGS:
        if candidate_data[flag] is not False:
            return _blocked(
                "authorization_atomic_consumption_plan_"
                "acceptance_boundary_open"
            )

    plan = candidate_data["plan"]

    if not isinstance(plan, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_plan_invalid"
        )

    plan_data = dict(plan)

    if set(plan_data) != PLAN_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_plan_structure_invalid"
        )

    if plan_data["version"] != 1:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_operation_invalid"
        )

    operation_id = plan_data["operationId"]

    if (
        not isinstance(operation_id, str)
        or not UUID_V4_PATTERN.fullmatch(operation_id)
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_operation_invalid"
        )

    if plan_data["operationAttempt"] != 1:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_operation_invalid"
        )

    if plan_data["sourceStatus"] != (
        "accepted_consumption_ready_execution_locked"
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_source_binding_invalid"
        )

    adapter = plan_data["adapter"]

    if not isinstance(adapter, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_adapter_invalid"
        )

    adapter_data = dict(adapter)

    if set(adapter_data) != ADAPTER_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_adapter_invalid"
        )

    if adapter_data != {
        "kind": "single_use_consumption_registry",
        "requiredCapability": (
            "atomic_compare_and_set_with_consumption_record"
        ),
        "invocationAllowed": False,
    }:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_adapter_invalid"
        )

    registry_key = plan_data["registryKey"]

    if not isinstance(registry_key, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_registry_invalid"
        )

    registry_key_data = dict(registry_key)

    if set(registry_key_data) != REGISTRY_KEY_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_registry_invalid"
        )

    request_id = registry_key_data["requestId"]
    request_nonce = registry_key_data["requestNonce"]
    plan_fingerprint = registry_key_data[
        "acceptedPlanFingerprint"
    ]

    if (
        not isinstance(request_id, str)
        or not UUID_V4_PATTERN.fullmatch(request_id)
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_registry_invalid"
        )

    if not _valid_nonce(request_nonce):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_registry_invalid"
        )

    if (
        not isinstance(plan_fingerprint, str)
        or not FINGERPRINT_PATTERN.fullmatch(plan_fingerprint)
    ):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_registry_invalid"
        )

    nonce_fingerprint = _nonce_fingerprint(request_nonce)

    compare_and_set = plan_data["compareAndSet"]

    if not isinstance(compare_and_set, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_compare_and_set_invalid"
        )

    compare_data = dict(compare_and_set)

    if set(compare_data) != COMPARE_AND_SET_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_compare_and_set_invalid"
        )

    if compare_data != {
        "expectedState": "unused",
        "desiredState": "consumed",
        "atomic": True,
        "withConsumptionRecord": True,
        "executionAllowed": False,
    }:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_compare_and_set_invalid"
        )

    consumption_record = _validate_record(
        plan_data["consumptionRecord"],
        request_id=request_id,
        nonce_fingerprint=nonce_fingerprint,
        plan_fingerprint=plan_fingerprint,
    )

    if consumption_record is None:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_record_invalid"
        )

    receipt_template = _validate_record(
        plan_data["receiptTemplate"],
        request_id=request_id,
        nonce_fingerprint=nonce_fingerprint,
        plan_fingerprint=plan_fingerprint,
    )

    if receipt_template is None:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_receipt_invalid"
        )

    if receipt_template != consumption_record:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_receipt_invalid"
        )

    conflicts = plan_data["conflicts"]

    if not isinstance(conflicts, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_conflicts_invalid"
        )

    conflicts_data = dict(conflicts)

    if set(conflicts_data) != CONFLICT_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_conflicts_invalid"
        )

    if conflicts_data != {
        "alreadyConsumed": (
            "authorization_consumption_already_consumed"
        ),
        "parallelConflict": (
            "authorization_consumption_parallel_conflict"
        ),
        "maximumParallelWinners": 1,
    }:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_conflicts_invalid"
        )

    errors = plan_data["errors"]

    if not isinstance(errors, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_errors_invalid"
        )

    errors_data = dict(errors)

    if set(errors_data) != ERROR_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_errors_invalid"
        )

    if errors_data != {
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
    }:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_errors_invalid"
        )

    rollback = plan_data["rollback"]

    if not isinstance(rollback, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_rollback_invalid"
        )

    rollback_data = dict(rollback)

    if set(rollback_data) != ROLLBACK_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_rollback_invalid"
        )

    if rollback_data != {
        "preCommitFailureLeavesUnused": True,
        "postCommitResetToUnusedAllowed": False,
        "rollbackWriteAllowed": False,
    }:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_rollback_invalid"
        )

    execution = plan_data["execution"]

    if not isinstance(execution, Mapping):
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_execution_invalid"
        )

    execution_data = dict(execution)

    if set(execution_data) != EXECUTION_KEYS:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_execution_invalid"
        )

    if execution_data != {
        "registryReadAllowed": False,
        "registryWriteAllowed": False,
        "atomicCompareAndSetAllowed": False,
        "authorizationConsumptionAllowed": False,
        "authorizationConsumed": False,
        "executionGrant": False,
    }:
        return _blocked(
            "authorization_atomic_consumption_plan_"
            "acceptance_execution_invalid"
        )

    canonical_plan = {
        "version": 1,
        "operationId": operation_id,
        "operationAttempt": 1,
        "sourceStatus": (
            "accepted_consumption_ready_execution_locked"
        ),
        "adapter": dict(adapter_data),
        "registryKey": {
            "requestId": request_id,
            "requestNonce": request_nonce,
            "acceptedPlanFingerprint": plan_fingerprint,
        },
        "compareAndSet": dict(compare_data),
        "consumptionRecord": consumption_record,
        "receiptTemplate": receipt_template,
        "conflicts": dict(conflicts_data),
        "errors": dict(errors_data),
        "rollback": dict(rollback_data),
        "execution": dict(execution_data),
    }

    return _result(
        "accepted_atomic_consumption_plan_execution_locked",
        "authorization_atomic_consumption_plan_"
        "accepted_execution_locked",
        True,
        canonical_plan,
    )
