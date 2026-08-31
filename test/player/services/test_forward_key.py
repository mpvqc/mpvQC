# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import Qt

from mpvqc.player.services import PlayerService


def test_forwarding_a_translatable_key_sends_keypress(player_handle):
    service = PlayerService(player_handle)

    service.forward_key(Qt.Key.Key_Space, Qt.KeyboardModifier.NoModifier)

    assert player_handle.async_commands == [("keypress", "SPACE")]


def test_forwarding_an_untranslatable_key_sends_nothing(player_handle):
    service = PlayerService(player_handle)

    service.forward_key(Qt.Key.Key_F1, Qt.KeyboardModifier.NoModifier)

    assert player_handle.async_commands == []
