# mpvQC
#
# Copyright (C) 2024 mpvQC developers
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from unittest.mock import MagicMock

import inject
import pytest

from mpvqc.models import Comment
from mpvqc.pyobjects.comment_model import MpvqcCommentModelPyObject, Role
from mpvqc.services import PlayerService

DEFAULT_COMMENTS = (
    Comment(time=0, comment_type="commentType", comment="Word 1"),
    Comment(time=5, comment_type="commentType", comment="Word 2"),
    Comment(time=10, comment_type="commentType", comment="Word 3"),
    Comment(time=15, comment_type="commentType", comment="Word 4"),
    Comment(time=20, comment_type="commentType", comment="Word 5"),
)


class SignalHelper:
    """Helper class to help with signal logging"""

    def __init__(self):
        self.signals_fired = {}

    def log(self, signal_name: str, val=True):
        self.signals_fired[signal_name] = val

    def has_logged(self, signal_name: str) -> bool:
        return signal_name in self.signals_fired


@pytest.fixture()
def signal_helper() -> SignalHelper:
    return SignalHelper()


def make_model(
    set_comments=DEFAULT_COMMENTS,
    set_player_time: int | float = 0,
) -> MpvqcCommentModelPyObject:
    # noinspection PyCallingNonCallable
    model: MpvqcCommentModelPyObject = MpvqcCommentModelPyObject()
    model.import_comments(set_comments)

    player_mock = MagicMock()
    player_mock.current_time = set_player_time

    def config(binder: inject.Binder):
        binder.bind(PlayerService, player_mock)

    inject.configure(config, clear=True)

    return model


def test_import_comments():
    model = make_model()
    # noinspection PyTypeChecker
    comment = Comment(time=999.99, comment_type="commentType", comment="Word 1")

    assert model.rowCount() == 5
    model.import_comments([comment])
    assert model.rowCount() == 6

    # Ensure even importing float time properties results in time being stored as int
    assert 999 == model.comments()[-1]["time"]


def test_import_comments_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.import_comments(list(DEFAULT_COMMENTS))

    assert model._searcher._hits is None


def test_import_comments_fires_signals(signal_helper):
    model = make_model()
    model.commentsImported.connect(lambda: signal_helper.log("commentsImported"))

    model.import_comments(list(DEFAULT_COMMENTS))

    assert signal_helper.has_logged("commentsImported")


def test_remove_comment():
    model = make_model()
    assert model.rowCount() == 5
    model.remove_row(0)
    assert model.rowCount() == 4


def test_remove_comment_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.remove_row(0)

    assert model._searcher._hits is None


def test_remove_comment_fires_signals(signal_helper):
    model = make_model()
    model.commentsChanged.connect(lambda: signal_helper.log("commentsChanged"))

    model.remove_row(0)

    assert signal_helper.has_logged("commentsChanged")


def test_clear_comments():
    model = make_model()
    model.clear_comments()
    assert 0 == model.rowCount()


def test_clear_comments_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.clear_comments()

    assert model._searcher._hits is None


def test_update_time_sorts_model_again():
    model = make_model()
    model.update_time(row=0, time=7)

    item = model.item(1, 0)
    actual = item.data(Role.COMMENT)

    assert actual == "Word 1"


def test_update_time_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.update_time(row=0, time=7)

    assert model._searcher._hits is None


def test_update_time_fires_signals(signal_helper):
    model = make_model()
    model.timeUpdated.connect(lambda: signal_helper.log("timeUpdated"))

    model.update_time(row=0, time=7)

    assert signal_helper.has_logged("timeUpdated")


def test_update_comment_invalidates_search_results():
    model = make_model()
    model._searcher._hits = ["result"]

    model.update_comment(index=0, comment="new")

    assert model._searcher._hits is None


def test_get_all_comments():
    model = make_model()

    actual = [
        Comment(time=comment["time"], comment_type=comment["commentType"], comment=comment["comment"])
        for comment in model.comments()
    ]

    assert actual == list(DEFAULT_COMMENTS)
