#!/bin/bash
# Script de test d'installation HyprYou
# Usage: ./test-install.sh

set -e

echo "════════════════════════════════════════"
echo "  Test d'installation HyprYou"
echo "════════════════════════════════════════"
echo ""

# Couleurs
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Fonction de test
test_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "  ${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "  ${RED}✗${NC} $1 (manquant)"
        return 1
    fi
}

# Test dépendances critiques
echo -e "${YELLOW}→ Vérification des dépendances critiques...${NC}"
MISSING=0

test_command gcc || MISSING=$((MISSING+1))
test_command python || MISSING=$((MISSING+1))
test_command hyprctl || MISSING=$((MISSING+1))
test_command sass || MISSING=$((MISSING+1))

echo ""

if [ $MISSING -gt 0 ]; then
    echo -e "${RED}✗ $MISSING dépendance(s) manquante(s)${NC}"
    echo -e "${YELLOW}Installez-les avec:${NC}"
    echo "  sudo pacman -S --needed gcc python hyprland dart-sass"
    exit 1
else
    echo -e "${GREEN}✓ Toutes les dépendances critiques sont présentes${NC}"
fi

echo ""
echo -e "${YELLOW}→ Test de compilation...${NC}"

# Test build
if make clean > /dev/null 2>&1 && make build > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Compilation réussie${NC}"
    
    # Vérifier binaires
    if [ -f "build/hypryouctl" ] && [ -f "build/hypryou-start" ]; then
        echo -e "${GREEN}✓ Binaires générés${NC}"
        ls -lh build/hypryouctl build/hypryou-start 2>/dev/null | awk '{print "  - " $9 " (" $5 ")"}'
    else
        echo -e "${RED}✗ Binaires manquants${NC}"
        exit 1
    fi
else
    echo -e "${RED}✗ Échec de compilation${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo -e "${GREEN}  ✓ Tests passés avec succès !${NC}"
echo -e "${GREEN}════════════════════════════════════════${NC}"
echo ""
echo "Prochaine étape:"
echo "  sudo make install"
