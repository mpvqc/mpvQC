# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import textwrap

import pytest
from set_build_info import (  # type: ignore[missing-import]
    determine_channel,
    determine_offers_update_check,
    render_build_info,
)

TEMPLATE = textwrap.dedent("""\
    [application]
    name = "mpvQC"
    version = ">>>tag<<<"             # CI replaces this
    commit = ">>>commit-id<<<"        # CI replaces this
    is_release = false                # CI replaces this
    channel = ""                      # CI replaces this. Empty means unofficial
    offers_update_check = false       # CI replaces this
""")


@pytest.mark.parametrize(
    ("is_release", "expected_line"),
    [
        (True, "is_release = true\n"),
        (False, "is_release = false\n"),
    ],
)
def test_replaces_tag_commit_and_is_release(is_release, expected_line):
    actual = render_build_info(
        TEMPLATE.splitlines(keepends=True),
        tag="0.9.0",
        commit="abcd1234",
        is_release=is_release,
        channel="",
        offers_update_check=False,
    )

    assert 'version = "0.9.0"\n' in actual
    assert 'commit = "abcd1234"\n' in actual
    assert expected_line in actual


@pytest.mark.parametrize(
    ("channel", "expected_line"),
    [
        ("mpvqc-github", 'channel = "mpvqc-github"\n'),
        ("mpvqc-flatpak", 'channel = "mpvqc-flatpak"\n'),
        ("", 'channel = ""\n'),
    ],
)
def test_stamps_channel_from_input(channel, expected_line):
    actual = render_build_info(
        TEMPLATE.splitlines(keepends=True),
        tag="0.9.0",
        commit="abcd1234",
        is_release=True,
        channel=channel,
        offers_update_check=False,
    )

    assert expected_line in actual


@pytest.mark.parametrize(
    ("offers_update_check", "expected_line"),
    [
        (True, "offers_update_check = true\n"),
        (False, "offers_update_check = false\n"),
    ],
)
def test_stamps_offers_update_check_from_input(offers_update_check, expected_line):
    actual = render_build_info(
        TEMPLATE.splitlines(keepends=True),
        tag="0.9.0",
        commit="abcd1234",
        is_release=True,
        channel="",
        offers_update_check=offers_update_check,
    )

    assert expected_line in actual


def test_preserves_formatting_and_leaves_other_sections_untouched():
    lines = textwrap.dedent("""\
        # SPDX-FileCopyrightText: mpvQC developers
        #
        # SPDX-License-Identifier: GPL-3.0-or-later

        [application]
        name = "mpvQC"
        app_id = "io.github.mpvqc.mpvQC"
        version = ">>>tag<<<"             # CI replaces this
        commit = ">>>commit-id<<<"        # CI replaces this
        is_release = false                # CI replaces this
        channel = ""                      # CI replaces this. Empty means unofficial
        offers_update_check = false       # CI replaces this

        [[dependency]]
        name = "inject"
        version = "5.5.0"                                      # Real version, updated by script
        platforms = ["linux", "win32"]                         # Match sys.platform values
    """)

    actual = render_build_info(
        lines.splitlines(keepends=True),
        tag="0.9.0",
        commit="abcd1234",
        is_release=True,
        channel="mpvqc-github",
        offers_update_check=True,
    )

    expected = textwrap.dedent("""\
        # SPDX-FileCopyrightText: mpvQC developers
        #
        # SPDX-License-Identifier: GPL-3.0-or-later

        [application]
        name = "mpvQC"
        app_id = "io.github.mpvqc.mpvQC"
        version = "0.9.0"
        commit = "abcd1234"
        is_release = true
        channel = "mpvqc-github"
        offers_update_check = true

        [[dependency]]
        name = "inject"
        version = "5.5.0"                                      # Real version, updated by script
        platforms = ["linux", "win32"]                         # Match sys.platform values
    """)
    assert "".join(actual) == expected


@pytest.mark.parametrize(
    ("template", "missing"),
    [
        (
            'name = "mpvQC"\nversion = ">>>tag<<<"\n',
            r"\[application\]",
        ),
        (
            '[application]\ncommit = ">>>commit-id<<<"\nis_release = false\nchannel = ""\noffers_update_check = false\n',
            "version",
        ),
        (
            '[application]\nversion = ">>>tag<<<"\ncommit = ">>>commit-id<<<"\nis_release = false\noffers_update_check = false\n',
            "channel",
        ),
        (
            '[application]\nversion = ">>>tag<<<"\ncommit = ">>>commit-id<<<"\nis_release = false\nchannel = ""\n',
            "offers_update_check",
        ),
    ],
)
def test_raises_on_incomplete_template(template, missing):
    with pytest.raises(KeyError, match=missing):
        render_build_info(
            template.splitlines(keepends=True),
            tag="0.9.0",
            commit="abcd1234",
            is_release=True,
            channel="",
            offers_update_check=False,
        )


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({}, ""),
        ({"MPVQC_BUILD_CHANNEL": "mpvqc-github"}, "mpvqc-github"),
    ],
)
def test_channel_comes_from_environment_and_defaults_to_empty(env, expected):
    assert determine_channel(env) == expected


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({}, False),
        ({"MPVQC_BUILD_OFFERS_UPDATE_CHECK": ""}, False),
        ({"MPVQC_BUILD_OFFERS_UPDATE_CHECK": "true"}, True),
    ],
)
def test_offers_update_check_comes_from_environment_and_defaults_to_false(env, expected):
    assert determine_offers_update_check(env) is expected


def test_version_has_no_flatpak_suffix():
    actual = render_build_info(
        TEMPLATE.splitlines(keepends=True),
        tag="0.9.0",
        commit="abcd1234",
        is_release=True,
        channel="",
        offers_update_check=False,
    )

    assert 'version = "0.9.0"\n' in actual
    assert "-flatpak" not in "".join(actual)
