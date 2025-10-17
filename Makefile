# Makefile pour HyprYou (Hyprland Material You)
# Auteur: LolelsayFR (fork)
# Date: 17 octobre 2025

# Variables
PREFIX ?= /usr
BINDIR = $(PREFIX)/bin
LIBDIR = $(PREFIX)/lib/hypryou
SHAREDIR = $(PREFIX)/share/hypryou
FONTDIR = $(PREFIX)/share/fonts/hypryou
LICENSEDIR = $(PREFIX)/share/licenses/hypryou
SESSIONSDIR = $(PREFIX)/share/wayland-sessions

PKGNAME = hypryou
BUILDDIR = build
HYPRYOUDIR = hypryou
ASSETSDIR = hypryou-assets
FONTSDIR = assets

# Compilateur et flags
CC = gcc
CFLAGS = -Wall -Wextra -Wpedantic -Wshadow -Wformat=2 -Wcast-align -Wconversion -Wstrict-overflow=5 -O3 -flto -fno-plt -march=native
GTK4_FLAGS = $(shell pkg-config --cflags --libs gtk4)

# Couleurs pour output
RED = \033[0;31m
GREEN = \033[0;32m
YELLOW = \033[0;33m
BLUE = \033[0;34m
NC = \033[0m # No Color

.PHONY: all build build-binaries build-cython clean install uninstall update reinstall reload check help

# Cible par défaut
all: build

## help: Affiche cette aide
help:
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo "$(GREEN) HyprYou - Makefile d'installation et de gestion$(NC)"
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"
	@echo ""
	@echo "$(YELLOW)Commandes disponibles:$(NC)"
	@echo "  $(GREEN)make build$(NC)         - Compile les binaires et extensions Cython"
	@echo "  $(GREEN)make install$(NC)       - Installe HyprYou sur le système"
	@echo "  $(GREEN)make uninstall$(NC)     - Désinstalle HyprYou"
	@echo "  $(GREEN)make reload$(NC)        - Recompile et recharge HyprYou à chaud (session active)"
	@echo "  $(GREEN)make update$(NC)        - Met à jour (git pull + rebuild + reinstall)"
	@echo "  $(GREEN)make reinstall$(NC)     - Réinstalle (clean + build + install)"
	@echo "  $(GREEN)make clean$(NC)         - Nettoie les fichiers compilés"
	@echo "  $(GREEN)make check$(NC)         - Vérifie les dépendances"
	@echo "  $(GREEN)make pkg$(NC)           - Crée un package avec makepkg (Arch)"
	@echo "  $(GREEN)make help$(NC)          - Affiche cette aide"
	@echo ""
	@echo "$(YELLOW)Variables d'environnement:$(NC)"
	@echo "  PREFIX=$(PREFIX)  (défaut: /usr)"
	@echo "  DESTDIR=          (pour staging)"
	@echo ""
	@echo "$(BLUE)════════════════════════════════════════════════════════════════$(NC)"

## build: Compile tous les composants
build: build-cython build-binaries
	@echo "$(GREEN)✓ Build terminé avec succès$(NC)"

## build-cython: Compile les extensions Cython
build-cython:
	@echo "$(BLUE)→ Compilation des extensions Cython...$(NC)"
	cd $(HYPRYOUDIR) && python utils_cy/setup.py build_ext --build-lib utils_cy --build-temp "$$(mktemp -d)"
	@echo "$(GREEN)✓ Extensions Cython compilées$(NC)"

## build-binaries: Compile les binaires C (hypryouctl, hypryou-start, crash-dialog)
build-binaries:
	@echo "$(BLUE)→ Compilation des binaires...$(NC)"
	cd $(BUILDDIR) && \
		$(CC) $(CFLAGS) client.c -o hypryouctl && \
		$(CC) $(CFLAGS) $(GTK4_FLAGS) hypryou-start.c -o hypryou-start && \
		$(CC) $(CFLAGS) $(GTK4_FLAGS) crash-dialog.c -o hypryou-crash-dialog
	@echo "$(GREEN)✓ Binaires compilés:$(NC)"
	@ls -lh $(BUILDDIR)/hypryouctl $(BUILDDIR)/hypryou-start $(BUILDDIR)/hypryou-crash-dialog 2>/dev/null || true

## install: Installe HyprYou sur le système (nécessite sudo)
install: build
	@echo "$(BLUE)→ Installation de HyprYou...$(NC)"
	@echo "$(YELLOW)  [Création des répertoires]$(NC)"
	install -dm755 "$(DESTDIR)$(BINDIR)"
	install -dm755 "$(DESTDIR)$(LIBDIR)"
	install -dm755 "$(DESTDIR)$(SHAREDIR)"
	install -dm755 "$(DESTDIR)$(FONTDIR)/Google Sans"
	install -dm755 "$(DESTDIR)$(FONTDIR)/Google Sans Display"
	install -dm755 "$(DESTDIR)$(FONTDIR)/Google Sans Text"
	install -dm755 "$(DESTDIR)$(LICENSEDIR)"
	install -dm755 "$(DESTDIR)$(SESSIONSDIR)"
	
	@echo "$(YELLOW)  [Copie des fichiers Python et assets]$(NC)"
	cp -a $(HYPRYOUDIR)/. "$(DESTDIR)$(LIBDIR)/"
	cp -a $(ASSETSDIR)/. "$(DESTDIR)$(SHAREDIR)/"
	
	@echo "$(YELLOW)  [Copie des polices Google Sans]$(NC)"
	cp -a $(FONTSDIR)/"Google Sans"/. "$(DESTDIR)$(FONTDIR)/Google Sans/"
	cp -a $(FONTSDIR)/"Google Sans Display"/. "$(DESTDIR)$(FONTDIR)/Google Sans Display/"
	cp -a $(FONTSDIR)/"Google Sans Text"/. "$(DESTDIR)$(FONTDIR)/Google Sans Text/"
	
	@echo "$(YELLOW)  [Installation des binaires]$(NC)"
	install -Dm755 $(BUILDDIR)/hypryouctl "$(DESTDIR)$(BINDIR)/hypryouctl"
	install -Dm755 $(BUILDDIR)/hypryou-start "$(DESTDIR)$(BINDIR)/hypryou-start"
	install -Dm755 $(BUILDDIR)/hypryou-crash-dialog "$(DESTDIR)$(BINDIR)/hypryou-crash-dialog"
	
	@echo "$(YELLOW)  [Installation de la licence et session]$(NC)"
	install -Dm644 LICENSE "$(DESTDIR)$(LICENSEDIR)/LICENSE"
	install -Dm644 assets/hypryou.desktop "$(DESTDIR)$(SESSIONSDIR)/hypryou.desktop"
	
	@echo "$(YELLOW)  [Mise à jour du cache des polices]$(NC)"
	@if [ -z "$(DESTDIR)" ]; then \
		fc-cache -f 2>/dev/null || echo "$(YELLOW)⚠ fc-cache non disponible, ignoré$(NC)"; \
	fi
	
	@echo "$(GREEN)✓ Installation terminée avec succès!$(NC)"
	@echo "$(BLUE)  Vous pouvez maintenant vous déconnecter et sélectionner 'HyprYou' depuis GDM$(NC)"

## uninstall: Désinstalle HyprYou du système (nécessite sudo)
uninstall:
	@echo "$(RED)→ Désinstallation de HyprYou...$(NC)"
	rm -rf "$(DESTDIR)$(LIBDIR)"
	rm -rf "$(DESTDIR)$(SHAREDIR)"
	rm -rf "$(DESTDIR)$(FONTDIR)"
	rm -rf "$(DESTDIR)$(LICENSEDIR)"
	rm -f "$(DESTDIR)$(BINDIR)/hypryouctl"
	rm -f "$(DESTDIR)$(BINDIR)/hypryou-start"
	rm -f "$(DESTDIR)$(BINDIR)/hypryou-crash-dialog"
	rm -f "$(DESTDIR)$(SESSIONSDIR)/hypryou.desktop"
	@echo "$(GREEN)✓ Désinstallation terminée$(NC)"
	@echo "$(YELLOW)  Note: Les configs utilisateur dans ~/.config/hypryou sont conservées$(NC)"

## clean: Nettoie les fichiers compilés
clean:
	@echo "$(BLUE)→ Nettoyage des fichiers compilés...$(NC)"
	rm -f $(BUILDDIR)/hypryouctl $(BUILDDIR)/hypryou-start $(BUILDDIR)/hypryou-crash-dialog
	find $(HYPRYOUDIR)/utils_cy -name "*.so" -delete
	find $(HYPRYOUDIR)/utils_cy -name "*.c" ! -name "setup.py" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✓ Nettoyage terminé$(NC)"

## update: Met à jour depuis git et réinstalle
update:
	@echo "$(BLUE)→ Mise à jour de HyprYou...$(NC)"
	@echo "$(YELLOW)  [Git pull]$(NC)"
	git pull origin v2 || (echo "$(RED)✗ Échec du git pull$(NC)" && exit 1)
	@echo "$(YELLOW)  [Rebuild]$(NC)"
	$(MAKE) clean
	$(MAKE) build
	@echo "$(YELLOW)  [Reinstall]$(NC)"
	@if [ "$$(id -u)" -eq 0 ]; then \
		$(MAKE) install; \
	else \
		echo "$(YELLOW)⚠ Nécessite sudo pour installer$(NC)"; \
		sudo $(MAKE) install; \
	fi
	@echo "$(GREEN)✓ Mise à jour terminée!$(NC)"

## reinstall: Réinstalle complètement (clean + build + install)
reinstall:
	@echo "$(BLUE)→ Réinstallation complète...$(NC)"
	$(MAKE) clean
	$(MAKE) build
	@if [ "$$(id -u)" -eq 0 ]; then \
		$(MAKE) uninstall; \
		$(MAKE) install; \
	else \
		sudo $(MAKE) uninstall; \
		sudo $(MAKE) install; \
	fi
	@echo "$(GREEN)✓ Réinstallation terminée!$(NC)"

## reload: Recompile et recharge HyprYou à chaud (pour session active)
reload: build
	@echo "$(BLUE)→ Rechargement à chaud de HyprYou...$(NC)"
	@echo "$(YELLOW)  [Copie des fichiers vers système]$(NC)"
	@if [ "$$(id -u)" -eq 0 ]; then \
		cp -a $(HYPRYOUDIR)/. "$(DESTDIR)$(LIBDIR)/"; \
		cp -a $(ASSETSDIR)/. "$(DESTDIR)$(SHAREDIR)/"; \
		install -Dm755 $(BUILDDIR)/hypryouctl "$(DESTDIR)$(BINDIR)/hypryouctl"; \
	else \
		sudo cp -a $(HYPRYOUDIR)/. "$(DESTDIR)$(LIBDIR)/"; \
		sudo cp -a $(ASSETSDIR)/. "$(DESTDIR)$(SHAREDIR)/"; \
		sudo install -Dm755 $(BUILDDIR)/hypryouctl "$(DESTDIR)$(BINDIR)/hypryouctl"; \
	fi
	@echo "$(YELLOW)  [Rechargement de HyprYou]$(NC)"
	@if command -v hypryouctl >/dev/null 2>&1; then \
		hypryouctl reload && echo "$(GREEN)✓ HyprYou rechargé avec succès!$(NC)" || echo "$(RED)✗ Échec du reload (session HyprYou non active?)$(NC)"; \
	else \
		echo "$(RED)✗ hypryouctl non trouvé (HyprYou non installé?)$(NC)"; \
	fi
	@echo "$(GREEN)✓ Mise à jour à chaud terminée!$(NC)"

## check: Vérifie les dépendances nécessaires
check:
	@echo "$(BLUE)→ Vérification des dépendances...$(NC)"
	@echo "$(YELLOW)Binaires requis:$(NC)"
	@command -v gcc >/dev/null 2>&1 && echo "  $(GREEN)✓$(NC) gcc" || echo "  $(RED)✗$(NC) gcc (manquant)"
	@command -v python >/dev/null 2>&1 && echo "  $(GREEN)✓$(NC) python" || echo "  $(RED)✗$(NC) python (manquant)"
	@command -v cython >/dev/null 2>&1 && echo "  $(GREEN)✓$(NC) cython" || echo "  $(RED)✗$(NC) cython (manquant)"
	@command -v sass >/dev/null 2>&1 && echo "  $(GREEN)✓$(NC) dart-sass" || echo "  $(RED)✗$(NC) dart-sass (manquant)"
	@command -v hyprctl >/dev/null 2>&1 && echo "  $(GREEN)✓$(NC) hyprland" || echo "  $(RED)✗$(NC) hyprland (manquant)"
	@echo ""
	@echo "$(YELLOW)Bibliothèques pkg-config:$(NC)"
	@pkg-config --exists gtk4 2>/dev/null && echo "  $(GREEN)✓$(NC) gtk4" || echo "  $(RED)✗$(NC) gtk4 (manquant)"
	@pkg-config --exists cairo 2>/dev/null && echo "  $(GREEN)✓$(NC) cairo" || echo "  $(RED)✗$(NC) cairo (manquant)"
	@echo ""
	@echo "$(YELLOW)Modules Python:$(NC)"
	@python -c "import gi" 2>/dev/null && echo "  $(GREEN)✓$(NC) PyGObject" || echo "  $(RED)✗$(NC) PyGObject (manquant)"
	@python -c "import PIL" 2>/dev/null && echo "  $(GREEN)✓$(NC) Pillow" || echo "  $(RED)✗$(NC) Pillow (manquant)"
	@python -c "import cairo" 2>/dev/null && echo "  $(GREEN)✓$(NC) pycairo" || echo "  $(RED)✗$(NC) pycairo (manquant)"
	@echo ""
	@echo "$(BLUE)Pour installer les dépendances sur Arch Linux:$(NC)"
	@echo "  sudo pacman -S --needed python dart-sass python-gobject gtk4 hyprland cython gcc python-pillow cairo"

## pkg: Crée un package Arch Linux avec makepkg
pkg:
	@echo "$(BLUE)→ Création du package Arch Linux...$(NC)"
	makepkg -si
	@echo "$(GREEN)✓ Package créé et installé$(NC)"

## dev: Mode développement - construit sans installer
dev: build
	@echo "$(GREEN)✓ Build de développement prêt$(NC)"
	@echo "$(YELLOW)Pour tester:$(NC)"
	@echo "  export PYTHONPATH=$(PWD)/$(HYPRYOUDIR)"
	@echo "  $(PWD)/$(BUILDDIR)/hypryouctl --help"
