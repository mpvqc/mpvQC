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

from unittest.mock import patch

import pytest

from mpvqc.services import ResourceReaderService


@pytest.fixture(scope="module")
def service() -> ResourceReaderService:
    return ResourceReaderService()


@pytest.mark.parametrize(
    "file_path",
    [
        ":/data/icon.svg",
        "/data/icon.svg",
        "data/icon.svg",
    ],
)
def test_read_from(service, file_path):
    assert service.read_from(file_path).startswith("<?xml ")


def test_read_from_errors(service):
    with pytest.raises(FileNotFoundError):
        service.read_from(">>")

    module = "mpvqc.services.resource_reader"

    with (
        patch(f"{module}.QFile.exists", return_value=True),
        patch(f"{module}.QFile.open", return_value=False),
        pytest.raises(ValueError),  # noqa: PT011
    ):
        service.read_from("")
