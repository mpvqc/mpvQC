# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from PySide6.QtCore import QObject
from PySide6.QtQml import QmlAttached, QmlElement

from mpvqc.controllers._attached_dialog_dimensions import DialogDimensionsAttached

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker,PyCallingNonCallable,PyArgumentList
@QmlElement
@QmlAttached(DialogDimensionsAttached)
class MpvqcShortcutDialogController(QObject):
    @staticmethod
    def qmlAttachedProperties(_, parent) -> DialogDimensionsAttached:
        return DialogDimensionsAttached(
            calculate_height=lambda h: min(1080, h * 0.70),
            parent=parent,
        )
