"""pixi environment manager: manage the environment with ``pixi``.

A pixi project is marked by either a ``pixi.toml`` or a ``pyproject.toml`` that
carries a ``[tool.pixi]`` table (the "pixi directive" pixi auto-detects). When
no manifest exists, a bare ``pixi.toml`` is created via ``pixi init
--format pixi`` -- the analog of ``uv init --bare``, with no source-package
scaffold or editable self-install.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import NoReturn

from ipykernel_env_core.manifest import load_toml, walk_up_for

_PACKAGE = "ipykernel"


def _is_pixi_pyproject(pyproject: Path) -> bool:
    """True if ``pyproject.toml`` carries a ``[tool.pixi]`` table."""
    try:
        data = load_toml(pyproject)
    except Exception:
        return False
    return "pixi" in data.get("tool", {})


class PixiEnvManager:
    """Adapts pixi to the kernel: pixi manifest + ``pixi run``."""

    name = "pixi"
    display = "pixi"

    def check_available(self) -> str:
        pixi = shutil.which("pixi")
        if pixi is None:
            raise RuntimeError(
                "pixi not found on PATH. Install pixi: "
                "https://pixi.prefix.dev/latest/installation/"
            )
        return pixi

    def find_manifest(self, start: Path) -> Path | None:
        # A bare pixi.toml always wins; otherwise a pyproject.toml only counts
        # when it carries the [tool.pixi] directive. The two are searched
        # together per directory while walking up so a plain pyproject.toml in
        # a parent does not shadow a pixi.toml closer to the notebook.
        current = start.resolve()
        while True:
            pixi_toml = current / "pixi.toml"
            if pixi_toml.is_file():
                return pixi_toml
            pyproject = current / "pyproject.toml"
            if pyproject.is_file() and _is_pixi_pyproject(pyproject):
                return pyproject
            parent = current.parent
            if parent == current:
                return None
            current = parent

    def init_project(self, directory: Path) -> Path:
        pixi = self.check_available()
        # --format pixi writes a bare pixi.toml ([workspace] with channels +
        # current platform, plus empty [tasks]/[dependencies]). Unlike
        # --format pyproject it does NOT scaffold a src/<name> package, a
        # [build-system], or an editable self-install -- none of which a
        # notebook environment wants. If a plain pyproject.toml already exists
        # it is left untouched; the standalone pixi.toml coexists with it and
        # is what this manager's find_manifest claims.
        subprocess.run(
            [pixi, "init", ".", "--format", "pixi"],
            cwd=directory,
            check=True,
        )
        return directory / "pixi.toml"

    def ensure_ipykernel(self, manifest: Path) -> None:
        if self._has_ipykernel(manifest):
            return
        pixi = self.check_available()
        subprocess.run(
            [pixi, "add", "--manifest-path", str(manifest), _PACKAGE],
            check=True,
        )

    def exec_kernel(self, manifest: Path, args: list[str]) -> NoReturn:
        pixi = self.check_available()
        cmd = [
            pixi,
            "run",
            "--manifest-path",
            str(manifest),
            "python",
            "-m",
            "ipykernel_launcher",
            *args,
        ]
        os.execvp(cmd[0], cmd)

    @staticmethod
    def _has_ipykernel(manifest: Path) -> bool:
        """True if ipykernel is declared anywhere pixi would resolve it.

        Covers pixi.toml tables and the pyproject.toml equivalents:
        conda deps (``[dependencies]`` / ``[tool.pixi.dependencies]``), pixi
        PyPI deps (``[pypi-dependencies]`` / ``[tool.pixi.pypi-dependencies]``),
        and standard ``[project.dependencies]``.
        """
        try:
            data = load_toml(manifest)
        except Exception:
            return False

        tool_pixi = data.get("tool", {}).get("pixi", {})

        # Mapping-style tables (name -> spec): check the keys.
        for table in (
            data.get("dependencies", {}),
            data.get("pypi-dependencies", {}),
            tool_pixi.get("dependencies", {}),
            tool_pixi.get("pypi-dependencies", {}),
        ):
            if isinstance(table, dict) and _PACKAGE in table:
                return True

        # List-style [project.dependencies]: check the bare names.
        from ipykernel_env_core.manifest import _dep_name

        project_deps = data.get("project", {}).get("dependencies", [])
        if isinstance(project_deps, list):
            if any(_dep_name(dep) == _PACKAGE for dep in project_deps):
                return True

        return False
