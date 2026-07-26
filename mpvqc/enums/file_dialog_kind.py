# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum, auto

from PySide6.QtCore import QEnum, QObject
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcFileDialogKind(QObject):
    class FileDialogKind(IntEnum):
        EXPORT_CLASSIC_DOCUMENT = auto()
        EXPORT_CUSTOM_DOCUMENT = auto()
        IMPORT_DOCUMENTS = auto()
        IMPORT_SUBTITLES = auto()
        IMPORT_VIDEO = auto()
        SAVE_DOCUMENT = auto()

    QEnum(FileDialogKind)


FileDialogKind = MpvqcFileDialogKind.FileDialogKind
