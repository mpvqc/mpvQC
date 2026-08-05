# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest

from mpvqc.importing.models import MpvqcImportSubtitlesModel

SUBTITLES = (
    Path("/work/one.srt"),
    Path("/work/two.srt"),
    Path("/work/three.srt"),
)


@pytest.fixture
def make_model():
    def _make(subtitles: tuple[Path, ...] = SUBTITLES) -> MpvqcImportSubtitlesModel:
        return MpvqcImportSubtitlesModel(subtitles)

    return _make


def test_subtitles_start_out_checked(make_model):
    model = make_model()

    assert model.rowCount() == 3
    assert model.checked_count == 3
    assert model.checked_paths == SUBTITLES


def test_subtitles_expose_their_filenames(make_model):
    model = make_model()

    filenames = [
        model.data(model.index(row, 0), MpvqcImportSubtitlesModel.FilenameRole) for row in range(model.rowCount())
    ]

    assert filenames == ["one.srt", "two.srt", "three.srt"]


def test_toggle_flips_the_row_alone_and_notifies_for_it(qt_app, make_model, make_spy):
    model = make_model()
    spy = make_spy(model.dataChanged)

    model.toggle(1)

    assert model.data(model.index(0, 0), MpvqcImportSubtitlesModel.IsCheckedRole) is True
    assert model.data(model.index(1, 0), MpvqcImportSubtitlesModel.IsCheckedRole) is False
    assert model.data(model.index(2, 0), MpvqcImportSubtitlesModel.IsCheckedRole) is True
    assert spy.count() == 1
    assert spy.at(0, 0).row() == 1
    assert spy.at(0, 1).row() == 1
    assert spy.at(0, 2) == [MpvqcImportSubtitlesModel.IsCheckedRole]


def test_toggle_twice_returns_the_row_to_checked(make_model):
    model = make_model()

    model.toggle(0)
    model.toggle(0)

    assert model.data(model.index(0, 0), MpvqcImportSubtitlesModel.IsCheckedRole) is True


def test_toggle_outside_the_rows_does_nothing(qt_app, make_model, make_spy):
    model = make_model()
    spy = make_spy(model.dataChanged)

    model.toggle(-1)
    model.toggle(3)

    assert model.checked_count == 3
    assert spy.count() == 0


def test_set_all_checked_false_unchecks_every_row(qt_app, make_model, make_spy):
    model = make_model()
    spy = make_spy(model.dataChanged)

    model.set_all_checked(False)

    assert model.checked_count == 0
    assert model.checked_paths == ()
    assert spy.count() == 1
    assert spy.at(0, 0).row() == 0
    assert spy.at(0, 1).row() == 2
    assert spy.at(0, 2) == [MpvqcImportSubtitlesModel.IsCheckedRole]


def test_set_all_checked_true_rechecks_every_row(qt_app, make_model, make_spy):
    model = make_model()
    model.set_all_checked(False)
    spy = make_spy(model.dataChanged)

    model.set_all_checked(True)

    assert model.checked_count == 3
    assert model.checked_paths == SUBTITLES
    assert spy.count() == 1
    assert spy.at(0, 2) == [MpvqcImportSubtitlesModel.IsCheckedRole]


def test_set_all_checked_on_an_empty_model_does_nothing(qt_app, make_model, make_spy):
    model = make_model(())
    spy = make_spy(model.dataChanged)

    model.set_all_checked(False)

    assert model.rowCount() == 0
    assert model.checked_count == 0
    assert model.checked_paths == ()
    assert spy.count() == 0


def test_checked_paths_only_include_checked_rows(make_model):
    model = make_model()

    model.toggle(1)

    assert model.checked_paths == (SUBTITLES[0], SUBTITLES[2])
    assert model.checked_count == 2
