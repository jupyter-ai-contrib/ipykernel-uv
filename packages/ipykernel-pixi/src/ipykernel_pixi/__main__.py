"""Entry point for ``python -m ipykernel_pixi``."""

import sys

from ipykernel_env_core import install_main, launch_kernel

from .envmanager import PixiEnvManager


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "install":
        install_main(
            sys.argv[2:],
            module="ipykernel_pixi",
            default_name="python3-pixi",
            default_display_name="Python (pixi)",
        )
    else:
        launch_kernel(PixiEnvManager(), sys.argv[1:])


if __name__ == "__main__":
    main()
