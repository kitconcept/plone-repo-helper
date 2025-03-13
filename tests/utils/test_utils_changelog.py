from plone_repo_helper.utils import changelog

import pytest


@pytest.fixture
def settings(test_public_project, bust_path_cache):
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
def test_update_changelog_draft(settings, version: str):
    func = changelog.update_changelog
    new_entries, fullchangelog = func(settings=settings, draft=True, version=version)
    assert f"## {version} (" in fullchangelog
    assert f"## {version} (" in new_entries
    assert "### Backend" in new_entries
    assert "### Frontend" in new_entries


@pytest.mark.parametrize(
    "version",
    [
        "1.0.0a1",
        "1.0.0b1",
        "1.0.0rc1",
        "1.0.0",
    ],
)
def test_update_changelog(settings, version: str):
    old_project_changelog = settings.changelogs.root.read_text()
    func = changelog.update_changelog
    new_entries, _ = func(settings=settings, draft=False, version=version)
    new_project_changelog = settings.changelogs.root.read_text()
    assert old_project_changelog != new_project_changelog
    assert new_entries in new_project_changelog
    assert f"## {version} (" in new_project_changelog
    assert f"## {version} (" in new_entries
    assert "### Backend" in new_entries
    assert "### Frontend" in new_entries


@pytest.mark.parametrize(
    "version,draft",
    [
        ["1.0.0a1", True],
        ["1.0.0b1", True],
        ["1.0.0rc1", True],
        ["1.0.0", True],
        ["1.0.0a1", False],
        ["1.0.0b1", False],
        ["1.0.0rc1", False],
        ["1.0.0", False],
    ],
)
def test_update_backend_changelog(settings, version: str, draft: bool):
    old_changelog = settings.backend.changelog.read_text()
    func = changelog.update_backend_changelog
    result = func(settings=settings, draft=draft, version=version)
    new_changelog = settings.backend.changelog.read_text()
    if draft:
        assert old_changelog == new_changelog
        assert result not in new_changelog
    else:
        assert old_changelog != new_changelog
        assert "Done" in result
