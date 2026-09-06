# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtGui import QWindow

from mpvqc.player.services import PlayerService
from mpvqc.session import SessionService
from mpvqc.shell.services import QuitService


@pytest.fixture
def player_service_mock() -> MagicMock:
    return MagicMock(spec_set=PlayerService)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock, session_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SessionService, session_service)

    common_bindings_with(custom_bindings)


@pytest.fixture
def window(qt_app):
    window = QWindow()
    window.show()
    assert window.isVisible()
    yield window
    window.destroy()


def test_saved_document_closes_window(window, configure_session, player_service_mock, make_spy):
    configure_session(saved=True)
    service = QuitService()
    service.attach(window)
    spy = make_spy(service.confirmation_needed)

    assert window.close() is True

    assert not window.isVisible()
    player_service_mock.terminate.assert_called_once_with()
    assert spy.count() == 0


def test_unsaved_document_keeps_window_open(window, configure_session, player_service_mock, make_spy):
    configure_session(saved=False)
    service = QuitService()
    service.attach(window)
    spy = make_spy(service.confirmation_needed)

    assert window.close() is False

    assert window.isVisible()
    assert spy.count() == 1
    player_service_mock.terminate.assert_not_called()


def test_confirming_quit_closes_window_after_handler_returns(
    qt_app, window, configure_session, player_service_mock, make_spy
):
    configure_session(saved=False)
    service = QuitService()
    service.attach(window)
    spy = make_spy(service.confirmation_needed)
    assert window.close() is False

    service.quit_despite_unsaved_changes()

    assert window.isVisible()
    player_service_mock.terminate.assert_not_called()

    qt_app.processEvents()

    assert not window.isVisible()
    player_service_mock.terminate.assert_called_once_with()
    assert spy.count() == 1
