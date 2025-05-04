# Import necessary modules
import sys  # For system-specific parameters and functions
import subprocess  # For running system commands
import os  # For interacting with the operating system

# Import required PySide6 modules for GUI
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel,
                               QVBoxLayout, QWidget, QFileDialog, QHBoxLayout, QLineEdit)
from PySide6.QtGui import QPixmap, QPalette, QColor
from PySide6.QtCore import Qt

# Import PIL for image processing
from PIL import Image


class MultiMonitorApp(QMainWindow):
    def __init__(self):
        super(MultiMonitorApp, self).__init__()
        self.file_inputs = None
        self.initUI()  # Initialize the user interface
        self.files = []  # List to store selected image files
        self.handleDarkMode()  # Set up dark mode if system is using it

    def initUI(self):
        # Set up the main window
        self.setWindowTitle("Multi-Monitor Background App")
        self.setGeometry(300, 300, 1000, 400)

        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create file selection layout
        file_layout = QHBoxLayout()
        self.file_inputs = [QLineEdit(self), QLineEdit(self)]
        for file_input in self.file_inputs:
            file_input.setPlaceholderText("Select an image file")
            # Set style based on dark mode
            file_input.setStyleSheet(
                "color: white; background-color: #353535;" if self.isSystemInDarkMode() else "color: black; background-color: white;")
            file_layout.addWidget(file_input)

            # Add browse button for each file input
            browse_button = QPushButton("Browse", self)
            browse_button.clicked.connect(lambda checked, fi=file_input: self.browseFile(fi))
            file_layout.addWidget(browse_button)

        main_layout.addLayout(file_layout)

        # Create buttons layout (Apply, Cancel, Quit)
        button_layout = QHBoxLayout()

        ok_button = QPushButton("Apply", self)
        ok_button.clicked.connect(self.setBackground)
        button_layout.addWidget(ok_button)

        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.clearInputs)
        button_layout.addWidget(cancel_button)

        quit_button = QPushButton("Quit", self)
        quit_button.clicked.connect(self.close)
        button_layout.addWidget(quit_button)

        main_layout.addLayout(button_layout)

    def browseFile(self, file_input):
        # Open file dialog to select an image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.jpg *.jpeg *.png)")
        if file_name:
            file_input.setText(file_name)

    def clearInputs(self):
        # Clear all file input fields
        for file_input in self.file_inputs:
            file_input.clear()

    def setBackground(self):
        # Get selected files from inputs
        self.files = [file_input.text() for file_input in self.file_inputs if file_input.text()]

        if len(self.files) < 1:
            self.statusBar().showMessage("Please select at least one image file.")
            return

        # Validate required dependencies
        if not self.validateDependencies():
            self.statusBar().showMessage("Missing required dependencies (gsettings, xrandr, ImageMagick).")
            return

        # Set background
        try:
            self.assembleBackgroundImage(self.files)
            success = self.applyBackground()
            if success:
                self.statusBar().showMessage(
                    "Background applied successfully. Please wait a moment for the changes to reflect.")
            else:
                self.statusBar().showMessage("Failed to apply background. Check logs for errors.")
        except Exception as e:
            print(f"Error setting background: {e}")
            self.statusBar().showMessage(f"Error setting background: {e}")

    def assembleBackgroundImage(self, image_paths):
        monitors = self.getMonitorsGeometry()
        output_dir = os.path.expanduser("~/.cinnamon/backgrounds")
        output_path = os.path.join(output_dir, "multiMonitorBackground.jpg")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Calculate total width and height
        total_width = max(monitor['offset'][0] + int(monitor['geometry'].split('x')[0]) for monitor in monitors)
        total_height = max(monitor['offset'][1] + int(monitor['geometry'].split('x')[1]) for monitor in monitors)

        print(f"Total screen size: {total_width}x{total_height}")
        print(f"Number of monitors: {len(monitors)}")

        # Create a blank canvas for the full screen size
        background = Image.new('RGB', (total_width, total_height), (0, 0, 0))

        try:
            for i, monitor in enumerate(monitors):
                geometry = monitor['geometry']
                offset_x, offset_y = monitor['offset']
                image_path = image_paths[i % len(image_paths)]

                print(f"Monitor {i} ({monitor['name']}): geometry={geometry}, offset=({offset_x}, {offset_y})")

                # Open and resize the image
                with Image.open(image_path) as img:
                    img = img.convert('RGB')  # Ensure the image is in RGB mode
                    mon_width, mon_height = map(int, geometry.split('x'))
                    img.thumbnail((mon_width, mon_height), Image.LANCZOS)

                    print(f"  Image size after resize: {img.width}x{img.height}")

                    # Create a new image with the correct size and paste the resized image
                    monitor_img = Image.new('RGB', (mon_width, mon_height), (0, 0, 0))
                    paste_x = (mon_width - img.width) // 2
                    paste_y = (mon_height - img.height) // 2
                    monitor_img.paste(img, (paste_x, paste_y))

                    # Paste the monitor image onto the main canvas
                    background.paste(monitor_img, (offset_x, offset_y))

            # Save the final image
            background.save(output_path, 'JPEG', quality=95)
            print(f"Saved background image to: {output_path}")

        except Exception as e:
            print(f"Error assembling background image: {e}")
            raise

        return output_path

    def applyBackground(self):
        output_path = os.path.expanduser("~/.cinnamon/backgrounds/multiMonitorBackground.jpg")
        try:
            # Set the background for all monitors
            subprocess.check_call([
                "gsettings", "set",
                "org.cinnamon.desktop.background",
                "picture-uri", f"file://{output_path}"
            ])
            subprocess.check_call([
                "gsettings", "set",
                "org.cinnamon.desktop.background",
                "picture-options", "spanned"
            ])

            # Refresh the Cinnamon settings
            subprocess.check_call(["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", "''"])
            subprocess.check_call(
                ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", f"file://{output_path}"])

            return True
        except subprocess.CalledProcessError as e:
            print(f"Error applying background: {e}")
            return False

    def getScreenGeometry(self):
        result = subprocess.run(["xrandr"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "current" in line:
                parts = line.split("current ")[1].split(",")[0].strip().split()
                if len(parts) >= 2:
                    return f"{parts[0]}x{parts[2]}"
        return "1920x1080"  # Default fallback

    def getMonitorsGeometry(self):
        result = subprocess.run(["xrandr", "--query"], capture_output=True, text=True)
        monitors = []
        for line in result.stdout.splitlines():
            if " connected" in line:
                parts = line.split()
                name = parts[0]
                if "primary" in parts:
                    parts.remove("primary")
                if len(parts) >= 3:
                    geometry = parts[2]
                    if '+' in geometry:
                        geometry_parts = geometry.split('+')
                        if len(geometry_parts) >= 3:
                            size = geometry_parts[0]
                            offset_x = int(geometry_parts[1])
                            offset_y = int(geometry_parts[2])
                            monitors.append({'name': name, 'geometry': size, 'offset': (offset_x, offset_y)})

        if not monitors:
            # Fallback to a single monitor setup if no valid monitors are detected
            monitors.append({'name': 'default', 'geometry': '1920x1080', 'offset': (0, 0)})

        # Sort monitors by their x offset to ensure correct order
        monitors.sort(key=lambda m: m['offset'][0])

        print("Detected monitors:")
        for monitor in monitors:
            print(f"  {monitor['name']}: {monitor['geometry']} at offset {monitor['offset']}")

        return monitors

    # Set up the palette based on the system's dark mode setting
    def handleDarkMode(self):
        palette = self.palette()
        if self.isSystemInDarkMode():
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.white)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)

        self.setPalette(palette)

    def isSystemInDarkMode(self):
        try:
            result = subprocess.run(["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                                    capture_output=True, text=True)
            return 'dark' in result.stdout.lower()
        except Exception as e:
            return False

    def validateDependencies(self):
        # Check if required commands are available
        for command in ["gsettings", "xrandr", "convert"]:
            if subprocess.call(["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
                print(f"Dependency '{command}' is missing.")
                return False
        return True

def main():
    app = QApplication(sys.argv)
    window = MultiMonitorApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 