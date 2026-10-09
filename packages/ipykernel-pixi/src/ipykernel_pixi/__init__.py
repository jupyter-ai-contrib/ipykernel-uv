"""An IPython kernel that uses pixi for package and environment management."""

from .envmanager import PixiEnvManager

__version__ = "0.1.0"

__all__ = ["PixiEnvManager", "__version__"]
