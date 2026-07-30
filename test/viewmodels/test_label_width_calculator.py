# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest
from PySide6.QtCore import QObject, Signal

from mpvqc.services import (
    CommentTypesPolicyService,
    FontLoaderService,
    InternationalizationService,
    LabelWidthCalculatorService,
    PlayerService,
    TimeFormatPolicyService,
)
from mpvqc.viewmodels import MpvqcLabelWidthCalculatorViewModel


class CommentTypesPolicyServiceMock(QObject):
    """Doubles the policy surface the view model consumes: a real signal, a stubbed accessor."""

    displayable_comment_types_changed = Signal(frozenset)

    def __init__(self):
        super().__init__()
        assert isinstance(CommentTypesPolicyService.displayable_comment_types_changed, Signal), (
            "mocked surface drifted: not a signal anymore"
        )
        assert isinstance(CommentTypesPolicyService.displayable_comment_types, property), (
            "mocked surface drifted: not a property anymore"
        )
        self._types: frozenset[str] = frozenset()

    @property
    def displayable_comment_types(self) -> frozenset[str]:
        return self._types

    def change_displayable_types(self, *types: str) -> None:
        self._types = frozenset(types)
        self.displayable_comment_types_changed.emit(self._types)


@pytest.fixture
def comment_types_policy_mock() -> CommentTypesPolicyServiceMock:
    return CommentTypesPolicyServiceMock()


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, player_service_mock, comment_types_policy_mock):
    def custom_bindings(binder: inject.Binder):
        binder.bind(PlayerService, player_service_mock)
        binder.bind(CommentTypesPolicyService, comment_types_policy_mock)
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


def test_comment_types_width_follows_displayable_types(view_model, comment_types_policy_mock, make_spy):
    spy = make_spy(view_model.commentTypesLabelWidthChanged)

    comment_types_policy_mock.change_displayable_types("i")
    narrow_width = view_model.commentTypesLabelWidth
    assert narrow_width > 0
    assert spy.count() == 1

    comment_types_policy_mock.change_displayable_types("i", "Wwwwwwwwwwwwwwwwwwww")
    wide_width = view_model.commentTypesLabelWidth
    assert wide_width > narrow_width
    assert spy.count() == 2
    assert spy.at(invocation=1, argument=0) == wide_width

    comment_types_policy_mock.change_displayable_types("i")
    assert view_model.commentTypesLabelWidth == narrow_width
    assert spy.count() == 3


def test_comment_types_width_recomputes_on_retranslation(qt_app, view_model, comment_types_policy_mock, make_spy):
    comment_types_policy_mock.change_displayable_types("Translation")
    spy = make_spy(view_model.commentTypesLabelWidthChanged)
    english_width = view_model.commentTypesLabelWidth
    assert english_width > 0

    inject.instance(InternationalizationService).retranslate(qt_app, "de-DE")

    assert view_model.commentTypesLabelWidth != english_width
    assert spy.count() == 1
    assert spy.at(invocation=0, argument=0) == view_model.commentTypesLabelWidth


def test_unknown_type_measures_verbatim_after_retranslation(qt_app, view_model, comment_types_policy_mock):
    comment_types_policy_mock.change_displayable_types("CustomTypeXyz")
    english_width = view_model.commentTypesLabelWidth
    assert english_width > 0

    inject.instance(InternationalizationService).retranslate(qt_app, "de-DE")

    assert view_model.commentTypesLabelWidth == english_width


def test_comment_types_width_of_same_value_does_not_emit(view_model, comment_types_policy_mock, make_spy):
    comment_types_policy_mock.change_displayable_types("Wwwwwwwwww")
    spy = make_spy(view_model.commentTypesLabelWidthChanged)

    comment_types_policy_mock.change_displayable_types("Wwwwwwwwww", "i")

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
