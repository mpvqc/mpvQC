# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .scan import RejectedDocument, ScanResult


@dataclass(frozen=True)
class ErrorsAbsent:
    pass


@dataclass(frozen=True)
class ErrorsPresent:
    rejected_documents: tuple[RejectedDocument, ...]


type ImportErrors = ErrorsAbsent | ErrorsPresent


def resolve_errors(scan: ScanResult) -> ImportErrors:
    if not scan.rejected_documents:
        return ErrorsAbsent()
    return ErrorsPresent(rejected_documents=scan.rejected_documents)
