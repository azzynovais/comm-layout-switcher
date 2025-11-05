"""
Constants and global variables for the Community Layout Switcher application.
"""

from pathlib import Path

# Application constants
APP_ID = 'org.bigappearance.app'
CONFIG_DIR = Path.home() / '.config' / 'big-appearance'
BACKUP_DIR = CONFIG_DIR / 'backups'
LAYOUTS_DIR = 'layouts'
ICONS_DIR = 'icons'
SETTINGS_FILE = CONFIG_DIR / 'settings.json'

# Theme color mapping
COLOR_MAP = {
    'blue': '#3584e4', 'green': '#26a269', 'yellow': '#cd9309',
    'orange': '#e66100', 'red': '#c01c28', 'purple': '#9141ac',
    'pink': '#d16d9e', 'teal': '#2190a4', 'grey': '#5e5c64',
    'gray': '#5e5c64', 'black': '#241f31', 'white': '#ffffff',
    'dark': '#241f31', 'light': '#ffffff', 'brown': '#865e3c',
    'cyan': '#00b4c8', 'magenta': '#c061cb', 'lime': '#2ec27e',
    'indigo': '#1c71d8'
}

# GNOME extensions data
EXTENSIONS = [
    {
        "name": "Desktop Cube",
        "description": "Rotate your desktop on a 3D cube",
        "uuid": "desktop-cube@schneegans.github.com",
        "url": "https://extensions.gnome.org/extension/4648/desktop-cube/"
    },
    {
        "name": "Magic Lamp",
        "description": "Animated window minimizing effect",
        "uuid": "compiz-alike-magic-lamp-effect@hermes83.github.com",
        "url": "https://extensions.gnome.org/extension/3740/compiz-alike-magic-lamp-effect/"
    },
    {
        "name": "Windows Effects",
        "description": "Additional window animations",
        "uuid": "compiz-windows-effect@hermes83.github.com",
        "url": "https://extensions.gnome.org/extension/3210/compiz-windows-effect/"
    },
    {
        "name": "Desktop Icons",
        "description": "Add icons to your desktop",
        "uuid": "ding@rastersoft.com",
        "url": "https://extensions.gnome.org/extension/2087/desktop-icons-ng-ding/",
        "has_settings": True
    }
]

# Layout definitions
LAYOUTS = [
    ("Classic", "classic.txt", "classic.svg", "view-continuous-symbolic"),
    ("Vanilla", "vanilla.txt", "vanilla.svg", "view-grid-symbolic"),
    ("G-Unity", "g-unity.txt", "g-unity.svg", "view-app-grid-symbolic"),
    ("New", "new.txt", "new.svg", "view-paged-symbolic"),
    ("Next-Gnome", "next-gnome.txt", "next-gnome.svg", "view-paged-symbolic"),
    ("Modern", "modern.txt", "modern.svg", "view-grid-symbolic")
]
