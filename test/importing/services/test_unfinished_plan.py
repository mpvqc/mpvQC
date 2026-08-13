# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import pytest

from mpvqc.importing.services import (
    ErrorsAbsent,
    SessionMerge,
    SubtitlesSkip,
    UnfinishedPlan,
    VideoSkip,
)


def test_a_plan_with_every_concern_resolved_and_no_errors_is_refused() -> None:
    with pytest.raises(ValueError, match="unresolved concern or import errors"):
        UnfinishedPlan(
            comments=(),
            session=SessionMerge(),
            video=VideoSkip(),
            subtitles=SubtitlesSkip(),
            errors=ErrorsAbsent(),
        )
