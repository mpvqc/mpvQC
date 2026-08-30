# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

from PySide6.QtCore import Qt

_NAMED_KEYS: dict[Qt.Key, str] = {
    Qt.Key.Key_PageUp: "PGUP",
    Qt.Key.Key_PageDown: "PGDWN",
    Qt.Key.Key_Play: "PLAY",
    Qt.Key.Key_Pause: "PAUSE",
    Qt.Key.Key_Stop: "STOP",
    Qt.Key.Key_Forward: "FORWARD",
    Qt.Key.Key_Back: "REWIND",
    Qt.Key.Key_MediaPlay: "PLAY",
    Qt.Key.Key_MediaStop: "STOP",
    Qt.Key.Key_MediaNext: "NEXT",
    Qt.Key.Key_MediaPrevious: "PREV",
    Qt.Key.Key_MediaPause: "PAUSE",
    Qt.Key.Key_MediaTogglePlayPause: "PLAYPAUSE",
    Qt.Key.Key_Home: "HOME",
    Qt.Key.Key_End: "END",
    Qt.Key.Key_Escape: "ESC",
    Qt.Key.Key_Left: "LEFT",
    Qt.Key.Key_Right: "RIGHT",
    Qt.Key.Key_Up: "UP",
    Qt.Key.Key_Down: "DOWN",
    Qt.Key.Key_Backspace: "BS",
    Qt.Key.Key_Return: "ENTER",
    Qt.Key.Key_Enter: "ENTER",
    Qt.Key.Key_Space: "SPACE",
}

_CHAR_NAMES = {"#": "SHARP"}


def key_command(key: Qt.Key, modifiers: Qt.KeyboardModifier) -> str | None:
    """The mpv key name for a key press, or None when there is none to send."""
    if not key:
        return None

    shift = bool(modifiers & Qt.KeyboardModifier.ShiftModifier)
    ctrl = bool(modifiers & Qt.KeyboardModifier.ControlModifier)
    alt = bool(modifiers & Qt.KeyboardModifier.AltModifier)

    if name := _NAMED_KEYS.get(key):
        return _join(name, shift=shift, ctrl=ctrl, alt=alt)

    try:
        char = chr(key)
    except ValueError:  # Qt's non-character keys sit above the Unicode range: F1, a dead key
        return None

    # Shift never prefixes a character: Qt reports a letter key uppercase and shift picks the case,
    # and any other character already reflects it
    if char.isupper():
        return _join(char if shift else char.lower(), ctrl=ctrl, alt=alt)

    name = _CHAR_NAMES.get(char, char)
    if sys.platform == "win32" and not char.isdecimal():  # AltGr arrives as ctrl+alt beside the symbol it produced
        return name
    return _join(name, ctrl=ctrl, alt=alt)


def _join(key: str, *, shift: bool = False, ctrl: bool = False, alt: bool = False) -> str:
    held = [name for name, down in (("shift", shift), ("ctrl", ctrl), ("alt", alt)) if down]
    return "+".join([*held, key])
