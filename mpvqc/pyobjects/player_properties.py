# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement

from mpvqc.services import OperatingSystemZoomDetectorService, TypeMapperService
from mpvqc.services.player import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming
@QmlElement
class MpvqcMpvPlayerPropertiesPyObject(QObject):
    _zoom_detector_service = inject.attr(OperatingSystemZoomDetectorService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)

    video_loaded_changed = Signal(bool)
    path_changed = Signal(str)
    filename_changed = Signal(str)
    duration_changed = Signal(float)
    percent_pos_changed = Signal(int)
    time_pos_changed = Signal(int)
    time_remaining_changed = Signal(int)
    scaledHeightChanged = Signal(int)
    scaledWidthChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.setObjectName("mpvqcPlayerProperties")
        self._mpv_version = ""
        self._ffmpeg_version = ""

        self._path = ""
        self._filename = ""
        self._height = 0
        self._width = 0

        self._duration = None
        self._percent_pos = None
        self._time_pos = None
        self._time_remaining = None

    def init(self):
        player = inject.instance(PlayerService)

        self._mpv_version = player.mpv_version
        self._ffmpeg_version = player.ffmpeg_version

        player.observe("path", self._on_player_path_changed)
        player.observe("filename", self._on_player_filename_changed)
        player.observe("duration", self._on_player_duration_changed)
        player.observe("percent-pos", self._on_player_percent_pos_changed)
        player.observe("time-pos", self._on_player_time_pos_changed)
        player.observe("time-remaining", self._on_player_time_remaining_changed)
        player.observe("height", self._on_player_height_changed)
        player.observe("width", self._on_player_width_changed)

        def on_zoom_factor_changed(new_factor):
            self.scaledHeightChanged.emit(self._height / new_factor)
            self.scaledWidthChanged.emit(self._width / new_factor)

        self._zoom_detector_service.zoom_factor_changed.connect(on_zoom_factor_changed)

    @Property(str, constant=True)
    def mpv_version(self) -> str:
        return self._mpv_version

    @Property(str, constant=True)
    def ffmpeg_version(self) -> str:
        return self._ffmpeg_version

    @Property(bool, notify=video_loaded_changed)
    def video_loaded(self) -> bool:
        return bool(self._path)

    @Property(str, notify=path_changed)
    def path(self) -> str:
        if self._path:
            return self._type_mapper.normalize_path_str(self._path)
        return ""

    def _on_player_path_changed(self, _, value: str):
        if value and value != self._path:
            self._path = value
            self.path_changed.emit(value)
        self.video_loaded_changed.emit(bool(value))

    @Property(str, notify=filename_changed)
    def filename(self) -> str:
        return self._filename

    def _on_player_filename_changed(self, _, value: str):
        if value and value != self._filename:
            self._filename = value
            self.filename_changed.emit(value)

    @Property(float, notify=duration_changed)
    def duration(self):
        return self._duration

    def _on_player_duration_changed(self, _, value: float):
        if value:
            self._duration = value
            self.duration_changed.emit(value)

    @Property(int, notify=percent_pos_changed)
    def percent_pos(self):
        return self._percent_pos

    def _on_player_percent_pos_changed(self, _, value: float):
        if value:
            value = round(value)
            if value != self._percent_pos:
                self._percent_pos = value
                self.percent_pos_changed.emit(value)

    @Property(int, notify=time_pos_changed)
    def time_pos(self):
        return self._time_pos

    def _on_player_time_pos_changed(self, _, value: float):
        if value:
            value = round(value)
            if value != self._time_pos:
                self._time_pos = value
                self.time_pos_changed.emit(value)

    @Property(int, notify=time_remaining_changed)
    def time_remaining(self):
        return self._time_remaining

    def _on_player_time_remaining_changed(self, _, value: float):
        if value:
            value = round(value)
            if value != self._time_remaining:
                self._time_remaining = value
                self.time_remaining_changed.emit(value)

    @Property(int, notify=scaledHeightChanged)
    def scaledHeight(self):
        return self._height / self._zoom_detector_service.zoom_factor if self._height else 0

    def _on_player_height_changed(self, _, value: float):
        if value:
            value = round(value)
            if value != self._height:
                self._height = value
                self.scaledHeightChanged.emit(value)

    @Property(int, notify=scaledWidthChanged)
    def scaledWidth(self):
        return self._width / self._zoom_detector_service.zoom_factor if self._width else 0

    def _on_player_width_changed(self, _, value: float):
        if value:
            value = round(value)
            if value != self._width:
                self._width = value
                self.scaledWidthChanged.emit(value)
