# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable

import pytest

from mpvqc.comments.services import CommentsSettingsService, default_comment_types


@pytest.fixture
def existing_settings_service(read_existing_settings) -> Callable[[str], CommentsSettingsService]:
    def read(content: str) -> CommentsSettingsService:
        return CommentsSettingsService(read_existing_settings(content))

    return read


def test_comment_types_default_to_the_shipped_types(comments_settings_service):
    assert comments_settings_service.comment_types == default_comment_types()


def test_comment_types_set_and_get(comments_settings_service):
    comments_settings_service.comment_types = ["Translation", "Phrasing"]

    assert comments_settings_service.comment_types == ["Translation", "Phrasing"]


def test_comment_types_signal_a_change(comments_settings_service, make_spy):
    spy = make_spy(comments_settings_service.comment_types_changed)

    comments_settings_service.comment_types = ["Translation"]
    assert spy.count() == 1
    assert spy.at(0, 0) == ["Translation"]

    comments_settings_service.comment_types = ["Translation"]
    assert spy.count() == 1


def test_comment_types_write_into_the_common_ini_section(comments_settings_service, ini_section):
    comments_settings_service.comment_types = ["Translation", "Phrasing"]

    assert ini_section("Common")["commentTypes"] == "Translation, Phrasing"


@pytest.mark.parametrize(
    ("stored", "expected"),
    [
        ("Translation, Phrasing", ["Translation", "Phrasing"]),
        ("Translation", ["Translation"]),
        ("@Invalid()", []),
    ],
    ids=["several", "single", "emptied"],
)
def test_comment_types_stored_by_an_earlier_run_read_on(existing_settings_service, stored, expected):
    service = existing_settings_service(f"""
        [Common]
        commentTypes={stored}
    """)

    assert service.comment_types == expected
