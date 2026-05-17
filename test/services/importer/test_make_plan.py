# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

import pytest

from mpvqc.datamodels import Comment, SubtitleSource, VideoSource
from mpvqc.enums import ImportFoundVideo
from mpvqc.services.importer import (
    FinishedPlan,
    ScanResult,
    UnfinishedPlan,
    make_plan,
)
from mpvqc.services.importer.concerns import errors, session, subtitles, video

if TYPE_CHECKING:
    from collections.abc import Sequence


DOC_A = Path("/work/a.qc")
DOC_B = Path("/work/b.qc")
DOC_BROKEN = Path("/work/broken.qc")
VIDEO_A = Path("/movies/a.mp4")
VIDEO_B = Path("/movies/b.mkv")
VIDEO_C = Path("/movies/c.avi")
VIDEO_D = Path("/movies/d.mov")
SUB_A = Path("/work/a.en.srt")
SUB_B = Path("/work/a.ja.srt")


# VideoSource shorthand for the shapes used in scenarios.
VID_A_DOC = VideoSource(path=VIDEO_A, found_in_document=True)
VID_B_DOC = VideoSource(path=VIDEO_B, found_in_document=True)
VID_C_DOC = VideoSource(path=VIDEO_C, found_in_document=True)
VID_D_DOC = VideoSource(path=VIDEO_D, found_in_document=True)
VID_A_EXPLICIT = VideoSource(path=VIDEO_A, explicitly_provided=True)
VID_B_EXPLICIT = VideoSource(path=VIDEO_B, explicitly_provided=True)
VID_A_EXPLICIT_DOC = VideoSource(path=VIDEO_A, explicitly_provided=True, found_in_document=True)
VID_A_SUB = VideoSource(path=VIDEO_A, found_in_subtitle=True)
VID_B_SUB = VideoSource(path=VIDEO_B, found_in_subtitle=True)

# SubtitleSource shorthand for the shapes used in scenarios.
SUB_A_DOC = SubtitleSource(path=SUB_A, found_in_document=True)
SUB_B_DOC = SubtitleSource(path=SUB_B, found_in_document=True)
SUB_A_EXPLICIT = SubtitleSource(path=SUB_A, explicitly_provided=True)
SUB_B_EXPLICIT = SubtitleSource(path=SUB_B, explicitly_provided=True)
SUB_A_EXPLICIT_DOC = SubtitleSource(path=SUB_A, explicitly_provided=True, found_in_document=True)


def stub_comments(count: int) -> tuple[Comment, ...]:
    return tuple(Comment(time=0, comment_type="", comment="") for _ in range(count))


def make_scan(
    *,
    videos: Sequence[Path | VideoSource] = (),
    subtitles: Sequence[Path | SubtitleSource] = (),
    comment_count: int = 0,
    valid_docs: Sequence[Path] = (),
    invalid_docs: Sequence[Path] = (),
) -> ScanResult:
    def _coerce_video(v: Path | VideoSource) -> VideoSource:
        if isinstance(v, VideoSource):
            return v
        return VideoSource(path=v, found_in_document=True)

    def _coerce_subtitle(s: Path | SubtitleSource) -> SubtitleSource:
        if isinstance(s, SubtitleSource):
            return s
        return SubtitleSource(path=s, found_in_document=True)

    return ScanResult(
        videos=tuple(_coerce_video(v) for v in videos),
        subtitles=tuple(_coerce_subtitle(s) for s in subtitles),
        comments=stub_comments(comment_count),
        valid_documents=tuple(valid_docs),
        invalid_documents=tuple(invalid_docs),
    )


class Scenario(NamedTuple):
    name: str
    scan: ScanResult
    expected: FinishedPlan | UnfinishedPlan
    found_video_setting: ImportFoundVideo = ImportFoundVideo.ASK_EVERY_TIME
    has_existing_comments: bool = False
    any_candidate_loaded: bool = False


def assert_plan_matches(scenario: Scenario) -> None:
    actual = make_plan(
        scenario.scan,
        found_video_setting=scenario.found_video_setting,
        has_existing_comments=scenario.has_existing_comments,
        any_candidate_loaded=scenario.any_candidate_loaded,
    )
    assert actual == scenario.expected


SIMPLE_DOCUMENT_IMPORTS = [
    Scenario(
        name="doc with video, ALWAYS",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        found_video_setting=ImportFoundVideo.ALWAYS,
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="doc with video, ALWAYS, with subs",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A], comment_count=3),
        found_video_setting=ImportFoundVideo.ALWAYS,
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
    Scenario(
        name="doc with video, ASK, no subs",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_DOC,)),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, ASK, with subs",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A], comment_count=3),
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_DOC,)),
            subtitles=subtitles.Unresolved(candidates=(SUB_A,)),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, NEVER",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        found_video_setting=ImportFoundVideo.NEVER,
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="doc with video, NEVER, with subs",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A], comment_count=3),
        found_video_setting=ImportFoundVideo.NEVER,
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="doc with comments only",
        scan=make_scan(valid_docs=[DOC_A], comment_count=3),
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="doc with video + 2 doc-derived subs, ASK",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A, SUB_B], comment_count=3),
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_DOC,)),
            subtitles=subtitles.Unresolved(candidates=(SUB_A, SUB_B)),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with 2 doc-derived subs, no video, subs dropped",
        scan=make_scan(valid_docs=[DOC_A], subtitles=[SUB_A, SUB_B], comment_count=3),
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
        ),
    ),
]


@pytest.mark.parametrize("scenario", SIMPLE_DOCUMENT_IMPORTS, ids=lambda s: s.name)
def test_simple_document_imports(scenario: Scenario) -> None:
    assert_plan_matches(scenario)


EXPLICIT_RESOURCE_IMPORTS = [
    Scenario(
        name="explicit video, ALWAYS",
        scan=make_scan(videos=[VID_A_EXPLICIT]),
        found_video_setting=ImportFoundVideo.ALWAYS,
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="explicit video, ASK",
        scan=make_scan(videos=[VID_A_EXPLICIT]),
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="explicit video, NEVER",
        scan=make_scan(videos=[VID_A_EXPLICIT]),
        found_video_setting=ImportFoundVideo.NEVER,
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="explicit video + explicit subs",
        scan=make_scan(videos=[VID_A_EXPLICIT], subtitles=[SUB_A_EXPLICIT]),
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
    Scenario(
        name="explicit subs only (no video)",
        scan=make_scan(subtitles=[SUB_A_EXPLICIT]),
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
    Scenario(
        name="two explicit subs only (no video)",
        scan=make_scan(subtitles=[SUB_A_EXPLICIT, SUB_B_EXPLICIT]),
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Load(paths=(SUB_A, SUB_B)),
        ),
    ),
    Scenario(
        name="explicit 2 videos",
        scan=make_scan(videos=[VID_A_EXPLICIT, VID_B_EXPLICIT]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_EXPLICIT, VID_B_EXPLICIT)),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="explicit 2 videos + explicit subs",
        scan=make_scan(videos=[VID_A_EXPLICIT, VID_B_EXPLICIT], subtitles=[SUB_A_EXPLICIT]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_EXPLICIT, VID_B_EXPLICIT)),
            subtitles=subtitles.Load(paths=(SUB_A,)),
            errors=errors.Absent(),
        ),
    ),
]


@pytest.mark.parametrize("scenario", EXPLICIT_RESOURCE_IMPORTS, ids=lambda s: s.name)
def test_explicit_resource_imports(scenario: Scenario) -> None:
    assert_plan_matches(scenario)


EXISTING_COMMENTS_IMPORTS = [
    Scenario(
        name="doc with video, ALWAYS",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=5),
        found_video_setting=ImportFoundVideo.ALWAYS,
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(5),
            session=session.Unresolved(incoming_comment_count=5),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, ASK",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=5),
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(5),
            session=session.Unresolved(incoming_comment_count=5),
            video=video.Unresolved(candidates=(VID_A_DOC,)),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, NEVER",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=5),
        found_video_setting=ImportFoundVideo.NEVER,
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(5),
            session=session.Unresolved(incoming_comment_count=5),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, no comments, ALWAYS",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A]),
        found_video_setting=ImportFoundVideo.ALWAYS,
        has_existing_comments=True,
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="doc with video, ALWAYS, with subs",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A], comment_count=5),
        found_video_setting=ImportFoundVideo.ALWAYS,
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(5),
            session=session.Unresolved(incoming_comment_count=5),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, ASK, with subs",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A], comment_count=5),
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(5),
            session=session.Unresolved(incoming_comment_count=5),
            video=video.Unresolved(candidates=(VID_A_DOC,)),
            subtitles=subtitles.Unresolved(candidates=(SUB_A,)),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, NEVER, with subs",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], subtitles=[SUB_A], comment_count=5),
        found_video_setting=ImportFoundVideo.NEVER,
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(5),
            session=session.Unresolved(incoming_comment_count=5),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="valid doc + explicit video + explicit sub, existing session",
        scan=make_scan(
            valid_docs=[DOC_A],
            videos=[VID_A_EXPLICIT],
            subtitles=[SUB_A_EXPLICIT],
            comment_count=3,
        ),
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Unresolved(incoming_comment_count=3),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
            errors=errors.Absent(),
        ),
    ),
]


@pytest.mark.parametrize("scenario", EXISTING_COMMENTS_IMPORTS, ids=lambda s: s.name)
def test_existing_comments_imports(scenario: Scenario) -> None:
    assert_plan_matches(scenario)


ERROR_IMPORTS = [
    Scenario(
        name="invalid doc + valid doc with video, ALWAYS",
        scan=make_scan(invalid_docs=[DOC_BROKEN], valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        found_video_setting=ImportFoundVideo.ALWAYS,
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
            errors=errors.Unresolved(invalid_documents=(DOC_BROKEN,)),
        ),
    ),
    Scenario(
        name="invalid docs only",
        scan=make_scan(invalid_docs=[DOC_BROKEN, DOC_B]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
            errors=errors.Unresolved(invalid_documents=(DOC_BROKEN, DOC_B)),
        ),
    ),
    Scenario(
        name="invalid doc + valid doc with video, ASK",
        scan=make_scan(invalid_docs=[DOC_BROKEN], valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_DOC,)),
            subtitles=subtitles.Skip(),
            errors=errors.Unresolved(invalid_documents=(DOC_BROKEN,)),
        ),
    ),
    Scenario(
        name="invalid doc + existing session + comments, ALWAYS",
        scan=make_scan(invalid_docs=[DOC_BROKEN], valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=5),
        found_video_setting=ImportFoundVideo.ALWAYS,
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(5),
            session=session.Unresolved(incoming_comment_count=5),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
            errors=errors.Unresolved(invalid_documents=(DOC_BROKEN,)),
        ),
    ),
    Scenario(
        name="invalid doc + existing session + 2 videos + subs",
        scan=make_scan(
            invalid_docs=[DOC_BROKEN],
            valid_docs=[DOC_A],
            videos=[VIDEO_A, VIDEO_B],
            subtitles=[SUB_A],
            comment_count=5,
        ),
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(5),
            session=session.Unresolved(incoming_comment_count=5),
            video=video.Unresolved(candidates=(VID_A_DOC, VID_B_DOC)),
            subtitles=subtitles.Unresolved(candidates=(SUB_A,)),
            errors=errors.Unresolved(invalid_documents=(DOC_BROKEN,)),
        ),
    ),
    Scenario(
        name="invalid doc + explicit video",
        scan=make_scan(invalid_docs=[DOC_BROKEN], videos=[VID_A_EXPLICIT]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
            errors=errors.Unresolved(invalid_documents=(DOC_BROKEN,)),
        ),
    ),
    Scenario(
        name="invalid doc + explicit video + explicit subs",
        scan=make_scan(invalid_docs=[DOC_BROKEN], videos=[VID_A_EXPLICIT], subtitles=[SUB_A_EXPLICIT]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
            errors=errors.Unresolved(invalid_documents=(DOC_BROKEN,)),
        ),
    ),
]


@pytest.mark.parametrize("scenario", ERROR_IMPORTS, ids=lambda s: s.name)
def test_error_imports(scenario: Scenario) -> None:
    assert_plan_matches(scenario)


ALREADY_LOADED_VIDEO = [
    Scenario(
        name="doc with video, already loaded, ALWAYS",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        found_video_setting=ImportFoundVideo.ALWAYS,
        any_candidate_loaded=True,
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="explicit video, already loaded",
        scan=make_scan(videos=[VID_A_EXPLICIT]),
        any_candidate_loaded=True,
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="2 doc videos, one already loaded",
        scan=make_scan(valid_docs=[DOC_A, DOC_B], videos=[VIDEO_A, VIDEO_B], comment_count=3),
        any_candidate_loaded=True,
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_DOC, VID_B_DOC)),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, already loaded, ASK",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        any_candidate_loaded=True,
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="doc with video, already loaded, NEVER",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        found_video_setting=ImportFoundVideo.NEVER,
        any_candidate_loaded=True,
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="doc with video, already loaded, ALWAYS, existing comments",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        found_video_setting=ImportFoundVideo.ALWAYS,
        any_candidate_loaded=True,
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Unresolved(incoming_comment_count=3),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, already loaded, ASK, existing comments",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        any_candidate_loaded=True,
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Unresolved(incoming_comment_count=3),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="doc with video, already loaded, NEVER, existing comments",
        scan=make_scan(valid_docs=[DOC_A], videos=[VIDEO_A], comment_count=3),
        found_video_setting=ImportFoundVideo.NEVER,
        any_candidate_loaded=True,
        has_existing_comments=True,
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Unresolved(incoming_comment_count=3),
            video=video.Skip(),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
]


@pytest.mark.parametrize("scenario", ALREADY_LOADED_VIDEO, ids=lambda s: s.name)
def test_already_loaded_video(scenario: Scenario) -> None:
    assert_plan_matches(scenario)


MIXED_PROVENANCE = [
    Scenario(
        name="explicit video + doc-found video",
        scan=make_scan(valid_docs=[DOC_A], videos=[VID_A_EXPLICIT, VID_B_DOC], comment_count=3),
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="2 explicit videos + doc-found video",
        scan=make_scan(valid_docs=[DOC_A], videos=[VID_A_EXPLICIT, VID_B_EXPLICIT, VID_C_DOC], comment_count=3),
        expected=UnfinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_EXPLICIT, VID_B_EXPLICIT)),
            subtitles=subtitles.Skip(),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="same video, explicit + doc-found",
        scan=make_scan(valid_docs=[DOC_A], videos=[VID_A_EXPLICIT_DOC], comment_count=3),
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Skip(),
        ),
    ),
    Scenario(
        name="mixed subs (explicit + doc), NEVER video",
        scan=make_scan(
            valid_docs=[DOC_A],
            videos=[VIDEO_A],
            subtitles=[SUB_A_EXPLICIT_DOC],
            comment_count=3,
        ),
        found_video_setting=ImportFoundVideo.NEVER,
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
    Scenario(
        name="explicit sub references video, ALWAYS",
        scan=make_scan(subtitles=[SUB_A_EXPLICIT], videos=[VID_A_SUB]),
        found_video_setting=ImportFoundVideo.ALWAYS,
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
    Scenario(
        name="explicit sub references video, ASK",
        scan=make_scan(subtitles=[SUB_A_EXPLICIT], videos=[VID_A_SUB]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_SUB,)),
            subtitles=subtitles.Load(paths=(SUB_A,)),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="two explicit subs reference same video, ALWAYS",
        scan=make_scan(subtitles=[SUB_A_EXPLICIT, SUB_B_EXPLICIT], videos=[VID_A_SUB]),
        found_video_setting=ImportFoundVideo.ALWAYS,
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A, SUB_B)),
        ),
    ),
    Scenario(
        name="two explicit subs reference same video, ASK",
        scan=make_scan(subtitles=[SUB_A_EXPLICIT, SUB_B_EXPLICIT], videos=[VID_A_SUB]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_SUB,)),
            subtitles=subtitles.Load(paths=(SUB_A, SUB_B)),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="two explicit subs reference two different videos",
        scan=make_scan(subtitles=[SUB_A_EXPLICIT, SUB_B_EXPLICIT], videos=[VID_A_SUB, VID_B_SUB]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_SUB, VID_B_SUB)),
            subtitles=subtitles.Load(paths=(SUB_A, SUB_B)),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="explicit sub + doc-derived sub, explicit wins (silent)",
        scan=make_scan(valid_docs=[DOC_A], subtitles=[SUB_A_EXPLICIT, SUB_B_DOC]),
        expected=FinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Skip(),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
    Scenario(
        name="explicit sub + doc-derived sub, video step fires",
        scan=make_scan(valid_docs=[DOC_A], subtitles=[SUB_A_EXPLICIT, SUB_B_DOC], videos=[VIDEO_A]),
        expected=UnfinishedPlan(
            comments=(),
            session=session.Merge(),
            video=video.Unresolved(candidates=(VID_A_DOC,)),
            subtitles=subtitles.Load(paths=(SUB_A,)),
            errors=errors.Absent(),
        ),
    ),
    Scenario(
        name="valid doc + explicit video + explicit sub, blank session",
        scan=make_scan(
            valid_docs=[DOC_A],
            videos=[VID_A_EXPLICIT],
            subtitles=[SUB_A_EXPLICIT],
            comment_count=3,
        ),
        expected=FinishedPlan(
            comments=stub_comments(3),
            session=session.Merge(),
            video=video.Load(path=VIDEO_A),
            subtitles=subtitles.Load(paths=(SUB_A,)),
        ),
    ),
]


@pytest.mark.parametrize("scenario", MIXED_PROVENANCE, ids=lambda s: s.name)
def test_mixed_provenance(scenario: Scenario) -> None:
    assert_plan_matches(scenario)
