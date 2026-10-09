"""Shared Jupyter kernelspec installation.

Each manager package calls :func:`install_main` with its own module name,
default kernel name, and default display name. The kernelspec's ``argv`` runs
``python -m <module>`` so the right environment manager handles the launch.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile


def install(
    module: str,
    name: str,
    display_name: str,
    user: bool = False,
    prefix: str | None = None,
) -> None:
    """Create and install a kernelspec that launches ``python -m <module>``."""
    from jupyter_client.kernelspec import KernelSpecManager

    kernel_json = {
        "argv": [sys.executable, "-m", module, "-f", "{connection_file}"],
        "display_name": display_name,
        "language": "python",
        "metadata": {"debugger": True},
    }

    with tempfile.TemporaryDirectory() as td:
        kernel_dir = os.path.join(td, name)
        os.makedirs(kernel_dir)
        with open(os.path.join(kernel_dir, "kernel.json"), "w") as f:
            json.dump(kernel_json, f, indent=1)

        ksm = KernelSpecManager()
        ksm.install_kernel_spec(
            kernel_dir, kernel_name=name, user=user, prefix=prefix
        )

    print(f"Installed kernel spec: {name}")


def install_main(
    argv: list[str],
    *,
    module: str,
    default_name: str,
    default_display_name: str,
) -> None:
    """Parse CLI args and install the kernelspec for an environment manager."""
    parser = argparse.ArgumentParser(
        prog=f"python -m {module} install",
        description=f"Install the {module} kernel spec",
    )
    parser.add_argument(
        "--name",
        default=default_name,
        help=f"kernel name (default: {default_name})",
    )
    parser.add_argument(
        "--display-name",
        default=default_display_name,
        help=f"display name (default: {default_display_name})",
    )
    parser.add_argument(
        "--user", action="store_true", help="install for the current user"
    )
    parser.add_argument("--prefix", help="install under a specific prefix")
    parser.add_argument(
        "--sys-prefix",
        action="store_true",
        help="install into sys.prefix (e.g. a virtualenv)",
    )
    args = parser.parse_args(argv)

    prefix = args.prefix
    if args.sys_prefix:
        prefix = sys.prefix

    install(
        module=module,
        name=args.name,
        display_name=args.display_name,
        user=args.user,
        prefix=prefix,
    )
