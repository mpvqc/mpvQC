# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

from mpvqc.player.services import PlayerService


def test_terminate_is_a_noop_before_the_player_opens(player_handle):
    service = PlayerService(player_handle)
    hook = MagicMock()
    service.set_shutdown_hook(hook)

    service.terminate()

    assert not player_handle.closed
    hook.assert_not_called()


def test_terminate_closes_the_handle(player_service, player_handle):
    player_service.open_in_scene()

    player_service.terminate()

    assert player_handle.closed


def test_terminate_invokes_the_shutdown_hook(player_service):
    player_service.open_in_scene()
    hook = MagicMock()
    player_service.set_shutdown_hook(hook)

    player_service.terminate()

    hook.assert_called_once_with()


def test_terminate_invokes_the_shutdown_hook_before_closing_the_handle(player_service, player_handle):
    player_service.open_in_scene()
    closed_while_hook_ran: list[bool] = []
    player_service.set_shutdown_hook(lambda: closed_while_hook_ran.append(player_handle.closed))

    player_service.terminate()

    assert closed_while_hook_ran == [False]
    assert player_handle.closed
