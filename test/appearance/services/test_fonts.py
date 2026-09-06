# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.appearance.services import application_font, monospace_font


def test_application_fonts_cover_all_shipped_scripts(qt_app):
    assert application_font().families() == ["Noto Sans", "Noto Sans Hebrew"]
    assert monospace_font().families() == ["Noto Sans Mono", "Noto Sans", "Noto Sans Hebrew"]
