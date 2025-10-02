# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum

import inject
from PySide6.QtCore import Property, QEnum, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.decorators import QmlSingletonInProductionOnly
from mpvqc.services import SettingsService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
@QmlSingletonInProductionOnly
class MpvqcSettings(QObject):
    _settings: SettingsService = inject.attr(SettingsService)

    @QEnum
    class WindowTitleFormat(IntEnum):
        DEFAULT = 0
        FILE_NAME = 1
        FILE_PATH = 2

    # Common
    languageChanged = Signal(str)
    commentTypesChanged = Signal(list)

    # Import
    lastDirectoryVideoChanged = Signal(str)
    lastDirectoryDocumentsChanged = Signal(str)
    lastDirectorySubtitlesChanged = Signal(str)

    # SplitView
    layoutOrientationChanged = Signal(int)

    # Window Title
    windowTitleFormatChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Connect settings service signals to our signals for QML
        self._settings.languageChanged.connect(self.languageChanged)
        self._settings.commentTypesChanged.connect(self.commentTypesChanged)
        self._settings.lastDirectoryVideoChanged.connect(self.lastDirectoryVideoChanged)
        self._settings.lastDirectoryDocumentsChanged.connect(self.lastDirectoryDocumentsChanged)
        self._settings.lastDirectorySubtitlesChanged.connect(self.lastDirectorySubtitlesChanged)
        self._settings.layoutOrientationChanged.connect(self.layoutOrientationChanged)
        self._settings.windowTitleFormatChanged.connect(self.windowTitleFormatChanged)

    @Property(str, notify=languageChanged)
    def language(self) -> str:
        return self._settings.language

    @language.setter
    def language(self, value: str):
        self._settings.language = value

    @Property(list, notify=commentTypesChanged)
    def commentTypes(self) -> list[str]:
        return self._settings.comment_types

    @commentTypes.setter
    def commentTypes(self, value: list[str]):
        self._settings.comment_types = value

    @Property(str, notify=lastDirectoryVideoChanged)
    def lastDirectoryVideo(self) -> str:
        return self._settings.last_directory_video

    @lastDirectoryVideo.setter
    def lastDirectoryVideo(self, value: str):
        self._settings.last_directory_video = value

    @Property(str, notify=lastDirectoryDocumentsChanged)
    def lastDirectoryDocuments(self) -> str:
        return self._settings.last_directory_documents

    @lastDirectoryDocuments.setter
    def lastDirectoryDocuments(self, value: str):
        self._settings.last_directory_documents = value

    @Property(str, notify=lastDirectorySubtitlesChanged)
    def lastDirectorySubtitles(self) -> str:
        return self._settings.last_directory_subtitles

    @lastDirectorySubtitles.setter
    def lastDirectorySubtitles(self, value: str):
        self._settings.last_directory_subtitles = value

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

    @layoutOrientation.setter
    def layoutOrientation(self, value: int):
        self._settings.layout_orientation = value

    @Property(int, notify=windowTitleFormatChanged)
    def windowTitleFormat(self) -> int:
        return self._settings.window_title_format

    @windowTitleFormat.setter
    def windowTitleFormat(self, value: int):
        self._settings.window_title_format = value
