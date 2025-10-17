from src.services.hyprland_keybinds.common import KeyBind, Category

key_binds = (
    # Media controls
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
    
    # System controls
    KeyBind(
        ("", "XF86Lock"),
        ("exec", "hypryouctl lock"),
        "Lock screen",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Tools"),
        ("exec", "hypryouctl settings"),
        "Settings",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Calculator"),
        ("exec", "qalculate-gtk"),
        "Calculator",
        Category.APPS
    ),
    
    # ThinkPad specific Fn keys
    KeyBind(
        ("", "XF86Display"),
        ("exec", "wdisplays"),
        "Display settings (Fn+F7)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86WLAN"),
        ("exec", "nm-connection-editor"),
        "WiFi settings (Fn+F8)",
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
        ("exec", "hypryouctl toggle_keyboard"),
        "Toggle keyboard (Fn+F11)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Favorites"),
        ("exec", "hypryouctl favorites"),
        "Favorites (Fn+F12)",
        Category.MISC
    ),
    
    # ThinkPad multimedia
    KeyBind(
        ("", "XF86AudioMicMute"),
        ("exec", "pactl set-source-mute @DEFAULT_SOURCE@ toggle"),
        "Mute microphone (Fn+F4)",
        Category.MISC
    ),
    KeyBind(
        ("", "XF86Explorer"),
        ("exec", "hypryouctl apps files"),
        "File explorer",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86HomePage"),
        ("exec", "hypryouctl apps browser"),
        "Web browser",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86Search"),
        ("exec", "hypryouctl launcher"),
        "Search/Launcher",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86LaunchA"),
        ("exec", "hypryouctl apps_menu"),
        "Apps menu",
        Category.APPS
    ),
    KeyBind(
        ("", "XF86LaunchB"),
        ("exec", "hypryouctl quick_settings"),
        "Quick settings",
        Category.MISC
    )
)
