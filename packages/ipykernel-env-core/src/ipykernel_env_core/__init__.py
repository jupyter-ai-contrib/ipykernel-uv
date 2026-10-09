"""Shared core for environment-managed IPython kernels.

Provides the environment-manager abstraction and the launch/install plumbing
shared by the uv and pixi kernels. An :class:`EnvManager` knows how to find (or
create) a project manifest, make sure ``ipykernel`` is declared, and exec into
``ipykernel_launcher`` inside the project's managed environment.
"""

from .envmanager import EnvManager
from .install import install, install_main
from .launcher import launch_kernel

__version__ = "0.1.0"

__all__ = ["EnvManager", "install", "install_main", "launch_kernel", "__version__"]
