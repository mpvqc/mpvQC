# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import Qt, QUrl

from mpvqc.comments.services import ResetService
from mpvqc.exporting.services import ExportService
from mpvqc.services import DesktopService, StateService
from mpvqc.shell.enums import DialogKind, FileDialogKind, MessageBoxKind
from mpvqc.shell.services import ShellSettingsService
from mpvqc.viewmodels import MpvqcMenuBarViewModel

MODULE = "mpvqc.viewmodels.views.header.menu_bar"


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
def view_model() -> MpvqcMenuBarViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcMenuBarViewModel()


@pytest.fixture(autouse=True)
def configure_inject(
    common_bindings_with,
    reset_service_mock,
    state_service,
    shell_settings_service,
    export_service_mock,
    desktop_service_mock,
):
    def custom_bindings(binder: inject.Binder):
        binder.bind(DesktopService, desktop_service_mock)
        binder.bind(StateService, state_service)
        binder.bind(ResetService, reset_service_mock)
        binder.bind(ShellSettingsService, shell_settings_service)
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
    spy = make_spy(view_model.fileDialogRequested)

    configure_state(document=None)
    view_model.requestSaveQcDocumentAs()
    assert spy.count() == 1
    export_service_mock.save.assert_not_called()

    configure_state(document=None)
    view_model.requestSaveQcDocument()
    assert spy.count() == 2
    assert spy.at(1, 0) == FileDialogKind.SAVE_DOCUMENT
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


@pytest.mark.parametrize(
    ("request_file_dialog", "expected_kind"),
    [
        (lambda vm: vm.requestOpenQcDocuments(), FileDialogKind.IMPORT_DOCUMENTS),
        (lambda vm: vm.requestSaveQcDocumentAs(), FileDialogKind.SAVE_DOCUMENT),
        (lambda vm: vm.requestExportQcDocumentClassic(), FileDialogKind.EXPORT_CLASSIC_DOCUMENT),
        (lambda vm: vm.requestOpenVideo(), FileDialogKind.IMPORT_VIDEO),
        (lambda vm: vm.requestOpenSubtitles(), FileDialogKind.IMPORT_SUBTITLES),
    ],
)
def test_request_file_dialog(view_model, make_spy, request_file_dialog, expected_kind):
    spy = make_spy(view_model.fileDialogRequested)

    request_file_dialog(view_model)

    assert spy.count() == 1
    assert spy.at(0, 0) == expected_kind


def test_request_custom_export(view_model, make_spy):
    spy = make_spy(view_model.customExportRequested)
    template = QUrl.fromLocalFile("template.jinja")

    view_model.requestExportQcDocumentCustom("custom", template)

    assert spy.count() == 1
    assert spy.at(0, 0) == template


@pytest.mark.parametrize(
    ("request_dialog", "expected_kind"),
    [
        (lambda vm: vm.requestOpenAppearanceDialog(), DialogKind.APPEARANCE),
        (lambda vm: vm.requestOpenCommentTypesDialog(), DialogKind.COMMENT_TYPES),
        (lambda vm: vm.requestOpenBackupSettingsDialog(), DialogKind.BACKUP_SETTINGS),
        (lambda vm: vm.requestOpenExportSettingsDialog(), DialogKind.EXPORT_SETTINGS),
        (lambda vm: vm.requestOpenImportSettingsDialog(), DialogKind.IMPORT_SETTINGS),
        (lambda vm: vm.requestOpenEditMpvConfigDialog(), DialogKind.EDIT_MPV_CONFIG),
        (lambda vm: vm.requestOpenEditInputConfigDialog(), DialogKind.EDIT_INPUT_CONFIG),
        (lambda vm: vm.requestOpenKeyboardShortcutsDialog(), DialogKind.KEYBOARD_SHORTCUTS),
        (lambda vm: vm.requestOpenAboutDialog(), DialogKind.ABOUT),
    ],
)
def test_request_dialog(view_model, make_spy, request_dialog, expected_kind):
    spy = make_spy(view_model.dialogRequested)

    request_dialog(view_model)

    assert spy.count() == 1
    assert spy.at(0, 0) == expected_kind


def test_request_check_for_updates(view_model, make_spy):
    spy = make_spy(view_model.messageBoxRequested)

    view_model.requestOpenCheckForUpdatesDialog()

    assert spy.count() == 1
    assert spy.at(0, 0) == MessageBoxKind.VERSION_CHECK


def test_request_custom_exports(view_model, make_spy):
    spy = make_spy(view_model.messageBoxRequested)

    view_model.requestOpenCustomExportsDialog()

    assert spy.count() == 1
    assert spy.at(0, 0) == MessageBoxKind.CUSTOM_EXPORT


def test_open_app_data_folder(view_model, desktop_service_mock):
    view_model.openAppDataFolder()

    desktop_service_mock.open_app_data_folder.assert_called_once_with()


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
