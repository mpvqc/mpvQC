# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import errno
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zipfile import ZipFile

import pytest

from mpvqc.exporting.services import backup
from mpvqc.shared import Comment

_CAPTURED_AT = datetime(2026, 3, 4, 5, 6, 7, tzinfo=timezone(timedelta(hours=2)))


def _entries(archive: Path) -> dict[str, str]:
    with ZipFile(archive) as file:
        return {name: file.read(name).decode("utf-8") for name in file.namelist()}


def test_archive_name(make_snapshot, tmp_path):
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT))

    assert [path.name for path in tmp_path.iterdir()] == ["2026-03.zip"]


def test_entry_name_keeps_the_video_extension(make_snapshot, tmp_path):
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT, video="/path/to/video.mkv"))

    assert list(_entries(tmp_path / "2026-03.zip")) == ["2026-03-04_05-06-07_video.mkv.json"]


def test_entry_name_falls_back_to_untitled(make_snapshot, tmp_path):
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT))

    assert list(_entries(tmp_path / "2026-03.zip")) == ["2026-03-04_05-06-07_untitled.json"]


def test_writes_rendered_backup(make_snapshot, tmp_path):
    snapshot = make_snapshot(
        captured_at=_CAPTURED_AT,
        comments=[Comment(time=50 * 1000, comment_type="Spelling", comment="My comment")],
    )

    backup(tmp_path, snapshot)

    (content,) = _entries(tmp_path / "2026-03.zip").values()
    document = json.loads(content)
    assert document["version"] == 1
    assert document["created_at"] == "2026-03-04T03:06:07Z"
    assert document["comments"] == [{"time": "00:00:50.000", "type": "Spelling", "text": "My comment"}]


def test_backup_fields_ignore_export_settings(make_snapshot, tmp_path):
    snapshot = make_snapshot(
        captured_at=_CAPTURED_AT,
        video="/path/to/video.mkv",
        nickname="lorem",
        write_header_date=False,
        write_header_generator=True,
        write_header_nickname=True,
        write_header_video_path=False,
        write_header_subtitles=True,
    )

    backup(tmp_path, snapshot)

    (content,) = _entries(tmp_path / "2026-03.zip").values()
    document = json.loads(content)
    assert list(document) == ["$schema", "version", "created_at", "video", "comments"]
    assert document["video"] == str(Path("/path/to/video.mkv").resolve())


def test_later_backup_joins_the_months_archive(make_snapshot, tmp_path):
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT))
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT + timedelta(minutes=1)))

    assert list(_entries(tmp_path / "2026-03.zip")) == [
        "2026-03-04_05-06-07_untitled.json",
        "2026-03-04_05-07-07_untitled.json",
    ]


def test_failed_backup_keeps_the_months_earlier_backups(make_snapshot, tmp_path, monkeypatch):
    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT))
    archive = tmp_path / "2026-03.zip"
    before = archive.read_bytes()

    def fail(*_args: object, **_kwargs: object) -> None:
        raise OSError(errno.ENOSPC, "disk full")

    monkeypatch.setattr(ZipFile, "writestr", fail)

    with pytest.raises(OSError, match="disk full"):
        backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT + timedelta(minutes=1)))

    assert archive.read_bytes() == before
    assert list(tmp_path.iterdir()) == [archive]


def test_unreadable_archive_is_set_aside_for_a_fresh_one(make_snapshot, tmp_path):
    archive = tmp_path / "2026-03.zip"
    archive.write_bytes(b"not a zip archive")

    backup(tmp_path, make_snapshot(captured_at=_CAPTURED_AT))

    assert list(_entries(archive)) == ["2026-03-04_05-06-07_untitled.json"]
    set_aside = tmp_path / "2026-03_unreadable_2026-03-04_05-06-07.zip"
    assert set_aside.read_bytes() == b"not a zip archive"
