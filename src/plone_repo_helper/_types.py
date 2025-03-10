from dataclasses import dataclass
from pathlib import Path


@dataclass
class Changelogs:
    """Changelog locations."""

    root: Path
    backend: Path
    frontend: Path

    def sanity(self) -> bool:
        return self.root.exists() and self.backend.exists() and self.frontend.exists()


@dataclass
class Package:
    """Package information."""

    name: str
    path: Path
    changelog: Path
    towncrier: Path

    def sanity(self) -> bool:
        return (
            self.path.exists() and self.changelog.exists() and self.towncrier.exists()
        )


@dataclass
class TowncrierSettings:
    """Towncrier settings."""

    backend: Path
    frontend: Path

    def sections(self) -> tuple[tuple[str, Path], ...]:
        return (
            ("Backend", self.backend),
            ("Frontend", self.frontend),
        )

    def sanity(self) -> bool:
        return self.backend.exists() and self.frontend.exists()


@dataclass
class RepositorySettings:
    """Settings for a distribution."""

    name: str
    is_distribution: bool
    root_path: Path
    backend: Package
    frontend: Package
    version_path: Path
    compose_path: Path
    towncrier: TowncrierSettings
    changelogs: Changelogs

    def sanity(self) -> bool:
        return all(
            [
                self.root_path.exists(),
                self.backend.sanity(),
                self.frontend.sanity(),
                self.version_path.exists(),
                self.compose_path.exists(),
                self.towncrier.sanity(),
                self.changelogs.sanity(),
            ]
        )


@dataclass
class CTLContextObject:
    """Context object used by cli."""

    settings: RepositorySettings
