# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import logging
import os
import re
import sys
from enum import StrEnum
from logging.handlers import RotatingFileHandler
from typing import TYPE_CHECKING, Final, override

from PySide6.QtCore import QtMsgType, qInstallMessageHandler

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

    from PySide6.QtCore import QMessageLogContext

MPV_LEVEL: Final[int] = 25
logging.addLevelName(MPV_LEVEL, "MPV")

FILE_LOG_MAX_BYTES: Final[int] = 1_000_000
FILE_LOG_BACKUP_COUNT: Final[int] = 5

_URL_SCHEME_PATTERN: Final = re.compile(r"^\w+:")


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
    def __init__(self, *, colored: bool) -> None:
        super().__init__()
        self._use_color = colored

    @override
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

        message = (
            f"{color}{timestamp}{reset} | "
            f"{color}{level}{reset} | "
            f"{cyan}{record.name}:{record.lineno}{reset} | "
            f"{color}{record.getMessage()}{reset}"
        )

        if record.exc_info and not record.exc_text:
            record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            message = f"{message}\n{record.exc_text}"

        return message


def setup_mpvqc_logging() -> None:
    _setup_console_logging()
    _setup_file_logging()
    qInstallMessageHandler(_qt_log_handler())


def _setup_console_logging() -> None:
    is_debug = os.getenv("MPVQC_DEBUG")

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG if is_debug else logging.INFO)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(MpvqcFormatter(colored=use_color()))
    root_logger.addHandler(console_handler)

    if is_debug:
        logging.getLogger("mpvqc").setLevel(logging.DEBUG)
        for name in ("inject",):
            logging.getLogger(name).setLevel(logging.WARNING)


def _setup_file_logging() -> None:
    try:
        from mpvqc.services.application_paths import ApplicationPathsService

        paths = ApplicationPathsService()
        paths.dir_logs.mkdir(parents=True, exist_ok=True)
        attach_file_logging(paths.file_log)
    except Exception:
        logging.getLogger(__name__).exception("Could not set up file logging")


def attach_file_logging(log_file: Path) -> None:
    handler = RotatingFileHandler(
        log_file,
        maxBytes=FILE_LOG_MAX_BYTES,
        backupCount=FILE_LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    handler.setFormatter(MpvqcFormatter(colored=False))
    logging.getLogger().addHandler(handler)


def _qt_log_handler() -> Callable[[QtMsgType, QMessageLogContext, str], None]:
    levels: Final[dict[QtMsgType, int]] = {
        QtMsgType.QtDebugMsg: logging.DEBUG,
        QtMsgType.QtInfoMsg: logging.INFO,
        QtMsgType.QtWarningMsg: logging.WARNING,
        QtMsgType.QtCriticalMsg: logging.ERROR,
        QtMsgType.QtFatalMsg: logging.CRITICAL,
    }

    def handler(message_type: QtMsgType, context: QMessageLogContext, message: str) -> None:
        file = str(context.file) if context.file else None

        if file:
            logger_name = logger_name_from(file)
            line = context.line if isinstance(context.line, int) else 0
        else:
            logger_name = "unknown"
            line = 0

        log_level = levels.get(message_type, logging.ERROR)
        qml_logger = logging.getLogger(logger_name)

        record = qml_logger.makeRecord(
            name=logger_name,
            level=log_level,
            fn="",
            lno=line,
            msg=message,
            args=(),
            exc_info=None,
        )
        qml_logger.handle(record)

    return handler


def logger_name_from(path: str) -> str:
    path = _URL_SCHEME_PATTERN.sub("", path).lstrip("/").removeprefix("qt/qml/")
    return path.replace("/", ".").removesuffix(".qml")
