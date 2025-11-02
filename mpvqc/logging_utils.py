# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import re
import sys
from collections.abc import Callable

import colorlog

MPV_LEVEL = 25
logging.addLevelName(MPV_LEVEL, "MPV")


MPVQC_LOG_FMT = (
    "%(log_color)s%(asctime)s%(reset)s | "
    "%(log_color)s%(levelname)-8s%(reset)s | "
    "%(cyan)s%(name)s:%(lineno)d%(reset)s | "
    "%(log_color)s%(message)s%(reset)s"
)

MPV_LOG_FMT = (
    "%(log_color)s%(asctime)s%(reset)s | "
    "%(log_color)s%(levelname)-8s%(reset)s | "
    "%(mpv_level)s • %(mpv_context)s • "
    "%(log_color)s%(message)s%(reset)s"
)


class DualFormatColoredFormatter(colorlog.ColoredFormatter):
    def __init__(self):
        super().__init__(
            fmt=MPVQC_LOG_FMT,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bold",
                "MPV": "purple",
            },
            style="%",
        )
        self.mpv_fmt = MPV_LOG_FMT
        self.standard_fmt = MPVQC_LOG_FMT

    def format(self, record):
        if record.levelname == "MPV":
            self._style._fmt = self.mpv_fmt  # noqa: SLF001
        else:
            self._style._fmt = self.standard_fmt  # noqa: SLF001

        return super().format(record)


def setup_mpvqc_logging() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if os.getenv("MPVQC_DEBUG", "") else logging.INFO)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(DualFormatColoredFormatter())
    root_logger.addHandler(console_handler)


def qt_log_handler() -> Callable:
    from PySide6.QtCore import QtMsgType

    levels = {
        QtMsgType.QtInfoMsg: logging.INFO,
        QtMsgType.QtWarningMsg: logging.WARNING,
        QtMsgType.QtCriticalMsg: logging.ERROR,
        QtMsgType.QtFatalMsg: logging.CRITICAL,
        QtMsgType.QtDebugMsg: logging.DEBUG,
    }

    logger_name_pattern = re.compile(r"file::(.*?):(.*?):\s(.*?)$")

    def handler(message_type: QtMsgType, context, message):
        if context.file:
            logger_name = context.file.lstrip("file::/").replace("/", ".").rstrip(".qml")
            line = int(context.line)
            msg = message
        elif message.startswith("file") and (match := logger_name_pattern.match(message)) is not None:
            logger_name = match.group(1).lstrip("/").replace("/", ".").rstrip(".qml")
            line = int(match.group(2).split(":")[0].strip())
            msg = match.group(3)
        else:
            logger_name = "unknown"
            line = 0
            msg = message

        log_level = levels.get(message_type, logging.ERROR)
        qml_logger = logging.getLogger(logger_name)

        record = qml_logger.makeRecord(
            name=logger_name,
            level=log_level,
            fn="",
            lno=line,
            msg=msg,
            args=(),
            exc_info=None,
        )
        qml_logger.handle(record)

    return handler
