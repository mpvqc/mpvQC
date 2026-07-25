# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.build import determine_build_origin

APP_ID = "io.github.mpvqc.mpvQC"


@pytest.mark.parametrize(
    ("channel", "flatpak_id", "expected"),
    [
        pytest.param(
            "",
            None,
            "unofficial",
            id="empty-channel",
        ),
        pytest.param(
            "mpvqc-github",
            None,
            "mpvqc-github",
            id="channel-set-outside-flatpak",
        ),
        pytest.param(
            "mpvqc-flatpak",
            APP_ID,
            "mpvqc-flatpak",
            id="channel-set-with-matching-id",
        ),
        pytest.param(
            "mpvqc-flatpak",
            "com.example.Rebuild",
            "unofficial",
            id="mismatched-id",
        ),
        pytest.param(
            "mpvqc-flatpak",
            "",
            "unofficial",
            id="empty-flatpak-id",
        ),
    ],
)
def test_determine_build_origin(channel, flatpak_id, expected):
    assert determine_build_origin(channel, APP_ID, flatpak_id) == expected
