# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
from collections.abc import Callable


def setup_mpvqc_logging() -> None:
    logging.basicConfig(level=logging.WARNING, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    mpvqc_loggers = logging.getLogger("mpvqc")
    mpvqc_loggers.setLevel(logging.DEBUG if os.getenv("MPVQC_DEBUG", "") else logging.INFO)


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
