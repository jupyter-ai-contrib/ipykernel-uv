# Making a Release

This project uses [Jupyter Releaser](https://jupyter-releaser.readthedocs.io/) to
automate changelog generation, version bumping, git tagging, GitHub Releases, and
publishing to PyPI.

## One-time repository setup

These steps must be completed by a repository admin before the first release.

1. **GitHub App** — Create a GitHub App on the organization (Contents: Read & write,
   web hook disabled), install it on this repo, and generate a private key.
2. **`release` environment** — In repo *Settings → Environments*, create an environment
   named `release`. Add an `APP_ID` environment **variable** and an `APP_PRIVATE_KEY`
   **secret** from the GitHub App. Restrict the environment to protected branches only.
3. **PyPI trusted publisher** — On PyPI, add a
   [trusted publisher](https://docs.pypi.org/trusted-publishers/adding-a-publisher/) for
   the `ipykernel-uv` project:
   - Owner: `jupyter-ai-contrib`
   - Repository: `ipykernel-uv`
   - Workflow name: `publish-release.yml`
   - Environment: `release`

   No PyPI API token is stored — publishing uses OIDC (`id-token: write`).
4. **Labels** — Ensure the standard triage labels exist so `enforce-label` and the
   changelog categorization work (`bug`, `enhancement`, `documentation`,
   `maintenance`, etc.).

## Cutting a release

1. Go to the **Actions** tab → **"Step 1: Prep Release"** → *Run workflow*.
   - **New Version Specifier**: the target version (e.g. `0.2.0`) or a hatch segment
     such as `patch`, `minor`, `major`.
   - This generates the changelog from merged PRs, bumps `__version__` in
     `src/ipykernel_uv/__init__.py`, and creates a **draft** GitHub Release.
2. Review the draft release and the changelog PR.
3. Run **"Step 2: Publish Release"** → *Run workflow*, pasting the draft release URL
   from Step 1 if prompted. This finalizes the tag + GitHub Release and publishes the
   sdist and wheel to PyPI.

## Testing the flow safely

Try Step 1 and Step 2 against a **fork** first so tags and releases are not pushed to
the source repo. To publish to TestPyPI instead of PyPI during a dry run, set the
`TWINE_REPOSITORY_URL` environment variable to `https://test.pypi.org/legacy/` on the
"Finalize Release" step.

## Version source of truth

The version lives only in `src/ipykernel_uv/__init__.py` (`__version__`). `pyproject.toml`
declares `dynamic = ["version"]` and reads it via `[tool.hatch.version]`, so there is no
duplicated hardcoded version to keep in sync.
