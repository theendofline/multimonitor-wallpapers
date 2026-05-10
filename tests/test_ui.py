"""Tests for `multimonitor_wallpapers.ui._update_thumbnail`.

Runs Qt against the offscreen platform plugin so no display server is
required (PySide6 ships the plugin out of the box). The whole module
is skipped if PySide6 isn't importable in the current environment.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

# Must be set before any Qt import so the QPA plugin is selected.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

pytest.importorskip("PySide6.QtWidgets")

from PIL import Image
from PySide6.QtWidgets import QApplication, QLabel

from multimonitor_wallpapers.ui import THUMBNAIL_SIZE, MultiMonitorApp


# A QApplication must exist before any QWidget is constructed; module-
# scoped + autouse keeps it implicit so individual tests stay terse.
@pytest.fixture(scope="module", autouse=True)
def _qapp() -> QApplication:
    return QApplication.instance() or QApplication([])


@pytest.fixture
def thumbnail() -> QLabel:
    label = QLabel()
    label.setFixedSize(THUMBNAIL_SIZE)
    return label


def _make_png(path: Path, size: tuple[int, int] = (1920, 1080)) -> None:
    Image.new("RGB", size, (200, 50, 50)).save(path, "PNG")


def test_empty_path_shows_placeholder(thumbnail: QLabel) -> None:
    MultiMonitorApp._update_thumbnail(thumbnail, "")
    assert thumbnail.text() == "No image selected"
    assert thumbnail.pixmap().isNull()


def test_invalid_path_shows_invalid_message(thumbnail: QLabel, tmp_path: Path) -> None:
    MultiMonitorApp._update_thumbnail(thumbnail, str(tmp_path / "does-not-exist.png"))
    assert thumbnail.text() == "Invalid image"
    assert thumbnail.pixmap().isNull()


def test_valid_image_scales_into_tile(thumbnail: QLabel, tmp_path: Path) -> None:
    img = tmp_path / "wallpaper.png"
    _make_png(img, (1920, 1080))

    MultiMonitorApp._update_thumbnail(thumbnail, str(img))

    pixmap = thumbnail.pixmap()
    assert thumbnail.text() == ""
    assert not pixmap.isNull()
    # 1920x1080 (16:9) fits exactly into the 240x135 (16:9) tile.
    assert (pixmap.width(), pixmap.height()) == (THUMBNAIL_SIZE.width(), THUMBNAIL_SIZE.height())


def test_portrait_image_letterboxes_inside_tile(thumbnail: QLabel, tmp_path: Path) -> None:
    img = tmp_path / "portrait.png"
    _make_png(img, (600, 1200))

    MultiMonitorApp._update_thumbnail(thumbnail, str(img))

    pixmap = thumbnail.pixmap()
    assert not pixmap.isNull()
    # KeepAspectRatio: 600x1200 scaled into a 240x135 box -> height-bound 135,
    # width = 135 * (600/1200) = 67 (Qt rounds toward floor).
    assert pixmap.height() == THUMBNAIL_SIZE.height()
    assert pixmap.width() < THUMBNAIL_SIZE.width()


def test_clearing_path_restores_placeholder(thumbnail: QLabel, tmp_path: Path) -> None:
    img = tmp_path / "wallpaper.png"
    _make_png(img)

    MultiMonitorApp._update_thumbnail(thumbnail, str(img))
    assert not thumbnail.pixmap().isNull()

    MultiMonitorApp._update_thumbnail(thumbnail, "")
    assert thumbnail.text() == "No image selected"
    assert thumbnail.pixmap().isNull()
