"""
Main application class for the Community Layout Switcher application.
"""

import os
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio

from constants import APP_ID
from translation import _
from managers import BackupManager
from app_window import BigAppearanceWindow


class BigAppearanceApp(Adw.Application):
    """Main application class"""
    
    def __init__(self):
        super().__init__(application_id=APP_ID)
        self.connect('activate', self.on_activate)
        
        # Set the application icon
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "hicolor", "scalable", "comm-layout-switcher.svg")
        if os.path.exists(icon_path):
            self.set_resource_base_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons"))
        
        # Add actions
        about_action = Gio.SimpleAction.new("about", None)
        about_action.connect("activate", self.on_about)
        self.add_action(about_action)
        
        quit_action = Gio.SimpleAction.new("quit", None)
        quit_action.connect("activate", self.on_quit)
        self.add_action(quit_action)
        
        restore_action = Gio.SimpleAction.new("restore_backup", None)
        restore_action.connect("activate", self.on_restore_backup)
        self.add_action(restore_action)
    
    def on_activate(self, app):
        """Handle application activation"""
        win = BigAppearanceWindow(app)
        win.present()
    
    def on_about(self, action, param):
        """Show about dialog"""
        about_dialog = Adw.AboutWindow()
        
        # Set transient parent
        active_window = self.get_active_window()
        if active_window:
            about_dialog.set_transient_for(active_window)
        
        # Set application information
        about_dialog.set_application_name(_("app_name"))
        about_dialog.set_version("1.0")
        about_dialog.set_developer_name("Big Community & Ari Novais")
        about_dialog.set_license_type(Gtk.License.GPL_3_0)
        about_dialog.set_license(_("license"))
        about_dialog.set_comments(_("about_description"))
        about_dialog.set_website("https://communitybig.org/")
        about_dialog.set_issue_url("https://github.com/big-comm/comm-layout-changer/issues")
        
        # Set logo icon using the correct method
        about_dialog.set_icon_name("org.bigappearance.app")
        
        # Add copyright information
        about_dialog.set_copyright("© 2022 - 2025 Big Community")
        
        # Show the about dialog
        about_dialog.present()
    
    def on_quit(self, action, param):
        """Handle quit action with confirmation dialog"""
        dialog = Adw.MessageDialog(
            transient_for=self.get_active_window(),
            heading=_("quit_confirm_title"),
            body=_("quit_confirm"),
        )
        
        dialog.add_response("cancel", _("cancel"))
        dialog.add_response("quit", _("quit"))
        dialog.set_response_appearance("quit", Adw.ResponseAppearance.DESTRUCTIVE)
        
        dialog.connect("response", self.on_quit_dialog_response)
        dialog.present()
    
    def on_quit_dialog_response(self, dialog, response):
        """Handle response from quit confirmation dialog"""
        if response == "quit":
            self.quit()
        
        dialog.destroy()
    
    def on_restore_backup(self, action, param):
        """Handle restore backup action"""
        active_window = self.get_active_window()
        backup_file = BackupManager.get_latest_backup()
        
        if not backup_file:
            active_window.show_toast(_("backup_restore_error").format(error=_("No backup found")))
            return
        
        dialog = Adw.MessageDialog(
            transient_for=active_window,
            heading=_("backup_restore_title"),
            body=_("backup_restore_message"),
        )
        
        dialog.add_response("cancel", _("cancel"))
        dialog.add_response("restore", _("backup_restore"))
        dialog.set_response_appearance("restore", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_restore_dialog_response, backup_file)
        dialog.present()
    
    def on_restore_dialog_response(self, dialog, response, backup_file):
        """Handle response from restore dialog"""
        if response == "restore":
            if BackupManager.restore_backup(backup_file):
                self.get_active_window().show_toast(_("backup_restore_success"))
            else:
                self.get_active_window().show_toast(_("backup_restore_error").format(error=_("unknown")))
        
        dialog.destroy()
