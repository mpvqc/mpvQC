# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
from pathlib import Path
from typing import NamedTuple

import pytest


class ExternalSubtitleTestCase(NamedTuple):
    name: str
    track_list_data: list[dict[str, str | bool]]
    expected_paths: tuple[str, ...]


SUBTITLE_DIR = Path.home() / "subtitles"
SUB_1 = str(SUBTITLE_DIR / "subtitle1.srt")
SUB_2 = str(SUBTITLE_DIR / "subtitle2.vtt")
SUB_3 = str(SUBTITLE_DIR / "subtitle3.ass")


@pytest.mark.parametrize(
    "case",
    [
        ExternalSubtitleTestCase(
            name="no_subtitles",
            track_list_data=[],
            expected_paths=(),
        ),
        ExternalSubtitleTestCase(
            name="single_external_subtitle",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_1,
                },
            ],
            expected_paths=(SUB_1,),
        ),
        ExternalSubtitleTestCase(
            name="multiple_external_subtitles",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_2,
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_1,
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_3,
                },
            ],
            expected_paths=(SUB_1, SUB_2, SUB_3),
        ),
        ExternalSubtitleTestCase(
            name="mixed_external_and_internal_subtitles",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_1,
                },
                {
                    "type": "sub",
                    "external": False,
                    "external-filename": "",
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_2,
                },
            ],
            expected_paths=(SUB_1, SUB_2),
        ),
        ExternalSubtitleTestCase(
            name="mixed_subtitle_and_audio_tracks",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_1,
                },
                {
                    "type": "audio",
                    "external": True,
                    "external-filename": str(Path.home() / "audio.mp3"),
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_2,
                },
            ],
            expected_paths=(SUB_1, SUB_2),
        ),
        ExternalSubtitleTestCase(
            name="duplicate_subtitles",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_1,
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": SUB_1,
                },
            ],
            expected_paths=(SUB_1,),
        ),
        ExternalSubtitleTestCase(
            name="no_external_only_internal",
            track_list_data=[
                {
                    "type": "sub",
                    "external": False,
                    "external-filename": "",
                },
                {
                    "type": "sub",
                    "external": False,
                    "external-filename": "",
                },
            ],
            expected_paths=(),
        ),
    ],
    ids=lambda case: case.name,
)
def test_external_subtitles(player_service, push_property, case: ExternalSubtitleTestCase):
    push_property("track-list", case.track_list_data)

    result = player_service.external_subtitles

    assert result == case.expected_paths
