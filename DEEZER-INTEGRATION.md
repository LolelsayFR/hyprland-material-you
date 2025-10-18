# Amélioration de l'intégration Deezer

## Résumé
Amélioration de l'intégration du lecteur Deezer dans HyprYou avec affichage des pochettes d'album en temps réel et icône personnalisée.

## Problème
- Les pochettes d'album ne se mettaient pas à jour lors du changement de piste dans Deezer
- Le cache local empêchait la mise à jour des images
- Le nom du lecteur affichait "Deezer" en texte au lieu de l'icône officielle

## Solution

### 1. Chargement direct des pochettes depuis CDN Deezer

**Fichier : `hypryou/src/modules/players.py`**

- Ajout d'une méthode `_is_deezer()` pour détecter le lecteur Deezer
- Pour Deezer : chargement direct de l'URL CDN sans cache local
- Pour les autres lecteurs : conservation du système de cache existant
- Fix GTK4 : utilisation de `load_from_string()` au lieu de `load_from_data()`

```python
def _is_deezer(self) -> bool:
    """Vérifie si le lecteur est Deezer"""
    bus_name = self._item.get_bus_name().lower()
    return "deezer" in bus_name

def update_image(self, force: bool = False) -> None:
    # ...
    if self._is_deezer():
        # Chargement direct depuis l'URL CDN
        css = f"box {{ background-image: url('{art_url}'); }}"
        self.image_provider.load_from_string(css)
    else:
        # Cache local pour les autres lecteurs
        downloader.download_image_async(art_url, self.on_download, (64, 64), "arts")
```

### 2. Détection automatique des changements de piste

**Modification de `update_label()`**

- Détection du changement de titre/artiste
- Appel de `update_image(force=True)` pour forcer le rechargement
- Mise à jour immédiate de la pochette même si l'URL est identique

```python
def update_label(self) -> None:
    # ...
    title_changed = (
        _artists != self.last_changed.artists
        or _title != self.last_changed.title
    )
    
    if title_changed:
        # Forcer la mise à jour de l'image quand la piste change
        self.update_image(force=True)
```

### 3. Icône Deezer au lieu du texte

**Remplacement du widget label par une icône**

```python
bus_name = item.get_bus_name()
if "deezer" in bus_name.lower():
    # Utiliser l'icône Deezer
    self.player = gtk.Image.new_from_icon_name("deezer-desktop")
    self.player.set_pixel_size(16)
    self.player.set_css_classes(["player-icon"])
else:
    self.player = gtk.Label(label=player_name)
```

### 4. Intégration dans la barre

**Fichier : `hypryou/src/modules/bar.py`**

- Même logique de détection Deezer
- Chargement direct des pochettes dans la barre (24x24px)
- Fix GTK4 : `load_from_string()` pour la cohérence

```python
def _is_deezer(self) -> bool:
    """Vérifie si le lecteur actuel est Deezer"""
    if len(current_player.value) != 2:
        return False
    bus_name = current_player.value[1].get_bus_name().lower()
    return "deezer" in bus_name

def update_image(self) -> None:
    # ...
    if self._is_deezer():
        css = f"box {{ background-image: url('{art_url}'); }}"
        self.image_provider.load_from_string(css)
    else:
        downloader.download_image_async(art_url, self.on_download, (24, 24), "arts")
```

### 5. Règles de flou Hyprland

**Fichier : `hypryou-assets/configs/hyprland/windowrule.conf`**

Ajout des règles de transparence et flou pour Deezer :

```conf
# Deezer
windowrulev2 = opacity 0.95 0.85, class:^(Deezer)$
windowrulev2 = opacity 0.95 0.85, class:^(deezer)$
windowrulev2 = opacity 0.95 0.85, class:^(com\.deezer\.Deezer)$
windowrulev2 = opacity 0.95 0.85, class:^(com\.deezer\.desktop)$
```

## Avantages

✅ **Mise à jour en temps réel** : Les pochettes se mettent à jour instantanément lors du changement de piste
✅ **Pas de cache obsolète** : Les images sont chargées directement depuis le CDN Deezer
✅ **Icône professionnelle** : Affichage de l'icône officielle Deezer au lieu du texte
✅ **Compatibilité préservée** : Les autres lecteurs (Spotify, etc.) utilisent toujours le cache local
✅ **Performance** : Pas de téléchargement local, utilisation du cache HTTP du navigateur

## Tests

1. ✅ Lancer Deezer et jouer une musique → Pochette visible dans la barre et le popup
2. ✅ Changer de piste → Pochette mise à jour instantanément
3. ✅ Vérifier l'icône Deezer dans le popup player
4. ✅ Tester avec d'autres lecteurs (Spotify) → Cache local toujours fonctionnel

## Version
- Date : 18 octobre 2025
- Branche : v2
- Commit : À venir

## Auteur
Développé avec l'aide de GitHub Copilot
