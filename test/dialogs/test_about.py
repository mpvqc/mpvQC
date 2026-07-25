# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtGui import QGuiApplication

from mpvqc.dialogs import MpvqcAboutDialogViewModel
from mpvqc.services import BuildInfoService

VERSION_INFO = "1.0.0 (abc12345) mpvqc-github"


@pytest.fixture
def build_info_service_mock() -> MagicMock:
    mock = MagicMock(spec_set=BuildInfoService)
    mock.version_info = VERSION_INFO
    return mock


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, build_info_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(BuildInfoService, build_info_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcAboutDialogViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcAboutDialogViewModel()


def test_application_version_shows_version_info(view_model: MpvqcAboutDialogViewModel):
    assert view_model.applicationVersion == VERSION_INFO


def test_copy_to_clipboard_copies_version_info(qt_app, view_model: MpvqcAboutDialogViewModel):
    view_model.copyVersionInfoToClipboard()

    assert QGuiApplication.clipboard().text() == VERSION_INFO
