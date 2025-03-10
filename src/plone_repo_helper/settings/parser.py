from dynaconf import Dynaconf


def _settings() -> Dynaconf:
    """Parse repo settings."""
    settings = Dynaconf(
        settings_files=["repository.toml"],
        merge_enabled=False,
    )
    return settings


raw_settings: Dynaconf = _settings()
