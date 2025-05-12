#!/usr/bin/env python3
"""
Development helper script for multimonitor-wallpapers project.
Automates common development tasks.
"""

import argparse
import os
import subprocess
import sys


def run_command(command, capture_output=False):
    """Run a command and return its output if requested."""
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=capture_output, text=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        if capture_output and result.stderr:
            print(result.stderr)
        sys.exit(result.returncode)
    return result.stdout if capture_output else None


def setup_env():
    """Set up development environment using uv."""
    if not os.path.exists(".venv"):
        run_command(["uv", "venv"])

    run_command(["uv", "pip", "install", "-e", ".[dev]"])
    print("Development environment set up successfully.")


def lint():
    """Run linting tools."""
    print("Running ruff...")
    run_command(["ruff", "check", "."])

    print("Running black in check mode...")
    run_command(["black", "--check", "."])

    print("Running mypy...")
    run_command(["mypy", "widget.py"])

    print("All linting checks passed!")


def format_code():
    """Format code with ruff and black."""
    print("Formatting with ruff...")
    run_command(["ruff", "check", "--fix", "."])

    print("Formatting with black...")
    run_command(["black", "."])

    print("Code formatting complete!")


def test():
    """Run tests."""
    print("Running pytest...")
    run_command(["pytest"])
    print("All tests passed!")


def clean():
    """Clean build artifacts and cached files."""
    directories = [
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        "build",
        "dist",
        "*.egg-info",
    ]

    for directory in directories:
        run_command(["rm", "-rf", directory])

    print("Cleaned up build artifacts and cache files.")


def build_appimage():
    """Build an AppImage for distribution."""
    print("Building AppImage...")

    # Make sure the scripts directory exists
    if not os.path.exists("scripts"):
        os.makedirs("scripts")

    # Check if the build script exists
    if not os.path.exists("scripts/build_appimage.py"):
        print("Error: scripts/build_appimage.py not found")
        return

    # Run the build script
    run_command(["python", "scripts/build_appimage.py"])

    print("AppImage build complete. Check dist/ directory for the output file.")


def main():
    """Parse arguments and run the requested command."""
    parser = argparse.ArgumentParser(description="Development helper script")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    subparsers.add_parser("setup", help="Set up development environment")
    subparsers.add_parser("lint", help="Run linting tools")
    subparsers.add_parser("format", help="Format code")
    subparsers.add_parser("test", help="Run tests")
    subparsers.add_parser("clean", help="Clean build artifacts")
    subparsers.add_parser("appimage", help="Build AppImage for distribution")

    args = parser.parse_args()

    if args.command == "setup":
        setup_env()
    elif args.command == "lint":
        lint()
    elif args.command == "format":
        format_code()
    elif args.command == "test":
        test()
    elif args.command == "clean":
        clean()
    elif args.command == "appimage":
        build_appimage()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
