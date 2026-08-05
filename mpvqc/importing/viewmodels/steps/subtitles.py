# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, assert_never

from PySide6.QtCore import Property, QAbstractItemModel, QObject, Qt, Signal, Slot
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import (
    SubtitlesConcern,
    SubtitlesLoad,
    SubtitlesResolved,
    SubtitlesSkip,
    SubtitlesUnresolved,
)
from mpvqc.importing.models import MpvqcImportSubtitlesModel

if TYPE_CHECKING:
    from pathlib import Path


QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardSubtitlesStepViewModel(QObject):
    selectAllTriStateChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: SubtitlesUnresolved) -> None:
        super().__init__(parent)
        self._subtitles = MpvqcImportSubtitlesModel(inputs.candidates)
        self._subtitles.dataChanged.connect(self._emit_tri_state_changed)

    @Property(QAbstractItemModel, constant=True, final=True)
    def subtitles(self) -> MpvqcImportSubtitlesModel:
        return self._subtitles

    @Property(int, notify=selectAllTriStateChanged, final=True)
    def selectAllTriState(self) -> int:
        total = self._subtitles.rowCount()
        if total == 0:
            return Qt.CheckState.Checked.value

        checked = self._subtitles.checked_count
        if checked == 0:
            return Qt.CheckState.Unchecked.value
        if checked == total:
            return Qt.CheckState.Checked.value
        return Qt.CheckState.PartiallyChecked.value

    @Slot(int)
    def toggle(self, index: int) -> None:
        self._subtitles.toggle(index)

    @Slot()
    def toggleSelectAll(self) -> None:
        all_checked = self.selectAllTriState == Qt.CheckState.Checked.value
        self._subtitles.set_all_checked(not all_checked)

    @property
    def checked_paths(self) -> tuple[Path, ...]:
        return self._subtitles.checked_paths

    @Slot()
    def _emit_tri_state_changed(self) -> None:
        self.selectAllTriStateChanged.emit(self.selectAllTriState)


def build_subtitles_step(parent: QObject, concern: SubtitlesConcern) -> MpvqcImportWizardSubtitlesStepViewModel | None:
    if isinstance(concern, SubtitlesUnresolved):
        return MpvqcImportWizardSubtitlesStepViewModel(parent, concern)
    return None


def resolve_subtitles(
    subtitles_step: MpvqcImportWizardSubtitlesStepViewModel | None,
    concern: SubtitlesConcern,
) -> SubtitlesResolved:
    match concern:
        case SubtitlesLoad() | SubtitlesSkip():
            return concern
        case SubtitlesUnresolved() if subtitles_step is not None:
            checked = subtitles_step.checked_paths
            return SubtitlesLoad(paths=checked) if checked else SubtitlesSkip()
        case SubtitlesUnresolved():
            msg = "SubtitlesUnresolved reached commit without a subtitles step view-model"
            raise RuntimeError(msg)
        case _:
            assert_never(concern)
