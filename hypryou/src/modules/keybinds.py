from repository import layer_shell, gtk
import weakref
from utils.logger import logger
from src.services.hyprland_keybinds import key_binds
from src.services.hyprland_keybinds.common import Category, sync_keybind_with_hyprland
from src.services.hyprland_keybinds.common import KeyBind
from src.services.hyprland_keybinds.common import KeyBindHint
import src.widget as widget


ICONS = {
    "super": "keyboard_command_key",
    "shift": "shift",
    "up": "arrow_upward",
    "down": "arrow_downward",
    "right": "arrow_right",
    "left": "arrow_left",
    "space": "space_bar"
}

REPLACE = {
    "slash": "/",
    "minus": "-",
    "plus": "+",
    "period": ".",
    "comma": ",",
    "semicolon": ";",
    "grave": "`",
    "equala": "=",
    "bracketleft": "[",
    "bracketright": "]",
    "backslash": "\\",
    "apostrophe": "'"
}

# Icônes pour les touches XF86 et touches uniques
XF86_ICONS = {
    "xf86audioplay": "play_circle",
    "xf86audiopause": "pause_circle",
    "xf86audionext": "skip_next",
    "xf86audioprev": "skip_previous",
    "xf86audiostop": "stop_circle",
    "xf86audiorewind": "fast_rewind",
    "xf86audioforward": "fast_forward",
    "xf86audiomute": "volume_off",
    "xf86audiolowervolume": "volume_down",
    "xf86audioraisevolume": "volume_up",
    "xf86audiomic": "mic",
    "xf86audiomicmute": "mic_off",
    "xf86monbrightnessdown": "brightness_low",
    "xf86monbrightnessup": "brightness_high",
    "xf86display": "monitor",
    "xf86wlan": "wifi",
    "xf86bluetooth": "bluetooth",
    "xf86tools": "settings",
    "xf86keyboard": "keyboard",
    "xf86favorites": "folder_special",
    "xf86notificationcenter": "notifications",
    "xf86pickupphone": "call",
    "xf86hangupphone": "call_end",
    "xf86rfkill": "airplanemode_active",
    "xf86launcha": "apps",
    "xf86launchb": "tune",
    "xf86homepage": "home",
    "xf86mail": "mail",
    "xf86search": "search",
    "xf86explorer": "folder_open",
    "xf86calculator": "calculate",
    "xf86lock": "lock",
    "xf86screensaver": "screen_lock_portrait",
    "xf86sleep": "bedtime",
    "xf86poweroff": "power_settings_new"
}

CATEGORIES = {
    Category.ACTIONS: "action_key",
    Category.TOOLS: "build",
    Category.APPS: "apps",
    Category.WINDOWS: "select_window",
    Category.WORKSPACES: "overview_key",
    Category.MISC: "construction"
}


class KeybindWidget(gtk.Box):
    def __init__(self, keybind: KeyBind | KeyBindHint) -> None:
        super().__init__(
            css_classes=("keybind",),
            spacing=4
        )
        self.keybind = keybind
        
        # Vérifier si c'est une touche unique (sans modifier)
        is_single_key = len(keybind.bind) == 1 or (len(keybind.bind) == 2 and keybind.bind[0] == "")
        single_key = keybind.bind[-1].lower() if is_single_key else None
        
        # Si touche unique avec icône XF86, afficher l'icône avant
        if is_single_key and single_key and single_key in XF86_ICONS:
            self.append(
                widget.Icon(
                    XF86_ICONS[single_key],
                    css_classes=("function-icon",)
                )
            )
        
        # Afficher les touches du bind
        bind_box = gtk.Box(css_classes=("bind-keys",))
        for i in range(0, len(keybind.bind)):
            key = keybind.bind[i].lower()
            # Ignorer les modifiers vides
            if key == "":
                continue
            is_end = i >= len(keybind.bind) - 1
            if key in ICONS:
                bind_box.append(
                    widget.Icon(
                        ICONS[key],
                        css_classes=("bind-key",)
                    )
                )
            else:
                if key in REPLACE:
                    key = REPLACE[key]
                # Pour les touches XF86, afficher un nom court
                display_key = key
                if key.startswith("xf86"):
                    # Extraire le nom après XF86
                    display_key = key[4:].capitalize()
                    if len(display_key) > 12:
                        display_key = display_key[:12] + "..."
                else:
                    display_key = key.capitalize()
                
                bind_box.append(
                    gtk.Label(
                        label=display_key, css_classes=("bind-key",)
                    )
                )
            if not is_end and len([k for k in keybind.bind if k != ""]) > 1:
                bind_box.append(gtk.Label(label="+", css_classes=("plus",)))
        
        self.append(bind_box)
        self.append(
            gtk.Label(
                label=f" - {keybind.description}",
                css_classes=("description",),
                halign=gtk.Align.START,
                xalign=0
            )
        )


class KeybindsBox(gtk.FlowBox):
    __gtype_name__ = "KeybindsBox"

    def __init__(self) -> None:
        super().__init__(
            css_classes=("keybinds-box",),
            selection_mode=gtk.SelectionMode.NONE,
            hexpand=True,
            max_children_per_line=3,
            min_children_per_line=3,
            row_spacing=8,
            column_spacing=8,
            homogeneous=True
        )
        self.boxes: dict[Category, gtk.Box] = {}
        for category, icon in CATEGORIES.items():
            box = gtk.Box(
                css_classes=("category-box",),
                orientation=gtk.Orientation.VERTICAL
            )
            label_box = gtk.Box(
                css_classes=("label-box",)
            )
            _icon = widget.Icon(icon)
            label = gtk.Label(
                label=category,
                css_classes=("category",),
                halign=gtk.Align.START
            )
            label_box.append(_icon)
            label_box.append(label)

            box.append(label_box)
            box.append(gtk.Separator())
            self.boxes[category] = box
            self.append(box)
        for keybind in key_binds:
            if not keybind.description or not keybind.category:
                continue
            # Synchroniser avec les keybinds réels de Hyprland
            synced_keybind = sync_keybind_with_hyprland(keybind)
            _widget = KeybindWidget(synced_keybind)
            self.boxes[keybind.category].append(_widget)

    def destroy(self) -> None:
        ...


class KeybindsWindow(widget.LayerWindow):
    __gtype_name__ = "KeybindsWindow"

    def __init__(self, app: gtk.Application) -> None:
        self.box = gtk.Box(
            hexpand=True,
            vexpand=True
        )
        super().__init__(
            app,
            css_classes=("keybinds",),
            keymode=layer_shell.KeyboardMode.ON_DEMAND,
            layer=layer_shell.Layer.OVERLAY,
            hide_on_esc=True,
            name="keybindings",
            height=1,
            width=1,
            setup_popup=True,
            child=self.box
        )
        self._child: KeybindsBox | None = None

        if __debug__:
            weakref.finalize(
                self, lambda: logger.debug("InfoWindow finalized")
            )

    def on_show(self) -> None:
        self._child = KeybindsBox()
        self.box.append(self._child)

    def on_hide(self) -> None:
        if self._child:
            self._child.destroy()
            self.box.remove(self._child)
        self._child = None

    def destroy(self) -> None:
        super().destroy()
