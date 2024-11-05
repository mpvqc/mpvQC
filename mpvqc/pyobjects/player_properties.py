# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
    heightChanged = Signal(int)
    scaledHeightChanged = Signal(int)
    widthChanged = Signal(int)
    scaledWidthChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.setObjectName("mpvqcPlayerProperties")
        self._mpv_version = ""
        self._ffmpeg_version = ""

        self._path = ""
        self._filename = ""
        self._duration = None
        self._percent_pos = None
        self._time_pos = None
        self._time_remaining = None
        self._height = None
        self._width = None

    def init(self):
        self.mpv = inject.instance(PlayerService).mpv

        self._subscribe_to_path()
        self._subscribe_to_filename()
        self._subscribe_to_duration()
        self._subscribe_to_percent_pos()
        self._subscribe_to_time_pos()
        self._subscribe_to_time_remaining()
        self._subscribe_to_height()
        self._subscribe_to_width()
        self._subscribe_to_zoom_factor_changes()

        self._mpv_version = self.mpv.mpv_version
        self._ffmpeg_version = self.mpv.ffmpeg_version

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

    def _subscribe_to_path(self):
        @self.mpv.property_observer("path")
        def observer(_, value: str):
            if value and value != self._path:
                self._path = value
                self.path_changed.emit(value)
            self.video_loaded_changed.emit(bool(value))

    @Property(str, notify=filename_changed)
    def filename(self) -> str:
        return self._filename

    def _subscribe_to_filename(self):
        @self.mpv.property_observer("filename")
        def observer(_, value: str):
            if value and value != self._filename:
                self._filename = value
                self.filename_changed.emit(value)

    @Property(float, notify=duration_changed)
    def duration(self):
        return self._duration

    def _subscribe_to_duration(self):
        @self.mpv.property_observer("duration")
        def observer(_, value: float):
            if value:
                self._duration = value
                self.duration_changed.emit(value)

    @Property(int, notify=percent_pos_changed)
    def percent_pos(self):
        return self._percent_pos

    def _subscribe_to_percent_pos(self):
        @self.mpv.property_observer("percent-pos")
        def observer(_, value: float):
            if value:
                value = round(value)
                if value != self._percent_pos:
                    self._percent_pos = value
                    self.percent_pos_changed.emit(value)

    @Property(int, notify=time_pos_changed)
    def time_pos(self):
        return self._time_pos

    def _subscribe_to_time_pos(self):
        @self.mpv.property_observer("time-pos")
        def observer(_, value: float):
            if value:
                value = round(value)
                if value != self._time_pos:
                    self._time_pos = value
                    self.time_pos_changed.emit(value)

    @Property(int, notify=time_remaining_changed)
    def time_remaining(self):
        return self._time_remaining

    def _subscribe_to_time_remaining(self):
        @self.mpv.property_observer("time-remaining")
        def observer(_, value: float):
            if value:
                value = round(value)
                if value != self._time_remaining:
                    self._time_remaining = value
                    self.time_remaining_changed.emit(value)

    @Property(int, notify=heightChanged)
    def height(self):
        return self._height or 0

    @Property(int, notify=scaledHeightChanged)
    def scaledHeight(self):
        return self._height / self._zoom_detector_service.zoom_factor if self._height else 0

    def _subscribe_to_height(self):
        @self.mpv.property_observer("height")
        def observer(_, value: float):
            if value:
                value = round(value)
                if value != self._height:
                    self._height = value
                    self.heightChanged.emit(value)
                    self.scaledHeightChanged.emit(value)

    @Property(int, notify=widthChanged)
    def width(self):
        return self._width or 0

    @Property(int, notify=scaledWidthChanged)
    def scaledWidth(self):
        return self._width / self._zoom_detector_service.zoom_factor if self._width else 0

    def _subscribe_to_width(self):
        @self.mpv.property_observer("width")
        def observer(_, value: float):
            if value:
                value = round(value)
                if value != self._width:
                    self._width = value
                    self.widthChanged.emit(value)
                    self.scaledWidthChanged.emit(value)

    def _subscribe_to_zoom_factor_changes(self):
        def on_change(new_factor):
            self.scaledHeightChanged.emit(self.height / new_factor)
            self.scaledWidthChanged.emit(self.width / new_factor)

        self._zoom_detector_service.zoom_factor_changed.connect(on_change)
