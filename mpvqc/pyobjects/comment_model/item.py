# mpvQC
#
# Copyright (C) 2022 mpvQC developers
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
        elif this_time > that_time:
            return False
        else:
            return self._id < other._id
