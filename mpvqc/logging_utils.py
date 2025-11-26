# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import os
import re
import sys
from collections.abc import Callable
from enum import StrEnum
from typing import Final

MPV_LEVEL: Final[int] = 25
logging.addLevelName(MPV_LEVEL, "MPV")


class AnsiColor(StrEnum):
    RESET = "\033[0m"
    CYAN = "\033[36m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    RED = "\033[31m"
    RED_BOLD = "\033[1;31m"
    PURPLE = "\033[35m"


LEVEL_COLORS: Final[dict[int, AnsiColor]] = {
    logging.DEBUG: AnsiColor.CYAN,
    logging.INFO: AnsiColor.GREEN,
    logging.WARNING: AnsiColor.YELLOW,
    logging.ERROR: AnsiColor.RED,
    logging.CRITICAL: AnsiColor.RED_BOLD,
    MPV_LEVEL: AnsiColor.PURPLE,
}


def use_color() -> bool:
    if os.getenv("NO_COLOR"):
        return False
    return sys.stdout.isatty()


class MpvqcFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__()
        self._use_color = use_color()

    def format(self, record: logging.LogRecord) -> str:
        if self._use_color:
            color = LEVEL_COLORS.get(record.levelno, AnsiColor.RESET)
            reset = AnsiColor.RESET
            cyan = AnsiColor.CYAN
        else:
            color = reset = cyan = ""

        timestamp = self.formatTime(record, self.datefmt)
        level = record.levelname.ljust(8)

        if record.levelname == "MPV":
            mpv_level = getattr(record, "mpv_level", "?")
            mpv_context = getattr(record, "mpv_context", "?")
            return (
                f"{color}{timestamp}{reset} | "
                f"{color}{level}{reset} | "
                f"{mpv_level} • {mpv_context} • "
                f"{color}{record.getMessage()}{reset}"
            )

        return (
            f"{color}{timestamp}{reset} | "
            f"{color}{level}{reset} | "
            f"{cyan}{record.name}:{record.lineno}{reset} | "
            f"{color}{record.getMessage()}{reset}"
        )


def setup_mpvqc_logging() -> None:
    is_debug = os.getenv("MPVQC_DEBUG")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(MpvqcFormatter())
    root_logger.addHandler(console_handler)

    if is_debug:
        logging.getLogger("mpvqc").setLevel(logging.DEBUG)
        for name in ("inject",):
            logging.getLogger(name).setLevel(logging.WARNING)


def qt_log_handler() -> Callable:
    from PySide6.QtCore import QtMsgType

    levels: Final[dict[QtMsgType, int]] = {
        QtMsgType.QtDebugMsg: logging.DEBUG,
        QtMsgType.QtInfoMsg: logging.INFO,
        QtMsgType.QtWarningMsg: logging.WARNING,
        QtMsgType.QtCriticalMsg: logging.ERROR,
        QtMsgType.QtFatalMsg: logging.CRITICAL,
    }

    logger_name_pattern = re.compile(r"file::(.*?):(.*?):\s(.*?)$")

    def handler(message_type: QtMsgType, context, message):
        if context.file:
            logger_name = context.file.lstrip("file::/").replace("/", ".").rstrip(".qml")
            line = int(context.line)
            msg = message
        elif message.startswith("file") and (match := logger_name_pattern.match(message)):
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
