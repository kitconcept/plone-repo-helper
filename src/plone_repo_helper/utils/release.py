from ._git import repo_for_project
from ._git import repo_has_version
from ._hatch import get_hatch
from ._path import change_cwd
from .changelog import update_backend_changelog
from .versions import convert_python_node_version
from plone_repo_helper import _types as t
from plone_repo_helper import logger

import subprocess


def release_backend(settings: t.RepositorySettings, version: str, dry_run: bool):
    hatch = get_hatch()
    if not dry_run:
        update_backend_changelog(settings, dry_run, version)
    with change_cwd(settings.backend.path):
        logger.info(f"Build backend package {settings.backend.name}")
        # Build package
        hatch("build")
        if not dry_run:
            logger.info(f"Publish backend package {settings.backend.name}")
            hatch("publish")


def release_frontend(settings: t.RepositorySettings, version: str, dry_run: bool):
    sem_version: str = convert_python_node_version(version)
    action = "dry-release" if dry_run else "release"
    logger.info(
        f"Do a {action} for frontend package {settings.frontend.name} ({sem_version})"
    )
    volto_addon_name = settings.frontend.name
    cmd = (
        f"pnpm --filter {volto_addon_name} {action} "
        f"--ci --no-git --no-github.release -i {sem_version}"
    )
    result = subprocess.run(  # noQA: S602
        cmd,
        capture_output=True,
        text=True,
        shell=True,
        cwd=settings.frontend.path,
    )
    if result.returncode:
        raise RuntimeError(f"Frontend release failed {result.stderr}")


def valid_next_version(settings: t.RepositorySettings, next_version: str) -> bool:
    """Check if next version is valid."""
    is_valid = True
    repo = repo_for_project(settings.root_path)
    if repo:
        is_valid = not (repo_has_version(repo, next_version))
    return is_valid
