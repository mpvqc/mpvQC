# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QObject

from mpvqc.importing.domain import session
from mpvqc.importing.enums import MpvqcImportWizardSessionMode
from mpvqc.importing.viewmodels import build_session_step, resolve_session

SessionMode = MpvqcImportWizardSessionMode.SessionMode

UNRESOLVED = session.Unresolved(incoming_comment_count=3)


@pytest.fixture
def parent(qt_app):
    # Held for the whole test: the step is parented to it, and a collected parent takes the step with it.
    return QObject()


@pytest.fixture
def step(parent):
    step = build_session_step(parent, UNRESOLVED)
    assert step is not None
    return step


def test_build_session_step_only_for_unresolved_concern(parent):
    assert build_session_step(parent, UNRESOLVED) is not None
    assert build_session_step(parent, session.Merge()) is None
    assert build_session_step(parent, session.Replace()) is None


def test_defaults_to_merge(step):
    assert step.resolved == session.Merge()
    assert step.property("mode") == SessionMode.MERGE.value


def test_setting_mode_from_qml_resolves_to_the_domain_variant(step, make_spy):
    spy = make_spy(step.modeChanged)

    step.setProperty("mode", SessionMode.REPLACE.value)

    assert step.resolved == session.Replace()
    assert spy.count() == 1
    assert spy.at(0, 0) == SessionMode.REPLACE.value


def test_setting_the_domain_variant_updates_the_qml_mode(step, make_spy):
    spy = make_spy(step.modeChanged)

    step.resolved = session.Replace()

    assert step.property("mode") == SessionMode.REPLACE.value
    assert spy.count() == 1
    assert spy.at(0, 0) == SessionMode.REPLACE.value


def test_setting_the_same_mode_twice_stays_quiet(step, make_spy):
    spy = make_spy(step.modeChanged)

    step.setProperty("mode", SessionMode.MERGE.value)

    assert spy.count() == 0


def test_an_unknown_mode_leaves_the_step_untouched(step, make_spy):
    # Starts from Replace so a silent fall back to the Merge default cannot pass for "untouched"
    step.resolved = session.Replace()
    spy = make_spy(step.modeChanged)

    step.setProperty("mode", 99)

    assert step.resolved == session.Replace()
    assert spy.count() == 0


def test_resolve_session_reports_what_the_step_holds(step):
    step.resolved = session.Replace()

    assert resolve_session(step, UNRESOLVED) == session.Replace()
