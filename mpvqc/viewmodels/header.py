# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import sys
from enum import IntEnum

import inject
from PySide6.QtCore import Property, QCoreApplication, QEnum, QObject, QUrl, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import ExportService, PlayerService, ResetService, SettingsService, StateService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcHeaderViewModel(QObject):
    _exporter: ExportService = inject.attr(ExportService)
    _state: StateService = inject.attr(StateService)
    _resetter: ResetService = inject.attr(ResetService)
    _player: PlayerService = inject.attr(PlayerService)
    _settings: SettingsService = inject.attr(SettingsService)

    class WindowTitleFormat(IntEnum):
        DEFAULT = 0
        FILE_NAME = 1
        FILE_PATH = 2

    QEnum(WindowTitleFormat)

    confirmResetRequested = Signal()
    exportPathRequested = Signal()

    openQcDocumentsRequested = Signal()
    extendedExportRequested = Signal(QUrl)

    openVideoRequested = Signal()
    openSubtitlesRequested = Signal()
    resizeVideoRequested = Signal()

    appearanceDialogRequested = Signal()
    commentTypesDialogRequested = Signal()
    backupSettingsDialogRequested = Signal()
    exportSettingsDialogRequested = Signal()
    importSettingsDialogRequested = Signal()
    editMpvConfigDialogRequested = Signal()
    editInputConfigDialogRequested = Signal()
    updateDialogRequested = Signal()
    keyboardShortcutsDialogRequested = Signal()
    extendedExportDialogRequested = Signal()
    aboutDialogRequested = Signal()

    windowDragRequested = Signal()
    minimizeAppRequested = Signal()
    toggleMaximizeAppRequested = Signal()
    closeAppRequested = Signal()

    windowTitleChanged = Signal(str)
    windowTitleFormatChanged = Signal(int)
    applicationLayoutChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._player.video_loaded_changed.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._player.path_changed.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._player.filename_changed.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._settings.windowTitleFormatChanged.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))
        self._settings.windowTitleFormatChanged.connect(lambda v: self.windowTitleFormatChanged.emit(v))
        self._settings.layoutOrientationChanged.connect(lambda v: self.applicationLayoutChanged.emit(v))
        self._state.saved_changed.connect(lambda _: self.windowTitleChanged.emit(self.windowTitle))

    @Property(bool, constant=True, final=True)
    def isWindows(self) -> bool:
        return sys.platform == "win32"

    @Property(bool, constant=True, final=True)
    def isUpdateMenuVisible(self) -> bool:
        return bool(os.environ.get("MPVQC_DEBUG")) or self.isWindows

    @Property(int, notify=windowTitleFormatChanged)
    def windowTitleFormat(self) -> int:
        return self._settings.window_title_format

    @Property(int, notify=applicationLayoutChanged)
    def applicationLayout(self) -> int:
        return self._settings.layout_orientation

    @Property(str, notify=windowTitleChanged)
    def windowTitle(self) -> str:
        window_title_format = self._settings.window_title_format

        if not self._player.video_loaded or window_title_format == self.WindowTitleFormat.DEFAULT:
            title = QCoreApplication.applicationName()
        elif window_title_format == self.WindowTitleFormat.FILE_NAME:
            title = self._player.filename or ""
        elif window_title_format == self.WindowTitleFormat.FILE_PATH:
            title = self._player.path or ""
        else:
            msg = "Cannot determine window title: configuration not known"
            raise ValueError(msg)

        if self._state.saved:
            return title

        return QCoreApplication.translate("MainWindow", "%1 (unsaved)").replace("%1", title)

    @Slot()
    def requestResetAppState(self) -> None:
        if self._state.saved:
            self._resetter.reset()
        else:
            self.confirmResetRequested.emit()

    @Slot()
    def requestOpenQcDocuments(self) -> None:
        self.openQcDocumentsRequested.emit()

    @Slot()
    def requestSaveQcDocument(self) -> None:
        if document := self._state.document:
            self._exporter.save(document)
        else:
            self.requestSaveQcDocumentAs()

    @Slot()
    def requestSaveQcDocumentAs(self) -> None:
        self.exportPathRequested.emit()

    @Slot(str, QUrl)
    def requestSaveQcDocumentExtendedUsing(self, _: str, exportTemplate: QUrl) -> None:
        self.extendedExportRequested.emit(exportTemplate)

    @Slot()
    def requestOpenVideo(self) -> None:
        self.openVideoRequested.emit()

    @Slot()
    def requestOpenSubtitles(self) -> None:
        self.openSubtitlesRequested.emit()

    @Slot()
    def requestResizeVideo(self) -> None:
        self.resizeVideoRequested.emit()

    @Slot()
    def requestOpenAppearanceDialog(self) -> None:
        self.appearanceDialogRequested.emit()

    @Slot()
    def requestOpenCommentTypesDialog(self) -> None:
        self.commentTypesDialogRequested.emit()

    @Slot()
    def requestOpenBackupSettingsDialog(self) -> None:
        self.backupSettingsDialogRequested.emit()

    @Slot()
    def requestOpenExportSettingsDialog(self) -> None:
        self.exportSettingsDialogRequested.emit()

    @Slot()
    def requestOpenImportSettingsDialog(self) -> None:
        self.importSettingsDialogRequested.emit()

    @Slot()
    def requestOpenEditMpvConfigDialog(self) -> None:
        self.editMpvConfigDialogRequested.emit()

    @Slot()
    def requestOpenEditInputConfigDialog(self) -> None:
        self.editInputConfigDialogRequested.emit()

    @Slot()
    def requestOpenCheckForUpdatesDialog(self) -> None:
        self.updateDialogRequested.emit()

    @Slot()
    def requestOpenKeyboardShortcutsDialog(self) -> None:
        self.keyboardShortcutsDialogRequested.emit()

    @Slot()
    def requestOpenExtendedExportsDialog(self) -> None:
        self.extendedExportDialogRequested.emit()

    @Slot()
    def requestOpenAboutDialog(self) -> None:
        self.aboutDialogRequested.emit()

    @Slot()
    def requestWindowDrag(self) -> None:
        self.windowDragRequested.emit()

    @Slot()
    def requestMinimize(self) -> None:
        self.minimizeAppRequested.emit()

    @Slot()
    def requestToggleMaximize(self) -> None:
        self.toggleMaximizeAppRequested.emit()

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
