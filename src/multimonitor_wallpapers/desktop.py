"""Desktop-environment integration: detection, gsettings, dark mode, deps."""

from __future__ import annotations

import logging
import os
import subprocess

logger = logging.getLogger(__name__)

WALLPAPER_FILENAME = "multiMonitorBackground.jpg"
GNOME_DIR = "~/.local/share/backgrounds"
CINNAMON_DIR = "~/.cinnamon/backgrounds"


def detect_desktop_environment() -> str:
    """Return one of "cinnamon", "gnome", "unknown" based on $XDG_CURRENT_DESKTOP."""
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    logger.debug("XDG_CURRENT_DESKTOP is: %s", desktop)
    if "cinnamon" in desktop:
        return "cinnamon"
    if "gnome" in desktop or "ubuntu" in desktop:
        return "gnome"
    return "unknown"


def wallpaper_output_paths(desktop_env: str) -> list[str]:
    """Resolve where to write the composed wallpaper image.

    GNOME also writes to the Cinnamon path so users who switch DEs keep a
    working wallpaper on both.
    """
    cinnamon_path = os.path.expanduser(os.path.join(CINNAMON_DIR, WALLPAPER_FILENAME))
    gnome_path = os.path.expanduser(os.path.join(GNOME_DIR, WALLPAPER_FILENAME))

    cinnamon_dir = os.path.expanduser(CINNAMON_DIR)
    gnome_dir = os.path.expanduser(GNOME_DIR)

    if desktop_env == "gnome":
        os.makedirs(gnome_dir, exist_ok=True)
        os.makedirs(cinnamon_dir, exist_ok=True)
        return [gnome_path, cinnamon_path]

    os.makedirs(cinnamon_dir, exist_ok=True)
    return [cinnamon_path]


def is_system_in_dark_mode() -> bool:
    """Return True if GNOME's color-scheme key reports a dark theme."""
    try:
        result = subprocess.run(
            ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
            capture_output=True,
            text=True,
        )
    except (FileNotFoundError, OSError):
        # gsettings is not installed; treat as light mode.
        return False
    return "dark" in result.stdout.lower()


def validate_dependencies() -> bool:
    """Check that the runtime tools we shell out to are installed."""
    for command in ["gsettings", "xrandr"]:
        if (
            subprocess.call(
                ["which", command], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            != 0
        ):
            logger.error("Dependency %r is missing.", command)
            return False
    return True


def apply_background(output_path: str, desktop_env: str) -> bool:
    """Tell the running desktop to load `output_path` as the wallpaper."""
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
            applied = False
            for option in ["spanned", "zoom", "stretched"]:
                try:
                    subprocess.check_call(
                        ["gsettings", "set", schema, "picture-uri", f"file://{output_path}"]
                    )
                    subprocess.check_call(["gsettings", "set", schema, "picture-options", option])
                    logger.info("Successfully set %s for GNOME", option)
                    applied = True
                    break
                except subprocess.CalledProcessError:
                    logger.warning("Option %s failed for GNOME, trying next", option)

            if not applied:
                logger.error("All GNOME picture-options values failed")
                return False

            if is_system_in_dark_mode():
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
                except subprocess.CalledProcessError:
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
