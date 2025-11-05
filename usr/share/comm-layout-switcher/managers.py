"""
Manager classes for the Community Layout Switcher application.
"""

import os
import subprocess
import datetime
import json
from pathlib import Path
from typing import Dict, List, Tuple, Optional

from constants import (
    CONFIG_DIR, BACKUP_DIR, LAYOUTS_DIR, ICONS_DIR, 
    COLOR_MAP, EXTENSIONS
)


class ThemeManager:
    """Manages theme operations"""
    
    @staticmethod
    def extract_color_from_theme_name(theme_name: str) -> str:
        """Extract color from theme name"""
        theme_lower = theme_name.lower()
        for color_name, hex_code in COLOR_MAP.items():
            if color_name in theme_lower:
                return hex_code
        
        # Default colors if no match
        if 'dark' in theme_lower:
            return '#241f31'
        if 'light' in theme_lower:
            return '#ffffff'
        
        # Generate a color based on the theme name hash
        hash_value = hash(theme_name)
        r = (hash_value & 0xFF0000) >> 16
        g = (hash_value & 0x00FF00) >> 8
        b = hash_value & 0x0000FF
        return f'#{r:02x}{g:02x}{b:02x}'
    
    @staticmethod
    def get_themes(theme_type: str) -> List[Tuple[str, str]]:
        """Get available themes of a specific type"""
        themes = []
        
        # Define search paths based on theme type
        if theme_type in ("gtk", "shell"):
            search_paths = [
                Path.home() / '.themes',
                Path('/usr/local/share/themes'),
                Path('/usr/share/themes')
            ]
        elif theme_type == "icons":
            search_paths = [
                Path.home() / '.icons',
                Path('/usr/local/share/icons'),
                Path('/usr/share/icons')
            ]
        else:
            return themes
        
        # Check all search paths
        for search_path in search_paths:
            if not search_path.exists():
                continue
                
            # Get all theme directories
            for theme_dir in search_path.iterdir():
                if not theme_dir.is_dir():
                    continue
                
                # Check based on theme type
                if theme_type == "gtk":
                    # Check for gtk-3.0 or gtk-2.0 directory
                    if (theme_dir / "gtk-3.0").exists() or (theme_dir / "gtk-2.0").exists():
                        themes.append((theme_dir.name, str(theme_dir)))
                
                elif theme_type == "icons":
                    # Check for index.theme file
                    if (theme_dir / "index.theme").exists():
                        themes.append((theme_dir.name, str(theme_dir)))
                
                elif theme_type == "shell":
                    # Check for gnome-shell directory
                    shell_dir = theme_dir / "gnome-shell"
                    if shell_dir.exists():
                        # Check for required files
                        if (shell_dir / "gnome-shell.css").exists() or (shell_dir / "gnome-shell.gresource").exists():
                            themes.append((theme_dir.name, str(theme_dir)))
        
        # Remove duplicates and sort
        themes = list(set(themes))
        themes.sort(key=lambda x: x[0].lower())
        
        return themes


class BackupManager:
    """Manages backup operations"""
    
    @staticmethod
    def create_backup_dir() -> Path:
        """Create backup directory if it doesn't exist"""
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        return BACKUP_DIR
    
    @staticmethod
    def create_backup() -> Optional[Path]:
        """Create a backup of current dconf settings"""
        try:
            backup_dir = BackupManager.create_backup_dir()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = backup_dir / f"backup_{timestamp}.dconf"
            
            # Create the backup
            with open(backup_file, 'w') as f:
                subprocess.run(["dconf", "dump", "/"], stdout=f, check=True)
            
            # Create a symlink to the latest backup
            latest_backup = backup_dir / "latest_backup.dconf"
            if latest_backup.exists():
                latest_backup.unlink()
            latest_backup.symlink_to(backup_file)
            
            return backup_file
        except Exception as e:
            print(f"Backup error: {e}")
            return None
    
    @staticmethod
    def restore_backup(backup_file: Path) -> bool:
        """Restore settings from a backup file"""
        try:
            if not backup_file.exists():
                return False
            
            # Load the backup
            subprocess.run(["dconf", "load", "/"], stdin=open(backup_file, 'r'), check=True)
            return True
        except Exception as e:
            print(f"Restore error: {e}")
            return False
    
    @staticmethod
    def get_latest_backup() -> Optional[Path]:
        """Get the path to the latest backup file"""
        backup_dir = BackupManager.create_backup_dir()
        latest_backup = backup_dir / "latest_backup.dconf"
        
        if latest_backup.exists():
            if latest_backup.is_symlink():
                return Path(os.path.realpath(latest_backup))
            return latest_backup
        
        # If no symlink, find the most recent backup
        backups = list(backup_dir.glob("backup_*.dconf"))
        if backups:
            return max(backups, key=lambda x: x.stat().st_mtime)
        
        return None


class ExtensionManager:
    """Manages GNOME Shell extensions"""
    
    @staticmethod
    def check_extension_installed(uuid: str) -> bool:
        """Check if a GNOME extension is installed"""
        user_extensions = Path.home() / '.local/share/gnome-shell/extensions'
        system_extensions = Path('/usr/share/gnome-shell/extensions')
        
        # Check user extensions
        if (user_extensions / uuid).exists():
            return True
        
        # Check system extensions
        if (system_extensions / uuid).exists():
            return True
        
        return False
    
    @staticmethod
    def check_extension_enabled(uuid: str) -> bool:
        """Check if a GNOME extension is enabled"""
        try:
            # Get list of enabled extensions
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.shell", "enabled-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the list
            enabled_extensions = result.stdout.strip().strip("[]").replace("'", "").split(", ")
            
            # Check if our extension is in the list
            return uuid in enabled_extensions
        except:
            return False
    
    @staticmethod
    def toggle_extension(uuid: str, enable: bool) -> bool:
        """Enable or disable a GNOME extension"""
        try:
            # Get current list of enabled extensions
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.shell", "enabled-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # Parse the list
            enabled_extensions = result.stdout.strip().strip("[]").replace("'", "").split(", ")
            
            if enable:
                # Add extension to list if not already there
                if uuid not in enabled_extensions:
                    enabled_extensions.append(uuid)
            else:
                # Remove extension from list
                if uuid in enabled_extensions:
                    enabled_extensions.remove(uuid)
            
            # Set the new list
            new_list = "@as [" + ", ".join([f"'{ext}'" for ext in enabled_extensions if ext]) + "]"
            subprocess.run(
                ["gsettings", "set", "org.gnome.shell", "enabled-extensions", new_list],
                check=True
            )
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error toggling extension: {e}")
            return False
    
    @staticmethod
    def check_gnome_extensions_enabled() -> bool:
        """Check if GNOME Shell extensions are enabled"""
        try:
            # Check if extensions are disabled
            result = subprocess.run(
                ["dconf", "read", "/org/gnome/shell/disable-extensions"],
                capture_output=True,
                text=True,
                check=True
            )
            # If the key is set to 'true', extensions are disabled
            return result.stdout.strip().lower() != "true"
        except subprocess.CalledProcessError as e:
            print(f"Error checking extensions status: {e}")
            # Assume extensions are enabled if we can't check
            return True
        except Exception as e:
            print(f"Unexpected error checking extensions status: {e}")
            return True
    
    @staticmethod
    def enable_gnome_extensions() -> bool:
        """Enable GNOME Shell extensions"""
        try:
            subprocess.run(
                ["dconf", "write", "/org/gnome/shell/disable-extensions", "false"],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error enabling extensions: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error enabling extensions: {e}")
            return False


class SystemUtils:
    """System utility functions"""
    
    @staticmethod
    def detect_desktop_environment() -> str:
        """Detect the current desktop environment"""
        desktop = os.environ.get('XDG_CURRENT_DESKTOP', '').lower()
        if 'gnome' in desktop:
            return 'gnome'
        else:
            # Fallback to checking other environment variables
            if 'GNOME_DESKTOP_SESSION_ID' in os.environ:
                return 'gnome'
            return 'gnome'  # Default to GNOME
    
    @staticmethod
    def find_file(file_name: str, search_dirs: List[str]) -> Optional[str]:
        """Search for a file in common locations"""
        if not file_name:
            return None
            
        possible_paths = []
        
        # Add script-relative paths
        script_dir = Path(__file__).parent
        for search_dir in search_dirs:
            possible_paths.append(script_dir / search_dir / file_name)
            possible_paths.append(Path.home() / f".local/share/{search_dir}" / file_name)
            possible_paths.append(Path(f"/usr/share/{search_dir}") / file_name)
            possible_paths.append(Path(f"/usr/local/share/{search_dir}") / file_name)
        
        # Try with different extensions
        base_name, ext = os.path.splitext(file_name)
        for ext in ['.png', '.jpg', '.jpeg', '.svg']:
            for path in possible_paths:
                test_path = path.with_suffix(ext)
                if test_path.exists():
                    return str(test_path)
        
        # Try original paths
        for path in possible_paths:
            if path.exists():
                return str(path)
        
        return None


class SettingsManager:
    """Manages application settings"""
    
    def __init__(self):
        from constants import SETTINGS_FILE
        self.settings_file = SETTINGS_FILE
        self.settings = self._load_settings()
    
    def _load_settings(self) -> Dict:
        """Load application settings"""
        if not CONFIG_DIR.exists():
            CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        
        if self.settings_file.exists():
            try:
                with open(self.settings_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        
        return {"intro_shown": False}
    
    def save_settings(self):
        """Save application settings"""
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f)
        except:
            pass
    
    def get(self, key: str, default=None):
        """Get a setting value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value):
        """Set a setting value"""
        self.settings[key] = value
        self.save_settings()
