# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment

DEFAULT_COMMENTS = [
    Comment(time=0, comment_type="Translation", comment="First"),
    Comment(time=5, comment_type="Spelling", comment="Second"),
    Comment(time=10, comment_type="Phrasing", comment="Third"),
]


@pytest.fixture
def model(make_model):
    # noinspection PyArgumentList
    return make_model(set_comments=DEFAULT_COMMENTS)


def test_comment_at(model):
    assert model.comment_at(0) == DEFAULT_COMMENTS[0]
    assert model.comment_at(1) == DEFAULT_COMMENTS[1]
    assert model.comment_at(2) == DEFAULT_COMMENTS[2]


def test_comment_text_at(model):
    assert model.comment_text_at(0) == "First"
    assert model.comment_text_at(1) == "Second"
    assert model.comment_text_at(2) == "Third"


def test_retrieve_comments(model):
    assert list(model.retrieve_comments()) == DEFAULT_COMMENTS
