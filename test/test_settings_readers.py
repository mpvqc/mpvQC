# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from enum import IntEnum

import pytest
from hypothesis import example, given
from hypothesis import strategies as st

from mpvqc.settings import read_bool, read_int, read_member


class Color(IntEnum):
    RED = 0
    GREEN = 1
    BLUE = 2


stored_values = st.one_of(
    st.text(),
    st.sampled_from(["true", "false", "TRUE", "False", "0", "1", "2", "-1", " 1 ", "1_000"]),
    st.from_regex(r"[+-]?\d+", fullmatch=True),
    st.integers(min_value=1, max_value=10_000).map(lambda length: "9" * length),
    st.integers(),
    st.integers(min_value=1, max_value=10_000).map(lambda length: 10**length),
    st.booleans(),
    st.floats(),
    st.none(),
    st.binary(),
    st.lists(st.text()),
    st.sampled_from(list(Color)),
    st.builds(object),
)


@pytest.mark.fuzz
@given(stored_values, st.booleans())
def test_read_bool_never_raises(stored: object, default: bool):
    assert type(read_bool(stored, lambda: default)) is bool


@pytest.mark.fuzz
@given(stored_values, st.integers())
@example(stored="9" * 5000, default=0)
@example(stored=Color.RED, default=0)
def test_read_int_never_raises(stored: object, default: int):
    assert type(read_int(stored, lambda: default)) is int


@pytest.mark.fuzz
@given(stored_values, st.sampled_from(list(Color)))
@example(stored="9" * 5000, default=Color.RED)
def test_read_member_never_raises(stored: object, default: Color):
    assert type(read_member(stored, Color, lambda: default)) is Color
