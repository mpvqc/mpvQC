# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.player.services import PlayerService


def test_without_a_window_id_the_player_draws_into_the_scene(player_handle):
    PlayerService(player_handle).init()

    assert player_handle.opened_with["vo"] == "libmpv"
    assert "wid" not in player_handle.opened_with


def test_with_a_window_id_the_player_draws_into_that_window(player_handle):
    PlayerService(player_handle).init(win_id=42)

    assert player_handle.opened_with["wid"] == 42
    assert "vo" not in player_handle.opened_with


def test_log_handler_set_when_mpvqc_debug_is_set(monkeypatch, player_handle):
    monkeypatch.setenv("MPVQC_DEBUG", "1")

    PlayerService(player_handle).init()

    assert "log_handler" in player_handle.opened_with


def test_log_handler_set_when_mpvqc_player_log_is_set(monkeypatch, player_handle):
    monkeypatch.setenv("MPVQC_PLAYER_LOG", "1")

    PlayerService(player_handle).init()

    assert "log_handler" in player_handle.opened_with


def test_log_handler_not_set_when_no_env_vars(monkeypatch, player_handle):
    monkeypatch.delenv("MPVQC_DEBUG", raising=False)
    monkeypatch.delenv("MPVQC_PLAYER_LOG", raising=False)

    PlayerService(player_handle).init()

    assert "log_handler" not in player_handle.opened_with
