from repository import gtk
from src.services.hyprland_keybinds.common import KeyBind
from src.services.hyprland_keybinds import key_binds
from src.services.hyprland_config import keybind_overrides
from src.services.hyprland_config import KeybindOverridesRaw
import re
import typing as t
import weakref
from utils.styles import toggle_css_class
from utils.debounce import sync_debounce
from utils.ref import Ref
import src.widget as widget
from config import Settings

from src.modules.settings.base import RowTemplate
from src.modules.settings.base import Category

split_regex = re.compile(r"[,+\s]+")
REPLACEMENTS: dict[str, str] = {
    "/": "SLASH",
    "-": "MINUS",
    "+": "PLUS",
    ".": "PERIOD",
    ",": "COMMA",
    ";": "SEMICOLON",
    "`": "GRAVE",
    "=": "EQUAL",
    "[": "BRACKETLEFT",
    "]": "BRACKETRIGHT",
    "\\": "BACKSLASH",
    "'": "APOSTROPHE"
}


def normalize_key(part: str) -> str:
    part = part.strip().upper()
    return REPLACEMENTS.get(part, part)


class KeybindRow(RowTemplate):
    __gtype_name__ = "SettingsKeybindRow"

    def __init__(
        self,
        keybind: KeyBind,
        on_bind_text: t.Callable[[t.Self, list[str] | None], None],
        on_action_text: t.Callable[[t.Self, list[str] | None], None]
    ) -> None:
        self.keybind = keybind
        self._on_bind_text = weakref.WeakMethod(on_bind_text)
        self._on_action_text = weakref.WeakMethod(on_action_text)

        super().__init__(
            self.keybind.description or "Uknown",
            description=None,
            css_classes=("keybind-row",),
            clickable=False
        )
        self.hbox = gtk.Box(
            hexpand=True
        )
        self.entries_box = gtk.Box(
            css_classes=("entries-box",),
            homogeneous=True,
            hexpand=True
        )
        self.bind_entry = gtk.Entry(
            css_classes=("bind-entry",),
            placeholder_text="Keybind"
        )
        self.action_entry = gtk.Entry(
            css_classes=("action-entry",),
            placeholder_text="Action"
        )

        self.debounced_on_bind_text = sync_debounce(500)(self.on_bind_text)
        self.debounced_on_action_text = sync_debounce(500)(self.on_action_text)

        self.reset = gtk.Button(
            css_classes=("icon-tonal", "reset-button"),
            child=widget.Icon("reset_settings"),
            tooltip_text="Reset",
            valign=gtk.Align.CENTER,
            halign=gtk.Align.CENTER,
            sensitive=False
        )

        self.handlers = {
            self.bind_entry: self.bind_entry.connect(
                "notify::text", self.debounced_on_bind_text
            ),
            self.action_entry: self.action_entry.connect(
                "notify::text", self.debounced_on_action_text
            ),
            self.reset: self.reset.connect(
                "clicked", self.on_reset
            )
        }

        self.set_orientation(gtk.Orientation.VERTICAL)
        self.entries_box.append(self.bind_entry)
        self.entries_box.append(self.action_entry)
        self.hbox.append(self.entries_box)
        self.hbox.append(self.reset)
        self.append(self.hbox)
        self.update()

    def on_reset(self, *args: t.Any) -> None:
        bind = self.keybind.bind
        action = self.keybind.action

        self.bind_entry.handler_block(self.handlers[self.bind_entry])
        self.action_entry.handler_block(self.handlers[self.action_entry])
        self.bind_entry.set_text(
            " + ".join([_bind.capitalize() for _bind in bind])
        )
        self.action_entry.set_text(
            ", ".join(action)
            if isinstance(action, tuple)
            else action
        )
        self.bind_entry.handler_unblock(self.handlers[self.bind_entry])
        self.action_entry.handler_unblock(self.handlers[self.action_entry])

        _on_bind_text = self._on_bind_text()
        _on_action_text = self._on_action_text()
        if callable(_on_bind_text):
            _on_bind_text(self, None)  # type: ignore
        if callable(_on_action_text):
            _on_action_text(self, None)  # type: ignore
        self.reset.set_sensitive(False)

    def update(self) -> None:
        self.reset.set_sensitive(False)
        override = keybind_overrides.value.get(self.keybind.id)
        bind = self.keybind.bind
        action = self.keybind.action
        if override is not None:
            if override.bind:
                bind = override.bind
                self.reset.set_sensitive(True)
            if override.action:
                action = override.action
                self.reset.set_sensitive(True)

        self.bind_entry.handler_block(self.handlers[self.bind_entry])
        self.action_entry.handler_block(self.handlers[self.action_entry])
        self.bind_entry.set_text(
            " + ".join([_bind.capitalize() for _bind in bind])
        )
        self.action_entry.set_text(
            ", ".join(action)
            if isinstance(action, tuple)
            else action
        )
        self.bind_entry.handler_unblock(self.handlers[self.bind_entry])
        self.action_entry.handler_unblock(self.handlers[self.action_entry])

    def on_bind_text(self, *args: t.Any) -> None:
        callback = self._on_bind_text()
        if not callable(callback):
            return

        text = self.bind_entry.get_text()
        binds = [
            normalize_key(part)
            for part in re.split(split_regex, text)
            if part.strip()
        ]

        if len(binds) > 3:
            toggle_css_class(self.bind_entry, "incorrect", True)
            self.bind_entry.set_tooltip_text("Too many modifiers (max 3).")
        elif len(binds) < 1:
            toggle_css_class(self.bind_entry, "incorrect", True)
            self.bind_entry.set_tooltip_text("Too few modifiers (min 1).")
        else:
            toggle_css_class(self.bind_entry, "incorrect", False)
            self.bind_entry.set_tooltip_text(None)
            callback(self, binds)  # type: ignore
            self.reset.set_sensitive(True)

    def on_action_text(self, *args: t.Any) -> None:
        callback = self._on_action_text()
        if not callable(callback):
            return

        text = self.action_entry.get_text()
        binds = [
            part.strip()
            for part in text.split(",")
            if part.strip()
        ]

        if len(binds) < 1:
            toggle_css_class(self.action_entry, "incorrect", True)
            self.action_entry.set_tooltip_text("Too few modifiers (min 1).")
        else:
            toggle_css_class(self.action_entry, "incorrect", False)
            self.action_entry.set_tooltip_text(None)
            callback(self, binds)  # type: ignore
            self.reset.set_sensitive(True)

    def destroy(self) -> None:
        super().destroy()
        for button, handler in self.handlers.items():
            button.disconnect(handler)


class KeybindsPage(gtk.ScrolledWindow):
    """Page Keybinds - Tous les keybinds"""
    __gtype_name__ = "SettingsKeybindsPage"

    def __init__(self) -> None:
        self.box = gtk.Box(
            css_classes=("page-box",),
            orientation=gtk.Orientation.VERTICAL
        )
        super().__init__(
            css_classes=("keybinds-page", "settings-page",),
            child=self.box,
            hscrollbar_policy=gtk.PolicyType.NEVER,
            vexpand=True
        )
        
        self.overrides: dict[str, dict[str, list[str] | None]] = {}
        
        # Créer les rows directement
        added_categories: list[str] = []
        for keybind in key_binds:
            if not isinstance(keybind, KeyBind):
                continue
            if not keybind.description:
                continue
            category = keybind.category or "Unknown"
            if category not in added_categories:
                self.box.append(Category(category))
                added_categories.append(category)
            row = KeybindRow(keybind, self.on_bind_text, self.on_action_text)
            self.box.append(row)
        
        # Boutons Save/Cancel en bas
        self.actions_box = gtk.Box(
            css_classes=("actions-box",),
            halign=gtk.Align.END,
            margin_top=12,
            margin_bottom=12
        )
        self.save_button = gtk.Button(
            css_classes=("filled",),
            label="Save",
            sensitive=False
        )
        self.cancel_button = gtk.Button(
            css_classes=("text",),
            label="Cancel"
        )

        self.cancel_button.connect("clicked", self.on_cancel)
        self.save_button.connect("clicked", self.on_save)

        self.actions_box.append(self.cancel_button)
        self.actions_box.append(self.save_button)
        self.box.append(self.actions_box)

    def on_cancel(self, *args: t.Any) -> None:
        self.overrides.clear()
        # Parcourir tous les KeybindRow dans la box
        child = self.box.get_first_child()
        while child:
            if isinstance(child, KeybindRow):
                child.update()
            child = child.get_next_sibling()
        self.save_button.set_sensitive(False)

    def on_save(self, *args: t.Any) -> None:
        overrides: Ref[KeybindOverridesRaw] = Settings().get_ref(
            "keybinds_overrides"
        )
        _map = {
            str(item["id"]): item
            for item in overrides.value
        }
        for id, to_change in self.overrides.items():
            if id not in _map:
                _map[id] = overrides._wrap_if_mutable({    # type: ignore
                    "id": id
                })
                overrides.value.append(_map[id])

            if "bind" in to_change:
                if to_change["bind"] is None:
                    if "bind" in _map[id]:
                        del _map[id]["bind"]
                else:
                    _map[id]["bind"] = to_change["bind"]

            if "action" in to_change:
                if to_change["action"] is None:
                    if "action" in _map[id]:
                        del _map[id]["action"]
                else:
                    _map[id]["action"] = to_change["action"]

        self.overrides.clear()
        self.save_button.set_sensitive(False)

    def on_bind_text(
        self,
        row: KeybindRow,
        bind: list[str] | None
    ) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}

        self.overrides[id]["bind"] = bind
        self.save_button.set_sensitive(True)

    def on_action_text(
        self,
        row: KeybindRow,
        action: list[str] | None
    ) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}

        self.overrides[id]["action"] = action
        self.save_button.set_sensitive(True)


# Classes séparées pour chaque page de keybinds dans la sidebar

class KeybindsByTypePage(gtk.ScrolledWindow):
    """Page Keybinds organisée par type/catégorie"""
    def __init__(self):
        super().__init__(
            hscrollbar_policy=gtk.PolicyType.NEVER,
            css_classes=("settings-page",)
        )
        self.overrides: dict[str, dict[str, t.Any]] = {}
        
        self.box = gtk.Box(
            css_classes=("page-box",),
            orientation=gtk.Orientation.VERTICAL,
            spacing=0
        )
        self.set_child(self.box)
        
        # Grouper par catégorie
        categories_map: dict[str, list[KeyBind]] = {}
        for keybind in key_binds:
            if not isinstance(keybind, KeyBind) or not keybind.description:
                continue
            category = keybind.category or "Unknown"
            if category not in categories_map:
                categories_map[category] = []
            categories_map[category].append(keybind)
        
        # Afficher par catégorie
        for category, keybinds in sorted(categories_map.items()):
            self.box.append(Category(category))
            for keybind in keybinds:
                row = KeybindRow(keybind, self.on_bind_text, self.on_action_text)
                self.box.append(row)
        
        # Boutons Cancel/Save
        self.actions_box = gtk.Box(
            css_classes=("actions-box",),
            orientation=gtk.Orientation.HORIZONTAL,
            spacing=10,
            halign=gtk.Align.END,
            margin_top=10,
            margin_bottom=10,
            margin_start=10,
            margin_end=10
        )
        
        self.cancel_button = gtk.Button(
            label="Cancel",
            css_classes=("cancel-button",)
        )
        self.save_button = gtk.Button(
            label="Save",
            css_classes=("save-button",),
            sensitive=False
        )
        
        self.cancel_button.connect("clicked", self.on_cancel)
        self.save_button.connect("clicked", self.on_save)
        
        self.actions_box.append(self.cancel_button)
        self.actions_box.append(self.save_button)
        self.box.append(self.actions_box)
    
    def on_cancel(self, *args: t.Any) -> None:
        self.overrides.clear()
        child = self.box.get_first_child()
        while child:
            if isinstance(child, KeybindRow):
                child.update()
            child = child.get_next_sibling()
        self.save_button.set_sensitive(False)
    
    def on_save(self, *args: t.Any) -> None:
        overrides: Ref[KeybindOverridesRaw] = Settings().get_ref("keybinds_overrides")
        _map = {str(item["id"]): item for item in overrides.value}
        for id, to_change in self.overrides.items():
            if id not in _map:
                _map[id] = overrides._wrap_if_mutable({"id": id})  # type: ignore
                overrides.value.append(_map[id])
            if "bind" in to_change:
                if to_change["bind"] is None:
                    if "bind" in _map[id]:
                        del _map[id]["bind"]
                else:
                    _map[id]["bind"] = to_change["bind"]
            if "action" in to_change:
                if to_change["action"] is None:
                    if "action" in _map[id]:
                        del _map[id]["action"]
                else:
                    _map[id]["action"] = to_change["action"]
        self.overrides.clear()
        self.save_button.set_sensitive(False)
    
    def on_bind_text(self, row: KeybindRow, bind: list[str] | None) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}
        self.overrides[id]["bind"] = bind
        self.save_button.set_sensitive(True)
    
    def on_action_text(self, row: KeybindRow, action: list[str] | None) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}
        self.overrides[id]["action"] = action
        self.save_button.set_sensitive(True)


class KeybindsKeyboardPage(gtk.ScrolledWindow):
    """Page Keybinds clavier standard (SUPER+...)"""
    def __init__(self):
        super().__init__(
            hscrollbar_policy=gtk.PolicyType.NEVER,
            css_classes=("settings-page",)
        )
        self.overrides: dict[str, dict[str, t.Any]] = {}
        
        self.box = gtk.Box(
            css_classes=("page-box",),
            orientation=gtk.Orientation.VERTICAL,
            spacing=0
        )
        self.set_child(self.box)
        
        self.box.append(Category("Clavier Standard"))
        
        for keybind in key_binds:
            if not isinstance(keybind, KeyBind) or not keybind.description:
                continue
            # Filtrer: SUPER + non-XF86
            if len(keybind.bind) > 1 and "super" in [b.lower() for b in keybind.bind]:
                has_xf86 = any("xf86" in b.lower() for b in keybind.bind)
                if not has_xf86:
                    row = KeybindRow(keybind, self.on_bind_text, self.on_action_text)
                    self.box.append(row)
        
        # Boutons Cancel/Save
        self.actions_box = gtk.Box(
            css_classes=("actions-box",),
            orientation=gtk.Orientation.HORIZONTAL,
            spacing=10,
            halign=gtk.Align.END,
            margin_top=10,
            margin_bottom=10,
            margin_start=10,
            margin_end=10
        )
        
        self.cancel_button = gtk.Button(label="Cancel", css_classes=("cancel-button",))
        self.save_button = gtk.Button(label="Save", css_classes=("save-button",), sensitive=False)
        
        self.cancel_button.connect("clicked", self.on_cancel)
        self.save_button.connect("clicked", self.on_save)
        
        self.actions_box.append(self.cancel_button)
        self.actions_box.append(self.save_button)
        self.box.append(self.actions_box)
    
    def on_cancel(self, *args: t.Any) -> None:
        self.overrides.clear()
        child = self.box.get_first_child()
        while child:
            if isinstance(child, KeybindRow):
                child.update()
            child = child.get_next_sibling()
        self.save_button.set_sensitive(False)
    
    def on_save(self, *args: t.Any) -> None:
        overrides: Ref[KeybindOverridesRaw] = Settings().get_ref("keybinds_overrides")
        _map = {str(item["id"]): item for item in overrides.value}
        for id, to_change in self.overrides.items():
            if id not in _map:
                _map[id] = overrides._wrap_if_mutable({"id": id})  # type: ignore
                overrides.value.append(_map[id])
            if "bind" in to_change:
                if to_change["bind"] is None:
                    if "bind" in _map[id]:
                        del _map[id]["bind"]
                else:
                    _map[id]["bind"] = to_change["bind"]
            if "action" in to_change:
                if to_change["action"] is None:
                    if "action" in _map[id]:
                        del _map[id]["action"]
                else:
                    _map[id]["action"] = to_change["action"]
        self.overrides.clear()
        self.save_button.set_sensitive(False)
    
    def on_bind_text(self, row: KeybindRow, bind: list[str] | None) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}
        self.overrides[id]["bind"] = bind
        self.save_button.set_sensitive(True)
    
    def on_action_text(self, row: KeybindRow, action: list[str] | None) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}
        self.overrides[id]["action"] = action
        self.save_button.set_sensitive(True)


class KeybindsThinkPadPage(gtk.ScrolledWindow):
    """Page Keybinds ThinkPad T14 Gen 2"""
    def __init__(self):
        super().__init__(
            hscrollbar_policy=gtk.PolicyType.NEVER,
            css_classes=("settings-page",)
        )
        self.overrides: dict[str, dict[str, t.Any]] = {}
        
        self.box = gtk.Box(
            css_classes=("page-box",),
            orientation=gtk.Orientation.VERTICAL,
            spacing=0
        )
        self.set_child(self.box)
        
        self.box.append(Category("ThinkPad T14 Gen 2 Fn Keys"))
        
        thinkpad_keys = [
            "XF86AudioMute", "XF86AudioLowerVolume", "XF86AudioRaiseVolume",
            "XF86AudioMicMute", "XF86MonBrightnessDown", "XF86MonBrightnessUp",
            "XF86Display", "XF86WLAN", "XF86Tools", "XF86Search",
            "XF86LaunchA", "XF86Explorer", "XF86Calculator", "XF86Favorites"
        ]
        
        for keybind in key_binds:
            if not isinstance(keybind, KeyBind) or not keybind.description:
                continue
            for key in thinkpad_keys:
                if any(key.lower() in b.lower() for b in keybind.bind):
                    row = KeybindRow(keybind, self.on_bind_text, self.on_action_text)
                    self.box.append(row)
                    break
        
        # Boutons Cancel/Save
        self.actions_box = gtk.Box(
            css_classes=("actions-box",),
            orientation=gtk.Orientation.HORIZONTAL,
            spacing=10,
            halign=gtk.Align.END,
            margin_top=10,
            margin_bottom=10,
            margin_start=10,
            margin_end=10
        )
        
        self.cancel_button = gtk.Button(label="Cancel", css_classes=("cancel-button",))
        self.save_button = gtk.Button(label="Save", css_classes=("save-button",), sensitive=False)
        
        self.cancel_button.connect("clicked", self.on_cancel)
        self.save_button.connect("clicked", self.on_save)
        
        self.actions_box.append(self.cancel_button)
        self.actions_box.append(self.save_button)
        self.box.append(self.actions_box)
    
    def on_cancel(self, *args: t.Any) -> None:
        self.overrides.clear()
        child = self.box.get_first_child()
        while child:
            if isinstance(child, KeybindRow):
                child.update()
            child = child.get_next_sibling()
        self.save_button.set_sensitive(False)
    
    def on_save(self, *args: t.Any) -> None:
        overrides: Ref[KeybindOverridesRaw] = Settings().get_ref("keybinds_overrides")
        _map = {str(item["id"]): item for item in overrides.value}
        for id, to_change in self.overrides.items():
            if id not in _map:
                _map[id] = overrides._wrap_if_mutable({"id": id})  # type: ignore
                overrides.value.append(_map[id])
            if "bind" in to_change:
                if to_change["bind"] is None:
                    if "bind" in _map[id]:
                        del _map[id]["bind"]
                else:
                    _map[id]["bind"] = to_change["bind"]
            if "action" in to_change:
                if to_change["action"] is None:
                    if "action" in _map[id]:
                        del _map[id]["action"]
                else:
                    _map[id]["action"] = to_change["action"]
        self.overrides.clear()
        self.save_button.set_sensitive(False)
    
    def on_bind_text(self, row: KeybindRow, bind: list[str] | None) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}
        self.overrides[id]["bind"] = bind
        self.save_button.set_sensitive(True)
    
    def on_action_text(self, row: KeybindRow, action: list[str] | None) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}
        self.overrides[id]["action"] = action
        self.save_button.set_sensitive(True)


class KeybindsKeychronPage(gtk.ScrolledWindow):
    """Page Keybinds Keychron Q1 HE"""
    def __init__(self):
        super().__init__(
            hscrollbar_policy=gtk.PolicyType.NEVER,
            css_classes=("settings-page",)
        )
        self.overrides: dict[str, dict[str, t.Any]] = {}
        
        self.box = gtk.Box(
            css_classes=("page-box",),
            orientation=gtk.Orientation.VERTICAL,
            spacing=0
        )
        self.set_child(self.box)
        
        self.box.append(Category("Keychron Q1 HE Fn Keys"))
        
        keychron_keys = [
            "XF86AudioPlay", "XF86AudioPause", "XF86AudioPrev", "XF86AudioNext",
            "XF86HomePage", "XF86Mail", "XF86Go", "XF86Back", "XF86Forward",
            "XF86Refresh", "XF86Sleep", "XF86WakeUp"
        ]
        
        for keybind in key_binds:
            if not isinstance(keybind, KeyBind) or not keybind.description:
                continue
            for key in keychron_keys:
                if any(key.lower() in b.lower() for b in keybind.bind):
                    row = KeybindRow(keybind, self.on_bind_text, self.on_action_text)
                    self.box.append(row)
                    break
        
        # Boutons Cancel/Save
        self.actions_box = gtk.Box(
            css_classes=("actions-box",),
            orientation=gtk.Orientation.HORIZONTAL,
            spacing=10,
            halign=gtk.Align.END,
            margin_top=10,
            margin_bottom=10,
            margin_start=10,
            margin_end=10
        )
        
        self.cancel_button = gtk.Button(label="Cancel", css_classes=("cancel-button",))
        self.save_button = gtk.Button(label="Save", css_classes=("save-button",), sensitive=False)
        
        self.cancel_button.connect("clicked", self.on_cancel)
        self.save_button.connect("clicked", self.on_save)
        
        self.actions_box.append(self.cancel_button)
        self.actions_box.append(self.save_button)
        self.box.append(self.actions_box)
    
    def on_cancel(self, *args: t.Any) -> None:
        self.overrides.clear()
        child = self.box.get_first_child()
        while child:
            if isinstance(child, KeybindRow):
                child.update()
            child = child.get_next_sibling()
        self.save_button.set_sensitive(False)
    
    def on_save(self, *args: t.Any) -> None:
        overrides: Ref[KeybindOverridesRaw] = Settings().get_ref("keybinds_overrides")
        _map = {str(item["id"]): item for item in overrides.value}
        for id, to_change in self.overrides.items():
            if id not in _map:
                _map[id] = overrides._wrap_if_mutable({"id": id})  # type: ignore
                overrides.value.append(_map[id])
            if "bind" in to_change:
                if to_change["bind"] is None:
                    if "bind" in _map[id]:
                        del _map[id]["bind"]
                else:
                    _map[id]["bind"] = to_change["bind"]
            if "action" in to_change:
                if to_change["action"] is None:
                    if "action" in _map[id]:
                        del _map[id]["action"]
                else:
                    _map[id]["action"] = to_change["action"]
        self.overrides.clear()
        self.save_button.set_sensitive(False)
    
    def on_bind_text(self, row: KeybindRow, bind: list[str] | None) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}
        self.overrides[id]["bind"] = bind
        self.save_button.set_sensitive(True)
    
    def on_action_text(self, row: KeybindRow, action: list[str] | None) -> None:
        id = row.keybind.id
        if id not in self.overrides.keys():
            self.overrides[id] = {}
        self.overrides[id]["action"] = action
        self.save_button.set_sensitive(True)

