# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.comments.services import TimeFormatPolicyService
from mpvqc.comments.viewmodels import MpvqcCommentTableTimeFormatViewModel
from mpvqc.player.services import PlayerService


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, fake_player_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, fake_player_service)
        binder.bind_to_constructor(TimeFormatPolicyService, TimeFormatPolicyService)

    common_bindings_with(custom_bindings)


@pytest.fixture
def view_model() -> MpvqcCommentTableTimeFormatViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcCommentTableTimeFormatViewModel()


def test_mirrors_policy_and_forwards_a_flip(view_model, fake_player_service, make_spy):
    assert view_model.useLongFormat is False

    spy = make_spy(view_model.useLongFormatChanged)
    fake_player_service.update(duration=3600.0)

    assert view_model.useLongFormat
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) is True
