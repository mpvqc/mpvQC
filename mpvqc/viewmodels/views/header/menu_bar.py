# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys

import inject
from PySide6.QtCore import Property, QObject, QUrl, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.comments.services import ResetService
from mpvqc.enums import DialogKind, FileDialogKind, MessageBoxKind
from mpvqc.exporting.services import ExportService
from mpvqc.services import (
    DesktopService,
    SettingsService,
    StateService,
)

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcMenuBarViewModel(QObject):
    _desktop = inject.attr(DesktopService)
    _exporter = inject.attr(ExportService)
    _resetter = inject.attr(ResetService)
    _settings = inject.attr(SettingsService)
    _state = inject.attr(StateService)

    confirmResetRequested = Signal()

    fileDialogRequested = Signal(int)
    customExportRequested = Signal(QUrl)

    resizeVideoRequested = Signal()

    dialogRequested = Signal(int)

    messageBoxRequested = Signal(int)

    closeAppRequested = Signal()

    windowTitleFormatChanged = Signal(int)
    applicationLayoutChanged = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._settings.window_title_format_changed.connect(self.windowTitleFormatChanged)
        self._settings.layout_orientation_changed.connect(self.applicationLayoutChanged)

    @Property(bool, constant=True, final=True)
    def isUpdateMenuVisible(self) -> bool:
        return bool(os.environ.get("MPVQC_DEBUG")) or sys.platform == "win32"

    @Property(int, notify=windowTitleFormatChanged)
    def windowTitleFormat(self) -> int:
        return self._settings.window_title_format

    @Property(int, notify=applicationLayoutChanged)
    def applicationLayout(self) -> int:
        return self._settings.layout_orientation

    @Slot()
    def requestResetAppState(self) -> None:
        if self._state.saved:
            self._resetter.reset()
        else:
            self.confirmResetRequested.emit()

    @Slot()
    def requestOpenQcDocuments(self) -> None:
        self.fileDialogRequested.emit(FileDialogKind.IMPORT_DOCUMENTS)

    @Slot()
    def requestSaveQcDocument(self) -> None:
        if document := self._state.document:
            self._exporter.save(document)
        else:
            self.requestSaveQcDocumentAs()

    @Slot()
    def requestSaveQcDocumentAs(self) -> None:
        self.fileDialogRequested.emit(FileDialogKind.SAVE_DOCUMENT)

    @Slot()
    def requestExportQcDocumentClassic(self) -> None:
        self.fileDialogRequested.emit(FileDialogKind.EXPORT_CLASSIC_DOCUMENT)

    @Slot(str, QUrl)
    def requestExportQcDocumentCustom(self, _: str, exportTemplate: QUrl) -> None:
        self.customExportRequested.emit(exportTemplate)

    @Slot()
    def requestOpenVideo(self) -> None:
        self.fileDialogRequested.emit(FileDialogKind.IMPORT_VIDEO)

    @Slot()
    def requestOpenSubtitles(self) -> None:
        self.fileDialogRequested.emit(FileDialogKind.IMPORT_SUBTITLES)

    @Slot()
    def requestResizeVideo(self) -> None:
        self.resizeVideoRequested.emit()

    @Slot()
    def requestOpenAppearanceDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.APPEARANCE)

    @Slot()
    def requestOpenCommentTypesDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.COMMENT_TYPES)

    @Slot()
    def requestOpenBackupSettingsDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.BACKUP_SETTINGS)

    @Slot()
    def requestOpenExportSettingsDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.EXPORT_SETTINGS)

    @Slot()
    def requestOpenImportSettingsDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.IMPORT_SETTINGS)

    @Slot()
    def requestOpenEditMpvConfigDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.EDIT_MPV_CONFIG)

    @Slot()
    def requestOpenEditInputConfigDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.EDIT_INPUT_CONFIG)

    @Slot()
    def requestOpenCheckForUpdatesDialog(self) -> None:
        self.messageBoxRequested.emit(MessageBoxKind.VERSION_CHECK)

    @Slot()
    def requestOpenKeyboardShortcutsDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.KEYBOARD_SHORTCUTS)

    @Slot()
    def requestOpenCustomExportsDialog(self) -> None:
        self.messageBoxRequested.emit(MessageBoxKind.CUSTOM_EXPORT)

    @Slot()
    def requestOpenAboutDialog(self) -> None:
        self.dialogRequested.emit(DialogKind.ABOUT)

    @Slot()
    def openAppDataFolder(self) -> None:
        self._desktop.open_app_data_folder()

    @Slot()
    def requestClose(self) -> None:
        self.closeAppRequested.emit()

    @Slot(int)
    def configureWindowTitleFormat(self, value: int) -> None:
        self._settings.window_title_format = value

    @Slot(int)
    def configureApplicationLayout(self, value: int) -> None:
        self._settings.layout_orientation = value

    @Slot(str)
    def configureLanguage(self, value: str) -> None:
        self._settings.language = value
