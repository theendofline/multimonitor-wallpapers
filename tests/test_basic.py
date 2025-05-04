import unittest
import os
import sys

# Add parent directory to path so we can import the module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.multimonitor_wallpapers.widget import MultiMonitorApp


class TestBasicFunctionality(unittest.TestCase):
    def test_imports(self):
        """Test that required modules can be imported."""
        import PySide6
        from PIL import Image
        
        self.assertTrue(True)  # If we got here, imports worked
    
    def test_class_exists(self):
        """Test that the main application class exists."""
        self.assertTrue(hasattr(MultiMonitorApp, '__init__'))
        self.assertTrue(callable(getattr(MultiMonitorApp, '__init__')))


if __name__ == '__main__':
    unittest.main() 