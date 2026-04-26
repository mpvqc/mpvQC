# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass

import inject
from PySide6.QtCore import Qt

from .host_integration import HostIntegrationService
from .player import PlayerService
from .settings import SettingsService
from .window_properties import WindowPropertiesService


@dataclass(frozen=True)
class ViewDimensions:
    header_height: int
    border_size: int
    handle_width: int
    handle_height: int
    table_width: int
    table_height: int


@dataclass(frozen=True)
class ResizeResult:
    window_width: int
    window_height: int
    table_width: int
    table_height: int


class VideoResizeService:
    _host_integration = inject.attr(HostIntegrationService)
    _player = inject.attr(PlayerService)
    _settings = inject.attr(SettingsService)
    _window_properties = inject.attr(WindowPropertiesService)

    def compute_resize(self, dimensions: ViewDimensions) -> ResizeResult | None:
        if self._window_properties.is_fullscreen or self._window_properties.is_maximized:
            return None
        if not self._player.video_loaded:
            return None

        video_width = self._scaled_width()
        video_height = self._scaled_height()
        available_width = self._available_screen_width()
        available_height = self._available_screen_height()

        if video_width >= available_width or video_height >= available_height:
            return None

        match self._settings.layout_orientation:
            case Qt.Orientation.Vertical.value:
                return calculate_vertical_layout_sizes(
                    video_width=video_width,
                    video_height=video_height,
                    header_height=dimensions.header_height,
                    border_size=dimensions.border_size,
                    handle_height=dimensions.handle_height,
                    table_height=dimensions.table_height,
                    available_height=available_height,
                )
            case Qt.Orientation.Horizontal.value:
                return calculate_horizontal_layout_sizes(
                    video_width=video_width,
                    video_height=video_height,
                    header_height=dimensions.header_height,
                    border_size=dimensions.border_size,
                    handle_width=dimensions.handle_width,
                    table_width=dimensions.table_width,
                    available_width=available_width,
                )
            case other:
                msg = f"Unexpected layout orientation: {other}"
                raise ValueError(msg)

    def _scaled_width(self) -> int:
        if width := self._player.width:
            return int(width / self._host_integration.display_zoom_factor)
        return 0

    def _scaled_height(self) -> int:
        if height := self._player.height:
            return int(height / self._host_integration.display_zoom_factor)
        return 0

    def _available_screen_width(self) -> int:
        return int(self._window_properties.screen_width * 0.95)

    def _available_screen_height(self) -> int:
        return int(self._window_properties.screen_height * 0.95)


def calculate_vertical_layout_sizes(
    video_width: int,
    video_height: int,
    header_height: int,
    border_size: int,
    handle_height: int,
    table_height: int,
    available_height: int,
) -> ResizeResult:
    height_without_table = 2 * border_size + header_height + video_height + handle_height
    new_table_height = max(0, min(table_height, available_height - height_without_table))

    return ResizeResult(
        window_width=video_width + 2 * border_size,
        window_height=height_without_table + new_table_height,
        table_width=video_width,
        table_height=new_table_height,
    )


def calculate_horizontal_layout_sizes(
    video_width: int,
    video_height: int,
    header_height: int,
    border_size: int,
    handle_width: int,
    table_width: int,
    available_width: int,
) -> ResizeResult:
    width_without_table = 2 * border_size + video_width + handle_width
    new_table_width = max(0, min(table_width, available_width - width_without_table))

    return ResizeResult(
        window_width=2 * border_size + video_width + handle_width + new_table_width,
        window_height=2 * border_size + header_height + video_height,
        table_width=new_table_width,
        table_height=video_height,
    )
