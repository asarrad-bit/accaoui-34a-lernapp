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

SOURCE_RESULT_KEYS = frozenset({
    "status",
    "reason",
    "ready",
    "readiness",
    "executionGrant",
    *SECURITY_KEYS,
})

READINESS_KEYS = frozenset({
    "version",
    "sourceStatus",
    "sourceReason",
    "descriptor",
    "adapterFacts",
    "adapterImplementationAllowed",
    "adapterInvocationAllowed",
    "registryReadAllowed",
    "registryWriteAllowed",
    "atomicCompareAndSetAllowed",
    "authorizationConsumptionAllowed",
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

EXPECTED_DESCRIPTOR = {
    "version": 1,
    "sourceVersion": "v27.32u",
    "sourceStatus": (
        "planned_atomic_consumption_registry_adapter_"
        "fully_locked_not_implemented"
    ),
    "adapterCapabilities": EXPECTED_ADAPTER,
    "timeouts": EXPECTED_TIMEOUTS,
    "results": EXPECTED_RESULTS,
    "reconciliation": EXPECTED_RECONCILIATION,
    "security": EXPECTED_SECURITY,
    "executionGrant": False,
}

EXPECTED_ADAPTER_FACTS = {
    "adapterKind": "single_use_consumption_registry",
    "adapterImplementationReportedAvailable": True,
    "requiredCapabilityReportedAvailable": True,
    "atomicCompareAndSetWithRecordReportedAvailable": True,
    "singleAdapterCallReportedSupported": True,
    "maximumParallelWinnersReported": 1,
    "exactResultKindsReportedSupported": list(
        EXPECTED_RESULTS["exactResultKinds"]
    ),
    "operationTimeoutMilliseconds": 15000,
    "connectTimeoutMilliseconds": 3000,
    "statementTimeoutMilliseconds": 5000,
    "lockTimeoutMilliseconds": 2000,
    "ambiguousCommitReconciliationReportedAvailable": True,
    "reconciliationReadByOperationIdReportedAvailable": True,
    "automaticRetryAfterAmbiguousAllowed": False,
    "rawErrorSuppressed": True,
    "adapterInvocationAllowed": False,
    "registryReadAllowed": False,
    "registryWriteAllowed": False,
    "atomicCompareAndSetAllowed": False,
    "authorizationConsumptionAllowed": False,
    "executionGrant": False,
}

EXPECTED_READINESS_EXECUTION = {
    "adapterImplementationAllowed": False,
    "adapterInvocationAllowed": False,
    "registryReadAllowed": False,
    "registryWriteAllowed": False,
    "atomicCompareAndSetAllowed": False,
    "authorizationConsumptionAllowed": False,
    "executionGrant": False,
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
    accepted_readiness=None,
):
    result = {
        "status": status,
        "reason": reason,
        "accepted": accepted,
        "acceptedReadiness": accepted_readiness,
        "executionGrant": False,
    }

    for key in SECURITY_KEYS:
        result[key] = False

    return result


def _blocked(reason: str):
    return _result("blocked", reason, False)


def accept_atomic_consumption_registry_adapter_readiness(candidate):
    if not isinstance(candidate, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_invalid_input"
        )

    source = dict(candidate)

    if set(source) != SOURCE_RESULT_KEYS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_structure_invalid"
        )

    if source["status"] != (
        "atomic_consumption_registry_adapter_readiness_"
        "ready_execution_locked"
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_source_status_invalid"
        )

    if source["reason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "readiness_ready_execution_locked"
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_source_reason_invalid"
        )

    if source["ready"] is not True:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_source_ready_invalid"
        )

    if source["executionGrant"] is not False:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_source_boundary_open"
        )

    for key in SECURITY_KEYS:
        if source[key] is not False:
            return _blocked(
                "atomic_consumption_registry_adapter_readiness_"
                "acceptance_source_boundary_open"
            )

    readiness = source["readiness"]

    if not isinstance(readiness, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_readiness_invalid"
        )

    data = dict(readiness)

    if set(data) != READINESS_KEYS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_readiness_structure_invalid"
        )

    if data["version"] != 1:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_readiness_version_invalid"
        )

    if (
        data["sourceStatus"] != (
            "accepted_atomic_consumption_registry_adapter_"
            "descriptor_execution_locked"
        )
        or data["sourceReason"] != (
            "authorization_atomic_consumption_registry_adapter_"
            "descriptor_accepted_execution_locked"
        )
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_readiness_source_invalid"
        )

    if data["descriptor"] != EXPECTED_DESCRIPTOR:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_readiness_descriptor_invalid"
        )

    if data["adapterFacts"] != EXPECTED_ADAPTER_FACTS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "acceptance_readiness_adapter_facts_invalid"
        )

    for key, expected in EXPECTED_READINESS_EXECUTION.items():
        if data[key] is not expected:
            return _blocked(
                "atomic_consumption_registry_adapter_readiness_"
                "acceptance_readiness_boundary_open"
            )

    canonical = {
        "version": 1,
        "sourceStatus": data["sourceStatus"],
        "sourceReason": data["sourceReason"],
        "descriptor": _clone(EXPECTED_DESCRIPTOR),
        "adapterFacts": _clone(EXPECTED_ADAPTER_FACTS),
        **EXPECTED_READINESS_EXECUTION,
    }

    return _result(
        (
            "accepted_atomic_consumption_registry_adapter_"
            "readiness_execution_locked"
        ),
        (
            "authorization_atomic_consumption_registry_adapter_"
            "readiness_accepted_execution_locked"
        ),
        True,
        canonical,
    )
