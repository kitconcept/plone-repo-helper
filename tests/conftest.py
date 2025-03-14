from pathlib import Path

import pytest
import shutil
import tomlkit


RESOURCES = Path(__file__).parent / "_resources"


@pytest.fixture
def test_dir(monkeypatch, tmp_path) -> Path:
    monkeypatch.chdir(tmp_path)
    return tmp_path


@pytest.fixture
def get_resource_file():
    def func(name: str) -> Path:
        return RESOURCES / name

    return func


@pytest.fixture
def toml_parse():
    def func(path: Path) -> dict:
        return tomlkit.parse(path.read_text())

    return func


@pytest.fixture
def update_pyproject():
    from plone_repo_helper.utils.dependencies import update_pyproject

    def func(path: Path, version: str, constraints: list[str]) -> dict:
        update_pyproject(path, version, constraints)

    return func


@pytest.fixture
def test_project(monkeypatch, tmp_path):
    src = RESOURCES / "fake_distribution"
    dst = tmp_path / "fake_distribution"
    shutil.copytree(src, dst)
    monkeypatch.chdir(dst)
    return dst


@pytest.fixture
def bust_path_cache():
    from plone_repo_helper.utils import _path

    for name in ("get_root_path",):
        func = getattr(_path, name)
        func.cache_clear()


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "ignore_localhost": True,
        "record_mode": "once",
    }


@pytest.fixture(scope="session")
def vcr_cassette_dir(request):
    return str(RESOURCES / "vcr")


@pytest.fixture
def settings(test_project):
    from plone_repo_helper import settings

    return settings.get_settings()
