# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging

import inject
from PySide6.QtCore import Property, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import HostIntegrationService, PlayerService, SettingsService, WindowPropertiesService

logger = logging.getLogger(__name__)

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcResizeHandler(QObject):
    _host_integration = inject.attr(HostIntegrationService)
    _player: PlayerService = inject.attr(PlayerService)
    _settings_service: SettingsService = inject.attr(SettingsService)
    _window_properties_service: WindowPropertiesService = inject.attr(WindowPropertiesService)

    headerHeightChanged = Signal(int)
    borderSizeChanged = Signal(int)
    handleWidthChanged = Signal(int)
    handleHeightChanged = Signal(int)
    tableWidthChanged = Signal(int)
    tableHeightChanged = Signal(int)

    appWindowSizeRequested = Signal(int, int)
    splitViewTableSizeRequested = Signal(int, int)

    def __init__(self, /):
        super().__init__()
        self._header_height = 0
        self._border_size = 0
        self._handle_width = 0
        self._handle_height = 0
        self._table_width = 0
        self._table_height = 0

        self._player.video_dimensions_changed.connect(self.recalculateSizes)

    @property
    def _scaled_height(self) -> int:
        if height := self._player.height:
            return int(height / self._host_integration.display_zoom_factor)
        return 0

    @property
    def _scaled_width(self) -> int:
        if width := self._player.width:
            return int(width / self._host_integration.display_zoom_factor)
        return 0

    @property
    def _available_screen_width(self) -> int:
        screen = self._window_properties_service.screen
        if not screen:
            logger.error("Primary screen is None - cannot determine available width")
            return 0
        return int(screen.geometry().width() * 0.95)

    @property
    def _available_screen_height(self) -> int:
        screen = self._window_properties_service.screen
        if not screen:
            logger.error("Primary screen is None - cannot determine available height")
            return 0
        return int(screen.geometry().height() * 0.95)

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
        if not self._can_resize():
            return

        match self._settings_service.layout_orientation:
            case Qt.Orientation.Vertical.value:
                self._recalculate_sizes_for_vertical_app_layout()
            case Qt.Orientation.Horizontal.value:
                self._recalculate_sizes_for_horizontal_app_layout()
            case _:
                msg = f"Unexpected layout orientation: {self._settings_service.layout_orientation}"
                raise ValueError(msg)

    def _can_resize(self) -> bool:
        return (
            not self._window_properties_service.is_fullscreen
            and not self._window_properties_service.is_maximized
            and self._player.video_loaded
            and self._requested_video_size_fits_on_screen()
        )

    def _requested_video_size_fits_on_screen(self) -> bool:
        fits_width = self._scaled_width < self._available_screen_width
        fits_height = self._scaled_height < self._available_screen_height
        return fits_width and fits_height

    def _recalculate_sizes_for_vertical_app_layout(self) -> None:
        window_width, window_height, table_width, table_height = calculate_vertical_layout_sizes(
            video_width=self._scaled_width,
            video_height=self._scaled_height,
            header_height=self._header_height,
            border_size=self._border_size,
            handle_height=self._handle_height,
            table_height=self._table_height,
            available_height=self._available_screen_height,
        )
        self.appWindowSizeRequested.emit(window_width, window_height)
        self.splitViewTableSizeRequested.emit(table_width, table_height)

    def _recalculate_sizes_for_horizontal_app_layout(self) -> None:
        window_width, window_height, table_width, table_height = calculate_horizontal_layout_sizes(
            video_width=self._scaled_width,
            video_height=self._scaled_height,
            header_height=self._header_height,
            border_size=self._border_size,
            handle_width=self._handle_width,
            table_width=self._table_width,
            available_width=self._available_screen_width,
        )
        self.appWindowSizeRequested.emit(window_width, window_height)
        self.splitViewTableSizeRequested.emit(table_width, table_height)


def calculate_vertical_layout_sizes(
    video_width: int,
    video_height: int,
    header_height: int,
    border_size: int,
    handle_height: int,
    table_height: int,
    available_height: int,
) -> tuple[int, int, int, int]:
    height_without_table = 2 * border_size + header_height + video_height + handle_height

    new_table_height = table_height
    while height_without_table + new_table_height > available_height:
        new_table_height -= 5

    window_width = video_width + 2 * border_size
    window_height = height_without_table + new_table_height
    table_width = video_width

    return window_width, window_height, table_width, new_table_height


def calculate_horizontal_layout_sizes(
    video_width: int,
    video_height: int,
    header_height: int,
    border_size: int,
    handle_width: int,
    table_width: int,
    available_width: int,
) -> tuple[int, int, int, int]:
    width_without_table = 2 * border_size + video_width + handle_width

    new_table_width = table_width
    while width_without_table + new_table_width > available_width:
        new_table_width -= 5

    window_width = 2 * border_size + video_width + handle_width + new_table_width
    window_height = 2 * border_size + header_height + video_height
    table_height = video_height

    return window_width, window_height, new_table_width, table_height
