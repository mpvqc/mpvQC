# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum

import inject
from PySide6.QtCore import Property, QEnum, QObject, Signal, Slot
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
    class TimeFormat(IntEnum):
        EMPTY = 0
        CURRENT_TIME = 1
        REMAINING_TIME = 2
        CURRENT_TOTAL_TIME = 3

    @QEnum
    class ImportWhenVideoLinkedInDocument(IntEnum):
        ALWAYS = 0
        ASK_EVERY_TIME = 1
        NEVER = 2

    @QEnum
    class WindowTitleFormat(IntEnum):
        DEFAULT = 0
        FILE_NAME = 1
        FILE_PATH = 2

    # Backup
    backupEnabledChanged = Signal(bool)
    backupIntervalChanged = Signal(int)

    # Common
    languageChanged = Signal(str)
    commentTypesChanged = Signal(list)

    # Export
    nicknameChanged = Signal(str)
    writeHeaderDateChanged = Signal(bool)
    writeHeaderGeneratorChanged = Signal(bool)
    writeHeaderNicknameChanged = Signal(bool)
    writeHeaderVideoPathChanged = Signal(bool)

    # StatusBar
    statusbarPercentageChanged = Signal(bool)
    timeFormatChanged = Signal(int)

    # Import
    lastDirectoryVideoChanged = Signal(str)
    lastDirectoryDocumentsChanged = Signal(str)
    lastDirectorySubtitlesChanged = Signal(str)
    importWhenVideoLinkedInDocumentChanged = Signal(int)

    # SplitView
    layoutOrientationChanged = Signal(int)

    # Theme
    themeIdentifierChanged = Signal(str)
    themeColorOptionChanged = Signal(int)

    # Window Title
    windowTitleFormatChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Connect settings service signals to our signals for QML
        self._settings.backupEnabledChanged.connect(self.backupEnabledChanged)
        self._settings.backupIntervalChanged.connect(self.backupIntervalChanged)
        self._settings.languageChanged.connect(self.languageChanged)
        self._settings.commentTypesChanged.connect(self.commentTypesChanged)
        self._settings.nicknameChanged.connect(self.nicknameChanged)
        self._settings.writeHeaderDateChanged.connect(self.writeHeaderDateChanged)
        self._settings.writeHeaderGeneratorChanged.connect(self.writeHeaderGeneratorChanged)
        self._settings.writeHeaderNicknameChanged.connect(self.writeHeaderNicknameChanged)
        self._settings.writeHeaderVideoPathChanged.connect(self.writeHeaderVideoPathChanged)
        self._settings.statusbarPercentageChanged.connect(self.statusbarPercentageChanged)
        self._settings.timeFormatChanged.connect(self.timeFormatChanged)
        self._settings.lastDirectoryVideoChanged.connect(self.lastDirectoryVideoChanged)
        self._settings.lastDirectoryDocumentsChanged.connect(self.lastDirectoryDocumentsChanged)
        self._settings.lastDirectorySubtitlesChanged.connect(self.lastDirectorySubtitlesChanged)
        self._settings.importWhenVideoLinkedInDocumentChanged.connect(self.importWhenVideoLinkedInDocumentChanged)
        self._settings.layoutOrientationChanged.connect(self.layoutOrientationChanged)
        self._settings.themeIdentifierChanged.connect(self.themeIdentifierChanged)
        self._settings.themeColorOptionChanged.connect(self.themeColorOptionChanged)
        self._settings.windowTitleFormatChanged.connect(self.windowTitleFormatChanged)

    @Slot(result=list)
    def getDefaultCommentTypes(self) -> list[str]:
        return self._settings.get_default_comment_types()

    @Property(bool, notify=backupEnabledChanged)
    def backupEnabled(self) -> bool:
        return self._settings.backup_enabled

    @backupEnabled.setter
    def backupEnabled(self, value: bool):
        self._settings.backup_enabled = value

    @Property(int, notify=backupIntervalChanged)
    def backupInterval(self) -> int:
        return self._settings.backup_interval

    @backupInterval.setter
    def backupInterval(self, value: int):
        self._settings.backup_interval = value

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

    @Property(str, notify=nicknameChanged)
    def nickname(self) -> str:
        return self._settings.nickname

    @nickname.setter
    def nickname(self, value: str):
        self._settings.nickname = value

    @Property(bool, notify=writeHeaderDateChanged)
    def writeHeaderDate(self) -> bool:
        return self._settings.write_header_date

    @writeHeaderDate.setter
    def writeHeaderDate(self, value: bool):
        self._settings.write_header_date = value

    @Property(bool, notify=writeHeaderGeneratorChanged)
    def writeHeaderGenerator(self) -> bool:
        return self._settings.write_header_generator

    @writeHeaderGenerator.setter
    def writeHeaderGenerator(self, value: bool):
        self._settings.write_header_generator = value

    @Property(bool, notify=writeHeaderNicknameChanged)
    def writeHeaderNickname(self) -> bool:
        return self._settings.write_header_nickname

    @writeHeaderNickname.setter
    def writeHeaderNickname(self, value: bool):
        self._settings.write_header_nickname = value

    @Property(bool, notify=writeHeaderVideoPathChanged)
    def writeHeaderVideoPath(self) -> bool:
        return self._settings.write_header_video_path

    @writeHeaderVideoPath.setter
    def writeHeaderVideoPath(self, value: bool):
        self._settings.write_header_video_path = value

    @Property(bool, notify=statusbarPercentageChanged)
    def statusbarPercentage(self) -> bool:
        return self._settings.statusbar_percentage

    @statusbarPercentage.setter
    def statusbarPercentage(self, value: bool):
        self._settings.statusbar_percentage = value

    @Property(int, notify=timeFormatChanged)
    def timeFormat(self) -> int:
        return self._settings.time_format

    @timeFormat.setter
    def timeFormat(self, value: int):
        self._settings.time_format = value

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

    @Property(int, notify=importWhenVideoLinkedInDocumentChanged)
    def importWhenVideoLinkedInDocument(self) -> int:
        return self._settings.import_when_video_linked_in_document

    @importWhenVideoLinkedInDocument.setter
    def importWhenVideoLinkedInDocument(self, value: int):
        self._settings.import_when_video_linked_in_document = value

    @Property(int, notify=layoutOrientationChanged)
    def layoutOrientation(self) -> int:
        return self._settings.layout_orientation

    @layoutOrientation.setter
    def layoutOrientation(self, value: int):
        self._settings.layout_orientation = value

    @Property(str, notify=themeIdentifierChanged)
    def themeIdentifier(self) -> str:
        return self._settings.theme_identifier

    @themeIdentifier.setter
    def themeIdentifier(self, value: str):
        self._settings.theme_identifier = value

    @Property(int, notify=themeColorOptionChanged)
    def themeColorOption(self) -> int:
        return self._settings.theme_color_option

    @themeColorOption.setter
    def themeColorOption(self, value: int):
        self._settings.theme_color_option = value

    @Property(int, notify=windowTitleFormatChanged)
    def windowTitleFormat(self) -> int:
        return self._settings.window_title_format

    @windowTitleFormat.setter
    def windowTitleFormat(self, value: int):
        self._settings.window_title_format = value
