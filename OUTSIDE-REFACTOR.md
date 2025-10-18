# Refactorisation Settings - Outside Parameters

## Résumé
Remplacement de la page "GTK Settings" intégrée par une page "Outside Parameters" qui fournit un accès rapide aux outils de configuration externes, respectant mieux la philosophie de l'auteur original de garder HyprYou simple et léger.

## Philosophie

L'auteur original de HyprYou privilégie une approche minimaliste : **HyprYou ne devrait pas réinventer la roue** pour des fonctionnalités déjà bien implémentées dans des outils dédiés. Au lieu de dupliquer des interfaces de configuration complètes dans HyprYou, il est préférable de :

1. ✅ Fournir un accès rapide aux outils existants
2. ✅ Laisser les outils spécialisés gérer leur domaine
3. ✅ Garder HyprYou léger et maintenable
4. ✅ Éviter les conflits de configuration

## Changements

### Supprimé
- ❌ Page "GTK Settings" intégrée avec dropdowns et sélecteurs
  - Trop complexe à maintenir
  - Risques de conflits avec les outils système
  - Duplication de fonctionnalités existantes

### Ajouté
- ✅ Page "Outside Parameters" avec accès aux outils externes
  - Boutons de lancement vers les outils spécialisés
  - Détection automatique de disponibilité
  - Descriptions claires de chaque outil
  - Organisation par catégories

## Structure de la page Outside

### 1. GTK Configuration
- **GTK Settings (GNOME Control Center)** - Configuration complète GTK
- **LXAppearance** - Alternative légère pour les thèmes

### 2. Display Configuration  
- **wdisplay** - Gestionnaire d'écrans Wayland
- **Hyprland Monitors** - Édition directe du fichier de config

### 3. Audio & Video
- **PulseAudio Volume Control (pavucontrol)** - Contrôle audio avancé
- **EasyEffects** - Effets audio professionnels

### 4. System Tools
- **dconf Editor** - Éditeur de configuration bas niveau

## Fichiers créés

### Code Python
**`hypryou/src/modules/settings/outside.py`**
- `OutsideToolButton` : Widget pour chaque outil externe
  - Icône + titre + description
  - Bouton de lancement
  - Vérification de disponibilité
- `OutsidePage` : Page principale avec sections organisées

### Styling
**`hypryou-assets/scss/_outside.scss`**
- Style Material Design 3
- Animations au hover
- États disabled pour outils non installés
- Sections organisées visuellement

### Configuration
**`hypryou/src/modules/settings/window.py`**
- Remplacement de `GTKPage` par `OutsidePage`
- Déplacement dans la sidebar (après Keybinds, avant Info)
- Icône : `open_in_new`

## Avantages de cette approche

### 🎯 Simplicité
- Pas de code de configuration complexe à maintenir
- Pas de risque de conflit avec les outils système
- Code plus léger et plus rapide

### 🔧 Flexibilité
- L'utilisateur choisit son outil préféré
- Accès direct aux fonctionnalités complètes
- Pas de limitations imposées par HyprYou

### 🚀 Performance
- Pas de scan des thèmes/icônes au démarrage
- Pas de timeout ou ralentissement
- Chargement instantané de la page

### 📦 Maintenabilité
- Moins de dépendances à gérer
- Pas de code UI complexe pour les dropdowns
- Évolution indépendante des outils

## Outils recommandés à installer

```bash
# GTK Configuration
sudo pacman -S gnome-control-center  # ou
sudo pacman -S lxappearance

# Display Management
yay -S wdisplay

# Audio
sudo pacman -S pavucontrol
sudo pacman -S easyeffects

# System
sudo pacman -S dconf-editor
```

## Utilisation

1. Ouvrir Settings (Super+,)
2. Naviguer vers "Outside" dans la sidebar
3. Cliquer sur le bouton de l'outil désiré
4. L'outil s'ouvre dans une nouvelle fenêtre

**Note :** Les outils non installés apparaissent grisés avec la mention "(non installé)"

## Extensibilité

Il est facile d'ajouter de nouveaux outils dans `outside.py` :

```python
# Exemple : ajouter un nouvel outil
new_tool_button = OutsideToolButton(
    title="Mon Outil",
    description="Description de l'outil",
    icon="icon_name",
    command="command-to-run",
    check_command="command"  # optionnel
)
section.append(new_tool_button)
```

## Comparaison Avant/Après

### Avant (GTK Settings intégré)
- ❌ 300+ lignes de code Python
- ❌ Dropdowns complexes
- ❌ Scans de thèmes au démarrage (timeouts)
- ❌ Risques de conflits
- ❌ Fonctionnalités limitées

### Après (Outside Parameters)
- ✅ ~280 lignes de code simple
- ✅ Boutons de lancement
- ✅ Pas de scan au démarrage
- ✅ Outils natifs complets
- ✅ Toutes les fonctionnalités disponibles

## Vision de l'auteur

Cette refactorisation respecte la philosophie de l'auteur original :

> **"Do one thing and do it well"**  
> HyprYou se concentre sur l'interface Wayland/Hyprland,  
> les outils spécialisés gèrent leur domaine d'expertise.

## Tests

✅ Page Outside s'affiche correctement  
✅ Boutons fonctionnels pour les outils installés  
✅ Détection de disponibilité correcte  
✅ Lancement des outils externes OK  
✅ Style Material Design cohérent  
✅ Pas d'erreur au démarrage  
✅ Performance améliorée

## Version
- Date : 18 octobre 2025
- Branche : v2
- Commit : À venir

---

**🎯 Objectif atteint :** Interface simplifiée et respectueuse de la vision originale, tout en offrant un accès rapide aux outils de configuration externes.
