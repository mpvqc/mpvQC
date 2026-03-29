# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import itertools
import typing

from PySide6.QtGui import QStandardItem

from mpvqc.datamodels import Comment

from .roles import Role

ID_COUNTER = itertools.count()


class CommentItem(QStandardItem):
    def __init__(self):
        super().__init__()
        self._id = next(ID_COUNTER)

    @property
    def time(self) -> int:
        return self.data(Role.TIME)

    @time.setter
    def time(self, value: float) -> None:
        self.setData(int(value), Role.TIME)

    @property
    def comment_type(self) -> str:
        return self.data(Role.TYPE)

    @comment_type.setter
    def comment_type(self, value: str) -> None:
        self.setData(value, Role.TYPE)

    @property
    def comment(self) -> str:
        return self.data(Role.COMMENT)

    @comment.setter
    def comment(self, value: str) -> None:
        self.setData(value, Role.COMMENT)

    def to_comment(self) -> Comment:
        return Comment(time=self.time, comment_type=self.comment_type, comment=self.comment)

    @typing.override
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        return self._id == other._id

    @typing.override
    def __ne__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        return self._id != other._id

    def __hash__(self) -> int:
        return super().__hash__()

    @typing.override
    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        t1, t2 = self.time, other.time
        if t1 != t2:
            return t1 < t2
        return self._id < other._id

    def __le__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        t1, t2 = self.time, other.time
        if t1 != t2:
            return t1 < t2
        return self._id <= other._id

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        t1, t2 = self.time, other.time
        if t1 != t2:
            return t1 > t2
        return self._id > other._id

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        t1, t2 = self.time, other.time
        if t1 != t2:
            return t1 > t2
        return self._id >= other._id
