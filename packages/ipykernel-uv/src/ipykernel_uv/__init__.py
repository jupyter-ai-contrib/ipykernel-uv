"""An IPython kernel that uses uv for package and environment management."""

from .envmanager import UvEnvManager

__version__ = "0.1.0"

__all__ = ["UvEnvManager", "__version__"]
