"""Detect and parse the monitor layout reported by `xrandr`."""

from __future__ import annotations

import logging
import subprocess
from typing import TypedDict

logger = logging.getLogger(__name__)


class Monitor(TypedDict):
    name: str
    geometry: str
    offset: tuple[int, int]


def parse_xrandr_output(stdout: str) -> list[Monitor]:
    """Extract connected monitors from `xrandr --query` text output.

    A connected monitor line looks like:
        DP-0 connected primary 1920x1080+0+0 (...) ...
    Disconnected monitors and mode lines are ignored. If no monitor with a
    valid geometry is found, a single 1920x1080 fallback is returned so the
    UI still has something to render.
    """
    monitors: list[Monitor] = []
    for line in stdout.splitlines():
        if " connected" not in line:
            continue
        parts = line.split()
        name = parts[0]
        if "primary" in parts:
            parts.remove("primary")
        if len(parts) < 3:
            continue
        geometry = parts[2]
        if "+" not in geometry:
            continue
        geometry_parts = geometry.split("+")
        if len(geometry_parts) < 3:
            continue
        size = geometry_parts[0]
        offset_x = int(geometry_parts[1])
        offset_y = int(geometry_parts[2])
        monitors.append({"name": name, "geometry": size, "offset": (offset_x, offset_y)})

    if not monitors:
        monitors.append({"name": "default", "geometry": "1920x1080", "offset": (0, 0)})

    # Sort by x offset so monitor 0 is the leftmost; matches user expectation.
    monitors.sort(key=lambda m: m["offset"][0])
    return monitors


def get_monitors() -> list[Monitor]:
    """Run `xrandr --query` and return the parsed monitor layout."""
    result = subprocess.run(["xrandr", "--query"], capture_output=True, text=True)
    monitors = parse_xrandr_output(result.stdout)

    logger.info("Detected monitors:")
    for monitor in monitors:
        logger.info(
            "  %s: %s at offset %s",
            monitor["name"],
            monitor["geometry"],
            monitor["offset"],
        )
    return monitors
