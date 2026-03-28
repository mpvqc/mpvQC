# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any

from mpvqc.datamodels import Comment

from .item import CommentItem


def create_item_from(comment: dict[str, Any] | Comment) -> CommentItem:
    item = CommentItem()
    if isinstance(comment, dict):
        item.time = comment["time"]
        item.comment_type = comment["commentType"]
        item.comment = comment["comment"]
    else:
        item.time = comment.time
        item.comment_type = comment.comment_type
        item.comment = comment.comment
    return item
