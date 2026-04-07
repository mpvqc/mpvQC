# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable, Iterable

import pytest

from mpvqc.datamodels import Comment
from mpvqc.models import MpvqcCommentModel


@pytest.fixture
def make_model() -> Callable[[Iterable[Comment]], MpvqcCommentModel]:
    def _make_model(
        set_comments: Iterable[Comment],
    ) -> MpvqcCommentModel:
        # noinspection PyCallingNonCallable
        model = MpvqcCommentModel()
        model.import_comments(tuple(set_comments))
        return model

    return _make_model
