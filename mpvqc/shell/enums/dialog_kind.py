# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum, auto

from PySide6.QtCore import QEnum, QObject
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcDialogKind(QObject):
    @QEnum
    class DialogKind(IntEnum):
        ABOUT = auto()
        APPEARANCE = auto()
        BACKUP_SETTINGS = auto()
        COMMENT_TYPES = auto()
        EDIT_INPUT_CONFIG = auto()
        EDIT_MPV_CONFIG = auto()
        EXPORT_SETTINGS = auto()
        IMPORT_SETTINGS = auto()
        KEYBOARD_SHORTCUTS = auto()


DialogKind = MpvqcDialogKind.DialogKind
