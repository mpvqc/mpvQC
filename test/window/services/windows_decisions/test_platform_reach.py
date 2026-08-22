# SPDX-FileCopyrightText: mpvQC developers
#
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import ast
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[4] / "mpvqc" / "window" / "services" / "windows_decisions"


def _import_targets(module: Path) -> list[str]:
    # `from . import windows` names what it reaches in the imported name rather
    # than in the module, so the two are joined and the whole path is scanned.
    tree = ast.parse(module.read_text(encoding="utf-8"))
    return [
        alias.name if isinstance(node, ast.Import) else f"{node.module or ''}.{alias.name}"
        for node in ast.walk(tree)
        if isinstance(node, (ast.Import, ast.ImportFrom))
        for alias in node.names
    ]


def _reaches_a_platform(target: str) -> bool:
    parts = target.split(".")
    return "ctypes" in parts or "windows" in parts


def test_the_decisions_reach_nothing_platform_specific():
    # A module-level reach would already break these tests' own import off
    # Windows. The scan is what catches one hidden inside a function, where it
    # would run on Windows and raise everywhere else.
    modules = sorted(PACKAGE.rglob("*.py"))
    assert modules, f"the scan found no modules under {PACKAGE}"

    reaches = [
        (module.relative_to(PACKAGE).as_posix(), target) for module in modules for target in _import_targets(module)
    ]

    assert reaches, "the scan read no imports; it would pass on a package of empty modules"
    assert not [f"{module} imports {target}" for module, target in reaches if _reaches_a_platform(target)]
