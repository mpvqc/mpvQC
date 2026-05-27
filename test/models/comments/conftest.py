# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable
from typing import Protocol

import pytest

from mpvqc.datamodels import Comment
from mpvqc.models.comments import CommentsFacade

DEFAULT_COMMENTS: tuple[Comment, ...] = (
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=5, comment_type="commentType", comment="Word 2"),
    Comment(time=10, comment_type="commentType", comment="Word 3"),
    Comment(time=15, comment_type="commentType", comment="Word 4"),
    Comment(time=20, comment_type="commentType", comment="Word 5"),
)


class FacadeFactory(Protocol):
    def __call__(self, *, set_comments: Iterable[Comment]) -> CommentsFacade: ...


@pytest.fixture
def make_facade() -> FacadeFactory:
    def _make_facade(*, set_comments: Iterable[Comment]) -> CommentsFacade:
        facade = CommentsFacade()
        facade.import_comments(tuple(set_comments))
        return facade

    return _make_facade


@pytest.fixture
def default_comments() -> tuple[Comment, ...]:
    return DEFAULT_COMMENTS


@pytest.fixture
def comments(make_facade, default_comments) -> CommentsFacade:
    return make_facade(set_comments=default_comments)
