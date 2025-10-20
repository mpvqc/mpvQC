# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import textwrap
from pathlib import Path

import pytest

from mpvqc.services import DocumentRenderService, ResourceService


@pytest.fixture
def document_render_service() -> DocumentRenderService:
    return DocumentRenderService()


@pytest.fixture
def resource_service() -> ResourceService:
    return ResourceService()


def test_render_service_video_path_video_name(make_mock, document_render_service):
    template = textwrap.dedent(
        """\
        video_path: {{ video_path }}
        video_name: {{ video_name }}
        """
    )

    make_mock(video=Path.home() / "video.mkv")
    expected = textwrap.dedent(f"""\
        video_path: {Path.home() / "video.mkv"}
        video_name: video.mkv
        """)
    actual = document_render_service.render(template)
    assert actual == expected

    make_mock(video=None)
    expected = textwrap.dedent("""video_path: \nvideo_name: \n""")
    actual = document_render_service.render(template)
    assert actual == expected


def test_render_service_renders_text_that_ends_with_newline(make_mock, document_render_service, resource_service):
    make_mock()
    actual = document_render_service.render(resource_service.default_export_template)
    assert actual[-1] == "\n"


def test_render_service_renders_no_headers(make_mock, document_render_service, resource_service):
    make_mock()

    expected = textwrap.dedent(
        """\
        [FILE]

        [DATA]
        # total lines: 0
        """
    )
    actual = document_render_service.render(resource_service.default_export_template)
    assert expected == actual


def test_render_service_renders_partial_headers(make_mock, document_render_service, resource_service):
    make_mock(
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
    actual = document_render_service.render(resource_service.default_export_template)
    assert expected == actual


def test_render_service_renders_comments(make_mock, document_render_service, resource_service):
    make_mock(
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
    actual = document_render_service.render(resource_service.default_export_template)
    assert expected == actual


def test_renderer_service_renders_backup(make_mock, document_render_service, resource_service):
    make_mock(
        write_header_video_path=False,
        video="/path/to/video/ignore/user/setting",
        comments=[
            {"time": 0, "commentType": "Translation", "comment": "My first comment"},
            {"time": 50, "commentType": "Spelling", "comment": "My second comment"},
            {"time": 100, "commentType": "Phrasing", "comment": "My third comment"},
        ],
    )

    rendered = document_render_service.render(resource_service.backup_template)

    assert f"path      : {Path('/path/to/video/ignore/user/setting')}" in rendered
    assert "[00:00:00] [Translation] My first comment" in rendered
    assert "[00:00:50] [Spelling] My second comment" in rendered
    assert "[00:01:40] [Phrasing] My third comment" in rendered
    assert "# total lines: 3" in rendered
