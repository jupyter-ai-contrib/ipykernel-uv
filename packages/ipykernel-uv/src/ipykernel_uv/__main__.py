"""Entry point for ``python -m ipykernel_uv``."""

import sys

from ipykernel_env_core import install_main, launch_kernel

from .envmanager import UvEnvManager


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        install_main(
            sys.argv[2:],
            module="ipykernel_uv",
            default_name="python3-uv",
            default_display_name="Python (uv)",
        )
    else:
        launch_kernel(UvEnvManager(), sys.argv[1:])


if __name__ == "__main__":
    main()
