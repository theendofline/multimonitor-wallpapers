# Justfile for MultiMonitor Wallpapers
# Use 'just <command>' to run commands

# Default command: show help
default: help

# 1. Ensure virtual environment (private helper)
_ensure_venv:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! command -v uv &> /dev/null; then
        echo "uv is not installed. Install from https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
    if [[ ! -d .venv ]]; then
        echo "Creating .venv and syncing from uv.lock..."
        uv sync --frozen --extra dev --extra build
    fi
    if [[ -z "${VIRTUAL_ENV:-}" ]]; then
        echo "Activating virtual environment..."
        if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
            source .venv/Scripts/activate
        else
            source .venv/bin/activate
        fi
    fi

# 2. Build AppImage for distribution
appimage: _ensure_venv
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Ensuring build extras are installed..."
    uv sync --frozen --extra dev --extra build
    echo "Building AppImage..."
    mkdir -p dist
    uv run python scripts/build_appimage.py

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

# 7. Install Just on the system
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

# 8. Run linting checks
lint: _ensure_venv
    @echo "Running ruff..."
    ruff check .
    @echo "Running black in check mode..."
    black --check .
    @echo "Running mypy..."
    mypy src/multimonitor_wallpapers
    @echo "All linting checks passed!"

# 9. Create and push a new version tag
release version:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Creating release v{{version}}..."
    git tag -a "v{{version}}" -m "Release v{{version}}"
    git push origin "v{{version}}"
    echo "Tag v{{version}} pushed. GitHub Actions will build and publish the release."

# 10. Run the application
run: _ensure_venv
    uv run multimonitor-wallpapers

# 11. Setup development environment (uv lockfile)
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Setting up development environment..."
    if ! command -v uv &> /dev/null; then
        echo "Installing uv..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi
    uv sync --frozen --extra dev --extra build
    echo "Development environment ready (.venv). Activate with: source .venv/bin/activate"

# 12. Run tests
test: _ensure_venv
    @echo "Running pytest..."
    pytest
    @echo "All tests passed!"

# 13. Refresh lockfile and resync environment
update: _ensure_venv
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Upgrading locked dependencies (respects ranges in pyproject.toml)..."
    uv lock --upgrade
    uv sync --frozen --extra dev --extra build
    echo "Lock updated (uv.lock) and .venv synced."
