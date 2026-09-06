# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import Qt, QUrl

from mpvqc.appdata.services import ApplicationPathsService
from mpvqc.comments.services import ResetService
from mpvqc.exporting.services import ExportService
from mpvqc.session import SessionService
from mpvqc.shell.enums import FileDialogKind, MessageBoxKind
from mpvqc.shell.services import DesktopService, QuitService, ShellSettingsService
from mpvqc.shell.viewmodels import MpvqcShellMenuBarViewModel

MODULE = "mpvqc.shell.viewmodels.menu_bar"


@pytest.fixture
def reset_service_mock() -> MagicMock:
    return MagicMock(spec_set=ResetService)


@pytest.fixture
def export_service_mock() -> MagicMock:
    return MagicMock(spec_set=ExportService)


@pytest.fixture
def desktop_service_mock() -> MagicMock:
    return MagicMock(spec_set=DesktopService)


@pytest.fixture
def quit_service() -> QuitService:
    return QuitService()


@pytest.fixture
def view_model() -> MpvqcShellMenuBarViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcShellMenuBarViewModel()


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    reset_service_mock,
    session_service,
    shell_settings_service,
    export_service_mock,
    desktop_service_mock,
    quit_service,
    tmp_path,
):
    def custom_bindings(binder: inject.Binder):
        paths = MagicMock(spec_set=ApplicationPathsService, dir_config=tmp_path / "app data")
        binder.bind(ApplicationPathsService, paths)
        binder.bind(DesktopService, desktop_service_mock)
        binder.bind(SessionService, session_service)
        binder.bind(ResetService, reset_service_mock)
        binder.bind(ShellSettingsService, shell_settings_service)
        binder.bind(ExportService, export_service_mock)
        binder.bind(QuitService, quit_service)

    common_bindings_with(custom_bindings)


def test_request_reset_app_state(view_model, configure_session, reset_service_mock, make_spy):
    spy = make_spy(view_model.messageBoxRequested)

    configure_session(saved=True)
    view_model.requestResetAppState()
    reset_service_mock.reset.assert_called_once()
    assert spy.count() == 0

    reset_service_mock.reset.reset_mock()
    configure_session(saved=False)
    view_model.requestResetAppState()
    assert spy.count() == 1
    assert spy.at(0, 0) == MessageBoxKind.RESET
    reset_service_mock.reset.assert_not_called()


def test_request_quit_confirmation(view_model, quit_service, make_spy):
    spy = make_spy(view_model.messageBoxRequested)

    quit_service.confirmation_needed.emit()

    assert spy.count() == 1
    assert spy.at(0, 0) == MessageBoxKind.QUIT


def test_request_export_error_message_box(common_bindings_with, shell_settings_service, quit_service, make_spy):
    export_service = ExportService()

    def custom_bindings(binder: inject.Binder):
        binder.bind(ShellSettingsService, shell_settings_service)
        binder.bind(ExportService, export_service)
        binder.bind(QuitService, quit_service)

    common_bindings_with(custom_bindings)
    view_model = MpvqcShellMenuBarViewModel()
    spy = make_spy(view_model.exportErrorMessageBoxRequested)

    export_service.export_error_occurred.emit("message", 42)

    assert spy.count() == 1
    assert spy.at(0, 0) == "message"
    assert spy.at(0, 1) == 42


def test_save(view_model, make_spy, configure_session, export_service_mock):
    spy = make_spy(view_model.fileDialogRequested)

    configure_session(document=None)
    view_model.requestSaveQcDocument()
    assert spy.count() == 1
    assert spy.at(0, 0) == FileDialogKind.SAVE_DOCUMENT
    export_service_mock.save.assert_not_called()

    path = Path() / "test_document.txt"
    configure_session(document=path)
    view_model.requestSaveQcDocument()
    assert spy.count() == 1
    assert export_service_mock.save.call_count == 1
    export_service_mock.save.assert_called_with(path)


def test_open_app_data_folder(view_model, desktop_service_mock, tmp_path):
    view_model.openAppDataFolder()

    desktop_service_mock.open_url.assert_called_once_with(QUrl.fromLocalFile(str(tmp_path / "app data")))


def test_configure_layout_orientation(view_model, shell_settings_service, make_spy):
    spy = make_spy(view_model.layoutOrientationChanged)
    horizontal = Qt.Orientation.Horizontal.value

    view_model.configureLayoutOrientation(horizontal)

    assert shell_settings_service.layout_orientation == horizontal
    assert view_model.layoutOrientation == horizontal
    assert spy.count() == 1
    assert spy.at(0, 0) == horizontal


@pytest.mark.parametrize(
    ("debug_env", "offers_update_check", "expected"),
    [
        (None, False, False),
        (None, True, True),
        ("1", False, True),
        ("1", True, True),
    ],
)
def test_is_update_menu_visible(
    view_model,
    make_build_info,
    monkeypatch,
    debug_env,
    offers_update_check,
    expected,
):
    if debug_env is None:
        monkeypatch.delenv("MPVQC_DEBUG", raising=False)
    else:
        monkeypatch.setenv("MPVQC_DEBUG", debug_env)
    info = make_build_info(offers_update_check=offers_update_check)
    monkeypatch.setattr(f"{MODULE}.get_build_info", lambda: info)

    assert view_model.isUpdateMenuVisible is expected
