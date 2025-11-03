# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock, patch

import pytest

from mpvqc.services import ResourceService


@pytest.fixture(autouse=True, scope="module")
def configure_injections(common_bindings_with):
    common_bindings_with()


@pytest.fixture(scope="module")
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


def test_os_specific_resources(resource_service):
    with patch("platform.system", MagicMock(return_value="Windows")):
        assert resource_service.mpv_conf_content
        assert "vo=gpu" in resource_service.mpv_conf_content.splitlines()

    other_oses = ["Linux", "Darwin"]

    for os in other_oses:
        with patch("platform.system", MagicMock(return_value=os)):
            assert resource_service.mpv_conf_content
            assert not any(line.startswith("vo=") for line in resource_service.mpv_conf_content.splitlines())
