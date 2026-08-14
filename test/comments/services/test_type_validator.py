# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.comments.services import validate_new_comment_type


class ValidationCase(NamedTuple):
    name: str
    new_comment_type: str
    existing_comment_types: list[str]
    expected_error: str


@pytest.mark.parametrize(
    "case",
    [
        ValidationCase(
            name="a blank type is rejected",
            new_comment_type="",
            existing_comment_types=[],
            expected_error="A comment type must not be blank",
        ),
        ValidationCase(
            name="square brackets are rejected",
            new_comment_type="New Comment [Type",
            existing_comment_types=[],
            expected_error="Characters '[]' not allowed",
        ),
        ValidationCase(
            name="an existing type is rejected",
            new_comment_type="Translation",
            existing_comment_types=["Phrasing", "Note", "Translation"],
            expected_error="Comment type already exists",
        ),
        ValidationCase(
            name="a translation of an existing type is rejected",
            new_comment_type="Hinweis",
            existing_comment_types=["Phrasing", "Note", "Translation"],
            expected_error="Comment type already exists",
        ),
    ],
    ids=lambda case: case.name,
)
def test_validate_new_comment_type(case: ValidationCase):
    actual_error = validate_new_comment_type(case.new_comment_type, case.existing_comment_types)
    assert actual_error == case.expected_error
