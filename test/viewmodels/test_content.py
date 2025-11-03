# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest
from PySide6.QtCore import Qt

from mpvqc.services import PlayerService, SettingsService
from mpvqc.viewmodels import MpvqcContentViewModel


@pytest.fixture
def view_model():
    # noinspection PyCallingNonCallable
    return MpvqcContentViewModel()


@pytest.fixture
def player_service_mock():
    return MagicMock(spec_set=PlayerService)


@pytest.fixture
def open_comment_menu_spy(view_model, make_spy):
    return make_spy(view_model.openNewCommentMenuRequested)


@pytest.fixture
def toggle_fullscreen_spy(view_model, make_spy):
    return make_spy(view_model.toggleFullScreenRequested)


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock, settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service)

    common_bindings_with(custom_bindings)


class KeyPressTestCase(NamedTuple):
    name: str
    key: Qt.Key
    modifiers: Qt.KeyboardModifier
    is_auto_repeat: bool
    expected_open_comment_menu_count: int
    expected_toggle_fullscreen_count: int
    expected_player_call_count: int


@pytest.mark.parametrize(
    "test_case",
    [
        KeyPressTestCase(
            name="plain_press_e_opens_comment_menu",
            key=Qt.Key.Key_E,
            modifiers=Qt.KeyboardModifier.NoModifier,
            is_auto_repeat=False,
            expected_open_comment_menu_count=1,
            expected_toggle_fullscreen_count=0,
            expected_player_call_count=0,
        ),
        KeyPressTestCase(
            name="plain_press_f_toggles_fullscreen",
            key=Qt.Key.Key_F,
            modifiers=Qt.KeyboardModifier.NoModifier,
            is_auto_repeat=False,
            expected_open_comment_menu_count=0,
            expected_toggle_fullscreen_count=1,
            expected_player_call_count=0,
        ),
        KeyPressTestCase(
            name="ctrl_e_passed_to_player",
            key=Qt.Key.Key_E,
            modifiers=Qt.KeyboardModifier.ControlModifier,
            is_auto_repeat=False,
            expected_open_comment_menu_count=0,
            expected_toggle_fullscreen_count=0,
            expected_player_call_count=1,
        ),
        KeyPressTestCase(
            name="auto_repeat_f_swallowed",
            key=Qt.Key.Key_F,
            modifiers=Qt.KeyboardModifier.NoModifier,
            is_auto_repeat=True,
            expected_open_comment_menu_count=0,
            expected_toggle_fullscreen_count=0,
            expected_player_call_count=0,
        ),
        KeyPressTestCase(
            name="space_passed_to_player",
            key=Qt.Key.Key_Space,
            modifiers=Qt.KeyboardModifier.NoModifier,
            is_auto_repeat=False,
            expected_open_comment_menu_count=0,
            expected_toggle_fullscreen_count=0,
            expected_player_call_count=1,
        ),
        KeyPressTestCase(
            name="return_with_ctrl_passed_to_player",
            key=Qt.Key.Key_Return,
            modifiers=Qt.KeyboardModifier.ControlModifier,
            is_auto_repeat=False,
            expected_open_comment_menu_count=0,
            expected_toggle_fullscreen_count=0,
            expected_player_call_count=1,
        ),
    ],
    ids=lambda d: d.name,
)
def test_on_key_pressed(
    view_model,
    player_service_mock,
    open_comment_menu_spy,
    toggle_fullscreen_spy,
    test_case: KeyPressTestCase,
):
    view_model.onKeyPressed(test_case.key, test_case.modifiers, test_case.is_auto_repeat)

    assert open_comment_menu_spy.count() == test_case.expected_open_comment_menu_count
    assert toggle_fullscreen_spy.count() == test_case.expected_toggle_fullscreen_count
    assert player_service_mock.handle_key_event.call_count == test_case.expected_player_call_count


class KeyPressBlockedTestCase(NamedTuple):
    name: str
    key: Qt.Key
    modifiers: Qt.KeyboardModifier


@pytest.mark.parametrize(
    "test_case",
    [
        KeyPressBlockedTestCase(
            name="up_key",
            key=Qt.Key.Key_Up,
            modifiers=Qt.KeyboardModifier.NoModifier,
        ),
        KeyPressBlockedTestCase(
            name="down_key",
            key=Qt.Key.Key_Down,
            modifiers=Qt.KeyboardModifier.NoModifier,
        ),
        KeyPressBlockedTestCase(
            name="return_no_modifier",
            key=Qt.Key.Key_Return,
            modifiers=Qt.KeyboardModifier.NoModifier,
        ),
        KeyPressBlockedTestCase(
            name="escape_no_modifier",
            key=Qt.Key.Key_Escape,
            modifiers=Qt.KeyboardModifier.NoModifier,
        ),
        KeyPressBlockedTestCase(
            name="delete_no_modifier",
            key=Qt.Key.Key_Delete,
            modifiers=Qt.KeyboardModifier.NoModifier,
        ),
        KeyPressBlockedTestCase(
            name="backspace_no_modifier",
            key=Qt.Key.Key_Backspace,
            modifiers=Qt.KeyboardModifier.NoModifier,
        ),
        KeyPressBlockedTestCase(
            name="ctrl_f",
            key=Qt.Key.Key_F,
            modifiers=Qt.KeyboardModifier.ControlModifier,
        ),
        KeyPressBlockedTestCase(
            name="ctrl_c",
            key=Qt.Key.Key_C,
            modifiers=Qt.KeyboardModifier.ControlModifier,
        ),
        KeyPressBlockedTestCase(
            name="ctrl_z",
            key=Qt.Key.Key_Z,
            modifiers=Qt.KeyboardModifier.ControlModifier,
        ),
    ],
    ids=lambda d: d.name,
)
def test_on_key_pressed_blocked_keys(
    view_model,
    player_service_mock,
    open_comment_menu_spy,
    toggle_fullscreen_spy,
    test_case: KeyPressBlockedTestCase,
):
    view_model.onKeyPressed(test_case.key, test_case.modifiers, False)

    assert open_comment_menu_spy.count() == 0
    assert toggle_fullscreen_spy.count() == 0
    assert player_service_mock.handle_key_event.call_count == 0
