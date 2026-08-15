# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.shared import Comment


def test_reports_distinct_types_of_document(make_comments):
    comments = make_comments(
        set_comments=(
            Comment(time=0, comment_type="Phrasing", comment=""),
            Comment(time=5, comment_type="Spelling", comment=""),
            Comment(time=10, comment_type="Phrasing", comment=""),
        )
    )

    assert comments.distinct_comment_types == {"Phrasing", "Spelling"}


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda c: c.add_row(25, "added type"), id="add"),
        pytest.param(lambda c: c.update_comment(0, "edited text"), id="update-text"),
        pytest.param(lambda c: c.update_comment_type(0, "other type"), id="update-type"),
        pytest.param(lambda c: c.update_time(0, 99), id="update-time"),
        pytest.param(lambda c: c.remove_row(0), id="remove-sole-carrier"),
        pytest.param(lambda c: c.remove_row(1), id="remove-one-of-several-carriers"),
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
