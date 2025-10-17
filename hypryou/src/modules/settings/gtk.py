from src.modules.settings.base import SettingsBoolRow, SettingsTextRow, SettingsDropdownRow
from src.modules.settings.base import Category
from src.modules.settings.base import int_kwargs, float_kwargs
from repository import gtk
import subprocess
import os


def get_gtk_themes():
    """Get list of installed GTK themes"""
    themes = []
    theme_dirs = [
        os.path.expanduser("~/.themes"),
        os.path.expanduser("~/.local/share/themes"),
        "/usr/share/themes"
    ]
    for theme_dir in theme_dirs:
        if os.path.exists(theme_dir):
            for theme in os.listdir(theme_dir):
                if os.path.isdir(os.path.join(theme_dir, theme)):
                    if theme not in themes:
                        themes.append(theme)
    return sorted(themes) if themes else ["Adwaita", "Adwaita-dark"]


def get_icon_themes():
    """Get list of installed icon themes"""
    icons = []
    icon_dirs = [
        os.path.expanduser("~/.icons"),
        os.path.expanduser("~/.local/share/icons"),
        "/usr/share/icons"
    ]
    for icon_dir in icon_dirs:
        if os.path.exists(icon_dir):
            for icon in os.listdir(icon_dir):
                if os.path.isdir(os.path.join(icon_dir, icon)):
                    if icon not in icons and not icon.startswith('.'):
                        icons.append(icon)
    return sorted(icons) if icons else ["Adwaita", "breeze", "hicolor"]


def get_cursor_themes():
    """Get list of installed cursor themes"""
    cursors = []
    cursor_dirs = [
        os.path.expanduser("~/.icons"),
        os.path.expanduser("~/.local/share/icons"),
        "/usr/share/icons"
    ]
    for cursor_dir in cursor_dirs:
        if os.path.exists(cursor_dir):
            for cursor in os.listdir(cursor_dir):
                cursor_path = os.path.join(cursor_dir, cursor, "cursors")
                if os.path.exists(cursor_path):
                    if cursor not in cursors and not cursor.startswith('.'):
                        cursors.append(cursor)
    return sorted(cursors) if cursors else ["Adwaita", "breeze_cursors"]


def get_fonts():
    """Get list of system fonts"""
    try:
        result = subprocess.run(
            ["fc-list", ":family", "style=Regular"],
            capture_output=True,
            text=True
        )
        fonts = []
        for line in result.stdout.split('\n'):
            if line.strip() and ':' in line:
                font_name = line.split(':')[0].strip()
                if font_name not in fonts:
                    fonts.append(font_name)
        return sorted(fonts) if fonts else ["Sans", "Serif", "Monospace"]
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
        
        self.children = (
            Category("GTK Theme"),
            SettingsDropdownRow(
                "GTK Theme",
                "Choose GTK3/4 application theme",
                "gtk.theme",
                options=get_gtk_themes()
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
                options=get_icon_themes()
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
                options=get_cursor_themes()
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
                "Default font for GTK applications",
                "gtk.font",
                options=get_fonts()
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
                "Font for code editors and terminals",
                "gtk.monospace_font",
                options=get_fonts()
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
