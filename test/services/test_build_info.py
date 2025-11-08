# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later
from unittest.mock import PropertyMock

import pytest

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


@pytest.mark.parametrize(
    ("is_release", "version", "commit", "expected"),
    [
        (True, "1.0.0", "abc12345", "1.0.0 - abc12345"),
        (False, "1.0.0", "abc12345", "dev build - abc12345"),
    ],
)
def test_combined_version_info(
    build_info_service: BuildInfoService,
    monkeypatch,
    is_release: bool,
    version: str,
    commit: str,
    expected: str,
):
    monkeypatch.setattr(type(build_info_service), "is_release", PropertyMock(return_value=is_release))
    monkeypatch.setattr(type(build_info_service), "version", PropertyMock(return_value=version))
    monkeypatch.setattr(type(build_info_service), "commit", PropertyMock(return_value=commit))

    assert build_info_service.combined_version_info == expected
