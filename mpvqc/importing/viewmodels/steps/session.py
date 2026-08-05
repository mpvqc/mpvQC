# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import assert_never

from PySide6.QtCore import Property, QObject, Signal
from PySide6.QtQml import QmlElement, QmlUncreatable

from mpvqc.importing.domain import SessionConcern, SessionMerge, SessionReplace, SessionResolved, SessionUnresolved
from mpvqc.importing.enums import MpvqcImportWizardSessionMode

QML_IMPORT_NAME = "io.github.mpvqc.mpvQC.Python"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
@QmlUncreatable("constructed by MpvqcImportWizardViewModel")
class MpvqcImportWizardSessionStepViewModel(QObject):
    modeChanged = Signal(int)

    def __init__(self, parent: QObject, inputs: SessionUnresolved) -> None:
        super().__init__(parent)
        self._incoming_comment_count = inputs.incoming_comment_count
        self._resolved: SessionResolved = SessionMerge()

    @property
    def resolved(self) -> SessionResolved:
        return self._resolved

    @resolved.setter
    def resolved(self, value: SessionResolved) -> None:
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


def build_session_step(parent: QObject, concern: SessionConcern) -> MpvqcImportWizardSessionStepViewModel | None:
    if isinstance(concern, SessionUnresolved):
        return MpvqcImportWizardSessionStepViewModel(parent, concern)
    return None


def _to_mode(resolved: SessionResolved) -> MpvqcImportWizardSessionMode.SessionMode:
    match resolved:
        case SessionMerge():
            return MpvqcImportWizardSessionMode.SessionMode.MERGE
        case SessionReplace():
            return MpvqcImportWizardSessionMode.SessionMode.REPLACE
        case _:
            assert_never(resolved)


def _to_resolved(mode: MpvqcImportWizardSessionMode.SessionMode) -> SessionResolved:
    match mode:
        case MpvqcImportWizardSessionMode.SessionMode.MERGE:
            return SessionMerge()
        case MpvqcImportWizardSessionMode.SessionMode.REPLACE:
            return SessionReplace()
        case _:
            assert_never(mode)
