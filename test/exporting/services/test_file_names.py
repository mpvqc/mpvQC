# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path
from typing import Literal, NamedTuple

import pytest

from mpvqc.exporting.services import propose_document_path

_VIDEOS = Path.home() / "Videos"
_FALLBACK = Path.home() / "Movies"


class ProposalCase(NamedTuple):
    name: str
    video: Path | None
    nickname: str | None
    suffix: Literal["json", "txt"]
    expected: Path


PROPOSAL_CASES = [
    ProposalCase(
        name="video and nickname",
        video=_VIDEOS / "my-movie.mp4",
        nickname="some-nickname",
        suffix="json",
        expected=_VIDEOS / "[QC]_my-movie_some-nickname.json",
    ),
    ProposalCase(
        name="video without nickname",
        video=_VIDEOS / "my-movie.mp4",
        nickname=None,
        suffix="txt",
        expected=_VIDEOS / "[QC]_my-movie.txt",
    ),
    ProposalCase(
        name="no video, nickname",
        video=None,
        nickname="some-nickname",
        suffix="txt",
        expected=_FALLBACK / "[QC]_untitled_some-nickname.txt",
    ),
    ProposalCase(
        name="no video, no nickname",
        video=None,
        nickname=None,
        suffix="json",
        expected=_FALLBACK / "[QC]_untitled.json",
    ),
    ProposalCase(
        name="nickname with characters a file name cannot hold",
        video=_VIDEOS / "my-movie.mp4",
        nickname='foo/bar\\baz:1<2>3"4|5?6*7\n\t',
        suffix="json",
        expected=_VIDEOS / "[QC]_my-movie_foo_bar_baz_1_2_3_4_5_6_7__.json",
    ),
    ProposalCase(
        name="empty nickname counts as none",
        video=_VIDEOS / "my-movie.mp4",
        nickname="",
        suffix="json",
        expected=_VIDEOS / "[QC]_my-movie.json",
    ),
]


@pytest.mark.parametrize("case", PROPOSAL_CASES, ids=lambda case: case.name)
def test_proposes_document_paths(case):
    actual = propose_document_path(
        video_path=str(case.video) if case.video else None,
        nickname=case.nickname,
        suffix=case.suffix,
        fallback_directory=_FALLBACK,
    )

    assert actual == case.expected


def test_proposal_is_absolute():
    actual = propose_document_path(
        video_path=None,
        nickname=None,
        suffix="json",
        fallback_directory=Path("relative-dir"),
    )

    assert actual == Path.cwd() / "relative-dir" / "[QC]_untitled.json"
