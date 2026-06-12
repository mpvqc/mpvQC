# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services import PlayerService


def test_reads_unrounded_time_from_mpv(player_service, mpv_mock):
    mpv_mock.time_pos = 929.340133

    assert player_service.exact_time_pos == pytest.approx(929.340133)


def test_falls_back_to_cached_when_mpv_reports_none(player_service, mpv_mock):
    mpv_mock.time_pos = None
    player_service._apply_property_update("time-pos", 929.6)

    assert player_service.exact_time_pos == pytest.approx(930.0)


def test_falls_back_to_cached_without_mpv():
    service = PlayerService()

    assert service.exact_time_pos == pytest.approx(0.0)
