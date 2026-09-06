# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.resources import read_resource


def test_missing_resource_raises_file_not_found():
    with pytest.raises(FileNotFoundError, match=":/missing-resource"):
        read_resource(":/missing-resource")
