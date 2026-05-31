# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock, call


def test_terminate_terminates_mpv(player_service, mpv_mock):
    player_service.terminate()

    mpv_mock.terminate.assert_called_once_with()


def test_terminate_invokes_the_shutdown_hook(player_service):
    hook = MagicMock()
    player_service.set_shutdown_hook(hook)

    player_service.terminate()

    hook.assert_called_once_with()


def test_terminate_invokes_the_shutdown_hook_before_terminating_mpv(player_service, mpv_mock):
    hook = MagicMock()
    player_service.set_shutdown_hook(hook)

    parent = MagicMock()
    parent.attach_mock(hook, "hook")
    parent.attach_mock(mpv_mock, "mpv")

    player_service.terminate()

    assert parent.mock_calls == [
        call.hook(),
        call.mpv.terminate(),
    ]
