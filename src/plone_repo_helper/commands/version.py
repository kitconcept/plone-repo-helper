from plone_repo_helper import __version__
from plone_repo_helper import logger

import typer


app = typer.Typer()


@app.command()
def version(ctx: typer.Context):
    """Report version of this application."""
    logger.info(f"plone_repo_helper {__version__}")
