from .parser import raw_settings
from plone_repo_helper import _types as t
from plone_repo_helper import utils
from plone_repo_helper.utils._path import get_root_path


def get_settings() -> t.RepositorySettings:
    """Return base settings."""
    root_path = get_root_path()
    try:
        name = raw_settings.repository.name
    except AttributeError:
        raise RuntimeError() from None
    root_changelog = root_path / raw_settings.repository.changelog
    version_path = root_path / raw_settings.repository.version
    compose_path = root_path / raw_settings.repository.compose
    backend = utils.get_backend(root_path, raw_settings)
    frontend = utils.get_frontend(root_path, raw_settings)
    towncrier = utils.get_towncrier_settings(backend, frontend)
    changelogs = utils.get_changelogs(root_changelog, backend, frontend)
    return t.RepositorySettings(
        name=name,
        root_path=root_path,
        backend=backend,
        frontend=frontend,
        version_path=version_path,
        compose_path=compose_path,
        towncrier=towncrier,
        changelogs=changelogs,
    )
