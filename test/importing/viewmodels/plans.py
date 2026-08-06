# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

from mpvqc.datamodels import Comment
from mpvqc.importing.domain import (
    DocumentRejectionReason,
    ErrorsAbsent,
    ErrorsPresent,
    RejectedDocument,
    SessionMerge,
    SessionUnresolved,
    SubtitlesSkip,
    SubtitlesUnresolved,
    UnfinishedPlan,
    VideoSkip,
    VideoSource,
    VideoUnresolved,
)

VIDEO_A = Path("/movies/a.mp4")
VIDEO_B = Path("/movies/b.mp4")
SUB_A = Path("/work/a.en.srt")
SUB_B = Path("/work/b.en.srt")
COMMENT = Comment(time=0, comment_type="", comment="")

VIDEO_A_FROM_DOCUMENT = VideoSource(path=VIDEO_A, found_in_document=True)

PRESENT_ERRORS = ErrorsPresent(
    rejected_documents=(RejectedDocument(Path("/broken.qc"), DocumentRejectionReason.INVALID),)
)
UNRESOLVED_SESSION = SessionUnresolved(incoming_comment_count=1)
UNRESOLVED_VIDEO = VideoUnresolved(candidates=(VIDEO_A_FROM_DOCUMENT,))
UNRESOLVED_SUBTITLES = SubtitlesUnresolved(candidates=(SUB_A,))

ALL_RESOLVED = UnfinishedPlan(
    comments=(),
    session=SessionMerge(),
    video=VideoSkip(),
    subtitles=SubtitlesSkip(),
    errors=ErrorsAbsent(),
)

ALL_UNRESOLVED = UnfinishedPlan(
    comments=(),
    session=UNRESOLVED_SESSION,
    video=UNRESOLVED_VIDEO,
    subtitles=UNRESOLVED_SUBTITLES,
    errors=PRESENT_ERRORS,
)
