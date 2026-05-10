#!/usr/bin/env bash
# Build a .deb from an existing MultiMonitor AppImage (same payload as AppImage).
# Requires: dpkg-deb, optional fakeroot for correct metadata ownership.
#
# Env:
#   RELEASE_VERSION — semantic version (e.g. 1.2.3), required
#   RELEASE_BUILD_NUMBER — Debian revision (default: 1)
#
# Arg:
#   $1 — path to AppImage
#        (default: dist/MultiMonitor-${RELEASE_VERSION}-x86_64.AppImage)

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

RELEASE_VERSION="${RELEASE_VERSION:?RELEASE_VERSION is required (e.g. 1.2.3)}"
RELEASE_BUILD_NUMBER="${RELEASE_BUILD_NUMBER:-1}"
APPIMAGE="${1:-dist/MultiMonitor-${RELEASE_VERSION}-x86_64.AppImage}"
ARCH="amd64"
APP_SLUG="multimonitor-wallpapers"
DIST_DIR="dist"
PKG_VERSION="${RELEASE_VERSION}-${RELEASE_BUILD_NUMBER}"

if [[ ! -f "$APPIMAGE" ]]; then
  echo "AppImage not found: $APPIMAGE" >&2
  exit 1
fi

WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

chmod +x "$APPIMAGE"
mkdir -p "$WORK/extract"
# Type-2 AppImage: extracts squashfs-root into cwd
( cd "$WORK/extract" && exec "$ROOT/$APPIMAGE" --appimage-extract )

SRC="$WORK/extract/squashfs-root"
if [[ ! -d "$SRC/usr" ]]; then
  echo "Extract layout missing usr/: $SRC" >&2
  ls -la "$SRC" >&2 || true
  exit 1
fi

PKG_BASENAME="${APP_SLUG}_${PKG_VERSION}_${ARCH}"
PKG_ROOT="$WORK/${PKG_BASENAME}"

mkdir -p "$PKG_ROOT/DEBIAN"
mkdir -p "$PKG_ROOT/opt/${APP_SLUG}"
cp -a "$SRC/usr" "$PKG_ROOT/opt/${APP_SLUG}/"

mkdir -p "$PKG_ROOT/usr/bin"
mkdir -p "$PKG_ROOT/usr/share/applications"
mkdir -p "$PKG_ROOT/usr/share/icons/hicolor/256x256/apps"

if [[ -f "$SRC/usr/share/applications/multimonitor-wallpapers.desktop" ]]; then
  cp "$SRC/usr/share/applications/multimonitor-wallpapers.desktop" \
    "$PKG_ROOT/usr/share/applications/${APP_SLUG}.desktop"
else
  cat > "$PKG_ROOT/usr/share/applications/${APP_SLUG}.desktop" <<EOF
[Desktop Entry]
Name=MultiMonitor Wallpapers
Comment=Set different wallpapers for multiple monitors
Exec=${APP_SLUG}
Icon=${APP_SLUG}
Type=Application
Categories=Utility;Graphics;
Terminal=false
StartupNotify=true
EOF
fi

if [[ -f "$SRC/usr/share/icons/hicolor/256x256/apps/multimonitor-wallpapers.png" ]]; then
  cp "$SRC/usr/share/icons/hicolor/256x256/apps/multimonitor-wallpapers.png" \
    "$PKG_ROOT/usr/share/icons/hicolor/256x256/apps/${APP_SLUG}.png"
fi

cat > "$PKG_ROOT/usr/bin/${APP_SLUG}" <<'WRAPPER'
#!/bin/bash
HERE=/opt/multimonitor-wallpapers
export PYTHONHOME="${HERE}/usr"
export PYTHONPATH="${HERE}/usr/lib/python3.12:${HERE}/usr/lib/python3.12/site-packages"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH:-}"
export XDG_DATA_DIRS="${HERE}/usr/share:${XDG_DATA_DIRS:-}"
export PATH="${HERE}/usr/bin:${PATH}"
export QT_PLUGIN_PATH="${HERE}/usr/lib/python3.12/site-packages/PySide6/plugins"
export QML2_IMPORT_PATH="${HERE}/usr/lib/python3.12/site-packages/PySide6/qml"
exec "${HERE}/usr/bin/python3" "${HERE}/usr/bin/multimonitor-wallpapers" "$@"
WRAPPER
chmod 755 "$PKG_ROOT/usr/bin/${APP_SLUG}"

cat > "$PKG_ROOT/DEBIAN/control" <<EOF
Package: ${APP_SLUG}
Version: ${PKG_VERSION}
Section: graphics
Priority: optional
Architecture: ${ARCH}
Maintainer: MultiMonitor Wallpapers Team <https://github.com>
Depends: libc6 (>= 2.31), libstdc++6, zlib1g
Description: Multi-monitor wallpaper tool for Linux
 Set different wallpapers per monitor (e.g. Cinnamon).
 Bundled Python 3.12 and PySide6 runtime (same tree as the AppImage).
EOF
chmod 644 "$PKG_ROOT/DEBIAN/control"
chmod 644 "$PKG_ROOT/usr/share/applications/${APP_SLUG}.desktop"
if [[ -f "$PKG_ROOT/usr/share/icons/hicolor/256x256/apps/${APP_SLUG}.png" ]]; then
  chmod 644 "$PKG_ROOT/usr/share/icons/hicolor/256x256/apps/${APP_SLUG}.png"
fi

mkdir -p "$DIST_DIR"
DEB_OUT="${DIST_DIR}/${APP_SLUG}-${RELEASE_VERSION}-linux-${ARCH}.deb"
rm -f "$DEB_OUT"

if command -v fakeroot >/dev/null 2>&1; then
  fakeroot dpkg-deb --build "$PKG_ROOT" "$DEB_OUT"
else
  dpkg-deb --build "$PKG_ROOT" "$DEB_OUT"
fi

echo "DEB package created at: $DEB_OUT"
