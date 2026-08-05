# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import assert_never

from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import session
from mpvqc.importing.enums import MpvqcImportWizardSessionMode

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardSessionStepViewModel(QObject):
    modeChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: session.Unresolved) -> None:
        super().__init__(parent)
        self._incoming_comment_count = inputs.incoming_comment_count
        self._resolved: session.Resolved = session.Merge()

    @property
    def resolved(self) -> session.Resolved:
        return self._resolved

    @resolved.setter
    def resolved(self, value: session.Resolved) -> None:
        if self._resolved == value:
            return
        self._resolved = value
        self.modeChanged.emit(_to_mode(value).value)

    @Property(int, constant=True, final=True)
    def incomingCommentCount(self) -> int:
        return self._incoming_comment_count

    @Property(int, notify=modeChanged, final=True)
    def mode(self) -> int:
        return _to_mode(self._resolved).value

    @mode.setter
    def mode(self, value: int) -> None:
        try:
            self.resolved = _to_resolved(MpvqcImportWizardSessionMode.SessionMode(value))
        except ValueError:
            return


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
            return session_step.resolved
        case session.Unresolved():
            msg = "session.Unresolved reached commit without a session step view-model"
            raise RuntimeError(msg)
        case _:
            assert_never(concern)


def _to_mode(resolved: session.Resolved) -> MpvqcImportWizardSessionMode.SessionMode:
    match resolved:
        case session.Merge():
            return MpvqcImportWizardSessionMode.SessionMode.MERGE
        case session.Replace():
            return MpvqcImportWizardSessionMode.SessionMode.REPLACE
        case _:
            assert_never(resolved)


def _to_resolved(mode: MpvqcImportWizardSessionMode.SessionMode) -> session.Resolved:
    match mode:
        case MpvqcImportWizardSessionMode.SessionMode.MERGE:
            return session.Merge()
        case MpvqcImportWizardSessionMode.SessionMode.REPLACE:
            return session.Replace()
        case _:
            assert_never(mode)
