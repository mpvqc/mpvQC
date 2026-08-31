# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.player.services import PlayerVersions, RawPropertyValue, clean_versions


class VersionsCase(NamedTuple):
    name: str
    mpv: RawPropertyValue
    ffmpeg: RawPropertyValue
    expected: PlayerVersions


CASES = [
    VersionsCase(
        name="strips both prefixes",
        mpv="mpv 0.38.0",
        ffmpeg="ffmpeg 7.0",
        expected=PlayerVersions(mpv="0.38.0", ffmpeg="7.0"),
    ),
    VersionsCase(
        name="keeps unprefixed strings",
        mpv="0.38.0",
        ffmpeg="7.0",
        expected=PlayerVersions(mpv="0.38.0", ffmpeg="7.0"),
    ),
    VersionsCase(
        name="strips only the leading prefix of dev builds",
        mpv="mpv v0.36.0-dev",
        ffmpeg="ffmpeg N-113000-g8b8b5c0",
        expected=PlayerVersions(mpv="v0.36.0-dev", ffmpeg="N-113000-g8b8b5c0"),
    ),
    VersionsCase(
        name="missing values fall back to empty",
        mpv=None,
        ffmpeg=None,
        expected=PlayerVersions(mpv="", ffmpeg=""),
    ),
    VersionsCase(
        name="mpv present while ffmpeg missing",
        mpv="mpv 0.38.0",
        ffmpeg=None,
        expected=PlayerVersions(mpv="0.38.0", ffmpeg=""),
    ),
    VersionsCase(
        name="ffmpeg present while mpv missing",
        mpv=None,
        ffmpeg="ffmpeg 7.0",
        expected=PlayerVersions(mpv="", ffmpeg="7.0"),
    ),
    VersionsCase(
        name="non-string values fall back to empty",
        mpv=1.5,
        ffmpeg=[],
        expected=PlayerVersions(mpv="", ffmpeg=""),
    ),
]


@pytest.mark.parametrize("case", CASES, ids=lambda case: case.name)
def test_clean_versions(case: VersionsCase):
    assert clean_versions(mpv=case.mpv, ffmpeg=case.ffmpeg) == case.expected


def test_service_reads_versions_from_the_mpv_property_names(player_service, player_handle):
    player_handle.properties["mpv-version"] = "mpv 0.38.0"
    player_handle.properties["ffmpeg-version"] = "ffmpeg 7.0"

    assert player_service.versions == PlayerVersions(mpv="0.38.0", ffmpeg="7.0")
