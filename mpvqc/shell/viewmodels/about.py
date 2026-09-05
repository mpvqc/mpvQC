# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys

import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlElement

from mpvqc.build import get_build_info
from mpvqc.player.services import PlayerService
from mpvqc.services import DesktopService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcAboutDialogViewModel(QObject):
    _player = inject.attr(PlayerService)
    _desktop = inject.attr(DesktopService)

    @Property(str, constant=True, final=True)
    def applicationName(self) -> str:
        return get_build_info().name

    @Property(str, constant=True, final=True)
    def applicationVersion(self) -> str:
        return get_build_info().version_label

    @Property(str, constant=True, final=True)
    def pythonVersion(self) -> str:
        return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

    @Property(str, constant=True, final=True)
    def mpvVersion(self) -> str:
        return self._player.versions.mpv

    @Property(str, constant=True, final=True)
    def ffmpegVersion(self) -> str:
        return self._player.versions.ffmpeg

    @Slot(QUrl)
    def openLink(self, link: QUrl) -> None:
        self._desktop.open_url(link)

    @Slot()
    def copyVersionInfoToClipboard(self) -> None:
        QGuiApplication.clipboard().setText(get_build_info().version_label)
