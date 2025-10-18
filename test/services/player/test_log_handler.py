# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


from mpvqc.services.player import PlayerService


def test_log_handler_set_when_mpvqc_debug_is_set(monkeypatch):
    monkeypatch.setenv("MPVQC_DEBUG", "1")

    service = PlayerService()

    assert "log_handler" in service._init_args


def test_log_handler_set_when_mpvqc_player_log_is_set(monkeypatch):
    monkeypatch.setenv("MPVQC_PLAYER_LOG", "1")

    service = PlayerService()

    assert "log_handler" in service._init_args


def test_log_handler_not_set_when_no_env_vars(monkeypatch):
    monkeypatch.delenv("MPVQC_DEBUG", raising=False)
    monkeypatch.delenv("MPVQC_PLAYER_LOG", raising=False)

    service = PlayerService()

    assert "log_handler" not in service._init_args
