# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable
from typing import NamedTuple

import pytest

from mpvqc.comments.services import CommentsService
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


class MutationCase(NamedTuple):
    name: str
    mutate: Callable[[CommentsService], None]


@pytest.mark.parametrize(
    "case",
    [
        MutationCase(
            name="add",
            mutate=lambda c: c.add_row(25, "added type"),
        ),
        MutationCase(
            name="update-text",
            mutate=lambda c: c.update_comment(0, "edited text"),
        ),
        MutationCase(
            name="update-type",
            mutate=lambda c: c.update_comment_type(0, "other type"),
        ),
        MutationCase(
            name="update-time",
            mutate=lambda c: c.update_time(0, 99),
        ),
        MutationCase(
            name="remove-sole-carrier",
            mutate=lambda c: c.remove_row(0),
        ),
        MutationCase(
            name="remove-one-of-several-carriers",
            mutate=lambda c: c.remove_row(1),
        ),
        MutationCase(
            name="import",
            mutate=lambda c: c.import_comments((Comment(time=99, comment_type="imported type", comment=""),)),
        ),
        MutationCase(
            name="reset",
            mutate=lambda c: c.reset(),
        ),
    ],
    ids=lambda case: case.name,
)
def test_property_equals_fresh_scan_after_every_mutation_kind(make_comments, case: MutationCase):
    comments = make_comments(
        set_comments=(
            Comment(time=0, comment_type="Spelling", comment="Word 1"),
            Comment(time=5, comment_type="Phrasing", comment="Word 2"),
            Comment(time=10, comment_type="Phrasing", comment="Word 3"),
        )
    )

    def fresh_scan():
        return frozenset(c.comment_type for c in comments.comments())

    case.mutate(comments)
    assert comments.distinct_comment_types == fresh_scan()

    comments.undo()
    assert comments.distinct_comment_types == fresh_scan()

    comments.redo()
    assert comments.distinct_comment_types == fresh_scan()
