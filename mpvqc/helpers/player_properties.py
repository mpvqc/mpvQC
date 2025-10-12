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

    def __init__(self):
        super().__init__()
        self.setObjectName("mpvqcPlayerProperties")

    def init(self):
        self._player.video_loaded_changed.connect(self.videoLoadedChanged)
        self._player.path_changed.connect(self._on_path_changed)
        self._player.filename_changed.connect(self.filenameChanged)
        self._player.duration_changed.connect(self.durationChanged)

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
