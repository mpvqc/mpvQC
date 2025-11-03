# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.services import CommentTypeValidatorService


@pytest.fixture(scope="module")
def service() -> CommentTypeValidatorService:
    return CommentTypeValidatorService()


@pytest.fixture(autouse=True, scope="module")
def configure_injections(common_bindings_with):
    common_bindings_with()


@pytest.mark.parametrize(
    ("expected_error", "new_comment_type", "existing_comment_types"),
    [
        ("A comment type must not be blank", None, []),
        ("A comment type must not be blank", "", []),
        ("Characters '[]' not allowed", "New Comment [Type", []),
        ("Comment type already exists", "Translation", ["Phrasing", "Note", "Translation"]),
        ("Comment type already exists", "Hinweis", ["Phrasing", "Note", "Translation"]),
    ],
)
def test_validate_new_comment_type(
    expected_error: str,
    new_comment_type: str,
    existing_comment_types: list[str],
    service,
):
    actual_error = service.validate_new_comment_type(new_comment_type, existing_comment_types)
    assert actual_error == expected_error


@pytest.mark.parametrize(
    ("expected_error", "new_comment_type", "comment_type_being_edited", "existing_comment_types"),
    [
        ("A comment type must not be blank", None, "blub", []),
        ("A comment type must not be blank", "", "blub", []),
        ("Characters '[]' not allowed", "New Comment [Type", "blub", []),
        (None, "Translation", "Translation", ["Phrasing", "Note", "Translation"]),
        ("Comment type already exists", "Translation", "Note", ["Phrasing", "Note", "Translation"]),
        (None, "Hinweis", "Note", ["Phrasing", "Note", "Translation"]),
        ("Comment type already exists", "Hinweis", "Phrasing", ["Phrasing", "Note", "Translation"]),
    ],
)
def test_validate_editing_of_comment_type(
    expected_error: str,
    new_comment_type: str,
    comment_type_being_edited: str,
    existing_comment_types: list[str],
    service,
):
    actual_error = service.validate_editing_of_comment_type(
        new_comment_type, comment_type_being_edited, existing_comment_types
    )
    assert actual_error == expected_error
