from ._hatch import get_hatch
from ._path import change_cwd
from packaging.version import Version as PyPIVersion
from pathlib import Path

import re
import semver


VERSION_PATTERNS = (
    (r"^(a)(\d{1,2})", r"alpha.\2"),
    (r"^(b)(\d{1,2})", r"beta.\2"),
    (r"^(rc)(\d{1,2})", r"rc.\2"),
)


def convert_python_node_version(version: str) -> str:
    """Converts a PyPI version into a semver version

    :param ver: the PyPI version
    :return: a semver version
    :raises ValueError: if epoch or post parts are used
    """
    pypi_version = PyPIVersion(version)
    pre = None if not pypi_version.pre else "".join([str(i) for i in pypi_version.pre])
    if pre:
        for raw_pattern, replace in VERSION_PATTERNS:
            pattern = re.compile(raw_pattern)
            if re.search(pattern, pre):
                pre = re.sub(pattern, replace, pre)
        major, minor, patch = pypi_version.release
        version = str(
            semver.Version(major, minor, patch, prerelease=pre, build=pypi_version.dev)
        )
    return version


def get_current_backend_version(backend_path: Path) -> str:
    """Get the current version used by the backend."""
    hatch = get_hatch()
    with change_cwd(backend_path):
        result = hatch("version")
    return result.stdout.strip()


def update_backend_version(backend_path: Path, version: str) -> str:
    """Update version used by the backend.

    ref: https://hatch.pypa.io/1.12/version/#updating
    """
    hatch = get_hatch()
    with change_cwd(backend_path):
        result = hatch("version", version)
    if result.exit_code:
        raise RuntimeError("Error setting backend version")
    return get_current_backend_version(backend_path)
