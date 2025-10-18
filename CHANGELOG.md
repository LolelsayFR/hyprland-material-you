# CHANGELOG - Fork LolelsayFR

> **🤖 Note :** Ce fork est entièrement géré par IA (GitHub Copilot) - une expérience pour tester les capacités de l'IA à modifier un projet complexe sans rien casser !

Tous les changements notables apportés à ce fork seront documentés ici.

Format basé sur [Keep a Changelog](https://keepachangelog.com/fr/1.0.0/).

---

## [Non publié] - 2025-10-18

### Ajouté
- **Intégration Deezer améliorée** 🎵
  - Chargement direct des pochettes depuis CDN Deezer (pas de cache local)
  - Icône officielle Deezer dans le player au lieu du texte
  - Mise à jour instantanée des pochettes lors des changements de piste
  - Support dans la barre et le popup player
  - Règles Hyprland (blur + opacity) pour Deezer
  - Voir [DEEZER-INTEGRATION.md](DEEZER-INTEGRATION.md)

- **Settings Keybinds refactorisé** ⌨️
  - Conversion du système d'onglets (Notebook) en 5 pages séparées
  - Nouvelle navigation dans la sidebar
  - Pages : All, By Type, Keyboard, ThinkPad, Keychron
  - Meilleure performance et expérience utilisateur
  - Voir [KEYBINDS-LAYOUT-UPDATE.md](KEYBINDS-LAYOUT-UPDATE.md)

- **Page Outside Parameters** 🔧
  - Remplacement de la page GTK Settings intégrée
  - Accès rapide aux outils de configuration externes
  - Boutons vers : GTK Settings, wdisplay, pavucontrol, EasyEffects, dconf-editor
  - Détection automatique de disponibilité
  - Respect de la philosophie originale : ne pas réinventer la roue
  - Voir [OUTSIDE-REFACTOR.md](OUTSIDE-REFACTOR.md)

### Modifié
- **Catégories Keybinds** : Fusion Workspaces → Windows
- **Compatibilité GTK4** : `load_from_string()` au lieu de `load_from_data()` pour CSS
- **Player widgets** : Détection automatique des changements de piste
- **Règles Hyprland** : Ajout support complet Deezer (4 classes)
- **Settings Architecture** : Approche plus simple et respectueuse de la vision originale

### Supprimé
- **Page GTK Settings intégrée** : Remplacée par Outside Parameters pour éviter la duplication

### Corrigé
- Pochettes d'album ne se mettant pas à jour dans Deezer
- Cache local empêchant les mises à jour d'images
- Compatibilité GTK4 pour CssProvider

### Documentation
- Ajout SESSION-SUMMARY.md : Récapitulatif complet de la session
- Ajout DEEZER-INTEGRATION.md : Documentation technique intégration Deezer
- Mise à jour KEYBINDS-LAYOUT-UPDATE.md
- Nettoyage fichiers MD obsolètes

---

## [Non publié] - 2025-10-17

### Ajouté
- **Makefile complet** pour installation et gestion système
  - Commandes: `build`, `install`, `uninstall`, `update`, `reinstall`, `reload`, `clean`, `check`, `pkg`, `dev`
  - **`make reload`** : Recompile et recharge HyprYou à chaud (session active)
  - Support compilation Cython + binaires C (hypryouctl, hypryou-start, crash-dialog)
  - Vérification automatique des dépendances avec `make check`
  - Mode développement avec `make dev`
  - Output coloré et aide formatée
  - Variables PREFIX et DESTDIR pour flexibilité
  
- **Documentation d'installation** (INSTALL.md)
  - Guide pas à pas (Makefile, makepkg, manuelle)
  - Liste exhaustive dépendances Arch/AUR
  - Documentation commandes Makefile
  - Section dépannage et mise à jour
  - Crédits et différences avec upstream
  
- **Script de test automatisé** (test-install.sh)
  - Vérifie dépendances critiques
  - Test compilation complète
  - Validation binaires générés
  - Suggestions si dépendances manquantes

### Modifié - Configuration Hyprland

#### `decoration.conf`
- **Blur renforcé** :
  - `enabled = true` (était `false`)
  - `size = 8` (était `4`)
  - `passes = 3` (maintenu)
  - `contrast = 1.1` (était `1`)
  - `vibrancy = 0.2` (était `0.3`)
  - Ajout `brightness = 1.0`
  - Ajout `ignore_opacity = true` (crucial pour layers)
  
- **Shadows optimisées** :
  - `range = 18` (était `10`)
  - `render_power = 3` (était `5`)
  - `color = rgba(0, 0, 0, 0.7)` (format RGBA moderne)

#### `windowrule.conf`
- **Règles wdisplays** (app Displays) :
  ```conf
  windowrulev2 = float, class:^(wdisplays)$
  windowrulev2 = size 900 600, class:^(wdisplays)$
  windowrulev2 = center, class:^(wdisplays)$
  windowrulev2 = stayfocused, class:^(wdisplays)$
  ```
  
- **Layer blur** pour overlays transparents :
  ```conf
  layerrule = blur, gtk-layer-shell
  layerrule = ignorealpha 0.3, gtk-layer-shell
  ```

#### `config.py` - Settings par défaut

**Apparence** :
- `opacity`: `0.85` (était `1.0`) - transparence légère
- `blur.xray`: `False` (était `True`) - blur sans effet X-ray
- `hide_empty_workspaces`: `True` (était `False`)
- `corners`: `True` (maintenu)

**Sécurité** :
- `secure_cliphist`: `True` (était `False`)

**Apps & Thèmes** :
- `apps.terminal`: `"gnome-terminal"` (était `"alacritty"`)
- `themes.kitty`: `True` (était `False`)
- `icons.dark/light`: `""` (vides, au lieu de Tela-circle-nord)

**Input & Clavier** :
- `input.kb_model`: `"pc105"` (était `""`)
- `input.kb_rules`: `"evdev"` (était `""`)
- `input.scroll_method`: `"2fg"` (était `""`)
- `input.follow_mouse`: `0` (était `1`)
- `input.mouse_refocus`: `False` (était `True`)
- `input.float_switch_override_focus`: `0` (était `1`)

**Touchpad** :
- `input.touchpad.enabled`: `True` (était `False`)
- `input.touchpad.natural_scroll`: `True` (était `False`)

**Hyprland Layout** :
- `hyprland.gaps_in`: `4` (était `5`)
- `hyprland.gaps_out`: `8` (était `12`)
- `hyprland.decoration.rounding`: `10` (était `16`)
- `hyprland.misc.vrr`: `3` (était `0`) - VRR fullscreen + always
- `hyprland.snap.enabled`: `True` (était `False`)

---

## Commits

### 2025-10-17

**[3c4d810]** ADD | Script de test d'installation automatisé
- Vérifie dépendances critiques (gcc, python, hyprland, sass)
- Test de compilation (make clean + build)
- Validation des binaires générés
- Output coloré et informatif
- Suggestions d'installation si dépendances manquantes

**[188a1cd]** ADD | Documentation d'installation complète (INSTALL.md)
- Guide pas à pas pour installation via Makefile, makepkg, manuelle
- Liste exhaustive des dépendances Arch/AUR
- Documentation des commandes Makefile
- Section dépannage et mise à jour
- Crédits et différences avec upstream

**[55edba7]** ADD | Makefile complet pour installation et gestion
- Commandes: build, install, uninstall, update, reinstall
- Support compilation Cython + binaires C (hypryouctl, etc.)
- Vérification des dépendances avec 'make check'
- Mode développement avec 'make dev'
- Couleurs et aide formatée pour meilleure UX
- Compatible makepkg et installation manuelle
- Variables PREFIX et DESTDIR pour flexibilité

**[957418c]** ADD | Enhanced blur settings with compositor integration
- Enabled and optimized blur (size=8, passes=3, vibrancy=0.2)
- Added ignore_opacity for better layer surface handling
- Improved shadow rendering (range=18, power=3)
- ADD | wdisplays window rules for proper display management
- ADD | Layer blur rules for transparent GTK overlays
- UPDATE | Default settings to match personal preferences

---

## Upstream

Ce fork est basé sur [koeqaife/hyprland-material-you](https://github.com/koeqaife/hyprland-material-you) v2.

### Synchronisation

Pour récupérer les mises à jour upstream :
```bash
git remote add upstream https://github.com/koeqaife/hyprland-material-you.git
git fetch upstream
git merge upstream/v2
```

---

## Philosophie du Fork

Ce fork vise à :
1. **Optimiser** l'expérience visuelle (blur, transparence, shadows)
2. **Simplifier** l'installation avec un Makefile moderne
3. **Documenter** exhaustivement le processus
4. **Personnaliser** les defaults selon mes préférences
5. **Maintenir** la compatibilité avec l'upstream

Les modifications restent **modulaires** et peuvent être fusionnées partiellement si nécessaire.

---

## Licence

GPL-3.0 - Voir [LICENSE](LICENSE)
