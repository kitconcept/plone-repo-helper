from plone_repo_helper import logger
from plone_repo_helper.utils import _git as gitutils
from plone_repo_helper.utils import changelog as chgutils
from plone_repo_helper.utils import release as utils
from plone_repo_helper.utils import versions as vutils
from typing import Annotated

import typer


app = typer.Typer()


@app.command()
def do(
    ctx: typer.Context,
    option: Annotated[
        str, typer.Argument(help="Which release type. a, minor, major, rc")
    ],
    dry_run: Annotated[bool, typer.Argument(help="Is this a dry run?")],
):
    """Release the packages in this mono repo."""
    settings = ctx.obj.settings
    backend_path = settings.backend.path
    cur_version = vutils.get_current_backend_version(backend_path)
    version = vutils.update_backend_version(backend_path, option)
    logger.info(f"Bumping version from {cur_version} to {version}")
    # Update version on version.txt
    version_file = settings.version_path
    version_file.write_text(f"{version}\n")
    logger.info(f"Updated {version_file} file")
    # Update docker-compose.yml
    compose_file = settings.compose_path
    contents = compose_file.read_text().replace(cur_version, version)
    compose_file.write_text(contents)
    logger.info(f"Updated {compose_file} file")
    # Changelog
    changelog = chgutils.update_changelog(settings, draft=dry_run, version=version)
    if dry_run:
        logger.info(f"{'=' * 50}\n{changelog}\n{'=' * 50}")
    else:
        logger.info(f"Updated {settings.changelogs.root} file")
    # Release backend
    utils.release_backend(settings, version, dry_run)
    # Release frontend
    utils.release_frontend(settings, version, dry_run)
    # Commit changes, create tag
    repo = gitutils.repo_for_project(settings.root_path)
    logger.info(f"Creating tag {version}")
    gitutils.finish_release(repo, version)
    logger.info(f"Release {version} complete")


@app.command()
def changelog(
    ctx: typer.Context,
):
    """Generate a draft of the final changelog."""
    settings = ctx.obj.settings
    backend_path = settings.backend.path
    version = vutils.get_current_backend_version(backend_path)
    # Changelog
    changelog = chgutils.update_changelog(settings, draft=True, version=version)
    logger.info(f"{'=' * 50}\n{changelog}\n{'=' * 50}")
