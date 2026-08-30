# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from mpvqc.player.services import make_in_scene_init_args


def make_args() -> dict:
    return make_in_scene_init_args(
        config_dir=Path("config"),
        screenshot_directory=Path("screenshots"),
        audio_client_name="mpvqc",
    )


def test_log_handler_set_when_mpvqc_debug_is_set(monkeypatch):
    monkeypatch.delenv("MPVQC_PLAYER_LOG", raising=False)
    monkeypatch.setenv("MPVQC_DEBUG", "1")

    assert "log_handler" in make_args()


def test_log_handler_set_when_mpvqc_player_log_is_set(monkeypatch):
    monkeypatch.delenv("MPVQC_DEBUG", raising=False)
    monkeypatch.setenv("MPVQC_PLAYER_LOG", "1")

    assert "log_handler" in make_args()


def test_log_handler_not_set_when_no_env_vars(monkeypatch):
    monkeypatch.delenv("MPVQC_DEBUG", raising=False)
    monkeypatch.delenv("MPVQC_PLAYER_LOG", raising=False)

    assert "log_handler" not in make_args()


def test_init_args_carry_the_locations_and_the_client_name(tmp_path):
    args = make_in_scene_init_args(
        config_dir=tmp_path / "config",
        screenshot_directory=tmp_path / "screenshots",
        audio_client_name="mpvQC",
    )

    assert args["config_dir"] == str(tmp_path / "config")
    assert args["screenshot_directory"] == str(tmp_path / "screenshots")
    assert args["audio_client_name"] == "mpvQC"
