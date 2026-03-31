# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from dataclasses import dataclass

from PySide6.QtCore import Qt

_ALPHANUMERICS = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÀÁÂÃÇÉÈÊËÍÌÎÏÑÓÒÔÕÚÙÛÝŸ"


@dataclass(frozen=True)
class KeyMapping:
    key_str: str
    mod_required: bool = False
    is_char: bool = False


# Mappings Qt -> MPV
_KEY_MAPPINGS: dict[Qt.Key, KeyMapping] = {
    Qt.Key.Key_PageUp: KeyMapping("PGUP"),
    Qt.Key.Key_PageDown: KeyMapping("PGDWN"),
    Qt.Key.Key_Play: KeyMapping("PLAY"),
    Qt.Key.Key_Pause: KeyMapping("PAUSE"),
    Qt.Key.Key_Stop: KeyMapping("STOP"),
    Qt.Key.Key_Forward: KeyMapping("FORWARD"),
    Qt.Key.Key_Back: KeyMapping("REWIND"),
    Qt.Key.Key_MediaPlay: KeyMapping("PLAY"),
    Qt.Key.Key_MediaStop: KeyMapping("STOP"),
    Qt.Key.Key_MediaNext: KeyMapping("NEXT"),
    Qt.Key.Key_MediaPrevious: KeyMapping("PREV"),
    Qt.Key.Key_MediaPause: KeyMapping("PAUSE"),
    Qt.Key.Key_MediaTogglePlayPause: KeyMapping("PLAYPAUSE"),
    Qt.Key.Key_Home: KeyMapping("HOME"),
    Qt.Key.Key_End: KeyMapping("END"),
    Qt.Key.Key_Escape: KeyMapping("ESC"),
    Qt.Key.Key_Left: KeyMapping("LEFT"),
    Qt.Key.Key_Right: KeyMapping("RIGHT"),
    Qt.Key.Key_Up: KeyMapping("UP", mod_required=True),
    Qt.Key.Key_Down: KeyMapping("DOWN", mod_required=True),
    Qt.Key.Key_Backspace: KeyMapping("BACKSPACE", mod_required=True),
    Qt.Key.Key_Return: KeyMapping("ENTER", mod_required=True),
    Qt.Key.Key_Enter: KeyMapping("ENTER", mod_required=True),
    Qt.Key.Key_Space: KeyMapping("SPACE"),
    Qt.Key.Key_NumberSign: KeyMapping("SHARP", is_char=True),
}


class KeyCommandGeneratorService:
    def generate_command(self, key: Qt.Key, modifiers: Qt.KeyboardModifier) -> str | None:
        if not key or modifiers is None:
            return None

        if key in _KEY_MAPPINGS:
            command = self._generate(modifiers, _KEY_MAPPINGS[key])
        else:
            try:
                text = chr(key)
                command = self._generate(modifiers, KeyMapping(text, is_char=True))
            except ValueError:
                return None

        return command

    @staticmethod
    def _generate(modifiers: Qt.KeyboardModifier, mapping: KeyMapping) -> str | None:
        shift = "shift" if modifiers & Qt.KeyboardModifier.ShiftModifier else ""
        ctrl = "ctrl" if modifiers & Qt.KeyboardModifier.ControlModifier else ""
        alt = "alt" if modifiers & Qt.KeyboardModifier.AltModifier else ""

        if mapping.mod_required and not (shift or ctrl or alt):
            return None

        key_str = mapping.key_str
        if mapping.is_char:
            if key_str not in _ALPHANUMERICS and sys.platform == "win32":
                ctrl = None
                alt = None
            if not shift and key_str in _ALPHANUMERICS:
                key_str = key_str.lower()
            shift = None

        return "+".join(key for key in [shift, ctrl, alt, key_str] if key)
