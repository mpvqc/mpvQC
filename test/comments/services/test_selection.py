# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.comments.services import Found, QuickSelectionAndEdit


def test_search_continues_from_the_row_a_view_action_announced(comments, make_spy):
    spy = make_spy(comments.view_action)
    comments.search("Word", include_current_row=True, top_down=True)

    comments.add_row(7, "commentType")

    assert spy.at(invocation=0, argument=0) == QuickSelectionAndEdit(row=2)
    assert comments.search("Word", include_current_row=False, top_down=True) == Found(index=3, current=3, total=5)
