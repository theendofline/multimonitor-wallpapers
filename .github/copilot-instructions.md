# Copilot Code Review — multimonitor-wallpapers

PySide6 + Pillow desktop app that sets per-monitor wallpapers on Linux
(GNOME / KDE / xrandr backends). Packaged as AppImage and DEB, released
by `semantic-release` from `main`. Python 3.12+, src-layout.

## Review priorities (in order)

1. Correctness on the targeted desktop environment (GNOME/KDE/xrandr).
2. Security: no shell injection in `subprocess` calls, no untrusted paths.
3. Behaviour preserved: tests under `tests/` still describe the contract.
4. Style: ruff, black (line length 100), mypy strict-ish are the source
   of truth. Don't suggest changes that fight `pyproject.toml`.

## Python

- Require Python 3.12+ idioms (PEP 604 `X | None`, `match`, etc.).
- All new public functions/methods need type hints (mypy enforces this).
- Prefer `pathlib.Path` over `os.path`; `subprocess.run([...], check=...)`
  with a list, never `shell=True`.
- Use module-level `logger = logging.getLogger(__name__)`. Don't use
  `print` in `src/`. `print` is acceptable in `scripts/build_*.py`.
- Narrow exception catches (`OSError`, `subprocess.CalledProcessError`,
  `ValueError`). Flag bare `except:` or `except Exception:` without a
  re-raise/log.

## PySide6 / Qt

- Use namespaced enums only:
  - `Qt.AlignmentFlag.AlignCenter` (not `Qt.AlignCenter`)
  - `Qt.GlobalColor.white` (not `Qt.white`)
  - `QPalette.ColorRole.Window` (not `QPalette.Window`)
  - `Qt.AspectRatioMode.KeepAspectRatio`, `Qt.TransformationMode.*`
- Tests must run headless: rely on `QT_QPA_PLATFORM=offscreen` (set in
  `tests/test_ui.py`). Don't suggest tests that need a real display.
- Don't introduce QML, QtMultimedia, QtWebEngine, Qt3D, QtCharts, or any
  module outside `QtCore`/`QtGui`/`QtWidgets` — `scripts/build_appimage.py`
  trims them and adding them silently breaks the AppImage.

## Pillow

- Use `Image.Resampling.LANCZOS` (not `Image.LANCZOS`).
- Always `with Image.open(...) as img:` for input files.

## Tests

- `pytest` only. New behaviour needs at least one happy-path and one
  failure-path test.
- Use `tmp_path` and `monkeypatch`; don't write into the repo.
- Don't suggest mocking `subprocess` at the stdlib level — prefer
  `monkeypatch.setattr` on the function under test.

## Build / packaging

- Don't reintroduce `ImageMagick convert` or any system binary that was
  intentionally removed from `validate_dependencies` / `_SYSTEM_BINARIES`.
- Don't bundle `pip`/`setuptools` into the AppImage.
- Treat `assets/icon.png` as a checked-in asset; do not regenerate it
  procedurally and do not propose adding ImageMagick back to do so.

## Commits & PRs

- Conventional Commits (`feat:`, `fix:`, `chore:`, `test:`, `docs:`,
  `refactor:`) — `semantic-release` parses them to compute versions.
  A `feat:` triggers a minor; `fix:` a patch; `BREAKING CHANGE:` a major.
- Each commit should be atomic and self-verifying (lints + tests pass).

## What NOT to suggest

- Speculative debounce/throttle/caching without a measured regression.
  This codebase prefers profile-driven optimization.
- Generic "add error handling" comments — name the concrete exception
  and recovery, or skip the comment.
- Style nits already enforced by ruff/black (trailing commas, quote
  style, import order) — they are auto-fixed pre-commit.
- Renames / refactors of code untouched by the PR.
- Replacing stdlib with extra dependencies (`requests`, `click`, etc.)
  unless the PR clearly needs them.

## Good comment examples

- "`subprocess.run(cmd, shell=True)` on line N — `cmd` interpolates
  `monitor['name']`. Pass a list and drop `shell=True`."
- "New `_resolve_path` lacks a test for the `~` expansion branch you
  added; `tests/test_*.py` should cover it."
- "PySide6 import on line N uses `Qt.AlignCenter`; PySide6 6.11 requires
  `Qt.AlignmentFlag.AlignCenter` (mypy will fail)."
