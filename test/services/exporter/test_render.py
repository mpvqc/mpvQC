# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import textwrap
from pathlib import Path

import pytest

from mpvqc.services import ResourceService
from mpvqc.services.exporter.documents.classic import render_classic


@pytest.fixture
def resource_service() -> ResourceService:
    return ResourceService()


def test_video_path_video_name(configure_mocks, render_context):
    template = textwrap.dedent(
        """\
        video_path: {{ video_path }}
        video_name: {{ video_name }}
        """
    )

    configure_mocks(video=Path.home() / "video.mkv")
    expected = textwrap.dedent(f"""\
        video_path: {(Path.home() / "video.mkv").resolve()}
        video_name: video.mkv
        """)
    actual = render_classic(template, render_context)
    assert actual == expected

    configure_mocks(video=None)
    expected = textwrap.dedent("""video_path: \nvideo_name: \n""")
    actual = render_classic(template, render_context)
    assert actual == expected


def test_renders_text_that_ends_with_newline(configure_mocks, render_context, resource_service):
    configure_mocks()
    actual = render_classic(resource_service.default_export_template, render_context)
    assert actual[-1] == "\n"


def test_renders_no_headers(configure_mocks, render_context, resource_service):
    configure_mocks()

    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        # total lines: 0
        """
    )
    actual = render_classic(resource_service.default_export_template, render_context)
    assert expected == actual


def test_renders_partial_headers(configure_mocks, render_context, resource_service):
    configure_mocks(
        write_header_video_path=True,
        video="/path/to/video",
        write_header_nickname=True,
        nickname="ಠ_ಠ",
    )

    expected = textwrap.dedent(
        f"""\
        [FILE]
        nick      : ಠ_ಠ
        path      : {Path("/path/to/video").resolve()}

        [DATA]
        # total lines: 0
        """
    )
    actual = render_classic(resource_service.default_export_template, render_context)
    assert expected == actual


def test_renders_partial_headers_generator(configure_mocks, render_context, resource_service, build_info_service_mock):
    build_info_service_mock.name = "Jon"
    build_info_service_mock.version = "Snow"
    configure_mocks(write_header_generator=True)

    expected = textwrap.dedent(
        """\
        [FILE]
        generator : Jon Snow

        [DATA]
        # total lines: 0
        """
    )
    actual = render_classic(resource_service.default_export_template, render_context)
    assert expected == actual


def test_renders_comments(configure_mocks, render_context, resource_service):
    configure_mocks(
        comments=[
            {"time": 0 * 1000, "commentType": "Translation", "comment": "My first comment"},
            {"time": 50 * 1000, "commentType": "Spelling", "comment": "My second comment"},
            {"time": 100 * 1000, "commentType": "Phrasing", "comment": "My third comment"},
        ]
    )

    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        [00:00:00] [Translation] My first comment
        [00:00:50] [Spelling] My second comment
        [00:01:40] [Phrasing] My third comment
        # total lines: 3
        """
    )
    actual = render_classic(resource_service.default_export_template, render_context)
    assert expected == actual


def test_templates_receive_time_in_seconds(configure_mocks, render_context):
    configure_mocks(comments=[{"time": 90 * 1000, "commentType": "Spelling", "comment": "My comment"}])

    assert render_classic("{{ comments[0]['time'] }}", render_context) == "90"


def test_renders_no_subtitles(configure_mocks, render_context, resource_service):
    subtitles = [Path.home() / "subtitle.ass"]
    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        # total lines: 0
        """
    )

    configure_mocks()
    assert expected == render_classic(resource_service.default_export_template, render_context)

    configure_mocks(subtitles=subtitles)
    assert expected == render_classic(resource_service.default_export_template, render_context)

    configure_mocks(write_header_subtitles=True)
    assert expected == render_classic(resource_service.default_export_template, render_context)

    configure_mocks(write_header_subtitles=True, subtitles=subtitles)
    assert expected != render_classic(resource_service.default_export_template, render_context), (
        "Documents should not match as subtitles should now be rendered"
    )


def test_renders_subtitles(configure_mocks, render_context, resource_service):
    subtitle1 = Path.home() / "subtitle-1.ass"
    subtitle2 = Path.home() / "subtitle-2.srt"

    configure_mocks(
        write_header_nickname=True,
        nickname="ಠ_ಠ",
        write_header_subtitles=False,
        subtitles=[subtitle1, subtitle2],
    )
    expected = textwrap.dedent(
        """\
        [FILE]
        nick      : ಠ_ಠ

        [DATA]
        # total lines: 0
        """
    )
    assert expected == render_classic(resource_service.default_export_template, render_context)

    configure_mocks(
        write_header_nickname=True,
        nickname="ಠ_ಠ",
        write_header_subtitles=True,
        subtitles=[subtitle1, subtitle2],
    )
    expected = textwrap.dedent(
        f"""\
        [FILE]
        nick      : ಠ_ಠ
        subtitle  : {subtitle1.resolve()}
        subtitle  : {subtitle2.resolve()}

        [DATA]
        # total lines: 0
        """
    )
    assert expected == render_classic(resource_service.default_export_template, render_context)
