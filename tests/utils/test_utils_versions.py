from plone_repo_helper.utils import _path
from plone_repo_helper.utils import versions

import pytest


@pytest.mark.parametrize(
    "python_version,expected",
    [
        ["1.0.0a0", "1.0.0-alpha.0"],
        ["1.0.0b1", "1.0.0-beta.1"],
        ["1.0.0rc1", "1.0.0-rc.1"],
        ["1.0.0", "1.0.0"],
    ],
)
def test_convert_python_node_version(python_version: str, expected: str):
    func = versions.convert_python_node_version
    result = func(python_version)
    assert result == expected


def test_get_current_backend_version(test_project, bust_path_cache):
    backend_path = _path.get_root_path() / "backend"
    func = versions.get_current_backend_version
    result = func(backend_path)
    assert result == "1.0.0a0"


@pytest.mark.parametrize(
    "version,expected",
    [
        ["1.0.0a1", "1.0.0a1"],
        ["1.0.0b1", "1.0.0b1"],
        ["1.0.0rc1", "1.0.0rc1"],
        ["1.0.0", "1.0.0"],
    ],
)
def test_update_backend_version(
    test_project, bust_path_cache, version: str, expected: str
):
    backend_path = _path.get_root_path() / "backend"
    func = versions.update_backend_version
    result = func(backend_path, version)
    assert result == expected
