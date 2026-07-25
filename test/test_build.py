# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.build import ChannelRelease, Unofficial, determine_build_origin

APP_ID = "io.github.mpvqc.mpvQC"


@pytest.mark.parametrize(
    ("channel", "flatpak_id", "expected"),
    [
        pytest.param(
            "",
            None,
            Unofficial(),
            id="empty-channel",
        ),
        pytest.param(
            "github-releases",
            None,
            ChannelRelease("github-releases"),
            id="channel-set-outside-flatpak",
        ),
        pytest.param(
            "mpvqc-flatpak",
            APP_ID,
            ChannelRelease("mpvqc-flatpak"),
            id="channel-set-with-matching-id",
        ),
        pytest.param(
            "mpvqc-flatpak",
            "com.example.Rebuild",
            Unofficial(),
            id="mismatched-id",
        ),
        pytest.param(
            "mpvqc-flatpak",
            "",
            Unofficial(),
            id="empty-flatpak-id",
        ),
    ],
)
def test_determine_build_origin(channel, flatpak_id, expected):
    assert determine_build_origin(channel, APP_ID, flatpak_id) == expected
