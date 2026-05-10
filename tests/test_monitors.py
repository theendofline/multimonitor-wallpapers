"""Tests for `multimonitor_wallpapers.monitors.parse_xrandr_output`.

Realistic `xrandr --query` excerpts taken from a typical multi-monitor
layout, trimmed to the lines the parser actually inspects.
"""

from __future__ import annotations

from multimonitor_wallpapers.monitors import parse_xrandr_output

DUAL_MONITOR_XRANDR = """\
Screen 0: minimum 320 x 200, current 5760 x 1080, maximum 16384 x 16384
DP-0 connected primary 1920x1080+1920+0 (normal left inverted right x axis y axis) 600mm x 340mm
   1920x1080     60.00*+
HDMI-1 connected 1920x1080+0+0 (normal left inverted right x axis y axis) 600mm x 340mm
   1920x1080     60.00*+
HDMI-2 connected 1920x1080+3840+0 (normal left inverted right x axis y axis) 600mm x 340mm
   1920x1080     60.00*+
DP-1 disconnected (normal left inverted right x axis y axis)
"""

LAPTOP_ONLY_XRANDR = """\
Screen 0: minimum 320 x 200, current 1920 x 1200, maximum 16384 x 16384
eDP-1 connected primary 1920x1200+0+0 (normal left inverted right x axis y axis) 340mm x 210mm
   1920x1200     60.00*+
"""

EMPTY_XRANDR = "Screen 0: minimum 320 x 200, current 0 x 0, maximum 16384 x 16384\n"


def test_parses_three_connected_monitors_sorted_left_to_right() -> None:
    monitors = parse_xrandr_output(DUAL_MONITOR_XRANDR)

    assert [m["name"] for m in monitors] == ["HDMI-1", "DP-0", "HDMI-2"]
    assert [m["offset"] for m in monitors] == [(0, 0), (1920, 0), (3840, 0)]
    assert all(m["geometry"] == "1920x1080" for m in monitors)


def test_strips_primary_marker_from_geometry_lookup() -> None:
    [primary] = [m for m in parse_xrandr_output(LAPTOP_ONLY_XRANDR) if m["name"] == "eDP-1"]
    assert primary["geometry"] == "1920x1200"
    assert primary["offset"] == (0, 0)


def test_ignores_disconnected_outputs() -> None:
    monitors = parse_xrandr_output(DUAL_MONITOR_XRANDR)
    assert "DP-1" not in [m["name"] for m in monitors]


def test_falls_back_to_single_default_monitor_when_none_connected() -> None:
    monitors = parse_xrandr_output(EMPTY_XRANDR)
    assert monitors == [{"name": "default", "geometry": "1920x1080", "offset": (0, 0)}]
