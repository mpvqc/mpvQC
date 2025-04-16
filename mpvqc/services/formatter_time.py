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


class TimeFormatterService:
    """"""

    @staticmethod
    def format_time_to_string(input_seconds: float, *, long_format: bool) -> str:
        hours, remainder = divmod(input_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if long_format:
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        else:  # noqa RET505
            return f"{int(minutes):02d}:{int(seconds):02d}"
