# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.datamodels import Comment


def test_reports_distinct_types_of_document(make_comments):
    comments = make_comments(
        set_comments=(
            Comment(time=0, comment_type="Phrasing", comment=""),
            Comment(time=5, comment_type="Spelling", comment=""),
            Comment(time=10, comment_type="Phrasing", comment=""),
        )
    )

    assert comments.distinct_comment_types == {"Phrasing", "Spelling"}


def test_add_introduces_the_new_type(comments):
    comments.add_row(30, "Translation")

    assert comments.distinct_comment_types == {"commentType", "Translation"}


def test_removing_the_last_carrier_drops_the_type(comments):
    comments.add_row(30, "Translation")

    comments.remove_row(5)

    assert comments.distinct_comment_types == {"commentType"}


def test_type_carried_by_several_comments_survives_removing_one(comments):
    comments.remove_row(0)

    assert comments.distinct_comment_types == {"commentType"}


def test_type_edit_away_from_single_carrier_drops_old_type_and_undo_restores_it(comments):
    comments.add_row(30, "Translation")

    comments.update_comment_type(5, "Phrasing")
    assert comments.distinct_comment_types == {"commentType", "Phrasing"}

    comments.undo()
    assert comments.distinct_comment_types == {"commentType", "Translation"}


def test_import_undo_redo_track_the_imported_types(comments):
    comments.import_comments((Comment(time=99, comment_type="Translation", comment=""),))
    assert comments.distinct_comment_types == {"commentType", "Translation"}

    comments.undo()
    assert comments.distinct_comment_types == {"commentType"}

    comments.redo()
    assert comments.distinct_comment_types == {"commentType", "Translation"}


def test_reset_empties_the_set(comments):
    comments.reset()

    assert comments.distinct_comment_types == frozenset()


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda c: c.add_row(25, "added type"), id="add"),
        pytest.param(lambda c: c.update_comment(0, "edited text"), id="update-text"),
        pytest.param(lambda c: c.update_comment_type(0, "other type"), id="update-type"),
        pytest.param(lambda c: c.update_time(0, 99), id="update-time"),
        pytest.param(lambda c: c.remove_row(0), id="remove"),
        pytest.param(
            lambda c: c.import_comments((Comment(time=99, comment_type="imported type", comment=""),)),
            id="import",
        ),
        pytest.param(lambda c: c.reset(), id="reset"),
    ],
)
def test_property_equals_fresh_scan_after_every_mutation_kind(make_comments, mutate):
    comments = make_comments(
        set_comments=(
            Comment(time=0, comment_type="Spelling", comment="Word 1"),
            Comment(time=5, comment_type="Phrasing", comment="Word 2"),
            Comment(time=10, comment_type="Phrasing", comment="Word 3"),
        )
    )

    def fresh_scan():
        return frozenset(c.comment_type for c in comments.comments())

    mutate(comments)
    assert comments.distinct_comment_types == fresh_scan()

    comments.undo()
    assert comments.distinct_comment_types == fresh_scan()

    comments.redo()
    assert comments.distinct_comment_types == fresh_scan()
