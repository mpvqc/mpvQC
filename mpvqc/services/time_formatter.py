#  mpvQC
#
#  Copyright (C) 2022 mpvQC developers
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


class TimeFormatterService:

    @staticmethod
    def format(seconds: float or None) -> tuple[int, str]:
        if seconds is None:
            return 0, '00:00:00'
        total = round(seconds)
        m, s = divmod(total, 60)
        h, m = divmod(m, 60)
        return total, "{:02d}:{:02d}:{:02d}".format(h, m, s)
