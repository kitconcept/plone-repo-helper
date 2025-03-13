import pytest


@pytest.fixture
def pyproject_toml(test_public_project):
    return test_public_project / "backend" / "pyproject.toml"
