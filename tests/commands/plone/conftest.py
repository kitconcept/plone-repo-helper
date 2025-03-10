import pytest


@pytest.fixture
def pyproject_toml(test_project):
    return test_project / "backend" / "pyproject.toml"
