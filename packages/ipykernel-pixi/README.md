# ipykernel-pixi

A Jupyter kernel that uses [pixi](https://pixi.prefix.dev/) to automatically manage
environments for your projects. When you select this kernel, it finds the nearest pixi
manifest, syncs the project's dependencies with `pixi`, and launches IPython inside that
environment.

Part of the [ipykernel-env](https://github.com/jupyter-ai-contrib/ipykernel-env) monorepo;
built on [`ipykernel-env-core`](../ipykernel-env-core).

## How it works

1. You select the **Python (pixi)** kernel in JupyterLab
2. The kernel finds the nearest pixi manifest by walking up from the notebook's directory —
   a `pixi.toml`, or a `pyproject.toml` carrying a `[tool.pixi]` table
3. If it can't find one, it creates a bare `pixi.toml` in the notebook's directory
   via `pixi init --format pixi` (no source-package scaffold, no build-system)
4. If `ipykernel` is not already declared, it adds it via `pixi add ipykernel`
5. It runs `pixi run --manifest-path <manifest> python -m ipykernel_launcher`
6. pixi syncs the project's environment and starts IPython inside it

## Requirements

- Python >= 3.10
- [pixi](https://pixi.prefix.dev/) installed and available on PATH

## Installation

```bash
pip install ipykernel-pixi
```

Then register the kernel spec:

```bash
# Install into the current virtual environment (recommended)
python -m ipykernel_pixi install --sys-prefix

# Install for the current user
python -m ipykernel_pixi install --user

# Install into a specific prefix
python -m ipykernel_pixi install --prefix /path/to/prefix
```

## Usage

1. Make sure your project directory has a pixi manifest (`pixi.toml`, or a `pyproject.toml`
   with `[tool.pixi]`), or let the kernel create one.
2. Open JupyterLab and create or open a notebook in your project directory.
3. Select the **Python (pixi)** kernel from the kernel picker.
4. Your notebook now runs inside your project's pixi-managed environment.
5. Add new packages with `!pixi add <package>` (conda-forge) or `!pixi add --pypi <package>`
   inside a notebook cell.

> **Adding dependencies:** use `!pixi add` (or edit the pixi manifest), not a plain
> `pyproject.toml`. pixi only reads dependencies from a manifest that carries its own
> marker — a `pixi.toml`, or a `pyproject.toml` with a `[tool.pixi]` table. Packages
> listed in a plain `[project.dependencies]` of a pyproject *without* that marker are
> not seen by pixi. (This differs from the uv kernel, which adopts any `pyproject.toml`.)

## Install options

| Flag | Description |
|------|-------------|
| `--name` | Kernel name (default: `python3-pixi`) |
| `--display-name` | Display name in Jupyter (default: `Python (pixi)`) |
| `--user` | Install for the current user |
| `--sys-prefix` | Install into `sys.prefix` (e.g. the active virtual environment) |
| `--prefix` | Install into a specific prefix directory |

## License

BSD-3-Clause
