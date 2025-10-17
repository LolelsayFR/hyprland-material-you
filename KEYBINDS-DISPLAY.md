# 🎨 Keybinds Menu - Display amélioré (3 colonnes + icônes)

## 🎯 Améliorations

### 1. **Layout 3 colonnes**
- Ancien : 2 colonnes (max_children_per_line=2)
- Nouveau : **3 colonnes** (max_children_per_line=3, min_children_per_line=3)
- Espacement amélioré : 8px entre colonnes et lignes
- Homogénéité : `homogeneous=True` pour colonnes égales

### 2. **Icônes pour touches uniques**
Les touches Fn et XF86 (sans modifier) affichent maintenant une **icône colorée** à gauche :

#### Icônes Media
| Touche | Icône | Action |
|--------|-------|--------|
| `XF86AudioPlay` | ▶️ play_circle | Play/Pause |
| `XF86AudioPause` | ⏸️ pause_circle | Pause |
| `XF86AudioNext` | ⏭️ skip_next | Next track |
| `XF86AudioPrev` | ⏮️ skip_previous | Previous track |
| `XF86AudioStop` | ⏹️ stop_circle | Stop |
| `XF86AudioRewind` | ⏪ fast_rewind | -10s |
| `XF86AudioForward` | ⏩ fast_forward | +10s |

#### Icônes Volume/Luminosité
| Touche | Icône | Action |
|--------|-------|--------|
| `XF86AudioMute` | 🔇 volume_off | Mute audio |
| `XF86AudioLowerVolume` | 🔉 volume_down | Volume - |
| `XF86AudioRaiseVolume` | 🔊 volume_up | Volume + |
| `XF86AudioMicMute` | 🎤❌ mic_off | Mic mute |
| `XF86MonBrightnessDown` | 🔅 brightness_low | Brightness - |
| `XF86MonBrightnessUp` | 🔆 brightness_high | Brightness + |

#### Icônes ThinkPad/System
| Touche | Icône | Action |
|--------|-------|--------|
| `XF86Display` | 🖥️ monitor | Display settings |
| `XF86WLAN` | 📶 wifi | WiFi toggle |
| `XF86Bluetooth` | 🔵 bluetooth | Bluetooth |
| `XF86Tools` | ⚙️ settings | Settings |
| `XF86Keyboard` | ⌨️ keyboard | Keyboard layout |
| `XF86Favorites` | ⭐ folder_special | Favorites |
| `XF86NotificationCenter` | 🔔 notifications | Notifications |
| `XF86PickupPhone` | 📞 call | Call pickup |
| `XF86HangupPhone` | 📴 call_end | Call hangup |
| `XF86RFKill` | ✈️ airplanemode_active | Airplane mode |

#### Icônes Apps
| Touche | Icône | Action |
|--------|-------|--------|
| `XF86LaunchA` | 📱 apps | Apps menu |
| `XF86LaunchB` | 🎛️ tune | Quick settings |
| `XF86HomePage` | 🏠 home | Browser home |
| `XF86Mail` | 📧 mail | Email |
| `XF86Search` | 🔍 search | Search/Launcher |
| `XF86Explorer` | 📂 folder_open | File explorer |
| `XF86Calculator` | 🧮 calculate | Calculator |

#### Icônes Power
| Touche | Icône | Action |
|--------|-------|--------|
| `XF86Lock` | 🔒 lock | Lock screen |
| `XF86ScreenSaver` | 🔐 screen_lock_portrait | Screen saver |
| `XF86Sleep` | 😴 bedtime | Suspend |
| `XF86PowerOff` | ⚡ power_settings_new | Power menu |

### 3. **Affichage optimisé**
- **Noms courts** : Les touches XF86 affichent seulement la partie après "XF86"
  - Exemple : `XF86AudioPlay` → "Audioplay"
  - Troncature si > 12 caractères : "AudioMicMu..."
- **Icônes Material Symbols** : Filled variant (`"FILL" 1`)
- **Couleur primaire** : Les icônes utilisent `$primary` pour cohérence UI
- **Spacing amélioré** : 4px entre icône et touches

## 📁 Fichiers modifiés

### 1. `hypryou/src/modules/keybinds.py`
**Ajouts** :
- `XF86_ICONS` : Dictionnaire de 40+ icônes Material Symbols
- `KeybindWidget` : Détection touches uniques + affichage icône
- `KeybindsBox` : 3 colonnes avec `min_children_per_line=3`, `homogeneous=True`

**Logique** :
```python
# Détection touche unique
is_single_key = len(keybind.bind) == 1 or (len(keybind.bind) == 2 and keybind.bind[0] == "")

# Si icône disponible, l'afficher avant les touches
if is_single_key and single_key in XF86_ICONS:
    self.append(widget.Icon(XF86_ICONS[single_key]))
```

### 2. `hypryou-assets/scss/_keybinds.scss`
**Ajouts** :
- `.function-icon` : Style pour icônes XF86 (1.25rem, FILL 1, couleur primary)
- Ajustements : Hauteur minimale keybind (2rem), opacité description (0.9)

## 🎨 Aperçu visuel

### Avant
```
┌─────────────────────────────────┬─────────────────────────────────┐
│ [SUPER][+][F7]  - Display      │ [SUPER][SHIFT][Q]  - Close     │
│ [SUPER][+][F8]  - WiFi toggle  │ [SUPER][+][T]  - Terminal      │
└─────────────────────────────────┴─────────────────────────────────┘
```

### Après
```
┌──────────────────────────┬──────────────────────────┬──────────────────────────┐
│ 🖥️ [Display] - Settings  │ 📶 [Wlan] - WiFi toggle  │ [SUPER][SHIFT][Q] - Close│
│ ▶️ [Audioplay] - Play    │ ⏭️ [Audionext] - Next    │ [SUPER][+][T] - Terminal │
└──────────────────────────┴──────────────────────────┴──────────────────────────┘
```

## 🚀 Test

### Ouvrir le menu
```bash
# Appuyer sur SUPER + /
SUPER + /
```

### Vérifier
✅ **3 colonnes** alignées  
✅ **Icônes colorées** pour touches Fn/XF86  
✅ **Noms courts** pour touches longues  
✅ **Espacement** amélioré (8px)  
✅ **Couleur primary** pour icônes  

## 📊 Statistiques

| Métrique | Valeur |
|----------|--------|
| **Icônes ajoutées** | 40+ (XF86_ICONS) |
| **Colonnes** | 2 → **3** |
| **Espacement** | 2px → **8px** |
| **Touches uniques identifiées** | Automatique (is_single_key) |
| **Material Symbols** | FILL 1, wght 400, opsz 24 |

## 🎯 Avantages

1. **Meilleure lisibilité** : 3 colonnes = plus de keybinds visibles en même temps
2. **Reconnaissance rapide** : Icônes = identification instantanée de la fonction
3. **Cohérence UI** : Utilisation de Material Symbols comme partout dans HyprYou
4. **Optimisation espace** : Layout homogène avec espacement équilibré
5. **Accessibilité** : Icônes + texte = double information

## 🔄 Prochain commit

```bash
git add hypryou/src/modules/keybinds.py hypryou-assets/scss/_keybinds.scss
git commit -m "UPDATE | Menu keybinds: 3 colonnes + icônes touches uniques
- Layout 3 colonnes (min_children_per_line=3, homogeneous=True)
- Espacement amélioré: 8px entre colonnes/lignes
- 
- 40+ icônes Material Symbols pour touches XF86:
  * Media: play_circle, skip_next, volume_off, etc.
  * System: monitor, wifi, bluetooth, settings, etc.
  * Apps: apps, mail, search, folder_open, calculate
  * Power: lock, bedtime, power_settings_new
-
- Détection automatique touches uniques (is_single_key)
- Affichage icône à gauche du keybind
- Noms courts pour touches XF86 (après XF86)
- Style .function-icon: 1.25rem, FILL 1, couleur primary
-
- Améliore lisibilité et reconnaissance visuelle
- Documentation: KEYBINDS-DISPLAY.md"
```
