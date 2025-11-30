# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
from PySide6.QtCore import Property, QObject, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.services import PlayerService

QML_IMPORT_NAME = "pyobjects"
QML_IMPORT_MAJOR_VERSION = 1


# noinspection PyPep8Naming,PyTypeChecker
@QmlElement
class MpvqcToolBarViewModel(QObject):
    _player: PlayerService = inject.attr(PlayerService)

    frameStepBackwardVisibleChanged = Signal(bool)
    frameStepForwardVisibleChanged = Signal(bool)
    cycleSubtitleTrackVisibleChanged = Signal(bool)
    cycleAudioTrackVisibleChanged = Signal(bool)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._frame_step_backward_visible = self._player.video_loaded
        self._frame_step_forward_visible = self._player.video_loaded
        self._cycle_subtitle_track_visible = self._should_show_cycle_subtitle()
        self._cycle_audio_track_visible = self._should_show_cycle_audio()

        self._player.video_loaded_changed.connect(self._on_video_loaded_changed)
        self._player.audio_track_count_changed.connect(self._on_audio_track_count_changed)
        self._player.subtitle_track_count_changed.connect(self._on_subtitle_track_count_changed)

    def _should_show_cycle_audio(self) -> bool:
        return self._player.video_loaded and self._player.audio_track_count > 0

    def _should_show_cycle_subtitle(self) -> bool:
        return self._player.video_loaded and self._player.subtitle_track_count > 0

    @Slot(bool)
    def _on_video_loaded_changed(self, video_loaded: bool) -> None:
        self.frameStepBackwardVisible = video_loaded
        self.frameStepForwardVisible = video_loaded
        self.cycleSubtitleTrackVisible = self._should_show_cycle_subtitle()
        self.cycleAudioTrackVisible = self._should_show_cycle_audio()

    @Slot(int)
    def _on_audio_track_count_changed(self, _: int) -> None:
        self.cycleAudioTrackVisible = self._should_show_cycle_audio()

    @Slot(int)
    def _on_subtitle_track_count_changed(self, _: int) -> None:
        self.cycleSubtitleTrackVisible = self._should_show_cycle_subtitle()

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

    @Property(bool, notify=frameStepBackwardVisibleChanged)
    def frameStepBackwardVisible(self) -> bool:
        return self._frame_step_backward_visible

    @frameStepBackwardVisible.setter
    def frameStepBackwardVisible(self, value: bool) -> None:
        if self._frame_step_backward_visible != value:
            self._frame_step_backward_visible = value
            self.frameStepBackwardVisibleChanged.emit(value)

    @Property(bool, notify=frameStepForwardVisibleChanged)
    def frameStepForwardVisible(self) -> bool:
        return self._frame_step_forward_visible

    @frameStepForwardVisible.setter
    def frameStepForwardVisible(self, value: bool) -> None:
        if self._frame_step_forward_visible != value:
            self._frame_step_forward_visible = value
            self.frameStepForwardVisibleChanged.emit(value)

    @Property(bool, notify=cycleSubtitleTrackVisibleChanged)
    def cycleSubtitleTrackVisible(self) -> bool:
        return self._cycle_subtitle_track_visible

    @cycleSubtitleTrackVisible.setter
    def cycleSubtitleTrackVisible(self, value: bool) -> None:
        if self._cycle_subtitle_track_visible != value:
            self._cycle_subtitle_track_visible = value
            self.cycleSubtitleTrackVisibleChanged.emit(value)

    @Property(bool, notify=cycleAudioTrackVisibleChanged)
    def cycleAudioTrackVisible(self) -> bool:
        return self._cycle_audio_track_visible

    @cycleAudioTrackVisible.setter
    def cycleAudioTrackVisible(self, value: bool) -> None:
        if self._cycle_audio_track_visible != value:
            self._cycle_audio_track_visible = value
            self.cycleAudioTrackVisibleChanged.emit(value)
