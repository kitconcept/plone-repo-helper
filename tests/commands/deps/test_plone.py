from plone_repo_helper.cli import app
from typer.testing import CliRunner

import logging
import pytest


runner = CliRunner()


@pytest.mark.parametrize("current_version", ["6.0.13", "6.1.0a1", "6.1.0a2"])
@pytest.mark.vcr
def test_check(
    caplog, bust_path_cache, pyproject_toml, update_pyproject, current_version: str
):
    update_pyproject(pyproject_toml, current_version, [])
    result = runner.invoke(app, ["deps", "plone", "check"])
    assert result.exit_code == 0
    with caplog.at_level(logging.INFO):
        messages = [record.message for record in caplog.records]
    assert f"Current version {current_version}, latest version 6.1.0" in messages


@pytest.mark.parametrize(
    "version",
    [
        "6.1.0rc1",
        "6.1.0",
    ],
)
@pytest.mark.vcr
def test_upgrade(pyproject_toml, bust_path_cache, toml_parse, version: str):
    result = runner.invoke(app, ["deps", "plone", "upgrade", version])
    assert result.exit_code == 0
    data = toml_parse(pyproject_toml)
    assert f"Products.CMFPlone=={version}" in data["project"]["dependencies"]
    tool_uv = data["tool"]["uv"]
    assert "constraint-dependencies" in tool_uv
    assert f"Products.CMFPlone=={version}" in tool_uv["constraint-dependencies"]
