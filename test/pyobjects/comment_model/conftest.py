# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Iterable
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.models import Comment
from mpvqc.pyobjects import MpvqcCommentModelPyObject
from mpvqc.services import PlayerService


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
