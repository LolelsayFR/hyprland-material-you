"""Outside Parameters - Accès rapide aux outils externes de configuration"""

from repository import gtk
from src.services.apps import launch_detached
from utils.logger import logger
import src.widget as widget
import typing as t
import subprocess
import weakref


class OutsideToolButton(gtk.Box):
    """Bouton pour lancer un outil externe"""
    
    def __init__(
        self,
        title: str,
        description: str,
        icon: str,
        command: str,
        check_command: str | None = None,
        close_window: bool = True
    ) -> None:
        super().__init__(
            css_classes=("outside-tool-button",),
            orientation=gtk.Orientation.HORIZONTAL,
            spacing=12
        )
        
        self.command = command
        self.check_command = check_command
        self.close_window = close_window
        self._settings_window: weakref.ReferenceType | None = None
        
        # Icône
        icon_box = gtk.Box(
            css_classes=("icon-box",),
            valign=gtk.Align.CENTER
        )
        icon_widget = widget.Icon(icon)
        icon_box.append(icon_widget)
        
        # Texte (titre + description)
        text_box = gtk.Box(
            css_classes=("text-box",),
            orientation=gtk.Orientation.VERTICAL,
            valign=gtk.Align.CENTER,
            hexpand=True
        )
        
        title_label = gtk.Label(
            label=title,
            css_classes=("tool-title",),
            halign=gtk.Align.START,
            xalign=0
        )
        
        desc_label = gtk.Label(
            label=description,
            css_classes=("tool-description",),
            halign=gtk.Align.START,
            xalign=0,
            wrap=True
        )
        
        text_box.append(title_label)
        text_box.append(desc_label)
        
        # Bouton de lancement
        launch_button = gtk.Button(
            child=widget.Icon("open_in_new"),
            css_classes=("launch-button",),
            valign=gtk.Align.CENTER
        )
        launch_button.connect("clicked", self.on_launch)
        
        # Vérifier si l'outil est disponible
        if not self._check_available():
            launch_button.set_sensitive(False)
            desc_label.set_label(f"{description} (non installé)")
        
        self.append(icon_box)
        self.append(text_box)
        self.append(launch_button)
    
    def _check_available(self) -> bool:
        """Vérifie si l'outil est disponible"""
        check_cmd = self.check_command if self.check_command else self.command.split()[0]
        try:
            result = subprocess.run(
                ["which", check_cmd],
                capture_output=True,
                timeout=1
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def on_launch(self, *args: t.Any) -> None:
        """Lance l'outil externe"""
        try:
            # Lancer l'outil externe
            launch_detached(self.command)
            if __debug__:
                logger.debug(f"Launched external tool: {self.command}")
            
            # Fermer le menu settings si demandé
            if self.close_window and self._settings_window is not None:
                window = self._settings_window()
                if window is not None and not window._destroyed:
                    window.destroy()
        except Exception as e:
            logger.error(f"Failed to launch {self.command}: {e}")
    
    def set_settings_window(self, window: gtk.ApplicationWindow) -> None:
        """Définit la fenêtre settings pour pouvoir la fermer"""
        self._settings_window = weakref.ref(window)


class OutsidePage(gtk.ScrolledWindow):
    """Page Outside Parameters avec accès aux outils externes"""
    
    def __init__(self) -> None:
        super().__init__(
            css_classes=("settings-page", "outside-page"),
            hexpand=True,
            vexpand=True
        )
        
        # Liste des boutons pour pouvoir leur passer la fenêtre plus tard
        self._tool_buttons: list[OutsideToolButton] = []
        
        # Container principal
        main_box = gtk.Box(
            css_classes=("outside-main-box",),
            orientation=gtk.Orientation.VERTICAL,
            spacing=24,
            margin_top=24,
            margin_bottom=24,
            margin_start=24,
            margin_end=24
        )
        
        # En-tête
        header_box = gtk.Box(
            css_classes=("outside-header",),
            orientation=gtk.Orientation.VERTICAL,
            spacing=8
        )
        
        title = gtk.Label(
            label="Outside Parameters",
            css_classes=("outside-title",),
            halign=gtk.Align.START,
            xalign=0
        )
        
        subtitle = gtk.Label(
            label="Accès rapide aux outils de configuration externe",
            css_classes=("outside-subtitle",),
            halign=gtk.Align.START,
            xalign=0
        )
        
        header_box.append(title)
        header_box.append(subtitle)
        main_box.append(header_box)
        
        # Séparateur
        separator1 = gtk.Separator(
            css_classes=("outside-separator",)
        )
        main_box.append(separator1)
        
        # Section GTK
        gtk_section = self._create_section(
            "GTK Configuration",
            "Outils de personnalisation GTK"
        )
        
        # GTK Settings
        gtk_button = OutsideToolButton(
            title="GTK Settings",
            description="Configure l'apparence des applications GTK (thèmes, icônes, fonts)",
            icon="new_window",
            command="env XDG_CURRENT_DESKTOP=GNOME gnome-control-center appearance",
            check_command="gnome-control-center"
        )
        self._tool_buttons.append(gtk_button)
        gtk_section.append(gtk_button)
        
        # LXAppearance (alternative)
        lxappearance_button = OutsideToolButton(
            title="LXAppearance",
            description="Alternative légère pour configurer les thèmes GTK",
            icon="palette",
            command="lxappearance"
        )
        self._tool_buttons.append(lxappearance_button)
        gtk_section.append(lxappearance_button)
        
        # nwg-look (Wayland native)
        nwglook_button = OutsideToolButton(
            title="nwg-look",
            description="Outil GTK natif pour Wayland (thèmes, icônes, curseurs)",
            icon="style",
            command="nwg-look"
        )
        self._tool_buttons.append(nwglook_button)
        gtk_section.append(nwglook_button)
        
        main_box.append(gtk_section)
        
        # Section Display
        display_section = self._create_section(
            "Display Configuration",
            "Gestion avancée des moniteurs"
        )
        
        # wdisplays
        wdisplays_button = OutsideToolButton(
            title="wdisplays",
            description="Gestionnaire d'écrans Wayland (position, rotation, résolution)",
            icon="monitor",
            command="wdisplays"
        )
        self._tool_buttons.append(wdisplays_button)
        display_section.append(wdisplays_button)
        
        # Hyprland monitors
        hyprland_monitor_button = OutsideToolButton(
            title="Hyprland Monitors",
            description="Configuration des moniteurs via fichier Hyprland",
            icon="tune",
            command="xdg-open ~/.config/hypr/monitors.conf",
            close_window=False  # Ne pas fermer pour éditer le fichier
        )
        self._tool_buttons.append(hyprland_monitor_button)
        display_section.append(hyprland_monitor_button)
        
        main_box.append(display_section)
        
        # Section Audio/Video
        av_section = self._create_section(
            "Audio & Video",
            "Contrôles audio et vidéo avancés"
        )
        
        # Pavucontrol
        pavucontrol_button = OutsideToolButton(
            title="PulseAudio Volume Control",
            description="Contrôle avancé du volume et des périphériques audio",
            icon="volume_up",
            command="pavucontrol"
        )
        self._tool_buttons.append(pavucontrol_button)
        av_section.append(pavucontrol_button)
        
        # EasyEffects
        easyeffects_button = OutsideToolButton(
            title="EasyEffects",
            description="Effets audio professionnels (égaliseur, compresseur, etc.)",
            icon="graphic_eq",
            command="easyeffects"
        )
        self._tool_buttons.append(easyeffects_button)
        av_section.append(easyeffects_button)
        
        main_box.append(av_section)
        
        # Section Système
        system_section = self._create_section(
            "System Tools",
            "Outils système et configuration avancée"
        )
        
        # dconf-editor
        dconf_button = OutsideToolButton(
            title="dconf Editor",
            description="Éditeur de configuration bas niveau pour GNOME/GTK",
            icon="settings",
            command="dconf-editor"
        )
        self._tool_buttons.append(dconf_button)
        system_section.append(dconf_button)
        
        main_box.append(system_section)
        
        self.set_child(main_box)
    
    def set_settings_window(self, window: gtk.ApplicationWindow) -> None:
        """Définit la fenêtre settings pour tous les boutons"""
        for button in self._tool_buttons:
            button.set_settings_window(window)
    
    def _create_section(self, title: str, description: str) -> gtk.Box:
        """Crée une section avec titre"""
        section = gtk.Box(
            css_classes=("outside-section",),
            orientation=gtk.Orientation.VERTICAL,
            spacing=12
        )
        
        section_header = gtk.Box(
            css_classes=("section-header",),
            orientation=gtk.Orientation.VERTICAL,
            spacing=4
        )
        
        section_title = gtk.Label(
            label=title,
            css_classes=("section-title",),
            halign=gtk.Align.START,
            xalign=0
        )
        
        section_desc = gtk.Label(
            label=description,
            css_classes=("section-description",),
            halign=gtk.Align.START,
            xalign=0
        )
        
        section_header.append(section_title)
        section_header.append(section_desc)
        section.append(section_header)
        
        return section
    
    def on_show(self) -> None:
        """Appelé quand la page est affichée"""
        pass
    
    def on_hide(self) -> None:
        """Appelé quand la page est masquée"""
        pass
    
    def destroy(self) -> None:
        """Nettoyage"""
        pass
