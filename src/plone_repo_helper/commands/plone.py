from plone_repo_helper import _types as t
from plone_repo_helper import logger
from plone_repo_helper import utils
from plone_repo_helper.utils import dependencies
from typing import Annotated

import typer


app = typer.Typer()


@app.command()
def check(ctx: typer.Context):
    """Check latest version of Products.CMFPlone and compare to our current pinning."""
    settings: t.RepositorySettings = ctx.obj.settings
    if not settings.is_distribution:
        typer.echo("Only available for distributions based on Products.CMFPlone.")
        raise typer.Exit(1)
    pyproject = utils.get_pyproject(settings)
    current = dependencies.current_plone(pyproject) if pyproject else None
    if not current:
        logger.info(f"Products.CMFPlone is not present in {pyproject}")
    else:
        latest_version = dependencies.latest_plone_version()
        logger.info(f"Current version {current}, latest version {latest_version}")


@app.command()
def upgrade(
    ctx: typer.Context,
    version: Annotated[str, typer.Argument(help="New version of Products.CMFPlone")],
):
    """Upgrade Products.CMFPlone to a newer version."""
    settings = ctx.obj.settings
    if not settings.is_distribution:
        typer.echo("Only available for distributions based on Products.CMFPlone.")
        raise typer.Exit(1)
    logger.info(f"Getting Plone constraints for version {version}")
    constraints = dependencies.get_plone_constraints(version)
    pyproject = utils.get_pyproject(settings)
    if pyproject:
        logger.info(f"Updating {pyproject} dependencies and constraints")
        dependencies.update_pyproject(pyproject, version, constraints)
        # Update versions.txt
        backend_path = settings.backend.path
        version_file = (backend_path / "version.txt").resolve()
        version_file.write_text(f"{version}\n")
        logger.info("Done")
    else:
        logger.info("No pyproject.toml found")
