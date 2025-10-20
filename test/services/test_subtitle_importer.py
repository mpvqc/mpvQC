# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services import SubtitleImporterService

SUBTITLE_EMPTY = """\
"""

SUBTITLE_INCOMPLETE_2 = """\
[Script Info]

[Aegisub Project Garbage]

"""

SUBTITLE_VIDEO_IN_SCRIPT_INFO = """\
[Script Info]
Video File: {video_file_existing_1}

[Aegisub Project Garbage]

"""

SUBTITLE_VIDEO_IN_AEGISUB = """\
[Script Info]

[Aegisub Project Garbage]
Video AR Mode: 4
Video AR Value: 1.777778
Video Zoom Percent: 0.500000
Video File: {video_file_existing_1}
Scroll Position: 0
Active Line: 0
Video Position: 276
"""

SUBTITLE_VIDEO_IN_AEGISUB_NONEXISTENT = """\
[Script Info]

[Aegisub Project Garbage]
Video AR Mode: 4
Video AR Value: 1.777778
Video Zoom Percent: 0.500000
Video File: {video_file_not_existing}
Scroll Position: 0
Active Line: 0
Video Position: 276
"""

SUBTITLE_VIDEO_IN_BOTH = """\
[Script Info]
Title: My Subtitles
ScriptType: v4.00
Video File: {video_file_existing_1}

[Aegisub Project Garbage]
Video AR Mode: 4
Video AR Value: 1.777778
Video Zoom Percent: 0.500000
Video File: {video_file_existing_2}
Scroll Position: 0
Active Line: 0
Video Position: 276
"""

SUBTITLE_VIDEO_RELATIVE_PATH = """\
[Script Info]
Video File: video_relative.mp4

[Aegisub Project Garbage]

"""


@pytest.fixture(scope="session")
def video_file_existing_1(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "video_1.mp4"
    file_path.touch()
    return file_path


@pytest.fixture(scope="session")
def video_file_existing_2(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "video_2.mp4"
    file_path.touch()
    return file_path


@pytest.fixture(scope="session")
def video_file_not_existing(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    return temp_dir / "nonexistent_video.mp4"


@pytest.fixture(scope="session", params=["ass", "ssa"])
def subtitle_empty(tmp_path_factory, request):
    ext = request.param
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / f"subtitle_empty.{ext}"
    file_path.write_text(SUBTITLE_EMPTY, encoding="utf-8-sig")
    return file_path


@pytest.fixture(scope="session", params=["ass", "ssa"])
def subtitle_incomplete(tmp_path_factory, request):
    ext = request.param
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / f"subtitle_incomplete_2.{ext}"
    file_path.write_text(SUBTITLE_INCOMPLETE_2, encoding="utf-8-sig")
    return file_path


@pytest.fixture(scope="session", params=["ass", "ssa"])
def subtitle_video_in_script_info(tmp_path_factory, video_file_existing_1, request):
    ext = request.param
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / f"subtitle_video_in_script_info.{ext}"
    content = SUBTITLE_VIDEO_IN_SCRIPT_INFO.format(video_file_existing_1=video_file_existing_1)
    file_path.write_text(content, encoding="utf-8-sig")
    return file_path


@pytest.fixture(scope="session", params=["ass", "ssa"])
def subtitle_video_in_aegisub(tmp_path_factory, video_file_existing_1, request):
    ext = request.param
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / f"subtitle_video_in_aegisub.{ext}"
    content = SUBTITLE_VIDEO_IN_AEGISUB.format(video_file_existing_1=video_file_existing_1)
    file_path.write_text(content, encoding="utf-8-sig")
    return file_path


@pytest.fixture(scope="session", params=["ass", "ssa"])
def subtitle_video_in_aegisub_nonexistent(tmp_path_factory, video_file_not_existing, request):
    ext = request.param
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / f"subtitle_video_in_aegisub_nonexistent.{ext}"
    content = SUBTITLE_VIDEO_IN_AEGISUB_NONEXISTENT.format(video_file_not_existing=video_file_not_existing)
    file_path.write_text(content, encoding="utf-8-sig")
    return file_path


@pytest.fixture(scope="session", params=["ass", "ssa"])
def subtitle_video_in_both(tmp_path_factory, video_file_existing_1, video_file_existing_2, request):
    ext = request.param
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / f"subtitle_video_in_both.{ext}"
    content = SUBTITLE_VIDEO_IN_BOTH.format(
        video_file_existing_1=video_file_existing_1,
        video_file_existing_2=video_file_existing_2,
    )
    file_path.write_text(content, encoding="utf-8-sig")
    return file_path


@pytest.fixture(scope="session", params=["ass", "ssa"])
def subtitle_video_relative_path(tmp_path_factory, request):
    ext = request.param
    temp_dir = tmp_path_factory.mktemp("data")

    video_path = temp_dir / "video_relative.mp4"
    video_path.touch()
    file_path = temp_dir / f"subtitle_video_relative_path.{ext}"
    file_path.write_text(SUBTITLE_VIDEO_RELATIVE_PATH, encoding="utf-8-sig")

    return file_path, video_path


@pytest.fixture(scope="session")
def service():
    return SubtitleImporterService()


def test_subtitles_no_existing_video_path(
    service,
    subtitle_empty,
    subtitle_incomplete,
):
    assert not service.read([subtitle_empty]).existing_videos
    assert not service.read([subtitle_incomplete]).existing_videos
    assert not service.read([subtitle_empty, subtitle_incomplete]).existing_videos


def test_subtitle_video_in_script_info(
    service,
    subtitle_video_in_script_info,
    video_file_existing_1,
):
    assert video_file_existing_1 in service.read([subtitle_video_in_script_info]).existing_videos


def test_subtitle_video_in_aegisub(
    service,
    subtitle_video_in_aegisub,
    video_file_existing_1,
):
    assert video_file_existing_1 in service.read([subtitle_video_in_aegisub]).existing_videos


def test_subtitle_video_in_aegisub_nonexistent(
    service,
    subtitle_video_in_aegisub_nonexistent,
    video_file_existing_1,
):
    assert not service.read([subtitle_video_in_aegisub_nonexistent]).existing_videos


def test_subtitle_video_in_both(
    service,
    subtitle_video_in_both,
    video_file_existing_1,
):
    assert video_file_existing_1 in service.read([subtitle_video_in_both]).existing_videos


def test_subtitle_video_relative_path(
    service,
    subtitle_video_relative_path,
):
    subtitle_path, expected_video_path = subtitle_video_relative_path
    result = service.read([subtitle_path])

    assert len(result.existing_videos) == 1
    assert result.existing_videos[0].resolve() == expected_video_path.resolve()
