# Copyright (C) 2016-2017 Frechdachs <frechdachs@rekt.cc>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QValidator

__ALPHANUMERICS = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜÀÁÂÃÇÉÈÊËÍÌÎÏÑÓÒÔÕÚÙÛÝŸ"

# Mappings Qt -> MPV
KEY_MAPPINGS = {
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

    shift = "shift" if modifiers & Qt.ShiftModifier else ""
    ctrl = "ctrl" if modifiers & Qt.ControlModifier else ""
    alt = "alt" if modifiers & Qt.AltModifier else ""

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


def replace_special_characters(string_to_replace) -> str:
    return string_to_replace \
        .replace(u'\xad', '')  # https://www.charbase.com/00ad-unicode-soft-hyphen


class SpecialCharacterValidator(QValidator):

    def validate(self, user_input: str, position: int):
        return QValidator.Acceptable, replace_special_characters(user_input), position
