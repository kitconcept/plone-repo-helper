from plone_repo_helper.utils import changelog

import pytest


@pytest.fixture
def settings(test_project):
    from plone_repo_helper.settings import get_settings

    return get_settings()


@pytest.mark.parametrize(
    "version",
    [
        "1.0.0a1",
        "1.0.0b1",
        "1.0.0rc1",
        "1.0.0",
    ],
)
def test_update_changelog_draft(settings, bust_path_cache, version: str):
    func = changelog.update_changelog
    result = func(settings=settings, draft=True, version=version)
    assert f"## {version} (" in result
    assert "### Backend" in result
    assert "### Frontend" in result


@pytest.mark.parametrize(
    "version",
    [
        "1.0.0a1",
        "1.0.0b1",
        "1.0.0rc1",
        "1.0.0",
    ],
)
def test_update_changelog(settings, bust_path_cache, version: str):
    old_project_changelog = settings.changelogs.root.read_text()
    func = changelog.update_changelog
    result = func(settings=settings, draft=False, version=version)
    new_project_changelog = settings.changelogs.root.read_text()
    assert old_project_changelog != new_project_changelog
    assert result == new_project_changelog
    assert f"## {version} (" in new_project_changelog
    assert "### Backend" in new_project_changelog
    assert "### Frontend" in new_project_changelog
