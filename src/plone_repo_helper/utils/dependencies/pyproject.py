from pathlib import Path
from tomlkit import container
from tomlkit import items

import re
import tomlkit


def _get_project_table(data: tomlkit.TOMLDocument) -> items.Table:
    """Return the current project information."""
    project = data["project"]
    if not isinstance(project, items.Table | container.OutOfOrderTableProxy):
        raise ValueError("Invalid data")
    return project


def _get_project_dependencies(data: tomlkit.TOMLDocument) -> items.Array:
    """Return the current project dependencies."""
    project = _get_project_table(data)
    dependencies: items.Array = project.get("dependencies") or tomlkit.array()
    return dependencies


def current_plone(pyproject: Path) -> str | None:
    """Return the current Plone version."""
    data = tomlkit.parse(pyproject.read_text())
    # Find Plone
    deps = _get_project_dependencies(data)
    for dep in deps:
        if match := re.match("^Products.CMFPlone==(?P<version>.*)$", dep):
            return match.groupdict()["version"]
    return None


def _update_dependency(data: tomlkit.TOMLDocument, package: str, version: str) -> None:
    project = _get_project_table(data)
    deps = tomlkit.array()
    deps.multiline(True)
    for dep in _get_project_dependencies(data):
        if re.match(f"^{package}", dep):
            dep = f"{package}=={version}"
        deps.append(dep)
    project.update({"dependencies": deps})


def _update_constraints(data: tomlkit.TOMLDocument, raw_constraints: list[str]) -> None:
    tool_uv = data.get("tool", {}).get("uv", {})
    if not tool_uv:
        tool_uv = tomlkit.table(False)
        data.append("tool.uv", tool_uv)
    constraints = tomlkit.array()
    constraints.multiline(True)
    for line in raw_constraints:
        item = tomlkit.item(line)
        constraints.append(item)
    tool_uv.update({"constraint-dependencies": constraints})


def update_pyproject(pyproject: Path, version: str, constraints: list[str]):
    """Update pyproject.toml with a new Plone version."""
    data: tomlkit.TOMLDocument = tomlkit.parse(pyproject.read_text())
    # Update dependency
    _update_dependency(data, "Products.CMFPlone", version)
    # Constraints
    _update_constraints(data, constraints)
    # Update pyproject
    pyproject.write_text(tomlkit.dumps(data))
