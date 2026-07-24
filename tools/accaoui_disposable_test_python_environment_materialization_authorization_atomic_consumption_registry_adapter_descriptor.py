from __future__ import annotations

from collections.abc import Mapping


RESULT_KINDS = [
    "committed",
    "already_consumed",
    "parallel_conflict",
    "binding_conflict",
    "expired",
    "adapter_unavailable",
    "atomicity_unavailable",
    "commit_ambiguous",
    "operation_failed",
]

SECURITY = {
    key: False
    for key in (
        "adapterImplementationAllowed",
        "adapterInvocationAllowed",
        "authorizationConsumptionAllowed",
        "authorizationGrantAllowed",
        "authorizationTokenAllowed",
        "registryReadAllowed",
        "registryWriteAllowed",
        "atomicCompareAndSetAllowed",
        "reconciliationReadAllowed",
        "trustedClockReadAllowed",
        "processEnvironmentReadAllowed",
        "filesystemReadAllowed",
        "filesystemMutationAllowed",
        "processExecutionAllowed",
        "networkExecutionAllowed",
        "driverImportAllowed",
        "databaseConnectionAllowed",
        "passwordAllowed",
        "databaseUrlAllowed",
        "connectionStringAllowed",
        "serviceRoleKeyAllowed",
        "productionSecretAllowed",
        "realParticipantDataAllowed",
        "frontendReferenceAllowed",
    )
}

EXPECTED_FACTS = {
    "sourceVersion": "v27.32u",
    "sourceStatus": (
        "planned_atomic_consumption_registry_adapter_"
        "fully_locked_not_implemented"
    ),
    "adapterCapabilities": {
        "kind": "single_use_consumption_registry",
        "requiredCapability": (
            "atomic_compare_and_set_with_consumption_record"
        ),
        "expectedState": "unused",
        "desiredState": "consumed",
        "singleAdapterCallRequired": True,
        "maximumParallelWinners": 1,
        "adapterInvocationAllowed": False,
    },
    "timeouts": {
        "operationTimeoutMilliseconds": 15000,
        "connectTimeoutMilliseconds": 3000,
        "statementTimeoutMilliseconds": 5000,
        "lockTimeoutMilliseconds": 2000,
        "timeoutAutomaticRetryAllowed": False,
    },
    "results": {
        "exactResultKinds": RESULT_KINDS,
        "executionGrant": False,
    },
    "reconciliation": {
        "ambiguousCommitTerminalForAutomaticRetry": True,
        "automaticRetryAfterAmbiguousAllowed": False,
        "reconciliationRequired": True,
        "reconciliationMayReadByOperationIdLater": True,
        "reconciliationMayWriteAllowed": False,
        "assumeCommittedAllowed": False,
        "assumeUnusedAllowed": False,
    },
    "security": SECURITY,
}


def _clone(value):
    if isinstance(value, Mapping):
        return {
            key: _clone(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [_clone(item) for item in value]

    return value


def _result(status: str, reason: str, descriptor=None):
    result = {
        "status": status,
        "reason": reason,
        "executionGrant": False,
    }

    for key, value in SECURITY.items():
        result[key] = value

    if descriptor is not None:
        result["descriptor"] = descriptor

    return result


def _blocked(reason: str):
    return _result("blocked", reason)


def resolve_atomic_consumption_registry_adapter_descriptor(facts):
    if not isinstance(facts, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "invalid_input"
        )

    if set(facts) != set(EXPECTED_FACTS):
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "structure_invalid"
        )

    for key, expected in EXPECTED_FACTS.items():
        if facts.get(key) != expected:
            return _blocked(
                "atomic_consumption_registry_adapter_descriptor_"
                f"{key}_invalid"
            )

    descriptor = {
        "version": 1,
        "sourceVersion": EXPECTED_FACTS["sourceVersion"],
        "sourceStatus": EXPECTED_FACTS["sourceStatus"],
        "adapterCapabilities": _clone(
            EXPECTED_FACTS["adapterCapabilities"]
        ),
        "timeouts": _clone(EXPECTED_FACTS["timeouts"]),
        "results": _clone(EXPECTED_FACTS["results"]),
        "reconciliation": _clone(
            EXPECTED_FACTS["reconciliation"]
        ),
        "security": _clone(EXPECTED_FACTS["security"]),
        "executionGrant": False,
    }

    return _result(
        (
            "atomic_consumption_registry_adapter_descriptor_"
            "ready_execution_locked"
        ),
        (
            "authorization_atomic_consumption_registry_adapter_"
            "descriptor_ready_execution_locked"
        ),
        descriptor,
    )
