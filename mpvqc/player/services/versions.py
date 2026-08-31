# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .state import RawPropertyValue


@dataclass(frozen=True)
class PlayerVersions:
    mpv: str
    ffmpeg: str


def clean_versions(*, mpv: RawPropertyValue, ffmpeg: RawPropertyValue) -> PlayerVersions:
    return PlayerVersions(mpv=_cleaned(mpv, prefix="mpv "), ffmpeg=_cleaned(ffmpeg, prefix="ffmpeg "))


def _cleaned(raw: RawPropertyValue, *, prefix: str) -> str:
    match raw:
        case str(value):
            return value.removeprefix(prefix)
        case _:
            return ""
