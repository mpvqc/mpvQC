# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, replace

import inject
from PySide6.QtCore import Property, QCoreApplication, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.i18n.services import InternationalizationService
from mpvqc.player.services import PlayerService
from mpvqc.services import StateService
from mpvqc.shell.services import ShellSettingsService, WindowTitleFormat

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class HeaderInputs:
    video_loaded: bool
    filename: str
    path: str
    window_title_format: int
    has_unsaved_document: bool
    app_name: str
    unsaved_template: str


@dataclass(frozen=True)
class HeaderProps:
    window_title: str


def derive_header_props(inputs: HeaderInputs) -> HeaderProps:
    if not inputs.video_loaded or inputs.window_title_format == WindowTitleFormat.DEFAULT:
        title = inputs.app_name
    elif inputs.window_title_format == WindowTitleFormat.FILE_NAME:
        title = inputs.filename
    elif inputs.window_title_format == WindowTitleFormat.FILE_PATH:
        title = inputs.path
    else:
        msg = "Cannot determine window title: configuration not known"
        raise ValueError(msg)

    if not inputs.has_unsaved_document:
        return HeaderProps(window_title=title)
    return HeaderProps(window_title=inputs.unsaved_template.replace("%1", title))


@QmlElement
class MpvqcShellHeaderViewModel(QObject):
    _player = inject.attr(PlayerService)
    _settings = inject.attr(ShellSettingsService)
    _state = inject.attr(StateService)
    _i18n = inject.attr(InternationalizationService)

    windowTitleChanged = Signal(str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._inputs = HeaderInputs(
            video_loaded=self._player.video_loaded,
            filename=self._player.filename,
            path=self._player.path,
            window_title_format=self._settings.window_title_format,
            has_unsaved_document=self._state.has_unsaved_document,
            app_name=QCoreApplication.applicationName(),
            unsaved_template=self._read_unsaved_template(),
        )
        self._props = derive_header_props(self._inputs)

        self._player.video_loaded_changed.connect(self._fold_video_loaded)
        self._player.filename_changed.connect(self._fold_filename)
        self._player.path_changed.connect(self._fold_path)
        self._settings.window_title_format_changed.connect(self._fold_window_title_format)
        self._state.has_unsaved_document_changed.connect(self._fold_has_unsaved_document)
        self._i18n.retranslated.connect(self._fold_retranslated)

    @staticmethod
    def _read_unsaved_template() -> str:
        #: %1 will be the title of the application (one of: mpvQC, file name, file path)
        return QCoreApplication.translate("MainWindow", "%1 (unsaved)")

    @Slot(bool)
    def _fold_video_loaded(self, value: bool) -> None:
        self._update(replace(self._inputs, video_loaded=value))

    @Slot(str)
    def _fold_filename(self, value: str) -> None:
        self._update(replace(self._inputs, filename=value))

    @Slot(str)
    def _fold_path(self, value: str) -> None:
        self._update(replace(self._inputs, path=value))

    @Slot(int)
    def _fold_window_title_format(self, value: int) -> None:
        self._update(replace(self._inputs, window_title_format=value))

    @Slot(bool)
    def _fold_has_unsaved_document(self, value: bool) -> None:
        self._update(replace(self._inputs, has_unsaved_document=value))

    @Slot()
    def _fold_retranslated(self) -> None:
        self._update(replace(self._inputs, unsaved_template=self._read_unsaved_template()))

    def _update(self, inputs: HeaderInputs) -> None:
        self._inputs = inputs
        new, old = derive_header_props(self._inputs), self._props
        if new == old:
            return
        self._props = new
        self.windowTitleChanged.emit(new.window_title)

    @Property(str, notify=windowTitleChanged)
    def windowTitle(self) -> str:
        return self._props.window_title
