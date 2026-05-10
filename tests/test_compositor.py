"""Tests for `multimonitor_wallpapers.compositor`.

`compute_canvas_size` is pure math, so it's covered by table tests.
`compose_wallpaper` is exercised end-to-end on real on-disk images
because the heavy lifting is Pillow IO; we just confirm the canvas
ends up the right size and gets written where we asked.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from multimonitor_wallpapers.compositor import compose_wallpaper, compute_canvas_size
from multimonitor_wallpapers.monitors import Monitor


@pytest.mark.parametrize(
    ("monitors", "expected"),
    [
        (
            [{"name": "A", "geometry": "1920x1080", "offset": (0, 0)}],
            (1920, 1080),
        ),
        (
            [
                {"name": "A", "geometry": "1920x1080", "offset": (0, 0)},
                {"name": "B", "geometry": "1920x1080", "offset": (1920, 0)},
            ],
            (3840, 1080),
        ),
        (
            [
                {"name": "A", "geometry": "2560x1440", "offset": (0, 0)},
                {"name": "B", "geometry": "1920x1080", "offset": (2560, 360)},
            ],
            (4480, 1440),
        ),
    ],
)
def test_compute_canvas_size_covers_all_monitors(
    monitors: list[Monitor], expected: tuple[int, int]
) -> None:
    assert compute_canvas_size(monitors) == expected


def _make_solid_image(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> None:
    Image.new("RGB", size, color).save(path, "JPEG", quality=90)


def test_compose_wallpaper_writes_canvas_with_correct_size(tmp_path: Path) -> None:
    img_a = tmp_path / "a.jpg"
    img_b = tmp_path / "b.jpg"
    _make_solid_image(img_a, (800, 600), (255, 0, 0))
    _make_solid_image(img_b, (800, 600), (0, 0, 255))

    monitors: list[Monitor] = [
        {"name": "A", "geometry": "1920x1080", "offset": (0, 0)},
        {"name": "B", "geometry": "1920x1080", "offset": (1920, 0)},
    ]
    output = tmp_path / "wallpaper.jpg"

    compose_wallpaper(monitors, [str(img_a), str(img_b)], [str(output)])

    assert output.exists()
    with Image.open(output) as result:
        assert result.size == (3840, 1080)


def test_compose_wallpaper_writes_to_every_output_path(tmp_path: Path) -> None:
    img = tmp_path / "src.jpg"
    _make_solid_image(img, (400, 400), (10, 200, 10))

    monitors: list[Monitor] = [{"name": "A", "geometry": "1920x1080", "offset": (0, 0)}]
    out_a = tmp_path / "a.jpg"
    out_b = tmp_path / "nested" / "b.jpg"
    out_b.parent.mkdir()

    compose_wallpaper(monitors, [str(img)], [str(out_a), str(out_b)])

    assert out_a.exists()
    assert out_b.exists()


def test_compose_wallpaper_cycles_image_paths_when_fewer_than_monitors(tmp_path: Path) -> None:
    only_image = tmp_path / "single.jpg"
    _make_solid_image(only_image, (200, 200), (50, 50, 50))

    monitors: list[Monitor] = [
        {"name": "A", "geometry": "1280x720", "offset": (0, 0)},
        {"name": "B", "geometry": "1280x720", "offset": (1280, 0)},
    ]
    output = tmp_path / "wall.jpg"

    compose_wallpaper(monitors, [str(only_image)], [str(output)])

    with Image.open(output) as result:
        assert result.size == (2560, 720)


def test_compose_wallpaper_rejects_empty_inputs(tmp_path: Path) -> None:
    monitors: list[Monitor] = [{"name": "A", "geometry": "1920x1080", "offset": (0, 0)}]
    out = tmp_path / "out.jpg"

    with pytest.raises(ValueError):
        compose_wallpaper(monitors, [], [str(out)])
    with pytest.raises(ValueError):
        compose_wallpaper(monitors, [str(tmp_path / "x.jpg")], [])
