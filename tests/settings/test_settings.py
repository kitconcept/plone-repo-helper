from pathlib import Path
from plone_repo_helper import _types as t
from plone_repo_helper import settings

import pytest


@pytest.mark.parametrize(
    "attr,expected",
    [
        ["name", str],
        ["root_path", Path],
        ["backend", t.Package],
        ["frontend", t.Package],
        ["version_path", Path],
        ["compose_path", Path],
        ["towncrier", t.TowncrierSettings],
        ["changelogs", t.Changelogs],
    ],
)
def test_get_settings(test_project, bust_path_cache, attr: str, expected):
    result = settings.get_settings()
    assert isinstance(result, t.RepositorySettings)
    settings_atts = getattr(result, attr)
    assert isinstance(settings_atts, expected)


def test_settings_sanity(test_project, bust_path_cache):
    result = settings.get_settings()
    assert isinstance(result, t.RepositorySettings)
    assert result.sanity() is True
