from pathlib import Path

import re
import tomlkit


def current_plone(pyproject: Path) -> str | None:
    """Return the current Plone version."""
    data = tomlkit.parse(pyproject.read_text())
    # Find Plone
    deps = data.get("project", {}).get("dependencies", [])
    for dep in deps:
        if match := re.match("^Products.CMFPlone==(?P<version>.*)$", dep):
            return match.groupdict()["version"]
    return None


def _update_dependency(data: dict, package: str, version: str) -> None:
    deps = data.get("project", {}).get("dependencies", [])
    for idx, dep in enumerate(deps):
        if re.match(f"^{package}", dep):
            deps[idx] = f"{package}=={version}"
            break
    data["project"]["dependencies"] = deps


def _update_constraints(data: dict, constraints: list[str]) -> None:
    tool_uv = data.get("tool", {}).get("uv", {})
    if not tool_uv:
        data["tool"] = {"uv": {}}
        tool_uv = data["tool"]["uv"]
    tool_uv.update({"constraint-dependencies": constraints})


def update_pyproject(pyproject: Path, version: str, constraints: list[str]):
    """Update pyproject.toml with a new Plone version."""
    data = tomlkit.parse(pyproject.read_text())
    # Update dependency
    _update_dependency(data, "Products.CMFPlone", version)
    # Constraints
    _update_constraints(data, constraints)
    # Update pyproject
    pyproject.write_text(tomlkit.dumps(data))
