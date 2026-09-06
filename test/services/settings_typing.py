# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Pyrefly checks this file through the project hook; pytest never collects it. A setting that stops reading
# back as its declared type fails the hook here, where nothing else would notice.

from typing import assert_type

from mpvqc.shell.services import ShellSettingsService, TimeDisplayMode, WindowTitleFormat


def reads_keep_their_declared_types(shell: ShellSettingsService) -> None:
    assert_type(shell.show_percentage, bool)
    assert_type(shell.layout_orientation, int)
    assert_type(shell.time_display_mode, TimeDisplayMode)
    assert_type(shell.window_title_format, WindowTitleFormat)
