# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import textwrap
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pytest

from mpvqc.exporting.services import render_template
from mpvqc.services import ResourceService
from mpvqc.shared import Comment


@pytest.fixture
def resource_service() -> ResourceService:
    return ResourceService()


def test_video_path_video_name(make_snapshot):
    template = textwrap.dedent(
        """\
        video_path: {{ video_path }}
        video_name: {{ video_name }}
        """
    )

    expected = textwrap.dedent(f"""\
        video_path: {(Path.home() / "video.mkv").resolve()}
        video_name: video.mkv
        """)
    actual = render_template(template, make_snapshot(video=Path.home() / "video.mkv"))
    assert actual == expected

    expected = textwrap.dedent("""video_path: \nvideo_name: \n""")
    actual = render_template(template, make_snapshot(video=None))
    assert actual == expected


def test_renders_text_that_ends_with_newline(make_snapshot, resource_service):
    actual = render_template(resource_service.default_export_template, make_snapshot())
    assert actual[-1] == "\n"


def test_renders_no_headers(make_snapshot, resource_service):
    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        # total lines: 0
        """
    )
    actual = render_template(resource_service.default_export_template, make_snapshot())
    assert expected == actual


def test_renders_partial_headers(make_snapshot, resource_service):
    snapshot = make_snapshot(
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
    actual = render_template(resource_service.default_export_template, snapshot)
    assert expected == actual


def test_renders_partial_headers_generator(make_snapshot, resource_service):
    snapshot = make_snapshot(write_header_generator=True, generator="Jon Snow")

    expected = textwrap.dedent(
        """\
        [FILE]
        generator : Jon Snow

        [DATA]
        # total lines: 0
        """
    )
    actual = render_template(resource_service.default_export_template, snapshot)
    assert expected == actual


def test_renders_the_captured_date(make_snapshot, resource_service):
    captured_at = datetime(2019, 3, 4, 5, 6, 7, tzinfo=timezone(timedelta(hours=2)))
    snapshot = make_snapshot(captured_at=captured_at, write_header_date=True)

    actual = render_template(resource_service.default_export_template, snapshot)

    assert "date      : 2019-03-04 05:06\n" in actual


def test_renders_comments(make_snapshot, resource_service):
    snapshot = make_snapshot(
        comments=[
            Comment(time=0 * 1000, comment_type="Translation", comment="My first comment"),
            Comment(time=50 * 1000, comment_type="Spelling", comment="My second comment"),
            Comment(time=100 * 1000, comment_type="Phrasing", comment="My third comment"),
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
    actual = render_template(resource_service.default_export_template, snapshot)
    assert expected == actual


def test_templates_receive_time_in_seconds(make_snapshot):
    snapshot = make_snapshot(comments=[Comment(time=90 * 1000, comment_type="Spelling", comment="My comment")])

    assert render_template("{{ comments[0]['time'] }}", snapshot) == "90"


def test_templates_receive_exact_time_in_milliseconds(make_snapshot):
    snapshot = make_snapshot(comments=[Comment(time=(15 * 60 + 29) * 1000 + 340, comment_type="Spelling", comment="")])

    assert render_template("{{ comments[0]['time_ms'] }}", snapshot) == "929340"


def test_as_time_ms_filter_formats_subsecond_time(make_snapshot):
    snapshot = make_snapshot(comments=[Comment(time=(15 * 60 + 29) * 1000 + 340, comment_type="Spelling", comment="")])

    assert render_template("{{ comments[0]['time_ms'] | as_time_ms }}", snapshot) == "00:15:29.340"


def test_renders_no_subtitles(make_snapshot, resource_service):
    subtitles = [Path.home() / "subtitle.ass"]
    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        # total lines: 0
        """
    )

    assert expected == render_template(resource_service.default_export_template, make_snapshot())

    assert expected == render_template(resource_service.default_export_template, make_snapshot(subtitles=subtitles))

    assert expected == render_template(
        resource_service.default_export_template, make_snapshot(write_header_subtitles=True)
    )

    assert expected != render_template(
        resource_service.default_export_template, make_snapshot(write_header_subtitles=True, subtitles=subtitles)
    ), "Documents should not match as subtitles should now be rendered"


def test_renders_subtitles(make_snapshot, resource_service):
    subtitle1 = Path.home() / "subtitle-1.ass"
    subtitle2 = Path.home() / "subtitle-2.srt"

    snapshot = make_snapshot(
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
    assert expected == render_template(resource_service.default_export_template, snapshot)

    snapshot = make_snapshot(
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
    assert expected == render_template(resource_service.default_export_template, snapshot)
