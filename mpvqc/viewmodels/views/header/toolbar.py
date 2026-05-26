# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import inject
from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class MpvqcToolBarViewModel(QObject):
    _player = inject.attr(PlayerService)

    frameStepActiveChanged = Signal(bool)
    subtitleActiveChanged = Signal(bool)
    audioActiveChanged = Signal(bool)

    _BURST_WINDOW_MS = 300

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._frame_step_active = False
        self._subtitle_active = False
        self._audio_active = False

        self._refresh_timer = QTimer(self)
        self._refresh_timer.setSingleShot(True)
        self._refresh_timer.setInterval(self._BURST_WINDOW_MS)
        self._refresh_timer.timeout.connect(self._refresh)

        self._player.video_loaded_changed.connect(self._schedule_refresh)
        self._player.audio_track_count_changed.connect(self._schedule_refresh)
        self._player.subtitle_track_count_changed.connect(self._schedule_refresh)
        self._player.file_loaded.connect(self._schedule_refresh)

    @Slot()
    def _schedule_refresh(self) -> None:
        self._refresh_timer.start()

    @Slot()
    def _refresh(self) -> None:
        video_loaded = self._player.video_loaded
        if video_loaded:
            # pyrefly: ignore [bad-assignment]
            self.frameStepActive = True

        # pyrefly: ignore [bad-assignment, unsupported-operation]
        self.subtitleActive = video_loaded and self._player.subtitle_track_count > 0
        # pyrefly: ignore [bad-assignment, unsupported-operation]
        self.audioActive = video_loaded and self._player.audio_track_count > 0

    @Property(bool, notify=frameStepActiveChanged)
    def frameStepActive(self) -> bool:
        return self._frame_step_active

    @frameStepActive.setter
    def frameStepActive(self, value: bool) -> None:
        if self._frame_step_active != value:
            self._frame_step_active = value
            self.frameStepActiveChanged.emit(value)

    @Property(bool, notify=subtitleActiveChanged)
    def subtitleActive(self) -> bool:
        return self._subtitle_active

    @subtitleActive.setter
    def subtitleActive(self, value: bool) -> None:
        if self._subtitle_active != value:
            self._subtitle_active = value
            self.subtitleActiveChanged.emit(value)

    @Property(bool, notify=audioActiveChanged)
    def audioActive(self) -> bool:
        return self._audio_active

    @audioActive.setter
    def audioActive(self, value: bool) -> None:
        if self._audio_active != value:
            self._audio_active = value
            self.audioActiveChanged.emit(value)

    @Slot()
    def requestFrameStepBackward(self) -> None:
        self._player.frame_step_backward()

    @Slot()
    def requestFrameStepForward(self) -> None:
        self._player.frame_step_forward()

    @Slot()
    def requestCycleSubtitleTrack(self) -> None:
        self._player.cycle_subtitle_track()

    @Slot()
    def requestCycleAudioTrack(self) -> None:
        self._player.cycle_audio_track()
