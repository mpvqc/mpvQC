# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock, call, patch


def test_terminate_terminates_mpv(player_service, mpv_mock):
    player_service.terminate()

    mpv_mock.terminate.assert_called_once_with()


def test_terminate_works_without_a_render_context(player_service, mpv_mock):
    assert player_service._render_context is None

    player_service.terminate()

    mpv_mock.terminate.assert_called_once_with()


def test_terminate_frees_the_render_context(player_service):
    render_context = MagicMock()
    player_service._render_context = render_context

    player_service.terminate()

    render_context.free.assert_called_once_with()


def test_terminate_clears_the_render_context_handle(player_service):
    player_service._render_context = MagicMock()

    player_service.terminate()

    assert player_service._render_context is None


def test_terminate_frees_the_render_context_before_terminating_mpv(player_service, mpv_mock):
    render_context = MagicMock()
    player_service._render_context = render_context

    parent = MagicMock()
    parent.attach_mock(render_context, "render_context")
    parent.attach_mock(mpv_mock, "mpv")

    player_service.terminate()

    assert parent.mock_calls == [
        call.render_context.free(),
        call.mpv.terminate(),
    ]


def test_create_render_context_stores_the_handle(player_service):
    sentinel = MagicMock()
    with (
        patch("mpv.MpvRenderContext", return_value=sentinel),
        patch("mpv.MpvGlGetProcAddressFn", side_effect=lambda f: f),
    ):
        result = player_service.create_render_context(get_proc_address=lambda *_: 0)

    assert result is sentinel
    assert player_service._render_context is sentinel
