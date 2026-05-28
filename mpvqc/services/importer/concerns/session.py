# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mpvqc.services.importer.scanner import ScanResult


@dataclass(frozen=True)
class Merge:
    pass


@dataclass(frozen=True)
class Replace:
    pass


@dataclass(frozen=True)
class Unresolved:
    incoming_comment_count: int


type Resolved = Merge | Replace
type Concern = Resolved | Unresolved


def resolve(scan: ScanResult, *, has_existing_comments: bool) -> Concern:
    if has_existing_comments and scan.comments:
        return Unresolved(incoming_comment_count=len(scan.comments))
    return Merge()
