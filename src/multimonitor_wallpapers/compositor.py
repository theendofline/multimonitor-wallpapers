"""Pure-ish image compositing: build one wallpaper covering all monitors."""

from __future__ import annotations

import logging
from collections.abc import Iterable

from PIL import Image

from .monitors import Monitor

logger = logging.getLogger(__name__)


def _parse_geometry(geometry: str) -> tuple[int, int]:
    width, height = geometry.split("x", 1)
    return int(width), int(height)


def compute_canvas_size(monitors: Iterable[Monitor]) -> tuple[int, int]:
    """Return the (width, height) of the bounding box that holds all monitors."""
    monitors = list(monitors)
    if not monitors:
        raise ValueError("compute_canvas_size requires at least one monitor")
    max_right = 0
    max_bottom = 0
    for monitor in monitors:
        mon_width, mon_height = _parse_geometry(monitor["geometry"])
        offset_x, offset_y = monitor["offset"]
        max_right = max(max_right, offset_x + mon_width)
        max_bottom = max(max_bottom, offset_y + mon_height)
    return max_right, max_bottom


def compose_wallpaper(
    monitors: list[Monitor],
    image_paths: list[str],
    output_paths: list[str],
) -> None:
    """Composite per-monitor images onto a single canvas and save it.

    `image_paths` is cycled if it is shorter than the monitor list. The same
    final image is written to every entry in `output_paths` (callers may want
    multiple write locations on GNOME for back-compat).
    """
    if not image_paths:
        raise ValueError("compose_wallpaper requires at least one image path")
    if not output_paths:
        raise ValueError("compose_wallpaper requires at least one output path")

    total_width, total_height = compute_canvas_size(monitors)
    logger.info("Total screen size: %dx%d", total_width, total_height)
    logger.info("Number of monitors: %d", len(monitors))

    canvas = Image.new("RGB", (total_width, total_height), (0, 0, 0))

    for i, monitor in enumerate(monitors):
        geometry = monitor["geometry"]
        offset_x, offset_y = monitor["offset"]
        image_path = image_paths[i % len(image_paths)]

        logger.info(
            "Monitor %d (%s): geometry=%s, offset=(%d, %d)",
            i,
            monitor["name"],
            geometry,
            offset_x,
            offset_y,
        )

        with Image.open(image_path) as src_img:
            rgb_img = src_img.convert("RGB")
            mon_width, mon_height = _parse_geometry(geometry)
            rgb_img.thumbnail((mon_width, mon_height), Image.Resampling.LANCZOS)

            logger.debug("Image size after resize: %dx%d", rgb_img.width, rgb_img.height)

            tile = Image.new("RGB", (mon_width, mon_height), (0, 0, 0))
            paste_x = (mon_width - rgb_img.width) // 2
            paste_y = (mon_height - rgb_img.height) // 2
            tile.paste(rgb_img, (paste_x, paste_y))

            canvas.paste(tile, (offset_x, offset_y))

    for output_path in output_paths:
        canvas.save(output_path, "JPEG", quality=95)
        logger.info("Saved background image to: %s", output_path)
