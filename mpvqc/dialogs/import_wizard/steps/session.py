# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import assert_never

from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.enums import SessionMode
from mpvqc.services.importer import session

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardSessionStepViewModel(QObject):
    modeChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: session.Unresolved) -> None:
        super().__init__(parent)
        self._incoming_comment_count = inputs.incoming_comment_count
        self._mode = SessionMode.MERGE

    @Property(int, constant=True, final=True)
    def incomingCommentCount(self) -> int:
        return self._incoming_comment_count

    @Property(int, notify=modeChanged, final=True)
    def mode(self) -> int:
        return self._mode.value

    @mode.setter
    def mode(self, value: int) -> None:
        try:
            new_mode = SessionMode(value)
        except ValueError:
            return
        if self._mode == new_mode:
            return
        self._mode = new_mode
        self.modeChanged.emit(new_mode.value)


def build_session_step(parent: QObject, concern: session.Concern) -> MpvqcImportWizardSessionStepViewModel | None:
    if isinstance(concern, session.Unresolved):
        return MpvqcImportWizardSessionStepViewModel(parent, concern)
    return None


def resolve_session(
    session_step: MpvqcImportWizardSessionStepViewModel | None,
    concern: session.Concern,
) -> session.Resolved:
    match concern:
        case session.Merge() | session.Replace():
            return concern
        case session.Unresolved() if session_step is not None:
            return session.Replace() if session_step.mode == SessionMode.REPLACE.value else session.Merge()
        case session.Unresolved():
            msg = "session.Unresolved reached commit without a session step view-model"
            raise RuntimeError(msg)
        case _:
            assert_never(concern)
