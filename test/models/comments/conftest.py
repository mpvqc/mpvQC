# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Iterable

import pytest

from mpvqc.datamodels import Comment
from mpvqc.models.comments import CommentsFacade


@pytest.fixture
def make_model() -> Callable[[Iterable[Comment]], CommentsFacade]:
    def _make_model(set_comments: Iterable[Comment]) -> CommentsFacade:
        # noinspection PyCallingNonCallable
        facade = CommentsFacade()
        facade.import_comments(tuple(set_comments))
        return facade

    return _make_model
