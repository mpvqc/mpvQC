# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

from PySide6.QtCore import Property, QAbstractItemModel, QObject, Signal
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import video
from mpvqc.importing.models import MpvqcImportVideosModel

if TYPE_CHECKING:
    from pathlib import Path


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardVideoStepViewModel(QObject):
    selectedIndexChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: video.Unresolved) -> None:
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
    def selected_path(self) -> Path | None:
        return self._candidates.path_at(self._selected_index)


def build_video_step(parent: QObject, concern: video.Concern) -> MpvqcImportWizardVideoStepViewModel | None:
    if isinstance(concern, video.Unresolved):
        return MpvqcImportWizardVideoStepViewModel(parent, concern)
    return None


def resolve_video(video_step: MpvqcImportWizardVideoStepViewModel | None, concern: video.Concern) -> video.Resolved:
    match concern:
        case video.Load() | video.Skip():
            return concern
        case video.Unresolved() if video_step is not None:
            if path := video_step.selected_path:
                return video.Load(path=path)
            return video.Skip()
        case video.Unresolved():
            msg = "video.Unresolved reached commit without a video step view-model"
            raise RuntimeError(msg)
        case _:
            assert_never(concern)
