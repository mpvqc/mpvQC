# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtGui import QClipboard

from mpvqc.datamodels import Comment


@pytest.fixture(scope="session")
def clipboard(qt_app) -> QClipboard:
    return qt_app.clipboard()


def test_copy_to_clipboard(make_model, clipboard):
    # noinspection PyArgumentList
    model, _ = make_model(
        set_comments=[
            Comment(time=100, comment_type="Phrasing", comment="Comment Content 1"),
            Comment(time=200, comment_type="Translation", comment="Comment Content 2"),
            Comment(time=300, comment_type="Spelling", comment="Comment Content 3"),
        ],
        set_player_time=0,
    )

    model.copy_to_clipboard(0)
    assert clipboard.text() == "[00:01:40] [Phrasing] Comment Content 1"

    model.copy_to_clipboard(1)
    assert clipboard.text() == "[00:03:20] [Translation] Comment Content 2"

    model.copy_to_clipboard(2)
    assert clipboard.text() == "[00:05:00] [Spelling] Comment Content 3"
