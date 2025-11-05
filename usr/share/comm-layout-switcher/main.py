#!/usr/bin/env python3
"""
Main entry point for the Community Layout Switcher application.
"""

import sys
import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gdk

# Add the path to our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from application import BigAppearanceApp

def main():
    # Create the application
    app = BigAppearanceApp()
    
    # Set the application icon
    icon_theme = Gtk.IconTheme.get_for_display(Gdk.Display.get_default())
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "hicolor", "scalable", "comm-layout-switcher.svg")
    
    # Register the icon with the system
    if os.path.exists(icon_path):
        icon_theme.add_resource_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons"))
    
    # Run the application
    app.run(sys.argv)

if __name__ == "__main__":
    main()
