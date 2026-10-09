# ipykernel-env-core

Shared core for environment-managed IPython kernels. Provides the `EnvManager`
abstraction and the launch/install plumbing used by the manager packages
([`ipykernel-uv`](../ipykernel-uv), [`ipykernel-pixi`](../ipykernel-pixi)).

You usually don't install this directly — install a manager package, which
depends on this one. Implement `EnvManager` to add a new environment manager.

## The `EnvManager` protocol

```python
class EnvManager(Protocol):
    name: str
    display: str
    def check_available(self) -> str: ...
    def find_manifest(self, start: Path) -> Path | None: ...
    def init_project(self, directory: Path) -> Path: ...
    def ensure_ipykernel(self, manifest: Path) -> None: ...
    def exec_kernel(self, manifest: Path, args: list[str]) -> NoReturn: ...
```

A manager package wires it up in its `__main__`:

```python
from ipykernel_env_core import launch_kernel, install_main
from .envmanager import MyEnvManager

manager = MyEnvManager()
# install path: install_main(argv, module="ipykernel_mine", ...)
# launch path:  launch_kernel(manager, args)
```

## License

BSD-3-Clause
