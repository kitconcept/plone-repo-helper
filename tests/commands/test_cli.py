from plone_repo_helper import __version__
from plone_repo_helper.cli import app
from typer.testing import CliRunner


runner = CliRunner()


def test_cli_option_version(test_public_project, bust_path_cache):
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert f"plone_repo_helper {__version__}" in result.stdout
