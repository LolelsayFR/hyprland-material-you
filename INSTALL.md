# 🚀 Guide d'installation - HyprYou (Fork personnalisé)

Ce fork de [Hyprland Material You](https://github.com/koeqaife/hyprland-material-you) inclut des configurations personnalisées et un Makefile pour une installation simplifiée.

## ✨ Modifications incluses

### Configuration Hyprland
- **Blur optimisé** : `size=8`, `passes=3`, `vibrancy=0.2` avec `ignore_opacity`
- **Shadows améliorées** : `range=18`, `render_power=3`
- **Règles wdisplays** : fenêtre flottante 900×600 centrée
- **Layer blur** : blur automatique pour `gtk-layer-shell`

### Settings par défaut
- Opacity: `0.85` (transparent)
- Terminal: `gnome-terminal`
- Gaps: `in=4`, `out=8`
- Rounding: `10`
- VRR: mode `3`
- Touchpad natural scroll activé
- Cliphist sécurisé par défaut
- Masquer workspaces vides

---

## 📦 Installation

### Méthode 1 : Makefile (Recommandé)

```bash
# Cloner le repo
git clone https://github.com/LolelsayFR/hyprland-material-you.git
cd hyprland-material-you
git checkout v2

# Vérifier les dépendances
make check

# Compiler
make build

# Installer (nécessite sudo)
sudo make install
```

### Méthode 2 : Package Arch Linux

```bash
# Depuis le répertoire du repo
make pkg
# Ou
makepkg -si
```

### Méthode 3 : Installation manuelle

```bash
# Compiler les binaires
cd build
gcc -O3 -march=native -flto client.c -o hypryouctl
gcc -O3 -march=native -flto $(pkg-config --cflags --libs gtk4) hypryou-start.c -o hypryou-start

# Compiler Cython
cd ../hypryou
python utils_cy/setup.py build_ext --build-lib utils_cy

# Installer manuellement
sudo cp -a hypryou /usr/lib/
sudo cp -a hypryou-assets /usr/share/hypryou/
sudo cp build/hypryouctl /usr/bin/
# ... etc
```

---

## 🔧 Commandes Makefile

| Commande | Description |
|----------|-------------|
| `make help` | Affiche l'aide complète |
| `make build` | Compile binaires + Cython |
| `make install` | Installe sur le système (sudo) |
| `make uninstall` | Désinstalle (sudo) |
| `make reload` | Recompile et recharge à chaud (session active) |
| `make update` | Git pull + rebuild + reinstall |
| `make reinstall` | Clean + build + install |
| `make clean` | Nettoie fichiers compilés |
| `make check` | Vérifie dépendances |
| `make pkg` | Crée package Arch |
| `make dev` | Build sans installer |

### 🔥 Développement à chaud

La commande `make reload` permet de **mettre à jour HyprYou sans redémarrer la session** :

```bash
# Modifier le code (Python, configs, assets)
nano hypryou/src/modules/bar.py

# Recompiler et recharger instantanément
make reload

# HyprYou se recharge automatiquement !
```

**Cas d'usage :**
- Modifier l'UI ou les modules Python
- Tester rapidement des changements de config
- Développement itératif sans logout/login

---

## 📋 Dépendances

### Obligatoires (Arch Linux)
```bash
sudo pacman -S --needed \
  python dart-sass python-gobject python-pam gtk4 libgirepository \
  hyprland dbus dbus-glib python-pillow cairo libnm hyprsunset \
  upower python-pywayland cliphist xdg-dbus-proxy \
  xdg-desktop-portal xdg-desktop-portal-gtk xdg-desktop-portal-hyprland \
  xdg-utils polkit-gnome adw-gtk-theme python-cairo networkmanager \
  hyprshot gtk4-layer-shell cython gcc python-setuptools
```

### AUR (requis)
```bash
yay -S python-materialyoucolor-git libastal-bluetooth-git \
       libastal-wireplumber-git ttf-material-symbols-variable-git
```

### Optionnelles
```bash
sudo pacman -S ttf-meslo-nerd-font-powerlevel10k alacritty
yay -S tela-circle-icon-theme-nord hypryou-utils hypryou-greeter
```

---

## 🎨 Utilisation

### Première connexion

1. Déconnectez-vous de votre session
2. Dans GDM, sélectionnez **"HyprYou"** dans le menu des sessions
3. Connectez-vous

### Configuration personnalisée

Les configs se trouvent dans `~/.config/hypryou/` :

```bash
~/.config/hypryou/
├── settings.json          # Settings HyprYou
├── hyprland.conf          # Config Hyprland personnalisée
└── hyprland_generated.conf # Keybinds générés
```

**Éditer les settings** :
```bash
nano ~/.config/hypryou/settings.json
# Puis recharger
hypryouctl reload
```

**Ajouter des configs Hyprland** :
```bash
nano ~/.config/hypryou/hyprland.conf
# Les configs sont chargées automatiquement
```

---

## 🔄 Mise à jour

### Mise à jour automatique
```bash
cd ~/Téléchargements/hyprland-material-you
make update
```

### Mise à jour manuelle
```bash
git pull origin v2
make clean
make build
sudo make install
```

---

## 🐛 Dépannage

### Vérifier installation
```bash
which hypryouctl hypryou-start
ls -la /usr/lib/hypryou /usr/share/hypryou
```

### Logs HyprYou
```bash
# Depuis une session HyprYou
journalctl --user -u hypryou -f
```

### Réinstallation complète
```bash
make reinstall
```

### Désinstallation propre
```bash
sudo make uninstall
rm -rf ~/.config/hypryou  # Si tu veux aussi supprimer tes configs
```

---

## 📝 Différences avec l'upstream

- Blur activé par défaut avec optimisations
- Règles window pour wdisplays
- Settings adaptés (opacity, gaps, terminal, etc.)
- Makefile d'installation complet
- Pas de dépendance wofi (launcher natif)

---

## 🤝 Contribution

Ce fork est personnel mais les PRs sont bienvenues pour :
- Améliorer le Makefile
- Corriger bugs
- Optimiser les settings par défaut

---

## 📄 Licence

GPL-3.0 (voir [LICENSE](LICENSE))

**Upstream** : [koeqaife/hyprland-material-you](https://github.com/koeqaife/hyprland-material-you)  
**Fork** : [LolelsayFR/hyprland-material-you](https://github.com/LolelsayFR/hyprland-material-you)

---

## 🙏 Crédits

- **koeqaife** - Auteur original de HyprYou
- **Community** - Contributeurs et testeurs
- **LolelsayFR** - Customisations et Makefile
