# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest
from PySide6.QtCore import QObject, QStringListModel, Signal


class RecordedBase(QObject):
    inheritedChanged = Signal()


class Recorded(RecordedBase):
    firstChanged = Signal(int)
    secondChanged = Signal(str)


DECLARED_NAMES = "inheritedChanged, firstChanged, secondChanged"


@pytest.fixture(autouse=True)
def qt_app_must_be_running(qt_app):
    pass


def test_naming_what_fired_passes(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.firstChanged.emit(1)
    recorded.firstChanged.emit(2)
    recorded.secondChanged.emit("a")

    emissions.assert_exactly(firstChanged=2, secondChanged=1)


def test_a_fired_signal_left_unnamed_fails(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.firstChanged.emit(1)
    recorded.secondChanged.emit("a")

    with pytest.raises(AssertionError, match="did not emit exactly the expected signals"):
        emissions.assert_exactly(firstChanged=1)


def test_an_untouched_object_is_silent(record_emissions):
    emissions = record_emissions(Recorded())

    emissions.assert_silent()


def test_a_fired_signal_fails_silence(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.secondChanged.emit("a")

    with pytest.raises(AssertionError, match="did not emit exactly the expected signals"):
        emissions.assert_silent()


def test_a_wrong_count_fails(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.firstChanged.emit(1)

    with pytest.raises(AssertionError, match="did not emit exactly the expected signals"):
        emissions.assert_exactly(firstChanged=2)


def test_a_named_signal_that_stayed_silent_fails(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.firstChanged.emit(1)

    with pytest.raises(AssertionError, match="did not emit exactly the expected signals"):
        emissions.assert_exactly(firstChanged=1, secondChanged=1)


def test_an_explicit_zero_passes_when_silent(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.firstChanged.emit(1)

    emissions.assert_exactly(firstChanged=1, secondChanged=0)


def test_an_explicit_zero_fails_when_fired(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.secondChanged.emit("a")

    with pytest.raises(AssertionError, match="did not emit exactly the expected signals"):
        emissions.assert_exactly(secondChanged=0)


def test_asserting_consumes_nothing(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.firstChanged.emit(1)
    emissions.assert_exactly(firstChanged=1)
    recorded.firstChanged.emit(2)

    emissions.assert_exactly(firstChanged=2)


def test_emissions_before_construction_are_not_counted(record_emissions):
    recorded = Recorded()
    recorded.firstChanged.emit(1)
    emissions = record_emissions(recorded)

    recorded.firstChanged.emit(2)

    emissions.assert_exactly(firstChanged=1)


def test_a_signal_of_a_base_class_is_recorded(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.inheritedChanged.emit()

    emissions.assert_exactly(inheritedChanged=1)


@pytest.mark.parametrize("count", [0, 1])
def test_an_unknown_name_fails_and_lists_the_declared_names(record_emissions, count):
    emissions = record_emissions(Recorded())

    with pytest.raises(AssertionError, match=DECLARED_NAMES):
        emissions.assert_exactly(firstChange=count)


def test_reading_an_unknown_name_fails_and_lists_the_declared_names(record_emissions):
    emissions = record_emissions(Recorded())

    with pytest.raises(AssertionError, match=DECLARED_NAMES):
        emissions["firstChange"]


def test_object_name_changed_is_not_recorded(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.setObjectName("renamed")

    emissions.assert_silent()
    with pytest.raises(AssertionError, match=DECLARED_NAMES):
        emissions.assert_exactly(objectNameChanged=0)


def test_counts_and_payloads_read_through_the_index(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.secondChanged.emit("a")
    recorded.secondChanged.emit("b")

    assert emissions["secondChanged"].count() == 2
    assert emissions["secondChanged"].at(invocation=1, argument=0) == "b"


def test_an_object_without_signals_is_refused(record_emissions):
    with pytest.raises(TypeError, match="QObject declares no signal"):
        record_emissions(QObject())


def test_a_qt_model_is_refused(record_emissions):
    with pytest.raises(TypeError, match="QStringListModel declares two signals named dataChanged"):
        record_emissions(QStringListModel())


def test_a_failure_shows_the_class_and_both_fired_sets(record_emissions):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.firstChanged.emit(1)
    recorded.firstChanged.emit(2)
    recorded.secondChanged.emit("a")

    with pytest.raises(AssertionError) as failure:
        emissions.assert_exactly(firstChanged=1, inheritedChanged=0)

    assert str(failure.value) == (
        "Recorded did not emit exactly the expected signals\n"
        "expected: {'firstChanged': 1}\n"
        "recorded: {'firstChanged': 2, 'secondChanged': 1}"
    )
    assert failure.traceback.filter(failure)[-1].name == "test_a_failure_shows_the_class_and_both_fired_sets"


@pytest.mark.parametrize("application", ["first", "second"])
def test_signals_are_found_under_each_application(record_emissions, application):
    recorded = Recorded()
    emissions = record_emissions(recorded)

    recorded.inheritedChanged.emit()

    emissions.assert_exactly(inheritedChanged=1)
