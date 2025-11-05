"""
Main application window for the Community Layout Switcher application.
"""

import os
import subprocess
import tempfile
import time
import concurrent.futures
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Adw, Gdk, GLib, Pango, Gio

from constants import LAYOUTS, EXTENSIONS
from translation import TranslationManager
from managers import (
    ThemeManager, BackupManager, ExtensionManager, 
    SystemUtils, SettingsManager
)
from ui_components import LayoutRow, ThemeCard, EffectCard


class BigAppearanceWindow(Adw.ApplicationWindow):
    """Main application window"""
    
    def __init__(self, app):
        super().__init__(application=app)
        self.translator = TranslationManager()
        self.settings_manager = SettingsManager()
        
        # Window setup
        self.set_title(self.translator._("app_name"))
        self.set_default_size(900, 600)
        self.set_size_request(800, 500)
        
        # Detect desktop environment
        self.desktop_env = SystemUtils.detect_desktop_environment()
        print(f"Detected desktop environment: {self.desktop_env}")
        print(f"System language: {self.translator._lang}")
        
        # Initialize state variables
        self.applying = False
        self.updating_selection = False
        self.selected_layout_item = None
        self.test_mode = False
        self.backup_created = False
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        
        # Create UI components
        self.create_ui()
        
        # Load CSS for styling
        self.load_css()
        
        # Connect to resize event for responsive adjustments
        self.connect("notify::default-width", self.on_resize)
        self.connect("notify::default-height", self.on_resize)
        
        # Show intro dialog if needed
        if not self.settings_manager.get("intro_shown", False):
            self.show_intro_dialog()
    
    def create_ui(self):
        """Create all UI components"""
        # Create toolbar view
        toolbar_view = Adw.ToolbarView()
        
        # Create header bar
        header_bar = Adw.HeaderBar()
        toolbar_view.add_top_bar(header_bar)
        
        # Add window title
        title_label = Gtk.Label()
        title_label.set_text(self.translator._("app_name"))
        title_label.add_css_class("title-3")
        header_bar.set_title_widget(title_label)
        
        # Add menu button
        menu_button = Gtk.MenuButton()
        menu_button.set_icon_name("open-menu-symbolic")
        
        # Create menu model
        menu = Gio.Menu()
        menu.append(self.translator._("backup_restore"), "app.restore_backup")
        menu.append(self.translator._("about"), "app.about")
        menu.append(self.translator._("quit"), "app.quit")
        
        # Set menu to button
        menu_button.set_menu_model(menu)
        header_bar.pack_end(menu_button)
        
        # Create toast overlay
        self.toast_overlay = Adw.ToastOverlay()
        
        # Create tab view for the three main sections
        self.tab_view = Adw.TabView()
        self.tab_view.set_vexpand(True)
        
        # Create tabs
        self.layouts_tab = self.create_layouts_tab()
        self.effects_tab = self.create_effects_tab()
        self.themes_tab = self.create_themes_tab()
        
        # Add tabs to tab view
        layouts_page = self.tab_view.append(self.layouts_tab)
        layouts_page.set_title(self.translator._("layouts_tab"))
        
        effects_page = self.tab_view.append(self.effects_tab)
        effects_page.set_title(self.translator._("effects_tab"))
        
        themes_page = self.tab_view.append(self.themes_tab)
        themes_page.set_title(self.translator._("themes_tab"))
        
        # Create tab bar
        tab_bar = Adw.TabBar()
        tab_bar.set_view(self.tab_view)
        tab_bar.set_autohide(False)
        
        # Create main container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        main_box.append(tab_bar)
        main_box.append(self.tab_view)
        
        # Set main content
        self.toast_overlay.set_child(main_box)
        toolbar_view.set_content(self.toast_overlay)
        
        # Set toolbar view as window content
        self.set_content(toolbar_view)
    
    def create_layouts_tab(self):
        """Create the Layouts tab"""
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(self.translator._("layouts_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(self.translator._("select_layout"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Create paned widget for main layout
        paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        paned.set_position(500)
        paned.set_resize_start_child(True)
        paned.set_shrink_start_child(False)
        paned.set_resize_end_child(False)
        paned.set_shrink_end_child(False)
        
        # Create preview area
        preview_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_container.set_halign(Gtk.Align.CENTER)
        preview_container.set_valign(Gtk.Align.CENTER)
        preview_container.set_vexpand(True)
        
        # Preview card
        preview_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        preview_card.add_css_class("card")
        preview_card.set_size_request(400, 300)
        
        # Preview title
        self.preview_title = Gtk.Label()
        self.preview_title.add_css_class("title-2")
        self.preview_title.set_margin_bottom(15)
        self.preview_title.set_halign(Gtk.Align.CENTER)
        preview_card.append(self.preview_title)
        
        # Preview image with frame
        image_frame = Gtk.Box()
        image_frame.add_css_class("frame")
        image_frame.set_halign(Gtk.Align.CENTER)
        image_frame.set_size_request(350, 180)
        
        self.preview_image = Gtk.Picture()
        self.preview_image.set_size_request(330, 160)
        self.preview_image.set_content_fit(Gtk.ContentFit.CONTAIN)
        image_frame.append(self.preview_image)
        preview_card.append(image_frame)
        
        # Preview description
        self.preview_description = Gtk.Label()
        self.preview_description.set_margin_top(15)
        self.preview_description.set_margin_bottom(20)
        self.preview_description.set_halign(Gtk.Align.CENTER)
        self.preview_description.set_wrap(True)
        self.preview_description.set_max_width_chars(40)
        preview_card.append(self.preview_description)
        
        # Buttons container
        buttons_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        buttons_box.set_halign(Gtk.Align.CENTER)
        buttons_box.set_margin_top(5)
        buttons_box.set_spacing(10)
        
        # Test button
        self.test_button = Gtk.Button(label=self.translator._("test_layout"))
        self.test_button.add_css_class("pill")
        self.test_button.set_size_request(150, 40)
        self.test_button.connect("clicked", self.on_test_layout_clicked)
        buttons_box.append(self.test_button)
        
        # Apply button
        self.apply_button = Gtk.Button(label=self.translator._("apply"))
        self.apply_button.add_css_class("suggested-action")
        self.apply_button.add_css_class("pill")
        self.apply_button.set_size_request(150, 40)
        self.apply_button.connect("clicked", self.on_apply_layout_clicked)
        buttons_box.append(self.apply_button)
        
        # Spinner for loading state
        self.spinner = Gtk.Spinner()
        self.spinner.set_size_request(20, 20)
        self.spinner.set_margin_start(10)
        self.spinner.set_visible(False)
        buttons_box.append(self.spinner)
        
        preview_card.append(buttons_box)
        preview_container.append(preview_card)
        
        # Status bar
        status_container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        status_container.set_halign(Gtk.Align.CENTER)
        status_container.set_margin_top(15)
        
        self.status_bar = Gtk.Label()
        self.status_bar.set_wrap(True)
        self.status_bar.set_max_width_chars(40)
        status_container.append(self.status_bar)
        preview_container.append(status_container)
        
        paned.set_start_child(preview_container)
        
        # Create sidebar
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        sidebar_box.set_size_request(200, -1)
        
        # Sidebar header
        sidebar_header = Gtk.Label()
        sidebar_header.set_text(self.translator._("select_layout"))
        sidebar_header.add_css_class("title-3")
        sidebar_header.set_margin_start(15)
        sidebar_header.set_margin_top(15)
        sidebar_header.set_margin_bottom(15)
        sidebar_header.set_halign(Gtk.Align.START)
        sidebar_box.append(sidebar_header)
        
        # Separator
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_margin_start(10)
        separator.set_margin_end(10)
        separator.set_margin_bottom(5)
        sidebar_box.append(separator)
        
        # Create scrolled window for layout list
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        
        # Layout list box
        self.layout_list_box = Gtk.ListBox()
        self.layout_list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.layout_list_box.connect("row-selected", self.on_layout_row_selected)
        
        # Create layout rows
        self.layout_buttons = []
        for name, config_file, icon_file, fallback_icon in LAYOUTS:
            row = LayoutRow(name, icon_file, fallback_icon, config_file, self.translator)
            self.layout_list_box.append(row)
            self.layout_buttons.append((row, name, config_file))
        
        scrolled_window.set_child(self.layout_list_box)
        sidebar_box.append(scrolled_window)
        
        paned.set_end_child(sidebar_box)
        container.append(paned)
        
        # Select first layout by default
        if LAYOUTS:
            self.select_layout_item((LAYOUTS[0][0], LAYOUTS[0][1]))
        
        return container
    
    def create_effects_tab(self):
        """Create the Effects tab"""
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(self.translator._("effects_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(self.translator._("effects_description"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Check if running on GNOME
        if self.desktop_env != 'gnome':
            # Show message that effects are only available on GNOME
            info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
            info_box.set_halign(Gtk.Align.CENTER)
            info_box.set_valign(Gtk.Align.CENTER)
            info_box.set_vexpand(True)
            
            info_icon = Gtk.Image.new_from_icon_name("dialog-information-symbolic")
            info_icon.set_pixel_size(64)
            info_icon.set_margin_bottom(20)
            info_box.append(info_icon)
            
            info_label = Gtk.Label()
            info_label.set_text(self.translator._("gnome_only"))
            info_label.add_css_class("title-3")
            info_label.set_wrap(True)
            info_label.set_max_width_chars(30)
            info_box.append(info_label)
            
            container.append(info_box)
            return container
        
        # Create effects grid
        effects_grid = Gtk.Grid()
        effects_grid.set_row_spacing(20)
        effects_grid.set_column_spacing(20)
        effects_grid.set_halign(Gtk.Align.CENTER)
        effects_grid.set_valign(Gtk.Align.CENTER)
        effects_grid.set_vexpand(True)
        
        # Create effect cards
        for i, effect in enumerate(EXTENSIONS):
            effect_card = EffectCard(
                effect, 
                self.translator,
                self.toggle_extension,
                self.open_url,
                self.open_extension_settings
            )
            effects_grid.attach(effect_card, i % 3, i // 3, 1, 1)
        
        container.append(effects_grid)
        
        return container
    
    def create_themes_tab(self):
        """Create the Themes tab"""
        # Create main container
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.set_margin_start(20)
        container.set_margin_end(20)
        container.set_margin_top(20)
        container.set_margin_bottom(20)
        
        # Title
        title = Gtk.Label()
        title.set_text(self.translator._("themes_tab"))
        title.add_css_class("title-1")
        title.set_margin_bottom(20)
        title.set_halign(Gtk.Align.START)
        container.append(title)
        
        # Description
        description = Gtk.Label()
        description.set_text(self.translator._("themes_description"))
        description.add_css_class("body")
        description.set_margin_bottom(30)
        description.set_halign(Gtk.Align.START)
        container.append(description)
        
        # Create theme categories
        theme_notebook = Gtk.Notebook()
        theme_notebook.set_vexpand(True)
        
        # GTK Themes
        gtk_themes_page = self.create_theme_page("gtk")
        gtk_themes_label = Gtk.Label(label=self.translator._("gtk_theme"))
        theme_notebook.append_page(gtk_themes_page, gtk_themes_label)
        
        # Icon Themes
        icon_themes_page = self.create_theme_page("icons")
        icon_themes_label = Gtk.Label(label=self.translator._("icon_theme"))
        theme_notebook.append_page(icon_themes_page, icon_themes_label)
        
        # Shell Themes
        shell_themes_page = self.create_theme_page("shell")
        shell_themes_label = Gtk.Label(label=self.translator._("shell_theme"))
        theme_notebook.append_page(shell_themes_page, shell_themes_label)
        
        container.append(theme_notebook)
        
        return container
    
    def create_theme_page(self, theme_type: str):
        """Create a theme page for a specific type"""
        # Create scrolled window
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_vexpand(True)
        
        # Create flow box for themes
        flow_box = Gtk.FlowBox()
        flow_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        flow_box.set_max_children_per_line(4)
        flow_box.set_min_children_per_line(2)
        flow_box.set_halign(Gtk.Align.CENTER)
        flow_box.set_valign(Gtk.Align.START)
        flow_box.set_row_spacing(20)
        flow_box.set_column_spacing(20)
        
        # Get themes based on type
        themes = ThemeManager.get_themes(theme_type)
        
        if not themes:
            # No themes found message
            no_themes_label = Gtk.Label()
            no_themes_label.set_text(self.translator._("no_themes_found"))
            no_themes_label.add_css_class("title-3")
            no_themes_label.set_margin_top(50)
            no_themes_label.set_halign(Gtk.Align.CENTER)
            flow_box.append(no_themes_label)
        else:
            # Create theme cards
            for theme_name, theme_path in themes:
                theme_card = ThemeCard(theme_name, theme_path, theme_type, self.translator, self.apply_theme)
                flow_box.append(theme_card)
        
        scrolled_window.set_child(flow_box)
        return scrolled_window
    
    def on_layout_row_selected(self, list_box, row):
        """Handle row selection (single click)"""
        if self.updating_selection or row is None:
            return
            
        # Get the layout data directly from the row
        name = row.layout_name
        config_file = row.config_file
        
        # Select the item
        self.select_layout_item((name, config_file))
    
    def select_layout_item(self, item):
        """Select an item and update the preview"""
        self.selected_layout_item = item
        
        # Clear previous selection
        self.clear_layout_selection()
        
        # Update preview
        name, config_file = item
        self.update_layout_preview(name)
        self.highlight_selected_layout_row(name)
    
    def update_layout_preview(self, name):
        """Update the preview area"""
        self.preview_title.set_text(name)
        self.preview_description.set_text(self.translator._("description_layout").format(layout=name))
        
        # Try to load preview image
        icon_path = None
        for layout in LAYOUTS:
            if layout[0] == name:
                icon_path = SystemUtils.find_file(layout[2], ['icons'])
                break
        
        # Set image or fallback
        if icon_path and os.path.exists(icon_path):
            self.preview_image.set_filename(icon_path)
        else:
            # Use fallback icon
            fallback_image = Gtk.Image.new_from_icon_name("view-grid-symbolic")
            fallback_image.set_pixel_size(80)
            self.preview_image.set_paintable(fallback_image.get_paintable())
    
    def highlight_selected_layout_row(self, name):
        """Highlight the selected row in the list"""
        self.updating_selection = True
        
        for row, row_name, _ in self.layout_buttons:
            if row_name == name:
                row.add_css_class("selected")
                self.layout_list_box.select_row(row)
                break
        
        self.updating_selection = False
    
    def clear_layout_selection(self):
        """Clear selection from all rows"""
        self.updating_selection = True
        
        for row, _, _ in self.layout_buttons:
            row.remove_css_class("selected")
        
        self.updating_selection = False
    
    def on_test_layout_clicked(self, widget):
        """Handle test button click"""
        if self.applying or not hasattr(self, 'selected_layout_item'):
            return
        
        # Ask user if they want to test the layout
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=self.translator._("test_layout_title"),
            body=self.translator._("test_layout_message"),
        )
        
        dialog.add_response("cancel", self.translator._("cancel"))
        dialog.add_response("test", self.translator._("test_layout"))
        dialog.set_response_appearance("test", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_test_dialog_response)
        dialog.present()
    
    def on_test_dialog_response(self, dialog, response):
        """Handle response from test dialog"""
        if response == "test":
            self.test_mode = True
            self.on_apply_layout_clicked(None)
        
        dialog.destroy()
    
    def on_apply_layout_clicked(self, widget):
        """Handle apply button click"""
        if self.applying or not hasattr(self, 'selected_layout_item'):
            return
        
        # Check if GNOME Shell extensions are enabled
        if not ExtensionManager.check_gnome_extensions_enabled():
            self.show_extensions_enable_dialog()
            return
        
        # If not in test mode, ask for backup confirmation
        if not self.test_mode and not self.backup_created:
            dialog = Adw.MessageDialog(
                transient_for=self,
                heading=self.translator._("backup_before_apply"),
                body=self.translator._("backup_before_apply"),
            )
            
            dialog.add_response("skip", self.translator._("skip"))
            dialog.add_response("backup", self.translator._("backup"))
            dialog.set_response_appearance("backup", Adw.ResponseAppearance.SUGGESTED)
            
            dialog.connect("response", self.on_backup_dialog_response)
            dialog.present()
            return
        
        # Disable button and show spinner
        self.set_applying_state(True)
        
        # Start applying in a separate thread
        self.executor.submit(self.apply_selected_layout)
    
    def on_backup_dialog_response(self, dialog, response):
        """Handle response from backup dialog"""
        if response == "backup":
            # Create backup
            backup_file = BackupManager.create_backup()
            if backup_file:
                self.backup_created = True
                self.show_toast(self.translator._("backup_created"))
            else:
                self.show_toast(self.translator._("backup_error").format(error=self.translator._("unknown")))
        
        # Continue with applying layout
        self.on_apply_layout_clicked(None)
        dialog.destroy()
    
    def set_applying_state(self, applying):
        """Set the applying state of the UI"""
        self.applying = applying
        self.apply_button.set_sensitive(not applying)
        self.test_button.set_sensitive(not applying)
        
        if applying:
            self.spinner.set_visible(True)
            self.spinner.start()
        else:
            self.spinner.set_visible(False)
            self.spinner.stop()
    
    def apply_selected_layout(self):
        """Apply the selected layout in a separate thread"""
        try:
            name, config_file = self.selected_layout_item
            GLib.idle_add(self.update_status, self.translator._("applying").format(layout=name))
            
            # Find config file path
            config_path = SystemUtils.find_file(config_file, ['layouts'])
            if not config_path:
                GLib.idle_add(self.update_status, self.translator._("error_config").format(file=config_file))
                return
            
            # Apply GNOME layout
            self.apply_gnome_layout(config_path)
            
            # Give desktop time to apply changes
            time.sleep(0.5)
            
            GLib.idle_add(self.update_status, self.translator._("success").format(layout=name))
            
            # If in test mode, show dialog to keep or revert changes
            if self.test_mode:
                self.test_mode = False
                GLib.idle_add(self.show_test_result_dialog)
        except subprocess.TimeoutExpired:
            GLib.idle_add(self.update_status, self.translator._("error_applying").format(error="Operation timed out"))
        except subprocess.CalledProcessError as e:
            GLib.idle_add(self.update_status, self.translator._("error_applying").format(error=str(e)))
        except Exception as e:
            GLib.idle_add(self.update_status, self.translator._("error").format(error=str(e)))
        finally:
            # Always reset applying state
            GLib.idle_add(self.set_applying_state, False)
    
    def show_test_result_dialog(self):
        """Show dialog to keep or revert test changes"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=self.translator._("test_layout_title"),
            body=self.translator._("test_layout_message"),
        )
        
        dialog.add_response("revert", self.translator._("test_layout_revert"))
        dialog.add_response("keep", self.translator._("test_layout_keep"))
        dialog.set_response_appearance("keep", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_test_result_dialog_response)
        dialog.present()
    
    def on_test_result_dialog_response(self, dialog, response):
        """Handle response from test result dialog"""
        if response == "revert":
            # Restore from backup
            backup_file = BackupManager.get_latest_backup()
            if backup_file:
                if BackupManager.restore_backup(backup_file):
                    self.show_toast(self.translator._("backup_restore_success"))
                else:
                    self.show_toast(self.translator._("backup_restore_error").format(error=self.translator._("unknown")))
        
        dialog.destroy()
    
    def apply_gnome_layout(self, config_path):
        """Apply GNOME layout using dconf"""
        # Use a more robust approach to apply the layout
        with open(config_path, 'r') as f:
            config_data = f.read()
        
        # Write to a temporary file to avoid issues
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp_file:
            temp_file.write(config_data)
            temp_file_path = temp_file.name
        
        try:
            # Apply the configuration
            subprocess.run(
                ["dconf", "load", "/org/gnome/shell/"],
                stdin=open(temp_file_path, 'r'),
                check=True,
                timeout=10
            )
        finally:
            # Clean up temporary file
            os.unlink(temp_file_path)
    
    def update_status(self, message):
        """Update the status bar safely from any thread"""
        self.status_bar.set_label(message)
        return False  # Don't call again
    
    def show_extensions_enable_dialog(self):
        """Show dialog to enable GNOME Shell extensions"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=self.translator._("extensions_disabled"),
            body=self.translator._("extensions_enable_prompt"),
        )
        
        dialog.add_response("cancel", self.translator._("cancel"))
        dialog.add_response("enable", self.translator._("enable"))
        dialog.set_response_appearance("enable", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_extensions_enable_dialog_response)
        dialog.present()
    
    def on_extensions_enable_dialog_response(self, dialog, response):
        """Handle response from extensions enable dialog"""
        if response == "enable":
            if ExtensionManager.enable_gnome_extensions():
                self.show_toast(self.translator._("extensions_enabled_success"))
                # Now, try to apply the layout again
                self.on_apply_layout_clicked(None)
            else:
                self.show_toast(self.translator._("extensions_enable_error").format(error=self.translator._("unknown")))
        
        dialog.destroy()
    
    def toggle_extension(self, uuid: str, enable: bool):
        """Toggle a GNOME extension"""
        if ExtensionManager.toggle_extension(uuid, enable):
            self.show_toast(f"{uuid} {'enabled' if enable else 'disabled'}")
        else:
            self.show_toast(f"Error toggling extension")
    
    def open_extension_settings(self, uuid: str):
        """Open the settings for a GNOME extension"""
        try:
            # Try to open the extension settings directly
            subprocess.run(["gnome-extensions-app", "prefs", uuid], check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to opening the extensions app
            try:
                subprocess.run(["gnome-extensions-app"], check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Last resort: open extensions.gnome.org
                self.open_url(f"https://extensions.gnome.org/extension/{uuid.split('@')[0]}/")
    
    def open_url(self, url: str):
        """Open a URL in the default browser"""
        subprocess.run(["xdg-open", url], check=True)
    
    def apply_theme(self, theme_name: str, theme_type: str):
        """Apply a theme using gsettings"""
        # Start applying in a separate thread
        self.executor.submit(self._apply_theme_thread, theme_name, theme_type)
    
    def _apply_theme_thread(self, theme_name: str, theme_type: str):
        """Apply the selected theme in a separate thread"""
        try:
            if theme_type == "shell":
                print(f"Applying shell theme: {theme_name}")
                GLib.idle_add(self.update_status, self.translator._("applying_shell").format(theme=theme_name))
                
                # Check if User Themes extension is installed and enabled
                user_theme_uuid = "user-theme@gnome-shell-extensions.gcampax.github.com"
                
                if not ExtensionManager.check_extension_installed(user_theme_uuid):
                    print("User Themes extension is not installed")
                    GLib.idle_add(self.show_user_theme_dialog)
                    return
                
                if not ExtensionManager.check_extension_enabled(user_theme_uuid):
                    print("User Themes extension is not enabled")
                    GLib.idle_add(self.show_user_theme_dialog)
                    return
                
                # Apply shell theme using dconf
                try:
                    print(f"Running: dconf write /org/gnome/shell/extensions/user-theme/name '{theme_name}'")
                    subprocess.run(
                        ["dconf", "write", "/org/gnome/shell/extensions/user-theme/name", f"'{theme_name}'"],
                        check=True
                    )
                    print("Command completed successfully")
                    
                    # Verify the setting
                    result = subprocess.run(
                        ["dconf", "read", "/org/gnome/shell/extensions/user-theme/name"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    current_theme = result.stdout.strip().strip("'").strip('"')
                    print(f"Current shell theme after setting: {current_theme}")
                    
                    if current_theme == theme_name:
                        GLib.idle_add(self.update_status, self.translator._("success_shell").format(theme=theme_name))
                        GLib.idle_add(self.show_toast, self.translator._("shell_theme_restart"))
                    else:
                        GLib.idle_add(self.update_status, self.translator._("error_shell").format(error=f"Theme not set. Current: {current_theme}"))
                except subprocess.CalledProcessError as e:
                    print(f"Error applying shell theme: {e}")
                    GLib.idle_add(self.update_status, self.translator._("error_shell").format(error=str(e)))
                except Exception as e:
                    print(f"Unexpected error applying shell theme: {e}")
                    GLib.idle_add(self.update_status, self.translator._("error").format(error=str(e)))
            
            elif theme_type == "gtk":
                GLib.idle_add(self.update_status, self.translator._("applying_gtk").format(theme=theme_name))
                
                # Apply GTK theme using dconf
                try:
                    print(f"Running: dconf write /org/gnome/desktop/interface/gtk-theme '{theme_name}'")
                    subprocess.run(
                        ["dconf", "write", "/org/gnome/desktop/interface/gtk-theme", f"'{theme_name}'"],
                        check=True
                    )
                    
                    # Verify the setting
                    result = subprocess.run(
                        ["dconf", "read", "/org/gnome/desktop/interface/gtk-theme"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    current_theme = result.stdout.strip().strip("'").strip('"')
                    print(f"Current GTK theme after setting: {current_theme}")
                    
                    if current_theme == theme_name:
                        GLib.idle_add(self.update_status, self.translator._("success_gtk").format(theme=theme_name))
                        GLib.idle_add(self.show_toast, self.translator._("gtk_theme_restart"))
                    else:
                        GLib.idle_add(self.update_status, self.translator._("error_gtk").format(error=f"Theme not set. Current: {current_theme}"))
                except subprocess.CalledProcessError as e:
                    GLib.idle_add(self.update_status, self.translator._("error_gtk").format(error=str(e)))
                except Exception as e:
                    GLib.idle_add(self.update_status, self.translator._("error").format(error=str(e)))
            
            elif theme_type == "icons":
                GLib.idle_add(self.update_status, self.translator._("applying_icons").format(theme=theme_name))
                
                # Apply icon theme using dconf
                try:
                    print(f"Running: dconf write /org/gnome/desktop/interface/icon-theme '{theme_name}'")
                    subprocess.run(
                        ["dconf", "write", "/org/gnome/desktop/interface/icon-theme", f"'{theme_name}'"],
                        check=True
                    )
                    
                    # Verify the setting
                    result = subprocess.run(
                        ["dconf", "read", "/org/gnome/desktop/interface/icon-theme"],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    current_theme = result.stdout.strip().strip("'").strip('"')
                    print(f"Current icon theme after setting: {current_theme}")
                    
                    if current_theme == theme_name:
                        GLib.idle_add(self.update_status, self.translator._("success_icons").format(theme=theme_name))
                        GLib.idle_add(self.show_toast, self.translator._("icon_theme_restart"))
                    else:
                        GLib.idle_add(self.update_status, self.translator._("error_icons").format(error=f"Theme not set. Current: {current_theme}"))
                except subprocess.CalledProcessError as e:
                    GLib.idle_add(self.update_status, self.translator._("error_icons").format(error=str(e)))
                except Exception as e:
                    GLib.idle_add(self.update_status, self.translator._("error").format(error=str(e)))
            
        except Exception as e:
            GLib.idle_add(self.update_status, self.translator._("error").format(error=str(e)))
    
    def show_user_theme_dialog(self):
        """Show dialog to install User Themes extension"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=self.translator._("user_theme_required"),
            body=self.translator._("user_theme_required"),
        )
        
        dialog.add_response("cancel", self.translator._("cancel"))
        dialog.add_response("install", self.translator._("install_user_theme"))
        dialog.set_response_appearance("install", Adw.ResponseAppearance.SUGGESTED)
        
        dialog.connect("response", self.on_user_theme_dialog_response)
        dialog.present()
    
    def on_user_theme_dialog_response(self, dialog, response):
        """Handle response from User Themes dialog"""
        if response == "install":
            # Open extensions.gnome.org for User Themes extension
            self.open_url("https://extensions.gnome.org/extension/19/user-themes/")
        
        dialog.destroy()
    
    def show_toast(self, message):
        """Show a toast notification"""
        toast = Adw.Toast.new(message)
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)
    
    def on_resize(self, widget, param):
        """Handle window resize for responsive adjustments"""
        width = self.get_width()
        
        # Adjust preview image size if in layouts tab
        if hasattr(self, 'preview_image'):
            if width < 700:
                self.preview_image.set_size_request(280, 140)
            else:
                self.preview_image.set_size_request(330, 160)
    
    def show_intro_dialog(self):
        """Show introduction dialog"""
        dialog = Adw.MessageDialog(
            transient_for=self,
            heading=self.translator._("intro_title"),
            body=self.translator._("intro_message"),
        )
        
        dialog.add_response("close", self.translator._("close"))
        dialog.set_response_appearance("close", Adw.ResponseAppearance.SUGGESTED)
        
        # Add "Don't show again" checkbox
        dont_show_check = Gtk.CheckButton(label=self.translator._("intro_dont_show"))
        dont_show_check.set_margin_top(12)
        dont_show_check.set_halign(Gtk.Align.CENTER)
        dialog.set_extra_child(dont_show_check)
        
        dialog.connect("response", self.on_intro_dialog_response, dont_show_check)
        dialog.present()
    
    def on_intro_dialog_response(self, dialog, response, dont_show_check):
        """Handle response from intro dialog"""
        if dont_show_check.get_active():
            self.settings_manager.set("intro_shown", True)
        
        dialog.destroy()
    
    def load_css(self):
        """Load CSS for styling"""
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"""
            .layout-row {
                border-radius: 8px;
                margin: 4px;
                transition: all 200ms ease;
                min-height: 70px;
            }
            .layout-row:hover {
                background-color: alpha(@theme_fg_color, 0.1);
            }
            .layout-row.selected {
                background-color: @theme_selected_bg_color;
                color: @theme_selected_fg_color;
            }
            .icon-container {
                background-color: alpha(@theme_fg_color, 0.05);
                border-radius: 12px;
                padding: 6px;
            }
            .icon-frame {
                background-color: alpha(@theme_fg_color, 0.1);
                border-radius: 8px;
                padding: 4px;
            }
            .layout-label {
                font-weight: 500;
                font-size: 13pt;
            }
            .success {
                color: #26a269;
                font-weight: bold;
            }
            .theme-card {
                transition: all 200ms ease;
            }
            .theme-card:hover {
                transform: translateY(-5px);
            }
        """)
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
