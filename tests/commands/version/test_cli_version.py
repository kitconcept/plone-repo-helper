from plone_repo_helper import __version__
from plone_repo_helper.cli import app
from typer.testing import CliRunner

import logging


runner = CliRunner()


def test_cli_version(caplog):
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    with caplog.at_level(logging.INFO):
        messages = [record.message for record in caplog.records]
    assert f"plone_repo_helper {__version__}" in messages
