"""uv environment manager: manage the environment with ``uv`` and a ``pyproject.toml``."""

from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path
from typing import NoReturn

from ipykernel_env_core.manifest import has_project_dependency, walk_up_for


class UvEnvManager:
    """Adapts uv to the kernel: nearest ``pyproject.toml`` + ``uv run``."""

    name = "uv"
    display = "uv"

    def check_available(self) -> str:
        uv = shutil.which("uv")
        if uv is None:
            raise RuntimeError(
                "uv not found on PATH. Install uv: "
                "https://docs.astral.sh/uv/getting-started/installation/"
            )
        return uv

    def find_manifest(self, start: Path) -> Path | None:
        return walk_up_for(start, "pyproject.toml")

    def init_project(self, directory: Path) -> Path:
        uv = self.check_available()
        subprocess.run([uv, "init", ".", "--bare"], cwd=directory, check=True)
        return directory / "pyproject.toml"

    def ensure_ipykernel(self, manifest: Path) -> None:
        if has_project_dependency(manifest, "ipykernel"):
            return
        uv = self.check_available()
        subprocess.run(
            [uv, "add", "--project", str(manifest.parent), "ipykernel"],
            check=True,
        )

    def exec_kernel(self, manifest: Path, args: list[str]) -> NoReturn:
        uv = self.check_available()
        cmd = [
            uv,
            "run",
            "--project",
            str(manifest.parent),
            "python",
            "-m",
            "ipykernel_launcher",
            *args,
        ]
        os.execvp(cmd[0], cmd)
