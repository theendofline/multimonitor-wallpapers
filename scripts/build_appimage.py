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
    
    # Copy the application script
    shutil.copy("multimonitor_wallpapers.py", f"{appdir}/usr/bin/multimonitor-wallpapers")
    
    # Make it executable
    os.chmod(f"{appdir}/usr/bin/multimonitor-wallpapers", 0o755)


def create_desktop_file(appdir):
    """Create desktop entry file."""
    desktop_file = f"{appdir}/usr/share/applications/multimonitor-wallpapers.desktop"
    with open(desktop_file, 'w') as f:
        f.write("""[Desktop Entry]
Name=MultiMonitor Wallpapers
Comment=Set different wallpapers for multiple monitors
Exec=multimonitor-wallpapers
Icon=multimonitor-wallpapers
Type=Application
Categories=Utility;Graphics;
Terminal=false
StartupNotify=true
""")
    
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
            img = Image.new('RGB', (256, 256), color=(73, 109, 137))
            d = ImageDraw.Draw(img)
            d.rectangle([20, 20, 236, 236], outline=(255, 255, 255), width=5)
            d.rectangle([60, 60, 120, 120], fill=(255, 255, 255))
            d.rectangle([136, 60, 196, 120], fill=(255, 255, 255))
            d.rectangle([60, 136, 196, 196], fill=(255, 255, 255))
            
            img.save(icon_path)
        except ImportError:
            print("Pillow not available. Using fallback solution.")
            # Fallback to copying a system icon if Pillow is not available
            with open(icon_path, 'wb') as f:
                f.write(b'')  # Create empty file as fallback
    
    # Copy icon to AppDir
    icon_dest = f"{appdir}/usr/share/icons/hicolor/256x256/apps/multimonitor-wallpapers.png"
    shutil.copy(icon_path, icon_dest)
    
    # Also copy to AppDir root as required by AppImage spec
    shutil.copy(icon_path, f"{appdir}/multimonitor-wallpapers.png")


def create_apprun(appdir):
    """Create AppRun executable script."""
    apprun_path = f"{appdir}/AppRun"
    
    with open(apprun_path, 'w') as f:
        f.write("""#!/bin/bash
HERE="$(dirname "$(readlink -f "${0}")")"
export PATH="${HERE}/usr/bin:${PATH}"
export PYTHONPATH="${HERE}/usr/lib/python3.12/site-packages:${PYTHONPATH}"
export LD_LIBRARY_PATH="${HERE}/usr/lib:${LD_LIBRARY_PATH}"
export XDG_DATA_DIRS="${HERE}/usr/share:${XDG_DATA_DIRS}"

# Launch the application
"${HERE}/usr/bin/multimonitor-wallpapers" "$@"
""")
    
    # Make it executable
    os.chmod(apprun_path, 0o755)


def install_dependencies(appdir):
    """Install Python and required packages into AppDir."""
    # Create a virtual environment inside the AppDir
    venv_path = f"{appdir}/usr/venv"
    run_command(["python3.12", "-m", "venv", venv_path])
    
    # Install dependencies using uv
    run_command([
        f"{venv_path}/bin/pip", "install", "uv"
    ])
    
    run_command([
        f"{venv_path}/bin/uv", "pip", "install", "PySide6", "pillow"
    ])
    
    # Copy installed packages to the AppDir lib directory
    site_packages = f"{venv_path}/lib/python3.12/site-packages"
    target_lib = f"{appdir}/usr/lib/python3.12/site-packages"
    os.makedirs(target_lib, exist_ok=True)
    
    for item in os.listdir(site_packages):
        if item.startswith('__pycache__'):
            continue
        source = os.path.join(site_packages, item)
        target = os.path.join(target_lib, item)
        if os.path.isdir(source):
            shutil.copytree(source, target, dirs_exist_ok=True)
        else:
            shutil.copy2(source, target)


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
    run_command([
        f"./{appimagetool}", "--no-appstream",
        appdir,
        output_path
    ])
    
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