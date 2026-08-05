# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from pathlib import Path

import pytest

from mpvqc.importing.domain import VideoSource
from mpvqc.importing.models import MpvqcImportVideosModel

CANDIDATES = (
    VideoSource(path=Path("/work/one.mp4"), found_in_document=True, found_in_subtitle=False),
    VideoSource(path=Path("/work/two.mp4"), found_in_document=False, found_in_subtitle=True),
)


@pytest.fixture
def make_model():
    def _make(videos: tuple[VideoSource, ...] = CANDIDATES) -> MpvqcImportVideosModel:
        return MpvqcImportVideosModel(videos)

    return _make


def test_the_skip_row_sits_after_the_candidates(make_model):
    model = make_model()

    assert model.rowCount() == 3
    assert model.data(model.index(2, 0), MpvqcImportVideosModel.IsNoVideoRole) is True
    assert not model.data(model.index(2, 0), MpvqcImportVideosModel.FilenameRole)
    assert not model.data(model.index(2, 0), MpvqcImportVideosModel.FullPathRole)
    assert model.data(model.index(2, 0), MpvqcImportVideosModel.FoundInDocumentRole) is False
    assert model.data(model.index(2, 0), MpvqcImportVideosModel.FoundInSubtitleRole) is False


def test_a_candidate_row_reports_itself_as_not_the_no_video_choice(make_model):
    model = make_model()

    assert model.data(model.index(0, 0), MpvqcImportVideosModel.IsNoVideoRole) is False
    assert model.data(model.index(0, 0), MpvqcImportVideosModel.FilenameRole) == "one.mp4"
    assert model.data(model.index(0, 0), MpvqcImportVideosModel.FullPathRole) == str(CANDIDATES[0].path)
    assert model.data(model.index(0, 0), MpvqcImportVideosModel.FoundInDocumentRole) is True
    assert model.data(model.index(0, 0), MpvqcImportVideosModel.FoundInSubtitleRole) is False


def test_the_skip_row_is_appended_even_with_no_candidates(make_model):
    model = make_model(())

    assert model.rowCount() == 1
    assert model.data(model.index(0, 0), MpvqcImportVideosModel.IsNoVideoRole) is True


def test_path_at_returns_a_candidates_path(make_model):
    model = make_model()

    assert model.path_at(0) == CANDIDATES[0].path
    assert model.path_at(1) == CANDIDATES[1].path


def test_path_at_the_skip_row_returns_none(make_model):
    model = make_model()

    assert model.path_at(2) is None


def test_path_at_outside_the_rows_returns_none(make_model):
    model = make_model()

    assert model.path_at(-1) is None
    assert model.path_at(3) is None
