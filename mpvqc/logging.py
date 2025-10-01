# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import re
import sys
from collections.abc import Callable

from loguru import logger


def setup_mpvqc_logging() -> None:
    logging_format = (
        "<green>{time:HH:mm:ss.SSSSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    logger.remove()
    logger.add(sys.stdout, format=logging_format, level="DEBUG" if os.getenv("MPVQC_DEBUG", "") else "INFO")


def qt_log_handler() -> Callable:
    from PySide6.QtCore import QtMsgType

    def identify_qml_log_line(record) -> None:
        if (extra := record.get("extra")) and (override := extra["override"]) is not None:
            record["name"] = override["name"]
            record["line"] = override["line"]
            record["message"] = override["message"]

    patched_logger = logger.patch(identify_qml_log_line)

    levels = {
        QtMsgType.QtInfoMsg: patched_logger.info,
        QtMsgType.QtWarningMsg: patched_logger.warning,
        QtMsgType.QtCriticalMsg: patched_logger.error,
        QtMsgType.QtFatalMsg: patched_logger.critical,
        QtMsgType.QtDebugMsg: patched_logger.debug,
    }

    logger_name_pattern = re.compile(r"file::(.*?):(.*?):\s(.*?)$")

    def handler(message_type: QtMsgType, context, message):
        log_func = levels.get(message_type, patched_logger.error)
        if context.file:
            override = {
                "name": context.file.lstrip("file::/").replace("/", ".").rstrip(".qml"),
                "line": context.line,
                "message": message,
            }
        elif message.startswith("file") and (match := logger_name_pattern.match(message)) is not None:
            override = {
                "name": match.group(1).lstrip("/").replace("/", ".").rstrip(".qml"),
                "line": match.group(2).split(":")[0],
                "message": match.group(3),
            }
        else:
            override = {"name": "unknown", "line": "unknown", "message": message}

        log_func("", override=override)

    return handler
