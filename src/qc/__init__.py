# mpvQC
#
# Copyright (C) 2020 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Comment:
    """
    A representation of a comment line.
    """

    def __init__(self, comment_time, comment_type, comment_note):
        self.comment_time = comment_time
        self.comment_type = comment_type
        self.comment_note = comment_note

    def __str__(self):
        return "[{}] [{}] {}".format(self.comment_time, self.comment_type, self.comment_note)

    def __eq__(self, other):
        if isinstance(other, Comment):
            return self.comment_time == other.comment_time \
                   and self.comment_type == other.comment_type \
                   and self.comment_note == other.comment_note
        return False
