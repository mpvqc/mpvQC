# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from collections.abc import Callable, Iterable
from typing import Any
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.models import Comment
from mpvqc.pyobjects import MpvqcCommentModelPyObject
from mpvqc.services import PlayerService


class SignalHelper:
    """Helper class to help with signal logging"""

    def __init__(self):
        self.signals_fired = {}

    def log(self, signal_name: str, val=True):
        self.signals_fired[signal_name] = val

    def has_logged(self, signal_name: str) -> bool:
        return signal_name in self.signals_fired

    def logged_value(self, signal_name: str) -> Any:
        return self.signals_fired[signal_name]

    def reset(self):
        self.signals_fired = {}


@pytest.fixture
def signal_helper() -> SignalHelper:
    return SignalHelper()


@pytest.fixture(scope="session")
def make_model() -> Callable[[Iterable[Comment], int | float], tuple[MpvqcCommentModelPyObject, Callable[[int], None]]]:
    def _make_model(
        set_comments: Iterable[Comment],
        set_player_time: float = 0.0,
    ):
        # noinspection PyCallingNonCallable
        model: MpvqcCommentModelPyObject = MpvqcCommentModelPyObject()
        model.import_comments(list(set_comments))

        player_mock = MagicMock()
        player_mock.current_time = set_player_time

        def set_time(value: int):
            player_mock.current_time = value

        def config(binder: inject.Binder):
            binder.bind(PlayerService, player_mock)

        inject.configure(config, clear=True)

        return model, set_time

    return _make_model
