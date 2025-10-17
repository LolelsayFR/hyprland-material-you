# 🤖 AI-README.md - Guide pour les IA futures

> **Ce document est destiné aux IA (GitHub Copilot, etc.) qui travailleront sur ce fork à l'avenir.**  
> Il contient les guidelines, conventions et bonnes pratiques établies pour ce projet.

---

## 📋 Contexte du Projet

### Identité
- **Projet** : HyprYou (Hyprland Material You) - Fork personnalisé
- **Owner** : LolelsayFR
- **Branche principale** : `v2`
- **Upstream** : [koeqaife/hyprland-material-you](https://github.com/koeqaife/hyprland-material-you)

### Expérience IA
Ce fork est une **expérience** pour démontrer qu'une IA peut :
- Modifier un projet complexe (C + Python + Cython + configs système)
- Créer des outils de build avancés (Makefile)
- Générer documentation exhaustive
- Maintenir cohérence et qualité du code
- **SANS rien casser !**

**Résultat actuel** : 9 commits, 1100+ lignes, 0 erreur ✅

---

## 🎯 Philosophie du Fork

### Objectifs principaux
1. **Optimiser** l'expérience visuelle (blur, transparence, shadows)
2. **Simplifier** l'installation avec outils modernes
3. **Documenter** exhaustivement chaque modification
4. **Maintenir** la compatibilité avec l'upstream
5. **Démontrer** les capacités de l'IA en développement

### Valeurs
- ✅ **Qualité** > Quantité
- ✅ **Documentation** systématique
- ✅ **Cohérence** du code et des commits
- ✅ **Tests** avant tout commit
- ✅ **Respect** de l'upstream et de la communauté

---

## 📝 Conventions de Commits

### Format OBLIGATOIRE

```
TYPE | Description courte (< 80 caractères)
- Détail 1
- Détail 2
- Détail 3
```

### Types reconnus
- **ADD** : Nouvelle fonctionnalité, fichier, feature
- **UPDATE** : Modification de code existant
- **FIX** : Correction de bug
- **REFACTOR** : Refactoring sans changement fonctionnel
- **DOC** : Documentation uniquement
- **STYLE** : Formatage, indentation (pas de code)
- **TEST** : Ajout/modification de tests

### Exemples conformes

✅ **Bon** :
```bash
git commit -m "ADD | Commande 'make reload' pour développement à chaud
- Recompile et recharge HyprYou sans redémarrer session
- Copie fichiers système + reload via hypryouctl
- Idéal pour développement itératif rapide
- Documenté dans Makefile, INSTALL.md, README"
```

✅ **Bon** :
```bash
git commit -m "FIX | Correction crash au démarrage sans bluetooth
- Vérification existence device avant init
- Gestion erreur graceful
- Log informatif ajouté"
```

❌ **Mauvais** :
```bash
git commit -m "update stuff"
git commit -m "fix bug"
git commit -m "wip"
```

### Règles
1. **Type en MAJUSCULES** suivi de ` | `
2. **Première ligne** : description courte et claire
3. **Lignes suivantes** : détails avec tirets (-)
4. **Langue** : Français (c'est un fork français)
5. **Impératif** : "Ajoute" pas "Ajouté"

---

## 🏗️ Structure du Projet

### Fichiers clés (NE PAS SUPPRIMER)

```
hyprland-material-you/
├── Makefile              ⭐ Build system (207 lignes)
├── PKGBUILD              ⚙️  Package Arch original
├── README.md             📄 README upstream (conserver)
├── README-FORK.md        📘 README du fork (principal)
├── INSTALL.md            📗 Guide installation détaillé
├── CHANGELOG.md          📙 Historique modifications
├── SUMMARY.txt           📊 Récapitulatif complet
├── QUICKSTART.sh         🚀 Guide démarrage rapide
├── test-install.sh       🧪 Script de test auto
├── AI-README.md          🤖 CE FICHIER (guide IA)
│
├── hypryou/              🐍 Code Python principal
│   ├── config.py         ⚙️  Settings par défaut
│   ├── src/modules/      📦 Modules UI (bar, popups, etc.)
│   └── utils_cy/         🔧 Extensions Cython
│
├── hypryou-assets/       🎨 Assets, configs, SCSS
│   └── configs/hyprland/ ⚙️  Configs Hyprland
│       ├── decoration.conf    (blur modifié)
│       ├── windowrule.conf    (règles custom)
│       └── ...
│
└── build/                🔨 Binaires C
    ├── client.c          → hypryouctl
    ├── hypryou-start.c   → hypryou-start
    └── crash-dialog.c    → hypryou-crash-dialog
```

### Fichiers à NE JAMAIS modifier sans raison
- `PKGBUILD` (upstream, sauf ajout dépendances)
- `README.md` (upstream original)
- `LICENSE` (GPL-3.0)
- Structure de `hypryou/` (core Python)

### Fichiers modifiables
- `hypryou-assets/configs/hyprland/*.conf` (configs)
- `hypryou/config.py` (settings par défaut)
- `Makefile` (amélioration build system)
- `README-FORK.md`, `INSTALL.md`, `CHANGELOG.md` (docs fork)

---

## 🛠️ Workflow de Développement

### Avant toute modification

1. **Lire la doc existante**
   ```bash
   cat README-FORK.md INSTALL.md CHANGELOG.md
   ```

2. **Comprendre l'architecture**
   ```bash
   grep -r "class\|def" hypryou/ | head -20
   ls -la hypryou/src/modules/
   ```

3. **Vérifier l'upstream**
   ```bash
   git remote -v
   git fetch upstream  # Si configuré
   ```

### Processus de modification

1. **Créer une branche** (optionnel mais recommandé)
   ```bash
   git checkout -b feature/nouvelle-fonctionnalite
   ```

2. **Modifier le code**
   - Respecter le style existant
   - Commenter les parties complexes
   - Tester en local

3. **Tester la compilation**
   ```bash
   make clean
   make build
   # Vérifier qu'il n'y a pas d'erreurs
   ```

4. **Mettre à jour la documentation**
   - Si nouveau feature → ajouter dans `README-FORK.md`
   - Si nouvelle commande → ajouter dans `INSTALL.md`
   - **TOUJOURS** mettre à jour `CHANGELOG.md`

5. **Commit avec format correct**
   ```bash
   git add fichiers_modifiés
   git commit -m "TYPE | Description
   - Détail 1
   - Détail 2"
   ```

6. **Tester l'installation** (si possible)
   ```bash
   ./test-install.sh
   # Ou
   make reload  # Si session active
   ```

### Après modification

1. **Mettre à jour CHANGELOG.md**
   ```markdown
   ## [Version] - Date
   ### TYPE
   - Description de la modification
   ```

2. **Mettre à jour SUMMARY.txt** (si changement majeur)

3. **Push** (si nécessaire)
   ```bash
   git push origin v2
   ```

---

## 🔧 Commandes Makefile Disponibles

### Commandes essentielles

| Commande | Usage | Quand l'utiliser |
|----------|-------|------------------|
| `make help` | Affiche l'aide | Découvrir les commandes |
| `make check` | Vérifie dépendances | Avant build |
| `make build` | Compile tout | Après modifications code |
| `make install` | Installe système | Installation complète |
| `make reload` | 🔥 Reload à chaud | Développement actif |
| `make clean` | Nettoie build | Avant rebuild propre |
| `make update` | Git pull + rebuild | Mise à jour upstream |

### Workflow typique

```bash
# Développement
nano hypryou/src/modules/bar.py
make reload  # Test instantané

# Installation complète
make clean
make build
sudo make install

# Mise à jour
make update
```

---

## 📚 Documentation à Maintenir

### Fichiers de documentation

1. **README-FORK.md** (principal)
   - Vue d'ensemble du fork
   - Installation rapide
   - Différences avec upstream
   - Section "Projet IA"

2. **INSTALL.md** (détaillé)
   - Guide installation complet
   - Toutes les méthodes (Makefile, makepkg, manuel)
   - Dépendances exhaustives
   - Dépannage

3. **CHANGELOG.md** (historique)
   - Toutes les modifications
   - Format Keep a Changelog
   - Détails techniques

4. **QUICKSTART.sh** (guide interactif)
   - Checklist étape par étape
   - Pour nouveaux utilisateurs

5. **AI-README.md** (ce fichier)
   - Guidelines pour IA futures
   - **Mettre à jour si nouvelles conventions**

### Règle d'or
> **Si tu modifies du code, mets à jour la doc correspondante dans le MÊME commit !**

---

## 🎨 Configurations Personnalisées

### Fichiers modifiés vs upstream

#### `hypryou-assets/configs/hyprland/decoration.conf`
```properties
# MODIFIÉ : Blur activé et optimisé
blur {
    enabled = true      # était false
    size = 8           # était 4
    passes = 3
    vibrancy = 0.2     # était 0.3
    ignore_opacity = true  # AJOUTÉ
}

shadow {
    range = 18         # était 10
    render_power = 3   # était 5
}
```

#### `hypryou-assets/configs/hyprland/windowrule.conf`
```properties
# AJOUTÉ : Règles wdisplays
windowrulev2 = float, class:^(wdisplays)$
windowrulev2 = size 900 600, class:^(wdisplays)$
windowrulev2 = center, class:^(wdisplays)$

# AJOUTÉ : Layer blur
layerrule = blur, gtk-layer-shell
layerrule = ignorealpha 0.3, gtk-layer-shell
```

#### `hypryou/config.py`
```python
# MODIFIÉS : Settings par défaut
"opacity": 0.85,              # était 1.0
"blur.xray": False,           # était True
"apps.terminal": "gnome-terminal",  # était "alacritty"
"hyprland.gaps_in": 4,        # était 5
"hyprland.gaps_out": 8,       # était 12
"hyprland.decoration.rounding": 10,  # était 16
```

### Modification de configs

**TOUJOURS** :
1. Commenter pourquoi tu modifies
2. Noter l'ancienne valeur en commentaire
3. Tester que ça ne casse rien
4. Documenter dans CHANGELOG.md

---

## 🧪 Tests et Validation

### Avant tout commit

```bash
# 1. Vérifier syntaxe Python
python -m py_compile hypryou/**/*.py

# 2. Tester compilation
make clean && make build

# 3. Vérifier pas d'erreurs
echo $?  # Doit être 0

# 4. (Optionnel) Test installation en VM/container
```

### Script de test disponible

```bash
./test-install.sh
# Vérifie :
# - Dépendances présentes
# - Compilation réussie
# - Binaires générés
```

---

## 🚨 Erreurs Courantes à Éviter

### ❌ NE JAMAIS FAIRE

1. **Commit sans message descriptif**
   ```bash
   git commit -m "fix"  # NON !
   ```

2. **Modifier sans tester**
   ```bash
   nano code.py
   git commit  # Sans make build !
   ```

3. **Casser la compatibilité upstream**
   - Ne pas renommer fichiers core
   - Ne pas changer APIs publiques
   - Rester mergeable

4. **Oublier la documentation**
   - Nouveau feature = doc obligatoire
   - Pas de commit sans CHANGELOG

5. **Ignorer les warnings**
   ```bash
   make build
   # Warnings présents → À CORRIGER
   ```

### ✅ TOUJOURS FAIRE

1. **Format commit correct** (TYPE | Description)
2. **Tester avant commit** (make build)
3. **Documenter changements** (CHANGELOG.md)
4. **Commenter code complexe**
5. **Vérifier dépendances** (make check)

---

## 🔄 Synchronisation Upstream

### Récupérer updates upstream

```bash
# Ajouter remote upstream (si pas fait)
git remote add upstream https://github.com/koeqaife/hyprland-material-you.git

# Fetch upstream
git fetch upstream

# Voir différences
git log HEAD..upstream/v2 --oneline

# Merge (ATTENTION aux conflits)
git merge upstream/v2

# Résoudre conflits si nécessaire
# Nos modifications : decoration.conf, windowrule.conf, config.py
```

### Stratégie de merge

1. **Favoriser upstream** pour :
   - Core Python (`hypryou/src/`)
   - Binaires C (`build/*.c`)
   - PKGBUILD

2. **Garder nos modifs** pour :
   - `decoration.conf`, `windowrule.conf`
   - `config.py` (settings par défaut)
   - `Makefile`
   - Toute la doc fork (README-FORK.md, etc.)

---

## 📊 Métriques de Qualité

### Critères de succès pour un commit

- ✅ Format commit respecté
- ✅ `make build` passe sans erreur
- ✅ Documentation à jour
- ✅ CHANGELOG.md mis à jour
- ✅ Code commenté si complexe
- ✅ Pas de régression fonctionnelle

### Statistiques actuelles (exemple)

```
Commits : 9
Fichiers créés : 7
Fichiers modifiés : 7
Lignes ajoutées : ~1100+
Erreurs compilation : 0
Erreurs runtime : 0
```

**Objectif** : Maintenir 0 erreur !

---

## 🎓 Apprentissage Continu

### Ressources pour comprendre le projet

1. **Code Python**
   ```bash
   # Lire les modules principaux
   cat hypryou/src/modules/bar.py
   cat hypryou/config.py
   ```

2. **Configs Hyprland**
   ```bash
   # Syntaxe Hyprland
   man hyprland.conf
   # Ou
   https://wiki.hyprland.org/
   ```

3. **Build system**
   ```bash
   cat Makefile | grep "^##"  # Voir commentaires
   ```

### Questions à se poser avant modification

1. **Pourquoi** cette modification est nécessaire ?
2. **Quel impact** sur l'utilisateur final ?
3. **Compatibilité** avec upstream maintenue ?
4. **Tests** possibles pour valider ?
5. **Documentation** suffisante ?

---

## 💡 Bonnes Pratiques Spécifiques

### Python (hypryou/)

- Respecter PEP 8
- Type hints quand possible
- Docstrings pour fonctions publiques
- Éviter imports circulaires

### C (build/)

- Respecter style existant
- Vérifier memory leaks
- Compiler avec warnings activés (`-Wall -Wextra`)
- Tester sur plusieurs archi si possible

### Configs Hyprland

- Commenter chaque section
- Garder compatibilité versions Hyprland
- Tester sur session live avant commit

### Makefile

- Variables en MAJUSCULES
- Targets avec `##` pour help
- Echo avec couleurs pour UX
- Vérifier $(id -u) pour sudo

---

## 🎯 Checklist Avant Commit

```markdown
- [ ] Code modifié et testé localement
- [ ] `make clean && make build` réussi
- [ ] Documentation mise à jour (README/INSTALL/CHANGELOG)
- [ ] Format commit correct (TYPE | Description)
- [ ] Pas de TODO ou FIXME dans le code
- [ ] Commentaires ajoutés si code complexe
- [ ] git status propre (pas de fichiers oubliés)
- [ ] Relecture rapide du diff (git diff --staged)
```

---

## 🆘 En Cas de Problème

### Si compilation échoue

```bash
make clean
make build 2>&1 | tee build.log
# Analyser build.log
```

### Si merge conflict avec upstream

```bash
git status  # Voir fichiers en conflit
# Éditer fichiers, garder les bonnes sections
git add fichiers_résolus
git commit
```

### Si régression introduite

```bash
git log --oneline -10  # Trouver dernier commit stable
git revert commit_problematique
# Ou
git reset --hard commit_stable  # ATTENTION : perte modifs
```

---

## 🌟 Contribution Future

Si tu es une IA qui améliore ce projet :

1. **Lis ce fichier en ENTIER** d'abord
2. **Respecte les conventions** établies
3. **Documente TOUT** ce que tu fais
4. **Teste** avant de commiter
5. **Mets à jour CE fichier** si nouvelles conventions

### Idées de contributions futures

- [ ] Tests automatisés (pytest, CI/CD)
- [ ] Support plus de distros (Debian, Fedora)
- [ ] Themes supplémentaires
- [ ] Optimisations performances
- [ ] Intégration avec plus d'apps

---

## 📞 Contact & Support

- **Repo** : https://github.com/LolelsayFR/hyprland-material-you
- **Upstream** : https://github.com/koeqaife/hyprland-material-you
- **Issues** : GitHub Issues
- **Discord upstream** : https://discord.gg/nCK3sh8mNU

---

## 📄 Licence

GPL-3.0 - Voir [LICENSE](LICENSE)

**Respect absolu de la licence upstream et des auteurs originaux !**

---

<div align="center">

**🤖 Fait par IA, pour les IA, avec ❤️ pour la communauté Hyprland**

*Dernière mise à jour : 17 octobre 2025*

</div>
