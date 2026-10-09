# ipykernel-env

Jupyter kernels that manage your project's environment for you.

Pick the kernel and start writing code. There is no virtual environment to create
first, no `ipykernel` to remember to install, no "which Python is this notebook
even using" — the kernel finds your project, makes sure the environment exists and
has what it needs, and launches IPython inside it. Add a package from a notebook
cell and it lands in that same project environment, declared in the manifest and
ready on the next cell.

The result is a notebook that is reproducible by construction: the dependencies a
notebook needs live in the project manifest next to it, so the next person to open
it (or you, on another machine) gets the same environment without a setup ritual.

<!-- TODO: demo GIF -- select kernel -> environment is prepared -> !uv add / !pixi add in a cell -->

## Install

Install the kernel for the environment manager you use. Each one pulls in the
shared core automatically — you do not install the core yourself.

### uv

```bash
pip install ipykernel-uv
python -m ipykernel_uv install --sys-prefix
```

Requires [uv](https://docs.astral.sh/uv/) on your PATH. Adds a **Python (uv)**
kernel.

### pixi

```bash
pip install ipykernel-pixi
python -m ipykernel_pixi install --sys-prefix
```

Requires [pixi](https://pixi.prefix.dev/) on your PATH. Adds a **Python (pixi)**
kernel.

You can install both side by side — each registers its own kernel, and a notebook
picks whichever one matches how its project is managed.

## Packages

This is a monorepo: a shared core plus one thin package per environment manager.

| Package | Manager | Kernel | PyPI |
|---|---|---|---|
| [`ipykernel-env-core`](packages/ipykernel-env-core) | — | — | `ipykernel-env-core` |
| [`ipykernel-uv`](packages/ipykernel-uv) | [uv](https://docs.astral.sh/uv/) | Python (uv) | `ipykernel-uv` |
| [`ipykernel-pixi`](packages/ipykernel-pixi) | [pixi](https://pixi.prefix.dev/) | Python (pixi) | `ipykernel-pixi` |

`ipykernel-env-core` defines a small `EnvManager` protocol and the
manager-agnostic flow every kernel runs:

```
find the project manifest (or create one) -> ensure ipykernel is declared -> launch the kernel inside the managed environment
```

Each manager fills in the specific pieces — how it discovers a manifest,
how it initializes a project, how it adds a dependency, how it runs the kernel.
Adding support for another environment manager is a new package implementing
`EnvManager`; the core flow does not change. See each package's README for the
manager's specifics.

## Development

This repo is a [uv workspace](https://docs.astral.sh/uv/concepts/workspaces/) for
local development.

```bash
git clone https://github.com/jupyter-ai-contrib/ipykernel-env.git
cd ipykernel-env

# Sync all three packages into one editable dev environment
uv sync

# Register the kernels locally
uv run python -m ipykernel_uv install --sys-prefix
uv run python -m ipykernel_pixi install --sys-prefix
```

## License

BSD-3-Clause
