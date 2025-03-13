from collections.abc import Callable
from dynaconf import Dynaconf
from dynaconf.utils.boxing import DynaBox
from pathlib import Path
from plone_repo_helper import _types as t
from plone_repo_helper.utils import versions


PYPROJECT_TOML = "pyproject.toml"


def get_changelogs(
    root_changelog: Path, backend: t.Package, frontend: t.Package
) -> t.Changelogs:
    return t.Changelogs(root_changelog, backend.changelog, frontend.changelog)


def get_towncrier_settings(
    backend: t.Package, frontend: t.Package
) -> t.TowncrierSettings:
    return t.TowncrierSettings(backend=backend.towncrier, frontend=frontend.towncrier)


def get_pyproject(settings: t.RepositorySettings) -> Path | None:
    """Return the pyproject.toml for a monorepo."""
    paths = [
        settings.root_path,
        settings.backend.path,
    ]
    for base_path in paths:
        path = base_path / PYPROJECT_TOML
        if path.exists():
            return path
    return None


def get_next_version(settings: t.RepositorySettings) -> str:
    version_file = settings.version_path
    cur_version = version_file.read_text().strip()
    next_version = cur_version.replace(".dev", "")
    return next_version


def _get_package_info(
    root_path: Path, package_settings: DynaBox, version_func: Callable
) -> t.Package:
    """Return package information for the frontend."""
    path = (root_path / package_settings.path).resolve()
    changelog = (root_path / package_settings.changelog).resolve()
    towncrier = (root_path / package_settings.towncrier_settings).resolve()
    version = version_func(path)
    publish = bool(package_settings.get("publish", True))
    return t.Package(
        name=package_settings.name,
        path=path,
        version=version,
        publish=publish,
        changelog=changelog,
        towncrier=towncrier,
    )


def get_backend(root_path: Path, raw_settings: Dynaconf) -> t.Package:
    """Return package information for the backend."""
    package_settings = raw_settings.backend.package
    version_func = versions.get_backend_version
    return _get_package_info(root_path, package_settings, version_func)


def get_frontend(root_path: Path, raw_settings: Dynaconf) -> t.Package:
    """Return package information for the frontend."""
    package_settings = raw_settings.frontend.package
    version_func = versions.get_frontend_version
    return _get_package_info(root_path, package_settings, version_func)
