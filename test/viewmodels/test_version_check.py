# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple
from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.services import VersionCheckerService
from mpvqc.services.version_checker import CheckOutcome, NewVersionAvailable, ServerError, ServerNotReachable, UpToDate
from mpvqc.viewmodels.message_boxes.version_check import MpvqcVersionCheckMessageBoxViewModel, present_outcome


class PresentCase(NamedTuple):
    name: str
    outcome: CheckOutcome
    expected_title: str


PRESENT_CASES = [
    PresentCase(name="server error", outcome=ServerError(code=500), expected_title="Server Error"),
    PresentCase(name="server not reachable", outcome=ServerNotReachable(), expected_title="Server Not Reachable"),
    PresentCase(
        name="new version available",
        outcome=NewVersionAvailable(version="9.9.9"),
        expected_title="New Version Available",
    ),
    PresentCase(name="up to date", outcome=UpToDate(), expected_title="👌"),
]


@pytest.mark.parametrize("case", PRESENT_CASES, ids=lambda c: c.name)
def test_present_maps_outcome_to_title(case: PresentCase) -> None:
    title, text = present_outcome(case.outcome)

    assert title == case.expected_title
    assert text


def test_present_escapes_remote_version() -> None:
    _, text = present_outcome(NewVersionAvailable(version="1.2.3<script>"))

    assert "&lt;script&gt;" in text
    assert "1.2.3<script>" not in text


@pytest.fixture
def checker_mock() -> MagicMock:
    mock = MagicMock(spec_set=VersionCheckerService)
    mock.check_for_new_version.return_value = UpToDate()
    return mock


@pytest.fixture
def configure_inject(common_bindings_with, checker_mock) -> None:
    def custom_bindings(binder: inject.Binder):
        binder.bind(VersionCheckerService, checker_mock)

    common_bindings_with(custom_bindings)


def test_check_runs_in_background_and_applies_on_drain(qt_app, configure_inject, manual_executor) -> None:
    view_model = MpvqcVersionCheckMessageBoxViewModel(executor=manual_executor)

    assert not view_model.title
    assert not view_model.text

    manual_executor.drain()

    assert view_model.title == "👌"
    assert view_model.text
