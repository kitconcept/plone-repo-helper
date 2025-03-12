from plone_repo_helper import _types as t
from plone_repo_helper.utils import _git as gitutils
from plone_repo_helper.utils import changelog as chgutils
from plone_repo_helper.utils import release as utils
from plone_repo_helper.utils import versions as vutils
from typing import Annotated

import typer


app = typer.Typer()


def _get_next_version(
    settings: t.RepositorySettings, original_version: str, desired_version: str
) -> tuple[str, str]:
    next_version = ""
    error = ""
    try:
        next_version = vutils.next_version(desired_version, original_version)
    except ValueError:
        next_version = ""
        error = "Invalid version."
    else:
        if not utils.valid_next_version(settings, next_version):
            error = f"The version {next_version} already exists as a tag in Git"
            next_version = ""
    return next_version, error


def _prepare_changelog(
    settings: t.RepositorySettings,
    original_version: str,
    next_version: str,
    dry_run: bool,
) -> bool:
    # Changelog
    ## First display the changelog
    new_entries, _ = chgutils.update_changelog(
        settings, draft=True, version=next_version
    )
    typer.echo(f"{'=' * 50}\n{new_entries}\n{'=' * 50}")

    status: bool = typer.confirm("Should we proceed?", default=True)
    if not (status):
        typer.echo("Exiting now")
    return status


def _update_repository(
    settings: t.RepositorySettings,
    original_version: str,
    next_version: str,
    dry_run: bool,
):
    if not dry_run:
        chgutils.update_changelog(settings, draft=dry_run, version=next_version)
        typer.echo(f"Updated {settings.changelogs.root} file")
    # Update next_version on version.txt
    version_file = settings.version_path
    version_file.write_text(f"{next_version}\n")
    typer.echo(f"Updated {version_file} file")
    # Update docker-compose.yml
    compose_file = settings.compose_path
    contents = compose_file.read_text().replace(original_version, next_version)
    compose_file.write_text(contents)
    typer.echo(f"Updated {compose_file} file")


def _release_backend(
    settings: t.RepositorySettings,
    original_version: str,
    next_version: str,
    dry_run: bool,
):
    typer.echo(f"Backend release {original_version} -> {next_version}")
    backend_path = settings.backend.path
    vutils.update_backend_version(backend_path, next_version)
    utils.release_backend(settings, next_version, dry_run)


def _release_frontend(
    settings: t.RepositorySettings,
    original_version: str,
    next_version: str,
    dry_run: bool,
):
    typer.echo(f"Frontend release {original_version} -> {next_version}")
    utils.release_frontend(settings, next_version, dry_run)


def _update_git(
    settings: t.RepositorySettings,
    original_version: str,
    next_version: str,
    dry_run: bool,
):
    if not dry_run:
        typer.echo(f"Creating tag {next_version}")
        repo = gitutils.repo_for_project(settings.root_path)
        gitutils.finish_release(repo, next_version)


@app.command()
def do(
    ctx: typer.Context,
    desired_version: Annotated[
        str,
        typer.Argument(
            help=(
                "Next version. Could be the version number, or "
                "a segment like: a, minor, major, rc"
            )
        ),
    ],
    dry_run: Annotated[bool, typer.Option(help="Is this a dry run?")] = False,
):
    """Release the packages in this mono repo."""
    settings: t.RepositorySettings = ctx.obj.settings
    original_version = settings.version
    next_version, error = _get_next_version(settings, original_version, desired_version)
    if error:
        typer.echo(error)
        typer.Exit(0)
        return
    typer.echo(f"Bump version from {original_version} to {next_version}")

    # Changelog
    proceed = _prepare_changelog(settings, original_version, next_version, dry_run)
    if not (proceed):
        typer.Exit(0)
        return

    # Update repository components
    _update_repository(settings, original_version, next_version, dry_run)

    # Release backend
    _release_backend(settings, original_version, next_version, dry_run)

    # Release frontend
    _release_frontend(settings, original_version, next_version, dry_run)

    # Commit changes, create tag
    _update_git(settings, original_version, next_version, dry_run)

    # Finish
    typer.echo(f"Completed the release of version {next_version}")


@app.command()
def changelog(
    ctx: typer.Context,
):
    """Generate a draft of the final changelog."""
    settings: t.RepositorySettings = ctx.obj.settings
    original_version = settings.version
    # Changelog
    new_entries, _ = chgutils.update_changelog(
        settings, draft=True, version=original_version
    )
    typer.echo(f"{'=' * 50}\n{new_entries}\n{'=' * 50}")
