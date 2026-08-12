# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from mpvqc.shared import MILLISECONDS_PER_SECOND


class TimeFormatterService:
    @staticmethod
    def format_time_to_string(input_seconds: float, *, long_format: bool) -> str:
        hours, remainder = divmod(input_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if long_format:
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

        return f"{int(minutes):02d}:{int(seconds):02d}"

    @staticmethod
    def format_milliseconds_to_string(input_milliseconds: int, *, long_format: bool) -> str:
        seconds = input_milliseconds // MILLISECONDS_PER_SECOND
        return TimeFormatterService.format_time_to_string(seconds, long_format=long_format)
