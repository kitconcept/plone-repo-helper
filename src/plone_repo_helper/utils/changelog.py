from ._path import change_cwd
from click.testing import CliRunner
from datetime import datetime
from pathlib import Path
from plone_repo_helper import _types as t
from plone_repo_helper import utils
from towncrier._shell import cli as towncrier_app


CHANGELOG_PLACEHOLDER = "<!-- towncrier release notes start -->"


def _prepare_section_changelog(text: str) -> str:
    """Prepare section changelog to be added to the project changelog."""
    # Ignore version header
    lines = text.split("\n")
    for idx, line in enumerate(lines):
        if line.startswith("## "):
            idx += 1
            break
    text = "\n".join(lines[idx:])
    # Increase header levels
    text = text.replace("###", "####")
    return text


def _run_towncrier(config: Path, name: str, version: str, draft: bool = True) -> str:
    cwd = config.parent
    runner = CliRunner()
    args = [
        "build",
        "--config",
        f"{config}",
        "--yes",
        "--name",
        f"'{name}'",
        "--version",
        version,
        "--draft" if draft else "",
    ]
    with change_cwd(cwd):
        result = runner.invoke(towncrier_app, args)
    return result.stdout


def generate_section_changelogs(
    settings: t.RepositorySettings, version: str = ""
) -> dict[str, str]:
    sections = {}
    config = settings.towncrier
    for section, config_path in config.sections():
        result = _run_towncrier(
            config_path, name=settings.name, version=version, draft=True
        )
        sections[section] = _prepare_section_changelog(result)
    return sections


# Update Changelog at root
def _update_project_changelog(
    settings: t.RepositorySettings,
    sections: dict[str, str],
    draft: bool = True,
    version: str = "",
) -> tuple[str, str]:
    root_changelog = settings.changelogs.root
    changelog_text = root_changelog.read_text()
    header = f"## {version} ({datetime.now():%Y-%m-%d})"
    new_entry = f"{header}\n"
    for section_id, text in sections.items():
        new_entry = f"{new_entry}\n### {section_id}\n{text}"

    text = f"{changelog_text}".replace(
        CHANGELOG_PLACEHOLDER, f"{CHANGELOG_PLACEHOLDER}\n{new_entry}"
    )
    if not draft:
        root_changelog.write_text(text)
    return new_entry, text


def update_backend_changelog(
    settings: t.RepositorySettings, draft: bool = True, version: str = ""
) -> str:
    config_path = settings.towncrier.backend
    result = _run_towncrier(
        config_path, name=settings.name, version=version, draft=draft
    )
    return result


def update_changelog(
    settings: t.RepositorySettings, draft: bool = True, version: str = ""
) -> tuple[str, str]:
    if draft and not version:
        version = utils.get_next_version(settings)
    sections = generate_section_changelogs(settings=settings, version=version)
    return _update_project_changelog(
        settings=settings, sections=sections, version=version, draft=draft
    )
