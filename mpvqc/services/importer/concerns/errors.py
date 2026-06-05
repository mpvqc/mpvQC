# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mpvqc.datamodels import RejectedDocument
    from mpvqc.services.importer.scanner import ScanResult


@dataclass(frozen=True)
class Absent:
    pass


@dataclass(frozen=True)
class Present:
    rejected_documents: tuple[RejectedDocument, ...]


type Concern = Absent | Present


def resolve(scan: ScanResult) -> Concern:
    if not scan.rejected_documents:
        return Absent()
    return Present(rejected_documents=scan.rejected_documents)
