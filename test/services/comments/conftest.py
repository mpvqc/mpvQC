# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterable
from typing import Protocol

import pytest

from mpvqc.datamodels import Comment
from mpvqc.services.comments import CommentsService

DEFAULT_COMMENTS: tuple[Comment, ...] = (
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=5, comment_type="commentType", comment="Word 2"),
    Comment(time=10, comment_type="commentType", comment="Word 3"),
    Comment(time=15, comment_type="commentType", comment="Word 4"),
    Comment(time=20, comment_type="commentType", comment="Word 5"),
)


class CommentsFactory(Protocol):
    def __call__(self, *, set_comments: Iterable[Comment]) -> CommentsService: ...


@pytest.fixture(autouse=True)
def configure_injections(common_bindings_with):
    common_bindings_with()


@pytest.fixture
def make_comments() -> CommentsFactory:
    def _make_comments(*, set_comments: Iterable[Comment]) -> CommentsService:
        service = CommentsService()
        service.import_comments(tuple(set_comments))
        return service

    return _make_comments


@pytest.fixture
def default_comments() -> tuple[Comment, ...]:
    return DEFAULT_COMMENTS


@pytest.fixture
def comments(make_comments, default_comments) -> CommentsService:
    return make_comments(set_comments=default_comments)
