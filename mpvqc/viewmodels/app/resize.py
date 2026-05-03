# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService, VideoResizeService
from mpvqc.services.video_resize import ViewDimensions

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcResizeViewModel(QObject):
    _player = inject.attr(PlayerService)
    _resize_service = inject.attr(VideoResizeService)

    headerHeightChanged = Signal(int)
    borderSizeChanged = Signal(int)
    handleWidthChanged = Signal(int)
    handleHeightChanged = Signal(int)
    tableWidthChanged = Signal(int)
    tableHeightChanged = Signal(int)

    appWindowSizeRequested = Signal(int, int)
    splitViewTableSizeRequested = Signal(int, int)

    def __init__(self, /) -> None:
        super().__init__()
        self._header_height = 0
        self._border_size = 0
        self._handle_width = 0
        self._handle_height = 0
        self._table_width = 0
        self._table_height = 0

        self._player.video_dimensions_changed.connect(self.recalculateSizes)

    @Property(int, notify=headerHeightChanged)
    def headerHeight(self) -> int:
        return self._header_height

    @headerHeight.setter
    def headerHeight(self, value: int) -> None:
        if value != self._header_height:
            self._header_height = value
            self.headerHeightChanged.emit(value)

    @Property(int, notify=borderSizeChanged)
    def borderSize(self) -> int:
        return self._border_size

    @borderSize.setter
    def borderSize(self, value: int) -> None:
        if value != self._border_size:
            self._border_size = value
            self.borderSizeChanged.emit(value)

    @Property(int, notify=handleWidthChanged)
    def handleWidth(self) -> int:
        return self._handle_width

    @handleWidth.setter
    def handleWidth(self, value: int) -> None:
        if value != self._handle_width:
            self._handle_width = value
            self.handleWidthChanged.emit(value)

    @Property(int, notify=handleHeightChanged)
    def handleHeight(self) -> int:
        return self._handle_height

    @handleHeight.setter
    def handleHeight(self, value: int) -> None:
        if value != self._handle_height:
            self._handle_height = value
            self.handleHeightChanged.emit(value)

    @Property(int, notify=tableWidthChanged)
    def tableWidth(self) -> int:
        return self._table_width

    @tableWidth.setter
    def tableWidth(self, value: int) -> None:
        if value != self._table_width:
            self._table_width = value
            self.tableWidthChanged.emit(value)

    @Property(int, notify=tableHeightChanged)
    def tableHeight(self) -> int:
        return self._table_height

    @tableHeight.setter
    def tableHeight(self, value: int) -> None:
        if value != self._table_height:
            self._table_height = value
            self.tableHeightChanged.emit(value)

    @Slot()
    def recalculateSizes(self) -> None:
        view_dims = ViewDimensions(
            header_height=self._header_height,
            border_size=self._border_size,
            handle_width=self._handle_width,
            handle_height=self._handle_height,
            table_width=self._table_width,
            table_height=self._table_height,
        )

        result = self._resize_service.compute_resize(view_dims)
        if result is None:
            return

        self.appWindowSizeRequested.emit(result.window_width, result.window_height)
        self.splitViewTableSizeRequested.emit(result.table_width, result.table_height)
