# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import ExportService, ResetService, SettingsService, StateService
from mpvqc.viewmodels import MpvqcMenuBarViewModel


@pytest.fixture
def reset_service_mock() -> MagicMock:
    return MagicMock(spec_set=ResetService)


@pytest.fixture
def export_service_mock() -> MagicMock:
    return MagicMock(spec_set=ExportService)


@pytest.fixture
def view_model() -> MpvqcMenuBarViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcMenuBarViewModel()


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    reset_service_mock,
    state_service,
    settings_service,
    export_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(StateService, state_service)
        binder.bind(ResetService, reset_service_mock)
        binder.bind(SettingsService, settings_service)
        binder.bind(ExportService, export_service_mock)

    common_bindings_with(custom_bindings)


def test_request_reset_app_state(view_model, configure_state, reset_service_mock, make_spy):
    spy = make_spy(view_model.confirmResetRequested)

    configure_state(saved=True)
    view_model.requestResetAppState()
    reset_service_mock.reset.assert_called_once()
    assert spy.count() == 0

    reset_service_mock.reset.reset_mock()
    configure_state(saved=False)
    view_model.requestResetAppState()
    assert spy.count() == 1
    reset_service_mock.reset.assert_not_called()


def test_save(view_model, make_spy, configure_state, export_service_mock):
    spy = make_spy(view_model.exportPathRequested)

    configure_state(document=None)
    view_model.requestSaveQcDocumentAs()
    assert spy.count() == 1
    export_service_mock.save.assert_not_called()

    configure_state(document=None)
    view_model.requestSaveQcDocument()
    assert spy.count() == 2
    export_service_mock.save.assert_not_called()

    path = Path() / "test_document.txt"
    configure_state(document=path)
    view_model.requestSaveQcDocument()
    assert spy.count() == 2
    assert export_service_mock.save.call_count == 1
    export_service_mock.save.assert_called_with(path)

    configure_state(document=path)
    view_model.requestSaveQcDocumentAs()
    assert export_service_mock.save.call_count == 1
    assert spy.count() == 3
