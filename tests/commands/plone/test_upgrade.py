from plone_repo_helper.cli import app
from typer.testing import CliRunner

import pytest


runner = CliRunner()


@pytest.mark.parametrize(
    "version",
    [
        "6.1.0rc1",
        "6.1.0",
    ],
)
@pytest.mark.vcr
def test_upgrade(pyproject_toml, bust_path_cache, toml_parse, version: str):
    result = runner.invoke(app, ["plone", "upgrade", version])
    assert result.exit_code == 0
    data = toml_parse(pyproject_toml)
    assert f"Products.CMFPlone=={version}" in data["project"]["dependencies"]
    tool_uv = data["tool"]["uv"]
    assert "constraint-dependencies" in tool_uv
    assert f"Products.CMFPlone=={version}" in tool_uv["constraint-dependencies"]
