# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Iterable
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.datamodels import Comment
from mpvqc.models import MpvqcCommentModel
from mpvqc.services import ImporterService, PlayerService, ResetService, StateService


@pytest.fixture
def state_service_mock():
    return MagicMock(spec_set=StateService)


@pytest.fixture
def make_model(
    ubiquitous_bindings,
    state_service_mock,
) -> Callable[[Iterable[Comment], int | float], tuple[MpvqcCommentModel, Callable[[int], None]]]:
    def _make_model(
        set_comments: Iterable[Comment],
        set_player_time: float = 0.0,
    ):
        player_mock = MagicMock(spec_set=PlayerService)
        player_mock.current_time = set_player_time

        def set_time(value: int):
            player_mock.current_time = value

        def config(binder: inject.Binder):
            binder.install(ubiquitous_bindings)
            binder.bind(StateService, state_service_mock)
            binder.bind(ResetService, MagicMock(spec_set=ResetService))
            binder.bind(ImporterService, MagicMock(spec_set=ImporterService))
            binder.bind(PlayerService, player_mock)

        inject.configure(config, bind_in_runtime=False, clear=True)

        # noinspection PyCallingNonCallable
        model: MpvqcCommentModel = MpvqcCommentModel()
        model.import_comments(tuple(set_comments))

        return model, set_time

    return _make_model
