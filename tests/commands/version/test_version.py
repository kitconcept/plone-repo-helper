from plone_repo_helper.cli import app
from typer.testing import CliRunner


runner = CliRunner()


def test_version(caplog, test_public_project):
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    messages = result.stdout.split("\n")
    assert "Repository: 1.0.0a0" in messages
    assert "fake.distribution (Backend): 1.0.0a0" in messages
    assert "fake-distribution (Frontend): 1.0.0-alpha.0" in messages
