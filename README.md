[![Python Tests](https://github.com/theendofline/multimonitor-wallpapers/actions/workflows/python-tests.yml/badge.svg)](https://github.com/theendofline/multimonitor-wallpapers/actions/workflows/python-tests.yml)
[![CodeQL Advanced](https://github.com/theendofline/multimonitor-wallpapers/actions/workflows/codeql.yml/badge.svg)](https://github.com/theendofline/multimonitor-wallpapers/actions/workflows/codeql.yml)
[![Build and Release](https://github.com/theendofline/multimonitor-wallpapers/actions/workflows/release.yml/badge.svg)](https://github.com/theendofline/multimonitor-wallpapers/actions/workflows/release.yml)

# Multi-Monitor Wallpapers

Python + PySide6 desktop app for **Linux Cinnamon**: pick different images per monitor, composite them, and apply via `gsettings`.

## System requirements

- **Python 3.12+**
- **Cinnamon**
- **`gsettings`**, **`xrandr`**, ImageMagick **`convert`**
- **[uv](https://docs.astral.sh/uv/)** (recommended) for installs aligned with **`uv.lock`**

## Install & run (uv, recommended)

Dependencies and exact transitive versions live in **`pyproject.toml`** + **`uv.lock`**.

```bash
# One-time: install uv — https://docs.astral.sh/uv/getting-started/installation/

# Create .venv and install app + dev + build extras from the lockfile
uv sync --frozen --extra dev --extra build

# Run without manually activating the venv
uv run multimonitor-wallpapers
# or: uv run python -m multimonitor_wallpapers
# or, after: source .venv/bin/activate
multimonitor-wallpapers
```

**Runtime only** (no pytest/ruff/black/mypy/build tools):

```bash
uv sync --frozen
uv run multimonitor-wallpapers
```

### Lock / sync workflow

| Command | Purpose |
|--------|---------|
| **`uv lock`** | Resolve deps from **`pyproject.toml`** and write **`uv.lock`** (exact versions for the full tree). |
| **`uv sync --frozen …`** | Make **`.venv`** match **`uv.lock`** without changing the lock; fails if the lock is out of date (CI uses this). |
| **`uv lock --upgrade`** | Refresh **`uv.lock`** to the newest versions allowed by pins/ranges, then commit the diff. |

**Benefits:** reproducible envs, fast installs, reviewable dependency PRs, and **`uv sync`** can prune packages no longer in the lock.

After editing dependencies in **`pyproject.toml`**, run **`uv lock`** (or **`just update`** to upgrade inside current constraints) and commit **`uv.lock`** so CI stays green.

### pip-only fallback

If you do not use uv:

```bash
pip install -e ".[dev]"   # app + dev tools
# or runtime only:
pip install -e .
```

Run the app with **`multimonitor-wallpapers`** or **`python -m multimonitor_wallpapers`** (after install, on **`PATH`**).

pip does **not** read **`uv.lock`**; you only get the direct pins from **`pyproject.toml`**.

## AppImage (Linux)

1. Download the latest **`.AppImage`** from [Releases](https://github.com/theendofline/multimonitor-wallpapers/releases).
2. `chmod +x MultiMonitor-*.AppImage`
3. `./MultiMonitor-*.AppImage`

The AppImage bundles Python, PySide6, and app code; no separate Python install is required.

## Usage (from source)

1. Start the UI: **`uv run multimonitor-wallpapers`** (or **`uv run python -m multimonitor_wallpapers`**; with an activated **`.venv`**, **`multimonitor-wallpapers`** on **`PATH`**).
2. Choose images per monitor, **Apply** to set wallpapers, **Cancel** / **Quit** as needed.

## How it works

1. Detect monitors with **`xrandr`**.
2. Resize/place images with **Pillow**.
3. Write a combined image and apply it with **`gsettings`** on Cinnamon.

## Development

**[Just](https://github.com/casey/just)** wraps common tasks (`just` to list recipes).

```bash
just setup     # uv sync --frozen --extra dev --extra build (creates .venv)
just run       # run the app
just test      # pytest
just lint      # ruff + black --check
just format    # ruff --fix + black
just appimage  # build AppImage into dist/
just update    # uv lock --upgrade && uv sync (refresh lock + venv)
```

### Layout

| Path | Role |
|------|------|
| `src/multimonitor_wallpapers/` | Application package (`widget.py`, **`__main__.py`**, **`__version__`**) |
| `scripts/` | **`build_appimage.py`**, **`build_deb.sh`**, **`bump_version_for_release.py`** |
| `pyproject.toml` | Project metadata, **`[project]`** deps, optional **`dev`** / **`build`** extras |
| **`uv.lock`** | Resolved dependency graph (commit when it changes) |
| `.github/workflows/` | CI: tests on PR/`dev`, release pipeline on **`main`** |

## Building an AppImage locally

```bash
sudo apt-get install -y libfuse2 desktop-file-utils libglib2.0-bin   # plus Qt/X deps as in CI if needed
just appimage
```

Output: **`dist/MultiMonitor-x86_64.AppImage`**.

## CI and releases

- **Pull requests / `dev`:** **`.github/workflows/python-tests.yml`** runs **`uv sync --frozen --extra dev`** then lint + tests.
- **`main`:** **`.github/workflows/release.yml`** runs tests, builds **AppImage** + **`.deb`**, then **[semantic-release](https://semantic-release.gitbook.io/)** creates GitHub releases from [Conventional Commits](https://www.conventionalcommits.org/). Release commits bump **`pyproject.toml`**, **`src/multimonitor_wallpapers/__init__.py`** (`__version__`), **`uv.lock`**, and are tagged **`[skip ci]`** so they do not retrigger the full build.

## Contributing

Pull requests welcome. Keep **`uv.lock`** in sync when you change **`pyproject.toml`** dependencies (`uv lock`).

## License

[GNU General Public License v3.0](LICENSE) (GPLv3).

## Troubleshooting

- If the wallpaper does not update, try logging out and back in.
- Confirm **`gsettings`**, **`xrandr`**, and **`convert`** are on **`PATH`**.
- If **`uv sync --frozen`** fails after a **`pyproject.toml`** edit, run **`uv lock`** and commit the updated **`uv.lock`**.

## Future ideas

- Other desktop environments, drag-and-drop, live preview, slideshows.
