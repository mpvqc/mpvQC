# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.services import ExportService, QuitService
from mpvqc.viewmodels import MpvqcMessageBoxRequestRelayViewModel


@pytest.fixture
def export_service() -> ExportService:
    return ExportService()


@pytest.fixture
def quit_service() -> QuitService:
    return QuitService()


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, export_service, quit_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ExportService, export_service)
        binder.bind(QuitService, quit_service)

    common_bindings_with(custom_bindings)


def test_relays_export_errors(export_service, make_spy):
    view_model = MpvqcMessageBoxRequestRelayViewModel()
    spy = make_spy(view_model.exportErrorOccurred)

    export_service.export_error_occurred.emit("message", 42)

    assert spy.count() == 1
    assert spy.at(0, 0) == "message"
    assert spy.at(0, 1) == 42


def test_relays_quit_confirmation(quit_service, make_spy):
    view_model = MpvqcMessageBoxRequestRelayViewModel()
    spy = make_spy(view_model.confirmQuit)

    quit_service.request_quit()

    assert spy.count() == 1
