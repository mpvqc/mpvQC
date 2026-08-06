# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scan import ScanResult


@dataclass(frozen=True)
class SessionMerge:
    pass


@dataclass(frozen=True)
class SessionReplace:
    pass


@dataclass(frozen=True)
class SessionUnresolved:
    incoming_comment_count: int


type SessionResolved = SessionMerge | SessionReplace
type SessionConcern = SessionResolved | SessionUnresolved


def resolve_session(scan: ScanResult, *, has_existing_comments: bool) -> SessionConcern:
    if has_existing_comments and scan.comments:
        return SessionUnresolved(incoming_comment_count=len(scan.comments))
    return SessionMerge()
