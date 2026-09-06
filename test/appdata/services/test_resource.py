# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.appdata.services import read_input_conf, read_mpv_conf


def test_resources():
    assert read_input_conf()


def test_mpv_conf_windows(monkeypatch):
    monkeypatch.setattr("sys.platform", "win32")
    assert "vo=gpu" in read_mpv_conf().splitlines()


@pytest.mark.parametrize("platform", ["linux", "darwin"])
def test_mpv_conf_non_windows(monkeypatch, platform):
    monkeypatch.setattr("sys.platform", platform)
    assert not any(line.startswith("vo=") for line in read_mpv_conf().splitlines())
