# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path

from mpvqc.importing.domain import (
    DocumentRejectionReason,
    ErrorsAbsent,
    ErrorsPresent,
    ImportErrors,
    RejectedDocument,
    SessionConcern,
    SessionMerge,
    SessionUnresolved,
    SubtitlesConcern,
    SubtitleSource,
    SubtitlesSkip,
    SubtitlesUnresolved,
    UnfinishedPlan,
    VideoConcern,
    VideoSkip,
    VideoSource,
    VideoUnresolved,
)
from mpvqc.shared import Comment

VIDEO_A = Path("/movies/a.mp4")
VIDEO_B = Path("/movies/b.mp4")
SUB_A = Path("/work/a.en.srt")
SUB_B = Path("/work/b.en.srt")
COMMENT = Comment(time=0, comment_type="", comment="")

VIDEO_A_FROM_DOCUMENT = VideoSource(path=VIDEO_A, found_in_document=True)
SUB_A_FROM_DOCUMENT = SubtitleSource(path=SUB_A, found_in_document=True)
SUB_B_FROM_DOCUMENT = SubtitleSource(path=SUB_B, found_in_document=True)

ABSENT_ERRORS = ErrorsAbsent()
MERGED_SESSION = SessionMerge()
SKIPPED_VIDEO = VideoSkip()
SKIPPED_SUBTITLES = SubtitlesSkip()

PRESENT_ERRORS = ErrorsPresent(
    rejected_documents=(RejectedDocument(Path("/broken.qc"), DocumentRejectionReason.INVALID),)
)
UNRESOLVED_SESSION = SessionUnresolved(incoming_comment_count=1)
UNRESOLVED_VIDEO = VideoUnresolved(candidates=(VIDEO_A_FROM_DOCUMENT,))
UNRESOLVED_SUBTITLES = SubtitlesUnresolved(candidates=(SUB_A,))


def plan_with(
    *,
    comments: tuple[Comment, ...] = (),
    session: SessionConcern = MERGED_SESSION,
    video: VideoConcern = SKIPPED_VIDEO,
    subtitles: SubtitlesConcern = SKIPPED_SUBTITLES,
    errors: ImportErrors = ABSENT_ERRORS,
) -> UnfinishedPlan:
    return UnfinishedPlan(comments=comments, session=session, video=video, subtitles=subtitles, errors=errors)


ALL_UNRESOLVED = plan_with(
    session=UNRESOLVED_SESSION,
    video=UNRESOLVED_VIDEO,
    subtitles=UNRESOLVED_SUBTITLES,
    errors=PRESENT_ERRORS,
)
