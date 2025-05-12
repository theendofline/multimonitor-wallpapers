#!/usr/bin/env python3
"""
Script to build an AppImage for the MultiMonitor Wallpapers application.
This script handles:
1. Creating the necessary AppDir structure
2. Installing required dependencies
3. Generating the desktop and icon files
4. Building the AppImage using appimagetool
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run_command(cmd, cwd=None):
    """Run a command and return its output."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        print(f"Error: {result.stderr}")
        sys.exit(result.returncode)
    return result.stdout


def create_appdir(appdir):
    """Create the AppDir directory structure."""
    print(f"Creating AppDir at {appdir}")

    # Create required directories
    os.makedirs(f"{appdir}/usr/bin", exist_ok=True)
    os.makedirs(f"{appdir}/usr/lib", exist_ok=True)
    os.makedirs(f"{appdir}/usr/share/applications", exist_ok=True)
    os.makedirs(f"{appdir}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)

    # Copy the application package (src/multimonitor_wallpapers)
    shutil.copytree(
        "src/multimonitor_wallpapers",
        f"{appdir}/usr/bin/multimonitor_wallpapers",
        dirs_exist_ok=True,
    )

    # Copy the entry script and ensure LF endings
    with (
        open("multimonitor_wallpapers.py", "rb") as src,
        open(f"{appdir}/usr/bin/multimonitor-wallpapers", "wb") as dst,
    ):
        content = src.read().replace(b"\r\n", b"\n")
        dst.write(content)
    os.chmod(f"{appdir}/usr/bin/multimonitor-wallpapers", 0o755)


def create_desktop_file(appdir):
    """Create desktop entry file."""
    desktop_file = f"{appdir}/usr/share/applications/multimonitor-wallpapers.desktop"
    with open(desktop_file, "w") as f:
        f.write(
            """[Desktop Entry]
Name=MultiMonitor Wallpapers
Comment=Set different wallpapers for multiple monitors
Exec=multimonitor-wallpapers
Icon=multimonitor-wallpapers
Type=Application
Categories=Utility;Graphics;
Terminal=false
StartupNotify=true
"""
        )

    # Also copy to AppDir root as required by AppImage spec
    shutil.copy(desktop_file, f"{appdir}/multimonitor-wallpapers.desktop")


def create_icon(appdir):
    """Create application icon or use existing one."""
    # For this example, we'll generate a simple icon if one doesn't exist
    # In a real app, you'd use your app's icon
    icon_path = Path("assets/icon.png")

    if not icon_path.exists():
        print("No icon found. Generating a simple placeholder icon...")
        os.makedirs("assets", exist_ok=True)

        try:
            from PIL import Image, ImageDraw

            # Create a simple 256x256 icon
            img = Image.new("RGB", (256, 256), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.rectangle([20, 20, 236, 236], outline=(255, 255, 255), width=5)
            d.rectangle([60, 60, 120, 120], fill=(255, 255, 255))
            d.rectangle([136, 60, 196, 120], fill=(255, 255, 255))
            d.rectangle([60, 136, 196, 196], fill=(255, 255, 255))

            img.save(icon_path)
        except ImportError:
            print("Pillow not available. Using fallback solution.")
            # Fallback to copying a system icon if Pillow is not available
            with open(icon_path, "wb") as f:
                f.write(b"")  # Create empty file as fallback

    # Copy icon to AppDir
    icon_dest = f"{appdir}/usr/share/icons/hicolor/256x256/apps/multimonitor-wallpapers.png"
    shutil.copy(icon_path, icon_dest)

    # Also copy to AppDir root as required by AppImage spec
    shutil.copy(icon_path, f"{appdir}/multimonitor-wallpapers.png")


def create_apprun(appdir):
    """Create AppRun executable script."""
    apprun_path = f"{appdir}/AppRun"

    with open(apprun_path, "w", newline="\n") as f:
        f.write(
            """#!/bin/bash
# Get the directory where the AppImage is mounted
HERE="$(dirname "$(readlink -f "${0}")")"

# Set up environment variables
export PATH="${HERE}/usr/bin:${PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3.12/site-packages:${PYTHONPATH}"
export PYTHONHOME="${HERE}/usr"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
export XDG_DATA_DIRS="${HERE}/usr/share:${XDG_DATA_DIRS}"
export QT_PLUGIN_PATH="${HERE}/usr/lib/python3.12/site-packages/PySide6/Qt/plugins"
export QML2_IMPORT_PATH="${HERE}/usr/lib/python3.12/site-packages/PySide6/Qt/qml"
export QT_QPA_PLATFORM_PLUGIN_PATH="${HERE}/usr/lib/python3.12/site-packages/PySide6/Qt/plugins/platforms"

# Log environment for debugging (uncomment if needed)
# echo "LD_LIBRARY_PATH: ${LD_LIBRARY_PATH}"
# echo "PYTHONPATH: ${PYTHONPATH}"
# echo "QT_PLUGIN_PATH: ${QT_PLUGIN_PATH}"

# Launch the application
"${HERE}/usr/bin/multimonitor-wallpapers" "$@"
"""
        )

    # Make it executable
    os.chmod(apprun_path, 0o755)


def install_dependencies(appdir):
    """Install Python and required packages into AppDir."""
    # Create a virtual environment inside the AppDir
    venv_path = f"{appdir}/usr/venv"
    run_command(["python3.12", "-m", "venv", venv_path])

    # Install dependencies using uv
    run_command([f"{venv_path}/bin/pip", "install", "uv"])

    # Install PySide6 and Pillow with specific versions for stability
    run_command(
        [
            f"{venv_path}/bin/uv",
            "pip",
            "install",
            "PySide6==6.9.0",  # Specify exact version for stability
            "pillow==11.2.1",  # Specify exact version for stability
        ]
    )

    print("Copying Python packages to AppDir...")
    # Copy installed packages to the AppDir lib directory
    site_packages = f"{venv_path}/lib/python3.12/site-packages"
    target_lib = f"{appdir}/usr/lib/python3.12/site-packages"
    os.makedirs(target_lib, exist_ok=True)

    for item in os.listdir(site_packages):
        if item.startswith("__pycache__"):
            continue
        source = os.path.join(site_packages, item)
        target = os.path.join(target_lib, item)
        if os.path.isdir(source):
            shutil.copytree(source, target, dirs_exist_ok=True)
        else:
            shutil.copy2(source, target)

    # Copy necessary system libraries for Qt
    copy_system_libraries(appdir)


def copy_system_libraries(appdir):
    """Copy system libraries needed by PySide6/Qt."""
    print("Copying system libraries for Qt...")
    target_lib = f"{appdir}/usr/lib"

    # Find and copy Qt dependencies from system
    try:
        # Use ldd to find dependencies of PySide6's core libraries
        qt_libs_path = f"{appdir}/usr/lib/python3.12/site-packages/PySide6"
        if os.path.exists(qt_libs_path):
            core_so = os.path.join(qt_libs_path, "libpyside6.abi3.so.6.9")
            if not os.path.exists(core_so):
                # Try to find any .so file if the specific one doesn't exist
                so_files = [f for f in os.listdir(qt_libs_path) if f.endswith(".so")]
                if so_files:
                    core_so = os.path.join(qt_libs_path, so_files[0])
                else:
                    print("Warning: Could not find PySide6 core library")
                    return

            print(f"Finding dependencies for: {core_so}")
            ldd_output = run_command(["ldd", core_so])

            # Parse ldd output to find libraries
            for line in ldd_output.splitlines():
                if "=>" in line and "not found" not in line:
                    lib_path = line.split("=>")[1].strip().split()[0]
                    if lib_path and lib_path.startswith("/"):
                        lib_name = os.path.basename(lib_path)
                        # Skip system libraries that should be on all systems
                        if not (
                            lib_name.startswith("libc.so")
                            or lib_name.startswith("libstdc++.so")
                            or lib_name.startswith("libdl.so")
                            or lib_name.startswith("libm.so")
                            or lib_name.startswith("libpthread.so")
                        ):
                            target = os.path.join(target_lib, lib_name)
                            if not os.path.exists(target):
                                print(f"Copying {lib_path} to {target}")
                                shutil.copy2(lib_path, target)
    except Exception as e:
        print(f"Warning: Error copying system libraries: {e}")
        # Continue despite errors


def download_appimagetool():
    """Download appimagetool if it doesn't exist."""
    appimagetool_path = Path("appimagetool-x86_64.AppImage")

    if not appimagetool_path.exists():
        print("Downloading appimagetool...")
        url = "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage"
        run_command(["curl", "-L", "-o", str(appimagetool_path), url])
        os.chmod(appimagetool_path, 0o755)

    return appimagetool_path


def build_appimage(appdir, output_path):
    """Build the AppImage using appimagetool."""
    print("Building AppImage...")

    appimagetool = download_appimagetool()

    # Build the AppImage
    run_command([f"./{appimagetool}", "--no-appstream", appdir, output_path])

    print(f"AppImage created: {output_path}")


def main():
    """Main function to build the AppImage."""
    print("Starting AppImage build process...")

    # Create a temporary directory for AppDir
    with tempfile.TemporaryDirectory() as temp_dir:
        appdir = f"{temp_dir}/MultiMonitor.AppDir"

        # Create AppDir structure
        create_appdir(appdir)

        # Create desktop and icon files
        create_desktop_file(appdir)
        create_icon(appdir)

        # Create AppRun script
        create_apprun(appdir)

        # Install dependencies
        install_dependencies(appdir)

        # Build AppImage
        output_dir = "dist"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.abspath(f"{output_dir}/MultiMonitor-x86_64.AppImage")

        build_appimage(appdir, output_path)

    print("AppImage build completed successfully!")


if __name__ == "__main__":
    main()
