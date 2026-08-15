# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.comments.services import Found


def test_text_edit_reaches_the_next_navigation(comments):
    outcome = comments.search("Word", include_current_row=True, top_down=True)
    assert outcome == Found(index=0, current=1, total=5)

    comments.update_comment(row=2, comment="edited")

    outcome = comments.search("Word", include_current_row=False, top_down=True)
    assert outcome == Found(index=3, current=3, total=4)
