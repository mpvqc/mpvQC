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

from typing import Any

from PySide6.QtGui import QStandardItem, QStandardItemModel

from mpvqc.models import Comment

from .item import CommentItem
from .roles import Role


def retrieve_comments_from(model: QStandardItemModel) -> list[dict[str, Any]]:
    comments = []
    for row in range(0, model.rowCount()):
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
