import sys

from PyQt5.QtCore import Qt

__ALPHANUMERICS = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÀÁÂÃÇÉÈÊËÍÌÎÏÑÓÒÔÕÚÙÛÝŸ"

"""
Mappings Qt -> MPV
"""
KEY_MAPPINGS = {Qt.Key_PageUp: ("PGUP",),
                Qt.Key_PageDown: ("PGDWN",),
                Qt.Key_Play: ("PLAY",),
                Qt.Key_Pause: ("PAUSE",),
                Qt.Key_Stop: ("STOP",),
                Qt.Key_Forward: ("FORWARD",),
                Qt.Key_Back: ("REWIND",),
                Qt.Key_MediaPlay: ("PLAY",),
                Qt.Key_MediaStop: ("STOP",),
                Qt.Key_MediaNext: ("NEXT",),
                Qt.Key_MediaPrevious: ("PREV",),
                Qt.Key_MediaPause: ("PAUSE",),
                Qt.Key_MediaTogglePlayPause: ("PLAYPAUSE",),
                Qt.Key_Home: ("HOME",),
                Qt.Key_End: ("END",),
                Qt.Key_Escape: ("ESC",),
                Qt.Key_Left: ("LEFT",),
                Qt.Key_Right: ("RIGHT",),
                Qt.Key_Up: ("UP", True),
                Qt.Key_Down: ("DOWN", True),
                }


def command_generator(modifiers, key_str, mod_required=False, is_char=False):
    """
    Generates a command for the mpv player using the given commands.

    :param modifiers: The modifiers to use (e.g SHIFT, CTRL, ALT)
    :param key_str: The key string to delegate to mpv
    :param mod_required: True if modifier required, False else
    :param is_char: Whether key_str is explicitly a char
    :return: The key-string to delegate to mpv if allowed. None else.
    """

    shift = "shift" if modifiers & Qt.SHIFT else ""
    ctrl = "ctrl" if modifiers & Qt.CTRL else ""
    alt = "alt" if modifiers & Qt.ALT else ""

    if mod_required and not (shift or ctrl or alt):
        return None

    if is_char:
        if key_str not in __ALPHANUMERICS and sys.platform.startswith("win32"):
            ctrl = None
            alt = None
        if not shift and key_str in __ALPHANUMERICS:
            key_str = key_str.lower()
        shift = None

    return "+".join([x for x in [shift, ctrl, alt, key_str] if x])
