#!/usr/bin/env python3
"""
Simple script to generate an icon for the MultiMonitor Wallpapers application.
"""

import os
from PIL import Image, ImageDraw

def generate_icon():
    """Generate a simple icon for the application."""
    
    # Create assets directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    # Create a 256x256 icon with a blue background
    img = Image.new('RGB', (256, 256), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    
    # Draw a white outline
    d.rectangle([20, 20, 236, 236], outline=(255, 255, 255), width=5)
    
    # Draw three white rectangles to represent monitors
    d.rectangle([60, 60, 120, 120], fill=(255, 255, 255))
    d.rectangle([136, 60, 196, 120], fill=(255, 255, 255))
    d.rectangle([60, 136, 196, 196], fill=(255, 255, 255))
    
    # Save the icon
    img.save('assets/icon.png')
    print("Icon generated and saved to assets/icon.png")

if __name__ == "__main__":
    generate_icon() 