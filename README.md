# Multi-Monitor Wallpapers App

## Description

The Multi-Monitor Wallpapers App is a Python-based desktop application designed for Linux systems running the Cinnamon desktop environment. It allows users to set different wallpapers for multiple monitors with ease. The app provides a user-friendly interface for selecting images, automatically assembles them into a single background image, and applies it across all connected monitors.

## Features

- Support for multiple monitors
- Intuitive graphical user interface
- Automatic image resizing and positioning
- Dark mode support
- Dependency validation
- Error handling with user feedback

## Requirements

- Python 3.12+
- PySide6
- Pillow (PIL)
- Cinnamon desktop environment
- Linux system with `gsettings`, `xrandr`, and ImageMagick's `convert` command

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/multi-monitor-wallpapers-app.git
   cd multi-monitor-wallpapers-app
   ```

2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

### Using the AppImage (Linux)

For Linux users, you can download and use the AppImage:

1. Download the latest AppImage from the [Releases](https://github.com/yourusername/multi-monitor-wallpapers-app/releases) page.
2. Make it executable:
   ```
   chmod +x MultiMonitor-*.AppImage
   ```
3. Run the application:
   ```
   ./MultiMonitor-*.AppImage
   ```

The AppImage is self-contained and does not require installation. It should work on most modern Linux distributions.

## Usage

1. Launch the application:
   ```
   python widget.py
   ```

2. Use the "Browse" buttons to select wallpaper images for each monitor.
3. Click "Apply" to set the wallpapers.
4. Use "Cancel" to clear your selections or "Quit" to exit the application.

## How It Works

1. The app detects connected monitors and their geometries using `xrandr`.
2. Users select image files for each monitor.
3. The app resizes and positions the images according to each monitor's resolution and position.
4. A combined wallpaper image is created and saved.
5. The app uses `gsettings` to apply the new wallpaper to the Cinnamon desktop.

## Development

The main application logic is contained in the `MultiMonitorApp` class in `widget.py`. The UI is created using PySide6, and image processing is done with Pillow.

To modify the UI:

1. Edit the `initUI` method in the `MultiMonitorApp` class.
2. If using Qt Designer, edit the `form.ui` file and regenerate `ui_form.py`.

### Developer Setup

1. Clone the repository and navigate to the project directory.

2. Install Just (recommended):
   ```
   # Linux/macOS with homebrew
   brew install just

   # Linux with apt
   sudo apt install just

   # With cargo
   cargo install just
   
   # Or use our helper script
   curl -LsSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
   ```

   If you don't want to install Just, you can use the usual Python tools directly.

3. Install uv (if not already installed):
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

4. Set up the development environment:
   ```
   just setup
   ```
   
   This will:
   - Create a virtual environment (.venv)
   - Install the package in development mode with all dev dependencies

5. Activate the virtual environment:
   ```
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

### Development Workflow

You can use the provided commands with `just`:

```bash
# List all available commands
just

# Run the application
just run

# Development tools
just lint        # Run linting checks
just format      # Format code
just test        # Run tests
just clean       # Clean build artifacts
just icon        # Generate application icon
just appimage    # Build AppImage for distribution

# Create a new release (e.g., "0.1.0")
just release 0.1.0
```

### Package Structure

- `widget.py`: Main application code
- `setup.py` and `pyproject.toml`: Packaging configuration
- `tests/`: Test directory
- `.github/workflows/`: CI configuration

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

The GNU General Public License v3.0 (GPLv3) is a free, copyleft license for software and other kinds of works. The licenses for most software and other practical works are designed to take away your freedom to share and change the works. By contrast, the GNU General Public License is intended to guarantee your freedom to share and change all versions of a program--to make sure it remains free software for all its users.

Key points of the GPLv3:

1. You can use the software for any purpose
2. You can change the software to suit your needs
3. You can share the software with your friends and neighbors
4. You can share the changes you make

However, if you distribute modified versions of the software, you must:

1. Clearly mark the software as modified
2. Distribute

## Acknowledgments

- PySide6 for the GUI framework
- Pillow for image processing
- Cinnamon desktop environment developers

## Troubleshooting

- If the wallpaper doesn't change immediately, try logging out and back in.
- Ensure all dependencies are installed and available in your system PATH.
- Check the console output for any error messages if the application fails.

## Future Improvements

- Add support for other desktop environments
- Implement drag-and-drop functionality for image selection
- Add preview functionality for the combined wallpaper
- Implement wallpaper cycling/slideshow feature

## Building and Distribution

### Building an AppImage

To build an AppImage for distribution:

1. Make sure you have the required dependencies:
   ```
   sudo apt-get install libfuse2 desktop-file-utils libglib2.0-bin
   ```

2. Build the AppImage:
   ```
   just appimage
   ```

3. The AppImage will be created in the `dist/` directory.

### Automated Builds with GitHub Actions

The project includes GitHub Actions workflows to automatically:

1. Run tests and linting checks on every push and pull request
2. Build and publish an AppImage when a new tag is created

To create a new release:

```bash
# Create and push a release tag
just release 0.2.0
```

GitHub Actions will automatically build the AppImage and create a release.
