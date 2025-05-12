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

    # Create a Python entry script that uses the shebang line
    entry_script = f"{appdir}/usr/bin/multimonitor-wallpapers"
    with open(entry_script, "w", newline="\n") as f:
        f.write(
            r"""#!/usr/bin/env python3
# Entry point for MultiMonitor Wallpapers application

import os
import sys

# Add the application directory to the Python path
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

# Ensure Python can find modules in site-packages
python_version = '.'.join(sys.version.split('.')[:2])  # Get "3.12" from version
site_packages = f"/tmp/.mount_*/usr/lib/python{python_version}/site-packages"
import glob
for sp in glob.glob(site_packages):
    if sp not in sys.path and os.path.exists(sp):
        sys.path.insert(0, sp)
        break

# Import and run the main function
from multimonitor_wallpapers import main

if __name__ == "__main__":
    main()
"""
        )

    # Make it executable
    os.chmod(entry_script, 0o755)

    # Copy the application package to the correct location
    # We'll put it both in bin and in site-packages to ensure it can be found
    shutil.copytree(
        "src/multimonitor_wallpapers",
        f"{appdir}/usr/bin/multimonitor_wallpapers",
        dirs_exist_ok=True,
    )


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
            r"""#!/bin/bash
# Get the directory where the AppImage is mounted
HERE="$(dirname "$(readlink -f "${0}")")"

# Determine Python version dynamically
PYTHON_VERSION=$(ls "${HERE}/usr/bin/" | grep -E "^python3\.[0-9]+$" | head -n 1)
if [ -z "$PYTHON_VERSION" ]; then
    PYTHON_VERSION="python3"
fi

# Set up environment variables
export PATH="${HERE}/usr/bin:${PATH}"
export PYTHONHOME="${HERE}/usr"
export PYTHONPATH="${HERE}/usr/lib/${PYTHON_VERSION}/site-packages:${PYTHONPATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
export XDG_DATA_DIRS="${HERE}/usr/share:${XDG_DATA_DIRS}"
export QT_PLUGIN_PATH="${HERE}/usr/lib/${PYTHON_VERSION}/site-packages/PySide6/Qt/plugins"
export QML2_IMPORT_PATH="${HERE}/usr/lib/${PYTHON_VERSION}/site-packages/PySide6/Qt/qml"
export QT_QPA_PLATFORM_PLUGIN_PATH="${HERE}/usr/lib/${PYTHON_VERSION}/site-packages/PySide6/Qt/plugins/platforms"

# For debugging (uncomment if needed)
# echo "PYTHONHOME: ${PYTHONHOME}"
# echo "PYTHONPATH: ${PYTHONPATH}"
# echo "LD_LIBRARY_PATH: ${LD_LIBRARY_PATH}"
# echo "Python version: ${PYTHON_VERSION}"
# ls -la "${HERE}/usr/bin"
# ls -la "${HERE}/usr/lib/${PYTHON_VERSION}"

# Check if the bundled Python exists
if [ -f "${HERE}/usr/bin/${PYTHON_VERSION}" ]; then
    # Use the bundled Python interpreter
    exec "${HERE}/usr/bin/${PYTHON_VERSION}" "${HERE}/usr/bin/multimonitor-wallpapers"
else
    echo "Error: Python interpreter not found in AppImage"
    exit 1
fi
"""
        )

    # Make it executable
    os.chmod(apprun_path, 0o755)


def install_dependencies(appdir):
    """Install Python and required packages into AppDir."""
    # Find the system Python installation
    python_version = "3.12"
    python_cmd = f"python{python_version}"

    # Get Python's site-packages and stdlib directories
    print("Detecting Python paths...")
    python_paths = (
        run_command(
            [
                python_cmd,
                "-c",
                "import sys, os; "
                "print(sys.prefix); "
                "print(os.path.dirname(os.__file__)); "
                "print([p for p in sys.path if p.endswith('site-packages')][0])",
            ]
        )
        .strip()
        .split("\n")
    )

    sys_prefix = python_paths[0]
    stdlib_path = python_paths[1]
    site_packages_path = python_paths[2]

    print(f"Python prefix: {sys_prefix}")
    print(f"Python stdlib: {stdlib_path}")
    print(f"Python site-packages: {site_packages_path}")

    # Create a temporary virtual environment for installing our packages
    temp_venv = os.path.join(os.path.dirname(appdir), "temp_venv")
    run_command([python_cmd, "-m", "venv", temp_venv])

    # Install packages into the temporary venv
    pip_cmd = os.path.join(temp_venv, "bin", "pip")

    # First install uv
    run_command([pip_cmd, "install", "uv"])

    # Then use uv to install our dependencies
    uv_cmd = os.path.join(temp_venv, "bin", "uv")
    run_command([uv_cmd, "pip", "install", "PySide6==6.9.0", "pillow==11.2.1"])

    # Get the site-packages directory from the venv
    venv_site_packages = os.path.join(temp_venv, "lib", f"python{python_version}", "site-packages")

    # Create target directories in AppDir
    target_lib = os.path.join(appdir, "usr", "lib")
    target_python_lib = os.path.join(target_lib, f"python{python_version}")
    target_site_packages = os.path.join(target_python_lib, "site-packages")
    target_bin = os.path.join(appdir, "usr", "bin")

    os.makedirs(target_python_lib, exist_ok=True)
    os.makedirs(target_site_packages, exist_ok=True)
    os.makedirs(target_bin, exist_ok=True)

    # Copy Python binary
    python_binary = run_command(["which", python_cmd]).strip()
    shutil.copy2(python_binary, os.path.join(target_bin, os.path.basename(python_binary)))

    # Make a symbolic link from python3 to the specific version
    os.symlink(os.path.basename(python_binary), os.path.join(target_bin, "python3"))

    # Copy the Python standard library
    print("Copying Python standard library...")
    for item in os.listdir(stdlib_path):
        if item in ["__pycache__", "site-packages", "dist-packages"]:
            continue

        source = os.path.join(stdlib_path, item)
        target = os.path.join(target_python_lib, item)

        try:
            if os.path.isdir(source):
                shutil.copytree(source, target, symlinks=True, dirs_exist_ok=True)
            else:
                shutil.copy2(source, target)
        except Exception as e:
            print(f"Warning: Failed to copy {source}: {e}")

    # Copy essential modules from system site-packages
    print("Copying essential system modules...")
    essential_modules = ["_distutils_hack", "pip", "setuptools", "pkg_resources"]
    for module in essential_modules:
        source = os.path.join(site_packages_path, module)
        if os.path.exists(source):
            target = os.path.join(target_site_packages, module)
            try:
                if os.path.isdir(source):
                    shutil.copytree(source, target, symlinks=True, dirs_exist_ok=True)
                else:
                    shutil.copy2(source, target)
            except Exception as e:
                print(f"Warning: Failed to copy {source}: {e}")

    # Copy our installed packages from the temporary venv
    print("Copying installed packages...")
    for item in os.listdir(venv_site_packages):
        if item in ["__pycache__", "pip", "setuptools", "pkg_resources", "_distutils_hack"]:
            continue

        source = os.path.join(venv_site_packages, item)
        target = os.path.join(target_site_packages, item)

        try:
            if os.path.isdir(source):
                shutil.copytree(source, target, symlinks=True, dirs_exist_ok=True)
            else:
                shutil.copy2(source, target)
        except Exception as e:
            print(f"Warning: Failed to copy {source}: {e}")

    # Copy our application package to site-packages as well for better import support
    print("Copying application package to site-packages...")
    app_source = "src/multimonitor_wallpapers"
    app_target = os.path.join(target_site_packages, "multimonitor_wallpapers")
    try:
        shutil.copytree(app_source, app_target, symlinks=True, dirs_exist_ok=True)
    except Exception as e:
        print(f"Warning: Failed to copy application to site-packages: {e}")

    # Create an __init__.py in site-packages to make it a proper package
    with open(os.path.join(target_site_packages, "__init__.py"), "w") as f:
        f.write("# This file makes the site-packages directory a proper package\n")

    # Copy dynamic libraries that Python depends on
    print("Copying Python dynamic libraries...")
    ldd_output = run_command(["ldd", python_binary])
    for line in ldd_output.splitlines():
        if "=>" in line and "not found" not in line:
            parts = line.split("=>")
            if len(parts) >= 2:
                lib_path = parts[1].strip().split()[0]
                if lib_path and lib_path.startswith("/") and os.path.exists(lib_path):
                    lib_name = os.path.basename(lib_path)
                    # Skip system libraries that should be on all systems
                    if not (
                        lib_name.startswith("libc.so")
                        or lib_name.startswith("libpthread.so")
                        or lib_name.startswith("libdl.so")
                        or lib_name.startswith("libm.so")
                    ):
                        target = os.path.join(target_lib, lib_name)
                        if not os.path.exists(target):
                            print(f"Copying {lib_path} to {target}")
                            shutil.copy2(lib_path, target)

    # Clean up the temporary venv
    shutil.rmtree(temp_venv)

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

    # Build the AppImage with explicit architecture
    run_command(["env", "ARCH=x86_64", f"./{appimagetool}", "--no-appstream", appdir, output_path])

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
