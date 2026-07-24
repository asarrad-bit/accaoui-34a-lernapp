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

INPUT_KEYS = frozenset({
    "acceptedDescriptorResult",
    "adapterFacts",
})

SOURCE_RESULT_KEYS = frozenset({
    "status",
    "reason",
    "accepted",
    "acceptedDescriptor",
    "executionGrant",
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


def _clone(value):
    if isinstance(value, Mapping):
        return {
            key: _clone(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [_clone(item) for item in value]

    return value


def _result(status: str, reason: str, readiness=None):
    result = {
        "status": status,
        "reason": reason,
        "ready": readiness is not None,
        "readiness": readiness,
        "executionGrant": False,
    }

    for key in SECURITY_KEYS:
        result[key] = False

    return result


def _blocked(reason: str):
    return _result("blocked", reason)


def resolve_atomic_consumption_registry_adapter_readiness(value):
    if not isinstance(value, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "invalid_input"
        )

    source = dict(value)

    if set(source) != INPUT_KEYS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "structure_invalid"
        )

    accepted = source["acceptedDescriptorResult"]

    if not isinstance(accepted, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "accepted_descriptor_invalid"
        )

    accepted_data = dict(accepted)

    if set(accepted_data) != SOURCE_RESULT_KEYS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "accepted_descriptor_structure_invalid"
        )

    if accepted_data["status"] != (
        "accepted_atomic_consumption_registry_adapter_"
        "descriptor_execution_locked"
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "accepted_descriptor_status_invalid"
        )

    if accepted_data["reason"] != (
        "authorization_atomic_consumption_registry_adapter_"
        "descriptor_accepted_execution_locked"
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "accepted_descriptor_reason_invalid"
        )

    if accepted_data["accepted"] is not True:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "accepted_descriptor_flag_invalid"
        )

    if accepted_data["executionGrant"] is not False:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "accepted_descriptor_boundary_open"
        )

    for key in SECURITY_KEYS:
        if accepted_data[key] is not False:
            return _blocked(
                "atomic_consumption_registry_adapter_readiness_"
                "accepted_descriptor_boundary_open"
            )

    descriptor = accepted_data["acceptedDescriptor"]

    if not isinstance(descriptor, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_invalid"
        )

    descriptor_data = dict(descriptor)

    if set(descriptor_data) != DESCRIPTOR_KEYS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_structure_invalid"
        )

    if descriptor_data["version"] != 1:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_version_invalid"
        )

    if (
        descriptor_data["sourceVersion"] != "v27.32u"
        or descriptor_data["sourceStatus"] != (
            "planned_atomic_consumption_registry_adapter_"
            "fully_locked_not_implemented"
        )
    ):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_source_invalid"
        )

    if descriptor_data["adapterCapabilities"] != EXPECTED_ADAPTER:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_adapter_invalid"
        )

    if descriptor_data["timeouts"] != EXPECTED_TIMEOUTS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_timeouts_invalid"
        )

    if descriptor_data["results"] != EXPECTED_RESULTS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_results_invalid"
        )

    if descriptor_data["reconciliation"] != EXPECTED_RECONCILIATION:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_reconciliation_invalid"
        )

    if descriptor_data["security"] != EXPECTED_SECURITY:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_security_invalid"
        )

    if descriptor_data["executionGrant"] is not False:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "descriptor_execution_invalid"
        )

    facts = source["adapterFacts"]

    if not isinstance(facts, Mapping):
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "adapter_facts_invalid"
        )

    if dict(facts) != EXPECTED_ADAPTER_FACTS:
        return _blocked(
            "atomic_consumption_registry_adapter_readiness_"
            "adapter_facts_invalid"
        )

    readiness = {
        "version": 1,
        "sourceStatus": accepted_data["status"],
        "sourceReason": accepted_data["reason"],
        "descriptor": _clone(descriptor_data),
        "adapterFacts": _clone(EXPECTED_ADAPTER_FACTS),
        "adapterImplementationAllowed": False,
        "adapterInvocationAllowed": False,
        "registryReadAllowed": False,
        "registryWriteAllowed": False,
        "atomicCompareAndSetAllowed": False,
        "authorizationConsumptionAllowed": False,
        "executionGrant": False,
    }

    return _result(
        (
            "atomic_consumption_registry_adapter_readiness_"
            "ready_execution_locked"
        ),
        (
            "authorization_atomic_consumption_registry_adapter_"
            "readiness_ready_execution_locked"
        ),
        readiness,
    )
