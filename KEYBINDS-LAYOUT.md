# 🎨 Keybinds Menu - Layout Grid Personnalisé

## 🎯 Nouveau Layout

Le menu keybinds (`SUPER + /`) utilise maintenant un **layout Grid personnalisé** avec **MISC occupant toute la colonne de droite** sur 2 lignes.

### Disposition visuelle

```
┌─────────────┬─────────────┬─────────────────┐
│   ACTIONS   │    TOOLS    │                 │  ← Row 0
│  (action_key│   (build)   │      MISC       │
│    + keybinds)             │  (construction) │
├─────────────┼─────────────┤   + keybinds    │  ← MISC: 2 lignes (rowspan=2)
│   WINDOWS   │  WORKSPACES │                 │  ← Row 1
│(select_window│(overview_key│                 │
│  + keybinds) │  + keybinds)│                 │
├─────────────┴─────────────┤─────────────────┤
│           APPS             │                 │  ← Row 2
│          (apps)            │                 │
│        + keybinds          │                 │
└────────────────────────────┴─────────────────┘
```

### Avantages

1. **MISC bien visible** : Colonne entière = plus d'espace pour les keybinds Fn (40+)
2. **Organisation logique** :
   - **Colonne gauche** : Actions, Windows
   - **Colonne centre** : Tools, Workspaces
   - **Colonne droite** : MISC (touches Fn/XF86)
3. **APPS en bas** : Prend 2 colonnes pour plus d'espace
4. **Layout adaptatif** : Chaque catégorie peut grandir selon son contenu

## 🔧 Implémentation

### 1. Passage de FlowBox à Grid

**Avant** :
```python
class KeybindsBox(gtk.FlowBox):
    max_children_per_line=3
    # Layout automatique
```

**Après** :
```python
class KeybindsBox(gtk.Grid):
    # Layout manuel avec attach()
    # Contrôle précis de la position et taille
```

### 2. Positionnement Grid

```python
# Row 0: ACTIONS, TOOLS, MISC (début)
self.attach(self.boxes[Category.ACTIONS], 0, 0, 1, 1)   # col=0, row=0, width=1, height=1
self.attach(self.boxes[Category.TOOLS], 1, 0, 1, 1)     # col=1, row=0, width=1, height=1
self.attach(self.boxes[Category.MISC], 2, 0, 1, 2)      # col=2, row=0, width=1, height=2 ← 2 lignes!

# Row 1: WINDOWS, WORKSPACES (MISC continue)
self.attach(self.boxes[Category.WINDOWS], 0, 1, 1, 1)    # col=0, row=1
self.attach(self.boxes[Category.WORKSPACES], 1, 1, 1, 1) # col=1, row=1

# Row 2: APPS (prend 2 colonnes)
self.attach(self.boxes[Category.APPS], 0, 2, 2, 1)       # col=0, row=2, width=2, height=1
```

### 3. Paramètres Grid

```python
gtk.Grid(
    row_spacing=8,          # Espacement vertical
    column_spacing=8,       # Espacement horizontal
    column_homogeneous=False,  # Colonnes non uniformes
    row_homogeneous=False,     # Lignes non uniformes
    hexpand=True,
    vexpand=True
)
```

## 📊 Répartition des catégories

| Catégorie | Position | Taille | Icône | Keybinds typiques |
|-----------|----------|--------|-------|-------------------|
| **ACTIONS** | (0,0) | 1x1 | action_key | SUPER+Q, SUPER+F, etc. |
| **TOOLS** | (1,0) | 1x1 | build | SUPER+/, SUPER+P, etc. |
| **MISC** | (2,0) | **1x2** | construction | **40+ Fn keys** (XF86) |
| **WINDOWS** | (0,1) | 1x1 | select_window | SUPER+Arrow, SUPER+J/K/L/M |
| **WORKSPACES** | (1,1) | 1x1 | overview_key | SUPER+1-9, SUPER+Tab |
| **APPS** | (0,2) | 2x1 | apps | SUPER+T, SUPER+B, SUPER+E |

## 🎨 Styles CSS

### Fenêtre principale
```scss
window.keybinds {
    min-width: 70rem;  // Augmenté pour 3 colonnes + MISC large
}
```

### Category boxes
```scss
.category-box {
    min-width: 20rem;  // Largeur minimale par colonne
    // MISC aura automatiquement la hauteur de 2 boxes
}
```

## 🚀 Test

### Ouvrir le menu
```bash
SUPER + /
```

### Vérifier le layout
✅ **MISC** occupe toute la colonne de droite sur 2 lignes  
✅ **WINDOWS** et **WORKSPACES** côte à côte (row 1)  
✅ **ACTIONS** et **TOOLS** en haut (row 0)  
✅ **APPS** en bas sur 2 colonnes (row 2)  
✅ **Espacement** uniforme (8px)  
✅ **Icônes + keybinds** bien visibles  

## 📈 Avant/Après

### Avant (FlowBox 3 colonnes)
```
┌─────┬─────┬─────┐
│  A  │  T  │  M  │  ← 3 colonnes uniformes
├─────┼─────┼─────┤
│  W  │  WS │  AP │  ← MISC petit, dispersé
└─────┴─────┴─────┘
```

### Après (Grid personnalisé)
```
┌─────┬─────┬───────┐
│  A  │  T  │   M   │  ← MISC commence (2 lignes)
├─────┼─────┤   I   │
│  W  │  WS │   S   │  ← MISC continue
├─────┴─────┤   C   │
│    AP     │       │  ← APPS large, MISC termine
└───────────┴───────┘
```

**Avantage** : MISC (40+ keybinds Fn) a **2x plus d'espace** !

## 🎯 Cas d'usage parfait

### Touches Fn nombreuses (ThinkPad + Keychron)
Avec 40+ keybinds dans MISC :
- 🎮 Media controls (7 keybinds)
- 🔊 Volume/Brightness (6 keybinds)
- 🖥️ ThinkPad Fn keys (10+ keybinds)
- ⌨️ Keychron function keys (10+ keybinds)
- ⚡ Power/System (7 keybinds)

→ **MISC a maintenant la place pour tout afficher confortablement !**

## 📁 Fichiers modifiés

1. ✅ `hypryou/src/modules/keybinds.py`
   - `KeybindsBox` : `gtk.FlowBox` → `gtk.Grid`
   - Layout manuel avec `attach()`
   - Rowspan=2 pour MISC
   - Colspan=2 pour APPS

2. ✅ `hypryou-assets/scss/_keybinds.scss`
   - `min-width: 60rem` → `70rem` (plus large)
   - `min-width: 20rem` pour category-box
   - Grid adaptatif

## 🔄 Prochain commit

```bash
git add -A
git commit -m "UPDATE | Layout Grid personnalisé: MISC colonne entière (2 lignes)
- Passage gtk.FlowBox → gtk.Grid pour contrôle précis
- MISC occupe colonne droite entière (rowspan=2)
- Layout: Actions/Tools (row 0), Windows/Workspaces (row 1), Apps (row 2)
- 
- Grid.attach() positions:
  * ACTIONS: (0,0, 1x1)
  * TOOLS: (1,0, 1x1)  
  * MISC: (2,0, 1x2) ← 2 lignes!
  * WINDOWS: (0,1, 1x1)
  * WORKSPACES: (1,1, 1x1)
  * APPS: (0,2, 2x1) ← 2 colonnes
-
- Avantage: MISC (40+ keybinds Fn) a 2x plus d'espace
- Fenêtre élargie: 60rem → 70rem
- Documentation: KEYBINDS-LAYOUT.md"
```
