# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os


def read_display_zoom_factor() -> float:
    # Assume that people who use linux are fine with setting it this way
    # until there's an official way of figuring this out

    default_factor = 1.0

    try:
        factor = os.getenv("MPVQC_VIDEO_SCALING_FACTOR", default_factor)
        return float(factor)
    except ValueError:
        return default_factor
