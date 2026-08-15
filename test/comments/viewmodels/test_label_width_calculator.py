# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable
from typing import NamedTuple

import inject
import pytest

from mpvqc.comments.services import CommentsSettingsService, CommentTypesPolicyService, TimeFormatPolicyService
from mpvqc.comments.viewmodels import (
    CommentLabelWidthCalculatorInputs,
    CommentLabelWidthCalculatorProps,
    MpvqcCommentLabelWidthCalculatorViewModel,
    derive_comment_label_width_calculator_props,
)
from mpvqc.services import FontLoaderService, InternationalizationService, LabelWidthCalculatorService, PlayerService


@pytest.fixture(autouse=True)
def configure_inject(common_bindings_with, comments_settings_service, fake_player_service):
    def custom_bindings(binder: inject.Binder):
        binder.bind(CommentsSettingsService, comments_settings_service)
        binder.bind(PlayerService, fake_player_service)
        binder.bind_to_constructor(CommentTypesPolicyService, CommentTypesPolicyService)
        binder.bind_to_constructor(TimeFormatPolicyService, TimeFormatPolicyService)
        binder.bind_to_constructor(FontLoaderService, FontLoaderService)
        binder.bind_to_constructor(LabelWidthCalculatorService, LabelWidthCalculatorService)

    common_bindings_with(custom_bindings)


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


@pytest.fixture
def view_model() -> MpvqcCommentLabelWidthCalculatorViewModel:
    # noinspection PyCallingNonCallable
    return MpvqcCommentLabelWidthCalculatorViewModel()


@pytest.fixture
def spy_notifies(make_spy):
    def _spy(view_model: MpvqcCommentLabelWidthCalculatorViewModel) -> dict:
        return {
            "commentTypesLabelWidth": make_spy(view_model.commentTypesLabelWidthChanged),
            "timeLabelWidth": make_spy(view_model.timeLabelWidthChanged),
        }

    return _spy


def emissions(spies: dict) -> dict[str, int]:
    return {name: spy.count() for name, spy in spies.items()}


def measure_by_length(texts: Iterable[str]) -> int:
    return max((len(text) for text in texts), default=0)


class DerivationCase(NamedTuple):
    name: str
    inputs: CommentLabelWidthCalculatorInputs
    expected: CommentLabelWidthCalculatorProps


@pytest.mark.parametrize(
    "case",
    [
        DerivationCase(
            name="no comment types leave that column at zero",
            inputs=CommentLabelWidthCalculatorInputs(
                displayable_comment_types=frozenset(),
                comment_type_labels=(),
                table_long_format=False,
            ),
            expected=CommentLabelWidthCalculatorProps(comment_types_label_width=0, time_label_width=len("00:00")),
        ),
        DerivationCase(
            name="the longest label sets the comment types width",
            inputs=CommentLabelWidthCalculatorInputs(
                displayable_comment_types=frozenset({"i", "Spelling"}),
                comment_type_labels=("i", "Spelling"),
                table_long_format=False,
            ),
            expected=CommentLabelWidthCalculatorProps(
                comment_types_label_width=len("Spelling"),
                time_label_width=len("00:00"),
            ),
        ),
        DerivationCase(
            name="the long format widens the time column",
            inputs=CommentLabelWidthCalculatorInputs(
                displayable_comment_types=frozenset({"i"}),
                comment_type_labels=("i",),
                table_long_format=True,
            ),
            expected=CommentLabelWidthCalculatorProps(
                comment_types_label_width=len("i"),
                time_label_width=len("00:00:00"),
            ),
        ),
    ],
    ids=lambda case: case.name,
)
def test_derivation(case: DerivationCase):
    assert derive_comment_label_width_calculator_props(case.inputs, measure_by_length) == case.expected


def test_comment_types_width_follows_displayable_types(view_model, comments_settings_service, spy_notifies):
    spies = spy_notifies(view_model)

    comments_settings_service.comment_types = ["i"]
    narrow_width = view_model.commentTypesLabelWidth
    assert narrow_width > 0
    assert spies["commentTypesLabelWidth"].count() == 1

    comments_settings_service.comment_types = ["i", "Wwwwwwwwwwwwwwwwwwww"]
    wide_width = view_model.commentTypesLabelWidth
    assert wide_width > narrow_width
    assert spies["commentTypesLabelWidth"].count() == 2
    assert spies["commentTypesLabelWidth"].at(invocation=1, argument=0) == wide_width

    comments_settings_service.comment_types = ["i"]
    assert view_model.commentTypesLabelWidth == narrow_width

    assert emissions(spies) == {"commentTypesLabelWidth": 3, "timeLabelWidth": 0}


def test_comment_types_width_recomputes_on_retranslation(qt_app, view_model, comments_settings_service, spy_notifies):
    # "Spelling" -> "Rechtschreibung" grows on every font engine; near-equal pairs tie on Windows.
    comments_settings_service.comment_types = ["Spelling"]
    spies = spy_notifies(view_model)
    english_width = view_model.commentTypesLabelWidth
    assert english_width > 0

    inject.instance(InternationalizationService).retranslate(qt_app, "de-DE")

    assert view_model.commentTypesLabelWidth > english_width
    assert emissions(spies) == {"commentTypesLabelWidth": 1, "timeLabelWidth": 0}
    assert spies["commentTypesLabelWidth"].at(invocation=0, argument=0) == view_model.commentTypesLabelWidth


def test_unknown_type_measures_verbatim_after_retranslation(
    qt_app, view_model, comments_settings_service, spy_notifies
):
    comments_settings_service.comment_types = ["CustomTypeXyz"]
    spies = spy_notifies(view_model)
    english_width = view_model.commentTypesLabelWidth
    assert english_width > 0

    inject.instance(InternationalizationService).retranslate(qt_app, "de-DE")

    assert view_model.commentTypesLabelWidth == english_width
    assert emissions(spies) == {"commentTypesLabelWidth": 0, "timeLabelWidth": 0}


def test_comment_types_width_of_same_value_does_not_emit(view_model, comments_settings_service, spy_notifies):
    comments_settings_service.comment_types = ["Wwwwwwwwww"]
    spies = spy_notifies(view_model)

    comments_settings_service.comment_types = ["Wwwwwwwwww", "i"]

    assert emissions(spies) == {"commentTypesLabelWidth": 0, "timeLabelWidth": 0}


def test_time_width_flips_with_format(view_model, fake_player_service, spy_notifies):
    spies = spy_notifies(view_model)
    short_width = view_model.timeLabelWidth
    assert short_width > 0

    fake_player_service.update(duration=3600.0)

    long_width = view_model.timeLabelWidth
    assert long_width > short_width
    assert spies["timeLabelWidth"].count() == 1
    assert spies["timeLabelWidth"].at(invocation=0, argument=0) == long_width

    fake_player_service.update(duration=3599.0)

    assert view_model.timeLabelWidth == short_width
    assert emissions(spies) == {"commentTypesLabelWidth": 0, "timeLabelWidth": 2}


def test_props_swap_completes_before_the_comment_types_emission(view_model, comments_settings_service):
    comments_settings_service.comment_types = ["i"]
    narrow_width = view_model.commentTypesLabelWidth
    observed: list[tuple[int, int]] = []

    view_model.commentTypesLabelWidthChanged.connect(
        lambda _: observed.append((view_model.commentTypesLabelWidth, view_model.timeLabelWidth))
    )

    comments_settings_service.comment_types = ["Wwwwwwwwwwwwwwwwwwww"]

    settled = (view_model.commentTypesLabelWidth, view_model.timeLabelWidth)
    assert observed == [settled]
    assert settled[0] > narrow_width


def test_props_swap_completes_before_the_time_emission(view_model, fake_player_service):
    short_width = view_model.timeLabelWidth
    observed: list[tuple[int, int]] = []

    view_model.timeLabelWidthChanged.connect(
        lambda _: observed.append((view_model.commentTypesLabelWidth, view_model.timeLabelWidth))
    )

    fake_player_service.update(duration=3600.0)

    settled = (view_model.commentTypesLabelWidth, view_model.timeLabelWidth)
    assert observed == [settled]
    assert settled[1] > short_width
