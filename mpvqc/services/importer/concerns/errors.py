# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

    from mpvqc.services.importer.scanner import ScanResult


@dataclass(frozen=True)
class Absent:
    pass


@dataclass(frozen=True)
class Unresolved:
    invalid_documents: tuple[Path, ...]


type Resolved = Absent
type Concern = Resolved | Unresolved


def resolve(scan: ScanResult) -> Concern:
    if not scan.invalid_documents:
        return Absent()
    return Unresolved(invalid_documents=scan.invalid_documents)
