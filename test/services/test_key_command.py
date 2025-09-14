# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent

from mpvqc.services import KeyCommandGeneratorService


@pytest.fixture(scope="module")
def service() -> KeyCommandGeneratorService:
    return KeyCommandGeneratorService()


# noinspection PyUnresolvedReferences, PyTypeChecker
@pytest.mark.parametrize(
    ("expected", "key", "modifiers"),
    [
        (None, None, Qt.NoModifier),
        (None, None, Qt.ShiftModifier),
        (None, None, Qt.AltModifier),
        (None, None, Qt.ControlModifier),
        (None, None, Qt.AltModifier | Qt.ControlModifier | Qt.ShiftModifier),
        ("PGUP", Qt.Key_PageUp, Qt.NoModifier),
        ("HOME", Qt.Key_Home, Qt.NoModifier),
        ("LEFT", Qt.Key_Left, Qt.NoModifier),
        ("RIGHT", Qt.Key_Right, Qt.NoModifier),
        ("SPACE", Qt.Key_Space, Qt.NoModifier),
        ("shift+SPACE", Qt.Key_Space, Qt.ShiftModifier),
        ("ctrl+SPACE", Qt.Key_Space, Qt.ControlModifier),
        ("alt+SPACE", Qt.Key_Space, Qt.AltModifier),
        ("shift+alt+SPACE", Qt.Key_Space, Qt.AltModifier | Qt.ShiftModifier),
        ("shift+LEFT", Qt.Key_Left, Qt.ShiftModifier),
        ("shift+RIGHT", Qt.Key_Right, Qt.ShiftModifier),
        ("ctrl+LEFT", Qt.Key_Left, Qt.ControlModifier),
        ("ctrl+RIGHT", Qt.Key_Right, Qt.ControlModifier),
        ("u", Qt.Key_U, Qt.NoModifier),
        ("U", Qt.Key_U, Qt.ShiftModifier),
        ("alt+u", Qt.Key_U, Qt.AltModifier),
        ("alt+U", Qt.Key_U, Qt.AltModifier | Qt.ShiftModifier),
        ("ctrl+u", Qt.Key_U, Qt.ControlModifier),
        ("ctrl+U", Qt.Key_U, Qt.ControlModifier | Qt.ShiftModifier),
        ("ctrl+alt+u", Qt.Key_U, Qt.ControlModifier | Qt.AltModifier),
        ("ctrl+alt+U", Qt.Key_U, Qt.AltModifier | Qt.ControlModifier | Qt.ShiftModifier),
        ("0", Qt.Key_0, Qt.NoModifier),
        ("ctrl+alt+0", Qt.Key_0, Qt.AltModifier | Qt.ControlModifier | Qt.ShiftModifier),
        ("p", Qt.Key_P, Qt.NoModifier),
        (".", Qt.Key_Period, Qt.NoModifier),
        (",", Qt.Key_Comma, Qt.NoModifier),
        ("9", Qt.Key_9, Qt.NoModifier),
        ("m", Qt.Key_M, Qt.NoModifier),
        ("j", Qt.Key_J, Qt.NoModifier),
        ("J", Qt.Key_J, Qt.ShiftModifier),
        ("SHARP", Qt.Key_NumberSign, Qt.NoModifier),
        ("SHARP", Qt.Key_NumberSign, Qt.ShiftModifier),
        ("l", Qt.Key_L, Qt.NoModifier),
        ("s", Qt.Key_S, Qt.NoModifier),
        ("S", Qt.Key_S, Qt.ShiftModifier),
        ("b", Qt.Key_B, Qt.NoModifier),
        ("i", Qt.Key_I, Qt.NoModifier),
    ],
)
def test_key_command(expected, key, modifiers, service):
    event = QKeyEvent(QEvent.Type.KeyPress, key.value if key else 0, modifiers)
    command = service.generate_command(event.key(), event.modifiers().value)
    assert command == expected
