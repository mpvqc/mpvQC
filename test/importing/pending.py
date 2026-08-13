# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from typing import TYPE_CHECKING, NamedTuple

from mpvqc.importing.services import PendingImport

if TYPE_CHECKING:
    from mpvqc.importing.services import FinishedPlan, UnfinishedPlan


class RecordedPending(NamedTuple):
    pending: PendingImport
    finished: list[FinishedPlan]
    dismissals: list[bool]


def record_pending(plan: UnfinishedPlan) -> RecordedPending:
    finished: list[FinishedPlan] = []
    dismissals: list[bool] = []
    pending = PendingImport(plan, on_finished=finished.append, on_dismissed=lambda: dismissals.append(True))
    return RecordedPending(pending, finished, dismissals)
