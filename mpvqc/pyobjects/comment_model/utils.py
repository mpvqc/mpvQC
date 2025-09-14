# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Any

from PySide6.QtGui import QStandardItem, QStandardItemModel

from mpvqc.models import Comment

from .item import CommentItem
from .roles import Role


def retrieve_comments_from(model: QStandardItemModel) -> list[dict[str, Any]]:
    comments = []
    for row in range(model.rowCount()):
        item = model.item(row, column=0)
        comment = create_comment_from(item)
        comments.append(comment)
    return comments


def create_comment_from(item: QStandardItem) -> dict[str, Any]:
    return {
        "time": int(item.data(Role.TIME)),
        "commentType": item.data(Role.TYPE),
        "comment": item.data(Role.COMMENT),
    }


def create_item_from(comment: dict[str, Any] | Comment) -> CommentItem:
    item = CommentItem()
    if isinstance(comment, Comment):
        item.setData(comment.time, Role.TIME)
        item.setData(comment.comment_type, Role.TYPE)
        item.setData(comment.comment, Role.COMMENT)
    else:
        item.setData(comment["time"], Role.TIME)
        item.setData(comment["commentType"], Role.TYPE)
        item.setData(comment["comment"], Role.COMMENT)
    return item
