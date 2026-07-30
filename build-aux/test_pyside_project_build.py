# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: MIT

import hashlib
import inspect

import pyside_project_build  # type: ignore[missing-import]
import pytest


@pytest.mark.parametrize(
    ("name", "func", "pinned_hash"),
    [
        (
            "Project._qml_module_check",
            pyside_project_build.pyside_project.Project._qml_module_check,
            "0aec984c4c00256f274b2a7a123cc55dd503461d9f112f6d8430e75f93e0a613",
        ),
        (
            "Project.build",
            pyside_project_build.pyside_project.Project.build,
            "7642952562d17d841c337e4944a3cfca7a977ddd8b8a5e4308bbc5a8e61d3ad0",
        ),
        (
            "Project._regenerate_qmldir",
            pyside_project_build.pyside_project.Project._regenerate_qmldir,
            "3fe6797508f30f66e8c4e389c86ac4a7da31925d8a4c5f2b56e418b72b944618",
        ),
        (
            "check_qml_decorators",
            pyside_project_build.project_data.check_qml_decorators,
            "31d1377f384619cfb4be8efbad805ff4cb1e7524f3750823382c0c1187bc7a7a",
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
