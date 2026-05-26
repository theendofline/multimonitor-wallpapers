"""PySide6 main window. Glue layer over `monitors`, `compositor`, `desktop`."""

from __future__ import annotations

import logging
import os
import sys

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from . import compositor, desktop, monitors

logger = logging.getLogger(__name__)

# 16:9 keeps the layout predictable across monitor aspect ratios; the
# chosen image is scaled with KeepAspectRatio so portrait/4:3 sources
# letterbox cleanly inside the tile.
THUMBNAIL_SIZE = QSize(240, 135)


class MultiMonitorApp(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.files: list[str] = []
        self.file_inputs: list[QLineEdit] = []
        self.thumbnails: list[QLabel] = []
        self.monitors: list[monitors.Monitor] = []
        self._dark_mode = desktop.is_system_in_dark_mode()

        self.init_ui()
        self.handle_dark_mode()

    def init_ui(self) -> None:
        self.setWindowTitle("Multi-Monitor Background App")
        self.setGeometry(300, 300, 1000, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.monitors = monitors.get_monitors()
        self.file_inputs = []
        self.thumbnails = []
        edit_style = (
            "color: white; background-color: #353535;"
            if self._dark_mode
            else "color: black; background-color: white;"
        )

        monitors_row = QHBoxLayout()
        for monitor in self.monitors:
            column = QVBoxLayout()

            thumbnail = QLabel("No image selected", self)
            thumbnail.setFixedSize(THUMBNAIL_SIZE)
            thumbnail.setAlignment(Qt.AlignmentFlag.AlignCenter)
            thumbnail.setStyleSheet("QLabel { border: 1px solid #888; }")
            column.addWidget(thumbnail, alignment=Qt.AlignmentFlag.AlignCenter)
            self.thumbnails.append(thumbnail)

            file_input = QLineEdit(self)
            file_input.setPlaceholderText(f"Select image for {monitor['name']}")
            file_input.setStyleSheet(edit_style)
            # textChanged fires for Browse, manual edits, and clear_inputs(),
            # so this is the single place keeping the preview in sync.
            file_input.textChanged.connect(
                lambda text, t=thumbnail: self._update_thumbnail(t, text)
            )
            column.addWidget(file_input)
            self.file_inputs.append(file_input)

            browse_button = QPushButton("Browse", self)
            browse_button.clicked.connect(lambda _, fi=file_input: self.browse_file(fi))
            column.addWidget(browse_button)

            monitors_row.addLayout(column)
        main_layout.addLayout(monitors_row)

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

    @staticmethod
    def _update_thumbnail(thumbnail: QLabel, file_path: str) -> None:
        if not file_path:
            thumbnail.setPixmap(QPixmap())
            thumbnail.setText("No image selected")
            return

        pixmap = QPixmap(file_path)
        if pixmap.isNull():
            thumbnail.setPixmap(QPixmap())
            thumbnail.setText("Invalid image")
            return

        thumbnail.setText("")
        thumbnail.setPixmap(
            pixmap.scaled(
                THUMBNAIL_SIZE,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def clear_inputs(self) -> None:
        for file_input in self.file_inputs:
            file_input.clear()

    def set_background(self) -> None:
        self.files = [file_input.text() for file_input in self.file_inputs if file_input.text()]

        if len(self.files) < 1:
            self.statusBar().showMessage("Please select at least one image file.")
            return

        if not desktop.validate_dependencies():
            self.statusBar().showMessage("Missing required dependencies (gsettings, xrandr).")
            return

        try:
            desktop_env = desktop.detect_desktop_environment()
            output_paths = desktop.wallpaper_output_paths(desktop_env)
            compositor.compose_wallpaper(self.monitors, self.files, output_paths)
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
        if self._dark_mode:
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
