# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

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
    def resolved(self) -> SubtitlesResolved:
        checked = self._subtitles.checked_paths
        return SubtitlesLoad(paths=checked) if checked else SubtitlesSkip()

    @Slot()
    def _emit_tri_state_changed(self) -> None:
        self.selectAllTriStateChanged.emit(self.selectAllTriState)


def build_subtitles_step(parent: QObject, concern: SubtitlesConcern) -> MpvqcImportWizardSubtitlesStepViewModel | None:
    if isinstance(concern, SubtitlesUnresolved):
        return MpvqcImportWizardSubtitlesStepViewModel(parent, concern)
    return None
