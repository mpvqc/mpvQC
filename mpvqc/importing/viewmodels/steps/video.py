# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from PySide6.QtCore import Property, QAbstractItemModel, QObject, Signal
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import VideoConcern, VideoLoad, VideoResolved, VideoSkip, VideoUnresolved
from mpvqc.importing.models import MpvqcImportVideosModel

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardVideoStepViewModel(QObject):
    selectedIndexChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: VideoUnresolved) -> None:
        super().__init__(parent)
        self._candidates = MpvqcImportVideosModel(inputs.candidates)
        self._selected_index = 0

    @Property(QAbstractItemModel, constant=True, final=True)
    def candidates(self) -> MpvqcImportVideosModel:
        return self._candidates

    @Property(int, notify=selectedIndexChanged, final=True)
    def selectedIndex(self) -> int:
        return self._selected_index

    @selectedIndex.setter
    def selectedIndex(self, value: int) -> None:
        if self._selected_index == value:
            return
        self._selected_index = value
        self.selectedIndexChanged.emit(value)

    @property
    def resolved(self) -> VideoResolved:
        if path := self._candidates.path_at(self._selected_index):
            return VideoLoad(path=path)
        return VideoSkip()


def build_video_step(parent: QObject, concern: VideoConcern) -> MpvqcImportWizardVideoStepViewModel | None:
    if isinstance(concern, VideoUnresolved):
        return MpvqcImportWizardVideoStepViewModel(parent, concern)
    return None
