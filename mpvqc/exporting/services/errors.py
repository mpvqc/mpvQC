# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later


class ExportError(Exception):
    __match_args__ = ("message", "lineno")

    def __init__(self, message: str, lineno: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.lineno = lineno
