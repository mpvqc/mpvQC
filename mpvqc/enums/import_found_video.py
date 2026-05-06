# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum

from PySide6.QtCore import QEnum, QObject
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcImportFoundVideo(QObject):
    class ImportFoundVideo(IntEnum):
        ALWAYS = 0
        ASK_EVERY_TIME = 1
        NEVER = 2

    QEnum(ImportFoundVideo)


ImportFoundVideo = MpvqcImportFoundVideo.ImportFoundVideo
