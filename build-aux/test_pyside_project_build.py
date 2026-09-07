# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import hashlib
import inspect
from collections.abc import Callable
from typing import NamedTuple

import pyside_project_build  # type: ignore[missing-import]
import pytest


class SourcePinCase(NamedTuple):
    name: str
    func: Callable[..., object]
    pinned_hash: str


@pytest.mark.parametrize(
    ("name", "func", "pinned_hash"),
    [
        SourcePinCase(
            name="Project._qml_module_check",
            func=pyside_project_build.pyside_project.Project._qml_module_check,
            pinned_hash="0aec984c4c00256f274b2a7a123cc55dd503461d9f112f6d8430e75f93e0a613",
        ),
        SourcePinCase(
            name="Project.build",
            func=pyside_project_build.pyside_project.Project.build,
            pinned_hash="7642952562d17d841c337e4944a3cfca7a977ddd8b8a5e4308bbc5a8e61d3ad0",
        ),
        SourcePinCase(
            name="Project._regenerate_qmldir",
            func=pyside_project_build.pyside_project.Project._regenerate_qmldir,
            pinned_hash="3fe6797508f30f66e8c4e389c86ac4a7da31925d8a4c5f2b56e418b72b944618",
        ),
        SourcePinCase(
            name="check_qml_decorators",
            func=pyside_project_build.project_data.check_qml_decorators,
            pinned_hash="31d1377f384619cfb4be8efbad805ff4cb1e7524f3750823382c0c1187bc7a7a",
        ),
    ],
)
def test_upstream_source_unchanged(name, func, pinned_hash):
    """The build driver reimplements these PySide6 functions, so upstream edits drift silently.

    On failure: diff the upstream function against its counterpart in pyside_project_build.py,
    port any behavior change, then update the pinned hash.
    """
    actual = hashlib.sha256(inspect.getsource(func).encode()).hexdigest()
    assert actual == pinned_hash, (
        f"PySide6 changed {name}. Review the matching override in build-aux/pyside_project_build.py, "
        f"then update the pinned hash to {actual}."
    )
