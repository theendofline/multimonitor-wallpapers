import os
import sys
import unittest

# Add parent directory to path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.multimonitor_wallpapers.widget import MultiMonitorApp


class TestBasicFunctionality(unittest.TestCase):
    def test_imports(self):
        """Test that required modules can be imported."""

        self.assertTrue(True)  # If we got here, imports worked

    def test_class_exists(self):
        """Test that the main application class exists."""
        self.assertTrue(hasattr(MultiMonitorApp, "__init__"))
        self.assertTrue(callable(MultiMonitorApp.__init__))


if __name__ == "__main__":
    unittest.main()
