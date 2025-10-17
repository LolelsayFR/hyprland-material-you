# HyprYou Fork - Keybinds & GTK Settings Update

## 🎯 Nouvelles fonctionnalités

### 1. 🎮 Keybinds enrichis

#### ThinkPad T14 Gen 2
Toutes les touches Fn du ThinkPad T14 Gen 2 sont maintenant prises en charge :

| Touche | Action | Description |
|--------|--------|-------------|
| **Fn+F4** | `XF86AudioMicMute` | Mute/unmute microphone |
| **Fn+F7** | `XF86Display` | Display settings (wdisplays) |
| **Fn+F8** | `XF86WLAN` | WiFi toggle (nm-connection-editor) |
| **Fn+F9** | `XF86Tools` | Settings menu |
| **Fn+F10** | `XF86Bluetooth` | Bluetooth manager |
| **Fn+F11** | `XF86Keyboard` | Keyboard layout toggle |
| **Fn+F12** | `XF86Favorites` | File manager (Thunar) |

**Touches additionnelles :**
- `XF86NotificationCenter` - Notification center (Fn+N)
- `XF86PickupPhone` - Pickup call (Fn+P)
- `XF86HangupPhone` - Hangup call (Fn+H)
- `XF86RFKill` - Airplane mode (Fn+F8 long press)

#### Keychron Q1 HE
Support complet des touches multimédia du Keychron Q1 HE :

| Touche | Action | Description |
|--------|--------|-------------|
| **Media** | `XF86AudioMute` | Mute audio |
| **Vol-** | `XF86AudioLowerVolume` | Volume down (-5%) |
| **Vol+** | `XF86AudioRaiseVolume` | Volume up (+5%) |
| **Bright-** | `XF86MonBrightnessDown` | Brightness down (-10%) |
| **Bright+** | `XF86MonBrightnessUp` | Brightness up (+10%) |
| **Play/Pause** | `XF86AudioPlay` | Toggle play/pause |
| **Next** | `XF86AudioNext` | Next track |
| **Prev** | `XF86AudioPrev` | Previous track |
| **Stop** | `XF86AudioStop` | Stop media |

**Touches fonction additionnelles :**
- `XF86LaunchA` - Apps menu (Fn+A)
- `XF86LaunchB` - Quick settings (Fn+B)
- `XF86HomePage` - Web browser (Firefox)
- `XF86Mail` - Email client (Thunderbird)
- `XF86Search` - Launcher
- `XF86Explorer` - File explorer
- `XF86Calculator` - Calculator

#### Contrôles média avancés
- `XF86AudioRewind` - Rewind 10 secondes
- `XF86AudioForward` - Forward 10 secondes

#### Contrôles système
- `XF86Lock` - Lock screen
- `XF86ScreenSaver` - Screen saver
- `XF86Sleep` - Suspend system
- `XF86PowerOff` - Power menu

### 2. 🖱️ Focus automatique sur scroll

**Nouvelle fonctionnalité :** La fenêtre sous le curseur prend automatiquement le focus lors d'un scroll avec la molette.

```conf
# Dans keybindings.conf
bind = , mouse_down, focuswindow, mouse
bind = , mouse_up, focuswindow, mouse
```

**Avantage :** Plus besoin de cliquer pour donner le focus avant de scroller !

### 3. 🎨 Nouvel onglet GTK Settings

Un nouvel onglet complet de configuration GTK a été ajouté au menu Settings.

#### Catégories disponibles :

##### 🎨 GTK Theme
- **GTK Theme** : Choix du thème GTK3/4
- **Prefer Dark Theme** : Forcer le variant dark

##### 🖼️ Icons
- **Icon Theme** : Choix du thème d'icônes
- **Enable Icon Fallback** : Fallback automatique

##### 🖱️ Cursor
- **Cursor Theme** : Thème de curseur
- **Cursor Size** : Taille (16-48px)

##### 🔤 Fonts
- **Interface Font** : Police par défaut (Google Sans)
- **Font Size** : Taille (8-16pt)
- **Monospace Font** : Police monospace (JetBrains Mono)

##### ⚙️ Behavior
- **Enable Animations** : Animations GTK
- **Enable Overlay Scrollbars** : Scrollbars overlay
- **Double Click Time** : Temps max entre clics (ms)
- **Show Hidden Files** : Fichiers cachés dans dialogs

##### 🔧 Advanced
- **Enable CSD** : Client-Side Decorations
- **Enable Mnemonics** : Raccourcis clavier soulignés
- **DPI Scale** : Facteur d'échelle (1.0 = 96 DPI)

#### Valeurs par défaut (config.py)
```python
"gtk.theme": "Adwaita",
"gtk.prefer_dark_theme": True,
"gtk.icon_theme": "Adwaita",
"gtk.cursor_theme": "Adwaita",
"gtk.cursor_size": 24,
"gtk.font": "Google Sans",
"gtk.font_size": 11,
"gtk.monospace_font": "JetBrains Mono",
# ... etc
```

## 📁 Fichiers modifiés

### Keybinds
- `hypryou/src/services/hyprland_keybinds/fn_keys.py` - 40+ nouveaux keybinds
- `hypryou-assets/configs/hyprland/keybindings.conf` - Focus on scroll

### GTK Settings
- `hypryou/src/modules/settings/gtk.py` - **NOUVEAU** (200+ lignes)
- `hypryou/src/modules/settings/window.py` - Intégration de la page GTK
- `hypryou/config.py` - 15+ defaults GTK

## 🚀 Utilisation

### Tester les keybinds
```bash
# Voir tous les keybinds dans le menu
SUPER + /

# Tester une touche Fn directement
Fn+F7  # Display settings
Fn+F8  # WiFi
Fn+F10 # Bluetooth
```

### Accéder aux settings GTK
1. Ouvrir Settings (`SUPER + I` ou waybar)
2. Cliquer sur **GTK** dans la sidebar
3. Configurer thèmes, icônes, polices, etc.

### Focus automatique
1. Placez le curseur sur une fenêtre
2. Scrollez avec la molette
3. → La fenêtre prend automatiquement le focus !

## 📊 Statistiques

- **Keybinds ajoutés** : 40+ (ThinkPad + Keychron + System)
- **Settings GTK** : 18 paramètres configurables
- **Lignes ajoutées** : 350+ lignes
- **Fichiers créés** : 2 (gtk.py, KEYBINDS.md)
- **Fichiers modifiés** : 4

## 🔄 Commit

```bash
git add -A
git commit -m "ADD | Keybinds ThinkPad T14 + Keychron Q1 HE + GTK Settings
- 40+ keybinds: ThinkPad T14 Gen 2 (Fn+F4-F12, N, P, H)
- Keychron Q1 HE: media controls, function keys
- Focus window automatique sur scroll (mouse_up/down)
- 
- Nouvel onglet GTK Settings:
  * Theme, Icons, Cursor configuration
  * Font management (interface + monospace)
  * Behavior: animations, scrollbars, double-click
  * Advanced: CSD, mnemonics, DPI scale
  * 18 paramètres avec defaults optimisés
-
- Auto-detection themes/icons/fonts système
- Integration complète dans Settings sidebar"
```

## 🎉 Résultat

Le fork HyprYou dispose maintenant de :
- ✅ Support complet ThinkPad T14 Gen 2
- ✅ Support complet Keychron Q1 HE
- ✅ Focus intelligent sur scroll
- ✅ Configuration GTK complète
- ✅ 13 commits ahead of origin/v2
