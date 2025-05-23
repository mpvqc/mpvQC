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

import inject
import pytest

from mpvqc.services import CommentTypeValidatorService, ReverseTranslatorService


@pytest.fixture(scope="module")
def service() -> CommentTypeValidatorService:
    return CommentTypeValidatorService()


@pytest.fixture(autouse=True, scope="module")
def configure_injections():
    def config(binder: inject.Binder):
        binder.bind(ReverseTranslatorService, ReverseTranslatorService())

    inject.configure(config, clear=True)


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
