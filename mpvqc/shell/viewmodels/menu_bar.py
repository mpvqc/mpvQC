# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.build import get_build_info
from mpvqc.comments.services import ResetService
from mpvqc.exporting.services import ExportService
from mpvqc.i18n.services import I18nSettingsService
from mpvqc.services import ApplicationPathsService
from mpvqc.session import SessionService
from mpvqc.shared import map_path_to_url
from mpvqc.shell.enums import FileDialogKind, MessageBoxKind
from mpvqc.shell.services import DesktopService, QuitService, ShellSettingsService, WindowTitleFormat

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcShellMenuBarViewModel(QObject):
    _desktop = inject.attr(DesktopService)
    _exporter = inject.attr(ExportService)
    _i18n_settings = inject.attr(I18nSettingsService)
    _paths = inject.attr(ApplicationPathsService)
    _quit = inject.attr(QuitService)
    _resetter = inject.attr(ResetService)
    _settings = inject.attr(ShellSettingsService)
    _session = inject.attr(SessionService)

    fileDialogRequested = Signal(int)

    messageBoxRequested = Signal(int)
    exportErrorMessageBoxRequested = Signal(str, int)

    windowTitleFormatChanged = Signal(int)
    layoutOrientationChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings.window_title_format_changed.connect(self.windowTitleFormatChanged)
        self._settings.layout_orientation_changed.connect(self.layoutOrientationChanged)
        self._exporter.export_error_occurred.connect(self.exportErrorMessageBoxRequested)
        self._quit.confirmation_needed.connect(self._request_quit_confirmation)

    @Property(bool, constant=True, final=True)
    def isUpdateMenuVisible(self) -> bool:
        return bool(os.environ.get("MPVQC_DEBUG")) or get_build_info().offers_update_check

    @Property(int, notify=windowTitleFormatChanged)
    def windowTitleFormat(self) -> int:
        return self._settings.window_title_format

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

    @Slot()
    def requestResetAppState(self) -> None:
        if self._session.saved:
            self._resetter.reset()
        else:
            self.messageBoxRequested.emit(MessageBoxKind.RESET)

    @Slot()
    def requestSaveQcDocument(self) -> None:
        if document := self._session.document:
            self._exporter.save(document)
        else:
            self.fileDialogRequested.emit(FileDialogKind.SAVE_DOCUMENT)

    @Slot()
    def openAppDataFolder(self) -> None:
        self._desktop.open_url(map_path_to_url(self._paths.dir_config))

    @Slot(int)
    def configureWindowTitleFormat(self, value: int) -> None:
        self._settings.window_title_format = WindowTitleFormat(value)

    @Slot(int)
    def configureLayoutOrientation(self, value: int) -> None:
        self._settings.layout_orientation = value

    @Slot(str)
    def configureLanguage(self, value: str) -> None:
        self._i18n_settings.language = value

    @Slot()
    def _request_quit_confirmation(self) -> None:
        self.messageBoxRequested.emit(MessageBoxKind.QUIT)
