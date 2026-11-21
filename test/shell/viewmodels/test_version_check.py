# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import sys
from typing import TYPE_CHECKING, NamedTuple

import pytest
from shiboken6 import delete

from mpvqc.shell.services import (
    CheckOutcome,
    NewVersionAvailable,
    ServerError,
    ServerNotReachable,
    UpToDate,
    VersionCheckerService,
)
from mpvqc.shell.viewmodels import MpvqcVersionCheckMessageBoxViewModel, derive_version_check_props

if TYPE_CHECKING:
    import inject

    from test.conftest import ManualJobExecutor


class PresentCase(NamedTuple):
    name: str
    outcome: CheckOutcome
    expected_title: str


PRESENT_CASES = [
    PresentCase(
        name="server error",
        outcome=ServerError(code=500),
        expected_title="Server Error",
    ),
    PresentCase(
        name="server not reachable",
        outcome=ServerNotReachable(),
        expected_title="Server Not Reachable",
    ),
    PresentCase(
        name="new version available",
        outcome=NewVersionAvailable(version="9.9.9"),
        expected_title="New Version Available",
    ),
    PresentCase(
        name="up to date",
        outcome=UpToDate(),
        expected_title="👌",
    ),
]


@pytest.mark.parametrize("case", PRESENT_CASES, ids=lambda case: case.name)
def test_derive_maps_outcome_to_title(case: PresentCase) -> None:
    props = derive_version_check_props(case.outcome)

    assert props.title == case.expected_title
    assert props.text


def test_derive_escapes_remote_version() -> None:
    props = derive_version_check_props(NewVersionAvailable(version="1.2.3<script>"))

    assert "&lt;script&gt;" in props.text
    assert "1.2.3<script>" not in props.text


NEW_VERSION = derive_version_check_props(NewVersionAvailable(version="9.9.9"))


@pytest.fixture
def checker(qt_app, manual_executor: ManualJobExecutor) -> VersionCheckerService:
    return VersionCheckerService(manual_executor, fetch=lambda: "9.9.9")


@pytest.fixture
def configure_inject(common_bindings_with, checker: VersionCheckerService) -> None:
    def custom_bindings(binder: inject.Binder):
        binder.bind(VersionCheckerService, checker)

    common_bindings_with(custom_bindings)


@pytest.fixture
def uncaught_exceptions(monkeypatch: pytest.MonkeyPatch) -> list[BaseException]:
    """PySide hands an exception raised in a slot to sys.excepthook instead of the caller."""
    caught: list[BaseException] = []
    monkeypatch.setattr(sys, "excepthook", lambda _type, value, _traceback: caught.append(value))
    return caught


def test_view_model_presents_outcome_once_check_finishes(configure_inject, manual_executor, make_spy) -> None:
    view_model = MpvqcVersionCheckMessageBoxViewModel()
    title_spy = make_spy(view_model.titleChanged)
    text_spy = make_spy(view_model.textChanged)

    assert not view_model.title
    assert not view_model.text

    manual_executor.drain()

    assert view_model.title == NEW_VERSION.title
    assert view_model.text == NEW_VERSION.text
    assert title_spy.size() == 1
    assert text_spy.size() == 1


def test_view_model_presents_cached_outcome_on_construction(configure_inject, manual_executor) -> None:
    MpvqcVersionCheckMessageBoxViewModel()
    manual_executor.drain()

    view_model = MpvqcVersionCheckMessageBoxViewModel()

    assert view_model.title == NEW_VERSION.title
    assert not manual_executor.pending


def test_view_model_notifies_with_settled_state(configure_inject, manual_executor) -> None:
    view_model = MpvqcVersionCheckMessageBoxViewModel()
    observed: list[tuple[object, object]] = []
    view_model.titleChanged.connect(lambda _: observed.append((view_model.title, view_model.text)))
    view_model.textChanged.connect(lambda _: observed.append((view_model.title, view_model.text)))

    manual_executor.drain()

    assert observed == [(NEW_VERSION.title, NEW_VERSION.text)] * 2


def test_destroying_view_model_mid_check_delivers_cleanly(
    configure_inject, checker, manual_executor, uncaught_exceptions
) -> None:
    outcomes: list[CheckOutcome] = []
    checker.outcome_ready.connect(outcomes.append)
    delete(MpvqcVersionCheckMessageBoxViewModel())

    manual_executor.drain()

    assert outcomes == [NewVersionAvailable(version="9.9.9")]
    assert uncaught_exceptions == []
