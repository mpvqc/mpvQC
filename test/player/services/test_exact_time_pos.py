# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.player.services import PlayerService


def test_reads_unrounded_time_from_the_handle(player_service, player_handle, push_property):
    push_property("time-pos", 929.340133)
    player_handle.properties["time-pos"] = 929.340133

    assert player_service.time_pos == 929
    assert player_service.exact_time_pos == pytest.approx(929.340133)


def test_falls_back_to_cached_when_the_handle_reports_no_time(player_service, player_handle, push_property):
    push_property("time-pos", 930)

    assert player_handle.properties.get("time-pos") is None
    assert player_service.exact_time_pos == pytest.approx(930.0)


def test_falls_back_to_cached_before_the_player_opens(player_handle):
    service = PlayerService(player_handle)

    assert service.exact_time_pos == pytest.approx(0.0)
