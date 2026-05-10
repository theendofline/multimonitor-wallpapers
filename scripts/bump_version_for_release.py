#!/usr/bin/env python3
"""Bump the project version in all tracked release files. Usage: bump_version_for_release.py X.Y.Z"""

from __future__ import annotations

import re
import sys
from pathlib import Path


def _set_init_version(text: str, version: str) -> tuple[str, int]:
    return re.subn(
        r"^(__version__\s*=\s*)[\"'][^\"']+[\"']",
        rf'\1"{version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )


def _set_pyproject_version(text: str, version: str) -> tuple[str, int]:
    return re.subn(
        r"^version\s*=\s*\"[^\"]+\"\s*$",
        f'version = "{version}"',
        text,
        count=1,
        flags=re.MULTILINE,
    )


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: bump_version_for_release.py <semver>")
    version = sys.argv[1].strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise SystemExit(f"Expected semver X.Y.Z, got: {version!r}")

    root = Path(__file__).resolve().parent.parent
    init_path = root / "src" / "multimonitor_wallpapers" / "__init__.py"
    original = init_path.read_text(encoding="utf-8")
    updated, n = _set_init_version(original, version)
    if n != 1:
        raise SystemExit(
            f"Expected exactly one __version__ line in {init_path.relative_to(root)}, replaced {n}"
        )
    init_path.write_text(updated, encoding="utf-8")

    pp = root / "pyproject.toml"
    body = pp.read_text(encoding="utf-8")
    updated, n = _set_pyproject_version(body, version)
    if n != 1:
        raise SystemExit(
            f"Expected exactly one project version line in pyproject.toml, replaced {n}"
        )
    pp.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
