# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


class TimeFormatterService:
    """"""

    @staticmethod
    def format_time_to_string(input_seconds: float, *, long_format: bool) -> str:
        hours, remainder = divmod(input_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        if long_format:
            return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
        else:  # noqa: RET505
            return f"{int(minutes):02d}:{int(seconds):02d}"
