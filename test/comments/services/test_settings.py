# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Callable

import pytest

from mpvqc.comments.services import CommentsSettingsService, default_comment_types

SHIPPED_TYPES = ["Translation", "Spelling", "Punctuation", "Phrasing", "Timing", "Typeset", "Note"]


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


def test_a_cleared_list_stays_empty_instead_of_restoring_the_defaults(comments_settings_service, ini_section):
    comments_settings_service.comment_types = []

    assert comments_settings_service.comment_types == []
    assert ini_section("Common")["commentTypes"] == "@Invalid()"


@pytest.mark.parametrize(
    ("stored", "expected"),
    [
        pytest.param("Translation, Phrasing", ["Translation", "Phrasing"], id="several"),
        pytest.param("Translation", ["Translation"], id="single"),
        pytest.param("@Invalid()", [], id="emptied"),
        pytest.param("", [""], id="empty-text"),
        pytest.param("Custom type", ["Custom type"], id="custom"),
    ],
)
def test_comment_types_stored_by_an_earlier_run_read_on(existing_settings_service, stored, expected):
    service = existing_settings_service(f"""
        [Common]
        commentTypes={stored}
    """)

    assert service.comment_types == expected


def test_missing_comment_types_return_a_fresh_default_list_on_each_read(
    comments_settings_service, settings_file, make_spy
):
    spy = make_spy(comments_settings_service.comment_types_changed)

    first = comments_settings_service.comment_types
    first.clear()
    assert comments_settings_service.comment_types == SHIPPED_TYPES

    comments_settings_service.comment_types = SHIPPED_TYPES.copy()
    assert not settings_file.qsettings.contains("Common/commentTypes")
    assert spy.count() == 0


@pytest.mark.parametrize(
    ("stored", "value"),
    [
        pytest.param("@Invalid()", [], id="emptied"),
        pytest.param("Custom", ["Custom"], id="custom"),
    ],
)
def test_equal_comment_types_preserve_earlier_run_encoding(read_existing_settings, make_spy, stored, value):
    store = read_existing_settings(f"[Common]\ncommentTypes={stored}\n")
    original = store.value("Common/commentTypes")
    service = CommentsSettingsService(store)
    spy = make_spy(service.comment_types_changed)

    service.comment_types = value

    assert store.contains("Common/commentTypes")
    assert store.value("Common/commentTypes") == original
    assert spy.count() == 0
