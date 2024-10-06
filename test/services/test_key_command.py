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


import unittest

from parameterized import parameterized
from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent

from mpvqc.services import KeyCommandGeneratorService


class KeyCommandTest(unittest.TestCase):
    _service = KeyCommandGeneratorService()

    @parameterized.expand(
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
            ("0", Qt.Key_0, Qt.NoModifier),
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
        ]
    )
    def test_key_command(self, expected, key, modifiers):
        event = QKeyEvent(QEvent.Type.KeyPress, key.value if key else 0, modifiers)
        command = self._service.generate_command(event.key(), event.modifiers().value)
        self.assertEqual(expected, command)
