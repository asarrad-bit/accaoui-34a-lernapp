from __future__ import annotations

from collections.abc import Mapping
from typing import Any


def build_connection_adapter_readiness(
    gate_result: Mapping[str, object],
) -> dict[str, Any]:
    if not isinstance(gate_result, Mapping):
        return {
            "status": "blocked",
            "reason": "gate_result_invalid",
            "descriptor": None,
            "driverSelected": False,
            "connectionAllowed": False,
            "connectionCreated": False,
        }

    decision = gate_result.get("decision")
    reason = gate_result.get("reason")
    descriptor = gate_result.get("descriptor")
    connection_allowed = gate_result.get("connectionAllowed")

    if (
        decision != "eligible_but_connection_locked"
        or reason != "adapter_not_implemented"
        or not isinstance(descriptor, Mapping)
        or connection_allowed is not False
    ):
        return {
            "status": "blocked",
            "reason": (
                reason
                if isinstance(reason, str) and reason
                else "environment_gate_denied"
            ),
            "descriptor": None,
            "driverSelected": False,
            "connectionAllowed": False,
            "connectionCreated": False,
        }

    expected_descriptor_keys = {
        "mode",
        "targetKind",
        "host",
        "port",
        "database",
    }

    if set(descriptor.keys()) != expected_descriptor_keys:
        return {
            "status": "blocked",
            "reason": "validated_descriptor_invalid",
            "descriptor": None,
            "driverSelected": False,
            "connectionAllowed": False,
            "connectionCreated": False,
        }

    return {
        "status": "descriptor_valid_connection_locked",
        "reason": "database_driver_not_selected",
        "descriptor": dict(descriptor),
        "driverSelected": False,
        "connectionAllowed": False,
        "connectionCreated": False,
    }
