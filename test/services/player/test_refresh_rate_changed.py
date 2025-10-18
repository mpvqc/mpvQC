# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.services import HostIntegrationService, PlayerService, TypeMapperService

MODULE = "mpvqc.services.player"


@pytest.fixture
def mpv_mock() -> Iterator[MagicMock]:
    with patch("mpv.MPV", return_value=MagicMock()) as mpv_mock:
        yield mpv_mock


@pytest.fixture
def player_service() -> PlayerService:
    return PlayerService()


@pytest.fixture
def host_integration_mock() -> MagicMock:
    return MagicMock(spec_set=HostIntegrationService)


@pytest.fixture(autouse=True)
def configure_inject(type_mapper, host_integration_mock) -> None:
    def config(binder: inject.Binder):
        binder.bind(TypeMapperService, type_mapper)
        binder.bind(HostIntegrationService, host_integration_mock)

    inject.configure(config, clear=True)


def test_windows(monkeypatch, player_service, mpv_mock):
    monkeypatch.setattr("sys.platform", "win32")

    player_service.init()

    assert "audio_delay" not in mpv_mock.return_value.__dict__


def test_linux_experimental_renderer_enabled(monkeypatch, player_service, mpv_mock, host_integration_mock):
    monkeypatch.setattr("sys.platform", "linux")
    host_integration_mock.refresh_rate = 60.0

    player_service.init()

    assert "audio_delay" in mpv_mock.return_value.__dict__


def test_linux_experimental_renderer_disabled(monkeypatch, player_service, mpv_mock):
    monkeypatch.setattr("sys.platform", "win32")

    player_service.init()

    assert "audio_delay" not in mpv_mock.return_value.__dict__


def test_linux_refresh_rate_changed(monkeypatch, player_service, mpv_mock, host_integration_mock):
    refresh_rate = 60.0
    monkeypatch.setattr("sys.platform", "linux")
    host_integration_mock.refresh_rate = refresh_rate

    player_service.init()

    host_integration_mock.refresh_rate_changed.connect.assert_called_once()

    callback = host_integration_mock.refresh_rate_changed.connect.call_args[0][0]
    callback(refresh_rate)

    audio_delay = mpv_mock.return_value.__dict__.get("audio_delay")
    assert audio_delay == pytest.approx((1 / refresh_rate) / 2, abs=1e-4)
