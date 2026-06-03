# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import Final


class TimeFormatterService:
    MILLISECONDS_PER_SECOND: Final = 1000

    @staticmethod
    def format_time_to_string(input_seconds: float, *, long_format: bool) -> str:
        hours, remainder = divmod(input_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if long_format:
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        return f"{int(minutes):02d}:{int(seconds):02d}"

    @staticmethod
    def format_milliseconds_to_string(input_milliseconds: int, *, long_format: bool) -> str:
        seconds = input_milliseconds // TimeFormatterService.MILLISECONDS_PER_SECOND
        return TimeFormatterService.format_time_to_string(seconds, long_format=long_format)

    @staticmethod
    def parse_string_to_milliseconds(time_string: str) -> int:
        hours, minutes, seconds = map(int, time_string.split(":"))
        return (hours * 3600 + minutes * 60 + seconds) * TimeFormatterService.MILLISECONDS_PER_SECOND
