# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pytest
from PySide6.QtGui import QClipboard

from mpvqc.models import Comment


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
    assert "[00:01:40] [Phrasing] Comment Content 1" == clipboard.text()

    model.copy_to_clipboard(1)
    assert "[00:03:20] [Translation] Comment Content 2" == clipboard.text()

    model.copy_to_clipboard(2)
    assert "[00:05:00] [Spelling] Comment Content 3" == clipboard.text()
