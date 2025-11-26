# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.logging_utils import use_color


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
