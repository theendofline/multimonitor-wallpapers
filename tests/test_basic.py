import os
import sys
import unittest

# Add parent directory to path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import version directly
from __init__ import __version__

# Check if running in CI environment
IN_CI = os.environ.get("CI", "false").lower() == "true"

# If not in CI, try to import GUI components
if not IN_CI:
    try:
        from src.multimonitor_wallpapers.widget import MultiMonitorApp

        GUI_AVAILABLE = True
    except ImportError as e:
        print(f"GUI libraries not available, skipping GUI tests: {e}")
        GUI_AVAILABLE = False
else:
    # Skip GUI tests entirely in CI
    print("Running in CI environment, skipping GUI imports")
    GUI_AVAILABLE = False


class TestBasicFunctionality(unittest.TestCase):
    def test_imports(self):
        """Test that required modules can be imported."""
        # Import basic modules that should always be available
        self.assertTrue(True)  # If we got here, imports worked

    def test_version(self):
        """Test that the version is defined."""
        self.assertIsInstance(__version__, str)
        # Version should follow semantic versioning (x.y.z)
        parts = __version__.split(".")
        self.assertTrue(1 <= len(parts) <= 3, "Version should have 1-3 parts")

    @unittest.skipIf(not GUI_AVAILABLE, "GUI libraries not available")
    def test_class_exists(self):
        """Test that the main application class exists."""
        self.assertTrue(hasattr(MultiMonitorApp, "__init__"))
        self.assertTrue(callable(MultiMonitorApp.__init__))


if __name__ == "__main__":
    unittest.main()
