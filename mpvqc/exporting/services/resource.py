# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.resources import read_resource


def read_shipped_export_template() -> str:
    return read_resource(":/data/config/export-template.jinja")
