from plone_repo_helper import logger
from plone_repo_helper import utils
from plone_repo_helper.utils import dependencies
from typing import Annotated

import typer


app = typer.Typer()


@app.command()
def check(ctx: typer.Context):
    """Upgrade Products.CMFPlone to a newer version."""
    settings = ctx.obj.settings
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
    logger.info(f"Getting Plone constraints for version {version}")
    constraints = dependencies.get_plone_constraints(version)
    pyproject = utils.get_pyproject(settings)
    if pyproject:
        logger.info(f"Updating {pyproject} dependencies and constraints")
        dependencies.update_pyproject(pyproject, version, constraints)
        logger.info("Done")
    else:
        logger.info("No pyproject.toml found")
