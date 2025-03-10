from .versions import plone_versions
from mxdev.processing import resolve_dependencies

import requests


def get_constraints(url: str) -> str:
    """Return the contents of an external constraints file."""
    response = requests.get(url)  # noQA: S113
    data = response.content.decode("utf-8")
    return data


def parse_constraints(lines: list[str]) -> list[str]:
    constraints = []
    for line in lines:
        line = line.strip()
        if line.startswith("#") or not line:
            continue
        constraints.append(line)
    return sorted(constraints, key=lambda x: x.lower())


def get_plone_constraints(version: str = "6.1.0") -> list[str]:
    """Return plone constraints for a version."""
    versions = plone_versions()
    if version not in versions:
        raise RuntimeError(f"Plone {version} not available.")
    url = f"https://dist.plone.org/release/{version}/constraints.txt"
    _, constraints = resolve_dependencies(url, [], [], [], "c")
    return parse_constraints(constraints)
