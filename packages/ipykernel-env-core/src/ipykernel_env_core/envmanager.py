"""The environment-manager abstraction.

An :class:`EnvManager` adapts one environment manager (uv, pixi, ...) to the
kernel. The launcher is manager-agnostic: it finds or creates a manifest,
ensures ``ipykernel`` is declared, then execs into the kernel inside the managed
environment. Each implementation supplies the manager-specific command strings.

To add support for a new manager, implement this protocol and expose it from a
thin package whose ``__main__`` calls :func:`ipykernel_env_core.launch_kernel` /
:func:`ipykernel_env_core.install_main` with an instance.
"""

from __future__ import annotations

from pathlib import Path
from typing import NoReturn, Protocol, runtime_checkable


@runtime_checkable
class EnvManager(Protocol):
    """One environment manager, adapted to the kernel launch/install flow."""

    #: Short identifier, e.g. ``"uv"`` or ``"pixi"``.
    name: str

    #: Human-facing name of the manager, used in messages, e.g. ``"uv"``.
    display: str

    def check_available(self) -> str:
        """Return the absolute path to the manager executable.

        Raise :class:`RuntimeError` with an actionable message if the manager
        is not installed / not on PATH.
        """
        ...

    def find_manifest(self, start: Path) -> Path | None:
        """Walk up from ``start`` and return the project manifest, or ``None``.

        "Manifest" is whatever marks a project this manager owns (for uv, a
        ``pyproject.toml``; for pixi, a ``pixi.toml`` or a ``pyproject.toml``
        carrying a ``[tool.pixi]`` table).
        """
        ...

    def init_project(self, directory: Path) -> Path:
        """Create a new project in ``directory`` and return its manifest path."""
        ...

    def ensure_ipykernel(self, manifest: Path) -> None:
        """Ensure ``ipykernel`` is a declared dependency of the project."""
        ...

    def exec_kernel(self, manifest: Path, args: list[str]) -> NoReturn:
        """Exec (replace this process) into ``ipykernel_launcher`` in the env."""
        ...
