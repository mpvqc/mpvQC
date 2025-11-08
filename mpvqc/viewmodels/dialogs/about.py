# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtGui import QDesktopServices, QGuiApplication
from PySide6.QtQml import QmlElement

from mpvqc.services import BuildInfoService, PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker,PyCallingNonCallable,PyArgumentList
@QmlElement
class MpvqcAboutDialogViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)
    _build_info: BuildInfoService = inject.attr(BuildInfoService)

    @Property(str, constant=True, final=True)
    def applicationName(self):
        return self._build_info.name

    @Property(str, constant=True, final=True)
    def applicationVersion(self):
        return self._build_info.combined_version_info

    @Property(str, constant=True, final=True)
    def pythonVersion(self) -> str:
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    @Property(str, constant=True, final=True)
    def mpvVersion(self) -> str:
        return self._player.mpv_version.replace("mpv ", "")

    @Property(str, constant=True, final=True)
    def ffmpegVersion(self) -> str:
        return self._player.ffmpeg_version.replace("ffmpeg ", "")

    @Slot(QUrl)
    def openLink(self, link: QUrl) -> None:
        QDesktopServices.openUrl(link)

    @Slot()
    def copyVersionInfoToClipboard(self) -> None:
        QGuiApplication.clipboard().setText(self.applicationVersion)
