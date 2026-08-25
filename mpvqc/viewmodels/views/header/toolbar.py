# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from dataclasses import dataclass, replace

import inject
from PySide6.QtCore import Property, QObject, QTimer, Signal, Slot
from PySide6.QtQml import QmlElement

from mpvqc.player.services import PlayerService

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@dataclass(frozen=True)
class ToolbarInputs:
    video_loaded: bool
    audio_track_count: int
    subtitle_track_count: int


@dataclass(frozen=True)
class ToolbarProps:
    frame_step_active: bool
    subtitle_active: bool
    audio_active: bool


def derive_toolbar_props(inputs: ToolbarInputs) -> ToolbarProps:
    return ToolbarProps(
        frame_step_active=inputs.video_loaded,
        subtitle_active=inputs.video_loaded and inputs.subtitle_track_count > 0,
        audio_active=inputs.video_loaded and inputs.audio_track_count > 0,
    )


@QmlElement
class MpvqcToolBarViewModel(QObject):
    _player = inject.attr(PlayerService)

    frameStepActiveChanged = Signal(bool)
    subtitleActiveChanged = Signal(bool)
    audioActiveChanged = Signal(bool)

    _BURST_WINDOW_MS = 300

    def __init__(self, parent: QObject | None = None, *, burst_window_ms: int = _BURST_WINDOW_MS) -> None:
        super().__init__(parent)
        self._inputs = ToolbarInputs(
            video_loaded=self._player.video_loaded,
            audio_track_count=self._player.audio_track_count,
            subtitle_track_count=self._player.subtitle_track_count,
        )
        self._props = derive_toolbar_props(self._inputs)

        self._settle_timer = QTimer(self)
        self._settle_timer.setSingleShot(True)
        self._settle_timer.setInterval(burst_window_ms)
        self._settle_timer.timeout.connect(self._derive_and_emit)

        self._player.video_loaded_changed.connect(self._fold_video_loaded)
        self._player.audio_track_count_changed.connect(self._fold_audio_track_count)
        self._player.subtitle_track_count_changed.connect(self._fold_subtitle_track_count)

    @Slot(bool)
    def _fold_video_loaded(self, value: bool) -> None:
        self._apply(replace(self._inputs, video_loaded=value))

    @Slot(int)
    def _fold_audio_track_count(self, value: int) -> None:
        self._apply(replace(self._inputs, audio_track_count=value))

    @Slot(int)
    def _fold_subtitle_track_count(self, value: int) -> None:
        self._apply(replace(self._inputs, subtitle_track_count=value))

    def _apply(self, inputs: ToolbarInputs) -> None:
        self._inputs = inputs
        self._settle_timer.start()

    @Slot()
    def _derive_and_emit(self) -> None:
        new, old = derive_toolbar_props(self._inputs), self._props
        if new == old:
            return
        self._props = new
        if new.frame_step_active != old.frame_step_active:
            self.frameStepActiveChanged.emit(new.frame_step_active)
        if new.subtitle_active != old.subtitle_active:
            self.subtitleActiveChanged.emit(new.subtitle_active)
        if new.audio_active != old.audio_active:
            self.audioActiveChanged.emit(new.audio_active)

    @Property(bool, notify=frameStepActiveChanged)
    def frameStepActive(self) -> bool:
        return self._props.frame_step_active

    @Property(bool, notify=subtitleActiveChanged)
    def subtitleActive(self) -> bool:
        return self._props.subtitle_active

    @Property(bool, notify=audioActiveChanged)
    def audioActive(self) -> bool:
        return self._props.audio_active

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
