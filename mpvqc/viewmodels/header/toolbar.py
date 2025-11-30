# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QObject, Signal, Slot
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcToolBarViewModel(QObject):
    openNewCommentMenuRequested = Signal()

    @Slot()
    def requestNewCommentMenu(self) -> None:
        self.openNewCommentMenuRequested.emit()
