# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum

from PySide6.QtCore import QEnum, QObject
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcTimeFormat(QObject):
    class TimeFormat(IntEnum):
        EMPTY = 0
        CURRENT_TIME = 1
        REMAINING_TIME = 2
        CURRENT_TOTAL_TIME = 3

    QEnum(TimeFormat)
