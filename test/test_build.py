# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import NamedTuple

import pytest

from mpvqc.build import determine_build_origin, get_build_info

APP_ID = "io.github.mpvqc.mpvQC"


class BuildOriginCase(NamedTuple):
    name: str
    channel: str
    flatpak_id: str | None
    expected: str


class VersionLabelCase(NamedTuple):
    name: str
    is_release: bool
    origin: str
    expected: str


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
    "case",
    [
        BuildOriginCase(
            name="empty-channel",
            channel="",
            flatpak_id=None,
            expected="unofficial",
        ),
        BuildOriginCase(
            name="channel-set-outside-flatpak",
            channel="mpvqc-github",
            flatpak_id=None,
            expected="mpvqc-github",
        ),
        BuildOriginCase(
            name="channel-set-with-matching-id",
            channel="mpvqc-flatpak",
            flatpak_id=APP_ID,
            expected="mpvqc-flatpak",
        ),
        BuildOriginCase(
            name="mismatched-id",
            channel="mpvqc-flatpak",
            flatpak_id="com.example.Rebuild",
            expected="unofficial",
        ),
        BuildOriginCase(
            name="empty-flatpak-id",
            channel="mpvqc-flatpak",
            flatpak_id="",
            expected="unofficial",
        ),
    ],
    ids=lambda case: case.name,
)
def test_determine_build_origin(case: BuildOriginCase):
    assert determine_build_origin(case.channel, APP_ID, case.flatpak_id) == case.expected


@pytest.mark.parametrize(
    "case",
    [
        VersionLabelCase(
            name="release-channel",
            is_release=True,
            origin="mpvqc-github",
            expected="1.0.0 (abc12345) mpvqc-github",
        ),
        VersionLabelCase(
            name="release-unofficial",
            is_release=True,
            origin="unofficial",
            expected="1.0.0 (abc12345) unofficial",
        ),
        VersionLabelCase(
            name="dev-unofficial",
            is_release=False,
            origin="unofficial",
            expected="dev build (abc12345) unofficial",
        ),
        VersionLabelCase(
            name="dev-channel",
            is_release=False,
            origin="mpvqc-flatpak",
            expected="dev build (abc12345) mpvqc-flatpak",
        ),
    ],
    ids=lambda case: case.name,
)
def test_version_label(make_build_info, case: VersionLabelCase):
    assert make_build_info(is_release=case.is_release, origin=case.origin).version_label == case.expected
