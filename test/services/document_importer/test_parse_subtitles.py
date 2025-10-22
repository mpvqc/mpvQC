# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

DOCUMENT_NO_SUBTITLES = """\
[FILE]
nick: some-weird-nick
"""

DOCUMENT_SUBTITLE_NOT_EXISTING = """\
[FILE]
nick: some-weird-nick
subtitle: {subtitle}
"""

DOCUMENT_ONE_SUBTITLE = """\
[FILE]
nick: some-weird-nick
subtitle: {subtitle}
"""

DOCUMENT_TWO_SUBTITLES = """\
[FILE]
nick: some-weird-nick
subtitle: {subtitle_1}
subtitle: {subtitle_2}
"""


@pytest.fixture(scope="session")
def subtitle_not_existing(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    return temp_dir / "subtitle_not_existing.ass"


@pytest.fixture(scope="session")
def subtitle_existing_1(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "subtitle_existing_1.ass"
    file_path.touch()
    return file_path


@pytest.fixture(scope="session")
def subtitle_existing_2(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "subtitle_existing_2.ass"
    file_path.touch()
    return file_path


@pytest.fixture(scope="session")
def document_no_subtitles(tmp_path_factory):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_no_subtitles.txt"
    file_path.write_text(DOCUMENT_NO_SUBTITLES, encoding="utf-8")
    return file_path


@pytest.fixture(scope="session")
def document_subtitle_not_existing(tmp_path_factory, subtitle_not_existing):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_subtitle_not_existing.txt"
    content = DOCUMENT_SUBTITLE_NOT_EXISTING.format(subtitle=subtitle_not_existing)
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture(scope="session")
def document_one_subtitle(tmp_path_factory, subtitle_existing_1):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_one_subtitle.txt"
    content = DOCUMENT_ONE_SUBTITLE.format(subtitle=subtitle_existing_1)
    file_path.write_text(content, encoding="utf-8")
    return file_path


@pytest.fixture(scope="session")
def document_two_subtitles(tmp_path_factory, subtitle_existing_1, subtitle_existing_2):
    temp_dir = tmp_path_factory.mktemp("data")
    file_path = temp_dir / "document_two_subtitles.txt"
    content = DOCUMENT_TWO_SUBTITLES.format(
        subtitle_1=subtitle_existing_1,
        subtitle_2=subtitle_existing_2,
    )
    file_path.write_text(content, encoding="utf-8")
    return file_path


def test_parse_document_no_subtitles(
    service,
    document_no_subtitles,
):
    result = service.read([document_no_subtitles])

    assert result.valid_documents
    assert not result.existing_subtitles


def test_parse_document_subtitle_not_existing(
    service,
    document_subtitle_not_existing,
):
    result = service.read([document_subtitle_not_existing])

    assert result.valid_documents
    assert not result.existing_subtitles


def test_parse_document_one_subtitle(
    service,
    document_one_subtitle,
    subtitle_existing_1,
):
    result = service.read([document_one_subtitle])

    assert result.valid_documents
    assert len(result.existing_subtitles) == 1
    assert subtitle_existing_1 in result.existing_subtitles


def test_parse_document_two_subtitles(
    service,
    document_two_subtitles,
    subtitle_existing_1,
    subtitle_existing_2,
):
    result = service.read([document_two_subtitles])

    assert result.valid_documents
    assert len(result.existing_subtitles) == 2
    assert subtitle_existing_1 in result.existing_subtitles
    assert subtitle_existing_2 in result.existing_subtitles
