# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.comments.viewmodels import MpvqcCommentPlaceholderViewModel
from mpvqc.shell.services import ShellSettingsService


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, shell_settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ShellSettingsService, shell_settings_service)

    common_bindings_with(custom_bindings)


def test_mirrors_settings_and_forwards_a_change(shell_settings_service, make_spy):
    shell_settings_service.layout_orientation = Qt.Orientation.Vertical.value
    # noinspection PyCallingNonCallable
    view_model = MpvqcCommentPlaceholderViewModel()
    assert view_model.layoutOrientation == Qt.Orientation.Vertical.value

    spy = make_spy(view_model.layoutOrientationChanged)
    shell_settings_service.layout_orientation = Qt.Orientation.Horizontal.value

    assert view_model.layoutOrientation == Qt.Orientation.Horizontal.value
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == Qt.Orientation.Horizontal.value
