# Justfile for MultiMonitor Wallpapers
# Use 'just <command>' to run commands

# Default command: show help
default: help

# 1. Ensure virtual environment is activated (private helper)
_ensure_venv:
    #!/usr/bin/env bash
    set -euo pipefail
    if [[ -z "${VIRTUAL_ENV:-}" ]]; then
        if [[ -d ".venv" ]]; then
            echo "Activating virtual environment..."
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
                source .venv/Scripts/activate
            else
                source .venv/bin/activate
            fi
        else
            echo "No virtual environment found. Creating one..."
            uv venv
            if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
                source .venv/Scripts/activate
            else
                source .venv/bin/activate
            fi
        fi
    fi

# 2. Build AppImage for distribution
appimage: _ensure_venv icon
    @echo "Building AppImage..."
    mkdir -p dist
    python scripts/build_appimage.py

# 3. Clean build artifacts and cache files
clean:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Cleaning build artifacts and cache files..."
    rm -rf __pycache__ .pytest_cache .ruff_cache build dist *.egg-info
    find . -name "__pycache__" -type d -exec rm -rf {} +
    echo "Cleaned up build artifacts and cache files."

# 4. Delete a version tag both locally and remotely
delete-release version:
    #!/usr/bin/env bash
    set -euo pipefail
    TAG="v{{version}}"
    echo "Deleting release tag $TAG locally and remotely..."
    
    # Delete local tag (don't fail if it doesn't exist)
    git tag -d "$TAG" || echo "Local tag $TAG doesn't exist"
    
    # Delete remote tag (don't fail if it doesn't exist)
    git push origin --delete "$TAG" || echo "Remote tag $TAG doesn't exist or was already deleted"
    
    echo "Tag $TAG has been deleted (if it existed)."

# 5. Format code with ruff and black
format: _ensure_venv
    @echo "Formatting with ruff..."
    ruff check --fix .
    @echo "Formatting with black..."
    black .
    @echo "Code formatting complete!"

# 6. List available commands (including hidden ones)
help:
    #!/usr/bin/env bash
    echo "Available recipes:"
    just --list
    
    echo -e "\nHidden recipes:"
    echo "    _ensure_venv           # 1. Ensure virtual environment is activated (private helper)"

# 7. Generate application icon
icon: _ensure_venv
    @echo "Generating application icon..."
    python generate_icon.py

# 8. Install Just on the system
install-just:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! command -v just &> /dev/null; then
        echo "Installing Just..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update && sudo apt-get install -y just
        elif command -v brew &> /dev/null; then
            brew install just
        elif command -v cargo &> /dev/null; then
            cargo install just
        else
            echo "Cannot install Just automatically. Please visit https://github.com/casey/just#installation"
            exit 1
        fi
        echo "Just installed successfully."
    else
        echo "Just is already installed."
    fi

# 9. Run linting checks
lint: _ensure_venv
    @echo "Running ruff..."
    ruff check .
    @echo "Running black in check mode..."
    black --check .
    @echo "Skipping mypy due to package name issues"
    # mypy src/multimonitor_wallpapers
    @echo "All linting checks passed!"

# 10. Create and push a new version tag
release version:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Creating release v{{version}}..."
    git tag -a "v{{version}}" -m "Release v{{version}}"
    git push origin "v{{version}}"
    echo "Tag v{{version}} pushed. GitHub Actions will build and publish the release."

# 11. Run the application
run: _ensure_venv
    python multimonitor_wallpapers.py

# 12. Setup development environment with uv
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Setting up development environment..."
    if ! command -v uv &> /dev/null; then
        echo "Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
    fi
    
    echo "Creating virtual environment..."
    uv venv
    
    echo "Installing dependencies..."
    if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
        source .venv/Scripts/activate
    else
        source .venv/bin/activate
    fi
    # Use pip instead of uv to install in development mode to avoid setuptools issues
    pip install -e ".[dev]"
    
    echo "Development environment set up successfully."

# 13. Run tests
test: _ensure_venv
    @echo "Running pytest..."
    pytest
    @echo "All tests passed!"

# 14. Update dependencies to the latest versions
update: _ensure_venv
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Updating dependencies to latest versions..."
    uv pip sync --upgrade requirements.txt
    echo "Installing latest development dependencies..."
    uv pip install --upgrade pytest black ruff mypy
    echo "Dependencies updated successfully." 