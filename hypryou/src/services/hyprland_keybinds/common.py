from dataclasses import dataclass
from enum import Enum
import json
import subprocess

main_mod = "SUPER"


class Category(str, Enum):
    ACTIONS = "Actions"
    TOOLS = "Tools"
    APPS = "Applications"
    WINDOWS = "Windows"
    WORKSPACES = "Workspaces"
    MISC = "Misc"


@dataclass
class KeyBind:
    bind: tuple[str, ...]
    action: tuple[str, ...] | str
    description: str | None = None
    category: Category | None = None

    @property
    def id(self) -> str:
        return "_".join(self.bind)


@dataclass
class KeyBindOverride:
    id: str
    bind: tuple[str, ...] | None
    action: tuple[str, ...] | str | None


@dataclass
class KeyBindHint:
    bind: tuple[str, ...]
    description: str | None = None
    category: Category | None = None


def get_hyprland_keybinds() -> dict[str, dict]:
    """
    Récupère les keybinds actuels depuis Hyprland via hyprctl.
    Retourne un dict avec la clé = 'modmask_key', valeur = {'dispatcher': ..., 'arg': ...}
    """
    try:
        result = subprocess.run(
            ["hyprctl", "binds", "-j"],
            capture_output=True,
            text=True,
            timeout=2
        )
        if result.returncode == 0:
            binds = json.loads(result.stdout)
            keybind_map = {}
            for bind in binds:
                modmask = bind.get("modmask", 0)
                key = bind.get("key", "").lower()
                dispatcher = bind.get("dispatcher", "")
                arg = bind.get("arg", "")
                
                # Convertir modmask en liste de mods
                mods = []
                if modmask & 64:  # SUPER
                    mods.append("SUPER")
                if modmask & 1:   # SHIFT
                    mods.append("SHIFT")
                if modmask & 4:   # CTRL
                    mods.append("CTRL")
                if modmask & 8:   # ALT
                    mods.append("ALT")
                
                # Créer la clé unique
                bind_key = "_".join(mods + [key.upper()])
                keybind_map[bind_key] = {
                    "dispatcher": dispatcher,
                    "arg": arg
                }
            return keybind_map
    except Exception as e:
        print(f"Erreur lors de la récupération des keybinds: {e}")
    return {}


def sync_keybind_with_hyprland(keybind: KeyBind) -> KeyBind:
    """
    Synchronise un KeyBind avec la configuration réelle de Hyprland.
    Si le bind a changé dans Hyprland, met à jour l'objet KeyBind.
    """
    hypr_binds = get_hyprland_keybinds()
    bind_id = keybind.id
    
    if bind_id in hypr_binds:
        hypr_info = hypr_binds[bind_id]
        # Le bind existe toujours, vérifier si l'action a changé
        action = keybind.action
        if isinstance(action, tuple) and len(action) >= 2:
            expected_dispatcher = action[0]
            expected_arg = action[1] if len(action) > 1 else ""
            
            # Mettre à jour si différent
            if hypr_info["dispatcher"] != expected_dispatcher or hypr_info["arg"] != expected_arg:
                keybind.action = (hypr_info["dispatcher"], hypr_info["arg"])
    
    return keybind

