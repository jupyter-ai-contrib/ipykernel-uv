"""Manifest discovery and inspection helpers shared across environment managers."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

try:  # Python 3.11+
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - 3.10 fallback
    import tomli as tomllib  # type: ignore[no-redef]


def walk_up_for(start: Path, filename: str) -> Path | None:
    """Walk up from ``start`` to the filesystem root looking for ``filename``.

    Returns the first matching file path, or ``None`` if the root is reached
    without a match.
    """
    current = start.resolve()
    while True:
        candidate = current / filename
        if candidate.is_file():
            return candidate
        parent = current.parent
        if parent == current:
            return None
        current = parent


def load_toml(path: Path) -> dict[str, Any]:
    """Parse a TOML file into a dict."""
    with open(path, "rb") as f:
        return tomllib.load(f)


def _dep_name(spec: str) -> str:
    """Return the bare package name from a PEP 508 / version-spec dependency."""
    return re.split(r"[><=!\[;~\s]", spec.strip())[0]


def has_project_dependency(pyproject: Path, package: str) -> bool:
    """True if ``package`` is listed in ``[project].dependencies``."""
    data = load_toml(pyproject)
    deps = data.get("project", {}).get("dependencies", [])
    return any(_dep_name(dep) == package for dep in deps)
