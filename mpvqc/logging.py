# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable


def qt_log_handler() -> Callable:
    from PySide6.QtCore import QtMsgType

    levels = {
        QtMsgType.QtInfoMsg: "INFO",
        QtMsgType.QtWarningMsg: "WARNING",
        QtMsgType.QtCriticalMsg: "CRITICAL",
        QtMsgType.QtFatalMsg: "FATAL",
        QtMsgType.QtDebugMsg: "DEBUG",
    }

    def handler(message_type: QtMsgType, _, message):
        level = levels.get(message_type)
        print(f"{level} {message}")

    return handler
