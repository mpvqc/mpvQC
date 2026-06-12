# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.datamodels import Comment


def test_get_all_comments(comments, default_comments):
    actual = [
        Comment(time=comment["time"], comment_type=comment["commentType"], comment=comment["comment"])
        for comment in comments.comments()
    ]

    assert actual == list(default_comments)
