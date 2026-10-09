# ipykernel-uv

A Jupyter kernel that uses [uv](https://docs.astral.sh/uv/) to automatically manage
Python environments for your projects. When you select this kernel, it finds the nearest
`pyproject.toml`, syncs the project's dependencies with `uv`, and launches IPython inside
that environment — no manual virtual environment management required.

Part of the [ipykernel-env](https://github.com/jupyter-ai-contrib/ipykernel-env) monorepo;
built on [`ipykernel-env-core`](../ipykernel-env-core).

## How it works

1. You select the **Python (uv)** kernel in JupyterLab
2. The kernel finds the nearest `pyproject.toml` by walking up from the notebook's directory
3. If it can't find one, it creates one in the notebook's directory (`uv init --bare`)
4. If `ipykernel` is not already in the project's dependencies, it adds it via `uv add`
5. It runs `uv run --project <dir> python -m ipykernel_launcher`
6. uv syncs the project's environment and starts IPython inside it

## Requirements

- Python >= 3.10
- [uv](https://docs.astral.sh/uv/) installed and available on PATH

## Installation

```bash
pip install ipykernel-uv
```

Then register the kernel spec:

```bash
# Install into the current virtual environment (recommended)
python -m ipykernel_uv install --sys-prefix

# Install for the current user
python -m ipykernel_uv install --user

# Install into a specific prefix
python -m ipykernel_uv install --prefix /path/to/prefix
```

## Usage

1. Make sure your project directory has a `pyproject.toml` (or let the kernel create one).
2. Open JupyterLab and create or open a notebook in your project directory.
3. Select the **Python (uv)** kernel from the kernel picker.
4. Your notebook now runs inside your project's uv-managed environment.
5. Add new packages with `!uv add <package>` inside a notebook cell.

## Install options

| Flag | Description |
|------|-------------|
| `--name` | Kernel name (default: `python3-uv`) |
| `--display-name` | Display name in Jupyter (default: `Python (uv)`) |
| `--user` | Install for the current user |
| `--sys-prefix` | Install into `sys.prefix` (e.g. the active virtual environment) |
| `--prefix` | Install into a specific prefix directory |

## License

BSD-3-Clause
