# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


def test_get_all_comments(comments, default_comments):
    assert comments.comments() == default_comments
