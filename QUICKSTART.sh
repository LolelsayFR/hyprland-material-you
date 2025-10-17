#!/bin/bash
# Guide de démarrage rapide - HyprYou Fork
# Exécutez ce script pour voir les étapes

cat << 'EOF'

╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║            🚀 GUIDE DE DÉMARRAGE RAPIDE 🚀                   ║
║              HyprYou Fork - LolelsayFR                        ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

📋 ÉTAPE 1 : VÉRIFIER LE STATUT
───────────────────────────────────────────────────────────────
EOF

echo "Branche actuelle : $(git branch --show-current)"
echo "Commits en avance : $(git rev-list --count origin/v2..HEAD 2>/dev/null || echo 'N/A')"
echo "État : $(git status --porcelain | wc -l) fichier(s) non commité(s)"

cat << 'EOF'

📦 ÉTAPE 2 : TESTER LA COMPILATION
───────────────────────────────────────────────────────────────
Commande :
  ./test-install.sh

Si succès → Passer à l'étape 3
Si échec → Installer dépendances manquantes

🔼 ÉTAPE 3 : PUSH VERS GITHUB (Optionnel)
───────────────────────────────────────────────────────────────
Si vous avez un repo GitHub configuré :

  git remote -v  # Vérifier remote
  
Si pas configuré :
  git remote set-url origin https://github.com/VotreUsername/hyprland-material-you.git
  
Push :
  git push origin v2
  
Tag version (optionnel) :
  git tag -a v2.1.5-fork.1 -m "Fork personnalisé avec Makefile"
  git push origin v2.1.5-fork.1

🛠️  ÉTAPE 4 : INSTALLER SUR LE SYSTÈME
───────────────────────────────────────────────────────────────
Méthode A - Makefile (recommandé) :
  make check        # Vérifier dépendances
  make build        # Compiler
  sudo make install # Installer

Méthode B - Package Arch :
  make pkg
  # ou
  makepkg -si

Méthode C - PKGBUILD traditionnel :
  makepkg -si

🎨 ÉTAPE 5 : PREMIÈRE CONNEXION
───────────────────────────────────────────────────────────────
1. Déconnectez-vous de votre session actuelle
2. Dans GDM, cliquez sur l'icône des paramètres (engrenage)
3. Sélectionnez "HyprYou"
4. Entrez votre mot de passe et connectez-vous

⚙️  ÉTAPE 6 : CONFIGURATION (Optionnel)
───────────────────────────────────────────────────────────────
Configs dans : ~/.config/hypryou/

Éditer settings :
  nano ~/.config/hypryou/settings.json
  hypryouctl reload

Créer config perso Hyprland :
  nano ~/.config/hypryou/hyprland.conf
  # Ajoutez vos binds, rules, etc.
  hypryouctl reload

Changer wallpaper :
  # Via l'interface HyprYou (icône engrenage dans la barre)
  # Ou manuellement :
  cp ~/Pictures/monwallpaper.jpg ~/.config/hypryou/wallpaper.jpg
  hypryouctl reload

📚 ÉTAPE 7 : DOCUMENTATION
───────────────────────────────────────────────────────────────
Lire les docs :
  • README-FORK.md  → Vue d'ensemble
  • INSTALL.md      → Guide complet
  • CHANGELOG.md    → Historique
  • SUMMARY.txt     → Récapitulatif

Commandes utiles :
  make help              → Aide Makefile
  hypryouctl --help      → Aide HyprYou
  hyprctl --help         → Aide Hyprland

🔧 DÉPANNAGE
───────────────────────────────────────────────────────────────
Problème : Dépendances manquantes
Solution :
  make check
  # Installer ce qui manque via pacman/yay

Problème : Compilation échoue
Solution :
  make clean
  make build 2>&1 | tee build.log
  # Envoyer build.log si besoin d'aide

Problème : HyprYou ne démarre pas
Solution :
  # Vérifier logs
  journalctl --user -u hypryou -f
  # Vérifier installation
  ls -la /usr/lib/hypryou /usr/share/hypryou

Problème : Blur ne fonctionne pas
Solution :
  # Vérifier config
  grep -r "blur" ~/.config/hypryou/
  # Recharger
  hypryouctl reload

🆘 AIDE SUPPLÉMENTAIRE
───────────────────────────────────────────────────────────────
• Issues GitHub : https://github.com/LolelsayFR/hyprland-material-you/issues
• Discord upstream : https://discord.gg/nCK3sh8mNU
• Wiki Hyprland : https://wiki.hyprland.org/

📝 CHECKLIST COMPLÈTE
───────────────────────────────────────────────────────────────
[ ] 1. Code modifié et commité
[ ] 2. ./test-install.sh passé avec succès
[ ] 3. git push origin v2 (si applicable)
[ ] 4. make build réussi
[ ] 5. sudo make install réussi
[ ] 6. Déconnexion et sélection "HyprYou" dans GDM
[ ] 7. Connexion réussie
[ ] 8. Interface affichée correctement
[ ] 9. Blur et transparence fonctionnent
[ ] 10. Configs personnalisées appliquées

═══════════════════════════════════════════════════════════════
            🎉 Profitez de votre HyprYou ! 🎉
═══════════════════════════════════════════════════════════════

EOF
