from __future__ import annotations

from importlib import metadata
from typing import Callable

DISTRIBUTION_NAME = "psycopg"
EXPECTED_VERSION = "3.3.4"
VersionReader = Callable[[str], str]

def resolve_driver_readiness(
    version_reader: VersionReader | None = None,
) -> dict[str, object]:
    reader = version_reader or metadata.version
    try:
        installed = reader(DISTRIBUTION_NAME)
    except metadata.PackageNotFoundError:
        return _result("blocked","driver_not_installed",None)
    except Exception:
        return _result("blocked","driver_metadata_unavailable",None)

    installed = str(installed).strip()
    if installed != EXPECTED_VERSION:
        return _result("blocked","driver_version_mismatch",installed)

    return _result(
        "metadata_ready_import_locked",
        "driver_import_not_authorized",
        installed,
    )

def _result(status: str, reason: str, installed: str | None):
    return {
        "status": status,
        "reason": reason,
        "distribution": DISTRIBUTION_NAME,
        "expectedVersion": EXPECTED_VERSION,
        "installedVersion": installed,
        "driverImportAttempted": False,
        "connectionAllowed": False,
    }
