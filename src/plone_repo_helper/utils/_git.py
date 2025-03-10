from git import Repo
from git import Tag
from pathlib import Path
from plone_repo_helper import logger


def _initialize_repo_for_project(path: Path) -> Repo:
    """Return the repository for a project."""
    repo = Repo.init(path)
    return repo


def repo_for_project(path: Path) -> Repo:
    """Return the repository for a project."""
    repo = Repo(path)
    return repo


def push_changes(repo: Repo, ref: Tag | None = None):
    origin = repo.remote("origin")
    if not origin:
        logger.info("No origin for this repo")
        return
    if ref:
        origin.push(ref)
    else:
        origin.push()


def commit_pending_changes(repo: Repo, message: str):
    git_cmd = repo.git
    git_cmd.commit("-am", message)


def repo_has_version(repo: Repo, version: str) -> bool:
    # Fetch existing tags
    origin = repo.remote("origin")
    if origin:
        origin.fetch()
    # List tags
    tags: list[Tag] = repo.tags
    names = [tag.name for tag in tags]
    return bool(version in names)


def create_version_tag(repo: Repo, version: str, message: str) -> Tag:
    # Create tag
    tag = repo.create_tag(version, message=message)
    # Push tag
    push_changes(repo, tag)
    return tag


def finish_release(repo: Repo, version: str) -> Tag:
    message = f"Release {version}"
    commit_pending_changes(repo, message)
    tag = create_version_tag(repo, version, message)
    push_changes(repo)
    return tag
