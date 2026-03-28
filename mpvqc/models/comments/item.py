# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


import itertools

from PySide6.QtGui import QStandardItem

from .roles import Role

ID_COUNTER = itertools.count()


class CommentItem(QStandardItem):
    def __init__(self):
        super().__init__()
        self._id = next(ID_COUNTER)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        return self._id == other._id

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        return self._id != other._id

    def __hash__(self):
        return super().__hash__()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        t1, t2 = self.data(Role.TIME), other.data(Role.TIME)
        if t1 != t2:
            return t1 < t2
        return self._id < other._id

    def __le__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        t1, t2 = self.data(Role.TIME), other.data(Role.TIME)
        if t1 != t2:
            return t1 < t2
        return self._id <= other._id

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        t1, t2 = self.data(Role.TIME), other.data(Role.TIME)
        if t1 != t2:
            return t1 > t2
        return self._id > other._id

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, CommentItem):
            return NotImplemented
        t1, t2 = self.data(Role.TIME), other.data(Role.TIME)
        if t1 != t2:
            return t1 > t2
        return self._id >= other._id
