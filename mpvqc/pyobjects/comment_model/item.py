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

    def __lt__(self, other: "CommentItem") -> bool:
        this_time = self.data(Role.TIME)
        that_time = other.data(Role.TIME)

        if this_time < that_time:
            return True
        if this_time > that_time:
            return False
        return self._id < other._id
