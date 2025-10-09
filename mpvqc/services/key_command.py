# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from PySide6.QtCore import Qt

_ALPHANUMERICS = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÀÁÂÃÇÉÈÊËÍÌÎÏÑÓÒÔÕÚÙÛÝŸ"

# Mappings Qt -> MPV
_KEY_MAPPINGS = {
    Qt.Key.Key_PageUp: ("PGUP",),
    Qt.Key.Key_PageDown: ("PGDWN",),
    Qt.Key.Key_Play: ("PLAY",),
    Qt.Key.Key_Pause: ("PAUSE",),
    Qt.Key.Key_Stop: ("STOP",),
    Qt.Key.Key_Forward: ("FORWARD",),
    Qt.Key.Key_Back: ("REWIND",),
    Qt.Key.Key_MediaPlay: ("PLAY",),
    Qt.Key.Key_MediaStop: ("STOP",),
    Qt.Key.Key_MediaNext: ("NEXT",),
    Qt.Key.Key_MediaPrevious: ("PREV",),
    Qt.Key.Key_MediaPause: ("PAUSE",),
    Qt.Key.Key_MediaTogglePlayPause: ("PLAYPAUSE",),
    Qt.Key.Key_Home: ("HOME",),
    Qt.Key.Key_End: ("END",),
    Qt.Key.Key_Escape: ("ESC",),
    Qt.Key.Key_Left: ("LEFT",),
    Qt.Key.Key_Right: ("RIGHT",),
    Qt.Key.Key_Up: ("UP", True),
    Qt.Key.Key_Down: ("DOWN", True),
    Qt.Key.Key_Backspace: ("BACKSPACE", True),
    Qt.Key.Key_Return: ("ENTER", True),
    Qt.Key.Key_Enter: ("ENTER", True),
    Qt.Key.Key_Space: ("SPACE",),
    Qt.Key.Key_NumberSign: ("SHARP", False, True),
}


class KeyCommandGeneratorService:
    def generate_command(self, key: Qt.Key, modifiers: Qt.KeyboardModifier) -> str | None:
        if not key or modifiers is None:
            return None

        if key in _KEY_MAPPINGS:
            command = self._generate(modifiers, *_KEY_MAPPINGS[key])
        else:
            try:
                text = chr(key)
                command = self._generate(modifiers, text, is_char=True)
            except ValueError:
                return None

        return command

    @staticmethod
    def _generate(modifiers: Qt.KeyboardModifier, key_str, mod_required=False, is_char=False) -> str | None:
        shift = "shift" if modifiers & Qt.KeyboardModifier.ShiftModifier else ""
        ctrl = "ctrl" if modifiers & Qt.KeyboardModifier.ControlModifier else ""
        alt = "alt" if modifiers & Qt.KeyboardModifier.AltModifier else ""

        if mod_required and not (shift or ctrl or alt):
            return None

        if is_char:
            if key_str not in _ALPHANUMERICS and sys.platform.startswith("win32"):
                ctrl = None
                alt = None
            if not shift and key_str in _ALPHANUMERICS:
                key_str = key_str.lower()
            shift = None

        return "+".join([key for key in [shift, ctrl, alt, key_str] if key])
