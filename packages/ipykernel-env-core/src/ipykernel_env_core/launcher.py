"""Manager-agnostic kernel launch flow.

The sequence is identical for every manager:

1. Confirm the manager is installed.
2. Find the nearest project manifest, or create one.
3. Clear inherited virtual-env variables so the manager owns the environment.
4. Ensure ``ipykernel`` is a declared dependency.
5. Exec into ``ipykernel_launcher`` inside the managed environment.

The per-manager differences live entirely in the :class:`EnvManager`.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from .envmanager import EnvManager

# Variables from the launching (JupyterLab) environment that would otherwise
# leak into and confuse the manager-owned environment.
_ENV_VARS_TO_CLEAR = ("VIRTUAL_ENV", "CONDA_PREFIX", "CONDA_DEFAULT_ENV")


def launch_kernel(env_manager: EnvManager, args: list[str]) -> None:
    """Run the launch flow for ``env_manager`` and exec into the kernel."""
    try:
        env_manager.check_available()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)

    cwd = Path.cwd()
    manifest = env_manager.find_manifest(cwd)
    if manifest is None:
        print(
            f"No project manifest found, creating one in {cwd} "
            f"using {env_manager.display}",
            file=sys.stderr,
        )
        manifest = env_manager.init_project(cwd)

    for var in _ENV_VARS_TO_CLEAR:
        os.environ.pop(var, None)

    env_manager.ensure_ipykernel(manifest)
    env_manager.exec_kernel(manifest, args)
