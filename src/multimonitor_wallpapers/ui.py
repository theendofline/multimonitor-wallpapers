"""PySide6 main window. Glue layer over `monitors`, `compositor`, `desktop`."""

from __future__ import annotations

import logging
import os
import sys

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

from . import compositor, desktop, monitors

logger = logging.getLogger(__name__)


class MultiMonitorApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.files: list[str] = []
        self.file_inputs: list[QLineEdit] = []

        self.init_ui()
        self.handle_dark_mode()

    def init_ui(self) -> None:
        self.setWindowTitle("Multi-Monitor Background App")
        self.setGeometry(300, 300, 1000, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        detected = monitors.get_monitors()
        self.file_inputs = []
        file_layout = QHBoxLayout()
        for monitor in detected:
            file_input = QLineEdit(self)
            file_input.setPlaceholderText(f"Select image for {monitor['name']}")
            file_input.setStyleSheet(
                "color: white; background-color: #353535;"
                if desktop.is_system_in_dark_mode()
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

    def browse_file(self, file_input: QLineEdit) -> None:
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Image File", "", "Images (*.jpg *.jpeg *.png)"
        )
        if file_name:
            file_input.setText(file_name)

    def clear_inputs(self) -> None:
        for file_input in self.file_inputs:
            file_input.clear()

    def set_background(self) -> None:
        self.files = [file_input.text() for file_input in self.file_inputs if file_input.text()]

        if len(self.files) < 1:
            self.statusBar().showMessage("Please select at least one image file.")
            return

        if not desktop.validate_dependencies():
            self.statusBar().showMessage(
                "Missing required dependencies (gsettings, xrandr, ImageMagick)."
            )
            return

        try:
            desktop_env = desktop.detect_desktop_environment()
            output_paths = desktop.wallpaper_output_paths(desktop_env)
            compositor.compose_wallpaper(monitors.get_monitors(), self.files, output_paths)
            success = desktop.apply_background(output_paths[0], desktop_env)
            if success:
                self.statusBar().showMessage(
                    "Background applied successfully. "
                    "Please wait a moment for the changes to reflect."
                )
            else:
                self.statusBar().showMessage("Failed to apply background. Check logs for errors.")
        except Exception as e:
            logger.exception("Error setting background")
            self.statusBar().showMessage(f"Error setting background: {e}")

    def handle_dark_mode(self) -> None:
        palette = self.palette()
        if desktop.is_system_in_dark_mode():
            white = Qt.GlobalColor.white
            palette.setColor(QPalette.ColorRole.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.WindowText, white)
            palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ToolTipBase, white)
            palette.setColor(QPalette.ColorRole.ToolTipText, white)
            palette.setColor(QPalette.ColorRole.Text, white)
            palette.setColor(QPalette.ColorRole.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ColorRole.ButtonText, white)
            palette.setColor(QPalette.ColorRole.BrightText, Qt.GlobalColor.red)

        self.setPalette(palette)


def main() -> None:
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
