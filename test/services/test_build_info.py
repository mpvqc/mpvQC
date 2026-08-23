# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

import inject
import pytest

from mpvqc.build import ApplicationInfo, BuildInfo
from mpvqc.services import BuildInfoService


@pytest.fixture
def build_info_service():
    return BuildInfoService()


def test_build_info(build_info_service):
    assert build_info_service.name == "mpvQC"
    assert build_info_service.organization == "mpvQC"
    assert build_info_service.domain == "mpvqc.github.io"
    assert build_info_service.version
    assert build_info_service.commit
    assert isinstance(build_info_service.is_release, bool)
    assert build_info_service.offers_update_check is False

    dependency_names = {dep.package for dep in build_info_service.dependencies}
    assert "PySide6-Essentials" in dependency_names
    assert "mpv" in dependency_names

    dev_dependency_names = {dep.package for dep in build_info_service.dev_dependencies}
    assert "pytest" in dev_dependency_names

    for dep in [*build_info_service.dependencies, *build_info_service.dev_dependencies]:
        assert dep.name
        assert dep.package
        assert dep.version
        assert dep.url
        assert dep.licence
        assert dep.platforms


def make_build_info(*, is_release: bool, origin: str, offers_update_check: bool = False) -> BuildInfo:
    return BuildInfo(
        application=ApplicationInfo(
            name="mpvQC",
            app_id="io.github.mpvqc.mpvQC",
            organization="mpvQC",
            domain="mpvqc.github.io",
            version="1.0.0",
            commit="abc12345",
            is_release=is_release,
            origin=origin,
            offers_update_check=offers_update_check,
        ),
        dependencies=(),
        dev_dependencies=(),
    )


@pytest.mark.parametrize("offers_update_check", [True, False])
def test_offers_update_check(build_info_service: BuildInfoService, offers_update_check: bool):
    # noinspection PyProtectedMember
    build_info_service._build_info = make_build_info(
        is_release=True,
        origin="mpvqc-github",
        offers_update_check=offers_update_check,
    )

    assert build_info_service.offers_update_check is offers_update_check


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
def test_version_info(build_info_service: BuildInfoService, is_release: bool, origin: str, expected: str):
    # noinspection PyProtectedMember
    build_info_service._build_info = make_build_info(is_release=is_release, origin=origin)

    assert build_info_service.version_info == expected
    assert build_info_service.full_version_info == f"mpvQC {expected}"


def test_instantiates_without_inject_container():
    inject.clear()

    service = BuildInfoService()

    assert service.name
    assert service.full_version_info.startswith(service.name)
