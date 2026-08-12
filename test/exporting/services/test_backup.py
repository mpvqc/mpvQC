# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mpvqc.exporting.services import backup
from mpvqc.shared import Comment

_CAPTURED_AT = datetime(2026, 3, 4, 5, 6, 7, tzinfo=timezone(timedelta(hours=2)))


@pytest.fixture
def zip_file():
    with patch("mpvqc.exporting.services.backup.ZipFile", return_value=MagicMock()) as mock:
        yield mock


def test_archive_name(make_snapshot, zip_file, tmp_path):
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT))

    assert zip_file.called
    zip_name = zip_file.call_args.args[0]
    assert zip_name.name == "2026-03.zip"


def test_entry_name_keeps_the_video_extension(make_snapshot, zip_file, tmp_path):
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT, video="/path/to/video.mkv"))

    writestr_mock = zip_file.return_value.__enter__.return_value.writestr
    assert writestr_mock.called

    filename, _ = writestr_mock.call_args.args
    assert filename == "2026-03-04_05-06-07_video.mkv.json"


def test_entry_name_falls_back_to_untitled(make_snapshot, zip_file, tmp_path):
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT))

    writestr_mock = zip_file.return_value.__enter__.return_value.writestr
    assert writestr_mock.called

    filename, _ = writestr_mock.call_args.args
    assert filename == "2026-03-04_05-06-07_untitled.json"


def test_writes_rendered_backup(make_snapshot, zip_file, tmp_path):
    snapshot = make_snapshot(
        captured_at=_CAPTURED_AT,
        comments=[Comment(time=50 * 1000, comment_type="Spelling", comment="My comment")],
    )

    backup(tmp_path, snapshot)

    writestr_mock = zip_file.return_value.__enter__.return_value.writestr
    assert writestr_mock.called

    _, content = writestr_mock.call_args.args

    document = json.loads(content)
    assert document["version"] == 1
    assert document["created_at"] == "2026-03-04T03:06:07Z"
    assert document["comments"] == [{"time": "00:00:50.000", "type": "Spelling", "text": "My comment"}]


def test_backup_fields_ignore_export_settings(make_snapshot, zip_file, tmp_path):
    snapshot = make_snapshot(
        video="/path/to/video.mkv",
        nickname="lorem",
        write_header_date=False,
        write_header_generator=True,
        write_header_nickname=True,
        write_header_video_path=False,
        write_header_subtitles=True,
    )

    backup(tmp_path, snapshot)

    _, content = zip_file.return_value.__enter__.return_value.writestr.call_args.args
    document = json.loads(content)
    assert list(document) == ["$schema", "version", "created_at", "video", "comments"]
    assert document["video"] == str(Path("/path/to/video.mkv").resolve())
