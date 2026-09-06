# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

# Pyrefly checks this file through the project hook; pytest never collects it. A setting that stops reading
# back as its declared type fails the hook here, where nothing else would notice.

from typing import assert_type

from PySide6.QtCore import QUrl

from mpvqc.comments.services import CommentsSettingsService
from mpvqc.exporting.services import ExportSettingsService
from mpvqc.i18n.services import I18nSettingsService
from mpvqc.importing.services import ImportSettingsService, LoadFoundVideo
from mpvqc.shell.services import ShellSettingsService, TimeDisplayMode, WindowTitleFormat


def reads_keep_their_declared_types(
    shell: ShellSettingsService,
    exporting: ExportSettingsService,
    importing: ImportSettingsService,
    i18n: I18nSettingsService,
    comments: CommentsSettingsService,
) -> None:
    assert_type(shell.show_percentage, bool)
    assert_type(shell.layout_orientation, int)
    assert_type(shell.time_display_mode, TimeDisplayMode)
    assert_type(shell.window_title_format, WindowTitleFormat)
    assert_type(exporting.nickname, str)
    assert_type(importing.import_found_video, LoadFoundVideo)
    assert_type(importing.last_directory_video, QUrl)
    assert_type(i18n.language, str)
    assert_type(comments.comment_types, list[str])
