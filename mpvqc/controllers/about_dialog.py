# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, QUrl, Slot
from PySide6.QtGui import QDesktopServices
from PySide6.QtQml import QmlAttached, QmlElement

from mpvqc.controllers._attachment_dialog_size import DialogDimensionsAttached
from mpvqc.services import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker,PyCallingNonCallable,PyArgumentList
@QmlElement
@QmlAttached(DialogDimensionsAttached)
class MpvqcAboutDialogControllerPyObject(QObject):
    _player: PlayerService = inject.attr(PlayerService)

    @staticmethod
    def qmlAttachedProperties(_, o) -> DialogDimensionsAttached:
        return DialogDimensionsAttached(
            calculate_height=lambda h: min(1080, h * 0.65),
            parent=o,
        )

    @Property(str, constant=True, final=True)
    def mpvVersion(self) -> str:
        return self._player.mpv_version.replace("mpv ", "")

    @Property(str, constant=True, final=True)
    def ffmpegVersion(self) -> str:
        return self._player.ffmpeg_version.replace("ffmpeg ", "")

    @Slot(QUrl)
    def openLink(self, link: QUrl) -> None:
        QDesktopServices.openUrl(link)
