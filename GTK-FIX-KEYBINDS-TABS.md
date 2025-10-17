# 🛠️ GTK Settings Fix & Keybinds Tabs (TODO)

## ✅ Corrigé dans ce commit

### 1. **Crash onglet GTK Settings**

**Problème** : L'onglet GTK crashait HyprYou au démarrage avec un timeout.

**Causes** :
1. `SettingsDropdownRow` nécessite `items: list[DropdownItem]` et non `options: list[str]`
2. Les fonctions `get_gtk_themes()`, `get_icon_themes()`, `get_cursor_themes()`, `get_fonts()` scannaient tous les répertoires système au démarrage
3. `fc-list` (fonts) prenait trop de temps sans timeout
4. Pas de limitation sur le nombre de résultats

**Solution** :
```python
# Import DropdownItem
from src.modules.settings.base import DropdownItem

# Listes minimales par défaut (pas de scan au boot)
gtk_themes = [DropdownItem("Adwaita", "Adwaita"), DropdownItem("Adwaita-dark", "Adwaita-dark")]
icon_themes = [DropdownItem("Adwaita", "Adwaita"), DropdownItem("breeze", "breeze")]
cursor_themes = [DropdownItem("Adwaita", "Adwaita"), DropdownItem("breeze_cursors", "breeze_cursors")]
fonts = [
    DropdownItem("Sans", "Sans"),
    DropdownItem("Serif", "Serif"),
    DropdownItem("Monospace", "Monospace"),
    DropdownItem("Google Sans", "Google Sans"),
    DropdownItem("JetBrains Mono", "JetBrains Mono")
]

# Optimisations des fonctions de scan
def get_fonts():
    try:
        result = subprocess.run(
            ["fc-list", ":family", "style=Regular"],
            capture_output=True,
            text=True,
            timeout=2  # Timeout 2s
        )
        fonts = []
        seen = set()
        for line in result.stdout.split('\n')[:100]:  # Limit 100
            if line.strip() and ':' in line:
                font_name = line.split(':')[0].strip()
                if font_name not in seen:
                    seen.add(font_name)
                    fonts.append(font_name)
        return sorted(fonts)[:50]  # Max 50 fonts
    except Exception:
        return ["Sans", "Serif", "Monospace", "Google Sans", "JetBrains Mono"]
```

**Résultat** :
- ✅ L'onglet GTK ne crashe plus
- ✅ HyprYou démarre normalement
- ✅ Dropdowns fonctionnels avec valeurs par défaut

---

## 🚧 TODO: Onglets Keybinds

### Objectif
Réorganiser le menu keybinds (`SUPER + /`) avec plusieurs onglets pour meilleure navigation.

### Plan d'implémentation

#### Structure proposée

```
┌─ Keybinds Menu ──────────────────────┐
│ [Toutes] [Par Type] [Clavier] [Fn]  │  ← Onglets
├──────────────────────────────────────┤
│                                      │
│  Contenu selon onglet sélectionné   │
│                                      │
└──────────────────────────────────────┘
```

#### Onglets prévus

1. **Toutes** : Layout actuel (Grid 3 colonnes avec MISC à droite)
2. **Par Type** : Organisation par catégories (Actions, Tools, Apps, Windows, Workspaces, Misc)
3. **Clavier** : Uniquement keybinds avec SUPER (clavier standard)
4. **ThinkPad** : Touches Fn ThinkPad (F7, F8, F10, etc.)
5. **Keychron** : Touches media Keychron (Play, Volume, Brightness, etc.)

#### Code préparé (désactivé pour l'instant)

```python
class KeybindsNotebook(gtk.Notebook):
    """Notebook avec onglets pour organiser les keybinds"""
    
    def __init__(self) -> None:
        super().__init__(css_classes=("keybinds-notebook",))
        
        self.pages = {
            "Toutes": self._create_all_page(),
            "Par Type": self._create_by_type_page(),
            "Clavier": self._create_keyboard_page(),
            "ThinkPad": self._create_thinkpad_page(),
            "Keychron": self._create_keychron_page(),
        }
        
        for label, page in self.pages.items():
            tab_label = gtk.Label(label=label)
            self.append_page(page, tab_label)
```

#### Problème rencontré

Lors de l'implémentation, `KeybindsNotebook` causait un crash similaire au GTK Settings :
- Création de multiples pages au `__init__`
- Chaque page scanne tous les keybinds
- Timeout au démarrage

#### Solution à implémenter

**Chargement lazy des pages** :
```python
def _create_page_on_demand(self, page_name: str) -> gtk.Widget:
    """Créer la page seulement quand l'onglet est activé"""
    if page_name not in self._loaded_pages:
        if page_name == "ThinkPad":
            self._loaded_pages[page_name] = self._create_thinkpad_page()
        # etc.
    return self._loaded_pages[page_name]
```

**Signal `switch-page`** :
```python
self.connect("switch-page", self._on_page_switched)

def _on_page_switched(self, notebook, page, page_num):
    # Charger la page si pas encore chargée
    ...
```

---

## 📝 Prochaines étapes

### Court terme
- [ ] Implémenter chargement lazy pour KeybindsNotebook
- [ ] Tester avec création pages à la demande
- [ ] Valider performance (pas de timeout)

### Moyen terme
- [ ] Ajouter filtres avancés (par modifier, par application, etc.)
- [ ] Recherche keybinds (barre de recherche en haut)
- [ ] Export keybinds en PDF/Markdown

### Long terme
- [ ] Éditeur de keybinds intégré
- [ ] Détection conflits keybinds
- [ ] Suggestions keybinds libres

---

## 🔧 Pour l'activer plus tard

### 1. Dans `keybinds.py`
```python
# Remplacer KeybindsBox par KeybindsNotebook dans KeybindsWindow
self._child: KeybindsNotebook | None = None

def on_show(self) -> None:
    self._child = KeybindsNotebook()
    self.box.append(self._child)
```

### 2. Ajouter styles dans `_keybinds.scss`
```scss
.keybinds-notebook {
    notebook > header {
        background-color: $surfaceContainer;
        
        tabs tab {
            &:checked {
                background-color: $primary;
                color: $onPrimary;
            }
        }
    }
}
```

### 3. Tester
```bash
SUPER + /  # Ouvrir menu
# Vérifier onglets cliquables
# Vérifier contenu de chaque onglet
```

---

## 📊 État actuel

| Fonctionnalité | État | Notes |
|----------------|------|-------|
| **GTK Settings** | ✅ Fonctionnel | Dropdowns fixes, pas de crash |
| **Keybinds 3 colonnes** | ✅ Fonctionnel | Layout Grid avec MISC à droite |
| **Icônes XF86** | ✅ Fonctionnel | 40+ icônes Material Symbols |
| **Onglets Keybinds** | 🚧 TODO | Code préparé, implémentation lazy requise |

---

## 🎯 Commit suivant suggéré

```bash
git commit -m "ADD | Onglets keybinds avec chargement lazy
- KeybindsNotebook avec 5 onglets (Toutes, Par Type, Clavier, ThinkPad, Keychron)
- Chargement lazy des pages (switch-page signal)
- Filtrage automatique par type de touche
- Styles notebook avec onglets Material You
-
- Performance optimisée (pas de crash au démarrage)
- Navigation fluide entre onglets
- Documentation: KEYBINDS-TABS.md"
```
