from ._hatch import get_hatch
from ._path import change_cwd
from .changelog import update_backend_changelog
from plone_repo_helper import _types as t

import subprocess


def release_backend(settings: t.RepositorySettings, version: str, dry_run: bool):
    hatch = get_hatch()
    if not dry_run:
        update_backend_changelog(settings, dry_run, version)
    with change_cwd(settings.backend.path):
        # Build package
        hatch("build")
        if not dry_run:
            hatch("publish")


def release_frontend(settings: t.RepositorySettings, version: str, dry_run: bool):
    action = "dry-release" if dry_run else "release"
    volto_addon_name = settings.frontend.name
    cmd = (
        f"pnpm --filter {volto_addon_name} {action} "
        f"--ci --no-git --no-github.release -i {version}"
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
