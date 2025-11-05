"""
UI component classes for the Community Layout Switcher application.
"""

import os
import subprocess
import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Adw, Pango, GLib
from typing import Dict, List, Tuple, Optional

from constants import LAYOUTS, EXTENSIONS
from managers import ThemeManager, ExtensionManager, SystemUtils


class LayoutRow(Gtk.ListBoxRow):
    """Custom layout row widget"""
    
    def __init__(self, name: str, icon_file: str, fallback_icon: str, config_file: str, translator):
        super().__init__()
        self.add_css_class("layout-row")
        
        # Store the layout data
        self.layout_name = name
        self.config_file = config_file
        
        # Create row content
        row_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        row_box.set_margin_start(12)
        row_box.set_margin_end(12)
        row_box.set_margin_top(10)
        row_box.set_margin_bottom(10)
        
        # Create icon container
        icon_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        icon_container.set_size_request(60, 60)
        icon_container.add_css_class("icon-container")
        
        # Icon frame
        icon_frame = Gtk.Box()
        icon_frame.set_size_request(48, 48)
        icon_frame.add_css_class("icon-frame")
        icon_frame.set_halign(Gtk.Align.CENTER)
        icon_frame.set_valign(Gtk.Align.CENTER)
        
        # Create image
        image = Gtk.Picture()
        image.set_size_request(40, 40)
        image.set_content_fit(Gtk.ContentFit.CONTAIN)
        image.set_halign(Gtk.Align.CENTER)
        image.set_valign(Gtk.Align.CENTER)
        
        # Try to load custom icon
        if icon_file:
            icon_path = SystemUtils.find_file(icon_file, ['icons'])
            if icon_path:
                image.set_filename(icon_path)
            else:
                # Use fallback icon
                fallback_image = Gtk.Image.new_from_icon_name(fallback_icon)
                fallback_image.set_pixel_size(32)
                image.set_paintable(fallback_image.get_paintable())
        else:
            # Use fallback icon
            fallback_image = Gtk.Image.new_from_icon_name(fallback_icon)
            fallback_image.set_pixel_size(32)
            image.set_paintable(fallback_image.get_paintable())
        
        icon_frame.append(image)
        icon_container.append(icon_frame)
        
        # Create label
        label = Gtk.Label(label=name)
        label.add_css_class("layout-label")
        label.set_halign(Gtk.Align.START)
        label.set_valign(Gtk.Align.CENTER)
        label.set_ellipsize(Pango.EllipsizeMode.END)
        label.set_max_width_chars(12)
        
        # Add to row box
        row_box.append(icon_container)
        row_box.append(label)
        self.set_child(row_box)


class ThemeCard(Gtk.Box):
    """Custom theme card widget"""
    
    def __init__(self, theme_name: str, theme_path: str, theme_type: str, translator, on_apply):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.add_css_class("card")
        self.set_size_request(200, 200)
        self.set_margin_start(10)
        self.set_margin_end(10)
        self.set_margin_top(10)
        self.set_margin_bottom(10)
        
        # Extract color from theme name
        color = ThemeManager.extract_color_from_theme_name(theme_name)
        
        # Create color circle
        color_circle = Gtk.DrawingArea()
        color_circle.set_size_request(80, 80)
        color_circle.set_halign(Gtk.Align.CENTER)
        color_circle.set_margin_top(20)
        color_circle.set_draw_func(self._draw_color_circle, color)
        self.append(color_circle)
        
        # Theme name
        name_label = Gtk.Label()
        name_label.set_text(theme_name)
        name_label.add_css_class("title-4")
        name_label.set_margin_top(15)
        name_label.set_halign(Gtk.Align.CENTER)
        name_label.set_ellipsize(Pango.EllipsizeMode.END)
        name_label.set_max_width_chars(15)
        self.append(name_label)
        
        # Apply button
        apply_button = Gtk.Button(label=translator._("apply_theme"))
        apply_button.add_css_class("pill")
        apply_button.set_margin_top(15)
        apply_button.set_margin_bottom(20)
        apply_button.set_halign(Gtk.Align.CENTER)
        apply_button.connect("clicked", lambda btn: on_apply(theme_name, theme_type))
        self.append(apply_button)
    
    def _draw_color_circle(self, drawing_area, ctx, width, height, color):
        """Draw a color circle"""
        # Set background color
        ctx.set_source_rgb(int(color[1:3], 16)/255, int(color[3:5], 16)/255, int(color[5:7], 16)/255)
        
        # Draw circle
        ctx.arc(width/2, height/2, min(width, height)/2 - 5, 0, 2 * 3.14159)
        ctx.fill()


class EffectCard(Gtk.Box):
    """Custom effect card widget"""
    
    def __init__(self, effect: Dict, translator, on_toggle, on_install, on_settings):
        super().__init__(orientation=Gtk.Orientation.VERTICAL)
        self.add_css_class("card")
        self.set_size_request(250, 220)
        self.effect = effect
        self.translator = translator
        
        # Effect icon
        effect_icon = Gtk.Image.new_from_icon_name("applications-graphics-symbolic")
        effect_icon.set_pixel_size(48)
        effect_icon.set_margin_top(20)
        effect_icon.set_halign(Gtk.Align.CENTER)
        self.append(effect_icon)
        
        # Effect name
        effect_name = Gtk.Label()
        effect_name.set_text(effect["name"])
        effect_name.add_css_class("title-3")
        effect_name.set_margin_top(10)
        effect_name.set_halign(Gtk.Align.CENTER)
        self.append(effect_name)
        
        # Effect description
        effect_description = Gtk.Label()
        effect_description.set_text(effect["description"])
        effect_description.add_css_class("body")
        effect_description.set_margin_top(5)
        effect_description.set_margin_bottom(15)
        effect_description.set_halign(Gtk.Align.CENTER)
        effect_description.set_wrap(True)
        effect_description.set_max_width_chars(20)
        self.append(effect_description)
        
        # Check if extension is installed
        installed = ExtensionManager.check_extension_installed(effect["uuid"])
        
        if installed:
            # Check if extension is enabled
            enabled = ExtensionManager.check_extension_enabled(effect["uuid"])
            
            # Create toggle switch
            toggle = Gtk.Switch()
            toggle.set_active(enabled)
            toggle.set_halign(Gtk.Align.CENTER)
            toggle.set_margin_bottom(10)
            toggle.connect("notify::active", lambda switch, _: on_toggle(effect["uuid"], switch.get_active()))
            self.append(toggle)
            
            # Status label
            status_label = Gtk.Label()
            status_label.set_text(translator._("enable") if not enabled else translator._("disable"))
            status_label.add_css_class("body")
            status_label.set_halign(Gtk.Align.CENTER)
            status_label.set_margin_bottom(10)
            self.append(status_label)
            
            # Add settings button if extension has settings and is enabled
            if effect.get("has_settings", False) and enabled:
                settings_button = Gtk.Button()
                settings_button.set_icon_name("settings-symbolic")
                settings_button.set_tooltip_text(translator._("extension_settings"))
                settings_button.set_halign(Gtk.Align.CENTER)
                settings_button.set_margin_bottom(10)
                settings_button.connect("clicked", lambda btn: on_settings(effect["uuid"]))
                self.append(settings_button)
        else:
            # Install button
            install_button = Gtk.Button(label=translator._("install_extension"))
            install_button.add_css_class("pill")
            install_button.set_margin_bottom(20)
            install_button.connect("clicked", lambda btn: on_install(effect["url"]))
            self.append(install_button)
