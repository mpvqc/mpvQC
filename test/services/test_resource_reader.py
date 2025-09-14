# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

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
