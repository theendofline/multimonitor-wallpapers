#!/usr/bin/env bash
# Build the versioned AppImage + DEB for a semantic-release run.
#
# Invoked by `.releaserc.json`'s @semantic-release/exec `prepareCmd` so the
# version it bumps and the version embedded in the artifact filenames are
# the *same* string that the GitHub release will be tagged with.
#
# Args:
#   $1 — semantic version (e.g. 1.2.3), required.
#
# Env (optional):
#   RELEASE_BUILD_NUMBER — Debian revision (default: ${GITHUB_RUN_NUMBER:-1}).

set -euo pipefail

VERSION="${1:?Usage: build_release_artifacts.sh <semver>}"
RELEASE_BUILD_NUMBER="${RELEASE_BUILD_NUMBER:-${GITHUB_RUN_NUMBER:-1}}"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> Bumping project version to $VERSION"
python3 scripts/bump_version_for_release.py "$VERSION"

echo "==> Refreshing uv.lock to match the bumped version"
uv lock
uv sync --frozen --extra build

echo "==> Building AppImage"
uv run python scripts/build_appimage.py
chmod +x dist/*.AppImage

echo "==> Building DEB from AppImage"
RELEASE_VERSION="$VERSION" RELEASE_BUILD_NUMBER="$RELEASE_BUILD_NUMBER" \
    scripts/build_deb.sh

echo "==> Release artifacts:"
ls -la dist/
