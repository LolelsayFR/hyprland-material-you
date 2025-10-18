# Réorganisation du menu d'aide aux Keybinds - 18 octobre 2025

## Changement demandé

Fusionner les catégories **Workspaces** et **Windows** pour libérer de la place pour la catégorie **Applications**.

## Ancienne disposition

```
┌─────────┬────────────┬─────────────┐
│ ACTIONS │   TOOLS    │    MISC     │
├─────────┼────────────┤  (2 lignes) │
│ WINDOWS │ WORKSPACES │             │
├─────────┴────────────┼─────────────┤
│       APPS           │             │
└──────────────────────┴─────────────┘
```

**Problème** : APPS était relégué en bas et prenait 2 colonnes, donnant trop d'importance aux Workspaces.

## Nouvelle disposition

```
┌─────────┬─────────┬─────────────┐
│ ACTIONS │  TOOLS  │    MISC     │
├─────────┼─────────┤  (2 lignes) │
│ WINDOWS │  APPS   │             │
│  + WS   │         │             │
└─────────┴─────────┴─────────────┘
```

**Avantages** :
- ✅ APPS a maintenant une position équivalente aux autres catégories (row 1)
- ✅ WINDOWS et WORKSPACES fusionnés logiquement (gestion des fenêtres et espaces de travail)
- ✅ Layout plus équilibré visuellement
- ✅ Meilleure lisibilité avec moins de catégories

## Modifications techniques

### 1. Dictionnaire CATEGORIES
**Fichier** : `hypryou/src/modules/keybinds.py`

**Avant** :
```python
CATEGORIES = {
    Category.ACTIONS: "action_key",
    Category.TOOLS: "build",
    Category.APPS: "apps",
    Category.WINDOWS: "select_window",
    Category.WORKSPACES: "overview_key",
    Category.MISC: "construction"
}
```

**Après** :
```python
CATEGORIES = {
    Category.ACTIONS: "action_key",
    Category.TOOLS: "build",
    Category.APPS: "apps",
    Category.WINDOWS: "select_window",  # Fusionné avec Workspaces
    Category.MISC: "construction"
}

# Catégories fusionnées : Windows inclut maintenant Workspaces
MERGED_CATEGORIES = {
    Category.WINDOWS: [Category.WINDOWS, Category.WORKSPACES]
}
```

### 2. Layout Grid (KeybindsBox)

**Changements** :
- Suppression de `Category.WORKSPACES` de l'attach
- `Category.APPS` déplacé de row 2 (colspan 2) vers row 1, col 1
- Label WINDOWS changé en "Windows & Workspaces"

**Code** :
```python
# Row 0: ACTIONS, TOOLS, MISC
self.attach(self.boxes[Category.ACTIONS], 0, 0, 1, 1)
self.attach(self.boxes[Category.TOOLS], 1, 0, 1, 1)
self.attach(self.boxes[Category.MISC], 2, 0, 1, 2)  # MISC: 2 lignes

# Row 1: WINDOWS (fusionné avec WORKSPACES), APPS
self.attach(self.boxes[Category.WINDOWS], 0, 1, 1, 1)
self.attach(self.boxes[Category.APPS], 1, 1, 1, 1)

# Remplir avec fusion WORKSPACES → WINDOWS
for keybind in key_binds:
    if keybind.category == Category.WORKSPACES:
        self.boxes[Category.WINDOWS].append(_widget)
    else:
        self.boxes[keybind.category].append(_widget)
```

### 3. Label dynamique

**Dans KeybindsBox** :
```python
# Label spécial pour WINDOWS (fusionné avec Workspaces)
label_text = "Windows & Workspaces" if category == Category.WINDOWS else category
label = gtk.Label(label=label_text, ...)
```

**Dans KeybindsNotebook._create_category_section** :
```python
# Même logique pour l'onglet "Par Type"
label_text = "Windows & Workspaces" if category == Category.WINDOWS else category
```

### 4. Fusion des keybinds

**Dans _create_category_section** :
```python
for keybind in key_binds:
    # Fusionner WORKSPACES dans WINDOWS
    keybind_category = keybind.category
    if keybind_category == Category.WORKSPACES:
        keybind_category = Category.WINDOWS
    
    if keybind_category == category and keybind.description:
        synced = sync_keybind_with_hyprland(keybind)
        box.append(KeybindWidget(synced))
```

## Comportement

### Menu principal (SUPER+/)
- Affiche maintenant "Windows & Workspaces" au lieu de deux catégories séparées
- Tous les keybinds de gestion de fenêtres ET d'espaces de travail sont regroupés
- APPS est visible dès row 1 avec même importance que les autres

### Onglet "Par Type" (KeybindsNotebook)
- Même logique de fusion appliquée
- Section "Windows & Workspaces" contient :
  - SUPER+Q : Fermer fenêtre
  - SUPER+1-9 : Changer d'espace de travail
  - SUPER+SHIFT+1-9 : Déplacer vers espace
  - SUPER+←↑→↓ : Navigation fenêtres
  - etc.

### Onglets Settings > Keybinds
- Pas de changement (filtrage par type de périphérique)
- Toujours : Toutes, Par Type, Clavier, ThinkPad, Keychron

## Tests

```bash
# Compilation
python -m py_compile hypryou/src/modules/keybinds.py

# Rechargement
make reload

# Vérification visuelle
# Ouvrir SUPER+/ → Vérifier layout et label "Windows & Workspaces"
# Naviguer dans les onglets → Vérifier fusion des keybinds
```

## Impact utilisateur

### Positif ✅
- Interface plus claire avec 5 catégories au lieu de 6
- APPS plus visible et accessible
- Logique de regroupement Windows/Workspaces (même domaine)
- Moins de scrolling nécessaire dans la catégorie Windows

### Neutre ⚪
- Pas de perte de fonctionnalité
- Tous les keybinds restent accessibles
- Même navigation dans les onglets

## Fichiers modifiés

- `hypryou/src/modules/keybinds.py` (4 fonctions modifiées)
  - CATEGORIES dict (ligne ~75)
  - KeybindsBox.__init__() (layout + fusion)
  - KeybindsBox label creation (label dynamique)
  - KeybindsNotebook._create_category_section() (fusion + label)

## Commit

```bash
git add hypryou/src/modules/keybinds.py
git commit -m "UX | Fusionner Workspaces dans Windows pour promouvoir Applications

- Windows & Workspaces fusionnés (logique similaire)
- Applications déplacé en row 1 (meilleure visibilité)
- Layout 3x2 plus équilibré
- Label dynamique 'Windows & Workspaces'
- Fusion appliquée dans KeybindsBox et KeybindsNotebook"
```

## Prochaines améliorations

1. **Sous-sections** : Séparer Windows et Workspaces avec des séparateurs visuels dans la même box
2. **Icônes doubles** : Afficher deux icônes (window + workspace) pour le label fusionné
3. **Statistiques** : Afficher le nombre de keybinds par catégorie dans le label
4. **Recherche** : Filtrer par catégorie avec recherche textuelle
