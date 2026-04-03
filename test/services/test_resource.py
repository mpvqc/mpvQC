# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services import ResourceService


@pytest.fixture
def resource_service() -> ResourceService:
    return ResourceService()


def test_resources(resource_service):
    assert resource_service.input_conf_content
    assert resource_service.backup_template
    assert resource_service.default_export_template

    export_template = resource_service.default_export_template
    assert "write_date" in export_template
    assert "date" in export_template
    assert "write_generator" in export_template
    assert "generator" in export_template
    assert "write_nickname" in export_template
    assert "nickname" in export_template
    assert "write_video_path" in export_template
    assert "video_path" in export_template
    assert "comments" in export_template
    assert "comment['time'] | as_time" in export_template
    assert "comment['commentType'] | as_comment_type" in export_template
    assert "comment['comment'] | trim" in export_template


def test_mpv_conf_windows(resource_service, monkeypatch):
    monkeypatch.setattr("sys.platform", "win32")
    assert "vo=gpu" in resource_service.mpv_conf_content.splitlines()


@pytest.mark.parametrize("platform", ["linux", "darwin"])
def test_mpv_conf_non_windows(resource_service, monkeypatch, platform):
    monkeypatch.setattr("sys.platform", platform)
    assert not any(line.startswith("vo=") for line in resource_service.mpv_conf_content.splitlines())
