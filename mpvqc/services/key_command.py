# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
import sys

from PySide6.QtCore import Qt

_ALPHANUMERICS = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÀÁÂÃÇÉÈÊËÍÌÎÏÑÓÒÔÕÚÙÛÝŸ"

# Mappings Qt -> MPV
_KEY_MAPPINGS = {
    Qt.Key_PageUp: ("PGUP",),
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
    Qt.Key_Backspace: ('BACKSPACE', True),
    Qt.Key_Return: ('ENTER', True),
    Qt.Key_Enter: ('ENTER', True),
    Qt.Key_Space: ('SPACE',),
    Qt.Key_NumberSign: ('SHARP', False, True),
}


class KeyCommandGeneratorService:

    def generate_command(self, key: int, modifiers: int) -> str or None:
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

        if command:
            return command

    @staticmethod
    def _generate(modifiers, key_str, mod_required=False, is_char=False):
        shift = "shift" if modifiers & Qt.ShiftModifier.value else ""
        ctrl = "ctrl" if modifiers & Qt.ControlModifier.value else ""
        alt = "alt" if modifiers & Qt.AltModifier.value else ""

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
