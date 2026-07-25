# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import textwrap

import pytest
from set_build_info import determine_channel, render_build_info  # type: ignore[missing-import]

TEMPLATE = textwrap.dedent("""\
    [application]
    name = "mpvQC"
    version = ">>>tag<<<"             # CI replaces this
    commit = ">>>commit-id<<<"        # CI replaces this
    is_release = false                # CI replaces this
    channel = ""                      # CI replaces this. Empty means unofficial
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
    )

    assert 'version = "0.9.0"\n' in actual
    assert 'commit = "abcd1234"\n' in actual
    assert expected_line in actual


@pytest.mark.parametrize(
    ("channel", "expected_line"),
    [
        ("github-releases", 'channel = "github-releases"\n'),
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
        channel="github-releases",
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
        channel = "github-releases"

        [[dependency]]
        name = "inject"
        version = "5.5.0"                                      # Real version, updated by script
        platforms = ["linux", "win32"]                         # Match sys.platform values
    """)
    assert "".join(actual) == expected


@pytest.mark.parametrize(
    ("template", "missing"),
    [
        ('name = "mpvQC"\nversion = ">>>tag<<<"\n', r"\[application\]"),
        ('[application]\ncommit = ">>>commit-id<<<"\nis_release = false\nchannel = ""\n', "version"),
        ('[application]\nversion = ">>>tag<<<"\ncommit = ">>>commit-id<<<"\nis_release = false\n', "channel"),
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
        )


@pytest.mark.parametrize(
    ("env", "expected"),
    [
        ({}, ""),
        ({"MPVQC_BUILD_CHANNEL": "github-releases"}, "github-releases"),
    ],
)
def test_channel_comes_from_environment_and_defaults_to_empty(env, expected):
    assert determine_channel(env) == expected


def test_version_has_no_flatpak_suffix():
    actual = render_build_info(
        TEMPLATE.splitlines(keepends=True),
        tag="0.9.0",
        commit="abcd1234",
        is_release=True,
        channel="",
    )

    assert 'version = "0.9.0"\n' in actual
    assert "-flatpak" not in "".join(actual)
