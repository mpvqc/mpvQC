# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Pin or translate, ADR 0013."""

from enum import IntEnum
from typing import NamedTuple

import pytest

from mpvqc.shell.enums import MpvqcTimeDisplayMode, MpvqcWindowTitleFormat
from mpvqc.shell.services import TimeDisplayMode, WindowTitleFormat


class PinCase(NamedTuple):
    name: str
    qml_enum: type[IntEnum]
    vocabulary: type[IntEnum]


@pytest.mark.parametrize(
    "case",
    [
        PinCase(
            name="time display mode",
            qml_enum=MpvqcTimeDisplayMode.TimeDisplayMode,
            vocabulary=TimeDisplayMode,
        ),
        PinCase(
            name="window title format",
            qml_enum=MpvqcWindowTitleFormat.WindowTitleFormat,
            vocabulary=WindowTitleFormat,
        ),
    ],
    ids=lambda case: case.name,
)
def test_the_qml_enum_restates_every_member_and_value_of_the_vocabulary(case: PinCase):
    restated = {member.name: member.value for member in case.qml_enum}
    vocabulary = {member.name: member.value for member in case.vocabulary}

    assert restated == vocabulary
