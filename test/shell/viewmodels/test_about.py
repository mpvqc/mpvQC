# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtGui import QGuiApplication

from mpvqc.shell.viewmodels import MpvqcAboutDialogViewModel

MODULE = "mpvqc.shell.viewmodels.about"
VERSION_LABEL = "1.0.0 (abc12345) mpvqc-github"


@pytest.fixture(autouse=True)
def patch_build_info(monkeypatch, make_build_info):
    build = make_build_info(version="1.0.0", is_release=True, origin="mpvqc-github")
    monkeypatch.setattr(f"{MODULE}.get_build_info", lambda: build)


@pytest.fixture
def view_model() -> MpvqcAboutDialogViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcAboutDialogViewModel()


def test_application_version_shows_version_label(view_model: MpvqcAboutDialogViewModel):
    assert view_model.applicationVersion == VERSION_LABEL


def test_copy_to_clipboard_copies_version_label(qt_app, view_model: MpvqcAboutDialogViewModel):
    view_model.copyVersionInfoToClipboard()

    assert QGuiApplication.clipboard().text() == VERSION_LABEL
