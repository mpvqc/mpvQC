# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.services import (
    FontLoaderService,
    InternationalizationService,
    LabelWidthCalculatorService,
    PlayerService,
    SettingsService,
    TimeFormatPolicyService,
)
from mpvqc.viewmodels import MpvqcLabelWidthCalculatorViewModel


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock, settings_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind(SettingsService, settings_service)
        binder.bind_to_constructor(FontLoaderService, FontLoaderService)
        binder.bind_to_constructor(InternationalizationService, InternationalizationService)
        binder.bind_to_constructor(LabelWidthCalculatorService, LabelWidthCalculatorService)
        binder.bind_to_constructor(TimeFormatPolicyService, TimeFormatPolicyService)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def view_model() -> MpvqcLabelWidthCalculatorViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcLabelWidthCalculatorViewModel()


def test_comment_types_width_recomputes_on_retranslation(qt_app, view_model, make_spy):
    spy = make_spy(view_model.commentTypesLabelWidthChanged)
    english_width = view_model.commentTypesLabelWidth
    assert english_width > 0

    inject.instance(InternationalizationService).retranslate(qt_app, "de-DE")

    assert view_model.commentTypesLabelWidth != english_width
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == view_model.commentTypesLabelWidth


def test_comment_types_width_recomputes_on_comment_types_change(view_model, settings_service, make_spy):
    spy = make_spy(view_model.commentTypesLabelWidthChanged)

    settings_service.comment_types = ["i"]
    narrow_width = view_model.commentTypesLabelWidth
    assert spy.count() == 1

    settings_service.comment_types = ["Wwwwwwwwwwwwwwwwwwww"]

    assert view_model.commentTypesLabelWidth > narrow_width
    assert spy.count() == 2


def test_comment_types_width_of_same_value_does_not_emit(view_model, settings_service, make_spy):
    settings_service.comment_types = ["Wwwwwwwwww"]
    spy = make_spy(view_model.commentTypesLabelWidthChanged)

    settings_service.comment_types = ["Wwwwwwwwww", "i"]

    assert spy.count() == 0


def test_time_width_flips_with_format(view_model, player_service_mock, make_spy):
    spy = make_spy(view_model.timeLabelWidthChanged)
    short_width = view_model.timeLabelWidth
    assert short_width > 0

    player_service_mock.update(duration=3600.0)

    long_width = view_model.timeLabelWidth
    assert long_width > short_width
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == long_width

    player_service_mock.update(duration=3599.0)

    assert view_model.timeLabelWidth == short_width
    assert spy.count() == 2
