# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import logging
import sys
from typing import NamedTuple

import pytest

from mpvqc.logging_utils import MpvqcFormatter, attach_file_logging, logger_name_from, use_color


class UseColorTestCase(NamedTuple):
    env_var: str | None
    is_tty: bool
    expected: bool


@pytest.fixture(autouse=True)
def clean_env(monkeypatch):
    monkeypatch.delenv("NO_COLOR", raising=False)


@pytest.mark.parametrize(
    "test_case",
    [
        UseColorTestCase(env_var="1", is_tty=True, expected=False),
        UseColorTestCase(env_var="yes", is_tty=True, expected=False),
        UseColorTestCase(env_var="", is_tty=True, expected=True),
        UseColorTestCase(env_var=None, is_tty=True, expected=True),
        UseColorTestCase(env_var=None, is_tty=False, expected=False),
        UseColorTestCase(env_var="", is_tty=False, expected=False),
    ],
)
def test_use_color(monkeypatch, test_case: UseColorTestCase):
    if test_case.env_var is not None:
        monkeypatch.setenv("NO_COLOR", test_case.env_var)
    monkeypatch.setattr("sys.stdout.isatty", lambda: test_case.is_tty)
    assert use_color() == test_case.expected


class LoggerNameCase(NamedTuple):
    name: str
    raw: str
    expected: str


@pytest.mark.parametrize(
    "case",
    [
        LoggerNameCase(
            name="qrc root file",
            raw="qrc:/qt/qml/MpvqcApplicationLinux.qml",
            expected="MpvqcApplicationLinux",
        ),
        LoggerNameCase(
            name="trailing qml chars kept",
            raw="qrc:/qt/qml/MpvqcOverlayPanel.qml",
            expected="MpvqcOverlayPanel",
        ),
        LoggerNameCase(
            name="nested module path",
            raw="qrc:/qt/qml/io/github/mpvqc/mpvQC/Views/Player/MpvqcPlayerView.qml",
            expected="io.github.mpvqc.mpvQC.Views.Player.MpvqcPlayerView",
        ),
    ],
    ids=lambda case: case.name,
)
def test_logger_name_from(case: LoggerNameCase):
    assert logger_name_from(case.raw) == case.expected


class FormatterColorCase(NamedTuple):
    name: str
    colored: bool
    expect_ansi: bool


@pytest.mark.parametrize(
    "case",
    [
        FormatterColorCase(name="colored emits ansi escapes", colored=True, expect_ansi=True),
        FormatterColorCase(name="plain has no ansi escapes", colored=False, expect_ansi=False),
    ],
    ids=lambda case: case.name,
)
def test_formatter_color(case: FormatterColorCase):
    formatter = MpvqcFormatter(colored=case.colored)
    record = logging.LogRecord("mpvqc", logging.INFO, "path", 1, "the message", None, None)
    assert ("\033[" in formatter.format(record)) == case.expect_ansi


def test_formatter_appends_exception_traceback():
    formatter = MpvqcFormatter(colored=False)
    try:
        msg = "boom"
        raise ValueError(msg)
    except ValueError:
        record = logging.LogRecord("mpvqc", logging.ERROR, "path", 1, "the message", None, sys.exc_info())

    formatted = formatter.format(record)

    assert "the message" in formatted
    assert "Traceback" in formatted
    assert "ValueError: boom" in formatted


@pytest.fixture
def isolated_root_logger():
    root = logging.getLogger()
    saved_handlers = root.handlers[:]
    saved_level = root.level
    root.handlers = []
    root.setLevel(logging.DEBUG)
    yield root
    for handler in root.handlers:
        handler.close()
    root.handlers = saved_handlers
    root.setLevel(saved_level)


def test_attach_file_logging_writes_plain_records(tmp_path, isolated_root_logger):
    log_file = tmp_path / "mpvQC.log"

    attach_file_logging(log_file)
    logging.getLogger("mpvqc.filetest").info("hello-from-file-test")
    for handler in isolated_root_logger.handlers:
        handler.flush()

    content = log_file.read_text(encoding="utf-8")
    assert "hello-from-file-test" in content
    assert "\033[" not in content
