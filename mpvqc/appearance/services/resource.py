# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.resources import read_resource


def read_palette_catalog() -> str:
    return read_resource(":/data/palette-catalog.json")
