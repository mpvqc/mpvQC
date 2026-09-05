# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import pytest

from mpvqc.build import determine_build_origin, get_build_info

APP_ID = "io.github.mpvqc.mpvQC"


def test_get_build_info_reads_the_bundle():
    build = get_build_info()

    assert build.name == "mpvQC"
    assert build.organization == "mpvQC"
    assert build.domain == "mpvqc.github.io"
    assert build.version
    assert build.commit
    assert isinstance(build.is_release, bool)
    assert build.offers_update_check is False

    dependency_names = {dep.package for dep in build.dependencies}
    assert "PySide6-Essentials" in dependency_names
    assert "mpv" in dependency_names

    dev_dependency_names = {dep.package for dep in build.dev_dependencies}
    assert "pytest" in dev_dependency_names

    for dep in [*build.dependencies, *build.dev_dependencies]:
        assert dep.name
        assert dep.package
        assert dep.version
        assert dep.url
        assert dep.licence


@pytest.mark.parametrize(
    ("channel", "flatpak_id", "expected"),
    [
        pytest.param(
            "",
            None,
            "unofficial",
            id="empty-channel",
        ),
        pytest.param(
            "mpvqc-github",
            None,
            "mpvqc-github",
            id="channel-set-outside-flatpak",
        ),
        pytest.param(
            "mpvqc-flatpak",
            APP_ID,
            "mpvqc-flatpak",
            id="channel-set-with-matching-id",
        ),
        pytest.param(
            "mpvqc-flatpak",
            "com.example.Rebuild",
            "unofficial",
            id="mismatched-id",
        ),
        pytest.param(
            "mpvqc-flatpak",
            "",
            "unofficial",
            id="empty-flatpak-id",
        ),
    ],
)
def test_determine_build_origin(channel, flatpak_id, expected):
    assert determine_build_origin(channel, APP_ID, flatpak_id) == expected


@pytest.mark.parametrize(
    ("is_release", "origin", "expected"),
    [
        pytest.param(
            True,
            "mpvqc-github",
            "1.0.0 (abc12345) mpvqc-github",
            id="release-channel",
        ),
        pytest.param(
            True,
            "unofficial",
            "1.0.0 (abc12345) unofficial",
            id="release-unofficial",
        ),
        pytest.param(
            False,
            "unofficial",
            "dev build (abc12345) unofficial",
            id="dev-unofficial",
        ),
        pytest.param(
            False,
            "mpvqc-flatpak",
            "dev build (abc12345) mpvqc-flatpak",
            id="dev-channel",
        ),
    ],
)
def test_version_label(make_build_info, is_release: bool, origin: str, expected: str):
    assert make_build_info(is_release=is_release, origin=origin).version_label == expected
