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

from typing import Callable, Iterable
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


@pytest.fixture(scope="session")
def make_model() -> Callable[[Iterable[Comment], int | float], MpvqcCommentModelPyObject]:
    def _make_model(
        set_comments: Iterable[Comment],
        set_player_time: int | float = 0,
    ):
        # noinspection PyCallingNonCallable
        model: MpvqcCommentModelPyObject = MpvqcCommentModelPyObject()
        model.import_comments(list(set_comments))

        player_mock = MagicMock()
        player_mock.current_time = set_player_time

        def config(binder: inject.Binder):
            binder.bind(PlayerService, player_mock)

        inject.configure(config, clear=True)

        return model

    return _make_model


@pytest.fixture()
def signal_helper() -> SignalHelper:
    return SignalHelper()
