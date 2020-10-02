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


def seconds_float_to_formatted_string_hours(seconds: float, short=True) -> str:
    """
    Transforms the seconds into a string of the following format **hh:mm:ss**.
    :param short: If True "mm:ss" will be returned, else "HH:mm:ss"
    :param seconds: The seconds to transform
    :return: string representing the time
    """

    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    h = "{:02d}:".format(h) if h else ("" if short else "00:")

    return "{}{:02d}:{:02d}".format(h, m, s)
