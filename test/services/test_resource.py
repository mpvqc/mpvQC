# mpvQC
#
# Copyright (C) 2022 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest.mock import MagicMock, patch

import inject
import pytest

from mpvqc.services import ResourceReaderService, ResourceService


@pytest.fixture(autouse=True, scope="module")
def configure_injections():
    def config(binder: inject.Binder):
        binder.bind(ResourceReaderService, ResourceReaderService())

    inject.configure(config, clear=True)


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
