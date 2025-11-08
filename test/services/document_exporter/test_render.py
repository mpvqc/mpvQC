# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import textwrap
from pathlib import Path

import pytest

from mpvqc.services import DocumentRenderService, ResourceService


@pytest.fixture
def service() -> DocumentRenderService:
    return DocumentRenderService()


@pytest.fixture
def resource_service() -> ResourceService:
    return ResourceService()


def test_video_path_video_name(configure_mocks, service):
    template = textwrap.dedent(
        """\
        video_path: {{ video_path }}
        video_name: {{ video_name }}
        """
    )

    configure_mocks(video=Path.home() / "video.mkv")
    expected = textwrap.dedent(f"""\
        video_path: {Path.home() / "video.mkv"}
        video_name: video.mkv
        """)
    actual = service.render(template)
    assert actual == expected

    configure_mocks(video=None)
    expected = textwrap.dedent("""video_path: \nvideo_name: \n""")
    actual = service.render(template)
    assert actual == expected


def test_renders_text_that_ends_with_newline(configure_mocks, service, resource_service):
    configure_mocks()
    actual = service.render(resource_service.default_export_template)
    assert actual[-1] == "\n"


def test_renders_no_headers(configure_mocks, service, resource_service):
    configure_mocks()

    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        # total lines: 0
        """
    )
    actual = service.render(resource_service.default_export_template)
    assert expected == actual


def test_renders_partial_headers(configure_mocks, service, resource_service):
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
        path      : {Path("/path/to/video")}

        [DATA]
        # total lines: 0
        """
    )
    actual = service.render(resource_service.default_export_template)
    assert expected == actual


def test_renders_partial_headers_generator(configure_mocks, service, resource_service, build_info_service_mock):
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
    actual = service.render(resource_service.default_export_template)
    assert expected == actual


def test_renders_comments(configure_mocks, service, resource_service):
    configure_mocks(
        comments=[
            {"time": 0, "commentType": "Translation", "comment": "My first comment"},
            {"time": 50, "commentType": "Spelling", "comment": "My second comment"},
            {"time": 100, "commentType": "Phrasing", "comment": "My third comment"},
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
    actual = service.render(resource_service.default_export_template)
    assert expected == actual


def test_renders_backup(configure_mocks, service, resource_service):
    configure_mocks(
        write_header_video_path=False,
        video="/path/to/video/ignore/user/setting",
        comments=[
            {"time": 0, "commentType": "Translation", "comment": "My first comment"},
            {"time": 50, "commentType": "Spelling", "comment": "My second comment"},
            {"time": 100, "commentType": "Phrasing", "comment": "My third comment"},
        ],
    )

    rendered = service.render(resource_service.backup_template)

    assert f"path      : {Path('/path/to/video/ignore/user/setting')}" in rendered
    assert "[00:00:00] [Translation] My first comment" in rendered
    assert "[00:00:50] [Spelling] My second comment" in rendered
    assert "[00:01:40] [Phrasing] My third comment" in rendered
    assert "# total lines: 3" in rendered


def test_renders_no_subtitles(configure_mocks, service, resource_service):
    subtitles = [Path.home() / "subtitle.ass"]
    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        # total lines: 0
        """
    )

    configure_mocks()
    assert expected == service.render(resource_service.default_export_template)

    configure_mocks(subtitles=subtitles)
    assert expected == service.render(resource_service.default_export_template)

    configure_mocks(write_header_subtitles=True)
    assert expected == service.render(resource_service.default_export_template)

    configure_mocks(write_header_subtitles=True, subtitles=subtitles)
    assert expected != service.render(resource_service.default_export_template), (
        "Documents should not match as subtitles should now be rendered"
    )


def test_renders_subtitles(configure_mocks, service, resource_service):
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
    assert expected == service.render(resource_service.default_export_template)

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
        subtitle  : {subtitle1}
        subtitle  : {subtitle2}

        [DATA]
        # total lines: 0
        """
    )
    assert expected == service.render(resource_service.default_export_template)
