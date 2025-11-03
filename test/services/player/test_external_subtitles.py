# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
from dataclasses import dataclass
from pathlib import Path

import pytest


@dataclass
class ExternalSubtitleTestCase:
    description: str
    track_list_data: list[dict]
    expected_paths: list[Path]


SUBTITLE_DIR = Path.home() / "subtitles"
SUB_1 = SUBTITLE_DIR / "subtitle1.srt"
SUB_2 = SUBTITLE_DIR / "subtitle2.vtt"
SUB_3 = SUBTITLE_DIR / "subtitle3.ass"


@pytest.mark.parametrize(
    "test_case",
    [
        ExternalSubtitleTestCase(
            description="no_subtitles",
            track_list_data=[],
            expected_paths=[],
        ),
        ExternalSubtitleTestCase(
            description="single_external_subtitle",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_1),
                },
            ],
            expected_paths=[SUB_1],
        ),
        ExternalSubtitleTestCase(
            description="multiple_external_subtitles",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_2),
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_1),
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_3),
                },
            ],
            expected_paths=[SUB_1, SUB_2, SUB_3],
        ),
        ExternalSubtitleTestCase(
            description="mixed_external_and_internal_subtitles",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_1),
                },
                {
                    "type": "sub",
                    "external": False,
                    "external-filename": "",
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_2),
                },
            ],
            expected_paths=[SUB_1, SUB_2],
        ),
        ExternalSubtitleTestCase(
            description="mixed_subtitle_and_audio_tracks",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_1),
                },
                {
                    "type": "audio",
                    "external": True,
                    "external-filename": str(Path.home() / "audio.mp3"),
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_2),
                },
            ],
            expected_paths=[SUB_1, SUB_2],
        ),
        ExternalSubtitleTestCase(
            description="duplicate_subtitles",
            track_list_data=[
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_1),
                },
                {
                    "type": "sub",
                    "external": True,
                    "external-filename": str(SUB_1),
                },
            ],
            expected_paths=[SUB_1],
        ),
        ExternalSubtitleTestCase(
            description="no_external_only_internal",
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
            expected_paths=[],
        ),
    ],
    ids=lambda tc: tc.description,
)
def test_external_subtitles(player_service, test_case):
    player_service._mpv.track_list = test_case.track_list_data

    result = player_service.external_subtitles

    assert result == test_case.expected_paths
