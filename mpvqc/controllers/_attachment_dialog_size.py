# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
from collections.abc import Callable

from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QmlAnonymous

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlAnonymous
class DialogDimensionsAttached(QObject):
    dialogWidthChanged = Signal(int)
    dialogHeightChanged = Signal(int)

    def __init__(
        self,
        calculate_width: Callable[[int], int] = lambda x: x,
        calculate_height: Callable[[int], int] = lambda x: x,
        parent=None,
    ):
        super().__init__(parent)
        self._calculate_width = calculate_width
        self._calculate_height = calculate_height

        self._dialog_width = 0
        self._dialog_height = 0

        self._window = QGuiApplication.topLevelWindows()[0]

        self._calculate_dialog_width(self._window.width())
        self._calculate_dialog_height(self._window.height())

        self._width_connection = self._window.widthChanged.connect(lambda w: self._calculate_dialog_width(w))
        self._height_connection = self._window.heightChanged.connect(lambda h: self._calculate_dialog_height(h))

        self.destroyed.connect(lambda *_: self._on_destroyed())

    def _on_destroyed(self):
        self._window.disconnect(self._width_connection)
        self._window.disconnect(self._height_connection)

    @Property(int, notify=dialogHeightChanged)
    def dialogHeight(self) -> int:
        return self._dialog_height

    def _calculate_dialog_height(self, app_window_height: int) -> None:
        new_value = self._calculate_height(app_window_height)
        if new_value != self._dialog_height:
            self._dialog_height = new_value
            self.dialogHeightChanged.emit(new_value)

    @Property(int, notify=dialogWidthChanged)
    def dialogWidth(self) -> int:
        return self._dialog_width

    def _calculate_dialog_width(self, app_window_width: int) -> None:
        new_value = self._calculate_width(app_window_width)
        if new_value != self._dialog_width:
            self._dialog_width = new_value
            self.dialogWidthChanged.emit(new_value)
