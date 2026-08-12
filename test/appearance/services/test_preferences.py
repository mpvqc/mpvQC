# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.appearance.services import AccentColor, AppearancePreference, Dark, FollowSystem, Light


@pytest.mark.parametrize(
    ("color_scheme", "expected"),
    [
        (Light(), AccentColor("#l1")),
        (Dark(), AccentColor("#d1")),
    ],
)
def test_appearance_preference_reads_the_accent_color_preference_of_the_asked_scheme(color_scheme, expected):
    appearance_preference = AppearancePreference(
        color_scheme_preference=FollowSystem(),
        light_accent_color_preference=AccentColor("#l1"),
        dark_accent_color_preference=AccentColor("#d1"),
    )

    assert appearance_preference.accent_color_preference_for(color_scheme) == expected
