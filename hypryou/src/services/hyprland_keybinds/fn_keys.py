from src.services.hyprland_keybinds.common import KeyBind, Category

key_binds = (
    # ==================== MEDIA CONTROLS ====================
    KeyBind(
        ("", "XF86AudioPlay"),
        ("exec", "hypryouctl player play-pause"),
        "Play/Pause media",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86AudioPause"),
        ("exec", "hypryouctl player pause"),
        "Pause media",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86AudioNext"),
        ("exec", "hypryouctl player next"),
        "Next track",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86AudioPrev"),
        ("exec", "hypryouctl player previous"),
        "Previous track",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86AudioStop"),
        ("exec", "hypryouctl player stop"),
        "Stop media",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86AudioRewind"),
        ("exec", "hypryouctl player seek -10"),
        "Rewind 10s",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86AudioForward"),
        ("exec", "hypryouctl player seek +10"),
        "Forward 10s",
        Category.MISC
    ),
    
    # ==================== THINKPAD T14 GEN 2 Fn KEYS ====================
    KeyBind(
        ("", "XF86AudioMicMute"),
        ("exec", "pactl set-source-mute @DEFAULT_SOURCE@ toggle"),
        "Mute microphone (Fn+F4)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Display"),
        ("exec", "wdisplays"),
        "Display settings (Fn+F7)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86WLAN"),
        ("exec", "nm-connection-editor"),
        "WiFi toggle (Fn+F8)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Tools"),
        ("exec", "hypryouctl settings"),
        "Settings (Fn+F9)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Bluetooth"),
        ("exec", "blueman-manager"),
        "Bluetooth (Fn+F10)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Keyboard"),
        ("exec", "hyprctl switchxkblayout at-translated-set-2-keyboard next"),
        "Toggle keyboard layout (Fn+F11)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Favorites"),
        ("exec", "thunar"),
        "File manager (Fn+F12)",
        Category.APPS
    ),
    # ThinkPad T14 Gen 2 additional keys
    KeyBind(
        ("", "XF86NotificationCenter"),
        ("exec", "hypryouctl toggle notifications"),
        "Notification center (Fn+N)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86PickupPhone"),
        ("exec", "hypryouctl toggle bluetooth_call"),
        "Pickup call (Fn+P)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86HangupPhone"),
        ("exec", "hypryouctl hangup"),
        "Hangup call (Fn+H)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86RFKill"),
        ("exec", "rfkill toggle all"),
        "Airplane mode (Fn+F8 long press)",
        Category.MISC
    ),
    
    # ==================== KEYCHRON Q1 HE KEYS ====================
    # Keychron media keys (usually Fn+number row)
    KeyBind(
        ("", "XF86AudioMute"),
        ("exec", "pactl set-sink-mute @DEFAULT_SINK@ toggle"),
        "Mute audio (Keychron)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86AudioLowerVolume"),
        ("exec", "pactl set-sink-volume @DEFAULT_SINK@ -5%"),
        "Volume down (Keychron)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86AudioRaiseVolume"),
        ("exec", "pactl set-sink-volume @DEFAULT_SINK@ +5%"),
        "Volume up (Keychron)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86MonBrightnessDown"),
        ("exec", "brightnessctl -q s 10%-"),
        "Brightness down (Keychron)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86MonBrightnessUp"),
        ("exec", "brightnessctl -q s +10%"),
        "Brightness up (Keychron)",
        Category.MISC
    ),
    # Keychron Q1 HE specific function keys
    KeyBind(
        ("", "XF86LaunchA"),
        ("exec", "hypryouctl apps_menu"),
        "Apps menu (Keychron Fn+A)",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86LaunchB"),
        ("exec", "hypryouctl quick_settings"),
        "Quick settings (Keychron Fn+B)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86HomePage"),
        ("exec", "firefox"),
        "Web browser (Keychron Home)",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86Mail"),
        ("exec", "thunderbird"),
        "Email client (Keychron Mail)",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86Search"),
        ("exec", "hypryouctl launcher"),
        "Search/Launcher (Keychron Search)",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86Explorer"),
        ("exec", "thunar"),
        "File explorer (Keychron Explorer)",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86Calculator"),
        ("exec", "qalculate-gtk"),
        "Calculator (Keychron Calc)",
        Category.APPS
    ),
    
    # ==================== SYSTEM CONTROLS ====================
    KeyBind(
        ("", "XF86Lock"),
        ("exec", "hypryouctl lock"),
        "Lock screen",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86ScreenSaver"),
        ("exec", "hypryouctl lock"),
        "Screen saver",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Sleep"),
        ("exec", "systemctl suspend"),
        "Suspend",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86PowerOff"),
        ("exec", "hypryouctl power"),
        "Power menu",
        Category.MISC
    )
)
