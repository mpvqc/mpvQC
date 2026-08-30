# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent

from mpvqc.player.services import key_command

Modifiers = Qt.KeyboardModifier
Keys = Qt.Key


@pytest.mark.parametrize(
    ("expected", "key", "modifiers"),
    [
        (None, None, Modifiers.NoModifier),
        (None, None, Modifiers.ShiftModifier),
        (None, None, Modifiers.AltModifier),
        (None, None, Modifiers.ControlModifier),
        (None, None, Modifiers.AltModifier | Modifiers.ControlModifier | Modifiers.ShiftModifier),
        ("PGUP", Keys.Key_PageUp, Modifiers.NoModifier),
        ("HOME", Keys.Key_Home, Modifiers.NoModifier),
        ("LEFT", Keys.Key_Left, Modifiers.NoModifier),
        ("RIGHT", Keys.Key_Right, Modifiers.NoModifier),
        ("SPACE", Keys.Key_Space, Modifiers.NoModifier),
        ("shift+SPACE", Keys.Key_Space, Modifiers.ShiftModifier),
        ("ctrl+SPACE", Keys.Key_Space, Modifiers.ControlModifier),
        ("alt+SPACE", Keys.Key_Space, Modifiers.AltModifier),
        ("shift+alt+SPACE", Keys.Key_Space, Modifiers.AltModifier | Modifiers.ShiftModifier),
        ("shift+LEFT", Keys.Key_Left, Modifiers.ShiftModifier),
        ("shift+RIGHT", Keys.Key_Right, Modifiers.ShiftModifier),
        ("ctrl+LEFT", Keys.Key_Left, Modifiers.ControlModifier),
        ("ctrl+RIGHT", Keys.Key_Right, Modifiers.ControlModifier),
        ("UP", Keys.Key_Up, Modifiers.NoModifier),
        ("shift+UP", Keys.Key_Up, Modifiers.ShiftModifier),
        ("DOWN", Keys.Key_Down, Modifiers.NoModifier),
        ("ctrl+DOWN", Keys.Key_Down, Modifiers.ControlModifier),
        ("BS", Keys.Key_Backspace, Modifiers.NoModifier),
        ("alt+BS", Keys.Key_Backspace, Modifiers.AltModifier),
        ("ENTER", Keys.Key_Return, Modifiers.NoModifier),
        ("ctrl+ENTER", Keys.Key_Return, Modifiers.ControlModifier),
        ("ENTER", Keys.Key_Enter, Modifiers.NoModifier),
        (None, Keys.Key_F1, Modifiers.NoModifier),
        (None, Keys.Key_F1, Modifiers.ControlModifier),
        ("u", Keys.Key_U, Modifiers.NoModifier),
        ("U", Keys.Key_U, Modifiers.ShiftModifier),
        ("alt+u", Keys.Key_U, Modifiers.AltModifier),
        ("alt+U", Keys.Key_U, Modifiers.AltModifier | Modifiers.ShiftModifier),
        ("ctrl+u", Keys.Key_U, Modifiers.ControlModifier),
        ("ctrl+U", Keys.Key_U, Modifiers.ControlModifier | Modifiers.ShiftModifier),
        ("ctrl+alt+u", Keys.Key_U, Modifiers.ControlModifier | Modifiers.AltModifier),
        ("ctrl+alt+U", Keys.Key_U, Modifiers.AltModifier | Modifiers.ControlModifier | Modifiers.ShiftModifier),
        ("0", Keys.Key_0, Modifiers.NoModifier),
        ("ctrl+alt+0", Keys.Key_0, Modifiers.AltModifier | Modifiers.ControlModifier | Modifiers.ShiftModifier),
        ("p", Keys.Key_P, Modifiers.NoModifier),
        (".", Keys.Key_Period, Modifiers.NoModifier),
        (",", Keys.Key_Comma, Modifiers.NoModifier),
        ("9", Keys.Key_9, Modifiers.NoModifier),
        ("m", Keys.Key_M, Modifiers.NoModifier),
        ("j", Keys.Key_J, Modifiers.NoModifier),
        ("J", Keys.Key_J, Modifiers.ShiftModifier),
        ("ä", Keys.Key_Adiaeresis, Modifiers.NoModifier),
        ("Ä", Keys.Key_Adiaeresis, Modifiers.ShiftModifier),
        ("å", Keys.Key_Aring, Modifiers.NoModifier),
        ("Å", Keys.Key_Aring, Modifiers.ShiftModifier),
        ("ø", Keys.Key_Ooblique, Modifiers.NoModifier),
        ("ctrl+ø", Keys.Key_Ooblique, Modifiers.ControlModifier),
        ("ß", Keys.Key_ssharp, Modifiers.NoModifier),
        ("ß", Keys.Key_ssharp, Modifiers.ShiftModifier),
        ("SHARP", Keys.Key_NumberSign, Modifiers.NoModifier),
        ("SHARP", Keys.Key_NumberSign, Modifiers.ShiftModifier),
        ("l", Keys.Key_L, Modifiers.NoModifier),
        ("s", Keys.Key_S, Modifiers.NoModifier),
        ("S", Keys.Key_S, Modifiers.ShiftModifier),
        ("b", Keys.Key_B, Modifiers.NoModifier),
        ("i", Keys.Key_I, Modifiers.NoModifier),
    ],
)
def test_key_command(expected: str | None, key: Keys | None, modifiers: Modifiers) -> None:
    event = QKeyEvent(QEvent.Type.KeyPress, key.value if key else 0, modifiers)
    assert key_command(Keys(event.key()), event.modifiers()) == expected
