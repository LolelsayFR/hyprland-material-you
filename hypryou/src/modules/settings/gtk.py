from src.modules.settings.base import SettingsBoolRow, SettingsTextRow, SettingsDropdownRow
from src.modules.settings.base import Category, DropdownItem
from src.modules.settings.base import int_kwargs, float_kwargs
from repository import gtk
from config import Settings
import subprocess
import os
import json


def get_gtk_themes():
    """Get list of installed GTK themes"""
    themes = set()
    theme_dirs = [
        os.path.expanduser("~/.themes"),
        os.path.expanduser("~/.local/share/themes"),
        "/usr/share/themes"
    ]
    try:
        for theme_dir in theme_dirs:
            if os.path.exists(theme_dir):
                for theme in os.listdir(theme_dir)[:50]:  # Limiter à 50
                    if os.path.isdir(os.path.join(theme_dir, theme)) and not theme.startswith('.'):
                        themes.add(theme)
        return sorted(themes) if themes else ["Adwaita", "Adwaita-dark"]
    except Exception:
        return ["Adwaita", "Adwaita-dark"]


def get_icon_themes():
    """Get list of installed icon themes"""
    icons = set()
    icon_dirs = [
        os.path.expanduser("~/.icons"),
        os.path.expanduser("~/.local/share/icons"),
        "/usr/share/icons"
    ]
    try:
        for icon_dir in icon_dirs:
            if os.path.exists(icon_dir):
                for icon in os.listdir(icon_dir)[:50]:  # Limiter à 50
                    if os.path.isdir(os.path.join(icon_dir, icon)) and not icon.startswith('.'):
                        icons.add(icon)
        return sorted(icons) if icons else ["Adwaita", "breeze", "hicolor"]
    except Exception:
        return ["Adwaita", "breeze", "hicolor"]


def get_cursor_themes():
    """Get list of installed cursor themes"""
    cursors = set()
    cursor_dirs = [
        os.path.expanduser("~/.icons"),
        os.path.expanduser("~/.local/share/icons"),
        "/usr/share/icons"
    ]
    try:
        for cursor_dir in cursor_dirs:
            if os.path.exists(cursor_dir):
                for cursor in os.listdir(cursor_dir)[:50]:  # Limiter à 50
                    cursor_path = os.path.join(cursor_dir, cursor, "cursors")
                    if os.path.exists(cursor_path) and not cursor.startswith('.'):
                        cursors.add(cursor)
        return sorted(cursors) if cursors else ["Adwaita", "breeze_cursors"]
    except Exception:
        return ["Adwaita", "breeze_cursors"]


def get_fonts():
    """Get list of system fonts"""
    try:
        result = subprocess.run(
            ["fc-list", ":family", "style=Regular"],
            capture_output=True,
            text=True,
            timeout=2  # Timeout de 2 secondes
        )
        fonts = []
        seen = set()
        for line in result.stdout.split('\n')[:100]:  # Limiter à 100 premiers
            if line.strip() and ':' in line:
                font_name = line.split(':')[0].strip()
                if font_name not in seen:
                    seen.add(font_name)
                    fonts.append(font_name)
        return sorted(fonts)[:50] if fonts else ["Sans", "Serif", "Monospace", "Google Sans", "JetBrains Mono"]
    except Exception:
        return ["Sans", "Serif", "Monospace", "Google Sans", "JetBrains Mono"]


class GTKPage(gtk.ScrolledWindow):
    __gtype_name__ = "SettingsGTKPage"

    def __init__(self) -> None:
        self.box = gtk.Box(
            css_classes=("page-box",),
            orientation=gtk.Orientation.VERTICAL
        )
        super().__init__(
            css_classes=("gtk-page", "settings-page",),
            child=self.box,
            hscrollbar_policy=gtk.PolicyType.NEVER
        )
        
        # Utiliser des listes minimales par défaut pour éviter le timeout au démarrage
        gtk_themes = [DropdownItem("Adwaita", "Adwaita"), DropdownItem("Adwaita-dark", "Adwaita-dark")]
        icon_themes = [DropdownItem("Adwaita", "Adwaita"), DropdownItem("breeze", "breeze")]
        cursor_themes = [DropdownItem("Adwaita", "Adwaita"), DropdownItem("breeze_cursors", "breeze_cursors")]
        fonts = [
            DropdownItem("Sans", "Sans"),
            DropdownItem("Serif", "Serif"),
            DropdownItem("Monospace", "Monospace"),
            DropdownItem("Google Sans", "Google Sans"),
            DropdownItem("JetBrains Mono", "JetBrains Mono"),
            DropdownItem("Noto Sans", "Noto Sans"),
            DropdownItem("DejaVu Sans", "DejaVu Sans"),
            DropdownItem("Liberation Sans", "Liberation Sans")
        ]
        font_styles = [
            DropdownItem("Regular", "Regular"),
            DropdownItem("Bold", "Bold"),
            DropdownItem("Italic", "Italic"),
            DropdownItem("Bold Italic", "Bold Italic"),
            DropdownItem("Light", "Light"),
            DropdownItem("Medium", "Medium"),
            DropdownItem("SemiBold", "SemiBold")
        ]
        
        self.children = (
            Category("GTK Theme"),
            SettingsDropdownRow(
                "GTK Theme",
                "Choose GTK3/4 application theme",
                "gtk.theme",
                gtk_themes
            ),
            SettingsBoolRow(
                "Prefer Dark Theme",
                "Request dark variant of GTK theme",
                "gtk.prefer_dark_theme"
            ),
            
            Category("Icons"),
            SettingsDropdownRow(
                "Icon Theme",
                "Choose icon theme for applications",
                "gtk.icon_theme",
                icon_themes
            ),
            SettingsBoolRow(
                "Enable Icon Fallback",
                "Use fallback icons when theme icons are missing",
                "gtk.icon_fallback"
            ),
            
            Category("Cursor"),
            SettingsDropdownRow(
                "Cursor Theme",
                "Choose mouse cursor theme",
                "gtk.cursor_theme",
                cursor_themes
            ),
            SettingsTextRow(
                "Cursor Size",
                "Size of mouse cursor in pixels (16-48)",
                "gtk.cursor_size",
                max_width_chars=3,
                **int_kwargs
            ),
            
            Category("Fonts"),
            SettingsDropdownRow(
                "Interface Font",
                "Font family for GTK applications",
                "gtk.font",
                fonts
            ),
            SettingsDropdownRow(
                "Interface Font Style",
                "Style for interface font",
                "gtk.font_style",
                font_styles
            ),
            SettingsTextRow(
                "Font Size",
                "Default font size in points (8-16)",
                "gtk.font_size",
                max_width_chars=3,
                **int_kwargs
            ),
            SettingsDropdownRow(
                "Monospace Font",
                "Font family for code editors and terminals",
                "gtk.monospace_font",
                fonts
            ),
            SettingsDropdownRow(
                "Monospace Font Style",
                "Style for monospace font",
                "gtk.monospace_font_style",
                font_styles
            ),
            
            Category("Behavior"),
            SettingsBoolRow(
                "Enable Animations",
                "Enable GTK animations (dialogs, menus, etc.)",
                "gtk.enable_animations"
            ),
            SettingsBoolRow(
                "Enable Overlay Scrollbars",
                "Use overlay scrollbars (auto-hide)",
                "gtk.overlay_scrollbars"
            ),
            SettingsTextRow(
                "Double Click Time",
                "Maximum time between clicks (ms)",
                "gtk.double_click_time",
                max_width_chars=4,
                **int_kwargs
            ),
            SettingsBoolRow(
                "Show Hidden Files",
                "Show hidden files in file chooser dialogs",
                "gtk.show_hidden_files"
            ),
            
            Category("Advanced"),
            SettingsBoolRow(
                "Enable Client Side Decorations",
                "Use client-side window decorations (CSD)",
                "gtk.enable_csd"
            ),
            SettingsBoolRow(
                "Enable Mnemonics",
                "Show keyboard mnemonics (underlined letters)",
                "gtk.enable_mnemonics"
            ),
            SettingsTextRow(
                "DPI Scale",
                "Text scaling factor (1.0 = 96 DPI)",
                "gtk.dpi_scale",
                max_width_chars=4,
                **float_kwargs
            )
        )

        for child in self.children:
            self.box.append(child)
        
        # Boutons Apply et Save
        button_box = gtk.Box(
            orientation=gtk.Orientation.HORIZONTAL,
            spacing=12,
            halign=gtk.Align.CENTER,
            css_classes=("gtk-buttons-box",)
        )
        button_box.set_margin_top(24)
        button_box.set_margin_bottom(24)
        
        self.apply_button = gtk.Button(
            label="Apply",
            css_classes=("apply-button", "suggested-action")
        )
        self.apply_button.connect("clicked", self._on_apply_clicked)
        
        self.save_button = gtk.Button(
            label="Save",
            css_classes=("save-button", "suggested-action")
        )
        self.save_button.connect("clicked", self._on_save_clicked)
        
        button_box.append(self.apply_button)
        button_box.append(self.save_button)
        self.box.append(button_box)
    
    def _on_apply_clicked(self, button):
        """Apply GTK settings temporarily (runtime only)"""
        settings = Settings()
        
        # Appliquer via gsettings
        try:
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "gtk-theme", settings.gtk.theme], check=False)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "icon-theme", settings.gtk.icon_theme], check=False)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "cursor-theme", settings.gtk.cursor_theme], check=False)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "cursor-size", str(settings.gtk.cursor_size)], check=False)
            
            # Police avec style
            font_style = getattr(settings.gtk, 'font_style', 'Regular')
            font_string = f"{settings.gtk.font} {font_style} {settings.gtk.font_size}"
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "font-name", font_string], check=False)
            
            monospace_style = getattr(settings.gtk, 'monospace_font_style', 'Regular')
            monospace_string = f"{settings.gtk.monospace_font} {monospace_style} {settings.gtk.font_size}"
            subprocess.run(["gsettings", "set", "org.gnome.desktop.interface", "monospace-font-name", monospace_string], check=False)
            
            print("✓ GTK settings applied (temporary)")
        except Exception as e:
            print(f"✗ Error applying GTK settings: {e}")
    
    def _on_save_clicked(self, button):
        """Save GTK settings to config file"""
        settings = Settings()
        settings_path = os.path.expanduser("~/.config/hypryou/settings.json")
        
        try:
            # Lire le fichier existant
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as f:
                    data = json.load(f)
            else:
                data = {}
            
            # Mettre à jour les valeurs GTK
            if 'gtk' not in data:
                data['gtk'] = {}
            
            data['gtk']['theme'] = settings.gtk.theme
            data['gtk']['icon_theme'] = settings.gtk.icon_theme
            data['gtk']['cursor_theme'] = settings.gtk.cursor_theme
            data['gtk']['cursor_size'] = settings.gtk.cursor_size
            data['gtk']['font'] = settings.gtk.font
            data['gtk']['font_style'] = getattr(settings.gtk, 'font_style', 'Regular')
            data['gtk']['font_size'] = settings.gtk.font_size
            data['gtk']['monospace_font'] = settings.gtk.monospace_font
            data['gtk']['monospace_font_style'] = getattr(settings.gtk, 'monospace_font_style', 'Regular')
            
            # Sauvegarder
            os.makedirs(os.path.dirname(settings_path), exist_ok=True)
            with open(settings_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            print("✓ GTK settings saved to", settings_path)
            
            # Appliquer aussi
            self._on_apply_clicked(button)
        except Exception as e:
            print(f"✗ Error saving GTK settings: {e}")
