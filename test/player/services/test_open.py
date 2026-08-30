# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.player.services import PlayerService


def test_opening_in_scene_draws_into_the_scene(player_handle):
    PlayerService(player_handle).open_in_scene()

    assert player_handle.opened_with["vo"] == "libmpv"
    assert "wid" not in player_handle.opened_with


def test_opening_embedded_draws_into_the_given_window(player_handle):
    PlayerService(player_handle).open_embedded(win_id=42)

    assert player_handle.opened_with["wid"] == 42
    assert "vo" not in player_handle.opened_with


def test_opening_carries_the_init_args(player_handle):
    PlayerService(player_handle).open_in_scene()

    assert "config_dir" in player_handle.opened_with
    assert "audio_client_name" in player_handle.opened_with
