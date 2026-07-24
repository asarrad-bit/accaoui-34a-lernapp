from __future__ import annotations

from collections.abc import Mapping


SECURITY_KEYS = (
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

TOP_LEVEL_KEYS = frozenset({
    "status",
    "reason",
    "executionGrant",
    "descriptor",
    *SECURITY_KEYS,
})

DESCRIPTOR_KEYS = frozenset({
    "version",
    "sourceVersion",
    "sourceStatus",
    "adapterCapabilities",
    "timeouts",
    "results",
    "reconciliation",
    "security",
    "executionGrant",
})

EXPECTED_ADAPTER = {
    "kind": "single_use_consumption_registry",
    "requiredCapability": (
        "atomic_compare_and_set_with_consumption_record"
    ),
    "expectedState": "unused",
    "desiredState": "consumed",
    "singleAdapterCallRequired": True,
    "maximumParallelWinners": 1,
    "adapterInvocationAllowed": False,
}

EXPECTED_TIMEOUTS = {
    "operationTimeoutMilliseconds": 15000,
    "connectTimeoutMilliseconds": 3000,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
    "timeoutAutomaticRetryAllowed": False,
}

EXPECTED_RESULTS = {
    "exactResultKinds": [
        "committed",
        "already_consumed",
        "parallel_conflict",
        "binding_conflict",
        "expired",
        "adapter_unavailable",
        "atomicity_unavailable",
        "commit_ambiguous",
        "operation_failed",
    ],
    "executionGrant": False,
}

EXPECTED_RECONCILIATION = {
    "ambiguousCommitTerminalForAutomaticRetry": True,
    "automaticRetryAfterAmbiguousAllowed": False,
    "reconciliationRequired": True,
    "reconciliationMayReadByOperationIdLater": True,
    "reconciliationMayWriteAllowed": False,
    "assumeCommittedAllowed": False,
    "assumeUnusedAllowed": False,
}

EXPECTED_SECURITY = {
    key: False
    for key in SECURITY_KEYS
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


def _result(
    status: str,
    reason: str,
    accepted: bool,
    accepted_descriptor=None,
):
    result = {
        "status": status,
        "reason": reason,
        "accepted": accepted,
        "acceptedDescriptor": accepted_descriptor,
        "executionGrant": False,
    }

    for key in SECURITY_KEYS:
        result[key] = False

    return result


def _blocked(reason: str):
    return _result("blocked", reason, False)


def accept_atomic_consumption_registry_adapter_descriptor(candidate):
    if not isinstance(candidate, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_invalid_input"
        )

    source = dict(candidate)

    if set(source) != TOP_LEVEL_KEYS:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_structure_invalid"
        )

    if source["status"] != (
        "atomic_consumption_registry_adapter_descriptor_"
        "ready_execution_locked"
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_source_status_invalid"
        )

    if source["reason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "descriptor_ready_execution_locked"
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_source_reason_invalid"
        )

    if source["executionGrant"] is not False:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_source_boundary_open"
        )

    for key in SECURITY_KEYS:
        if source[key] is not False:
            return _blocked(
                "atomic_consumption_registry_adapter_descriptor_"
                "acceptance_source_boundary_open"
            )

    descriptor = source["descriptor"]

    if not isinstance(descriptor, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_invalid"
        )

    data = dict(descriptor)

    if set(data) != DESCRIPTOR_KEYS:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_structure_invalid"
        )

    if data["version"] != 1:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_version_invalid"
        )

    if (
        data["sourceVersion"] != "v27.32u"
        or data["sourceStatus"] != (
            "planned_atomic_consumption_registry_adapter_"
            "fully_locked_not_implemented"
        )
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_source_invalid"
        )

    if data["adapterCapabilities"] != EXPECTED_ADAPTER:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_adapter_invalid"
        )

    if data["timeouts"] != EXPECTED_TIMEOUTS:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_timeouts_invalid"
        )

    if data["results"] != EXPECTED_RESULTS:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_results_invalid"
        )

    if data["reconciliation"] != EXPECTED_RECONCILIATION:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_reconciliation_invalid"
        )

    if data["security"] != EXPECTED_SECURITY:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_security_invalid"
        )

    if data["executionGrant"] is not False:
        return _blocked(
            "atomic_consumption_registry_adapter_descriptor_"
            "acceptance_descriptor_execution_invalid"
        )

    canonical = {
        "version": 1,
        "sourceVersion": "v27.32u",
        "sourceStatus": (
            "planned_atomic_consumption_registry_adapter_"
            "fully_locked_not_implemented"
        ),
        "adapterCapabilities": _clone(EXPECTED_ADAPTER),
        "timeouts": _clone(EXPECTED_TIMEOUTS),
        "results": _clone(EXPECTED_RESULTS),
        "reconciliation": _clone(EXPECTED_RECONCILIATION),
        "security": _clone(EXPECTED_SECURITY),
        "executionGrant": False,
    }

    return _result(
        (
            "accepted_atomic_consumption_registry_adapter_"
            "descriptor_execution_locked"
        ),
        (
            "authorization_atomic_consumption_registry_adapter_"
            "descriptor_accepted_execution_locked"
        ),
        True,
        canonical,
    )
