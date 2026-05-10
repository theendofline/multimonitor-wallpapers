import logging
import os
import subprocess
import sys

from PIL import Image
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

logger = logging.getLogger(__name__)


class MultiMonitorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.files = []
        self.file_inputs = []

        self.init_ui()
        self.handle_dark_mode()

    def init_ui(self):
        self.setWindowTitle("Multi-Monitor Background App")
        self.setGeometry(300, 300, 1000, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        monitors = self.get_monitors_geometry()
        self.file_inputs = []
        file_layout = QHBoxLayout()
        for _i, monitor in enumerate(monitors):
            file_input = QLineEdit(self)
            file_input.setPlaceholderText(f"Select image for {monitor['name']}")
            file_input.setStyleSheet(
                "color: white; background-color: #353535;"
                if self.is_system_in_dark_mode()
                else "color: black; background-color: white;"
            )
            file_layout.addWidget(file_input)
            self.file_inputs.append(file_input)

            browse_button = QPushButton("Browse", self)
            browse_button.clicked.connect(lambda _, fi=file_input: self.browse_file(fi))
            file_layout.addWidget(browse_button)
        main_layout.addLayout(file_layout)

        button_layout = QHBoxLayout()
        ok_button = QPushButton("Apply", self)
        ok_button.clicked.connect(self.set_background)
        button_layout.addWidget(ok_button)
        cancel_button = QPushButton("Cancel", self)
        cancel_button.clicked.connect(self.clear_inputs)
        button_layout.addWidget(cancel_button)
        quit_button = QPushButton("Quit", self)
        quit_button.clicked.connect(self.close)
        button_layout.addWidget(quit_button)
        main_layout.addLayout(button_layout)

    def browse_file(self, file_input):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image File", "", "Images (*.jpg *.jpeg *.png)"
        )
        if file_name:
            file_input.setText(file_name)

    def clear_inputs(self):
        for file_input in self.file_inputs:
            file_input.clear()

    def set_background(self):
        self.files = [file_input.text() for file_input in self.file_inputs if file_input.text()]

        if len(self.files) < 1:
            self.statusBar().showMessage("Please select at least one image file.")
            return

        if not self.validate_dependencies():
            self.statusBar().showMessage(
                "Missing required dependencies (gsettings, xrandr, ImageMagick)."
            )
            return

        try:
            self.assemble_background_image(self.files)
            success = self.apply_background()
            if success:
                self.statusBar().showMessage(
                    "Background applied successfully. Please wait a moment for the changes to reflect."
                )
            else:
                self.statusBar().showMessage("Failed to apply background. Check logs for errors.")
        except Exception as e:
            logger.exception("Error setting background")
            self.statusBar().showMessage(f"Error setting background: {e}")

    def assemble_background_image(self, image_paths):
        monitors = self.get_monitors_geometry()
        desktop_env = self.detect_desktop_environment()

        # GNOME also writes to ~/.cinnamon/backgrounds for back-compat
        # if a user has switched DEs after first using this app on Cinnamon.
        if desktop_env == "gnome":
            output_dir = os.path.expanduser("~/.local/share/backgrounds")
            cinnamon_dir = os.path.expanduser("~/.cinnamon/backgrounds")
            if not os.path.exists(cinnamon_dir):
                os.makedirs(cinnamon_dir)
        else:
            output_dir = os.path.expanduser("~/.cinnamon/backgrounds")

        output_path = os.path.join(output_dir, "multiMonitorBackground.jpg")

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        total_width = max(
            monitor["offset"][0] + int(monitor["geometry"].split("x")[0]) for monitor in monitors
        )
        total_height = max(
            monitor["offset"][1] + int(monitor["geometry"].split("x")[1]) for monitor in monitors
        )

        logger.info("Total screen size: %dx%d", total_width, total_height)
        logger.info("Number of monitors: %d", len(monitors))
        logger.info("Detected desktop environment: %s", desktop_env)
        logger.info("Using output directory: %s", output_dir)

        background = Image.new("RGB", (total_width, total_height), (0, 0, 0))

        try:
            for i, monitor in enumerate(monitors):
                geometry = monitor["geometry"]
                offset_x, offset_y = monitor["offset"]
                # Cycle through provided images if fewer images than monitors.
                image_path = image_paths[i % len(image_paths)]

                logger.info(
                    "Monitor %d (%s): geometry=%s, offset=(%d, %d)",
                    i,
                    monitor["name"],
                    geometry,
                    offset_x,
                    offset_y,
                )

                with Image.open(image_path) as img:
                    img = img.convert("RGB")
                    mon_width, mon_height = map(int, geometry.split("x"))
                    img.thumbnail((mon_width, mon_height), Image.LANCZOS)

                    logger.debug("Image size after resize: %dx%d", img.width, img.height)

                    monitor_img = Image.new("RGB", (mon_width, mon_height), (0, 0, 0))
                    paste_x = (mon_width - img.width) // 2
                    paste_y = (mon_height - img.height) // 2
                    monitor_img.paste(img, (paste_x, paste_y))

                    background.paste(monitor_img, (offset_x, offset_y))

            background.save(output_path, "JPEG", quality=95)
            logger.info("Saved background image to: %s", output_path)

            if desktop_env == "gnome":
                cinnamon_path = os.path.join(cinnamon_dir, "multiMonitorBackground.jpg")
                background.save(cinnamon_path, "JPEG", quality=95)
                logger.info("Also saved to Cinnamon location: %s", cinnamon_path)

        except Exception:
            logger.exception("Error assembling background image")
            raise

        return output_path

    def detect_desktop_environment(self):
        desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
        logger.debug("XDG_CURRENT_DESKTOP is: %s", desktop)

        if "cinnamon" in desktop:
            return "cinnamon"
        elif "gnome" in desktop or "ubuntu" in desktop:
            return "gnome"
        return "unknown"

    def apply_background(self):
        desktop_env = self.detect_desktop_environment()

        if desktop_env == "gnome":
            output_path = os.path.expanduser(
                "~/.local/share/backgrounds/multiMonitorBackground.jpg"
            )
            cinnamon_path = os.path.expanduser("~/.cinnamon/backgrounds/multiMonitorBackground.jpg")
            if not os.path.exists(output_path) and os.path.exists(cinnamon_path):
                output_path = cinnamon_path
        else:
            output_path = os.path.expanduser("~/.cinnamon/backgrounds/multiMonitorBackground.jpg")

        logger.info("Using wallpaper file: %s", output_path)
        logger.debug("File exists: %s", os.path.exists(output_path))

        try:
            if desktop_env == "cinnamon":
                schema = "org.cinnamon.desktop.background"
                options = "spanned"

                subprocess.check_call(
                    ["gsettings", "set", schema, "picture-uri", f"file://{output_path}"]
                )
                subprocess.check_call(["gsettings", "set", schema, "picture-options", options])

                # Cinnamon caches the URI; clear-then-set forces a refresh
                # so the picture is reloaded from disk.
                subprocess.check_call(["gsettings", "set", schema, "picture-uri", "''"])
                subprocess.check_call(
                    ["gsettings", "set", schema, "picture-uri", f"file://{output_path}"]
                )

            elif desktop_env == "gnome":
                schema = "org.gnome.desktop.background"

                # Different GNOME versions accept different picture-options
                # values; try them in order of preference.
                for option in ["spanned", "zoom", "stretched"]:
                    try:
                        subprocess.check_call(
                            ["gsettings", "set", schema, "picture-uri", f"file://{output_path}"]
                        )
                        subprocess.check_call(
                            ["gsettings", "set", schema, "picture-options", option]
                        )
                        logger.info("Successfully set %s for GNOME", option)
                        break
                    except subprocess.CalledProcessError:
                        logger.warning("Option %s failed for GNOME, trying next", option)

                if self.is_system_in_dark_mode():
                    try:
                        subprocess.check_call(
                            [
                                "gsettings",
                                "set",
                                schema,
                                "picture-uri-dark",
                                f"file://{output_path}",
                            ]
                        )
                        logger.info("Set dark mode wallpaper as well")
                    except Exception:
                        # picture-uri-dark is optional; older GNOME lacks it.
                        pass

            else:
                schema = "org.cinnamon.desktop.background"
                options = "spanned"
                subprocess.check_call(
                    ["gsettings", "set", schema, "picture-uri", f"file://{output_path}"]
                )
                subprocess.check_call(["gsettings", "set", schema, "picture-options", options])

            return True

        except subprocess.CalledProcessError:
            logger.exception("Error applying background")
            return False

    def get_screen_geometry(self):
        result = subprocess.run(["xrandr"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "current" in line:
                parts = line.split("current ")[1].split(",")[0].strip().split()
                if len(parts) >= 2:
                    return f"{parts[0]}x{parts[2]}"
        return "1920x1080"

    def get_monitors_geometry(self):
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
                    if "+" in geometry:
                        geometry_parts = geometry.split("+")
                        if len(geometry_parts) >= 3:
                            size = geometry_parts[0]
                            offset_x = int(geometry_parts[1])
                            offset_y = int(geometry_parts[2])
                            monitors.append(
                                {"name": name, "geometry": size, "offset": (offset_x, offset_y)}
                            )

        if not monitors:
            monitors.append({"name": "default", "geometry": "1920x1080", "offset": (0, 0)})

        # Sort by x offset so monitor 0 is leftmost; matches user expectation.
        monitors.sort(key=lambda m: m["offset"][0])

        logger.info("Detected monitors:")
        for monitor in monitors:
            logger.info(
                "  %s: %s at offset %s",
                monitor["name"],
                monitor["geometry"],
                monitor["offset"],
            )

        return monitors

    def handle_dark_mode(self):
        palette = self.palette()
        if self.is_system_in_dark_mode():
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

    def is_system_in_dark_mode(self):
        try:
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                capture_output=True,
                text=True,
            )
            return "dark" in result.stdout.lower()
        except Exception:
            return False

    def validate_dependencies(self):
        for command in ["gsettings", "xrandr", "convert"]:
            if (
                subprocess.call(
                    ["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                != 0
            ):
                logger.error("Dependency %r is missing.", command)
                return False
        return True


def main():
    logging.basicConfig(
        level=os.environ.get("MULTIMONITOR_LOG_LEVEL", "INFO").upper(),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    app = QApplication(sys.argv)
    window = MultiMonitorApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
