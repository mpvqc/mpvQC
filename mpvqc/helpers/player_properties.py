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


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcMpvPlayerPropertiesPyObject(QObject):
    _zoom_detector_service = inject.attr(OperatingSystemZoomDetectorService)
    _type_mapper: TypeMapperService = inject.attr(TypeMapperService)
    _player: PlayerService = inject.attr(PlayerService)

    videoLoadedChanged = Signal(bool)
    pathChanged = Signal(str)
    filenameChanged = Signal(str)
    durationChanged = Signal(float)
    percentPosChanged = Signal(int)
    timePosChanged = Signal(int)
    timeRemainingChanged = Signal(int)
    scaledHeightChanged = Signal(int)
    scaledWidthChanged = Signal(int)

    def __init__(self):
        super().__init__()
        self.setObjectName("mpvqcPlayerProperties")

    def init(self):
        self._player.video_loaded_changed.connect(self.videoLoadedChanged)
        self._player.path_changed.connect(self._on_path_changed)
        self._player.filename_changed.connect(self.filenameChanged)
        self._player.duration_changed.connect(self.durationChanged)
        self._player.percent_pos_changed.connect(self.percentPosChanged)
        self._player.time_pos_changed.connect(self.timePosChanged)
        self._player.time_remaining_changed.connect(self.timeRemainingChanged)
        self._player.height_changed.connect(self._on_height_changed)
        self._player.width_changed.connect(self._on_width_changed)

        self._zoom_detector_service.zoom_factor_changed.connect(self._on_zoom_factor_changed)

    @Property(bool, notify=videoLoadedChanged)
    def video_loaded(self) -> bool:
        return self._player.video_loaded

    @Property(str, notify=pathChanged)
    def path(self) -> str:
        player_path = self._player.path
        if player_path:
            return self._type_mapper.normalize_path_str(player_path)
        return ""

    def _on_path_changed(self, value: str) -> None:
        normalized_path = self._type_mapper.normalize_path_str(value) if value else ""
        self.pathChanged.emit(normalized_path)

    @Property(str, notify=filenameChanged)
    def filename(self) -> str:
        return self._player.filename or ""

    @Property(float, notify=durationChanged)
    def duration(self) -> float:
        return self._player.duration

    @Property(int, notify=percentPosChanged)
    def percent_pos(self) -> int:
        return self._player.percent_pos or 0

    @Property(int, notify=timePosChanged)
    def time_pos(self) -> int:
        return self._player.time_pos or 0

    @Property(int, notify=timeRemainingChanged)
    def time_remaining(self) -> int:
        return self._player.time_remaining or 0

    @Property(int, notify=scaledHeightChanged)
    def scaledHeight(self) -> int:
        height = self._player.height
        if height:
            return int(height / self._zoom_detector_service.zoom_factor)
        return 0

    def _on_height_changed(self, value: int) -> None:
        if value:
            scaled_value = int(value / self._zoom_detector_service.zoom_factor)
            self.scaledHeightChanged.emit(scaled_value)

    @Property(int, notify=scaledWidthChanged)
    def scaledWidth(self) -> int:
        width = self._player.width
        if width:
            return int(width / self._zoom_detector_service.zoom_factor)
        return 0

    def _on_width_changed(self, value: int) -> None:
        if value:
            scaled_value = int(value / self._zoom_detector_service.zoom_factor)
            self.scaledWidthChanged.emit(scaled_value)

    def _on_zoom_factor_changed(self, new_factor: float) -> None:
        height = self._player.height
        width = self._player.width

        if height:
            self.scaledHeightChanged.emit(int(height / new_factor))
        if width:
            self.scaledWidthChanged.emit(int(width / new_factor))
