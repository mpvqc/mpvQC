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
def player_service_mock():
    return MagicMock(spec_set=PlayerService)


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with, state_service_mock, player_service_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(ImporterService, MagicMock(spec_set=ImporterService))
        binder.bind(PlayerService, player_service_mock)
        binder.bind(ResetService, MagicMock(spec_set=ResetService))
        binder.bind(StateService, state_service_mock)

    common_bindings_with(custom_bindings)


@pytest.fixture
def make_model(
    player_service_mock,
) -> Callable[[Iterable[Comment], int | float], tuple[MpvqcCommentModel, Callable[[int], None]]]:
    def _make_model(
        set_comments: Iterable[Comment],
        set_player_time: float = 0.0,
    ):
        player_service_mock.current_time = set_player_time

        def set_time(value: int):
            player_service_mock.current_time = value

        # noinspection PyCallingNonCallable
        model: MpvqcCommentModel = MpvqcCommentModel()
        model.import_comments(tuple(set_comments))

        return model, set_time

    return _make_model
